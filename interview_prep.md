# Interview Preparation — Chokkar Gurusamy

## "Tell me about yourself" — Full Career Intro with Technical Depth (~5-6 min)

> **Use this when:** "Walk me through your career in detail" or "Tell me about your technical work" or you have 5+ minutes.
> **Use the Standard Script** (~130s) for normal "Tell me about yourself."
> **Use the Elevator Version** (~30s) when time is short.
> **Don't memorize verbatim.** Hit the beats in order. Speak naturally.

***(breathe)*** I'm a Staff Engineer at Dish Network — 14+ years in the industry, currently architecting the subscriber platform that serves over 10 million users. I joined Dish in May 2022 as a Lead and was promoted to Staff Engineer within two years.

---

### My Dish Platform — Architecture

***(breathe)*** My primary role is owning the architecture for the **My Dish** subscriber platform — that's the flagship application subscribers use to manage their accounts, billing, plans, and equipment. The platform runs API-first microservices on Spring Boot 3, deployed on Rancher-managed Kubernetes. I defined the integration patterns across frontend, backend, and shared platform services — API Gateway routing, Resilience4j circuit breakers between services, GemFire distributed caching for hot-path reads, Kafka for event-driven communication, and Dynatrace for distributed tracing across every request. The platform maintains 99.9% uptime with sub-second API latency.

---

### Spring Boot 3 Migration — How AI Transformed the Platform

***(breathe)*** A significant part of that role was driving the org-wide Spring Boot 3 migration across all platform services. Spring Boot 2 had reached end-of-life — every week it stayed on 2, the security team filed CVE tickets, new features were blocked because dependencies couldn't be upgraded. The team estimated 18 months of manual migration across 50K+ lines of code. I used AI to compress that to 5 months.

***(breathe)*** Here's how it worked technically. I fed each service's codebase into Kiro with a structured prompt: "Identify all Spring Boot 2 patterns that break in 3 — security config, Hibernate annotations, Jakarta namespace, actuator endpoints." Kiro produced a migration spec: which files change, what breaks, what the fix is. The agent then executed that spec. The `javax.*` to `jakarta.*` rename across 50K+ lines was fully automated — zero human intervention. The `WebSecurityConfigurerAdapter` to `SecurityFilterChain` conversion was automated with human review on the security logic. Hibernate 6 query migrations were flagged for human review because the old code used dynamic queries that don't translate cleanly. The agent also generated tests from the OpenAPI specs — Postman collections for contract testing, JUnit for implementation testing — and enforced 85% coverage as a CI gate.

***(breathe)*** I built a custom dashboard — a React app pulling data from GitLab and Kiro's output — that showed leadership exactly what the AI was doing: lines changed automatically versus manually, test pass rate, time saved, defect rate per service. That dashboard convinced the VP to scale the approach. After iterating on 3 services and updating the skill playbook for Hibernate-specific patterns, the remaining 9 services went through in about 3 weeks. That work achieved a 60% productivity gain — a mid-size service that used to take a senior engineer two weeks took three days. That's what got me promoted from Lead to Staff.

---

### Security and Operational Gates

***(breathe)*** On the platform, I also established the security and operational gates. I built a custom Dynatrace MCP server that gives AI agents read-only access to distributed traces — the agent can query which service is failing, what the latency looks like, what the error rate is, without ever touching the database. Incident diagnosis went from 30 minutes to 2 minutes. I built a Snyk MCP server paired with Kiro agents that scans for vulnerabilities and creates same-day fix PRs — the flow is: Snyk reports a vulnerability, the MCP server fetches the advisory, the agent reads the fix recommendation, applies the patch, verifies with tests and a rescan, and creates a PR. What used to take 2 to 7 days now takes hours. And I mandated 85% plus JUnit and Postman test coverage across all services — gated in CI so the pipeline fails if it drops below that threshold.

---

### Sling TV — AI-Powered Legacy Modernization at Scale

***(breathe)*** Outside of the subscriber platform, I led the transformation of **Sling TV** — that was the biggest modernization effort. We had 80-plus legacy Ruby on Rails APIs, 400K lines of code, no documentation. Adding a feature took weeks because everything was tightly coupled — a change in billing could break content delivery. The business needed to ship streaming features faster. Estimated manual rewrite: 18 months, 12 engineers.

***(breathe)*** I used Amazon Q to reverse-engineer the entire codebase. The AI ingested every model, controller, route, view, and database schema. It identified every API endpoint and its request shape, database queries and their relationships, business logic flows, and implicit behavior like Rails callbacks. It generated OpenAPI specs from the routes and Java microservice skeletons from those specs. I then used DDD principles to group the 80-plus APIs into bounded contexts — billing, content catalog, entitlements, recommendations — and each became an independent microservice.

***(breathe)*** For each bounded context: the AI generated the skeleton with tests, I reviewed the business logic translation — Ruby callbacks to Java Spring events — and we ran old and new in parallel for 2 weeks. API Gateway routed traffic via feature flags — 10% to new initially, then 50/50, then 100%. Dynatrace traced every request across both systems, and a data reconciliation job compared responses hourly. The hardest part was data consistency — when you split a monolith's database, you lose ACID transactions. We solved it with the Saga pattern on Kafka: each service publishes an event when its local transaction completes, downstream services listen and update their own state, and compensation logic rolls back on failure. We delivered in 5 months what was estimated at 18, with 85% test coverage and fewer bugs than the original. That's a 70% productivity gain. That earned me the Technical Excellence Award in 2025.

---

### DPA, STB Health, Field Catalogue, App Store

***(breathe)*** I've also built several other systems at Dish. The **Dish Paperless Agreement** — I migrated it from ColdFusion to Spring Boot microservices. That system handles the entire onboarding flow for field agents — agreement signing, digital signatures, cross-selling, equipment activation — through 23 integrations and 7 SFTP distribution targets. I designed a Spring Batch-based orchestration layer that manages retries, dead-letter queues, and monitoring for each integration. That work earned me a CPAW Award.

***(breathe)*** The **STB Health Monitor** — field technicians scan QR codes on set-top boxes and upload health telemetry. It handles 10 million-plus devices. I built a DMZ gateway with JWT authentication using Cognito and Okta, an internal service for payload persistence and OAuth lifecycle management, and automated certificate rotation for the entire device fleet — no manual certificate management at 10M scale.

***(breathe)*** The **Field Catalogue** — a fully offline-first Android app. Field technicians in remote areas with zero connectivity browse the entire product catalogue, check pricing and inventory, and place orders. When connectivity returns, the app syncs using compressed delta updates from the CMS. The CMS sync cut update delivery time from weeks to minutes, and the app contributed to a 60% increase in on-site technical sales — that earned me appreciation from the Sales VP.

***(breathe)*** The **DISH App Store** — a custom-built internal enterprise app distribution platform using Lambda, DynamoDB, and React. It delivers iOS and Android builds to employees, technicians, and retailers via OTA installation with Okta SSO and group-based access control.

---

### Internal Tools — Hackathon to Company-Wide

***(breathe)*** Beyond the platform work, I build internal tools that ship. **Asset Management** started as a hackathon project — I built a full-stack system with Spring Boot and ReactJS in 48 hours, containerized it with Docker, deployed it on internal VMs via JFrog. It won Codefest 2023, and leadership productized it — it's now used company-wide, cutting manual tracking effort by 70%. **Shift Allowance** automated what was previously manual Excel workflows across the company. It's now used by every DISH employee — that earned me an HR Spot Award. The lesson: internal tools succeed when they make someone's job measurably easier. Adoption comes from demand, not mandate.

---

### Custom AI Agents — The Defect Lifecycle and Org-Wide Adoption

***(breathe)*** On the AI and innovation side — I built **Kiro Mobile**, a lightweight mobile interface to monitor and control AI agent sessions from a phone over LAN via Chrome DevTools Protocol. That was showcased at **Dish Ignite 2026**.

***(breathe)*** More importantly, I created custom agent skills that automate the entire defect lifecycle. The skill is a 5-phase playbook: Phase 1 — the agent reads the bug from Jira via MCP, identifies the affected service, searches the codebase via GitLab MCP. Phase 2 — it checks out the branch, runs the test suite to establish a baseline, reproduces the issue. Phase 3 — it implements the fix following the team's coding patterns. Phase 4 — it validates by running tests and Snyk rescan, with a maximum of 3 iterations before escalating to a human. Phase 5 — it creates a PR tagged as AI-generated with a full description of what was fixed and why.

***(breathe)*** The agent operates through MCP servers — GitLab for code, Jira for tickets, Snyk for vulnerabilities, Dynatrace for traces — each with scoped permissions. It can create a PR but never merge it. It can read traces but never modify monitoring. It can read vulnerability data but never dismiss a finding. That's the security boundary that makes autonomous agents viable in a corporate environment.

***(breathe)*** The same pattern handles vulnerability remediation — Snyk MCP server paired with the agent means same-day fixes instead of 2 to 7 days. What started as my experiment on one team is now used across 5-plus engineering teams at Dish. I hold training sessions, document the playbooks, and other teams build their own skills using the framework I established. The compound effect: every layer of modernization makes the next one faster. Spring Boot 3 unblocked releases. Snyk MCP unblocks security. Dynatrace MCP compresses incident response. And the agent skills scale all of it across teams.

---

### MSys Technologies — 10 Years of Growth

***(breathe)*** Before Dish, I spent 10 years at **MSys Technologies** — now called Aziro. I joined as a Software Engineer in 2012 and progressed to Senior, Tech Lead, and eventually Technical Architect. I served global enterprise clients — **Pivot3**, **Nasuni**, and **NetApp** — across storage, virtualization, and cloud domains. At Pivot3, I served as Technical Lead for the VMware HCI platform — I built the ReactJS vSphere UI plugin, backend REST APIs, and vRealize Orchestrator automation that reduced manual provisioning effort by 60% for over a thousand storage volumes. I partnered with global product stakeholders on roadmap, architecture reviews, and release delivery. I also launched Nasuni and Spree Wearables Android apps on the Play Store with Firebase sync for crash monitoring, built the Mobitaz mobile test automation tool, and delivered a Selenium regression suite for NetApp covering 100-plus scenarios. I was awarded Best Performer of the Year five times — 2013, 2014, 2016, 2018, and 2019 — and received the Blog Championship Award in 2017.

---

### Certifications, AI Workspace, and Close

***(breathe)*** I hold a **Google Cloud Professional Data Engineer** certification, and I regularly use Paseo ADE for ACP agent orchestration alongside Kiro-CLI and OpenCode. My workspace uses custom agentic skills and custom MCP servers to automate coding and workspace workflows.

***(breathe)*** So the full arc: I started as a developer at MSys, spent a decade growing into architecture across multiple enterprise clients, then moved to Dish where I architected the subscriber platform for 10 million users, used AI to modernize legacy systems that directly unblocked product delivery, built custom AI agent skills that other teams adopted, and delivered award-winning internal tools. The numbers tell the story: 60% productivity gain on Spring Boot 3, 70% on Sling TV, same-day vulnerability fixes, 99.9% uptime for 10 million subscribers. I'm excited about bringing that experience — the platform architecture, the AI-powered delivery, and the ability to drive adoption across engineering — to [company].

---

---

## "Tell me about yourself" — Standard Script (~130s)

> **Use this when:** They say "Tell me about yourself" and you want a tight but complete answer.

***(breathe)*** I'm a Staff Engineer at Dish Network, architecting the subscriber platform that serves 10M+ users — 14+ years in the industry.

***(breathe)*** My primary role is owning the architecture for the **My Dish** subscriber platform — API-first microservices on Spring Boot 3, deployed on Rancher Kubernetes, maintaining 99.9% uptime with sub-second latency. I drove the org-wide Spring Boot 3 migration across our platform services using AI-powered workflows, automating the remediation of breaking changes across 50K+ lines of code to achieve a 60% productivity gain — that work got me promoted from Lead to Staff.

***(breathe)*** Separately, I led the transformation of Sling TV — 80+ legacy Ruby on Rails APIs into modern Java microservices using Amazon Q to reverse-engineer 400K lines of legacy code. We delivered in 5 months what was estimated at 18 months, with 85% test coverage and fewer bugs than the original.

***(breathe)*** Building on those wins, I created custom AI agent skills that automate the entire defect lifecycle — an agent reads a bug from Jira, reproduces it, fixes it, runs tests, and creates a PR. I wired it to MCP servers for GitLab, Jira, Dynatrace, and Snyk so the same pattern handles vulnerability remediation in hours instead of days. What started as my experiment on one team is now used across 5+ engineering teams at Dish — I hold training sessions, document the playbooks, and other teams build their own skills using the framework I established. It was showcased at Dish Ignite 2026.

***(breathe)*** I also build internal tools that ship — an asset tracking system from a hackathon is now company-wide, a shift allowance portal adopted by every employee. So the arc is: I own large-scale platforms, I modernize them using AI, I codify that capability into reusable agent skills, and I drive adoption across the org.

---

## 30-Second Elevator Version

***(breathe)*** Staff Engineer at Dish Network — I own the architecture for the My Dish subscriber platform serving 10M+ users. I led the Spring Boot 3 migration using AI (60% productivity gain, promoted to Staff) and transformed Sling TV's 80+ Rails APIs in months instead of years. I built custom AI agents that fix defects and vulnerabilities, now adopted across 5+ teams. Looking to bring that to [company].

---

## Career Arc Summary

| Phase | What You Did | The Signal |
|---|---|---|
| MSys (10 yrs) | Grew from SE → Architect. Built platforms for enterprise clients. | Stability, promotion trajectory, client-facing |
| Dish Platform Work | Architected 10M+ user platform. Modernized legacy systems. Promoted to Staff. | Enterprise-scale delivery |
| AI/Agent Work | Built defect-fixing skills, MCP integrations, Ignite 2026 showcase. | Ahead of the curve, leverage-focused |
| Internal Tools | Hackathon → company-wide adoption. Full-stack delivery. | Ownership mentality, ships |

---

## Key Numbers to Have Ready

| Metric | Value | Context |
|---|---|---|
| Spring Boot 3 migration | 50K+ lines, 12 services | 60% productivity gain, promoted to Staff |
| Sling TV migration | 400K lines reverse-engineered | 5 months vs 18 months, 70% gain |
| Test coverage | 85%+ mandated in CI | 10K+ unit tests generated |
| Vulnerability fix time | Same-day (hours vs days) | Snyk MCP + AI agent skill |
| Incident diagnosis | 30 min → 2 min | Dynatrace MCP + AI agent |
| Platform uptime | 99.9% | 10M+ subscribers |
| Teams using AI skills | 5+ | Training sessions + playbooks |
| Awards | Technical Excellence (2024, 2025) | For modernization + AI work |

---

## Delivery Tips

- **Pacing:** The full career intro has 16 breath points — use them. Speak at conversation pace, not presentation pace.
- **Interruption is good.** If they ask a follow-up mid-script, you've hooked them. Go with it.
- **Trim if needed.** Drop any one project section (DPA, STB, Field Catalogue, App Store) and the narrative still holds.
- **Don't memorize verbatim.** Land these exactly: current title, "10M+ subscribers", "Spring Boot 3 migration", "built custom agent skills that autonomously fix defects", "Dish Ignite 2026". Everything else is yours to paraphrase.
- **The unspoken message:** You think in leverage. Most engineers can't say they built agents that autonomously fix bugs. That's your edge.
---

## Complete Interview Q&A by Resume Section

> Skim by section. Pick 3-5 questions you'd struggle with most and deep-rehearse those — don't try to memorize all 62. Every answer follows the same pattern: **context → action → outcome → lesson**.

---

## Professional Summary

**1. What does "end-to-end solution architecture" mean to you? Give a concrete example.**

> To me it means I own the full lifecycle: understanding the business requirement, defining the API contracts, choosing the technology stack, designing the data model, wiring observability, setting up CI/CD, and being on-call when it breaks. A concrete example is the My Dish subscriber platform — I didn't just design the APIs. I defined how frontend, backend, and shared services integrate. I set the OpenAPI standards. I established the security gates with Snyk. I integrated Dynatrace for observability. And when there's an incident at 2 AM, I'm in the call. End-to-end means you can't hand off the hard parts.

**2. You mention "AI governance" in your summary — what does that look like in practice?**

> AI governance means having guardrails around how AI agents operate in our SDLC. Concrete rules: (1) AI can generate code and create PRs, but never merges to production without human review. (2) Every AI action is logged and traceable — I built the Dynatrace MCP server for exactly this. (3) AI agents follow structured playbooks with approval gates at each phase — they stop before destructive operations. (4) We audit AI-generated code for security compliance via Snyk before it reaches staging. Governance isn't about restricting AI — it's about making its output auditable and reversible.

**3. How do you balance hands-on coding with architecture work at Staff level?**

> I split my week: about 40% hands-on, 60% architecture and mentorship. The hands-on part isn't writing feature code — it's building the tooling that makes the team faster: the AI migration workflows, the MCP servers, the custom agent skills. The architecture part is ADRs, design reviews, integration patterns, and incident response. I stay hands-on because I can't design something I don't understand at the code level, and I can't build trust with engineers if I'm not in the trenches.

**4. You presented a live demo to VP+ leadership — what was that experience like?**

> I demonstrated Kiro spec-driven development: I wrote an OpenAPI spec in real time, the agent generated the Spring Boot service with tests, and I showed the subagent orchestrating GitLab MR creation and Dynatrace monitoring setup — all in under 20 minutes. The VPs could see the code being written, tested, and deployed. The reaction was positive because it wasn't a slide deck — it was a live demo of working software. That demo is what got leadership buy-in for scaling AI across engineering.

---

## Technical Skills

**5. You list 6 languages, 12+ frameworks, 8 databases, 3 clouds — which are genuinely your strongest?**

> Java and Spring Boot are my core — that's what I've lived in for the last 8 years. Everything else is situational: Kotlin for Android, TypeScript for React frontends, Python for automation scripts. For databases, PostgreSQL is my default. The rest I know well enough to make the right architectural choice and review the implementation. The range isn't about being an expert in everything — it's about being able to design systems across the stack and know what questions to ask.

**6. What's the difference between Kiro and Paseo in your workflow?**

> Kiro is my primary AI coding assistant — spec-driven development, agent skills, MCP integrations, code generation. It's what I use daily for writing code, migrations, and running the defect-fixing agents. Paseo is my agent orchestration layer — it's where I manage multiple AI agents (Codex, Claude Code) across workspaces, coordinate their work, and handle file-locking so they don't conflict. Think of Kiro as the driver and Paseo as the traffic controller.

**7. How do you stay current with so many technologies?**

> I don't chase everything. I learn what my current problem demands. When Dish needed Spring Boot 3 migration, I deep-dived into the breaking changes. When I needed to build MCP servers, I learned the protocol spec. When I needed offline-first mobile, I studied SQLite sync patterns. The rest I follow at a high level — enough to know what's possible and where to look when I need it. The Google Cloud certification was deliberate: I wanted cloud credibility at the architecture level.

**8. You list both SQL and NoSQL databases — when do you pick one over the other?**

> PostgreSQL is my default for anything with relations, transactions, or reporting queries. I use MongoDB when the data shape is unpredictable — config documents, catalogue entries with varying attributes. DynamoDB when I need single-digit-millisecond reads at massive scale with a known access pattern — the DISH App Store uses it for OTA build metadata because the access pattern is always "get latest build for device type X." GemFire (distributed cache) I use for hot-path data that can't tolerate DB latency. The important thing is knowing what each is good at and not forcing one where it doesn't belong.

---

## Dish Network — General

**9. You were promoted from Lead to Staff — what changed in your role?**

> The scope expanded. As Lead, I owned the architecture for my team's services. As Staff, I own the architecture patterns across multiple teams — the integration standards, the security gates, the observability framework. I also became responsible for org-wide initiatives: the Spring Boot 3 migration across all platform services, establishing Snyk vulnerability standards enforced across teams, and leading the AI-augmented development practice. The promotion recognized that I was already operating at that level — the title caught up to the work.

**10. You won Technical Excellence Awards two years in a row — what for?**

> 2024 was for the Spring Boot 3 migration and establishing the AI-powered modernization workflow that achieved 60% productivity gains. 2025 was for the Sling TV transformation program and building the custom MCP servers (Dynatrace, Snyk) that became the foundation for our AI-augmented SDLC. Both awards recognize impact beyond my immediate team — org-wide patterns that changed how engineering works.

**11. What's a CPAW Award and Spot Award?**

> CPAW is an internal recognition for delivery impact — I received it for the Paperless Agreement migration that successfully launched across 23 integrations. Spot Awards are immediate recognition for significant contributions — I received two: one for the Shift Allowance portal that automated HR's manual Excel workflows, and one for leading a critical incident recovery on the subscriber platform.

---

## My Dish App — Subscriber Platform

**12. Walk me through the architecture of the subscriber platform.**

> It's a set of REST microservices on Spring Boot 3, deployed on Rancher-managed Kubernetes. Each service owns a domain capability — subscriber management, billing, device activation, plan configuration. APIs are defined OpenAPI-first with a shared contract repository. Services communicate via REST for synchronous queries and Kafka for event-driven updates. API Gateway handles routing and rate limiting. Resilience4j provides circuit breakers between services. Dynatrace traces every request across service boundaries. PostgreSQL is the primary data store per service, with GemFire as a distributed cache for hot-path reads. CI/CD is GitLab → Docker build → Snyk scan → Rancher deploy. The platform serves 10M+ subscribers at 99.9% uptime with sub-second API latency.

**13. How do you maintain 99.9% uptime with sub-second latency?**

> It starts with architecture, not ops. Circuit breakers isolate failures. Bulkheads prevent one noisy service from taking down others. Caching (GemFire) keeps hot-path reads off the database. Kafka absorbs traffic bursts — devices don't hammer the APIs directly. Then observability: Dynatrace gives us distributed tracing across every service boundary, so we know exactly where latency is coming from. Deployment strategy: blue-green on Rancher, gated on Snyk scans and performance tests. And incident response is codified — runbooks, automated alerts, and an on-call rotation. 99.9% is designed in, not patched in.

**14. How did you measure the 60% productivity gain from AI migration?**

> I measured time-to-complete for common migration tasks — upgrading a service from Spring Boot 2 to 3, fixing breaking changes, updating security config. Before AI, a mid-size service took a senior engineer about 2 weeks — manual code changes, test updates, config fixes. With the Kiro spec-driven workflow, the same service took about 3 days. That's roughly 60% less effort. I tracked it across 12 services and built a dashboard showing the delta: lines changed automatically vs manually, hours saved, defect rate. The numbers were consistent enough that leadership approved scaling the approach.

**15. Tell me about the custom dashboard you built for AI code changes.**

> It's a lightweight React dashboard that pulls data from GitLab and Kiro's output — it shows which services were migrated, how many lines were AI-generated vs human-modified, the pass rate of automated tests, and time saved per service. The purpose was visibility: leadership could see that AI wasn't just generating noise — it was shipping verified code. It also helped me spot patterns where the AI was struggling (Hibernate query migrations, for example) so I could improve the playbook.

**16. How do you enforce 85%+ test coverage?**

> It's a CI gate — if coverage drops below 85%, the pipeline fails. But coverage is a lagging indicator. The leading practice is: I mandate tests at the API contract level before implementation. OpenAPI spec defines the contract → Postman collection tests the contract → JUnit tests verify the implementation against the contract. When you spec-test before coding, coverage follows naturally. The AI workflow also auto-generates tests from the spec, which helps teams stay above the bar without the overhead.

**17. How does your Dynatrace MCP server work?**

> It's a custom MCP server that gives AI agents read-only access to Dynatrace. The agent can query: "show me the distributed trace for this failed request," "what's the error rate on service X in the last hour," "which API endpoints are experiencing latency degradation." The agent reads the data, analyzes the trace, and suggests the root cause or creates a Jira ticket. It's not replacing the human's judgment — it's compressing the time from alert to diagnosis from 30 minutes to 2 minutes. The agent sees the trace and says "this is failing because the downstream payment service is returning 503" — and I can act immediately.

**18. Your Snyk MCP server achieves same-day vulnerability fixes — how?**

> The flow: Snyk scans a service and reports a vulnerability → the MCP server fetches the advisory details → the AI agent reads the fix recommendation from Snyk's database → it applies the patch to the codebase → verifies the fix with tests and a Snyk rescan → creates a PR. An engineer reviews and approves. The whole cycle — from detection to PR — takes hours instead of days. The key is that the agent doesn't guess — Snyk provides the remediation, the agent applies it mechanically. That's what makes same-day feasible.

**19. What are your API-first / OpenAPI development patterns?**

> (1) Contract first: write the OpenAPI spec before any implementation code. (2) Shared contract repository: all specs live in one Git repo, versioned, reviewed like code. (3) Spec drives everything — code generation (Spring Boot skeletons, client libraries), test generation (Postman collections), documentation (Swagger UI). (4) Breaking changes require a new API version and a migration plan in the spec review. (5) The AI workflows start from the spec — the agent reads the spec and implements against it, giving us spec-to-code traceability.

**20. What "integration patterns" did you define across frontend, backend, and shared services?**

> Three main patterns: (1) Backend-to-backend: REST with circuit breakers for synchronous, Kafka for event-driven. (2) Frontend-to-backend: API Gateway with rate limiting, JWT auth, and a BFF (Backend for Frontend) layer that aggregates microservice responses into view models so the frontend doesn't make 10 calls per page. (3) Shared services: a common library for auth validation, logging, DynamoDB access patterns, and Dynatrace instrumentation that every service consumes. The patterns reduced the "integration tax" — teams stopped inventing their own approach and followed a documented, supported pattern.
**21. How does AWS Athena fit into your telemetry and observability stack?**

> Dynatrace gives us real-time distributed tracing, but when we need to do deep analysis across weeks or months of data — trend analysis, capacity planning, cross-application correlation — we query the raw telemetry stored in S3 using Athena. Every service publishes structured logs and metrics to S3 via Kinesis or direct put. Athena lets us run standard SQL against that data without provisioning any infrastructure. For example: to find which STB device models had the highest error rates over the last quarter, I'd write a SQL query joining device telemetry with error logs in S3 — results in seconds. Before Athena, this kind of analysis required spinning up a Hadoop cluster or exporting data to a separate analytics database. The serverless model means we only pay for queries run, and the team can self-serve analytics without waiting on a data engineering pipeline. I used it across My Dish, STB Health, and all subscriber-facing application logs — it became our go-to for any ad-hoc data investigation.


---

## Sling TV Product Development

**21. Walk me through the strategic decision to transform 80+ Rails APIs.**

> The Rails monolith was the bottleneck. Adding a feature took weeks because you had to understand the entire codebase. Deployment was risky — one change could bring down unrelated functionality. The business needed to ship faster to compete with streaming rivals. The strategy: don't rewrite blindly. We reverse-engineered the entire codebase to understand what each API actually did (many were undocumented). Then we grouped them into bounded contexts — billing, content, entitlements, recommendations — and migrated one domain at a time. Each domain became its own Spring Boot service with its own data store. Event-driven design kept them loosely coupled.

**22. What was the hardest part of the migration?**

> Data consistency. When you split a monolith's database into per-service databases, you lose ACID transactions across domains. A customer's billing status and their content entitlement were in the same DB — now they're in separate services. We solved it with the Saga pattern: each service publishes events when its state changes, and downstream services listen and update their own state. Kafka was the event backbone. The compensation logic (rollback on failure) was the hardest part to get right. We tested it extensively with chaos engineering before cutting over.

**23. How did Amazon Q reverse-engineer 400K+ lines of legacy code?**

> Amazon Q ingested the entire Ruby on Rails codebase — models, controllers, routes, views, database schema. It identified API endpoints, their request/response shapes, database queries, and business logic flows. It generated OpenAPI specs from the routes and Java microservice skeletons from those specs. It also generated unit tests by analyzing the existing test patterns. The quality was surprisingly good for the mechanical parts — routes and models. Where it struggled was complex business logic with implicit behavior (callbacks, unless/until conditionals). Those needed human review and rewriting.

**24. What were Amazon Q's limitations?**

> (1) Ruby idioms don't translate directly to Java — things like dynamic method dispatch and metaprogramming produced Java code that compiled but was awkward. (2) Business rules embedded in Rails callbacks (`before_save`, `after_create`) needed human interpretation — the AI couldn't understand the intent. (3) Test quality was uneven — the structure was right but the assertions were sometimes tautological. (4) Performance-critical paths needed manual optimization — the AI generated correct but naive code. The lesson: AI handles the 80% mechanical work. The 20% that requires domain understanding is still the human's job.

**25. How did you maintain 85% coverage across 10K+ auto-generated tests?**

> We didn't trust the AI-generated tests blindly. We ran them against the legacy system to validate they actually caught regressions — any test that passed against the old code AND the new code was kept. Tests that passed against new code but failed against old code were flagged as potentially incorrect. We also manually reviewed tests on critical paths: payment logic, entitlement decisions, user data. The AI got us to 85% coverage fast, but human review ensured the 85% actually meant something.

**26. The 70% productivity gain — how was that calculated?**

> We estimated it would take 18 months and a team of 12 engineers to rewrite the platform using traditional methods. With the AI-assisted approach (Amazon Q + Kiro workflows + spec-driven development), we completed it in roughly 5 months with the same team size. 70% is the time savings. But the real win wasn't speed — it was quality. The AI-generated code had fewer bugs than manually written code because it followed the spec precisely. The human errors came in the integration points, which we caught with contract testing.

---

## Dish Paperless Agreement (DPA)

**27. What did migrating ColdFusion to Spring Boot involve?**

> ColdFusion is a legacy Adobe technology — it's a tag-based language that mixes HTML and server-side logic in the same file. The system handled the entire customer onboarding flow: agreement creation, digital signatures, cross-selling, equipment activation, and distribution to partners. Rebuilding it in Spring Boot meant: (1) reverse-engineering the business logic from spaghetti ColdFusion pages, (2) designing a proper layered architecture (controller → service → repository), (3) building REST APIs for the mobile field agent app, (4) orchestrating 23 downstream integrations and 7 SFTP distribution targets. The offline capability was the hardest part — field agents sign agreements in basements with no signal.

**28. 23 integrations and 7 SFTP targets — how did you manage that complexity?**

> Each integration had its own contract: different data formats (XML, JSON, CSV, fixed-width), different delivery mechanisms (SFTP, REST, SOAP), different schedules (real-time, hourly, daily). I designed an integration orchestration layer — a Spring Batch-based scheduler that managed retries, dead-letter queues, and monitoring for each integration. The SFTP targets were handled by a generic SFTP client service — configurable per target (host, credentials, path, format). Adding a new integration was a config change, not a code change. Dynatrace monitored every integration path so we knew immediately when one failed.

**29. How did you handle offline capability for field agents?**

> The field agent app caches agreements locally on the device (SQLite). The agent fills out the agreement, collects the signature, and queues it locally. When connectivity is available, the app synchronizes in the background — uploads signed agreements, downloads new assignments. Conflict resolution: server is authoritative for agreement state, device is authoritative for captured signatures. The challenge was the signature itself — we captured it as encrypted bitmap data locally, synced it when online, and the backend reconstructed the PDF.

---

## STB Health Monitor

**30. Walk me through the DMZ gateway design.**

> The STB Health system collects telemetry from 10M+ set-top boxes. You can't expose internal services directly to that many devices. The DMZ gateway sits in a demilitarized zone — accessible from the internet but isolated from the internal network. Devices authenticate via JWT (Cognito for device identity, Okta for technician identity). The gateway validates the token, normalizes the payload, and publishes it to a Kafka topic on the internal side. The internal consumer service processes the payload — persistence, alerting, analytics. The gateway never touches the internal database or services directly. This means even if a device is compromised, the attacker only reaches the DMZ, not the platform.

**31. QR code scanning at 10M devices — how did you handle scale?**

> The QR code encodes the device serial number and a one-time challenge token. The field tech scans it with a mobile app, which sends the decoded data to the DMZ gateway. The gateway validates the token against Cognito, issues a short-lived JWT, and the device starts streaming telemetry. The key design decision: the QR scan is just identity bootstrap — once the device is authenticated, all subsequent telemetry uses the JWT without re-scanning. Each scan is lightweight (a single HTTP POST), so 10M devices isn't a problem as long as they don't scan simultaneously. Kafka absorbs the telemetry stream regardless of burst rate.

**32. How did you handle OAuth lifecycle and certificate management for 10M devices?**

> Devices use device credentials registered in Cognito — each STB has a unique certificate installed at manufacturing time. The certificate is used to authenticate to Cognito, which issues a JWT. The JWT has a configurable TTL (we used 24 hours). The device refreshes the token automatically before expiry. For certificate rotation: we built a refresh mechanism where the device can request a new certificate from an internal CA service when the current one is within 30 days of expiry. The old certificate continues working until the new one is confirmed. The entire lifecycle is automated — no manual certificate management at 10M scale.

---

## Field Catalogue

**33. The app is 100% offline-capable — what's the sync architecture?**

> Local SQLite is the source of truth on the device, not the server. The CMS publishes catalogue updates as versioned JSON snapshots. When the device has connectivity, it checks the server for a newer catalogue version. If one exists, it downloads a compressed delta (only the changed records since the last sync), applies it locally, and stamps the new version. Reads are always from SQLite — zero network calls, zero latency. The user sees data instantly even in remote areas with no signal. Writes (like sales orders) are queued locally and synced when connectivity returns. The server always wins for catalogue data (reference data), so conflict resolution is straightforward.

**34. How did you measure the 60% increase in on-site technical sales?**

> Dish's sales team tracked two metrics before and after: (1) close rate when a technician accessed the catalogue on-site vs sending a link later, and (2) average time from product inquiry to sale. Before the app, agents had to call the office or wait to return to check inventory and pricing — by then the customer had lost interest. With the offline catalogue, the agent could show products, specs, pricing, and availability right there in the field. The 60% increase was tracked by comparing same-period sales data before and after the rollout. The Sales VP validated the number independently.

**35. How did the CMS sync cut delivery time from weeks to minutes?**

> Before: the marketing team created catalogue updates (new products, price changes, promotions) and distributed them via email — someone had to manually process the file, upload it somewhere, and communicate the update to field teams. The whole cycle took 1-3 weeks to reach the field. After: the marketing team publishes changes directly in the CMS, which triggers a pipeline that generates the versioned snapshot and notifies the sync service. The next time any device connects, it downloads the delta. End-to-end: minutes. The bottleneck shifted from distribution to publishing.

---

## DISH App Store

**36. How does OTA installation work technically?**

> The DISH App Store is an internal enterprise app distribution platform — it delivers iOS/Android builds to employees, technicians, and retailers without going through the public App Store or Play Store. Architecture: Lambda handles build upload and metadata storage. DynamoDB tracks builds, device registrations, and access control. React frontend lets users browse and install apps. For iOS, OTA uses the `itms-services://` protocol — a plist manifest hosted on the platform directs the device to download and install the IPA. For Android, it's a direct APK download. Okta SSO authenticates users. Group-based access control determines which apps each user sees.

**37. How did you design group-based access control?**

> Users are assigned to groups in Okta (e.g., "Field Technician," "Retailer," "Engineering"). Each app has a group whitelist. When a user accesses the App Store, the platform reads their Okta group membership via SAML assertion and filters the available apps accordingly. A technician sees field tools and diagnostic apps. A retailer sees sales enablement apps. An engineer sees internal build tools. The control is at the app level, not the file level — granular enough for security, simple enough to administer.

---

## Asset Management & Shift Allowance

**38. Walk me through building the asset management system in a hackathon.**

> Dish ran an internal hackathon — 48 hours, no constraints. I picked asset tracking because I personally experienced the pain: getting a new laptop meant emailing a distribution list and hoping someone responded. I built it over that weekend: Spring Boot backend with REST APIs for asset CRUD, React frontend with search and assignment tracking, Docker + Portainer for containerization, deployed on internal VMs via JFrog. It tracked laptops, monitors, peripherals, and software licenses — check-in/check-out, assignment history, maintenance schedules. Won the hackathon. The real win came after: leadership liked it enough to productize it.

**39. How did you get company-wide adoption?**

> I didn't force it. I demoed it at the hackathon showcase, and other teams started asking to use it. Asset management is one of those problems every company has — nobody enjoys tracking hardware on a spreadsheet. Once two or three teams adopted it, word spread. The HR Spot Award for the Shift Allowance portal followed the same pattern: build something that solves a real pain, and adoption comes from demand, not mandate. The lesson: internal tools succeed when they make someone's job measurably easier.

**40. How did the Shift Allowance portal replace manual Excel workflows?**

> HR was managing shift allowance requests in Excel — employees submitted requests via email, someone manually entered them into a spreadsheet, approvals went back and forth via email, and payroll processed from the spreadsheet. It was error-prone and consumed hours every cycle. I built a Spring Boot + React portal where: employees submit requests through a simple form → managers approve/reject in the same system → HR sees a real-time dashboard → payroll exports clean data. The approval workflow was the key feature — it automated the email chain. HR's processing time dropped from days to minutes. The Spot Award recognized the operational impact.

---

## Kiro Mobile & Custom Agent Skills

**41. How does the mobile monitoring interface work technically?**

> Kiro IDE runs on a workstation with a Chrome DevTools Protocol debug endpoint exposed over LAN. The mobile app (built with React Native) connects to this endpoint and receives live updates — the agent's current task, the code it's editing, the terminal output, the chat conversation. It's essentially a remote desktop for the AI agent, optimized for phone screens. The architecture: Kiro → CDP interface → WebSocket bridge → mobile app. The bridge translates CDP events into a lightweight JSON stream that the mobile app renders as a task feed.

**42. Why CDP (Chrome DevTools Protocol) — why not build a custom API?**

> Because CDP already gives us everything for free: DOM updates, console logs, network requests, breakpoints. Kiro runs in a browser-based IDE, so the protocol was already there. Building a custom API would mean instrumenting Kiro at every layer — more code, more maintenance, more attack surface. CDP gave us 90% of what we needed with zero instrumentation. I added a thin bridge for the remaining 10% — agent task state, session management — but the core visibility came for free.

**43. Walk me through creating a custom agent skill from scratch.**

> Step 1: Document the manual process as a runbook — what does a human do to fix a Snyk vulnerability or migrate a Spring Boot service? Step 2: Identify decision points and validation gates — where does the agent need to stop and ask for human input? Step 3: Codify the runbook into a skill — phases, each with instructions, tools the agent can use, and exit criteria. Step 4: Wire MCP integrations — GitLab for PR creation, Jira for ticket updates, Snyk for vulnerability data, Dynatrace for verification. Step 5: Test with real scenarios and iterate on failures. The skill is never "done" — every failed run improves the playbook.

**44. How do you ensure the agent doesn't make destructive changes?**

> Three layers of protection. (1) MCP scoping — the agent only has access to the tools I explicitly grant. It can create a PR but not merge or deploy. (2) Skill-level gates — the playbook has checkpoints where the agent must pause and wait for human approval before actions like "delete code" or "modify database config." (3) Observability — every action is logged to Dynatrace. If an agent behaves unexpectedly, I see it immediately and can kill the session. The agent is designed to ask permission, not forgiveness.

**45. What's the most surprising failure you've seen from an agent?**

> The agent once "fixed" a test by modifying the assertion to match the broken output — it passed tests, preserved the bug, and created a PR that looked correct on the surface. It took a human code reviewer to catch that the test was testing the wrong thing. That taught me an important lesson: never trust AI-generated test assertions without human review. The agent can implement a fix, but it can't verify the fix independently — that requires a human understanding the intended behavior.

---

## MSys Technologies — General

**46. You stayed 10 years at MSys — unusual in today's market. Why?**

> Because I kept growing. I joined as a Software Engineer and left as a Technical Architect. The company gave me exposure to different clients (Pivot3, Nasuni, NetApp), different domains (storage, virtualization, mobile), and different responsibilities (coding, leading, architecting, client-facing). Every 2-3 years my role changed significantly enough that I was learning. The 5 Best Performer awards tell the story — I wasn't coasting. The moment I stopped growing would have been the moment I left. I'm applying the same filter to my next move.

**47. How did you manage client relationships as a Technical Lead?**

> Translation was the key skill. The client's product team spoke in business outcomes — "reduce provisioning time," "improve dashboard load speed." My engineers spoke in technical terms — "optimize the query," "refactor the component." My job was to bridge that gap: take the business requirement, break it into technical tasks the team could execute, and report progress back in business language the client could understand. I also handled the difficult conversations — scope changes, timeline adjustments, technical debt tradeoffs. The trust came from always being transparent about what we could deliver and when.

---

## Pivot3 — VMware HCI Platform

**48. What was the vSphere UI plugin you built?**

> Pivot3's HCI platform integrates with VMware vSphere — administrators manage storage and virtualization through a single console. I built a ReactJS plugin that embedded Pivot3's storage management UI directly inside the vSphere Web Client. Instead of switching between vSphere and Pivot3's management console, administrators could provision storage, monitor health, and configure policies from within vSphere. The integration was through VMware's Extension SDK — I had to work within their component model, which was restrictive. The lesson: platform integrations are 20% feature work and 80% working within someone else's constraints.

**49. What was the vRealize Orchestrator automation?**

> vRealize Orchestrator is VMware's workflow automation engine. I built automation workflows that reduced manual provisioning effort by 60% for 1000+ storage volumes. Before: an admin manually created volumes, configured RAID levels, assigned them to hosts. After: the admin submitted a request through vRealize, and the orchestrator workflow provisioned the volume, configured the storage policy, attached it to the correct host, and sent a confirmation — all without human intervention. The 60% reduction came from eliminating the back-and-forth between storage admins and VM admins. The automation handled the handoff.

---

## Enterprise Mobile & Test Automation

**50. Tell me about launching Nasuni and Spree Wearables on Play Store.**

> Nasuni is a file storage platform — the Android app gave users mobile access to their Nasuni filer data. Spree Wearables was a fitness/health tracking app with wearable device integration. Both apps went through the full Play Store lifecycle: development, testing, beta distribution, production release, crash monitoring via Firebase Analytics, engagement tracking. The key learning was the Android ecosystem at the time — device fragmentation was a real problem. We used Firebase for crash reporting and prioritized fixes based on crash frequency per device model. The Play Store launch taught me that mobile release engineering (signing, versioning, staged rollouts) is a discipline in itself.

**51. How did the Mobitaz test automation tool work?**

> Mobitaz was a record-and-playback tool for mobile test automation — you performed actions on the device once, the tool recorded them, and you could replay the recording as an automated test. It was built for client demos where we needed to show mobile app functionality reliably without manual execution every time. The technical challenge was reliable element identification across device configurations — screen sizes, OS versions, OEM customizations. We used a combination of accessibility IDs and coordinate-based matching with retry logic.

**52. How did you achieve 100+ Selenium scenarios for NetApp?**

> The NetApp product had a web-based management interface. I led a team that built a Selenium regression suite covering 100+ scenarios — user management, storage provisioning, system monitoring, alert configuration, report generation. The suite was designed to run against every build, cutting manual regression effort by 50%. The key was page object pattern — each screen had a reusable page object class, so when the UI changed, we updated one class instead of 50 test scripts. We also parallelized test execution across multiple browser instances to keep run time under 30 minutes.

---

## Education & Certifications

**53. Your degree is in Information Technology, not Computer Science — does that matter?**

> Not at all. My curriculum covered the fundamentals: data structures, algorithms, operating systems, networking, databases, and software engineering. What mattered more was what I did with it — I was coding from year one, building projects, and learning beyond the syllabus. In 14+ years of working, no one has asked about the distinction between IT and CS. They ask about what I've built.

**54. Google Cloud Professional Data Engineer — how do you use it day-to-day?**

> The certification gave me a structured understanding of GCP's data services — BigQuery, Dataflow, Pub/Sub, Cloud Storage, Bigtable. In practice: I use the concepts for architecture decisions even when the platform is on-prem or AWS. The Data Engineering mindset — treat data as a product, design for scale, think about cost — applies regardless of cloud provider. The cert also gives me credibility when I discuss cloud architecture with platform teams. It's not about using GCP daily; it's about having the framework to reason about data architecture.

---

## AI Workspace & Tooling

**55. You mention Paseo ADE, Codex, Claude Code, Kiro-CLI, OpenCode — which is your primary?**

> Kiro is my daily driver for coding. Paseo ADE is my orchestration layer for managing multiple agents across workspaces. I use Claude Code and Codex through Paseo for specific tasks — Codex for quick analysis, Claude Code for complex reasoning work. OpenCode is a newer tool I'm evaluating. The ecosystem is evolving fast, and I try not to be dogmatic about any single tool. The skill is in knowing which tool fits which problem, not in being an expert in one.

**56. What's "cross-session AI memory persistence" and why does it matter?**

> It means the AI agent remembers context across sessions — decisions, architecture choices, code patterns — without being retold every time. When I start a new task, the agent already knows the project's coding conventions, the team's API standards, the deployment topology. It doesn't ask "what database are you using?" for the tenth time. This matters because it eliminates the biggest productivity killer with AI: context loss. Every session restart used to mean re-establishing context. Cross-session memory makes the AI feel like a team member who's been there from day one.

---

## General / Behavioral

**57. Why did you choose software engineering?**

> I got into coding because I liked building things that worked. In college, I wrote a program that solved a problem my roommate had — it was trivial, but seeing someone actually use something I built was addictive. 14 years later, the motivation is the same: I still get energy from shipping something that makes someone's job easier or solves a problem at scale. The difference is that now I build systems that serve 10M people instead of scripts that serve one roommate.

**58. What's your approach to technical debt?**

> Technical debt is a tradeoff, not a sin. Every team incurs it to ship faster. The question is: are you intentionally taking debt with a plan to pay it down, or are you accruing debt unconsciously? My approach: (1) document the debt as it's incurred — ADR or Jira ticket. (2) Classify it — architectural debt (expensive), code debt (cheap). (3) Allocate some capacity every quarter for architectural debt. (4) For code debt, let the AI handle it — that's what the defect-fixing skill is for. The key insight: if you don't track debt, it compounds. If you track it, you can manage it.

**59. How do you handle a project with unclear requirements?**

> I don't wait for clarity. I start with what I know and build toward what I don't. (1) Define the smallest concrete deliverable — something that provides value and forces decisions. (2) Build it, demo it, get feedback. (3) The feedback is worth more than a spec document because it's grounded in something real. (4) Iterate. The Sling TV migration started with a single API — we migrated one of the 80 Rails endpoints, showed it working, and used that to refine the approach for the remaining 79. Unclear requirements become clear when you show working software.

**60. You've been on both sides — individual contributor and architect. Which do you prefer?**

> I prefer the hybrid role that Staff Engineer gives me: deep technical work on the tooling and architecture, combined with influence across teams. I don't want to be pure IC — I'd miss the impact of defining patterns that multiple teams adopt. And I don't want to be pure architect — I'd miss building things myself. The Staff level is the sweet spot: I write code that matters (MCP servers, agent skills, migration frameworks) and I set direction that scales.

**61. What do you look for when you hire senior engineers?**

> Three signals: (1) Can they reason about tradeoffs? I don't care if they know the "right" answer — I care if they can articulate why one approach is better than another given specific constraints. (2) Have they shipped something end-to-end? Not just "I wrote the API" but "I owned the feature from design to production to on-call." (3) Can they explain something complex to a non-technical person? A senior engineer who can't communicate with product managers or stakeholders will be a bottleneck. If they have those three, the tech stack is learnable.

**62. Where do you see yourself in 5 years?**

> I want to be the person who defines how AI-augmented engineering works at scale — not just at one company, but as a practice. Today I'm doing that at Dish with custom agent skills, MCP integrations, and spec-driven workflows. In 5 years, I want to be at a company where this is a core competency, building the platform and the team that makes AI-assisted development the default, not the exception. The title matters less than the impact: I want to look back and say "we changed how engineering works here."

