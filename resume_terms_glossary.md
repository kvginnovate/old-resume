# Resume Term Glossary — Shorthand Explanations

> Quick reference for every term/technology on your resume. Each entry:
> **What it is** + **Why it's on your resume** + **One-liner to say in interview**

---

## Professional Summary

| Term | Shorthand |
|---|---|
| **Distributed systems** | Multiple services running on different machines, talking over a network. Not a single monolithic app. Interview: *"I design systems where each service runs independently, communicates via APIs or events, and can fail without taking down the whole platform."* |
| **Rancher-managed Kubernetes** | Rancher is a management UI on top of Kubernetes. K8s orchestrates containers (Docker). Rancher adds multi-cluster management, RBAC, and monitoring. Interview: *"Rancher gives us a single pane of glass to manage multiple K8s clusters — deploy, scale, monitor, rollback."* |
| **Kiro spec-driven development** | Kiro is an AI coding tool. You write a spec (OpenAPI, requirements), the AI generates the implementation. Interview: *"You write the contract first — OpenAPI spec, test cases. Kiro generates the Spring Boot service, the tests, the docs. Humans review and ship."* |
| **Spring Boot 3 migration** | Upgraded Java microservices from Spring Boot 2 (EOL, no security patches) to Boot 3. Involved breaking changes — Jakarta namespace, security config, Hibernate 6. Interview: *"Spring Boot 2 reached end-of-life — no security patches, blocking dependency upgrades. I used AI to automate the migration across 12 services."* |
| **API design org-wide** | Standardizing how APIs are designed — OpenAPI specs, naming conventions, versioning, error formats. Interview: *"Every team writes OpenAPI specs before code. Shared contract repo. Breaking changes require a new version and migration plan."* |
| **Architectural reviews** | Formal sessions where you review another team's design before they build. Interview: *"I sit in on other teams' architecture discussions — not to approve, but to ask the hard questions they might miss."* |
| **Incident response** | On-call process when production breaks. Triage → mitigate → fix → post-mortem. Interview: *"I led the incident response process — PagerDuty alerts, runbooks, post-mortems with action items."* |
| **Org-wide migrations** | Changes that affect every team — not just yours. Spring Boot 3 migration, Snyk adoption. Interview: *"Org-wide means you can't force anyone. You build the guide, do the first one yourself, show the data, and let adoption follow."* |

---

## Technical Skills

### Languages

| Term | Shorthand |
|---|---|
| **Java** | Your primary language. JVM, object-oriented. Spring Boot, Hibernate. Interview: *"Java is my core — 8+ years, Spring Boot ecosystem."* |
| **Kotlin** | Modern JVM language. Less boilerplate than Java. Used for Android. Interview: *"Kotlin for Android native apps. Less code, null safety, coroutines."* |
| **TypeScript** | JavaScript with types. Used in React/Next.js frontends. Interview: *"TypeScript on the frontend — React, Next.js. Static types catch bugs before runtime."* |
| **Python** | Used for scripting, automation, data analysis. Interview: *"Python for automation scripts, data analysis, and quick prototypes."* |

### Frameworks

| Term | Shorthand |
|---|---|
| **Spring Boot** | Java framework for building microservices. Embedded server, auto-configuration, production-ready. Interview: *"Spring Boot is my default for backend services. Embedded Tomcat, auto-config, actuator for health checks."* |
| **Spring Cloud** | Extends Spring Boot for distributed systems — service discovery, config, circuit breakers. Interview: *"Spring Cloud adds the distributed-system primitives: config server, service discovery, API gateway patterns."* |
| **Hibernate** | JPA implementation — maps Java objects to database tables (ORM). Interview: *"Hibernate for ORM. Lazy loading, caching, query optimization. Migrated from Hibernate 5 to 6 in the Boot 3 upgrade."* |
| **ReactJS** | JavaScript library for building UIs. Component-based, virtual DOM. Interview: *"React for web frontends. Component-based, state management via hooks or Redux."* |
| **Next.js** | React framework with server-side rendering, routing, API routes. Interview: *"Next.js adds SSR — pages render on the server, faster initial load, better SEO."* |
| **React Native** | Build mobile apps (iOS/Android) using React/JavaScript. Interview: *"React Native for cross-platform mobile — share code between Android and iOS. Used for Kiro Mobile and Field Catalogue."* |
| **Android SDK** | Native Android development tools. Java/Kotlin, Android APIs, Google Play Store. Interview: *"Native Android SDK for the early apps (Nasuni, Spree). Deep integration with device features."* |
| **JUnit** | Java testing framework. Unit tests, integration tests. Interview: *"JUnit for automated testing. Mandated 85%+ coverage as a CI gate."* |

### Distributed Systems

| Term | Shorthand |
|---|---|
| **Microservices Architecture** | Breaking an application into small, independent services. Each owns its data, deploys independently. Interview: *"Each service owns a domain capability and its own data store. Independent deploy, independent scaling."* |
| **Circuit Breaker** | Pattern that stops calling a failing service to prevent cascading failures. Interview: *"If service A calls B and B is failing, the circuit breaker trips — instead of timing out every request, it fails fast. B recovers, breaker closes."* |
| **API Gateway** | Single entry point for all client requests. Routes to the right service, handles auth, rate limiting. Interview: *"API Gateway is the front door — route requests, authenticate, rate-limit, aggregate responses."* |
| **REST APIs** | HTTP-based APIs. Resources identified by URLs, actions by HTTP methods (GET, POST, PUT, DELETE). Interview: *"Stateless, resource-oriented HTTP APIs. Every service exposes REST endpoints documented via OpenAPI."* |

### Infrastructure

| Term | Shorthand |
|---|---|
| **Docker** | Packages applications into containers — lightweight, portable, consistent across environments. Interview: *"Docker containers package the app + its dependencies. Same image runs on dev, test, prod."* |
| **Kubernetes** | Orchestrates containers — scheduling, scaling, load balancing, self-healing. Interview: *"K8s deploys and manages containers. If one crashes, it restarts. If load increases, it scales."* |
| **Rancher** | Management platform for multiple K8s clusters. UI, RBAC, monitoring. Interview: *"Rancher manages our K8s clusters — deploy apps via UI or API, manage access, view logs and metrics."* |
| **AWS S3** | Object storage — store files, backups, logs, static assets. Interview: *"S3 for object storage — telemetry data, Athena queries, build artifacts."* |
| **AWS DynamoDB** | NoSQL database. Key-value + document. Single-digit-millisecond latency at any scale. Interview: *"DynamoDB for high-throughput, low-latency key-value access. DISH App Store uses it for build metadata."* |
| **Firebase** | Google's mobile development platform — real-time DB, auth, push notifications, analytics. Interview: *"Firebase for real-time sync in mobile apps (Nasuni, Spree). Auth, Firestore, analytics."* |
| **GCP** | Google Cloud Platform — compute, storage, data services. Interview: *"GCP for cloud services beyond AWS — BigQuery, Cloud Functions, Pub/Sub."* |

### Observability & DevOps

| Term | Shorthand |
|---|---|
| **Dynatrace** | Application performance monitoring (APM). Distributed tracing, service health dashboards, AI-driven root cause. Interview: *"Dynatrace traces every request across service boundaries. 30-minute incident diagnosis→2 minutes. Built a custom MCP server for it."* |
| **Prometheus** | Open-source monitoring and alerting. Collects metrics from services. Interview: *"Prometheus scrapes metrics from services. Used alongside Dynatrace for open-source monitoring."* |
| **ELK Stack** | Elasticsearch (search), Logstash (ingest), Kibana (visualize). Log aggregation. Interview: *"ELK for log aggregation — search across all service logs during incident analysis."* |
| **GitLab CI/CD** | GitLab's built-in CI/CD pipeline. Auto-build, test, scan, deploy on every commit. Interview: *"GitLab CI/CD runs on every push — build, Snyk scan, run tests, deploy to Rancher."* |
| **Snyk** | Security scanning tool. Finds vulnerabilities in dependencies, Docker images, IaC. Interview: *"Snyk scans every build for CVEs. Triaged by exploitability. Built a MCP server so AI agents create same-day fix PRs."* |

### AI Agent Tooling

| Term | Shorthand |
|---|---|
| **Antigravity** | AI coding tool — part of the modern AI engineering stack. Agent-based code generation. Interview: *"AI coding assistant. Evaluated it as part of the internal AI tools group."* |
| **Kiro (Spec-Driven Dev)** | Your primary AI dev tool. Write spec → agent generates code → tests → PR. Interview: *"Kiro takes a spec (OpenAPI, requirements) and generates the implementation with tests. Used daily for migrations, fixes, new features."* |
| **Paseo** | Agent orchestration — manages multiple AI agents across workspaces. File-locking, coordination. Interview: *"Paseo orchestrates multiple AI agents (Codex, Claude, Kiro) so they don't conflict. Manages worktrees, file locks, scheduling."* |
| **Orca** | Terminal UI for AI workflows. Interview: *"Orca is a terminal-based interface for AI agent workflows — think of it as the cockpit for your local AI stack."* |
| **OpenCode** | An AI coding tool in the agent ecosystem. Interview: *"AI coding assistant in the OMP ecosystem. Used alongside Kiro."* |
| **OMP** | Oh My Paseo — the overarching AI agent platform. Models, providers, agent profiles. Interview: *"OMP is the platform that connects AI models, providers, and agents. I use it to configure and route between different AI backends."* |
| **psmux-terminal** | Multi-session AI terminal manager. Interview: *"Terminal multiplexer for managing multiple AI agent sessions simultaneously."* |
| **Custom Agent Skills** | Reusable playbooks for AI agents: defect-fix, test-gen, code-review, migration. Interview: *"Pre-built skill playbooks. Defect-fix: agent reads Jira, reproduces bug, fixes it, runs tests, creates PR. 5 phases with guardrails."* |
| **LLM Workflows** | Structured sequences of LLM calls (not just chat). Multi-step, tool-using, stateful. Interview: *"Agents don't just answer questions — they follow structured workflows: read code → plan → implement → verify → create PR. Each step uses the right tool."* |

### MCP (Model Context Protocol)

| Term | Shorthand |
|---|---|
| **Model Context Protocol (MCP)** | Open protocol that connects AI agents to external tools/servers. Standardized tool access. Interview: *"MCP is how agents talk to tools. Each server exposes capabilities — read Jira, search GitLab, query Dynatrace — with scoped permissions."* |
| **Jira MCP** | MCP server → Jira. Agent reads tickets, creates issues, updates status. Interview: *"Agent reads bug descriptions from Jira, creates tickets for findings, updates status as it works."* |
| **GitLab MCP** | MCP server → GitLab. Agent reads repos, checks code, creates MRs. Interview: *"Agent clones repos, searches code, reads MRs, creates fix branches and merge requests."* |
| **GitHub MCP** | Same as GitLab MCP but for GitHub-hosted repos. Interview: *"Same pattern as GitLab MCP — read code, search issues, create PRs."* |
| **Firebase MCP** | MCP server → Firebase/Firestore. Agent reads/writes data with permissions. Interview: *"Agent reads Firestore collections, manages Firebase Auth, deploys Cloud Functions — all with scoped read-only or write permissions."* |
| **Google Cloud MCP** | MCP server → GCP services. Agent queries Cloud Storage, BigQuery, etc. Interview: *"Agent queries GCP resources — BigQuery tables, Cloud Storage buckets, Cloud Run services."* |

### Architecture

| Term | Shorthand |
|---|---|
| **System Design** | The process of defining architecture, components, interfaces, and tradeoffs at scale. Interview: *"System design is about making intentional tradeoffs — consistency vs. availability, sync vs. async, SQL vs. NoSQL — based on the problem you're solving."* |
| **DDD (Domain-Driven Design)** | Methodology where software structure mirrors business domain. Bounded contexts, ubiquitous language. Interview: *"DDD means the code structure mirrors the business structure. Each domain (billing, content, entitlements) is its own service with its own language."* |
| **Microservices Patterns** | Reusable solutions to common distributed-system problems: Saga, CQRS, Event Sourcing, Strangler Fig. Interview: *"Patterns like Saga for distributed transactions, Strangler Fig for incremental migration, Circuit Breaker for fault isolation."* |
| **API Design (OpenAPI)** | OpenAPI Specification (formerly Swagger) — standard for describing REST APIs. YAML/JSON. Interview: *"OpenAPI specs define the contract — endpoints, request/response schemas, error codes. Spec-first means the contract is agreed before coding."* |
| **ADR (Architectural Decision Records)** | Documents capturing an architecture decision — context, options, decision, consequences. Interview: *"ADRs capture why a decision was made and what alternatives were considered. Prevents the same debate from happening twice."* |

### Certifications

| Term | Shorthand |
|---|---|
| **Google Cloud Professional Data Engineer** | GCP certification. Design, build, manage data processing systems. Interview: *"Deep-dived into GCP for this certification. Covers BigQuery, Dataflow, Pub/Sub, ML — useful for data-heavy design conversations."* |

---

## Professional Experience — Projects

| Term | Shorthand |
|---|---|
| **GemFire** | In-memory distributed data grid (cache). Stores hot data across nodes for low-latency reads. Interview: *"GemFire sits between services and the database. Frequently accessed data — subscriber profiles, device configs — served from memory instead of hitting PostgreSQL every time."* |
| **Spring Boot 3 breaking changes** | Jakarta (javax.\* → jakarta.\*), Security (WebSecurityConfigurerAdapter → SecurityFilterChain), Hibernate 6. Interview: *"Boot 3 changed the Java namespace (javax.\* to jakarta.\*), replaced the security config class, and upgraded Hibernate. All breaking, all automatable."* |
| **GC behavior** | Garbage Collection — how Java reclaims memory. Boot 3 + newer JDK → improved GC = fewer pauses. Interview: *"Spring Boot 3 on JDK 17 meant generational ZGC — shorter GC pauses, more predictable latency under load."* |
| **Snyk triaging by exploitability** | Not all CVEs are equal. Prioritize by: is there a known exploit in the wild? Can this be reached from our code? Interview: *"We triaged Snyk findings: critical (exploit exists) → fix same-day. High → fix within sprint. Medium → add to backlog. Low → accept risk."* |
| **APM (Application Performance Monitoring)** | Monitoring app performance — response times, error rates, throughput. Interview: *"APM tracks how your app performs from the user's perspective. Dynatrace APM shows every request's path, duration, and where it failed."* |
| **Distributed tracing** | Trace a single request across multiple microservices. Each service adds a span. Interview: *"Every request gets a trace ID. When it crosses 5 services, Dynatrace stitches all 5 spans into one trace. You see the full path — and exactly which hop failed."* |
| **PagerDuty** | Incident alerting and on-call management. Escalation policies, push notifications. Interview: *"PagerDuty pages the on-call engineer when Dynatrace detects an anomaly. Escalates if no response in N minutes."* |
| **Runbooks** | Documented step-by-step procedures for handling specific incidents. Interview: *"For every known incident type — database connection pool exhaustion, cache miss storm — we have a runbook: symptoms, diagnosis steps, fix commands."* |
| **Kiro Mobile (WebSocket)** | Real-time communication protocol. Full-duplex — server pushes updates to the phone without polling. Interview: *"WebSocket keeps a persistent connection between app and server. GitLab MR status changes → pushed to phone immediately. No polling."* |
| **GitLab MR status** | Merge Request lifecycle — opened, running CI, tests passed, approved, merged, deployed. Interview: *"The app shows real-time MR status: CI running, tests passed, ready for review, merged. Engineers don't need to open GitLab."* |
| **Dish Ignite 2026** | Internal Dish AI demo day where employees present innovative projects to leadership. Interview: *"I presented Kiro Mobile and the MCP-powered agent skills. Live demo of agent fixing a bug from Jira. Got buy-in from VPs to scale the practice."* |
| **Offline-first mobile app** | App works without internet. Data stored locally (SQLite), syncs when connectivity returns. Interview: *"Field technicians work in basements with no signal. App caches everything locally — catalogue, pricing, inventory. Syncs compressed delta updates when online."* |
| **Local content caching** | Store content (images, product data) on the device. Serve from cache, not network. Interview: *"Catalogue images and product specs stored locally on the device. Zero loading time during customer visits."* |
| **Lightweight CMS** | Content Management System. Admin UI for non-technical users to publish content. Interview: *"Built a simple CMS so the marketing team manages catalogue content directly — upload images, update prices, publish changes. Zero engineering involvement."* |
| **ColdFusion** | Legacy Adobe technology. Tag-based language, mixed HTML and server logic. End-of-life, hard to maintain. Interview: *"ColdFusion is a legacy tech from the 2000s — tag-based, mixed presentation and logic. Hard to hire for, hard to maintain, prone to production issues."* |
| **Spring Batch** | Spring framework for batch processing — scheduled jobs, chunk processing, retries, error handling. Interview: *"Spring Batch orchestrates the DPA's 23 downstream integrations — processes files in chunks, retries on failure, sends failed jobs to a dead-letter queue."* |
| **SFTP distribution** | Secure file transfer (SSH-based). Scheduled file drops to partner servers. Interview: *"DPA generates agreements as PDFs, SFTPs them to 7 partner systems (regulatory bodies, fulfillment centers). Each target has its own schedule and format."* |
| **Dead-letter queue** | Queue for messages that failed processing. Safe place to investigate without losing data. Interview: *"When an integration fails after retries, the message goes to a dead-letter queue. We investigate, fix the issue, and replay it."* |
| **DMZ Gateway** | Demilitarized Zone — a network layer between the internet and internal services. Adds security. Interview: *"STB devices in the field connect to a DMZ gateway — not directly to internal services. Gateway handles auth (JWT via Cognito/Okta) and forwards verified requests."* |
| **JWT (JSON Web Token)** | Token format for authentication. Contains claims (user ID, expiry), cryptographically signed. Interview: *"JWT tokens carry the device identity. STB sends token with each request. Gateway verifies signature before forwarding."* |
| **OAuth lifecycle** | OAuth2 authorization flow. Token issuance, refresh, expiry, revocation. Interview: *"We managed the full OAuth lifecycle — token refresh before expiry, revocation when a device is decommissioned, rotation of signing keys."* |
| **Certificate rotation** | Replacing TLS/SSL certificates before they expire. At 10M devices, automation is the only option. Interview: *"10M devices each with a client certificate. Manual rotation is impossible. We automated it — devices check for new certs on schedule, pull from a secure endpoint."* |
| **Codefest 2023** | Internal Dish hackathon. You built Asset Management in 48 hours — won. Interview: *"48-hour hackathon. Built Asset Management (Spring Boot + React), containerized, deployed. Won. Leadership productized it — now company-wide."* |
| **vSphere UI Plugin** | VMware vSphere is the hypervisor management interface. A plugin adds features to its UI. Interview: *"Built a ReactJS plugin that sits inside VMware's vSphere UI. Admins provision storage volumes from inside their existing tool instead of a separate app."* |
| **vRealize Orchestrator** | VMware's automation platform. Drag-and-drop workflows to automate data center tasks. Interview: *"vRO plugin automates bulk HCI volume provisioning. What used to take manual steps per-volume became a single-click workflow."* |
| **HCI (Hyper-Converged Infrastructure)** | Combines compute + storage + networking into one appliance. VMware vSAN, Nutanix. Interview: *"HCI means the storage and compute are on the same box. Pivot3's platform ran VMs with local storage instead of a separate SAN."* |
| **Mobitaz** | In-house mobile test automation framework. Record user actions → replay on multiple devices simultaneously. Interview: *"I built Mobitaz — you record a test on one device, it replays on 10 devices at once. Used in client demos as a QA service offering."* |
| **Selenium regression suite** | Selenium automates browser testing. Regression suite = automated tests that run on every build to catch regressions. Interview: *"Built NetApp's Selenium test suite from scratch. Automated browser testing for their web app — caught regressions before release."* |
| **Record and playback (mobile)** | Automation technique. Record screen taps once, replay the script on many devices. Interview: *"Record your test once — tap here, type there, swipe. Replay on every Android device. No scripting needed."* |

---

## AI Innovation & Pilots

| Term | Shorthand |
|---|---|
| **Gemini** | Google's LLM. Evaluated as part of the AI tools assessment. Interview: *"Trialed Gemini for code generation and review. Compared it against other models for accuracy and cost."* |
| **Open-source LLMs** | Models like Llama, Mistral — self-hosted instead of API-based. Interview: *"Evaluated self-hosted models (Llama, Mistral) for use cases where data can't leave Dish's network."* |
| **AI evaluation group** | Internal committee at Dish that trials and benchmarks AI dev tools. Interview: *"I'm on the internal panel that picks which AI tools to adopt — we trial, benchmark, and recommend. Keeps Dish ahead without chasing every hype cycle."* |

---

## Quick Reference by Category

### If you're asked about... say this:

| If asked about | 1-liner |
|---|---|
| Your primary stack | "Java, Spring Boot, Kubernetes. REST microservices with OpenAPI specs, deployed on Rancher, monitored by Dynatrace." |
| What you architected | "My Dish subscriber platform — 10M+ users, 12+ microservices, 99.9% uptime, sub-second latency." |
| Your biggest migration | "Spring Boot 2 → 3 across 12 services. AI automated 80% of the work. 60% productivity gain. Got me promoted." |
| Legacy modernization | "Sling TV — reverse-engineered 400K lines of Rails, extracted into 6 bounded contexts as Spring Boot services. 5 months vs estimated 18." |
| AI/agent work | "Built custom MCP servers for Dynatrace and Snyk. Agents fix bugs from Jira tickets autonomously. Adopted by 5+ teams." |
| Your leadership style | "Hands-on, tool-building leader. I don't just design — I build the scaffolds that make the team faster." |
| How you measure impact | "Time saved, velocity unblocked, incidents compressed. Concrete numbers: Spring Boot 3 (60%), Sling TV (70%), incident diagnosis (30min→2min)." |
| A failure / lesson | "Early AI agent skill was too rigid — teams tried once and didn't come back. Redesigned as configurable playbook. Adopted widely." |
| Internal tools | "Asset Management from a hackathon → company-wide. Shift Allowance → every employee. I build things people actually use." |
| 10 years at MSys | "Grew from dev to architect. Client-facing across US enterprises. Learned how to deliver under real constraints." |
