# MDA — Interview Prep Docs

Deep-dive documentation of the **My Dish App (MDA)** microservice architecture, built from the source code in `C:/Projects/1_Research/5_mda`.

18 backend Java/Spring Boot microservices + 2 Android apps. DISH Network customer-facing mobile platform: account management, billing, equipment control, content access.

## Documents

| # | Doc | What it covers |
|---|-----|----------------|
| 1 | [01-microservice-patterns.md](01-microservice-patterns.md) | Full inventory of microservice design patterns used in MDA, with code evidence |
| 2 | [02-auth-flow-deep-dive.md](02-auth-flow-deep-dive.md) | End-to-end walkthrough: login → token issuance → token validation → logout (the strongest interview story) |
| 3 | [03-why-not-kafka.md](03-why-not-kafka.md) | How to answer "why aren't you using Kafka/RabbitMQ?" — grounded in the actual architecture |
| 4 | [04-bff-pattern.md](04-bff-pattern.md) | What the Backend-for-Frontend (BFF) pattern is, and how `My-Dish-App_Int` (mdaint) implements it |

## The one-paragraph summary

MDA is a synchronous, request-response mobile backend. Mobile apps hit a **DMZ gateway layer** (`itma-auth-server` for auth, `My-Dish-App_Svc` for API proxying) that forwards to an **internal service layer** — dominated by the **BFF** (`My-Dish-App_Int`), which orchestrates 20+ legacy DISH SOAP services into clean REST. Resilience comes from **circuit breakers** (Resilience4j modern / Hystrix legacy), **GemFire cache-aside** for hot data, and **GemFire blacklist regions** for instant token revocation. The only async path is **telemetry/events** (Kafka-backed DES Event Service) — everything else is synchronous by design, which is precisely why a service bus isn't needed.

## Key file references (source of truth)

- `docs/01_ARCHITECTURE_OVERVIEW.md` — architecture + service inventory
- `docs/04_DATA_ARCHITECTURE.md` — databases, GemFire regions, config
- `docs/07_INTEGRATION_LOGGING.md` — SOAP integrations, communication patterns, logging
- `Backend/itma-auth-server/src/main/java/com/dish/itma/server/auth/controller/UserAuthController.java`
- `Backend/itma-auth-server-int/src/main/java/com/dish/itma/server/authint/service/JwtTokenService.java`
- `Backend/itma-auth-server-int/src/main/java/com/dish/itma/server/authint/service/ItmaTokenServiceImpl.java`
- `Backend/itma-auth-server-int/src/main/java/com/dish/itma/server/authint/service/PersistTokenFilter.java`
- `Backend/itma-auth-server-int/src/main/java/com/dish/itma/server/authint/service/BlacklistTokenService.java`
- `Backend/itma-auth-server-int/src/main/java/com/dish/itma/server/authint/config/MdaUserDetailsService.java`
