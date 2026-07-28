# Interview Cheat Sheet — Chokkar Gurusamy

> Print this. Glance before you walk in. These are your talking points — not a script.

---

## Your Identity

- Staff Engineer at Dish Network (promoted from Lead)
- 14+ years experience (2011–present)
- Dish: 4+ years (May 2022–present)
- MSys Technologies: 10 years (Feb 2012–May 2022)
- Education: B.Tech IT, Anna University (2007–2011)
- Certification: Google Cloud Professional Data Engineer

---

## 5 Beats of Your Intro

1. **Who you are** — Staff Engineer, 10M+ subscribers, 14+ yrs
2. **My Dish platform + Spring Boot 3** — your primary role, promoted to Staff
3. **Sling TV modernization** — 80+ Rails APIs → Java, 5mo vs 18mo
4. **Custom AI agents** — defect fixing, vulnerability remediation, 5+ teams adopted
5. **Internal tools + close** — hackathon → company-wide, the arc

---

## My Dish Platform (Primary Role)

- API-first microservices on Spring Boot 3
- Deployed on Rancher-managed Kubernetes
- 10M+ subscribers, 99.9% uptime, sub-second latency
- API Gateway + Resilience4j circuit breakers + GemFire caching + Kafka + Dynatrace
- OpenAPI-first development, shared contract repository
- 85%+ JUnit/Postman test coverage gated in CI
- Defined integration patterns across frontend, backend, shared services (BFF pattern)
- AWS Athena: serverless SQL analytics on S3 telemetry (MDA, STB Health, all apps)

---

## Spring Boot 3 Migration (→ Promoted to Staff)

- 12 platform services, 50K+ lines of code
- Breaking changes: Jakarta namespace, Hibernate 6, Spring Security rewrite
- Used Kiro spec-driven AI workflows to automate remediation
- `javax.*` → `jakarta.*`: fully automated, zero human intervention
- Security config: automated + human review
- Hibernate queries: flagged for human review
- Built React dashboard to track AI code changes (convinced VP to scale)
- **Result: 60% productivity gain** (2 weeks → 3 days per service)
- **Result: promoted Lead → Staff**

---

## Security & Operational Gates (Built by You)

- **Dynatrace MCP server:** AI agents read distributed traces, incident diagnosis 30 min → 2 min
- **Snyk MCP server:** AI agents fix vulnerabilities, same-day fixes (was 2–7 days)
- **85%+ coverage mandate:** CI gate, auto-generated tests from OpenAPI specs
- **AI governance:** AI never merges to prod without human review, every action logged

---

## Sling TV Modernization

- 80+ legacy Ruby on Rails APIs → modern Java microservices
- 400K+ lines reverse-engineered using Amazon Q
- Scaffolded 2M+ lines of Java + 10K+ unit tests
- 85% test coverage maintained
- DDD bounded contexts: billing, content, entitlements, recommendations
- Saga pattern on Kafka for cross-service data consistency
- Parallel run with feature flags + Dynatrace + hourly reconciliation
- **Result: 5 months vs 18 months estimated, 70% productivity gain**
- **Result: 50% faster delivery timeline**
- **Result: Technical Excellence Award 2025**

---

## Dish Paperless Agreement (DPA)

- ColdFusion → Spring Boot microservices
- Field agent onboarding: signing, cross-selling, equipment activation
- 23 integrations, 7 SFTP distribution targets
- Spring Batch orchestration layer (retries, dead-letter queues, monitoring)
- Offline capability for field agents in basements with no signal
- **Result: CPAW Award for delivery impact**

---

## STB Health Monitor

- 10M+ set-top box devices
- DMZ gateway: JWT auth (Cognito device + Okta technician)
- QR code scanning → identity bootstrap → JWT streaming
- OAuth lifecycle + automated certificate rotation
- Integrated with Spring Cloud Config, Dynatrace, GitLab/Jenkins CI/CD
- **Result: no manual certificate management at 10M scale**

---

## Field Catalogue

- 100% offline-first Android app
- Local SQLite as source of truth
- Compressed delta sync from CMS
- CMS sync cut delivery time: weeks → minutes
- **Result: 60% increase in on-site technical sales**
- **Result: Sales VP appreciation**

---

## DISH App Store

- Lambda + DynamoDB + React
- Internal enterprise app distribution (iOS/Android)
- OTA installation (`itms-services://` for iOS, direct APK for Android)
- Okta SSO + group-based access control (SAML assertions)
- Technicians, retailers, employees — different app visibility per group

---

## Internal Tools

**Asset Management**
- Hackathon (48 hours) → company-wide adoption
- Spring Boot + ReactJS + Docker + Portainer + JFrog
- **Result: won Codefest 2023, 70% manual effort reduction**

**Shift Allowance**
- Spring Boot + ReactJS
- Automated manual Excel workflows
- **Result: HR Spot Award, used by every DISH employee**

---

## Kiro Mobile & AI Agent Skills

**Kiro Mobile**
- React Native mobile interface for monitoring AI agent sessions
- Chrome DevTools Protocol over LAN
- Live preview: chat, tasks, code edits
- **Result: showcased at Dish Ignite 2026**

**Custom Agent Skills (Defect Lifecycle)**
- 5-phase playbook: Read → Reproduce → Fix → Validate → Create PR
- MCP integrations: GitLab, Jira, Snyk, Dynatrace
- Scoped permissions: can create PR but never merge, read traces but never modify
- Same pattern handles vulnerability remediation (hours vs days)
- **Result: adopted across 5+ engineering teams**
- **Result: training sessions + playbooks + framework for others to build on**

---

## MSys Technologies (10 Years)

- Software Engineer → Senior → Tech Lead → Technical Architect
- Clients: Pivot3, Nasuni, NetApp
- Domains: storage, virtualization, cloud, mobile
- **Result: Best Performer of the Year 5x (2013, 2014, 2016, 2018, 2019)**
- **Result: Blog Championship Award 2017**

---

## Pivot3 — VMware HCI

- Technical Lead + Full-Stack Developer
- ReactJS vSphere UI plugin, REST APIs, vRealize Orchestrator
- Automated provisioning for 1000+ storage volumes
- **Result: 60% reduction in manual provisioning effort**

---

## Enterprise Mobile & Test Automation

- Nasuni + Spree Wearables Android apps (Play Store)
- Firebase sync + crash monitoring
- Mobitaz mobile test automation (record/playback)
- NetApp Selenium suite: 100+ scenarios
- **Result: 50% manual regression effort reduction**

---

## Key Numbers (Memorize These)

| Number | What It Represents |
|---|---|
| **10M+** | Subscribers on My Dish platform |
| **99.9%** | Uptime maintained |
| **14+** | Years of experience |
| **50K+** | Lines of code in Spring Boot 3 migration |
| **60%** | Productivity gain (Spring Boot 3) |
| **400K+** | Lines of legacy Rails code reverse-engineered |
| **2M+** | Lines of Java microservices scaffolded by AI |
| **10K+** | Unit tests generated |
| **85%** | Test coverage mandate |
| **70%** | Productivity gain (Sling TV) |
| **80+** | Rails APIs transformed |
| **5 months** | Actual delivery (vs 18 months estimated) |
| **23** | Integrations in DPA |
| **7** | SFTP distribution targets |
| **12** | Platform services migrated |
| **5+** | Teams using custom AI agent skills |
| **2** | Technical Excellence Awards (2024, 2025) |
| **5x** | Best Performer of the Year at MSys |

---

## Awards & Recognition

- Technical Excellence Award 2024 (Spring Boot 3 + AI workflow)
- Technical Excellence Award 2025 (Sling TV + MCP servers)
- CPAW Award (DPA delivery impact)
- Spot Award 2023 (Shift Allowance)
- Spot Award 2025 (incident recovery)
- Codefest 2023 (Asset Management hackathon)
- Best Performer of the Year 5x at MSys
- Blog Championship Award 2017
- Sales VP Appreciation (Field Catalogue)

---

## Why You're Looking (Answer for "Why leave Dish?")

- Hit Staff level, delivered AI showcase at Ignite 2026
- Want to apply AI-augmented engineering practice at a company where it's a core competency
- Looking for the next challenge at scale

---

## Questions They'll Ask — Quick Answers

**Why 10 years at MSys?** → Kept growing (SE → Architect). 5 Best Performer awards.

**Why Staff promotion?** → Spring Boot 3 migration + AI workflow adopted across teams.

**What did Technical Excellence Awards recognize?** → 2024: SB3 + AI workflow. 2025: Sling TV + MCP servers.

**How did you measure 60%?** → Time-to-complete: 2 weeks → 3 days per service, tracked across 12 services.

**What about the 20% AI can't handle?** → Hibernate queries, business logic, performance paths. Human reviews.

**How did other teams adopt AI skills?** → Demoed on one team, showed metrics, held training, documented playbooks. Demand, not mandate.

**What's the failure rate?** → 5–10% of runs need human intervention. Exit criteria escalate automatically.

**Isn't this just prompt engineering?** → No. It's a multi-phase playbook with decision gates, MCP integrations, and escalation paths. Closer to CI/CD than a ChatGPT prompt.

**How do you use AWS Athena?** → Serverless SQL on S3 telemetry across MDA, STB Health, and all apps. Replaces Hadoop/spin-up-analytics-DB pattern. Self-serve analytics for the team.

---

## Your Arc (One Sentence)

I started as a developer, grew into architecture, and now I use AI to modernize platforms at scale, codify that capability into reusable agent skills, and drive adoption across the org.
