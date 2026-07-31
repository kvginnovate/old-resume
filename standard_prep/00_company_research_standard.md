# Company Research: The Standard (Insurance, Portland / Bengaluru)

> What The Standard does, their tech stack, insurance domain constraints, IBTE context, and why this role fits Chokkar's trajectory. Builds on the narrative hook from `00_sling_narrative_3min.md`.

---

## Company Overview

| Attribute | Detail |
|-----------|--------|
| Founded | 1906 (as Oregon Life Insurance Company), renamed Standard Insurance Company in 1946 |
| HQ | Portland, Oregon, USA |
| Parent | Meiji Yasuda (since 2016) — a Japanese mutual insurance group |
| Customers | 13+ million |
| Employees | ~4,400+ |
| Assets Under Administration | $108+ billion |
| India Offices | Bengaluru (Embassy Tech Village) — opened April 2026; Pune |

### What They Do

The Standard provides **workplace benefits** in the United States — insurance and financial products sold through employers, not directly to individuals:

- **Group Life Insurance** — term life, accidental death & dismemberment
- **Group Disability Insurance** — short-term and long-term disability income replacement
- **Retirement Plans** — 401(k) administration, pooled retirement assets, corporate benefit programs
- **Annuities & Investments** — fixed and variable annuities, investment products
- **Employer Voluntary Benefits** — supplemental coverage employees buy at work (Allstate EVB acquisition)

Their business model: employers choose The Standard as their benefits provider; employees receive coverage through their workplace. The company describes their differentiator as **service and empathy, not price**.

---

## The Bengaluru GCC & IBTE Rationale

The Bengaluru Global Capability Centre (GCC) opened in April 2026 at Embassy Tech Village. It is not a support outpost — it is a **direct extension** of the US IT organization:

> *"It's truly an extension of the IT organization over here, where our ways of working are the exact same, the tools we use are the same. The accountability to deliver the outcomes are shared across India and the US."* — Greg Chandler, CIO

**IBTE (Insurance Business Technology Enablement)** is The Standard's strategic platform initiative. The Bengaluru center is chartered to own it end-to-end: architecture, engineering, AI, and operational readiness. The role you're interviewing for — Principal Software Engineer V, IBTE — is a **founding architecture hire** for this center.

### Why IBTE Exists

1. **Modernize a 119-year-old technology estate.** The Standard has legacy systems built over decades. They need to migrate to cloud-native, event-driven architecture without disrupting 13 million customers.
2. **Acquisition integration.** The Standard grows through acquisition (Allstate EVB, others). Each acquisition brings its own systems. IBTE is building the integration playbook — API-led, event-driven, AI-accelerated.
3. **AI-driven underwriting and claims.** The CIO explicitly said: *"We want to solve the hardest problems of AI first and not go after flashy things like chatbots."* Their focus: group insurance underwriting (pricing risk across populations), claims recommendation engines, acquisition integration.
4. **BenTech ecosystem integration.** The Standard sells through brokers and benefits technology platforms. IBTE owns the API strategy for connecting with the broader benefits technology ecosystem.

---

## Tech Stack & Architecture (from Job Description)

| Layer | Technology | Candidate's Relevance |
|-------|-----------|----------------------|
| **Backend** | Java, Spring Boot 3, REST APIs | Core expertise — subscriber platform runs on this |
| **Messaging / Events** | Apache Kafka, Confluent Platform, Kafka Connect, Apache Flink | Deep Kafka experience from Sling TV and subscriber platform |
| **Cloud** | Microsoft Azure, AKS, Azure Networking | **Gap area** — needs study (see `00_azure_cheatsheet.md`, `00_study_plan.md`) |
| **API Gateway** | Kong / Kong Konnect | **New area** — study plan covers this |
| **Infrastructure** | Terraform, Docker, Kubernetes, Azure DevOps, GitHub, Maven | Medium overlap — Terraform for Azure is new |
| **Frontend** | React (awareness — not deep) | Has React experience from internal tools |
| **Databases** | SQL + NoSQL | Strong — query optimization, data access patterns |
| **Testing** | Selenium, JMeter, Gatling, Postman, SOAPUI | Has established CI gates and quality frameworks |

---

## Insurance Domain Constraints

This is a **regulated industry**. Every architecture decision must account for:

| Constraint | Implication |
|------------|-------------|
| **Compliance (NAIC, state insurance regulators)** | Systems must support regulatory audits, financial reporting, and state-by-state variation in insurance law |
| **Data privacy (HIPAA, state privacy laws)** | Health data in disability and life claims is protected. Encryption at rest/transit, access controls, data minimization |
| **Audit trails** | Every policy change, claim action, and premium adjustment must be logged immutably. Event sourcing on Kafka is a natural fit |
| **Data retention** | Insurance records retained for 7-10+ years (longer for death claims). Archival strategy needed |
| **Security** | Azure Key Vault, NSG, Private Link, Firewall — all called out in the JD. Zero-trust networking |
| **Operational readiness** | 99.9%+ uptime for claims processing. PagerDuty, runbooks, disaster recovery, multi-region failover |
| **Business continuity** | Insurance cannot stop. Claims must be processed even during outages. Kafka's replay capability is critical |

### Why Event-Driven Architecture Is Essential for Insurance

The JD emphasizes Kafka/Confluent. This is not accidental — insurance workflows are naturally event-driven:

- **Claims processing** — A claim event triggers: intake, validation, investigation, adjudication, payment, appeals. Each step is an asynchronous event. Saga pattern ensures consistency across steps without locking.
- **Policy management** — Policy issued, premium paid, beneficiary changed, policy lapsed, policy reinstated. Each event triggers downstream systems (billing, CRM, compliance reporting).
- **Underwriting workflows** — RFP received, data collected, risk assessed, quote generated, quote accepted. GenAI processes unstructured data (RFP documents, spreadsheets, emails) and publishes structured events for pricing models.
- **Acquisition integration** — When Allstate EVB is acquired, their systems must publish events into The Standard's platform. Kafka Connect ingests legacy data, Schema Registry ensures compatibility, and the event stream is replayed for historical migration.
- **Audit & replay** — Every insurance transaction needs an immutable log. Kafka's compaction and replay capability means you can reconstruct system state at any point in time — essential for regulatory audits.

---

## "Why The Standard" — 5 Talking Points

Use these when the interviewer asks why you want this role. They integrate with the narrative in `00_sling_narrative_3min.md`.

1. **"Founding architecture role at a new center."** The Bengaluru GCC opened in April 2026. This role is not backfill — it's a founding architecture hire shaping how IBTE is built from day one. I want to be the person who defines the patterns, not the person who inherits them.

2. **"Event-driven architecture at insurance scale."** Insurance workflows (claims, underwriting, policy management) are textbook event-driven domains. Kafka is not bolted on — it's the nervous system. That's exactly what I built at Dish with Kafka for subscriber event streams, and I want to double down on it at Principal level.

3. **"AI applied to hard problems, not chatbots."** The CIO said: *"We want to solve the hardest problems of AI first."* That matches my philosophy — I built AI agents that actually migrated code and diagnosed incidents, not demos. The Standard's focus on AI for underwriting and claims is the real thing.

4. **"Ten-year architecture horizon."** Insurance systems have a 30-year+ lifespan. The architecture decisions I make today will be running in production longer than I will be at the company. That's the kind of responsibility I'm looking for — not a two-year project, but a platform that outlasts me.

5. **"Service and empathy, not price."** The Standard competes on service quality, not being the cheapest. That means engineering investment in reliability, performance, and user experience is valued — it's not a cost center. My experience with 99.9% uptime, incident response, and operational excellence maps directly to that culture.

---

## Questions to Ask (About Platform Modernization)

1. **"The IBTE platform is modernizing a 119-year-old estate. How are you sequencing the migration — greenfield services alongside the monolith, strangler fig, or are there specific domains being carved out first?"**

   *Why this question:* Shows you've thought about the hardest part of legacy modernization — sequencing. Bridges to Sling TV story.

2. **"The job description mentions Apache Flink. What are the specific use cases you're targeting — real-time claims processing, fraud detection, or something else?"**

   *Why this question:* Flink is unusual to see in an insurance JD. This shows you noticed it and understand stream processing use cases in this domain.

3. **"How are you thinking about the organizational boundary between the India GCC and the US engineering teams? Is IBTE a fully autonomous team with its own product ownership, or is it integrated into US-led squads?"**

   *Why this question:* The CIO said the model is "shared accountability." This question shows you're thinking about the operating model, not just the tech — Principal-level concern.

---

## "Why Leave Dish?" — Honest Answer for This Role

> *Frame this as growth, not dissatisfaction. Do not complain about Dish.*

**The honest truth:** After 4 years at Dish with two consecutive Technical Excellence Awards, I've delivered significant impact — the subscriber platform, the Spring Boot 3 migration, the Sling TV modernization. But I've reached a ceiling in scope. Dish is a single-product company (Sling TV + Boost Mobile). The architecture decisions I make affect one platform.

**What I want next:** A Principal role where I drive technical strategy across multiple product lines — insurance, retirement, investments — each with its own domain complexity, regulatory constraints, and legacy systems. The Standard's IBTE initiative gives me that breadth. Additionally, the Bengaluru GCC is a greenfield opportunity to define architecture patterns from day one, not inherit them.

**Why The Standard specifically:** The insurance domain is a natural fit for event-driven architecture, and the CIO's vision for AI — solving real problems in underwriting and claims, not chatbots — aligns with what I've actually built and shipped. I could have joined any Bangalore GCC, but I chose The Standard because the technical challenge is real and the leadership is clear about what they want to build.

---

## Quick Facts for Interview Small Talk

| Fact | Why It Helps |
|------|-------------|
| Founded 1906 — 119-year-old company | Shows you did your homework |
| Meiji Yasuda (parent since 2016) | Shows you know the ownership structure |
| Greg Chandler is CIO and has a direct report in Bengaluru | Shows you read the news (ET CIO article, April 2026) |
| They compete on service and empathy, not price | Shows you understand their business model |
| Allstate EVB acquisition was the catalyst for the GCC | Shows you know their growth strategy |
| 13M+ customers, $108B+ in assets | Shows the scale you're signing up for |