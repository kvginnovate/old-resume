# Interview Workbook — Chokkar Gurusamy

> **Principal Engineer Interview Prep — Consolidated Edition**
> Combines: story scripts, resume glossary, 62 Q&As, Principal-level strategy, system design, behavioral STAR, and tricks.

---

## Contents

| Tab | Section | Page |
|---|---|---|
| 1 | Your Story — Scripts & Numbers | 2 |
| 2 | Resume Glossary — One-Liner Per Term | 5 |
| 3 | Resume Q&A — 62 Questions by Section | 11 |
| 4 | Principal-Level Questions | 24 |
| 5 | System Design & Technical Concepts | 29 |
| 6 | Behavioral STAR — Stories & Frameworks | 34 |
| 7 | Strategy & Vision | 37 |
| 8 | Company-Specific Questions | 39 |
| 9 | Quick Reference — Cheat Sheets & Tricks | 40 |

---

## TAB 1: Your Story — Scripts & Numbers

### Open on your desktop. Read, rehearse, record. Do not skip.

---

### 30-Second Elevator (~30s)

> *Staff Engineer at Dish Network — I own the architecture for the My Dish subscriber platform serving 10M+ users. I led the Spring Boot 3 migration using AI (60% productivity gain, promoted to Staff) and transformed Sling TV's 80+ Rails APIs in months instead of years. I built custom AI agents that autonomously fix defects and vulnerabilities, now adopted across 5+ teams. Looking to bring that to [company].*

---

### Standard Script (~130s)

> ***(breathe)*** I'm a Staff Engineer at Dish Network, architecting the subscriber platform that serves 10M+ users — 14+ years in the industry.
>
> ***(breathe)*** My primary role is owning the architecture for the **My Dish** subscriber platform — API-first microservices on Spring Boot 3, deployed on Rancher Kubernetes, maintaining 99.9% uptime with sub-second latency. I drove the org-wide Spring Boot 3 migration across our platform services using AI-powered workflows, automating the remediation of breaking changes across 50K+ lines of code to achieve a 60% productivity gain — that work got me promoted from Lead to Staff.
>
> ***(breathe)*** Separately, I led the transformation of Sling TV — 80+ legacy Ruby on Rails APIs into modern Java microservices using Amazon Q to reverse-engineer 400K lines of legacy code. We delivered in 5 months what was estimated at 18 months, with 85% test coverage and fewer bugs than the original.
>
> ***(breathe)*** Building on those wins, I created custom AI agent skills that automate the entire defect lifecycle — an agent reads a bug from Jira, reproduces it, fixes it, runs tests, and creates a PR. I wired it to MCP servers for GitLab, Jira, Dynatrace, and Snyk so the same pattern handles vulnerability remediation in hours instead of days. What started as my experiment on one team is now used across 5+ engineering teams at Dish — I hold training sessions, document the playbooks, and other teams build their own skills using the framework I established. It was showcased at Dish Ignite 2026.
>
> ***(breathe)*** I also build internal tools that ship — an asset tracking system from a hackathon is now company-wide, a shift allowance portal adopted by every employee. So the arc is: I own large-scale platforms, I modernize them using AI, I codify that capability into reusable agent skills, and I drive adoption across the org.

---

### Full Career Intro (~5-6 min)

See `interview_prep.md` lines 10-87 for the full narrative with all 16 breath-delimited sections. Use when they ask "walk me through your career in detail."

---

### Key Numbers to Have Ready

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
| MSys tenure | 10 years, SE → Architect | 5x Best Performer awards |
| Promotion rate (MSys) | SE → Senior → TL → Architect | 4 promotions in 10 years |

---

### Delivery Tips

- **Pacing:** Use the breath points. Speak at conversation pace, not presentation pace.
- **Interruption is good.** If they ask a follow-up mid-script, you've hooked them. Go with it.
- **Land these exactly:** "Staff Engineer", "10M+ subscribers", "Spring Boot 3 migration using AI", "custom agent skills that autonomously fix defects", "Dish Ignite 2026". Everything else is yours to paraphrase.
- **The unspoken message:** Most engineers can't say they built agents that autonomously fix bugs. That's your edge.

---

## TAB 2: Resume Glossary — One-Liner Per Term

> Every term on your resume with a 1-2 sentence explanation. If asked "what is X?" on any resume line, this is your answer.

---

### Professional Summary

| Term | One-Liner for Interview |
|---|---|
| **Distributed systems** | "I design systems where each service runs independently, communicates via APIs or events, and can fail without taking down the whole platform." |
| **Rancher-managed Kubernetes** | "Rancher gives us a single pane of glass to manage multiple K8s clusters — deploy, scale, monitor, rollback." |
| **Kiro spec-driven development** | "You write the contract first — OpenAPI spec, test cases. Kiro generates the Spring Boot service, the tests, the docs. Humans review and ship." |
| **Spring Boot 3 migration** | "Spring Boot 2 reached end-of-life — no security patches, blocking dependency upgrades. I used AI to automate the migration across 12 services." |
| **API design org-wide** | "Every team writes OpenAPI specs before code. Shared contract repo. Breaking changes require a new version and migration plan." |
| **Architectural reviews** | "I sit in on other teams' architecture discussions — not to approve, but to ask the hard questions they might miss." |
| **Incident response** | "I led the incident response process — PagerDuty alerts, runbooks, post-mortems with action items." |
| **Org-wide migrations** | "Org-wide means you can't force anyone. You build the guide, do the first one yourself, show the data, and let adoption follow." |

---

### Technical Skills — Languages & Frameworks

| Term | One-Liner for Interview |
|---|---|
| **Java** | "Java is my core — 8+ years, Spring Boot ecosystem." |
| **Kotlin** | "Kotlin for Android native apps. Less boilerplate, null safety, coroutines." |
| **TypeScript** | "TypeScript on the frontend — React, Next.js. Static types catch bugs before runtime." |
| **Python** | "Python for automation scripts, data analysis, and quick prototypes." |
| **Spring Boot** | "Spring Boot is my default for backend services. Embedded Tomcat, auto-config, actuator for health checks." |
| **Spring Cloud** | "Spring Cloud adds distributed-system primitives: config server, service discovery, API gateway patterns." |
| **Hibernate** | "Hibernate for ORM. Migrated from 5 to 6 in the Boot 3 upgrade. Lazy loading, caching, query optimization." |
| **ReactJS** | "React for web frontends. Component-based, state management via hooks or Redux." |
| **Next.js** | "Next.js adds server-side rendering — faster initial load, better SEO." |
| **React Native** | "React Native for cross-platform mobile — share code between Android and iOS. Used for Kiro Mobile and Field Catalogue." |
| **Android SDK** | "Native Android SDK for the early apps (Nasuni, Spree). Deep integration with device features." |
| **JUnit** | "JUnit for automated testing. Mandated 85%+ coverage as a CI gate." |

---

### Distributed Systems

| Term | One-Liner for Interview |
|---|---|
| **Microservices Architecture** | "Each service owns a domain capability and its own data store. Independent deploy, independent scaling." |
| **Circuit Breaker** | "If service A calls B and B is failing, the circuit breaker trips — instead of timing out every request, it fails fast. B recovers, breaker closes." |
| **API Gateway** | "API Gateway is the front door — route requests, authenticate, rate-limit, aggregate responses." |
| **REST APIs** | "Stateless, resource-oriented HTTP APIs. Every service exposes REST endpoints documented via OpenAPI." |

---

### Infrastructure

| Term | One-Liner for Interview |
|---|---|
| **Docker** | "Docker containers package the app + its dependencies. Same image runs on dev, test, prod." |
| **Kubernetes** | "K8s deploys and manages containers. If one crashes, it restarts. If load increases, it scales." |
| **Rancher** | "Rancher manages our K8s clusters — deploy apps via UI or API, manage access, view logs and metrics." |
| **AWS S3** | "S3 for object storage — telemetry data, build artifacts." |
| **AWS DynamoDB** | "DynamoDB for high-throughput, low-latency key-value access." |
| **Firebase** | "Firebase for real-time sync in mobile apps. Auth, Firestore, analytics." |
| **GCP** | "GCP for cloud services — BigQuery, Cloud Functions, Pub/Sub." |

---

### Observability & DevOps

| Term | One-Liner for Interview |
|---|---|
| **Dynatrace** | "Dynatrace traces every request across service boundaries. 30-minute incident diagnosis → 2 minutes. Built a custom MCP server for it." |
| **Prometheus** | "Prometheus scrapes metrics from services. Used alongside Dynatrace for open-source monitoring." |
| **ELK Stack** | "ELK for log aggregation — search across all service logs during incident analysis." |
| **GitLab CI/CD** | "GitLab CI/CD runs on every push — build, Snyk scan, run tests, deploy to Rancher." |
| **Snyk** | "Snyk scans every build for CVEs. Triaged by exploitability. Built a MCP server so AI agents create same-day fix PRs." |

---

### AI Agent Tooling

| Term | One-Liner for Interview |
|---|---|
| **Antigravity** | "AI coding assistant. Evaluated it as part of the internal AI tools group." |
| **Kiro (Spec-Driven Dev)** | "Kiro takes a spec (OpenAPI, requirements) and generates the implementation with tests. Used daily for migrations, fixes, new features." |
| **Paseo** | "Paseo orchestrates multiple AI agents so they don't conflict. Manages worktrees, file locks, scheduling." |
| **Orca** | "Terminal-based interface for AI agent workflows — the cockpit for your local AI stack." |
| **OpenCode** | "AI coding assistant in the OMP ecosystem. Used alongside Kiro." |
| **OMP** | "OMP connects AI models, providers, and agents. I use it to configure and route between different AI backends." |
| **psmux-terminal** | "Terminal multiplexer for managing multiple AI agent sessions simultaneously." |
| **Custom Agent Skills** | "Pre-built playbooks. Defect-fix: agent reads Jira, reproduces bug, fixes, tests, creates PR. 5 phases with guardrails." |
| **LLM Workflows** | "Structured multi-step agent sequences — read code → plan → implement → verify → create PR. Each step uses the right tool." |

---

### MCP (Model Context Protocol)

| Term | One-Liner for Interview |
|---|---|
| **MCP** | "MCP is how agents talk to tools. Each server exposes capabilities — read Jira, search GitLab, query Dynatrace — with scoped permissions." |
| **Jira MCP** | "Agent reads bug descriptions from Jira, creates tickets for findings, updates status as it works." |
| **GitLab MCP** | "Agent clones repos, searches code, reads MRs, creates fix branches and merge requests." |
| **GitHub MCP** | "Same pattern as GitLab MCP — read code, search issues, create PRs." |
| **Firebase MCP** | "Agent reads Firestore collections, manages Firebase Auth, deploys Cloud Functions — all with scoped permissions." |
| **Google Cloud MCP** | "Agent queries GCP resources — BigQuery tables, Cloud Storage buckets, Cloud Run services." |

---

### Architecture Terms

| Term | One-Liner for Interview |
|---|---|
| **System Design** | "System design is about making intentional tradeoffs — consistency vs. availability, sync vs. async, SQL vs. NoSQL — based on the problem you're solving." |
| **DDD (Domain-Driven Design)** | "DDD means the code structure mirrors the business structure. Each domain (billing, content, entitlements) is its own service with its own language." |
| **Microservices Patterns** | "Patterns like Saga for distributed transactions, Strangler Fig for incremental migration, Circuit Breaker for fault isolation." |
| **OpenAPI** | "OpenAPI specs define the contract — endpoints, request/response schemas, error codes. Spec-first means the contract is agreed before coding." |
| **ADR (Architectural Decision Records)** | "ADRs capture why a decision was made and what alternatives were considered. Prevents the same debate from happening twice." |

---

### Project-Specific Terms

| Term | One-Liner for Interview |
|---|---|
| **GemFire** | "In-memory distributed cache. Sits between services and DB. Hot data served from memory instead of hitting PostgreSQL every time." |
| **Spring Boot 3 breaking changes** | "Jakarta namespace (javax.\* → jakarta.\*), Security config class replaced, Hibernate 5 → 6. All breaking, all automatable." |
| **GC behavior** | "Spring Boot 3 on JDK 17 meant generational ZGC — shorter GC pauses, more predictable latency under load." |
| **Snyk triaging by exploitability** | "We triaged: critical (exploit exists) → fix same-day, High → this sprint, Medium → backlog, Low → accept risk." |
| **APM** | "APM tracks how your app performs from the user's perspective. Dynatrace APM shows every request's path and latency." |
| **Distributed tracing** | "Every request gets a trace ID across 5+ services. Dynatrace stitches all spans into one trace — you see the exact hop that failed." |
| **PagerDuty** | "PagerDuty pages the on-call engineer when Dynatrace detects an anomaly. Escalates if no response." |
| **Runbooks** | "Documented procedures per incident type — symptoms, diagnosis steps, fix commands." |
| **WebSocket** | "Full-duplex persistent connection. Server pushes GitLab MR status updates to phone — no polling." |
| **Dish Ignite 2026** | "Internal AI demo day at Dish. Live demo of agent fixing a bug from Jira. Got VP buy-in to scale." |
| **Offline-first mobile** | "App works without internet. SQLite local cache. Syncs compressed deltas when online." |
| **ColdFusion** | "Legacy Adobe technology — tag-based, mixed presentation and logic. Hard to maintain, hard to hire for." |
| **Codefest 2023** | "48-hour hackathon. Built Asset Management (Spring Boot + React), containerized, won. Productized company-wide." |
| **vSphere UI Plugin** | "ReactJS plugin embedded inside VMware vSphere. Admins manage storage from existing tool — no context switching." |
| **vRealize Orchestrator** | "VMware automation. One-click workflow replaced manual per-volume provisioning." |
| **HCI (Hyper-Converged Infrastructure)** | "Storage and compute on the same box. No separate SAN." |
| **Mobitaz** | "In-house mobile test automation. Record once, replay on 10 devices. Used in client demos." |
| **Selenium regression suite** | "Automated browser tests for NetApp. 100+ scenarios, ran against every build, caught regressions before release." |

---

### AI Innovation

| Term | One-Liner for Interview |
|---|---|
| **Gemini** | "Google's LLM. Trialed for code generation and review. Compared against other models for accuracy and cost." |
| **Open-source LLMs** | "Self-hosted models (Llama, Mistral) for use cases where data can't leave Dish's network." |
| **AI evaluation group** | "Internal panel at Dish that trials and benchmarks AI dev tools. I'm on it — helps Dish stay ahead without chasing every hype cycle." |

---

## TAB 3: Resume Q&A — 62 Questions by Section

> **Pattern for every answer:** Context → Action → Outcome → Lesson.

---

### Professional Summary (4 Questions)

**Q1: What does "end-to-end solution architecture" mean to you? Give a concrete example.**

> To me it means I own the full lifecycle: understanding the business requirement, defining the API contracts, choosing the technology stack, designing the data model, wiring observability, setting up CI/CD, and being on-call when it breaks. A concrete example: My Dish subscriber platform — I didn't just design the APIs. I defined how frontend, backend, and shared services integrate. I set the OpenAPI standards. I established security gates with Snyk. I integrated Dynatrace for observability. And when there's an incident at 2 AM, I'm in the call. End-to-end means you can't hand off the hard parts.

**Q2: You mention "AI governance" in your summary — what does that look like in practice?**

> Concrete rules: (1) AI can generate code and create PRs, but never merges to production without human review. (2) Every AI action is logged and traceable — I built the Dynatrace MCP server for exactly this. (3) AI agents follow structured playbooks with approval gates at each phase — they stop before destructive operations. (4) We audit AI-generated code for security compliance via Snyk before it reaches staging. Governance isn't about restricting AI — it's about making its output auditable and reversible.

**Q3: How do you balance hands-on coding with architecture work at Staff level?**

> About 40% hands-on, 60% architecture and mentorship. The hands-on part isn't feature code — it's building the tooling that makes the team faster: AI migration workflows, MCP servers, agent skills. The architecture part is ADRs, design reviews, integration patterns, incident response. I stay hands-on because I can't design something I don't understand at the code level, and I can't build trust with engineers if I'm not in the trenches.

**Q4: You presented a live demo to VP+ leadership — what was that experience like?**

> I demonstrated Kiro spec-driven development: wrote an OpenAPI spec in real time, the agent generated the Spring Boot service with tests, and the subagent orchestrated GitLab MR creation and Dynatrace monitoring setup — all in under 20 minutes. The VPs could see the code being written, tested, and deployed. The reaction was positive because it wasn't a slide deck — it was a live demo of working software.

---

### Technical Skills (4 Questions)

**Q5: You list 6 languages, 12+ frameworks, 8 databases, 3 clouds — which are genuinely your strongest?**

> Java and Spring Boot are my core — that's what I've lived in for the last 8 years. Everything else is situational: Kotlin for Android, TypeScript for React frontends, Python for automation. For databases, PostgreSQL is my default. The range isn't about being an expert in everything — it's about being able to design systems across the stack and know what questions to ask.

**Q6: What's the difference between Kiro and Paseo in your workflow?**

> Kiro is my daily driver for AI coding — spec-driven development, agent skills, MCP integrations. Paseo is the orchestration layer — managing multiple agents across workspaces, file-locking so they don't conflict. Kiro = driver. Paseo = traffic controller.

**Q7: How do you stay current with so many technologies?**

> I learn what my current problem demands. When Dish needed Spring Boot 3 migration, I deep-dived into the breaking changes. When I needed MCP servers, I learned the protocol spec. The rest I follow at a high level — enough to know what's possible and where to look when I need it.

**Q8: You list both SQL and NoSQL — when do you pick one over the other?**

> PostgreSQL is my default for anything with relations, transactions, or reporting. MongoDB when data shape is unpredictable. DynamoDB when I need single-digit-millisecond reads at massive scale with a known access pattern. GemFire for hot-path data that can't tolerate DB latency. The important thing is knowing what each is good at.

---

### Dish Network — General (3 Questions)

**Q9: You were promoted from Lead to Staff — what changed in your role?**

> As Lead, I owned the architecture for my team's services. As Staff, I own the architecture patterns across multiple teams — integration standards, security gates, observability framework. I also became responsible for org-wide initiatives: Spring Boot 3 migration, Snyk standards, AI-augmented development practice. The promotion recognized that I was already operating at that level.

**Q10: You won Technical Excellence Awards two years in a row — what for?**

> 2024: Spring Boot 3 migration and AI-powered modernization workflow (60% productivity gain). 2025: Sling TV transformation and custom MCP servers (Dynatrace, Snyk) that became the foundation for AI-augmented SDLC.

**Q11: What's a CPAW Award and Spot Award?**

> CPAW is internal recognition for delivery impact — I received it for the Paperless Agreement migration across 23 integrations. Spot Awards are for significant immediate contributions — Shift Allowance portal (automated HR's manual Excel) and leading a critical incident recovery.

---

### My Dish App — Subscriber Platform (10 Questions)

**Q12: Walk me through the architecture of the subscriber platform.**

> REST microservices on Spring Boot 3, deployed on Rancher-managed Kubernetes. Each service owns a domain — subscriber management, billing, device activation, plan configuration. OpenAPI-first contracts. Services communicate via REST (sync) and Kafka (event-driven). API Gateway for routing and rate limiting. Resilience4j for circuit breakers. Dynatrace traces every request. PostgreSQL per service, GemFire distributed cache for hot-path reads. CI/CD: GitLab → Docker → Snyk → Rancher. 99.9% uptime, sub-second latency.

**Q13: How do you maintain 99.9% uptime with sub-second latency?**

> Designed in: circuit breakers isolate failures. Bulkheads prevent noisy neighbor problems. GemFire caching keeps hot-path reads off the database. Kafka absorbs traffic bursts. Operations: blue-green deployment on Rancher, gated on Snyk scans and performance tests. Observability: Dynatrace distributed tracing. Incident response: documented runbooks, on-call rotation.

**Q14: How did you measure the 60% productivity gain from AI migration?**

> Time-to-complete for migration tasks. Before AI: 2 weeks for a mid-size service. With Kiro spec-driven workflow: ~3 days. Tracked across 12 services with a dashboard showing lines changed automatically vs manually, hours saved, defect rate. Consistent enough that leadership approved scaling.

**Q15: Tell me about the custom dashboard you built for AI code changes.**

> Lightweight React dashboard pulling data from GitLab and Kiro's output. Showed which services were migrated, AI-generated vs human-modified lines, test pass rate, time saved per service. Purpose: leadership visibility that AI was shipping verified code, not noise.

**Q16: How do you enforce 85%+ test coverage?**

> CI gate — pipeline fails if coverage drops below 85%. But leading practice is: mandate tests at API contract level before implementation. OpenAPI spec → Postman collection → JUnit tests. When you spec-test before coding, coverage follows naturally.

**Q17: How does your Dynatrace MCP server work?**

> Custom MCP server giving AI agents read-only access to Dynatrace. Agent queries: "show me the distributed trace for this failed request," "what's the error rate on service X?" Agent analyzes the trace, suggests root cause, creates Jira ticket. Compresses diagnosis from 30 minutes to 2 minutes.

**Q18: Your Snyk MCP server achieves same-day vulnerability fixes — how?**

> Flow: Snyk scans and reports vulnerability → MCP server fetches advisory → AI agent applies fix from Snyk's recommendation → verifies with tests and rescan → creates PR. Engineer reviews and approves. Detection to PR in hours — because the agent applies the fix mechanically, it doesn't guess.

**Q19: What are your API-first / OpenAPI development patterns?**

> (1) Contract first — write spec before code. (2) Shared contract repo, versioned, reviewed. (3) Spec drives everything — code generation, test generation, documentation. (4) Breaking changes require new API version + migration plan.

**Q20: What "integration patterns" did you define across frontend, backend, and shared services?**

> (1) Backend-to-backend: REST + circuit breakers for sync, Kafka for event-driven. (2) Frontend-to-backend: API Gateway + BFF layer that aggregates microservice responses. (3) Shared services: common library for auth, logging, Dynatrace instrumentation. Reduced integration tax — teams stopped inventing their own approach.

**Q21: How does AWS Athena fit into your telemetry stack?**

> Dynatrace gives real-time traces. Athena gives deep analysis across months of telemetry data stored in S3 — trend analysis, capacity planning, cross-application correlation. Standard SQL, no infrastructure to provision. Serverless model means we only pay for queries run.

---

### Sling TV (6 Questions)

**Q22: Walk me through the strategic decision to transform 80+ Rails APIs.**

> The Rails monolith was the bottleneck. Adding features took weeks. Deployment was risky. Business needed to ship faster. Strategy: don't rewrite blindly — reverse-engineer the entire codebase first (Amazon Q), group into bounded contexts (DDD), migrate one domain at a time via Strangler Fig pattern.

**Q23: What was the hardest part of the migration?**

> Data consistency. Splitting a monolith's database into per-service databases loses ACID transactions across domains. Solved with Saga pattern on Kafka — each service publishes events, downstream services listen, compensation logic rolls back on failure. Tested with chaos engineering.

**Q24: How did Amazon Q reverse-engineer 400K+ lines of legacy code?**

> Amazon Q ingested the entire Rails codebase — models, controllers, routes, views, database schema. It identified API endpoints, request/response shapes, DB queries, business logic flows. Generated OpenAPI specs from routes and Java microservice skeletons from specs. Also generated unit tests from existing test patterns.

**Q25: What were Amazon Q's limitations?**

> (1) Ruby idioms (metaprogramming, dynamic dispatch) didn't translate cleanly to Java. (2) Business rules embedded in Rails callbacks needed human interpretation. (3) Test assertions were sometimes tautological. (4) Performance-critical paths needed manual optimization. AI handles 80% mechanical — 20% domain understanding is still human.

**Q26: How did you maintain 85% coverage across 10K+ auto-generated tests?**

> Ran AI-generated tests against the legacy system to validate they caught regressions. Kept tests that passed against both old and new code. Manual review on critical paths (payment, entitlement). AI got us to 85% fast — human review ensured it meant something.

**Q27: The 70% productivity gain — how was that calculated?**

> Traditional rewrite estimate: 18 months, 12 engineers. AI-assisted approach: 5 months, same team. 70% time savings. But real win was quality — AI-generated code had fewer bugs than manual code because it followed the spec precisely. Human errors came at integration points, caught by contract testing.

---

### Dish Paperless Agreement (3 Questions)

**Q28: What did migrating ColdFusion to Spring Boot involve?**

> ColdFusion is tag-based legacy Adobe tech — mixes HTML and server logic. Rebuilding meant: reverse-engineering business logic from spaghetti pages, designing proper layered architecture (controller → service → repository), building REST APIs, orchestrating 23 downstream integrations + 7 SFTP distribution targets. Offline was hardest — field agents sign agreements in basements with no signal.

**Q29: 23 integrations and 7 SFTP targets — how did you manage that complexity?**

> Spring Batch-based orchestration layer. Generic SFTP client service configurable per target (host, credentials, path, format). Adding a new integration = config change, not code change. Dynatrace monitored every path — immediate visibility on failures.

**Q30: How did you handle offline capability for field agents?**

> Agreements cached locally (SQLite). Field agent fills, signs, queues locally. Syncs in background when online — server authoritative for agreement state, device authoritative for captured signatures. Signatures captured as encrypted bitmap locally, backend reconstructs PDF after sync.

---

### STB Health Monitor (3 Questions)

**Q31: Walk me through the DMZ gateway design.**

> STB Health collects telemetry from 10M+ devices. DMZ gateway sits between internet and internal network. Devices authenticate via JWT (Cognito for device identity, Okta for technician identity). Gateway validates token, normalizes payload, publishes to internal Kafka topic. Gateway never touches internal DB or services directly.

**Q32: QR code scanning at 10M devices — how did you handle scale?**

> QR code encodes serial number + one-time challenge token. Scan → DMZ gateway validates → short-lived JWT issued → device streams telemetry. QR scan is identity bootstrap — subsequent telemetry uses JWT without re-scanning. Kafka absorbs telemetry stream regardless of burst rate.

**Q33: How did you handle OAuth lifecycle and certificate management for 10M devices?**

> Each STB has a unique certificate installed at manufacturing. Certificate authenticates to Cognito → JWT issued (24h TTL). Device refreshes token automatically before expiry. Certificate rotation: device requests new certificate from internal CA when current one is within 30 days of expiry. Old cert continues working until new one confirmed. Fully automated — no manual management at 10M scale.

---

### Field Catalogue (3 Questions)

**Q34: The app is 100% offline-capable — what's the sync architecture?**

> Local SQLite is source of truth on device, not server. CMS publishes catalogue updates as versioned JSON snapshots. Device checks for newer version when online, downloads compressed delta (changed records only), applies locally. Reads are always from SQLite — zero network calls, zero latency. Writes (sales orders) queued locally, synced when online.

**Q35: How did you measure the 60% increase in on-site technical sales?**

> Sales team tracked close rate and time-to-sale before and after. Before the app: agents had to call office or wait to check inventory — customers lost interest. After: catalogue with specs, pricing, availability right there in the field. Sales VP validated the numbers independently.

**Q36: How did the CMS sync cut delivery time from weeks to minutes?**

> Before: email-based distribution, manual processing, 1-3 weeks to reach field. After: marketing publishes in CMS → pipeline generates versioned snapshot → sync service notified. Next device connection = download delta. End-to-end: minutes.

---

### DISH App Store (2 Questions)

**Q37: How does OTA installation work technically?**

> Internal enterprise app distribution platform — no App Store/Play Store. Lambda handles build upload, DynamoDB tracks builds and access control, React frontend for browsing/installing. iOS: `itms-services://` plist manifest. Android: direct APK download. Okta SSO for auth. Group-based access control.

**Q38: How did you design group-based access control?**

> Users assigned to groups in Okta. Each app has a group whitelist. Platform reads Okta group membership via SAML assertion and filters visible apps. Technician sees field tools. Retailer sees sales apps. Engineer sees internal builds.

---

### Asset Management & Shift Allowance (3 Questions)

**Q39: Walk me through building Asset Management in a hackathon.**

> 48 hours. Spring Boot backend for asset CRUD, React frontend with search, Docker + Portainer, deployed on internal VMs via JFrog. Tracked laptops, monitors, peripherals, software licenses — check-in/out, assignment history, maintenance. Won. Leadership productized it.

**Q40: How did you get company-wide adoption?**

> Didn't force it. Demoed at hackathon showcase. Teams started asking to use it because asset tracking is a pain everyone has. Adoption comes from demand, not mandate.

**Q41: How did the Shift Allowance portal replace manual Excel workflows?**

> HR was managing shift allowance requests in Excel — email submission, manual entry, email approvals, payroll exported from spreadsheet. Built Spring Boot + React portal: submit request → manager approves → HR dashboard → clean data export. Approval workflow automated the email chain. HR processing time: days → minutes.

---

### Kiro Mobile & Custom Agent Skills (5 Questions)

**Q42: How does the mobile monitoring interface work technically?**

> Kiro runs on a workstation with CDP debug endpoint exposed over LAN. Mobile app (React Native) connects to this endpoint, receives live agent updates — current task, code being edited, terminal output, chat. Architecture: Kiro → CDP interface → WebSocket bridge → mobile app.

**Q43: Why CDP — why not build a custom API?**

> CDP already gives us DOM updates, console logs, network requests, breakpoints for free — Kiro runs in a browser-based IDE. Custom API would mean instrumenting at every layer. CDP gave 90% with zero instrumentation. I added a thin bridge for the remaining 10%.

**Q44: Walk me through creating a custom agent skill from scratch.**

> (1) Document manual process as runbook. (2) Identify decision points + validation gates. (3) Codify into skill phases with instructions, tools, exit criteria. (4) Wire MCP integrations — GitLab, Jira, Snyk, Dynatrace. (5) Test with real scenarios, iterate on failures. Skill is never "done" — every failed run improves the playbook.

**Q45: How do you ensure the agent doesn't make destructive changes?**

> Three layers: (1) MCP scoping — agent only has access to explicitly granted tools. Can create PR, never merge or deploy. (2) Skill-level gates — pause for human approval before destructive actions. (3) Observability — every action logged to Dynatrace. Agent designed to ask permission, not forgiveness.

**Q46: What's the most surprising failure you've seen from an agent?**

> Agent once "fixed" a test by modifying the assertion to match the broken output — passed tests, preserved the bug, looked correct on the surface. Lesson: never trust AI-generated test assertions without human review. Agent can implement a fix but can't verify intent independently.

---

### MSys Technologies (2 Questions)

**Q47: You stayed 10 years at MSys — unusual in today's market. Why?**

> Because I kept growing. Joined as SE, left as Technical Architect. Different clients (Pivot3, Nasuni, NetApp), different domains (storage, virtualization, mobile), different responsibilities (coding, leading, architecting, client-facing). Every 2-3 years my role changed significantly. 5 Best Performer awards tell the story — I wasn't coasting.

**Q48: How did you manage client relationships as a Technical Lead?**

> Translation was the key skill. Client spoke in business outcomes ("reduce provisioning time"). Engineers spoke in technical terms ("optimize the query"). My job was to bridge that gap. Also handled difficult conversations — scope changes, timeline adjustments, debt tradeoffs. Trust came from always being transparent.

---

### Pivot3 — VMware HCI Platform (2 Questions)

**Q49: What was the vSphere UI plugin you built?**

> ReactJS plugin embedded inside VMware vSphere Web Client. Administrators could provision storage, monitor health, configure policies from within vSphere — no context switching. Built on VMware's Extension SDK, which was restrictive. Lesson: platform integrations are 20% feature, 80% working within someone else's constraints.

**Q50: What was the vRealize Orchestrator automation?**

> Automated workflows for HCI volume provisioning. Before: admin manually created volumes, configured RAID, assigned to hosts. After: submit request → orchestrator provisions, configures, attaches, confirms. 60% reduction in provisioning effort for 1000+ volumes.

---

### Enterprise Mobile & Test Automation (3 Questions)

**Q51: Tell me about launching Nasuni and Spree Wearables on Play Store.**

> Nasuni: Android app for mobile access to Nasuni filer data. Spree: fitness/health app with wearable integration. Full Play Store lifecycle — development, beta, production, crash monitoring (Firebase), staged rollouts. Key learning: Android device fragmentation was real. Prioritized fixes by crash frequency per device model.

**Q52: How did Mobitaz test automation tool work?**

> Record-and-playback for mobile. Perform actions once on device → tool records → replay as automated test on multiple devices. Built for client demos. Technical challenge: reliable element identification across screen sizes, OS versions, OEM customizations. Used accessibility IDs + coordinate matching with retry.

**Q53: How did you achieve 100+ Selenium scenarios for NetApp?**

> Led a team building a Selenium regression suite covering 100+ scenarios — user management, storage provisioning, monitoring, alerting, reporting. Page object pattern meant UI changes updated one class instead of 50 scripts. Parallel execution across multiple browsers kept run time under 30 minutes.

---

### Education & Certifications (2 Questions)

**Q54: Your degree is in Information Technology, not Computer Science — does that matter?**

> Not at all. Curriculum covered fundamentals — data structures, algorithms, OS, networking, databases. What mattered was what I did with it. In 14+ years, no one has asked about IT vs CS distinction. They ask about what I've built.

**Q55: Google Cloud Professional Data Engineer — how do you use it day-to-day?**

> Certification gave me structured understanding of GCP's data services — BigQuery, Dataflow, Pub/Sub, Bigtable. The Data Engineering mindset — treat data as product, design for scale, think about cost — applies regardless of cloud provider. The cert gives credibility when I discuss data architecture with platform teams.

---

### AI Workspace & Tooling (2 Questions)

**Q56: You mention Paseo ADE, Codex, Claude Code, Kiro-CLI, OpenCode — which is your primary?**

> Kiro is my daily driver for coding. Paseo is the orchestration layer. Claude Code and Codex through Paseo for specific tasks. The ecosystem evolves fast — the skill is knowing which tool fits which problem, not being an expert in one.

**Q57: What's "cross-session AI memory persistence" and why does it matter?**

> AI remembers context across sessions — decisions, architecture choices, code patterns — without being retold every time. When I start a new task, the agent knows the project's coding conventions, API standards, deployment topology. Eliminates the number one productivity killer with AI: context loss.

---

### General / Behavioral (6 Questions)

**Q58: Why did you choose software engineering?**

> I liked building things that worked. In college, I wrote a program that solved a problem my roommate had — trivial, but seeing someone use something I built was addictive. 14 years later, the motivation is the same: building systems that serve 10M people instead of scripts that serve one roommate.

**Q59: What's your approach to technical debt?**

> Debt is a tradeoff, not a sin. My approach: (1) Document as incurred — ADR or Jira ticket. (2) Classify — architectural debt (expensive) vs code debt (cheap). (3) Allocate capacity every quarter for architectural debt. (4) Let AI handle code debt — that's what the defect-fixing skill is for. If you don't track it, it compounds. If you track it, you can manage it.

**Q60: How do you handle a project with unclear requirements?**

> I don't wait for clarity. (1) Define smallest concrete deliverable that forces decisions. (2) Build it, demo it, get feedback. (3) The feedback is worth more than a spec document because it's grounded in something real. (4) Iterate. Sling TV started with one API — migrated one Rails endpoint, showed it working, used that to refine the rest.

**Q61: You've been on both sides — IC and architect. Which do you prefer?**

> The hybrid Staff Engineer role: deep technical work (MCP servers, agent skills, migration frameworks) combined with influence across teams. Don't want pure IC (miss impact of defining patterns) and don't want pure architect (miss building things). Staff is the sweet spot.

**Q62: What do you look for when you hire senior engineers?**

> Three signals: (1) Can they reason about tradeoffs — not "right answer" but can they articulate why one approach wins given specific constraints? (2) Have they shipped end-to-end — owned from design to production to on-call? (3) Can they explain something complex to a non-technical person? Three signals present → tech stack is learnable.

**Q63: Where do you see yourself in 5 years?**

> I want to be the person who defines how AI-augmented engineering works at scale — not just at one company, but as a practice. Today at Dish with agent skills, MCP integrations, spec-driven workflows. In 5 years, at a company where this is core competency, building the platform and team that makes AI-assisted development the default. The title matters less than the impact: "we changed how engineering works here."

---

## TAB 4: Principal-Level Questions

### The Staff → Principal Shift

| Dimension | Staff | Principal |
|---|---|---|
| Scope | Multiple teams | Organization / company-wide |
| Influence | Cross-team | C-level visible |
| Time horizon | 6–12 months | 2–5 years |
| Decisions | Technical architecture | Technical strategy + org investment |
| Audience | Eng leadership | VP+ |

**Key insight:** Your Staff-level Q&As (Tab 3) will be asked at Principal interviews too — but at a higher altitude. Not "how you did it," but "how you decided to do it, how you measured business impact, and what you'd do differently."

---

### Technology Strategy & Roadmap

**Q: What should our 3-year technical roadmap for this platform look like?**

Framework:
1. Current state assessment — what works, what's accruing debt, what's blocking velocity
2. Business alignment — what does the business need in 3 years?
3. Phased evolution — Y1: critical migrations + quick wins. Y2: platform consolidation. Y3: differentiation
4. Exit criteria per phase — how do you know when to stop?

For Dish context: What comes after Rancher K8s? GemFire → Redis? API governance evolution from manual to automated? AI practice from team-level to platform-level?

**Q: How do you decide which technical debt to prioritize?**

1. Classify by risk — security (CVEs), velocity (slow CI/change), reliability (incidents), cost (inefficient infra)
2. Rank by business impact — debt blocking feature > debt making code ugly
3. Create a debt budget — X% of each sprint
4. Know when to carry debt — if it has an expiration date

**Q: Your AI practice is used by 5 teams now. What would it take to scale to 20 teams?**

1. Platform, not project — self-service onboarding, reference implementations, docs
2. Internal champions — train one per team, train the trainers
3. Health metrics — adoption rate, time saved, defect rate, satisfaction
4. Governance at scale — central guardrails, team-level customization
5. Feedback loop — every adopter improves the playbook

**Q: Where should our infrastructure strategy go next?**

Have a view on 2-3 of: container orchestration evolution, caching strategy (GemFire vs Redis), observability consolidation (OpenTelemetry?), multi-cloud readiness.

---

### Organizational Design

**Q: How would you organize engineering teams to scale this platform?**

1. DDD-driven team boundaries — each bounded context is one team owning its domain end-to-end
2. Platform team — small, owns shared concerns (API gateway, observability, CI/CD, security). Metric: product team velocity
3. API governance — centralized standards, decentralized execution. Platform maintains contract repo + enforcement gates
4. Team size — 6-8 engineers. Larger = split domain. Smaller = combine or under-invested

**Q: Your platform team ships internal services. How do you prevent it from becoming a bottleneck?**

1. Self-service first — platform team builds tooling, not bespoke solutions
2. SLAs with teeth — if SLAs aren't met, product teams have escalation path
3. Don't build what you can buy — unless differentiation is strategic
4. Listening tours — platform team embedded with product teams quarterly. Fix top 3 pain points

**Q: Two teams disagree on API design standards. How do you resolve it without authority?**

1. Understand both positions — talk to each team lead individually first
2. Bring data — what's the current org pattern? What's migration cost of each option?
3. Focus on principles, not preferences — "I don't care if you use Kafka or RabbitMQ. I care about: events documented in schema registry, consumers can handle retries, producer owns the schema"
4. Tier decisions — some non-negotiable (security, observability), some team preference (language, framework)
5. Document the outcome — prevents same debate recurring

---

### Business & Executive Alignment

**Q: Explain distributed tracing to a non-technical VP.**

> "Every customer request touches 5-6 services. When something fails, we used to spend 30+ minutes manually log-hopping. Distributed tracing attaches a unique ID to every request that follows it through every service. When something fails, we pinpoint the exact service and API call within 30 seconds. Business impact: P1 incidents resolved 20x faster, fewer customer-facing outages, proactive detection of degrading services before customers complain."

**Q: How do you connect engineering investment to business outcomes?**

Frame each engineering story starting with business goal:

> "Spring Boot 2 to 3 cost 5 months. Business case: (1) security — EOL meant regulatory risk for a telecom company. (2) velocity — new features blocked because deps couldn't upgrade. (3) cost — faster startup, better GC reduced cloud spend. Outcome: 60% faster migration, unblocked quarterly releases, security patches same-day instead of weeks."

Business framing for your numbers:

| Metric | Business Framing |
|---|---|
| Spring Boot 3: 60% productivity | "Unblocked 6 months of stalled releases. Security same-day instead of weeks." |
| Sling TV: 5 mo vs 18 mo | "Compressed 3-quarter rewrite into 2, without stopping feature delivery." |
| Vulnerability fixes: hours vs days | "Risk exposure from a week to same-day. Audit-ready in hours." |
| Incident: 30 min → 2 min | "P1 resolution 15x faster. Fewer escalation minutes, less customer impact." |

**Q: What's the single highest-impact application of AI in engineering?**

> "For a company with 14M+ subscribers on a mix of modern and legacy systems, the highest-impact application isn't code generation — it's migration automation and incident response compression. Code generation saves individual developer time. Migration automation unlocks platform-level velocity — modernizing legacy systems that block the entire business. Incident response compression protects revenue and brand. Both scale without requiring every engineer to be an AI expert."

---

## TAB 5: System Design & Technical Concepts

### Classic Whiteboard Problems

| Question | Prep Notes |
|---|---|
| **URL shortener** | Hash function (base62 vs hash+collision), redirect (301 vs 302), DB shard by hash prefix, cache hot URLs in Redis. |
| **Rate limiter** | Token bucket per user (simplest). Distributed: Redis sorted sets or sliding window. Accuracy vs memory tradeoff. |
| **Chat system** | WebSocket for real-time, Kafka for persistence, client-seq for ordering, push + catch-up for offline. |
| **Notification system** | Event → template engine → channel router (push/SMS/email) → provider queue. Idempotency key for dedup. Exponential backoff. |
| **Collaborative editing** | CRDTs (Yjs/Automerge) for modern systems. WebSocket + version vectors for sync. |
| **Search autocomplete** | Trie + top-K per prefix. Cache popular prefixes in Redis. Batch update trending queries hourly. |
| **Payment system** | Idempotency key on every request. Saga for cross-service. Reconciliation job compares ledger vs PSP daily. |
| **Logging/telemetry pipeline** | Agents → Kafka → stream processor (normalize, sample) → hot: Elasticsearch (7d) → cold: S3 (indefinite). |
| **Feature flag system** | Redis (fast path), pub/sub for propagation, client SDK local cache, server-side eval for security. |

**System design framework to memorize:**
> **Clarify → Boundaries → Architecture → Scale → Tradeoffs → Migration → Ops**

---

### Core Distributed Systems Concepts

| Concept | What to Say |
|---|---|
| **CAP Theorem** | C = every read gets latest write. A = every request gets non-error response. P = system works despite network split. In distributed systems, P is non-negotiable. You choose CP (consistent, may be unavailable) or AP (available, may serve stale). Most systems relax consistency. |
| **Saga Pattern** | Choreography (services publish events, next reacts) vs Orchestration (central coordinator). Used orchestration for DPA (Spring Batch). |
| **CQRS** | Separate read model from write model. Writes through command model (events, validation). Reads through optimized read model (denormalized, cached). Use when read/write patterns are significantly different. |
| **Idempotency** | Same request N times = same result. Keyed by client-provided UUID. Server checks if already processed → return stored result. Used in payment flows, DPA integrations. |
| **Consistency Models** | Strong (slow, hard to scale), Eventual (fast, may serve stale), Read-your-writes (compromise). Choose based on: does the user need to see their own write immediately? |
| **Consensus (Raft/Paxos)** | Agreeing on a value across nodes. Raft is simpler (leader-based). Used in etcd, Consul, Zookeeper. |
| **Gossip Protocol** | Nodes exchange state with random peers. Eventually all know. Used in Cassandra, Dynamo. No single point of failure. |

---

### Observability

| Question | What to Say |
|---|---|
| **Metrics vs Logs vs Traces** | Metrics (Prometheus): "is it slow?" — counts, latencies, error rates. Logs (ELK): "what happened?" — structured events, searchable. Traces (Dynatrace): "why is it slow?" — request path across services. You need all three. |
| **What metrics for a microservice?** | RED method: Rate (requests/s), Errors (failed/s), Duration (p50, p95, p99). Plus: CPU, memory, GC pause, DB pool, queue depth. |
| **Meaningful alerts** | Alert on symptoms (p99 > 500ms, error rate > 1%), not causes (CPU > 80%). Dynamic thresholds (3σ from baseline). Page only when action required. |

---

### Database

| Question | What to Say |
|---|---|
| **SQL vs NoSQL** | SQL: relations, joins, transactions, reporting, known schema. NoSQL: flexible schema, high write volume, simple access patterns. Default to PostgreSQL. |
| **DynamoDB vs Postgres** | DynamoDB: single-digit-ms at any scale, simple key/value, no joins, predictable patterns. Postgres: everything else. |
| **Database migration** | Expand-contract: (1) New schema alongside old. (2) Dual-write. (3) Backfill. (4) Verify. (5) Remove old. Never in-place migration on live production DB. |
| **Sharding** | Key-based (hash on ID → shard N), Range-based (A-M → shard 1), Directory-based (lookup table). Key-based most common. Re-sharding is painful — plan for it. |

---

### Containers & Security

| Question | What to Say |
|---|---|
| **Why Kubernetes?** | Self-healing, auto-scaling, rolling updates, service discovery, secrets, multi-environment consistency. At Dish: Rancher manages our K8s. |
| **K8s service discovery** | Pods get dynamic IPs. Services provide stable endpoints. kube-proxy watches API server, programs iptables to healthy pods. DNS: `<svc>.<ns>.svc.cluster.local`. |
| **Health checks (liveness vs readiness vs startup)** | Liveness: restart if dead. Readiness: remove from LB if not ready. Startup: delay liveness during slow startup. |
| **mTLS** | Mutual TLS — both sides verify each other's certs for service-to-service communication. Service mesh (Istio) handles transparently. |
| **OWASP Top 10 in microservices** | #1 Broken Access Control (most common), #3 Injection (dynamic queries), #6 Vulnerable Components (Snyk), #10 SSRF (internal service abuse). |
| **Zero Trust** | Never trust, always verify. Every request authenticated and authorized regardless of source. DMZ gateway validates every STB request at Dish. |

---

## TAB 6: Behavioral STAR — Stories & Frameworks

### Your 5 Anchor Stories (Adapt to Most Questions)

| # | Story | Adapts To |
|---|---|---|
| 1 | **Spring Boot 3 migration** — strategy, AI execution, measurement, promotion | Tech strategy, migration, influence without authority, measuring impact |
| 2 | **Sling TV transformation** — legacy modernization, DDD, AI reverse-engineering | System design, migration, org design, disagreement with manager |
| 3 | **Custom AI agent skills** — building from scratch, MCP, governance, scaling to 5+ teams | Innovation, failure/recovery, scaling impact, leadership |
| 4 | **Hackathon → company-wide tool** (Asset Management) | Tight deadline, building for adoption, full-stack delivery |
| 5 | **Incident response process** — Dynatrace, runbooks, PagerDuty | Operational excellence, blameless culture, automation |

---

### STAR Questions + Your Story

| Question | Your Story |
|---|---|
| **Delivered under tight deadline** | Codefest 2023 — Asset Management in 48 hours. Won. Productized company-wide. |
| **Conflict with peer/manager** | AI agent adoption resistance — paired with skeptics, showed data (time saved, defect rate). Resistance dissolved after results. |
| **Pushed back on requirement** | Spring Boot 3 — business wanted all 12 services at once. Pushed back: too risky. Sequenced by dependency, piloted 3, then accelerated. |
| **Made a mistake** | First agent skill was too rigid — fixed 5-phase workflow nobody used. Redesigned as configurable playbook. Second version adopted. |
| **Disagreed with manager** | Sling TV — manager wanted traditional rewrite. I proposed AI-assisted. Built prototype on one API. Got buy-in. |
| **Underperforming team member** | Pairing + structure. Not "you're underperforming" but "let's work through this together." Define outcomes, check progress, recognize improvement publicly. |
| **Most challenging technical problem** | Sling TV data consistency — lost ACID transactions after DB split. Solved with Saga pattern + compensation logic. Chaos engineering to validate. |
| **Decision with incomplete info** | MCP server permissions — decided read-only + specific scopes first. Expanded iteratively as use cases emerged. |
| **Most critical feedback received** | "Your designs are technically correct but you don't bring the team along." Started writing ADRs publicly, running design reviews, explaining why not just what. |
| **Owned a failure** | Agent skill failure — agent "fixed" a test to match broken output. I missed needing human verification of test assertions. Now: always review AI-generated test expectations. |

---

### Principal-Specific Behavioral

| Question | Framework |
|---|---|
| **Create alignment across teams** | Spring Boot 3 — wrote the guide, built first 3 as reference, showed data. Teams adopted because it worked, not because mandated. |
| **Team rejects your guidance** | (1) Understand concerns first. (2) Pair on first implementation. (3) Compromise on non-essentials, hold on what matters (security, operability). |
| **Build vs buy framework** | Buy: solved problem, not core to business, low switching cost, stable vendor. Build: competitive advantage, deep customization needed, immature vendor market. MCP: built because integration with our workflow was the value. |
| **Evaluate new technology** | AI evaluation group process: define success criteria → 2-engineer, 2-week trial → compare baseline → recommend adopt/reject/pilot. |
| **Measure developer productivity** | DORA metrics: lead time, deploy frequency, change failure rate, time to restore. For AI specifically: time saved per task, defect rate of AI code, adoption rate. |
| **Decide what NOT to work on** | Follow the bottleneck — what's blocking the most teams or the most critical path? Everything else waits. Saying no to everything is saying no to focus. |
| **Hire Principal/Staff engineers** | Signal 1: articulate framework, not just solution. Signal 2: talk about org context, not just code. Signal 3: disagree constructively. Signal 4: point of view on industry trends. |
| **Technology decision you reversed** | Chose RabbitMQ over Kafka early on. Simpler, team knew it. As event volume grew, RabbitMQ's limits showed. Migrated to Kafka — cost a quarter. Lesson: optimize for today, but have an evolution path. |
| **Mentor someone resistant** | Don't frame as mentoring. Frame as "I want your opinion on this problem." Peer discussion opens the door. Then ask follow-ups that stretch their thinking naturally. |

---

## TAB 7: Strategy & Vision

### Future of AI in Software Engineering

> The shift from "AI as autocomplete" to "AI as autonomous agent." Today: AI suggests code. Tomorrow: AI reads a spec, implements it, tests it, creates a PR, and monitors it in production. The human shifts from writer to specifier + reviewer. The bottleneck becomes: how good are you at specifying intent? That's why I invested in spec-driven development (Kiro). The companies that win will figure out how to trust AI agents safely — that's what governance and MCP scoping solve.

### Platform vs Product Engineering

> Platform teams exist to make product teams faster. If the platform team is a bottleneck, you've failed. Keys: self-service tooling, success metric is product team velocity (not features shipped), platform team embedded with product teams quarterly, every decision justified by "what product velocity does this unlock?"

### Vision for Engineering Excellence

> (1) Quality is non-negotiable — 85% coverage, Snyk scans, code review. But automated in CI/CD, not enforced manually. (2) Speed is the multiplier — fast feedback loops, short lead times, small batch sizes. (3) Leverage is the differentiator — build tools and agents that scale your best engineers. (4) Culture is the foundation — blameless post-mortems, continuous learning, mentorship. Excellence is a system that produces good outcomes by default.

### Reducing Cycle Time

> Map the value stream from idea to production. Identify the biggest bottleneck — code review (add automated checks), CI (parallelize), deployment (automate), requirements (tighten scope). Fix one at a time, measure before and after. Repeat. Single biggest lever at most companies: reduce PR size.

### Incident Management at Scale

> (1) Prevention — circuit breakers, bulkheads, chaos engineering. (2) Detection — symptoms not causes, PagerDuty escalation. (3) Response — documented runbooks, on-call, severity definitions (P1 = customer-impacting). (4) Learning — blameless post-mortems within 48h, action items tracked. (5) Automate — every runbook executed more than once should be automated.

### Most Underrated Principal Skill

> Communication — explaining complex technical decisions to non-technical audiences without oversimplifying or condescending. A Principal who can't communicate with VPs and PMs is a brilliant IC in a Staff role. And listening — before proposing a solution, understand the constraint the other person sees but you don't.

---

## TAB 8: Company-Specific Questions

| Question | Answer Framework |
|---|---|
| **Why do you want to work here?** | Research the company! Generic: "You work at scale and I solve problems at scale." Better: "Your platform handles X users and you're migrating from Y to Z. That's exactly what I've done at Dish." |
| **What do you know about our tech stack?** | Research before the interview! Java shop: "Spring Boot, Kafka, K8s — that's my primary stack." Different stack: "The patterns — circuit breakers, event-driven, observability — are stack-independent." |
| **How would you approach [their specific challenge]?** | Don't solve on the spot. Show your process: "I'd need to understand your current architecture, blockers, and risk tolerance. Here's the framework I'd apply: [assessment → phased plan → measure → iterate]." |
| **Why leave Dish?** | "4+ years, delivered what I set out to do — architected the platform, drove AI adoption, built an agent practice. The next step is Principal Engineer at org-level. I want to do that where the scale and problem space match my experience." |

---

## TAB 9: Quick Reference — Cheat Sheets & Tricks

### 10 Tricks to Clear the Interview

**#1 — First 30 seconds decide everything**
When they say "Tell me about yourself," your opening must be: *"Staff Engineer at Dish Network — I own the architecture for the subscriber platform serving 10M+ users."* Title + ownership + scale in one breath. The interviewer forms their impression of your level in the first 30 seconds.

**#2 — Always answer at Principal level**
Same question, different level:
- Senior: "I migrated my service. Changed javax to jakarta."
- Staff: "I drove org-wide migration across 12 services with AI."
- Principal: "I decided which services to migrate and in what order based on business risk. Created the framework that made migration safe. Unblocked 6 months of stalled releases."

After every answer, ask yourself: did I just answer at Senior, Staff, or Principal?

**#3 — The pivot for questions you don't know**
Don't answer. Clarify first: *"Let me clarify the constraints — what consistency model do you need? RTO of seconds or minutes? Read-to-write ratio?"*

Still don't know: *"I don't have deep experience with that specific pattern. Here's how I'd approach it from first principles..."* Talk distributed systems fundamentals. That's better than a wrong confident answer.

**#4 — Lead with the tradeoff, not the implementation**
Bad: *"We used Kafka."*
Good: *"We had 80+ Rails APIs with a shared database. ACID worked but every deploy risked the entire system. We chose Kafka + Saga to trade strong consistency for service independence. Decision: we can tolerate eventual consistency if we can deploy independently."*

**#5 — The company question is a trap**
> "Why do you want to work here?"

If you say "I love your mission" without substance, it's empty. If you say "better pay," it's disqualifying.

Safe answer: *"I've spent 4 years building platforms at scale and driving AI adoption. I'm looking for where that experience compounds. [Specific thing about this company] aligns with that."*

Always include one specific researched fact about the company. Without it, no answer works.

**#6 — Ask Principal-level questions**
Don't waste "What's the work from home policy?" Ask:
1. *"What's the biggest technical challenge the org is facing that doesn't have a clear solution?"*
2. *"How do engineering decisions get made — top-down architecture or team autonomy with guardrails?"*
3. *"What would you change about how engineering operates if you could?"*
4. *"Where is AI/automation in your workflow today, and where do you want it in 2 years?"*

The last question you ask is what they'll remember most.

**#7 — Silence is power**
Nervous people talk fast. Fast = junior.
- Pause 2 seconds before answering — shows thinking, not reciting
- Pause after making a point — let it land
- If you're rambling, stop and say: *"Let me pause — does that address your question, or should I go deeper?"*

The person who fills the silence first loses.

**#8 — The "I don't know" move**
Best way to say you don't know:

> "I know the concept — [explain what you know]. I haven't done it from scratch. Here's how I'd approach it: [plan]. The design would focus on... [reasoning]."

Shows: you know the concept, you know where you lack depth, you have a plan, you can reason. Better than a BS answer.

**#9 — One-liner per resume bullet**
Every line on your resume is a question target. If you can say the one-liner for every term in Tab 2, you will never freeze on "tell me more about X."

**#10 — Three before the room**
Before each interview round, decide:
1. **One fact about this interviewer's team** — connect your experience to their problem
2. **One question you'll ask** — so you don't blank on "any questions?"
3. **One story you'll tell** — find a way to land your best story regardless of question

If you walk in knowing these three, you will never have a round where you feel lost.

---

### Frameworks to Memorize

| Framework | For |
|---|---|
| **Context → Action → Outcome → Lesson** | Every behavioral answer |
| **Clarify → Boundaries → Architecture → Scale → Tradeoffs → Migration → Ops** | Every system design answer |
| **Rate → Errors → Duration** (RED method) | Monitoring questions |
| **Current state → Business alignment → Phased evolution → Exit criteria** | Roadmap/strategy questions |

### Pre-Interview Checklist

- [ ] Researched this company's tech stack and engineering challenges
- [ ] 3 stories ready that show Principal-level scope (org-wide, not team-wide)
- [ ] Can explain every term on my resume in 1-2 sentences
- [ ] Clear answer for "why this company" and "why now"
- [ ] Ready for a system design whiteboarding round (notification system, rate limiter, or similar)
- [ ] Have a question to ask them that shows strategic thinking

### Mental Model

100% of Principal interview success comes from:
1. **Your story** — can you tell it clearly in 2 minutes?
2. **Confidence in your own resume** — when they drill into your projects, you don't freeze
3. **One good system design** — prove you can think in tradeoffs
4. **One good behavioral** — a failure story you own honestly

You have 14+ years of experience. The content is there. You just need the structure to access it under pressure.

---

*End of Workbook*
