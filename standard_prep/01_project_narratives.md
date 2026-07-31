# Project Narratives — Principal Engineer Interview Prep

> **14 project stories at Principal altitude.** Each is self-contained (use in any order). Each follows: Problem → Approach → Outcome → Principal Signal → Bridge → Watchpoints.
>
> **What changes at Principal level:** Every answer must show org-wide influence, business metrics, stakeholder management, and strategic thinking — not just technical execution.

---

## How to Use This Document

| Section | How to Use |
|---------|-----------|
| **Headline** | 5-second hook. Say this when they ask "tell me about a project" |
| **Problem** | The business context that made this worth doing |
| **What I Did** | Strategy, decisions, influencing — the 80% they care about |
| **Outcome** | Business metrics + org impact — lead with the number |
| **Principal Signal** | The meta-lesson: what this proves about your scope |
| **Bridge** | How to connect this story to the interviewer's company |
| **Watchpoints** | Prepare for these follow-ups before telling the story |

---

## Contents

| # | Project | Rehearse Priority | Principal Signal |
|---|---------|------------------|-----------------|
| 1 | My Dish Subscriber Platform | **P0** | Owned architecture for 10M+ users end-to-end |
| 2 | Spring Boot 3 Migration | **P0** | AI + org-wide strategy = compressed 18mo→5mo |
| 3 | Sling TV Modernization | **P0** | 80 APIs → Java microservices, DDD, Saga pattern |
| 4 | Custom AI Agent Skills & MCP Servers | **P0** | Built practice adopted by 5+ teams org-wide |
| 5 | DPA (ColdFusion → Spring Boot) | **P1** | 23 integrations, 7 SFTP targets, offline-first |
| 6 | STB Health Monitor | **P1** | 10M devices, DMZ security, certificate rotation |
| 7 | Field Catalogue (Offline-First Android) | **P1** | 100% offline → 60% sales increase |
| 8 | DISH App Store | **P1** | Internal distribution platform, serverless |
| 9 | Asset Management (Hackathon → Company-Wide) | **P1** | 48hr hackathon → company-wide adoption |
| 10 | Shift Allowance (Company-Wide HR Tool) | **P1** | Automated manual Excel → every employee uses it |
| 11 | Kiro Mobile (Dish Ignite 2026) | **P2** | Mobile AI agent monitoring, showcased to VPs |
| 12 | Pivot3 VMware HCI | **P2** | Enterprise full-stack, client-facing |
| 13 | Enterprise Mobile & Mobitaz Automation | **P2** | Shipped Android apps, built framework from scratch |
| 14 | GCP + Firebase MCP — Zero-Touch Auto-Provisioning POC | **P2** | AI agent provisions GCP/Firebase from spec in 5 min |

---

> **Project 14 is documented separately at `14_gcp_firebase_mcp_poc.md`**

---

# Project 1: My Dish Subscriber Platform

## Headline
*"I own the architecture for Dish's flagship subscriber platform — 10M+ users, 99.9% uptime, sub-second latency — and defined the integration patterns, security gates, and observability framework that every platform team follows."*

## The Problem (Business Context)
Dish's subscriber platform — My Dish — is the primary interface for 10+ million customers to manage accounts, billing, plans, and equipment. When it's slow, customers call support. When it breaks, revenue is impacted. The platform was a collection of services built by different teams with different patterns — no shared API standards, no consistent observability, no common security posture. Adding a new feature required understanding the unique pattern of each service. The business needed to ship faster, but the "integration tax" was growing with every new service.

## What I Did (Strategy, Not Just Code)
Four decisions, each at the architecture/org level:

**1. API-first + shared contract repository.** I mandated that every service publish an OpenAPI spec before writing code. All specs live in one version-controlled repository. Breaking changes require a new API version and a documented migration plan. This eliminated the "integration by Slack message" pattern.

**2. Three integration patterns, not ten.** Backend-to-backend: REST + circuit breakers for sync, Kafka for async. Frontend-to-backend: API Gateway + BFF (Backend for Frontend) layer that aggregates microservice responses into view models. Shared services: a common library for auth validation, logging, and Dynatrace instrumentation. Teams stopped inventing their own approaches.

**3. Observability as a requirement, not an afterthought.** Every service must emit metrics, structured logs, and distributed traces. Dynatrace traces every request across service boundaries. The mandate wasn't "use Dynatrace" — it was "your service is not production-ready without observable output." This is what enabled 2-minute incident diagnosis later.

**4. Security gates in CI/CD, not in review.** Snyk scans every build. Vulnerabilities are triaged by exploitability: critical = same-day, high = this sprint, medium = backlog, low = accept risk. No service deploys without passing scan.

## The Outcome
- Platform serves **10M+ subscribers** at **99.9% uptime** with **sub-second API latency**
- New services ship with consistent patterns — no more "integration tax"
- Incident diagnosis: **30 minutes → 2 minutes** (Dynatrace distributed tracing)
- Vulnerability fix time: **days → hours** (Snyk CI gate)
- **Technical Excellence Award** (2024) for establishing the engineering practice

## Principal Signal
*I don't just build systems — I build the patterns that scale across teams. The platform's reliability isn't luck; it's designed in at the architecture level with gates that enforce it automatically.*

## Bridge to Any Company
*"Your platform likely has the same challenges Dish had — multiple services, inconsistent patterns, growing integration cost. I would: audit the current integration patterns, identify the top 3 pain points across teams, define the patterns that eliminate those pain points, and make them self-service so teams adopt them without being forced."*

## Watchpoints
| Question | Your Anchor |
|----------|------------|
| "How do you measure 99.9% uptime?" | "Dynatrace — request-based SLI. Three 9s = 8.7 hours of downtime/year. We track against this monthly in the architecture review." |
| "What breaks at 10M users?" | "Database connection pools under load. GemFire cache misses during peak. We solved the first with HikariCP tuning, the second with pre-warming." |
| "How did you get teams to adopt your patterns?" | "I didn't mandate — I made them self-service. Shared library, documented playbooks, office hours. After the first team saved time, others followed." |
| "What would you do differently?" | "I'd invest in contract testing earlier. OpenAPI specs defined the contracts, but we didn't automatically verify that implementations matched until later." |

---

# Project 2: Spring Boot 3 Migration

## Headline
*"I led the org-wide Spring Boot 2-to-3 migration across 12 services — 50K+ lines of code — using AI to compress 18 months of work into 5 months. The data convinced leadership to scale the approach org-wide. I was promoted to Staff Engineer as a result."*

## The Problem (Business Context)
Spring Boot 2 reached end-of-life. Every week Dish stayed on 2, the security team filed CVE tickets. New features were blocked because dependencies couldn't upgrade past Boot 2. The team estimated 18 months of manual migration across 12 services — 50K+ lines of code. That timeline meant an entire year of stalled feature delivery. The business couldn't wait that long.

## What I Did (Strategy, Not Just Code)

**1. I didn't ask for permission — I built the first one.** Rather than write a proposal and wait for approval, I picked the simplest service and ran the migration myself using AI. I showed the working result at the architecture guild meeting with hard numbers: 3 days instead of 2 weeks, 85% test coverage, zero production incidents. That's what got buy-in.

**2. I made the playbook, not the pipeline.** The AI workflow I built was a structured playbook: (a) feed the service codebase into Kiro with a migration spec, (b) the agent identifies all Boot 2 patterns that break in 3, (c) it executes the migration, (d) it regenerates tests, (e) human reviews. I documented every step so other teams could self-serve.

**3. I built a dashboard for leadership visibility.** A React app pulling from GitLab + Kiro output showing: lines changed by AI vs manually, test pass rate, time saved per service, defect rate. This wasn't a vanity metric — it was the data that convinced the VP to scale the approach. After 3 pilot services, the remaining 9 went through in ~3 weeks.

**4. I measured the right thing.** Not "AI wrote X lines." The metric was: *time-to-migrate per service, before and after AI.* That's a business metric. A mid-size service went from 2 weeks to 3 days — that's what 60% productivity gain means in terms an exec cares about.

## The Outcome
- **18-month estimate → 5-month delivery** across all 12 platform services
- **60% productivity gain** per service (2 weeks → 3 days)
- **Promoted from Lead to Staff Engineer** — the promotion documented this work as the reason
- **Technical Excellence Award (2024)**
- Unblocked quarterly feature releases that had been stalled for 6 months
- Security patches went from "weeks to ship" to same-day

## Principal Signal
*I don't wait for permission to solve big problems. I built the reference implementation, showed the data, and let results drive adoption. The promotion was a lagging indicator — the real impact was org-wide velocity improvement.*

## Bridge to Any Company
*"You probably have a similar migration story — EOL framework, stalled releases, growing security risk. My approach scales to any tech stack: (1) automate the mechanical parts, (2) measure the impact, (3) build the playbook so others self-serve, (4) show leadership the data that proves the approach."*

## Watchpoints
| Question | Your Anchor |
|----------|------------|
| "How did you handle Hibernate 5→6 queries that didn't migrate cleanly?" | "We flagged them for human review. Dynamic queries with criteria API didn't translate well. The agent flagged these — not silent failures." |
| "What if the AI introduced bugs?" | "Two safeguards: (1) test coverage gate — tests had to pass against both old and new code, (2) human review of the security config — that's where the risk was." |
| "Why not just assign 12 engineers for 18 months?" | "That would have stopped feature delivery for a year. The business couldn't accept that. AI-compressed migration kept feature work running in parallel." |
| "60% productivity gain — how exactly?" | "Before: senior engineer, 2 weeks, manual code changes + test updates. After: AI agent, 3 days, human review. Measured across 12 services, consistent." |

---

# Project 3: Sling TV Modernization

## Headline
*"I led the transformation of Sling TV from 80+ legacy Ruby on Rails APIs into modern Java microservices — using AI to reverse-engineer 400K lines of undocumented code and deliver in 5 months instead of 18. The key wasn't the AI — it was knowing which architectural decisions to make so the AI could accelerate without creating chaos."*

## The Problem (Business Context)
Sling TV's backend was 80+ Ruby on Rails APIs — 400K lines of code, zero documentation, tightly coupled. A change in billing could break content delivery. Adding a feature took weeks because you had to understand the entire codebase before touching anything. The business needed to ship streaming features faster to compete with rivals like YouTube TV and Hulu Live. The traditional estimate: 18 months, 12 engineers, full rewrite.

## What I Did (Strategy, Not Just Code)

**1. I chose what NOT to reverse-engineer.** Rather than try to understand every line (impossible for 400K lines of undocumented Ruby), I focused on the API surface — what endpoints exist, what they accept, what they return. Amazon Q ingested models, controllers, routes, and database schemas to generate OpenAPI specs. The business logic inside callbacks and unless/until conditionals was flagged for human review.

**2. DDD bounded contexts were the key decision.** I grouped 80+ APIs into bounded contexts — billing, content catalog, entitlements, recommendations — using domain-driven design workshops with the product team. Each context became its own independent Spring Boot microservice with its own data store. This decision determined the architecture quality more than any code the AI generated.

**3. The migration strategy was incremental, not Big Bang.** Per bounded context: (a) AI generated skeleton + tests, (b) I reviewed business logic translation (Ruby callbacks → Spring events), (c) ran old and new in parallel for 2 weeks, (d) API Gateway routed traffic via feature flags — 10% to new, then 50/50, then 100%, (e) Dynatrace traced every request across both systems, (f) data reconciliation job compared responses hourly.

**4. I solved the hardest problem first — data consistency.** Splitting a monolith's database into per-service databases means losing ACID transactions. We solved this with the Saga pattern on Kafka: each service publishes an event when its local transaction completes, downstream services listen and update their own state, compensation logic rolls back on failure. We tested this with chaos engineering before going live.

## The Outcome
- **5 months delivery vs 18 months estimated** — compressed 3 quarters into 1
- **70% productivity gain** per engineer (a service that took 2 weeks now takes 3 days)
- **400K lines reverse-engineered, 2M+ lines of Java scaffolded, 10K+ unit tests at 85% coverage**
- Fewer production bugs than the original Rails code — AI-generated code followed the spec precisely
- **Technical Excellence Award (2025)**
- Feature delivery velocity increased — what took weeks now takes days

## Principal Signal
*I know that in large migrations, the critical decisions aren't technical — they're strategic. Where to start, what to reverse-engineer vs. rewrite, how to sequence the migration, how to maintain business continuity, and how to handle the data consistency problem that every monolith-split faces.*

## Bridge to Any Company
*"If you have legacy systems that are blocking velocity, the playbook is: (1) reverse-engineer the surface before touching internals, (2) identify bounded contexts using DDD, (3) migrate one domain at a time with feature flags, (4) solve data consistency before code migration — Saga pattern is usually the answer, (5) measure every phase so you know if you're accelerating or just adding risk."*

## Watchpoints
| Question | Your Anchor |
|----------|------------|
| "What were Amazon Q's limitations?" | "Ruby metaprogramming produced awkward Java. Rails callbacks needed human interpretation. Test assertions were sometimes tautological. Performance-critical paths needed manual optimization. AI handled the 80% mechanical work; humans did the 20% domain-critical work." |
| "How did you verify 10K+ AI-generated tests?" | "We ran tests against the legacy system — tests had to pass old AND new code. Any test that only passed against new code was flagged as potentially incorrect. Manual review on critical paths." |
| "What was the biggest risk that materialized?" | "Data consistency during the split — but we anticipated it. The Saga pattern with compensation logic handled it. We tested with chaos engineering before cutover." |
| "How did you sequence the migration across 80 APIs?" | "By dependency graph. Billing first (least dependencies, highest business criticality), then content catalog, then entitlements, then everything else. Each domain was a 2-week parallel-run cycle." |

---

# Project 4: Custom AI Agent Skills & MCP Server Ecosystem

## Headline
*"I built custom AI agent skills that autonomously fix defects and vulnerabilities — wired to MCP servers for Dynatrace, Snyk, GitLab, and Jira. What started as my experiment on one team is now used across 5+ engineering teams. It was showcased at Dish Ignite 2026."*

## The Problem (Business Context)
Dish had AI coding tools, but they were used individually — an engineer here, an engineer there. There was no standardized way to use AI for repeatable workflows: fix a bug, remediate a vulnerability, diagnose an incident. Each engineer figured it out themselves. The result: inconsistent quality, no governance, no way to measure impact. Meanwhile, the incident diagnosis took 30 minutes, vulnerability fixes took 2-7 days, and bug fixes were unpredictable.

## What I Did (Strategy, Not Just Code)

**1. I built the first skill — defect lifecycle automation.** A 5-phase playbook: Phase 1 — agent reads the bug from Jira via MCP, identifies the affected service, searches codebase via GitLab MCP. Phase 2 — checks out branch, runs test suite for baseline, reproduces the issue. Phase 3 — implements the fix following team patterns. Phase 4 — validates by running tests and Snyk rescan, max 3 iterations before escalating. Phase 5 — creates PR tagged as AI-generated with full description.

**2. I defined the security boundary before anyone asked.** Every MCP server has scoped permissions: GitLab MCP can read code and create PRs but never merge. Dynatrace MCP can read traces but never modify monitoring. Snyk MCP can read vulnerabilities but never dismiss findings. This boundary is what made autonomous agents viable in a corporate environment. When security asked "what stops an agent from deleting production data?" I had the answer ready.

**3. I didn't pitch — I paired.** Rather than sending a presentation, I invited one senior engineer from another team to shadow our process for a week. They saw the real workflow, the time saved, the defects caught. Then I held open office hours — 2 hours every Friday, any team could bring their specific problem. Within 3 months, 5+ teams were using the agent skills.

**4. I made it customizable, not prescriptive.** The first version was too rigid — fixed 5-phase workflow. Teams had different needs. I redesigned it as a configurable playbook where teams could customize phases, approval gates, and notification preferences. That's when adoption took off.

## The Outcome
- **Incident diagnosis: 30 minutes → 2 minutes** (Dynatrace MCP)
- **Vulnerability fix: 2-7 days → same-day** (Snyk MCP + agent)
- **5+ engineering teams actively using the agent skills**
- MCP servers became the standard way to integrate AI workflows with Dish's tooling
- **Dish Ignite 2026 showcase** — live demo of agent fixing a bug from Jira
- Playbook approach adopted by the platform team as the template for all internal tooling

## Principal Signal
*I don't just build tools — I build practices that scale across teams. The architecture decision wasn't the code; it was the security model, the customization framework, and the adoption strategy that got 5 teams to use something I built on my own time.*

## Bridge to Any Company
*"Every engineering org has repeatable workflows that consume engineer hours: bug fixing, vulnerability remediation, incident diagnosis. The question is: how do you make AI agents safe enough to run autonomously? I've already solved that at Dish — the MCP security model, the playbook architecture, the adoption playbook. I can bring that framework to your company in weeks, not months."*

## Watchpoints
| Question | Your Anchor |
|----------|------------|
| "What stops an agent from making a destructive change?" | "Three layers: (1) MCP permissions — agents read-only for Dynatrace, write-PR but never merge for GitLab. (2) Playbook gates — agent stops before destructive operations and escalates to human. (3) Code review — every AI-generated PR needs human approval." |
| "How did you measure impact?" | "Time from alert to diagnosis (30 min → 2 min for Dynatrace), time from vulnerability report to fix PR (days → hours), time from Jira bug assignment to fix PR (unpredictable → one session)." |
| "What if the agent creates a wrong fix?" | "Happened in early version — agent patched the test instead of the bug. Fixed by: (a) tests must pass against old and new code, (b) human reviews every AI-generated test assertion, (c) max 3 iterations before escalating." |
| "How did you get 5 teams to adopt?" | "Paired with one early adopter, held open office hours, made it configurable, shared wins. Never forced it. Peer adoption is stronger than any mandate." |

---

# Project 5: Dish Paperless Agreement (DPA) — ColdFusion to Spring Boot

## Headline
*"I migrated Dish's paperless customer onboarding system from ColdFusion to Spring Boot microservices — handling 23 downstream integrations, 7 SFTP distribution targets, and offline field agent operation. The migration was completed without a single day of downtime."*

## The Problem (Business Context)
Dish's Paperless Agreement system was the backbone of customer onboarding — field agents used it to sign agreements, cross-sell services, and activate equipment. It ran on ColdFusion, a legacy Adobe technology from the early 2000s. ColdFusion is tag-based, mixing HTML and server-side logic in the same file. It was impossible to hire engineers for it, hard to debug, and every deployment was a risk. The system also had to work offline — field agents work in basements and rural areas with no signal.

## What I Did

**1. I reverse-engineered the business logic from ColdFusion pages.** ColdFusion mixes HTML and server logic — you can't just "read the code." I extracted business rules page by page, documented them, and designed a proper Spring Boot layered architecture (controller → service → repository).

**2. The integration orchestration layer was the key architecture decision.** 23 downstream integrations, each with different contracts: XML, JSON, CSV, fixed-width formats. Different delivery mechanisms: SFTP, REST, SOAP. Different schedules: real-time, hourly, daily. I designed a Spring Batch-based orchestration layer that managed retries, dead-letter queues, and monitoring for each integration. Adding a new integration became a config change, not a code change.

**3. Offline capability was non-negotiable.** Field agents sign agreements in basements with no signal. The mobile app caches agreements locally (SQLite), collects the signature, and queues it. When connectivity returns, the app syncs — uploads signed agreements, downloads new assignments. Conflict resolution: server is authoritative for agreement state, device is authoritative for captured signatures. The signature itself was captured as encrypted bitmap data locally, reconstructed as PDF on the backend.

## The Outcome
- **Zero downtime migration** — ColdFusion system ran in parallel until cutover was validated
- **23 active integrations** — all monitored by Dynatrace, with automated retry and dead-letter handling
- **CPAW Award** for delivery impact
- Field agents can sign agreements in any connectivity condition
- New integrations added as config changes, not code changes

## Principal Signal
*Complex integrations aren't a technical problem — they're a design problem. A configurable orchestration layer with monitoring, retries, and dead-letter queues makes any integration manageable. The architecture decision that mattered most was: "make each integration a config entry, not a code path."*

## Bridge
*"If your company has a legacy system that (a) runs on an unmaintainable tech stack, (b) has dozens of integrations, and (c) must never go down — the DPA playbook works: reverse-engineer the surface, build an orchestration layer that makes integrations configurable, run parallel until cutover is validated."*

## Watchpoints
| Question | Your Anchor |
|----------|------------|
| "23 integrations — how did you test them all?" | "Integration test suite per target. Dynatrace synthetic monitoring on every integration path. Data reconciliation job comparing old vs new system outputs hourly." |
| "What was the hardest integration?" | "The 7 SFTP targets — each with different file formats, schedules, and delivery confirmations. The generic SFTP client service handled this with per-target configuration." |
| "How did you handle offline signature capture?" | "Encrypted bitmap locally, reconstructed on backend. The signature PDF was assembled server-side after sync." |

---

# Project 6: STB Health Monitor

## Headline
*"I built the STB Health Monitor — a system that ingests telemetry from 10M+ set-top boxes through a DMZ gateway with JWT authentication, automated certificate rotation, and Dynatrace monitoring. Zero manual certificate management at 10M device scale."*

## The Problem (Business Context)
Dish has 10M+ set-top boxes deployed across subscriber homes. Field technicians needed to scan QR codes on devices, run health diagnostics, and upload telemetry. The system had to be secure (devices are in untrusted locations), scalable (10M+ devices hitting the API), and maintainable (no manual certificate management at that scale).

## What I Did

**1. DMZ gateway architecture was the key decision.** Devices connect through a DMZ gateway that handles JWT authentication (Cognito + Okta). Only authenticated requests pass to the internal service. This isolates the core platform from the device fleet's unpredictable traffic patterns.

**2. Automated certificate rotation.** At 10M device scale, you cannot manually rotate certificates. I built automated OAuth lifecycle management — certificates are renewed automatically before expiry, with Dynatrace monitoring on the rotation process. If rotation fails, an alert fires before any device is impacted.

**3. Three-layer architecture:**
- DMZ gateway: JWT validation, rate limiting, initial auth
- Internal service: payload persistence, OAuth lifecycle, certificate management
- Telemetry pipeline: S3 storage + AWS Athena for analytical queries

## The Outcome
- **10M+ devices** ingesting health telemetry reliably
- **Zero manual certificate management** — fully automated rotation
- Security: DMZ isolates core platform from device-facing traffic
- Telemetry data queryable via standard SQL (Athena) without provisioning analytics infrastructure

## Principal Signal
*Security at scale isn't about adding more checks at each layer — it's about designing the isolation so that even if the outer layer is compromised, the inner system is protected. The DMZ architecture, automated certificate rotation, and JWT auth are designed as a system, not bolted on.*

## Bridge
*"If your IoT/platform has device-facing APIs that must be secure at scale: DMZ gateway for external traffic, automated cert rotation as a system (not a script), and always keep device auth separate from user auth — different token lifetimes, scopes, and rotation policies."*

## Watchpoints
| Question | Your Anchor |
|----------|------------|
| "How did you handle device auth at 10M scale?" | "Cognito + Okta for JWT issuance. Devs don't manage secrets — the OAuth flow handles it. Rate limiting at the gateway prevents device floods." |
| "What if a device's certificate expired?" | "Automated renewal before expiry. Dynatrace monitors renewal process. If renewal fails, alert fires before cert expires — we proactively rotate." |
| "Why AWS Athena for telemetry?" | "Dynatrace handles real-time. Athena handles deep analysis — long-range trends, cross-device correlation, capacity planning. Serverless SQL on S3 data. No infrastructure to manage." |

---

# Project 7: Field Catalogue (Offline-First Android)

## Headline
*"I built an offline-first Android app for Dish field technicians — 100% offline capability in remote areas with zero connectivity. The app contributed to a 60% increase in on-site technical sales and cut catalogue update delivery time from weeks to minutes."*

## The Problem (Business Context)
Dish field technicians visit customer homes in remote areas with no cellular connectivity. They needed to browse the full product catalogue — pricing, inventory, technical specs — in front of customers, during visits. The existing process: print catalogue PDFs that were outdated within days, or drive to an area with signal to sync. Sales were being lost because technicians couldn't access current pricing and inventory on-site.

## What I Did

**1. 100% offline-first design.** The entire catalogue — products, pricing, inventory, technical specs — is cached locally on the device using SQLite. The app works identically with or without connectivity. No "offline mode" switch — it's always offline-first.

**2. Compressed delta sync for updates.** When connectivity is available, the app syncs using compressed deltas from the CMS — only the changes since last sync, not the full catalogue. This made updates fast even on slow connections (edge networks, 3G).

**3. CMS integration.** The centralized CMS manages all product data. Technicians don't need to know which version of the catalogue they're on — the app syncs silently. Update delivery time: weeks (print) → minutes (digital).

## The Outcome
- **100% offline capability** — app works everywhere, every time
- **60% increase in on-site technical sales** — technicians can show current pricing and inventory
- **Update delivery: weeks → minutes** — CMS sync cut catalogue update time dramatically
- **Sales VP appreciation** — formal recognition for revenue impact
- **Adopted by all field technicians company-wide**

## Principal Signal
*The best feature is the one that works when nothing else does. Offline-first isn't a constraint — it's a design decision that forces you to handle every edge case upfront. The sales impact wasn't about the app's features — it was about removing the friction that prevented technicians from selling.*

## Bridge
*"If your company has field workers, sales reps, or anyone who works outside of reliable connectivity: offline-first isn't optional. It's the difference between an app that's used and an app that's ignored. The principle: design for disconnected operation first, then add sync as an enhancement."*

## Watchpoints
| Question | Your Anchor |
|----------|------------|
| "How did you handle conflict resolution when two technicians updated the same product?" | "Technicians don't modify product data — they consume it. Conflicts only existed for order placement, which is a different write path with server-side authority." |
| "What was the biggest technical challenge?" | "The CMS integration. The existing system pushed full catalogues — we had to redesign the sync to push only deltas. Compressed JSON patches with version-aware reconciliation." |
| "How did you measure the 60% sales increase?" | "Sales data before and after rollout, controlled for seasonal variation. The Sales VP tracked monthly on-site conversion rates." |

---

# Project 8: DISH App Store

## Headline
*"I built a serverless internal enterprise app distribution platform — Lambda, DynamoDB, React — that delivers iOS/Android builds to Dish employees, technicians, and retailers via OTA installation with Okta SSO and group-based access control."*

## The Problem (Business Context)
Dish had no standard way to distribute internal builds. Engineers emailed APKs, posted on Slack, or uploaded to shared drives. No version control, no access control, no rollback capability. Retailers needed controlled access (only specific builds), technicians needed latest builds, and security needed to know who downloaded what.

## What I Did

**1. Serverless architecture.** Lambda + DynamoDB + S3 — zero infrastructure to manage. Builds uploaded once, delivered to authorized devices OTA. DynamoDB access pattern: "get latest build for device type X" — single-digit-ms reads at any scale.

**2. Okta SSO + group-based access control.** Not everyone can download every build. Engineers see all builds. Retailers see only approved builds. Technicians see only the latest stable build. Access is managed via Okta groups — zero-touch onboarding.

**3. React frontend** for uploading builds, managing versions, viewing download analytics.

## The Outcome
- Eliminated the "email the APK" pattern
- Controlled access by role (Okta groups)
- Full audit trail — every download logged
- Zero infrastructure management (serverless)

## Principal Signal
*Not every problem needs a complex solution. Serverless was the right call here — the access pattern was simple, the scale was moderate, and the operational overhead of managing servers would have been higher than the value delivered.*

## Bridge
*"If your company still distributes internal builds via Slack or shared drives, this is a quick win: serverless backend, Okta SSO, OTA delivery. Two sprints to build, years of friction eliminated."*

---

# Project 9: Asset Management (Hackathon → Company-Wide)

## Headline
*"I built an asset tracking system in 48 hours during a hackathon — Spring Boot, ReactJS, containerized. It won Codefest 2023. Leadership productized it. It's now used company-wide, cutting manual tracking effort by 70%."*

## The Problem (Business Context)
Dish had no centralized asset tracking. IT assets — laptops, monitors, phones — were tracked in spreadsheets. Lost devices, no audit trail, manual reconciliation every quarter. The company needed a system but it wasn't prioritized on any team's roadmap.

## What I Did

**1. I built it in a hackathon.** 48 hours, Spring Boot backend, React frontend, Docker container, deployed on internal VMs via JFrog. The hackathon constraint forced me to prioritize: the core loop (check in/check out, search, reports) worked on day 1. Everything else was optional.

**2. I made it easy to adopt, not perfect.** When leadership asked to productize it, I didn't say "let me rebuild it properly." I said "let me add the features you need incrementally." We added Okta SSO, reporting, and integration with the procurement system — each as a sprint, not a rewrite.

**3. Adoption was demand-driven, not mandated.** The first team to use it told another team, who told another. Within 6 months, it was company-wide. No announcement, no forced rollout.

## The Outcome
- **Codefest 2023 winner**
- **Company-wide adoption** — every Dish employee uses it
- **70% reduction in manual tracking effort**
- Full audit trail for IT asset lifecycle

## Principal Signal
*Speed of delivery matters more than perfection. The hackathon didn't produce a production-ready system — but it proved the concept existed. The willingness to iterate in small sprints, not rewrite from scratch, is what made it succeed.*

## Bridge
*"There's no faster way to prove an idea than a hackathon. If I join your company and see a problem that's hurting teams but isn't on the roadmap, I'll build the prototype myself in a sprint, show the data, and let demand drive adoption."*

---

# Project 10: Shift Allowance (Company-Wide HR Tool)

## Headline
*"I built a full-stack portal that automated Dish's manual Excel-based shift allowance system — it's now used by every Dish employee for shift requests and payroll approvals. The project earned an HR Spot Award."*

## The Problem (Business Context)
Dish's shift allowance system was entirely manual — Excel spreadsheets emailed back and forth. Employees submitted requests, managers approved, HR reconciled — all in email threads with attachments. Errors were common. Payroll reconciliation took days. Employee satisfaction was low because nobody knew the status of their request.

## What I Did

**1. Full-stack build in one sprint.** Spring Boot backend, React frontend, deployed on internal infrastructure. Core flow: employee submits shift request → manager approves → HR reconciles → payroll processes. Status visible at every step.

**2. Designed for company-wide scale from day 1.** The system had to handle every Dish employee — different shift types, different approval chains, different pay rates. I made the workflow configurable so each department could define their own rules.

**3. Minimal training needed.** The UI mirrored the existing Excel templates so employees didn't need to learn a new workflow. Adoption happened organically because the portal was strictly better than emailing spreadsheets.

## The Outcome
- **Used by every Dish employee** company-wide
- **HR Spot Award** for automating manual Excel workflows
- Eliminated email-based approval chain
- Payroll reconciliation: days → automated

## Principal Signal
*Internal tools succeed when they remove friction, not when they add features. The Shift Allowance portal replaced an email chain with a web form — the technical complexity was low, but the organizational impact was high. I prioritize building things that unblock people.*

## Bridge
*"Most companies have painful manual workflows that nobody prioritizes because 'it's not the product.' I have a pattern for these: build the core loop in one sprint, mirror the existing workflow so no training needed, and let demand drive adoption."*

---

# Project 11: Kiro Mobile & Dish Ignite 2026 Showcase

## Headline
*"I built Kiro Mobile — a lightweight mobile interface to monitor and control AI agent sessions from a phone. It was showcased at Dish Ignite 2026, Dish's internal AI demo day, where I demonstrated an agent autonomously fixing a bug from Jira in under 20 minutes — live, in front of VPs."*

## The Problem (Business Context)
Dish's AI agents ran on engineers' workstations. You had to be at your desk to see what an agent was doing, check progress, or intervene. Engineers wanted to kick off a migration overnight and check progress from their phone. Leadership wanted to see AI in action, not hear about it in slides.

## What I Did

**1. The mobile interface was a thin client.** Chrome DevTools Protocol over LAN — the phone shows a live preview of the agent's chat, task progress, and code changes. No backend to build — it piggybacked on the existing agent infrastructure.

**2. The Ignite demo was carefully sequenced.** I wrote an OpenAPI spec in real time, the agent generated the Spring Boot service with tests, and the subagent orchestrated GitLab MR creation and Dynatrace monitoring setup — all in under 20 minutes. The VPs saw working code, not a slide deck.

**3. The demo was the catalyst, not the final product.** After Ignite, two additional teams adopted the agent skills because they saw it work live. The demo proved the concept was real, not theoretical.

## The Outcome
- **Dish Ignite 2026 showcase** — live demo to VP+ audience
- **VP buy-in** to scale AI agent skills across engineering
- Catalyzed adoption by teams who saw the demo
- Two more teams adopted within weeks of Ignite

## Principal Signal
*Presentations convince your peers. Live demos convince your leadership. I invested in making AI work visibly — showing working code, not architecture diagrams. That's what got the sponsorship to scale.*

## Bridge
*"When I come into a new company, I won't need months to demonstrate value. I can build a working prototype in days, show it to leadership, and let results drive the conversation. That's how AI adoption starts."*

## Watchpoints
| Question | Your Anchor |
|----------|------------|
| "What was the most surprising feedback?" | "That the demo was credible because I showed a failure case, too — the agent hit a test failure, self-corrected, and retried. Showing the agent handle errors was more convincing than showing it succeed perfectly." |
| "Why Kiro Mobile specifically?" | "Because the pain point was real — engineers wanted to start AI workflows and walk away. Mobile monitoring was the unlock." |

---

# Project 12: Pivot3 VMware HCI Platform

## Headline
*"At Pivot3, I served as Technical Lead for the VMware Hyper-Converged Infrastructure platform — building backend REST APIs, a ReactJS vSphere UI plugin, and vRealize Orchestrator automation. The automation reduced manual provisioning effort by 60% for 1000+ storage volumes. I partnered with global product stakeholders on roadmap, architecture reviews, and release delivery."*

## What I Did

**1. Full-stack delivery.** Backend REST APIs for volume management, ReactJS plugin embedded inside VMware vSphere (admins manage storage from their existing tool — no context switching), and vRealize Orchestrator automation that replaced a manual per-volume provisioning workflow.

**2. Client-facing architecture role.** I didn't just code — I partnered with Pivot3's product stakeholders (US-based) on roadmap planning, architecture reviews, and release cadence. This was my first experience translating technical decisions into language that non-technical stakeholders could evaluate.

**3. Automation as leverage.** The vRealize Orchestrator plugin turned a 30-minute manual provisioning task into a one-click workflow. That 60% reduction wasn't from writing more code — it was from identifying which manual step was the bottleneck and automating ONLY that step.

## The Outcome
- **60% reduction in manual provisioning effort** across 1000+ volumes
- VMware integration: ReactJS plugin inside vSphere UI
- Client-facing delivery — managed US-based stakeholder relationships

## Principal Signal
*My first exposure to the leverage principle: automating the right bottleneck removes more friction than optimizing every step. The vRO workflow replaced ONE manual step that blocked every provisioning request — 60% improvement from a single automation.*

## Bridge
*"This was my first experience designing for enterprise integration constraints — the VMware plugin had to match the look and feel of vSphere's own interface, and the API contracts had to be stable across releases. The lesson: enterprise software succeeds when it fits into existing workflows, not when it adds new ones."*

---

# Project 13: Enterprise Mobile & Mobitaz Test Automation

## Headline
*"Early in my career, I led the development and launch of Nasuni and Spree Wearables Android apps on the Google Play Store — and built Mobitaz, a mobile test automation framework from scratch that later became part of MSys's QA service offering."*

## What I Did

**1. Shipped two Android apps end-to-end.** Nasuni (cloud storage client) and Spree Wearables (fitness companion) — UI, local caching, REST API integration, analytics, Play Store deployment. Led a team of 3 engineers.

**2. Built Mobitaz from scratch.** A record-and-playback test automation framework that could replay tests across multiple Android devices simultaneously. This was before the mobile test automation tooling ecosystem matured. I identified the gap (teams testing manually on one device at a time), built the framework, and validated it on real projects.

**3. The framework became a product.** Mobitaz was used in client demos at MSys and became part of their QA service offering. The lesson: building internal tools that others can use is a multiplier — one framework accelerates every project.

## The Outcome
- **Nasuni & Spree Wearables** launched on Google Play Store
- **Mobitaz** — internal tool → client demo → QA service offering
- **NetApp Selenium regression suite**: 100+ scenarios, 50% manual regression reduction

## Principal Signal
*This taught me that impact comes from building tools that others use, not just features that end users see. Mobitaz was more valuable as a framework for 10+ projects than any single app it tested.*

## Bridge
*"Early in my career, I learned that building for leverage — tools, frameworks, automation — compounds over time. That lesson shaped how I approach every problem: ask 'what's the one thing I can build that makes everyone faster?' before writing any feature code."*

---

# Appendix: Narrative Selection Matrix

| Question Type | Best Narrative # | Why |
|---------------|-----------------|-----|
| "Tell me about yourself" | #1 + #2 + #4 | Platform scope → AI migration → org-wide adoption |
| "Your most challenging project" | #3 (Sling TV) | Data consistency, migration strategy, AI at scale |
| "How do you drive adoption?" | #4 (AI skills) | No authority, paired, customized, 5+ teams |
| "A time you influenced without authority" | #2 (Spring Boot 3) | Built reference, showed data, let results drive |
| "A time you made a mistake" | #4 (AI test fix bug) | Agent patched symptom, not root cause |
| "How do you handle conflict?" | #3 (Sling approach) | Manager wanted traditional rewrite — you built prototype |
| "Building vs buying decision" | #4 (MCP security) | Built because integration with workflow was the value |
| "Tell me about an initiative that failed" | #4 (first agent skill) | Too rigid, redesigned as configurable |
| "How do you mentor?" | #4 (paired adoption) | Shadowing, office hours, peer learning |
| "How do you think about scale?" | #6 (STB Health) | 10M devices, DMZ, auto cert rotation |
| "Tell me about a deadline-driven project" | #9 (Asset Management) | 48-hour hackathon → company-wide |
| "Why should we hire you?" | #2 + #4 | AI + org-wide impact + proven adoption playbook |
