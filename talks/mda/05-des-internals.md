# DES (DISH Event System) — Internal Working

How DES works end-to-end in the MDA codebase: producers → des-logger → routing → transformation → chunking → delivery → Kafka.

---

## The pipeline at a glance

```
Business service (mdaint / auth-server / auth-server-int)
   │  desUtils.desLogging("MDA_LOGIN", ...)          ← producer utility
   ▼
itma-des-logger  POST /v{version}/client/des-events  ← the only DES gateway
   │  CFT header routing: DPA/STBH/COMMON → CSA transaction log
   │  else (MDA) → DES system events
   ├─ data hygiene (backfill accountId/ip, base64-decode v2)
   ├─ group by event type → transform to DES Request payloads
   ├─ chunk (max 9/request) + fresh interactionId per chunk
   ▼
DES Event Service  (Kafka-backed)  /produce/{page-event|login-event|...}
```

---

## 1. Producer side — `desUtils.desLogging(...)`

Every business service builds a `DESEventsList` of `DESEvent` objects and fires them. Event types observed in source:

| Event | Where (evidence) |
|-------|------------------|
| `MDA_LOGIN` / `MDA_LOGOUT` | UserAuthController, ItmaAuthIntController (login/logout outcomes) |
| `MDA_PAYMENT`, `MDA_PAYMENT_TOKEN`, `MDA_PAYPAL_URL`, `MDA_PAYMENT_EXTENSION` | mdaint ExternalPaymentRestService, PaypalRestService, PaymentServiceImpl |
| `MDA_PPV_ORDER` | mdaint ClientProcessingEventsServiceImpl |
| `MDA_REQUEST_A_CALL` | mdaint AcqueonRestService |
| `MDA_FORGOT_PASSWORD`, `MDA_RESET_PASSWORD`, `MDA_FORGOT_ONLINEID`, `MDA_CREATE_ONLINEID`, `MDA_REGISTER_ONLINEID`, `MDA_VERIFYTOKEN`, `MDA_VERIFY_LAST4DIGIT`, `MDA_SEND_AUTHCODE` | mdaint TwoFactorUserManagementServiceImpl, UserIdServiceImpl, ForgotPasswordServiceImpl |
| `MDA_RAF` (Refer-a-Friend) | mdaint RAFRedemptionImpl |
| `MDA_GIFT_CARD` | mdaint GiftCardService |
| `MDA_RESTART` | mdaint ClientAccountsServiceImplV1 |
| `MDA_UPDATE_OFFERS` | mdaint ClientOffersServiceImpl |
| `MDA_DISH_OUTDOOR_MANAGE_LOCALS`, `MDA_DISH_OUTDOOR_PERFORM_ACCOUNT_HIT` | mdaint DishOutDoorSelfServiceImpl, AccountEquipmentService |
| `MDA_SCHEDULE_APPOINTMENT` | mdaint MDAtoCSAAppointment converter |

`DESEvent` fields: `eventName`, `accountId`, `interactionId`, `eventDateTime` (epoch seconds), `appVersion`, `ipAddress`, `languageIndicator`, `loginMethod`, `eventStatus`, device metadata.

## 2. The transport hop (producer → des-logger)

`mdaint`'s **`ItmaDesRestServiceImpl.postItmaDesPageEvent()`** posts the batch via `RestTemplate` to `itma-des-logger` — wrapped in a circuit breaker:

```java
// Backend/My-Dish-App_Int/.../webservice/ItmaDesRestServiceImpl.java:50
@HystrixCommand(fallbackMethod = "postItmaDesPageEventDefault")
public void postItmaDesPageEvent(String accountId, DESEventsList desEventsList) { ... }
```

**This is the fire-and-forget guarantee: DES being down never blocks a business request.** Same pattern elsewhere (`getEmptyLocation`, `postItmaDesPageEventDefault` fallbacks).

## 3. Ingestion + routing — `DESEventsController.postDESEvents()`

`POST /v{version}/client/des-events?accountId=...` — routes on the **`Customer-Facing-Tool` header** (`Backend/itma-des-logger/.../controller/DESEventsController.java`):

| CFT | Route | Destination |
|-----|-------|-------------|
| `DPA` / `STBH` / `COMMON` | `postDESEventsToCSA()` | `MdaDesLoggingService.logDpaDesTransaction(...)` → `csa-transaction-log-event` endpoint |
| anything else (MDA) | `postDESEvents()` | DES system endpoints |

The CSA route **field-remaps** the generic DESEvent into a fixed-position CSA transaction record — an ugly but necessary adapter:

| DESEvent field | Becomes (CSA) |
|----------------|---------------|
| `osType` | `returnCD`, `deviceName` |
| `deviceModel` | `deviceModel`, `pmtMethodType` |
| `interactionId` | `tranLogId` |
| `osVersion` | `tranType`, `osVersion` |
| `billingSystemId` | `svcAdd`, `agreementId` |
| `paymentMethod` | `svcRemove`, `oeNumber` |
| `afterUnlockMethod` | `fddAction`, `claimId` |
| `beforeUnlockMethod` | `orderId`, `onlineStatus` |
| `pageName` | `flowName` |
| `message` | `tranDesc` |
| `appVersion` | `productDesc` |
| `eventStatus` | `transactionStatus` |
| `videoEventId` / `videoEventType` | `currentServiceCode` / `pmtAmount` |

(`MDA_SOCIAL` events take a separate `postMDAEventsToCSA` path, checked first.)

## 4. Data hygiene (MDA path)

`postDESEvents()` normalizes before sending (`DESEventsServiceImpl.java`):

- **accountId** — if blank or not matching `\d{16}`, backfill from the `accountId` query param
- **ipAddress** — if blank / `"NA"` / `"null"` / `"No WiFi Address"` / `"0.0.0.0"`, backfill from the client IP header
- **v2+** — `pageName` and `ipAddress` arrive base64-encoded → `DesUtils.base64Decode()` both

## 5. Grouping + transformation — the strategy pattern

`getDesSystemEventFromDesClientEvent()`:

1. Groups incoming events by `DesEventNameType` → `EnumMap<DesEventNameType, DesSystemEvent>`
2. Builds one shared **`Context`** per batch: `customerFacingTool="ITMA_MYDISH_APP"`, `generatedTimeStamp` (ISO from the last event's epoch), `interactionId` (fresh UUID — deliberately NOT the session id), `sourceIpAddress`
3. Enriches from request headers: `osType`, `osVersion`, `deviceModel`
4. Picks a transformer per event type via switch:

| Event type | Transformer |
|-----------|-------------|
| `PAGE_LOAD` | `ClientEventToPageLoadPayload` |
| `APPLICATION_LOGIN_ATTEMPTED` | `ClientEventToLoginEventPayload` |
| `APPLICATION_INFO_UPDATED` | `ClientEventToApplicationInfoUpdatePayload` |
| `VIDEO_EVENT_PURCHASE_ATTEMPTED` | `ClientEventToVideoPurchasePayload` (+ `ppvEventsRestService` injected for enrichment) |
| `DPA_EVENT` / `STBH_EVENT` / `COMMON_EVENT` | `ClientEventToPageLoadPayload` |

Each `DESEvent` (MDA-shaped) becomes a `Request` payload shaped for the specific DES endpoint.

## 6. Chunking

```java
// DESEventsServiceImpl.java
private static final int MAX_NUM_EVENTS_CHUNK = 9;
List<List<Request>> smallerLists = ListUtils.partition(largeList, MAX_NUM_EVENTS_CHUNK);
```

Batches are partitioned into chunks of <10, and **each chunk gets a fresh unique `interactionId`** (DES treats interactionId as per-publish, not per-session).

## 7. Delivery — `DESSystemRestServiceImpl.sendToDES()`

URL mapping per event type (`getDesSystemUrl()`):

| Event type | Prod endpoint (`itma-des-logger-production.yml`) |
|-----------|---------------------------------------------------|
| `PAGE_LOAD` | `https://apps.global.dish.com/des-event-service/Events/v2/produce/page-event` |
| `APPLICATION_LOGIN_ATTEMPTED` | `.../produce/login-event` |
| `APPLICATION_INFO_UPDATED` | `.../produce/application-attribute-update-event` |
| `VIDEO_EVENT_PURCHASE_ATTEMPTED` | `.../produce/video-event-purchase-attempted` |
| IoT | `.../produce/iot-device-install-assist` |
| CSA | `.../produce/csa-transaction-log-event` |

(Int/dev use legacy direct middleware: `tvip-m1-mw-rt.dish.com/Events/v1/produce/...`)

POSTs the `DesSystemEvent` (context + request[]) as JSON with headers `INTERACTION_ID`, `REQUEST_ID`, `CUSTOMER_FACING_TOOL`, `CLIENT: itma-des-logger`. **Any exception is caught and logged — the event is dropped, the caller never sees a failure.** (A deprecated `sendToDESAsync` was replaced by sync calls since AsyncRestTemplate was removed in Boot 3.)

## 8. The tail — Kafka

The DES Event Service at `apps.global.dish.com/des-event-service` is the Kafka-backed ingestion layer. **MDA's code never touches Kafka directly** — it stops at the des-logger's REST call to `des-event-service`. That's the abstraction boundary: MDA services speak REST, DES owns the Kafka.

## 9. IoT side (separate controllers)

- `IoTInstallAssistController` / `IoTInstallAssistImagesController` — iot-device-install-assist events + image uploads
- `PPVEventsRestService` → mdaint `/v1/client/events` for PPV purchase events (backward path)

## Not to be confused with

- **Theia** (`itma-theia-logger`) — client *telemetry* (screen metrics, device stats), separate pipeline
- **Application logging** — Logstash JSON to stdout → ELK/Splunk

---

## Interview talking points

1. **Fire-and-forget by design** — `@HystrixCommand` fallback on the producer hop; swallowed exceptions at delivery. DES failure never blocks a business request.
2. **The gateway service owns DES protocol knowledge** — services just call `desUtils.desLogging()`; only des-logger knows endpoint URLs, payload shapes, chunking.
3. **The strategy pattern** — one client event model, per-type transformers into DES payloads.
4. **The CSA adapter** — field remapping shows how a modern service accommodates a legacy fixed-position contract.
5. **This is the only Kafka in MDA** — which is the answer to "why not Kafka for inter-service messaging" (see `03-why-not-kafka.md`).
