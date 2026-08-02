# Microservice Design Patterns in MDA

Complete inventory, with source-code evidence. Grounded in `C:/Projects/1_Research/5_mda`.

---

## 1. API Gateway / Proxy Pattern

**Where:** `My-Dish-App_Svc` (mda), `itma-auth-server`, `itma-common-services` — all DMZ services

**Evolution:** Netflix Zuul (`@EnableZuulProxy`) → Spring Cloud Gateway → custom `ProxyController` (current)

```
Mobile App → ProxyController (50+ routes) → Internal Services
```

All three DMZ services use a `ProxyController` that forwards requests via `RestTemplate` to internal services. The proxy handles:
- Token transformation (`Mda token=` → `Bearer`)
- Path traversal prevention, XSS prevention
- Content-Type whitelist, security headers
- Connection pooling + timeout management

**Evidence:**
- `Backend/My-Dish-App_Svc/src/main/java/com/dish/itma/server/mdasvc/controller/ProxyController.java` — `@RestController` with 50+ `@RequestMapping` methods proxying to `external.base.url` (`https://apps-int.global.dish.com` in integration)
- `Backend/My-Dish-App_Svc/GATEWAY_MIGRATION_CHANGES.md` — "Spring Cloud Gateway → ProxyController, following itma-common-services proven architecture"
- `Backend/itma-auth-server/docs/gateway-mvc-removal-analysis.md` — Gateway MVC removed; ProxyController handles all 5 proxy endpoints

---

## 2. Backend for Frontend (BFF) Pattern

**Where:** `My-Dish-App_Int` (mdaint) — the heaviest service: 4GB × 4 instances

**Role:** Orchestrates calls to 20+ DISH enterprise SOAP services and aggregates them into REST responses for the mobile app. See [04-bff-pattern.md](04-bff-pattern.md) for the full treatment.

**Evidence:** `docs/01_ARCHITECTURE_OVERVIEW.md` — "BFF Pattern — mdaint aggregates/orchestrates calls to multiple SOA services"

---

## 3. Circuit Breaker Pattern

**Two implementations across the codebase:**

| Service | Implementation | Status |
|---------|---------------|--------|
| `itma-auth-server-int` | Resilience4j `@CircuitBreaker` | Modern |
| `itma-des-logger` | Spring Cloud Circuit Breaker (Resilience4j) | Modern |
| `My-Dish-App_Int` (mdaint) | Netflix Hystrix `@HystrixCommand` | Legacy (migration planned) |

**Evidence:**
- `Backend/itma-auth-server-int/src/main/java/com/dish/itma/server/authint/config/MdaUserDetailsService.java:56`
  ```java
  @CircuitBreaker(name = "accountService", fallbackMethod = "getDefaultAuthorities")
  public List<GrantedAuthority> getAuthoritiesFromAccount(String username) { ... }
  ```
- `Backend/My-Dish-App_Int/src/main/java/com/dish/itma/server/mdaint/service/EstOrdersServiceImpl.java:43`
  ```java
  @HystrixCommand(fallbackMethod = "fallbackESTOrdersExist", commandProperties = {
      @HystrixProperty(name = "execution.isolation.strategy", value = "SEMAPHORE") })
  ```
- `Backend/My-Dish-App_Int/.../webservice/ItmaDesRestServiceImpl.java:50` — `@HystrixCommand(fallbackMethod = "postItmaDesPageEventDefault")`
- `Backend/My-Dish-App_Int/.../webservice/ItmaLocationRestServiceImpl.java:50` — `@HystrixCommand(fallbackMethod = "getEmptyLocation")`

**Migration path (documented in `.kiro/specs/`):** `@HystrixCommand` → `@CircuitBreaker(name=..., fallbackMethod=...)`; `hystrix:` YAML → `resilience4j:` YAML. Behavioral note: thresholds differ between the two, so tuning is required.

---

## 4. Externalized Configuration (Config Server) Pattern

**Where:** `itma-config-server` (Spring Cloud Config Server, native filesystem backend)

```
All services → itma-config-server (port 8888) → Git-branched YAML
```

**Evidence:**
- `Backend/itma-config-server/src/main/java/itmaconfigserver/ItmaConfigserverApplication.java:8` — `@EnableConfigServer`
- `Backend/itma-config-server/src/main/resources/application.properties` — `spring.cloud.config.server.native.searchLocations=file:${user.home}/config_files/`
- Canary config pattern: `{service}-{env}.yml` files pinned to release versions, pushed to `dish_properties_canary` repo
- Environment files: `properties/{service}-integration.yml`, `{service}-test.yml`, `{service}-production.yml`

---

## 5. Cache-Aside Pattern

**Where:** Apache Geode / VMware GemFire — distributed cache regions shared across services

```
Service → check GemFire region → miss → load from SOA/DB → put in GemFire → return
```

| Region | Data | Service(s) |
|--------|------|-----------|
| AccountCache | Account data | itma-account, mdaint |
| BillCache | Billing data | itma-bill |
| EquipmentCache | Equipment data | itma-equipment |
| ItmaAccessTokenRevoke | Token blacklist | itma-auth-server-int |
| ItmaRefreshTokenRevoke | Refresh token blacklist | itma-auth-server-int |

**Evidence:**
- `Backend/My-Dish-App_Int/src/main/java/com/dish/itma/server/mdaint/dao/CMSAssetsDaoJdbcTemplateImpl.java` — manual cache-aside: `region.get(key)` → miss → load → `region.put(key, value)`, gated by `enableGemFireCaching` flag
- `getCacheableAccountDetails()` pattern used across mdaint controllers (AccountController, ClientAppointmentController, RestrictedEventsController, etc.)
- `Backend/My-Dish-App_Int/.../config/GemFireConfiguration.java` — `ClientCache` with locators + security; `GemFireServiceConfiguration` with `@EnableCaching`

---

## 6. SOAP Bridge / Adapter Pattern

**Where:** `My-Dish-App_Int` (mdaint), `itma-account`, `itma-bill`, `itma-equipment`, `itma-location`

```
REST API → Java Service → JAX-WS Stub → SOAP/XML → DISH Enterprise SOA
```

20+ SOAP services wrapped as REST: PriceQuoteService_v2, billingMapperService-v11/v15, AccountManagement-v13, AccountReinstatement-v6, AccountEquipment-v4, Equipment-v3, NetQual, ScrubAddress, PayCustomerBill-v5, ManageAppointments-v6, AccountStatement-v2, PayPerView-v4, AccountOrder-v13, OcsContacts-v1, CustomerBill-v5, ResourceEntitlement-v7, WebAccountManagement-v4, AccountAttributes-v4, ClubDish-v1, AccountContactInfoVerification-v6.

**Evidence:** `docs/07_INTEGRATION_LOGGING.md` — full table of WSDL services consumed via JAX-WS generated stubs (Maven `buildWsdls` profile). SOAP endpoints: `tvip-m1-mw-rt.dish.com` (primary), `pvip-mw-rt.global.dish.com` (secondary).

---

## 7. DMZ / Internal Network Segmentation

**Two-tier architecture with strict network zones:**

| Zone | Services | Visibility |
|------|---------|-----------|
| **DMZ** | mda, itma-auth-server, itma-common-services | `mobileapps.dish.com` |
| **Internal** | All other services | `apps-int.global.dish.com` |

Internal services are unreachable from the internet. Shared JWT secret (HMAC-SHA256) allows **zero-hop token validation** across internal services — every internal service can validate a token locally without calling back to the auth server.

**Evidence:** `docs/01_ARCHITECTURE_OVERVIEW.md` — "DMZ/Internal Split — Auth and API gateways in DMZ protect internal services"; "Shared JWT Secret — internal services share HMAC signing key for zero-hop token validation"

---

## 8. Fire-and-Forget / Event Publishing (Async Messaging)

**Where:** `itma-des-logger` → DES Event Service (Kafka-backed)

```
Service → itma-des-logger → DES Event Service (Kafka) → page-event, login-event, ...
```

**Evidence:** `docs/07_INTEGRATION_LOGGING.md` — "Event Publishing (Fire-and-Forget) — DES Events published to DISH Event System (Kafka-backed)". Event types: page-event, login-event, video-event-purchase-attempted, iot-device-install-assist, application-attribute-update-event, csa-transaction-log-event.

This is the **only** async inter-system path. Everything else is synchronous REST by design — see [03-why-not-kafka.md](03-why-not-kafka.md).

---

## 9. Polyglot Persistence

| Database | Purpose | Services |
|----------|---------|---------|
| MongoDB | Documents, tokens, user state | auth-server-int, itma-employee |
| Oracle | Relational, device registry | auth-server-int (PRM), itma-push |
| MS SQL Server | HR, equipment, sales | mdaint, itma-equipment, itma-employee |
| Apache Geode/GemFire | Distributed cache | account, bill, equipment, employee, auth-server-int |
| H2 | Dev/test (in-memory) | All services |

**Evidence:** `docs/04_DATA_ARCHITECTURE.md` — "Polyglot Persistence — different databases for different concerns (MongoDB for documents, Oracle for relational, GemFire for caching)"

---

## 10. Distributed Tracing (Correlation ID Propagation)

MDC context propagation via headers across service boundaries:

```
X-Correlation-Id, X-Request-Id, X-Account-Id, X-Device-Token, X-App-Version, X-Originating-Ip
```

All inter-service calls propagate standard headers via `RequestContextBuilder`. Logging: Logstash JSON encoder → stdout → PCF log drain → ELK/Splunk.

**Evidence:** `docs/07_INTEGRATION_LOGGING.md` §5-6

---

## 11. Multi-Provider Authentication

**Where:** `itma-auth-server` (DMZ), `itma-auth-server-int` (Internal)

```
Mobile App → itma-auth-server → itma-auth-server-int (JWT issuer)
               ├── Synacor (consumer identity)
               ├── Okta (enterprise SSO)
               ├── DISH API (internal)
               ├── LDAP (dealer/retailer)
               └── OAuth Token Check
```

- Token: JWT, HMAC-SHA256 (internal) / RSA-256 (DMZ)
- Access TTL ~20 min, refresh TTL 90 days (internal) / 30 days (DMZ)
- Token storage: MongoDB (`ITMA` db) + GemFire blacklist

**Evidence:** `Backend/itma-auth-server/src/main/java/com/dish/itma/server/auth/config/` — `SynacorCustomAuthenticationProvider`, `OktaCustomAuthenticationProvider`, `DishApiCustomAuthenticationProvider`, `LdapCustomAuthenticationProvider`, `CheckOAuthTokenAuthenticationProvider`

---

## 12. Strangler Fig Pattern (Active Migration)

Legacy components being incrementally replaced alongside the running system:

| Legacy | Replaced By | Status |
|--------|------------|--------|
| Netflix Zuul | ProxyController | Done |
| Spring Cloud Gateway | ProxyController | Done |
| Netflix Hystrix | Resilience4j | Done (auth-server-int, des-logger) / Pending (mdaint) |
| javax.* | jakarta.* (OpenRewrite) | In progress |
| Spring Boot 2.x / Java 8 | Spring Boot 3.4+ / Java 17/21 | In progress |
| Cloud Foundry | Rancher2/Kubernetes | In progress |
| spring-security-oauth2 | Spring Authorization Server | Done (auth-server-int) |

---

## What's NOT Used

Notable absent patterns:

- **Service Discovery** — no Eureka, Consul, or Kubernetes-native DNS. All URLs configured via Config Server. (Ribbon explicitly disabled: `ribbon.eureka.enabled=false`)
- **Client-Side Load Balancing** — no `@LoadBalanced` RestTemplate
- **Saga / Distributed Transactions** — no saga orchestrator or choreography; transactions are service-local
- **CQRS / Event Sourcing** — absent. DES events are fire-and-forget, not sourced state
- **SEDA / Event-Driven Architecture** — absent. Service-to-service is synchronous REST
- **Message Queue as service bus** — Kafka used only by DES event system, not inter-service messaging

---

## TL;DR for interviews

MDA = **synchronous request-response mobile backend** with a **DMZ gateway layer**, a **BFF orchestrator** over 20+ legacy SOAP services, **circuit breakers + cache-aside** for resilience, and **Kafka reserved for telemetry only**. Its complexity budget goes into the modernization (Boot 2→3, Java 8→21, CF→K8s, Zuul/Hystrix→ProxyController/Resilience4j), not into async infrastructure the workload doesn't need.
