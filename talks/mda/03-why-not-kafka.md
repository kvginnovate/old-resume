# Why MDA Doesn't Use Kafka/RabbitMQ for Inter-Service Messaging

How to answer "why aren't you using Kafka?" in an interview — grounded in what the codebase actually shows, not hypotheticals.

---

## 1. The workload is request-response by nature

MDA is a **mobile backend** — user taps a button, expects an instant answer. Look at the endpoints:

```
Check token → immediate "is this valid?"
Get account → return account details
Pay bill → process payment, return result
Get equipment → return device list
```

Every flow is a synchronous user action. Adding a message queue between the mobile app and the service inserts latency and complexity with zero benefit — the response still has to come back *somehow*.

## 2. The async use case that *does* exist — already uses Kafka

There is exactly one genuinely async pattern: **telemetry and business events** (login events, page views, PPV purchases). And it's already Kafka-backed: the `itma-des-logger` service publishes to the **DES Event Service**, which is a Kafka-backed system. The architecture doc explicitly calls this out:

> **"Event Publishing (Fire-and-Forget) — DES Events published to DISH Event System (Kafka-backed)"** — `docs/07_INTEGRATION_LOGGING.md`

So the answer is: **they do use Kafka — for the one thing that needs it.** The decision is not "Kafka vs no Kafka," it's "what goes through Kafka." Telemetry is fire-and-forget, so Kafka is ideal. Business operations are synchronous, so REST is correct.

## 3. The SOA backend is already synchronous

MDA's backend is 20+ DISH SOAP services (PriceQuote, billingMapper, AccountManagement, etc.) — synchronous XML-over-HTTP services. Putting a message queue in front of them doesn't make them async — it just adds a buffer. The BFF pattern (`My-Dish-App_Int`) already handles orchestration: it calls multiple SOAP services in sequence and aggregates the results. That *is* the orchestration layer. Replacing it with Kafka would be:

- **Harder to debug** — a chain of Kafka topics is harder to trace than a single REST call stack
- **Harder to maintain** — consumer groups, offsets, poison messages, replay semantics
- **Not faster** — the SOAP services are still synchronous, so total latency is unchanged

## 4. The architecture doesn't need the problems Kafka solves

Kafka is typically used for:

- **Eventual consistency** — MDA doesn't need it. Every operation is strongly consistent by design (validate token → check account → return data).
- **Producer/consumer decoupling** — MDA's services are coupled by domain anyway: account, bill, equipment, preferences. They're separate because they have different data stores and change independently, not because they need to be async.
- **Load leveling** — at 30-35 instances with 2-4GB RAM each, the system isn't latency-sensitive enough to need a buffer. No throughput crisis in the docs.
- **Event sourcing / CQRS** — not used. The data model is simple CRUD (read from SOA, cache in GemFire, return to client).

## 5. The cost of adding it

18 services, each syncing configuration from Spring Cloud Config Server, deployed across Cloud Foundry → Rancher2/Kubernetes. Adding Kafka for inter-service messaging means:

- Consumer group management per service
- Serialization schemas (Avro/Protobuf or JSON)
- Dead-letter queues, retry logic, idempotency
- Monitoring Kafka lag alongside everything else
- Another infrastructure dependency (the team already manages MongoDB, Oracle, SQL Server, Geode, Cloud Foundry — and already *has* Kafka infrastructure via DES)

The team spent that complexity budget on the migration that matters: **Cloud Foundry → Kubernetes, Spring Boot 2.x → 3.x, Java 8 → 21, Hystrix → Resilience4j, Zuul → ProxyController.** That's the right call.

---

## The honest interview answer

> "MDA uses synchronous REST for all service-to-service calls because the workload is request-response by nature — a mobile app user tapping a button expects an immediate answer. The one genuinely async use case, telemetry and business events, is already Kafka-backed via the DES Event System. Adding Kafka for inter-service messaging would introduce consumer group management, ordering guarantees, and eventual consistency — all of which add complexity without solving a real problem. The team spent their complexity budget on the modernization that matters: migrating from Cloud Foundry to Kubernetes, Java 8 to 21, and legacy patterns (Zuul, Hystrix) to modern ones. That was the right tradeoff."

Defensible because it's exactly what the codebase shows: `docs/07_INTEGRATION_LOGGING.md` explicitly calls the DES pattern "Fire-and-Forget" and documents the Kafka-backed event publishing. The rest is synchronous REST.

---

## Where Kafka WOULD fit (if asked "what would you change?")

Be ready to name the cases that *would* justify a broker in MDA — shows you understand the tradeoff rather than defending the status quo:

1. **Billing event fan-out** — after a payment, multiple consumers (notifications, statements, DES) currently have to be called in sequence or fire-and-forget; a `payment.completed` topic would decouple them.
2. **Cross-service data propagation** — e.g., account changes currently require callers to invalidate GemFire regions manually; an `account.changed` event could drive cache invalidation.
3. **mdaint modernization** — the BFF (Java 8, Hystrix) is slated for refactor; a move to event-driven orchestration would be a candidate *if* the SOA layer were replaced with modern services that could consume events. It isn't — so it stays synchronous.

Frame it as: *"The moment a second consumer appears for a business event, or a service needs to react to another service's state change asynchronously, Kafka becomes the right call. Today, MDA has one consumer of events (DES/telemetry) and zero async business workflows, so the cost isn't justified."*
