# BFF (Backend for Frontend) Pattern — Explained with MDA

## The concept

A **Backend for Frontend** is a dedicated service that sits **between the mobile app and the downstream backend systems**, existing *specifically to serve that one frontend*. Instead of the app calling 20 different backend systems directly, it calls **one** service that:

- **Orchestrates** — calls multiple downstream services (SOAP, REST) in the right order
- **Aggregates** — combines several responses into one payload shaped exactly for the app's screens
- **Translates** — converts legacy formats (SOAP/XML) into clean REST/JSON
- **Hides complexity** — the app never knows the enterprise backend exists

**Key difference from an API Gateway:** a gateway routes *and forwards* (thin); a BFF *transforms and composes* (thick — it contains business logic about how to assemble the response).

## In MDA: `My-Dish-App_Int` (mdaint)

The doc calls it out explicitly:

> `docs/01_ARCHITECTURE_OVERVIEW.md` — **"BFF Pattern — mdaint aggregates/orchestrates calls to multiple SOA services"**

```
Mobile App → itma-auth-server (auth)
           → My-Dish-App_Svc  (mda, DMZ gateway — thin proxy)
                              ↓ forwards
           → My-Dish-App_Int  (mdaint, BFF — the thick one)
                              ↓ orchestrates + aggregates
              ┌─────────────────┬──────────────────┬──────────────────┐
              ▼                 ▼                  ▼                  ▼
         billingMapper    PriceQuote      AccountManagement    PayCustomerBill
         (SOAP v11/v15)   (SOAP v2)       (SOAP v13)           (SOAP v5)
              └─────────────────┴──────────────────┴──────────────────┘
                       20+ DISH enterprise SOAP services
```

**Concrete example from the code** — one mdaint endpoint pulling multiple backend concerns together. `ClientAppointmentController.scheduleAppointment()` (`ClientAppointmentController.java:309`):

```java
Account account = itmaAccountService.getCacheableAccountDetails(accountId, ...);
//  ↑ account lookup → SOA AccountManagement service + GemFire cache-aside

OrderStatus status = clientAppointmentService.scheduleAppointment(accountId, appointment, account, ...);
//  ↑ appointment booking → SOA ManageAppointments-v6, reusing the account object
```

One REST endpoint → validates the account through one downstream chain, books the appointment through another, and returns a single `OrderStatus` JSON to the app. The app made **one** call; the BFF made **multiple** behind the scenes.

Every `getCacheableAccountDetails()` call across mdaint controllers is the same pattern: the BFF is the only place that knows *how* to get an account (which SOAP service, which cache region, what fallback) — so the mobile app and the thin `mda` gateway never do.

## Why mdaint is the BFF and mda is not

| | `My-Dish-App_Svc` (mda) | `My-Dish-App_Int` (mdaint) |
|---|---|---|
| Role | DMZ **gateway** | Internal **BFF** |
| Behavior | Forwards 50+ routes, token transform, security checks | Orchestrates SOAP calls, aggregates, caches, applies business rules |
| What it knows | URL of mdaint (`external.base.url`) | 20+ WSDL endpoints, SOAP contracts, GemFire regions |
| Thickness | Thin (proxy) | Thick (composition logic) |

## Why the BFF answers the Kafka question

The BFF is exactly the piece that makes a message queue unnecessary: **mdaint *is* the orchestration layer, and it's synchronous by design.** A user tapping "schedule appointment" needs the answer *now* — the BFF blocks on SOAP calls, aggregates, returns. Kafka would replace this synchronous composition with async choreography (fire an event, hope a consumer picks it up, poll for the result) — strictly harder to debug and trace, for zero user-visible benefit. The one async concern (telemetry) is already on Kafka via DES.

> Interview line: *"MDA's BFF, mdaint, already solves the composition problem synchronously. Kafka solves a different problem — decoupling producers from consumers in time — which MDA's request-response workload doesn't have."*

## Honest caveat — the BFF is the legacy hotspot

mdaint is the **legacy** service (Spring Boot 2.7, Java 8, Hystrix, JAX-WS SOAP stubs). The strategic assessment (`docs/09_STRATEGIC_ASSESSMENT_CTO_RESPONSE.md`) recommends refactoring or retiring it. Be ready to say:

> *"The BFF is right for the current SOA world — it's the only sane way to expose 20 synchronous SOAP services to a mobile app. It's also the top modernization candidate precisely because it concentrates all the orchestration complexity in one place: 6-9 months of work to move it off Java 8."*

## Related patterns the BFF relies on

- **SOAP Bridge** — the BFF wraps legacy SOAP/XML as REST (`JAX-WS` generated stubs, Maven `buildWsdls` profile)
- **Cache-Aside** — `getCacheableAccountDetails()` checks GemFire before hitting SOA, caches on miss
- **Circuit Breaker** — Hystrix `@HystrixCommand(fallbackMethod=...)` on every external SOA call, returning safe defaults (empty location, default video, etc.) when the enterprise backend is down
