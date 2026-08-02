# My Dish App (MDA) — App Intro for Interviews

Business-first intro, corrected deployment facts (Cloud Foundry primary, Rancher2/K8s migration in progress). Three lengths + cheat sheet.

---

## 30-second elevator pitch (non-technical)

> "My Dish App is DISH Network's mobile platform — how subscribers manage their whole account from their phone: pay bills, change programming, manage equipment, book service appointments, redeem rewards. It serves millions of subscribers across consumer and internal apps. Behind it are 18 Java microservices on Cloud Foundry, with a gateway layer that keeps the public internet separated from internal systems, and we're mid-migration to Kubernetes on Rancher2. I worked on [your part]."

---

## What the app does (functionality — grounded in the 50+ route inventory)

| Area | What the user does |
|------|--------------------|
| **Account** | View account details, certificates, account history |
| **Billing & payments** | Pay bill, manage payment methods, PayPal, statements, payment extensions |
| **Programming** | View current/proposed programming, options, autofill, review, modify, outdoor channels |
| **Equipment** | View, reactivate, review, modify, replace equipment |
| **Appointments & support** | Schedule/manage service appointments, support center |
| **Rewards & offers** | Refer-a-Friend, available offers |
| **Extras** | Internet usage, movie trailers, EST wallet/orders, 2FA, password/online-ID recovery, preferences |

One-liner: **"subscribers manage their entire DISH relationship from the app."**

---

## 2-minute structured version

**What it is.** MDA is DISH's mobile app ecosystem — consumer app on phone/TV/Wear, an internal employee gamification app ("Zombie"), and a dealer app (DPA). Users sign in, view bills, pay, manage equipment, book appointments, change programming, redeem offers.

**Who uses it.** DISH satellite TV subscribers (consumer), DISH dealers/retailers (DPA), DISH employees (internal gamification).

**How it's built (light touch).** 18 Java/Spring Boot microservices + 2 Android apps. Public traffic lands in a **DMZ layer** (auth gateway + API gateway), then crosses to an **internal layer** behind the firewall where a BFF (`My-Dish-App_Int`) talks to DISH's enterprise backend (20+ legacy SOAP services) and domain services (account, bill, equipment, location, push) handle specific concerns.

**Platform.** Cloud Foundry (PCF/TAS), 4 environments (dev → int → test → prod), ~30-35 instances at 1-4GB each. **Mid-migration to Rancher2/Kubernetes** — currently 2 services containerized (itma-employee, itma-iot-zombie).

**My contribution.** [Insert — only what you actually owned: gateway migration / auth token flow / Spring Boot 3 upgrade / DES events / caching / something else.]

**Outcome.** [e.g., unified gateway pattern across ITMA with enhanced security; platform modernizing from Java 8/Spring Boot 2 to Java 17-21/Spring Boot 3.]

---

## The one-diagram version

```
Mobile Apps ──► DMZ: itma-auth-server (OAuth2, 5 auth providers) + My-Dish-App_Svc (ProxyController, 50+ routes)
                     │
                     ▼
                INTERNAL: My-Dish-App_Int (BFF) ──► 20+ DISH SOAP services (billing, pricing, equipment...)
                     │          │
              domain services   └── GemFire cache + MongoDB/Oracle/MSSQL
              (account, bill, equipment, location, push)
                     │
                     ▼
              DES Event System (Kafka) — telemetry + business events
```

---

## Numbers cheat sheet (memorize 5-6)

| Fact | Value |
|---|---|
| Microservices | 18 Spring Boot (Java 17-21 mostly; mdaint legacy Java 8) |
| Android apps | 2 (consumer + internal "Zombie" gamification) |
| Gateway routes | 50+ in ProxyController |
| SOAP services wrapped | 20+ (billingMapper-v11/v15, PriceQuote, AccountManagement, NetQual…) |
| Auth | JWT HMAC-SHA256, access 20 min / refresh 90 days, 5 providers (Synacor, Okta, DISH API, LDAP, OAuth check) |
| Data | MongoDB (tokens), Oracle (push), MSSQL (HR/equipment), GemFire (cache + blacklist), H2 (dev) |
| **Platform** | **Cloud Foundry (PCF/TAS) primary — dev/int/test/prod; Rancher2/Kubernetes migration in progress (2 services containerized)** |
| Async | only DES events (Kafka) — everything else synchronous by design |
| Migration | CF → Rancher2/K8s; Boot 2→3; Java 8→21; Zuul→ProxyController; Hystrix→Resilience4j |

---

## When to go technical

- **Don't** lead with ProxyController, Resilience4j, GemFire in the opening — signals you can't abstract
- **Do** drill in when asked: gateway migration, auth flow, BFF/SOAP orchestration, "why not Kafka" (see `03-why-not-kafka.md`), DES internals (see `05-des-internals.md`)
