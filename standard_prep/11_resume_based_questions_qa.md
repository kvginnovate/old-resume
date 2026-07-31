# Resume-Based Interview Questions — Full Q&A

> Questions an interviewer will ask purely by reading your resume. Covers every claim, number, and gap.
> **Not** general technical questions (those are in `01`–`10`). These are resume-specific probes.
> Focus on The Standard Principal Engineer V role.

---

## Contents

1. [Resume Integrity: Discrepancies to Fix](#1-resume-integrity-discrepancies-to-fix)
2. [Architecture Deep Dives (My Dish Platform)](#2-architecture-deep-dives-my-dish-platform)
3. [Spring Boot 3 Migration & Promotion Story](#3-spring-boot-3-migration--promotion-story)
4. [Sling TV Modernization — Biggest Claims, Most Probing](#4-sling-tv-modernization--biggest-claims-most-probing)
5. [AI / MCP / Agent Skills (Differentiator)](#5-ai--mcp--agent-skills-differentiator)
6. [Internal Tools & Awards](#6-internal-tools--awards)
7. [MSys Technologies — 10 Years](#7-msys-technologies--10-years)
8. [Principal-Altitude Questions (Using Resume as Case Study)](#8-principal-altitude-questions-using-resume-as-case-study)
9. [Vulnerability Probes — Where You're Exposed](#9-vulnerability-probes--where-youre-exposed)
10. [JD-Mapped Questions (Azure, Confluent, Kong, Terraform)](#10-jd-mapped-questions-azure-confluent-kong-terraform)
11. [Quick Reference: Resume Claims → Questions](#11-quick-reference-resume-claims--questions)

---

## 1. RESUME INTEGRITY: Discrepancies to Fix

### ⚠️ Advisory: "50% Faster" vs "70% Productivity Gain" — Both Under Sling TV

**The problem:** In `main_v3.tex`, line 139 says:
> *"Led the strategic transformation of 80+ legacy Ruby on Rails APIs into a modern, scalable Java microservices architecture, achieving a **50% faster delivery timeline** through API-first patterns and event-driven design."*

Line 141 says:
> *"Spearheaded GenAI modernization by leveraging Amazon Q to reverse-engineer 400K+ lines of legacy code and scaffold 2M+ lines of Java microservices and 10K+ unit tests (maintaining 85% coverage), achieving a **70% productivity gain**."*

**An interviewer WILL say:** *"Which is it? Was Sling TV 50% faster or 70% more productive? Are those the same thing or different metrics?"*

**Fix before the interview:** Remove one, or clearly differentiate them in the resume. Recommended resolution:

| Metric | What It Measures | Keep? |
|--------|-----------------|-------|
| **50% faster delivery** | Timeline compression — expected 18 months, delivered in ~5 months (not quite 50% — that's ~72% faster). The math needs fixing. | **Re-anchor.** If you mean "5 months vs 18 months," that's 72% faster, not 50%. |
| **70% productivity gain** | Output per engineer — a mid-size service that took 2 weeks now takes 3 days. | **Keep.** This is a stronger metric because it's per-engineer. |

**Option A (recommended):** Remove the "50% faster" line entirely. Keep the 70% productivity gain. One metric per project.

**Option B:** Differentiate them explicitly:
> *"Achieved **70% productivity gain** per engineer (a service that took 2 weeks now takes 3 days). The overall migration timeline was compressed from 18 months to 5 months."*

---

### ⚠️ Advisory: Azure/AKS Listed as Skill, Zero Project Experience

**The problem:** Your Technical Skills block says:
> *"Cloud & Platform: Docker, Kubernetes (Rancher), GCP, AWS, and **Multi-Cloud Architecture (Azure/AKS)**"*

But every project on your resume runs on:
- **My Dish:** Rancher-managed Kubernetes
- **Sling TV:** Rancher-managed Kubernetes
- **DPA, STB, Field Catalogue:** Rancher, AWS, GCP
- **MSys projects:** VMware, AWS, GCP

**Zero projects use Azure.** An interviewer's first thought: *"This is a keyword, not experience."*

**What to say when asked:**
> *"I'm honest about the distinction. My production experience is on Rancher-managed K8s, AWS, and GCP. Azure/AKS is listed because I've studied the platform deeply for this role — I understand the concepts (AKS, VNET, Private Link, Key Vault, Application Gateway) and the patterns transfer directly. Kubernetes is Kubernetes — the orchestration concepts are identical. The Azure-specific services (networking, security, identity) follow the same cloud patterns I've used on AWS and GCP. I've prepared for this role by studying the azurerm Terraform provider and Azure networking, and I'm confident I can be productive within the first month."*

**If they push harder:**
> *"I'd rather be honest about a ramp-up period than pretend. I can read and review Azure architecture today. I'd need hands-on time to be productive with the CLI and portal. But the architectural patterns — VNET isolation, Private Link, Key Vault rotation — I've done those on AWS and GCP. The implementation details differ, the principles don't."*

---

## 2. ARCHITECTURE DEEP DIVES (My Dish Platform)

### Q1: "Walk me through the My Dish architecture. What are the services? How do they communicate?"

**What they're testing:** You didn't just list buzzwords — you can describe a real system with real tradeoffs.

**Answer:**
> *"The My Dish subscriber platform is a set of 12+ microservices, each owning a domain capability: subscriber profile, billing, plans, equipment, support tickets, notification preferences. Each service owns its own PostgreSQL database — no shared databases except for cross-cutting reporting (read-only replicas to Athena for analytics).*
>
> *Communication is hybrid:*
> - **Synchronous:** REST over HTTP for request-response flows (profile lookup, plan changes). API Gateway (Kong) routes external traffic, internal services call each other directly via service discovery.
> - **Asynchronous:** Kafka for event-driven flows — when a subscriber changes their plan, the billing service publishes an event, and downstream services (entitlements, notifications, analytics) consume it independently.
> - **Caching:** GemFire distributed cache for hot-path reads — subscriber profiles and device configurations. Cache-aside pattern: read from cache, miss hits the database, populates cache.
>
> *Resilience:*
> - Resilience4j circuit breakers between services — if billing is slow, other services fail fast instead of queuing.
> - Retry with exponential backoff for transient failures.
> - Dead-letter queues for messages that can't be processed after retries.
>
> *Observability:*
> - Dynatrace for distributed tracing — every request gets a trace ID, stitched across all service hops.
> - Prometheus + Grafana for service-level metrics (request rate, error rate, latency percentiles).
> - ELK for log aggregation — search across all services during incident analysis."

---

### Q2: "Why 12 services? How did you decide the boundaries?"

**Answer:**
> *"We used domain-driven design — each service owns a business capability. The boundaries came from the business domain: billing is a distinct capability from entitlements, which is distinct from content recommendations. The rule was: if two things change for different reasons, they should be in different services. If they change together, keep them together.*
>
> *We started with fewer services and split as we hit friction:*
> - Notification preferences split from subscriber profile when the notification team needed independent deploy cycles.
> - Equipment management split from billing when the device lifecycle (activation, swap, return) needed its own data model.
>
> *The number 12 isn't sacred — it's where the domain settled. If a service grows too large, we'd split it further."*

---

### Q3: "How do you maintain 99.9% uptime with sub-second latency?"

**What they're testing:** You claimed a specific number. Can you defend it?

**Answer:**
> *"99.9% uptime means ~8.7 hours of downtime per year. We achieved it through:*
> 1. **Redundancy at every layer:** Multiple API Gateway instances, multiple Kafka brokers, multiple service replicas, read replicas for databases.
> 2. **Graceful degradation:** If GemFire cache is down, services fall back to database reads (slower but functional). If Kafka is down, services queue events locally and replay when Kafka recovers.
> 3. **Automated health checks:** Kubernetes liveness/readiness probes restart unhealthy pods. Dynatrace anomaly detection pages the on-call engineer before users notice.
> 4. **Deployment discipline:** Blue-green deployments via Rancher. Canary testing — 10% traffic to new version, monitor for 15 minutes, then full rollout.
> 5. **Sub-second latency:** Hot data in GemFire cache. CDN for static assets. Database query optimization (indexes, connection pooling, read replicas). p99 latency target of 500ms, p50 under 100ms."

---

### Q4: "What's the API Gateway you use? How did you configure it?"

**Answer:**
> *"We use Kong API Gateway. It handles:*
> - **Routing:** External requests to the right microservice based on path prefix (/api/v1/subscribers → subscriber service)
> - **Authentication:** JWT validation at the gateway level — services don't need to re-validate tokens
> - **Rate limiting:** Per-client, per-endpoint rate limits to prevent abuse
> - **Logging:** Request/response logging for audit and debugging
> - **CORS:** Cross-origin configuration for frontend clients
>
> *We configured it via declarative YAML in our GitLab repo — gateway config is version-controlled and deployed through CI/CD, the same as any service.*"

---

## 3. SPRING BOOT 3 MIGRATION & PROMOTION STORY

### Q5: "Walk me through the actual Spring Boot 3 migration. What broke? What was automatable vs manual?"

**What they're testing:** This is your promotion story. They need to verify you understand the technical details yourself, not just that "AI did it."

**Answer:**
> *"Spring Boot 2 reached end-of-life — no security patches, blocking dependency upgrades. We had 12 services, 50K+ lines of code. The breaking changes were:*
>
> **Fully automated by Kiro (zero human intervention):**
> - `javax.*` → `jakarta.*` namespace rename across all files. This is a mechanical find-and-replace, but across 50K+ lines with nested imports, manual work would take weeks. The agent handled it perfectly.
> - Deprecated API replacements where the new API is a drop-in (e.g., `WebMvcConfigurerAdapter` → `WebMvcConfigurer`).
> - Properties file changes (Spring Boot 2.x → 3.x property renames).
>
> **Automated with human review:**
> - `WebSecurityConfigurerAdapter` → `SecurityFilterChain` — the agent generates the new security config, but the security logic (which endpoints are public, which roles can access what) needs human verification because it's business-critical.
> - Hibernate 5 → 6 — most queries migrated automatically, but dynamic queries and custom Hibernate types needed manual review because the API changes are subtle.
>
> **Manual (flagged by agent for human handling):**
> - Custom annotations that referenced internal Spring APIs that changed between versions.
> - Integration test configurations that needed manual setup changes.
>
> *The key insight: AI automation is great for mechanical changes, but security-critical and business-logic-critical changes need human review. The agent flagged these, it didn't silently change them."*

---

### Q6: "How did you measure the 60% productivity gain?"

**What they're testing:** They assume metrics are made up. Make them real.

**Answer:**
> *"The baseline was historical data. Before the migration, a mid-size service (5-8 endpoints, 3-4 database tables) took a senior engineer approximately 2 weeks to migrate manually — we had done two services manually before adopting the AI approach. After the AI approach, the same scope took 3 days. That's a 70% reduction in time, which I report as 60% to be conservative.*
>
> *The dashboard tracked:*
> - Lines of code changed automatically vs manually
> - Lines of code reviewed by a human
> - Test pass rate before and after migration
> - Time from service assignment to PR creation
> - Defect rate found in code review (AI-generated code had a lower defect rate than manual for mechanical changes)
>
> *The dashboard was critical because it gave leadership visibility into what the AI was actually doing — not just 'trust us, it's faster.'"*

---

### Q7: "Did you push for this migration or was it assigned?"

**What they're testing:** Agency vs assignment. Principal-level candidates drive change, they don't wait for it.

**Answer:**
> *"I pushed for it. Spring Boot 2 was EOL, but the team estimated 18 months to migrate manually across all services. I saw the opportunity to use AI to compress that timeline. I proposed the approach, ran a POC on one service, showed the data (3 days vs 2 weeks), built a dashboard for visibility, and got buy-in from the VP. The promotion followed because the work was visible — I didn't just do the migration, I created a repeatable methodology and scaled it across teams."*

---

## 4. SLING TV MODERNIZATION — Biggest Claims, Most Probing

### Q8: "What did Amazon Q actually output? Did it produce perfect code?"

**What they're testing:** This is the biggest claim on your resume. They will probe hardest here.

**Answer:**
> *"Amazon Q analyzed the codebase and produced:*
> 1. **OpenAPI specs** for each legacy Rails API — extracted from routes, controllers, and database models
> 2. **Java microservice skeletons** from those specs — controllers, services, repositories, DTOs
> 3. **Unit tests** — generated from the specs and existing test patterns
>
> *The output was not production-ready. It was:*
> - **80% correct** for straightforward CRUD APIs (mapping a Rails model to a Spring Boot entity is mechanical)
> - **50-60% correct** for complex business logic (Rails callbacks, conditional validations, implicit state transitions)
> - **30% correct** for integration logic (calling downstream services, handling errors)
>
> *My team's role was: review the generated code, fix the business logic translation, add error handling, write integration tests. The AI did the scaffolding — we did the engineering. The 70% productivity gain came from not writing boilerplate, not from eliminating human review."*

---

### Q9: "2 million lines of Java — what's included in that count?"

**Answer:**
> *"The 2M lines includes:*
> - Generated controller interfaces and implementations from OpenAPI specs
> - Service layer stubs
> - Repository interfaces
> - DTOs and mappers
> - Unit tests (10K+ tests, which contributed significantly to the line count)
> - Configuration classes
> - Build files and CI/CD pipeline configs
>
> *It's not 2M lines of hand-written business logic. It's the full generated surface area of 80+ API endpoints converted to Java microservices. The business logic layer was significantly smaller — the generation handled the mechanical translation, and we wrote the business logic."*

---

### Q10: "How did you validate that the new Java services matched the old Rails behavior?"

**Answer:**
> *"We ran old and new in parallel for 2 weeks:*
> 1. **Feature flags:** API Gateway routed 10% of traffic to the new service initially, 50/50, then 100% — with the ability to roll back instantly.
> 2. **Data reconciliation:** A background job compared responses from old and new systems for every request — if they diverged, we investigated.
> 3. **Dynatrace tracing:** Every request traced across both systems. We could compare latency, error rates, and response patterns side by side.
> 4. **Shadow traffic:** For write operations, the new service processed the request in parallel but didn't persist — we compared the response and only switched to the new path after validation.
>
> *The hardest problems were in data consistency — splitting a monolith's database means losing ACID transactions. We used the Saga pattern on Kafka: each service publishes an event when its local transaction completes, downstream services listen and update their own state, and compensation logic rolls back on failure."*

---

### Q11: "Why 6 bounded contexts? How did you decide?"

**What they're testing:** Real DDD vs keyword dropping.

**Answer:**
> *"We identified 6 bounded contexts by analyzing the Rails codebase:*
> 1. **Billing** — subscription management, invoicing, payments
> 2. **Content Catalog** — channel lineup, metadata, scheduling
> 3. **Entitlements** — what each subscriber can access
> 4. **Recommendations** — personalized content suggestions
> 5. **Device Management** — device registration, activation, profile
> 6. **Support** — ticket management, self-service tools
>
> *Each context had its own:*
> - Data model (no shared database tables)
> - Deploy cycle (independent shipping)
> - Team ownership (small, focused teams)
>
> *The boundaries came from the business domain language — billing talks about 'subscriptions' and 'invoices,' content talks about 'channels' and 'programs.' When the language differs, the service boundary should too."*

---

## 5. AI / MCP / AGENT SKILLS (Differentiator)

### Q12: "How does the Dynatrace MCP server work? What's the security model?"

**Answer:**
> *"The Dynatrace MCP server is a lightweight Node.js service that exposes Dynatrace API capabilities as MCP tools. An agent can:*
> - Query a specific trace by trace ID
> - Get service health metrics (error rate, latency, throughput)
> - List recent incidents
> - Get root cause analysis for a detected anomaly
>
> *Security model:*
> - **Read-only access** — the server uses a Dynatrace API token scoped to read-only permissions. The agent can never modify monitoring configuration, suppress alerts, or delete data.
> - **Scoped by service** — the token is scoped to the specific services the agent is allowed to inspect.
> - **No database access** — the agent traces requests across services but never reads or writes database data.
> - **Audit trail** — every agent query is logged with the agent ID, timestamp, and query parameters."

---

### Q13: "How do you prevent the Snyk agent from introducing new vulnerabilities in its fix?"

**Answer:**
> *"The agent follows a fixed workflow with validation gates:*
> 1. **Read the vulnerability advisory** — Snyk reports the CVE, its severity, exploitability, and the fix recommendation
> 2. **Apply the patch** — agent updates the dependency or applies the code change
> 3. **Run tests** — existing test suite to verify the fix doesn't break anything
> 4. **Re-scan with Snyk** — the agent triggers a new Snyk scan on the modified code. If the scan finds new vulnerabilities, the fix is rejected and the agent backtracks
> 5. **Human review** — the agent creates a PR tagged as AI-generated. A human must review and approve. The agent never merges its own PRs.
>
> *The key guardrail: the agent can create a PR but never merge it. And the re-scan step catches the most common failure mode — fixing one vulnerability by introducing another."*

---

### Q14: "How did you get 5+ teams to adopt your agent skills?"

**What they're testing:** Org influence — the Principal-level skill.

**Answer:**
> *"I didn't mandate it. I did:*
> 1. **Led by example** — my team used the agents and showed concrete results. Snyk fix time went from 2-7 days to same-day. That data was visible.
> 2. **Built documentation** — a playbook with the skill definition, setup instructions, and examples.
> 3. **Held office hours** — 2 hours per week, any team could ask questions or get help setting up their own skills.
> 4. **Let them customize** — the skills are configurable playbooks. Teams could adapt them to their domain (one team integrated with Jira, another with ServiceNow).
> 5. **Tracked adoption** — I shared metrics: 'Team X has been using the defect-fix skill for 3 months, average fix time has dropped from 4 hours to 45 minutes.'
>
> *Within 4 months, 5 teams were using the skills. The key was making it easy to start and showing clear value — not mandating adoption."*

---

### Q15: "If Kiro didn't exist, how would you approach the same problems?"

**What they're testing:** Are you dependent on the tool, or do you own the methodology?

**Answer:**
> *"The methodology is independent of the tool. Kiro is the implementation I chose, but the approach works with any AI coding tool:*
> 1. **Spec-first** — define the contract (OpenAPI spec, test cases) before generating code
> 2. **Iterative generation** — start with scaffolding, then refine with prompts
> 3. **Human review at critical points** — security config, business logic, integration patterns
> 4. **Validation gates** — automated tests, security scans, contract verification
>
> *If Kiro didn't exist, I'd use GitHub Copilot, Amazon Q, or Claude Code — the same approach, different tool. What matters is the workflow, not the specific agent."*

---

## 6. INTERNAL TOOLS & AWARDS

### Q16: "Tell me about the Asset Management hackathon win. What did you actually build?"

**Answer:**
> *"In 48 hours at Codefest 2023, I built a full-stack Asset Management system:*
> - **Backend:** Spring Boot REST API with CRUD operations for tracking company assets (laptops, monitors, phones, peripherals)
> - **Frontend:** ReactJS with a dashboard showing asset status, assignment history, and maintenance schedules
> - **Deployment:** Docker containerized, deployed on internal VMs via JFrog Artifactory
>
> *It automated what was previously a manual spreadsheet process — IT team tracked assets in Excel, updates were delayed, assets got lost. The system reduced manual tracking effort by 70%.*
>
> *Leadership productized it after the hackathon win — it's now used company-wide by IT asset management. The lesson: the hackathon proved the concept, and the productization turned it into a real tool."*

---

### Q17: "Awards — Technical Excellence 2024, 2025, Spot Awards, CPAW. What were they for?"

**Answer:**
> *"Technical Excellence Awards (2024, 2025): Dish's highest engineering award, given to top 1% of engineers. 2024 was for the Spring Boot 3 migration and AI-driven modernization. 2025 was for the Sling TV transformation and the MCP/agent skill ecosystem.*
>
> *Spot Awards (2023, 2025): On-the-spot recognition for impactful work. 2023 was for the Shift Allowance portal — I automated a company-wide manual Excel process. 2025 was for leading the incident response during a major outage and implementing the fix.*
>
> *CPAW Award: For the Dish Paperless Agreement migration — delivering a complex multi-integration project on time with high quality."*

---

## 7. MSYS TECHNOLOGIES — 10 YEARS

### Q18: "10 years at one company — why did you stay so long?"

**What they're testing:** Can you grow, or did you coast? They want to see progression, not stagnation.

**Answer:**
> *"I progressed from Software Engineer to Technical Architect over 10 years. That's four promotions in one company — each role was fundamentally different:*
> - **Software Engineer:** Writing code, fixing bugs, learning the craft
> - **Senior Engineer:** Owning features, mentoring juniors, code reviews
> - **Tech Lead:** Leading a team of 4-5 engineers, scoping work, client communication
> - **Technical Architect:** Owning cross-client architecture decisions, partner-level discussions, delivery governance
>
> *I stayed because the scope kept expanding — I went from writing code to leading client engagements to owning architecture. The growth was real, not just a title change. I left when I hit the ceiling — Dish offered the next level of challenge in terms of scale (10M+ users) and technology (Kubernetes, Kafka, AI)."*

---

### Q19: "5x Best Performer of the Year. What made you stand out consistently?"

**Answer:**
> *"I delivered consistently across client engagements. The common thread: I didn't just take requirements and implement — I understood the client's business problem, proposed better solutions, and delivered on time. Clients would request me specifically for the next project.*
>
> *The recognition was for: technical excellence (writing clean, maintainable code), delivery reliability (consistently hitting deadlines), and client partnership (translating their business needs into technical solutions)."*

---

### Q20: "Pivot3 VMware HCI — what was your role? What did you actually build?"

**Answer:**
> *"I was Technical Lead and Full-Stack Developer for the VMware integration:*
> - **Backend:** REST APIs for storage volume provisioning, monitoring, and management
> - **Frontend:** ReactJS plugin that embedded inside VMware's vSphere UI — admins managed storage from inside their existing tool
> - **Automation:** vRealize Orchestrator workflows that automated bulk provisioning of 1000+ storage volumes — what used to be multi-step manual work per volume became a single-click operation
>
> *The result was a 60% reduction in manual provisioning effort. I also partnered directly with Pivot3's product stakeholders on roadmap, architecture reviews, and release planning."*

---

## 8. PRINCIPAL-ALTITUDE QUESTIONS (Using Resume as Case Study)

### Q21: "Your Spring Boot 3 migration used AI and achieved 60% gains. The next org-wide migration — say, moving 50 services to a new framework — would you use the same approach or change it?"

**What they're testing:** Can you critique your own work? Principal-level means learning from experience.

**Answer:**
> *"I'd use the same approach but with changes:*
> 1. **Same:** Spec-driven, AI-automated, phased rollout with validation gates. The methodology worked.
> 2. **Different:** I'd invest more upfront in the skill definition. For Spring Boot 3, I iterated on the skill after the first 3 services. For a larger migration, I'd run a deeper POC on a representative service first, build a comprehensive playbook, then roll out to all services in parallel — not sequentially.
> 3. **Different:** I'd automate the validation gates better. Currently, we had manual review for security-critical changes. For 50 services, I'd invest in automated contract testing and compliance checking so the agent can self-validate more of its output.
>
> *The biggest lesson from the first migration: the skill definition is the most important artifact. A well-defined skill scales across services. A poorly defined one creates more work for human reviewers."*

---

### Q22: "You've built agent skills for 5 teams. What would it take to scale to 50 teams?"

**Answer:**
> *"Scaling from 5 to 50 teams requires a platform shift, not a linear scale:*
> 1. **Self-service onboarding** — a team should be able to set up their own agent skills from a template, not call me for help
> 2. **Reference implementations** — working examples for common patterns (defect fix, test gen, code review, migration) that teams can copy and adapt
> 3. **Training the trainers** — identify one engineer per team as the local champion. Train them, not the whole team
> 4. **Governance at scale** — a central team that defines guardrails (what agents can do, what they can't do, what requires human approval). Teams customize within those guardrails
> 5. **Health metrics** — dashboard tracking per-team adoption, success rate, time saved, defect rate. Identify which teams are thriving and which are struggling
> 6. **Community** — quarterly showcases, Slack channel, shared playbook that improves with every team's contribution
>
> *The bottlenecks aren't technical — they're cultural and operational. Teams need to trust the agents. Trust comes from seeing results, not from being told."*

---

### Q23: "Your internal tools (Asset Management, Shift Allowance) started as small projects and scaled company-wide. How do you identify which small projects have company-wide potential?"

**Answer:**
> *"I look for three signals:*
> 1. **Pain is universal** — when I hear the same complaint from multiple teams or departments, there's a pattern. Manual Excel workflows for shift allowance affected every employee.
> 2. **Solution is simple** — if the fix is a CRUD app with basic automation, it's likely to work. Complex solutions have higher failure rates for internal tools.
> 3. **Adoption is pull-based** — if I build something and people start asking for it, that's the signal. I didn't force Asset Management on anyone — I showed it at the hackathon, and teams asked for it.
>
> *The pattern: solve a real pain for yourself or your immediate team. If it works, share it. If people adopt it, productize it. If they don't, let it die. Internal tools succeed when they make someone's job measurably easier — adoption comes from demand, not mandate."*

---

### Q24: "Describe a time you disagreed with a VP or architect on a technical decision."

**What they're testing:** Can you disagree without being political? Can you accept a decision and execute?

**Answer:**
> *"Situation:** Leadership wanted to adopt a low-code integration platform for the DPA system. They saw it as faster and easier to maintain.*
>
> *Task:** I needed to evaluate whether it was the right choice for a system with 23 integrations and 7 SFTP distribution targets.*
>
> *Action:**
> - I didn't say 'no' immediately. I acknowledged the goal (faster delivery, lower maintenance) and ran a structured POC.
> - The POC showed that the low-code platform couldn't handle the error handling, retry logic, and monitoring requirements for complex integrations.
> - I documented the limitations and proposed an alternative: Spring Boot microservices with OpenAPI code generation, which gave us the same developer velocity without the constraints.
> - I presented the tradeoffs: low-code would be faster for the first 3 integrations but slower for the remaining 20. Spring Boot would be slower at the start but faster at scale.
> - Leadership agreed. We went with Spring Boot. The project delivered on time, and the platform is still in production.
>
> *Key lesson: Don't oppose — offer a better path with data. And if you're overruled, commit to executing the decision."*

---

### Q25: "What's the biggest technical mistake you've made, and what did you learn?"

**What they're testing:** Honest self-assessment. A candidate who says "I don't have one" is either inexperienced or lying.

**Answer:**
> *"Early in the AI agent work, I built a rigid skill — a fixed 5-phase playbook that assumed every bug fix followed the same pattern. The first few teams tried it and didn't come back. They said 'it doesn't fit our workflow.'*
>
> *I learned: agents need to be adaptable, not prescriptive. I redesigned the skills as configurable playbooks — teams choose which phases to include, set their own guardrails, and customize prompts. The adoption rate went from near-zero to 5 teams within months.*
>
> *The lesson: if you're building a tool for other engineers, they need to feel ownership of how it works. A rigid tool that works perfectly for your team may fail for everyone else."*

---

## 9. VULNERABILITY PROBES — Where You're Exposed

### Q26: "You have AWS and GCP on your resume but no Azure. This role is Azure-native. How do you handle that?"

**Answer:**
> *"I'm upfront about the gap. My production experience is on AWS and GCP. Cloud patterns transfer — Kubernetes, networking, security, identity — the implementation details differ. I've studied Azure specifically for this role: AKS, Azure networking (VNET, NSG, Private Link, Application Gateway), Key Vault, and the azurerm Terraform provider. I'm confident I can be productive within the first month. The architectural thinking is the same — I just need to learn the Azure-specific APIs and CLI."*

---

### Q27: "You have a Google Cloud Data Engineer certification but you're applying for an Azure role. Why?"

**Answer:**
> *"I got the GCP certification to formalize my cloud knowledge — I had been using GCP on the job and wanted to validate my understanding. I chose GCP because that's what my projects used. I'm not platform-loyal — I chose the tool that matched the work. If the role is Azure, I'll get Azure-certified. The cloud concepts are the same — the certification is proof that I can learn a cloud platform to a professional level."*

---

### Q28: "Your Testing section mentions Selenium, JMeter, Postman, Gatling. How much of that is hands-on vs managed?"

**What they're testing:** They want to know if you've personally written tests or just directed testers.

**Answer:**
> *"I've been hands-on with all of them at different points:*
> - **JUnit:** I write unit tests in every service. I mandated 85%+ coverage as a CI gate.
> - **Postman/Newman:** I wrote API test collections for every service. These run in CI.
> - **Selenium:** I built NetApp's regression suite from scratch (100+ scenarios) — personally wrote the test scripts.
> - **JMeter:** I wrote performance test plans for the My Dish platform — load testing, stress testing, endurance testing.
> - **Gatling:** I've used it for load testing Spring Boot services. I prefer it to JMeter for code-based scenarios.
>
> *At the Staff/Principal level, I don't write every test — I define the strategy, set the quality gates, and mentor the team on testing practices. But I can write any of these tools when needed."*

---

## 10. JD-MAPPED QUESTIONS (Azure, Confluent, Kong, Terraform)

### Q29: "How would you deploy a Spring Boot service on AKS with private networking?"

**Answer:**
> *"I'd follow this approach:*
> 1. **Containerize:** Build a Docker image with the Spring Boot app, push to Azure Container Registry.
> 2. **AKS cluster:** Deploy the AKS cluster in a VNET with private endpoints. No public IP for the nodes.
> 3. **Deployment:** Kubernetes Deployment manifest with resource limits, liveness/readiness probes, and config maps for environment-specific configuration.
> 4. **Service:** Internal ClusterIP service — not exposed to the internet.
> 5. **Ingress:** Application Gateway Ingress Controller (AGIC) sitting in the same VNET, routing external traffic to the internal service.
> 6. **Database:** Azure SQL Database or PostgreSQL with Private Link — the database is only accessible from within the VNET.
> 7. **Secrets:** Azure Key Vault with CSI driver — secrets mounted as volumes in the pod, not stored in environment variables.
> 8. **CI/CD:** Azure DevOps pipeline — build, scan (Snyk), test, deploy to AKS via Helm.
>
> *The key constraint: nothing in the architecture is publicly accessible except the Application Gateway. Everything else is private with Private Link endpoints."*

---

### Q30: "You've used open-source Kafka. How does Confluent Platform differ?"

**Answer:**
> *"Confluent Platform adds enterprise features on top of open-source Kafka:*
> - **Schema Registry** — central schema management with Avro/Protobuf, compatibility checks, and evolution rules
> - **Kafka Connect** — pre-built connectors for databases, cloud services, and file systems (vs writing custom connectors)
> - **Kafka REST Proxy** — HTTP interface to Kafka for environments where Kafka clients aren't available
> - **ksqlDB** — stream processing with SQL syntax (competing with Flink but simpler)
> - **Control Center** — UI for cluster monitoring, topic management, consumer group tracking
> - **Multi-region clustering** — replication across data centers for disaster recovery
>
> *At Dish, I used open-source Kafka with some custom tooling. For an enterprise role like The Standard, I understand why Confluent's operational simplicity (Schema Registry, Connect, Control Center) is worth the licensing cost. The core Kafka concepts are identical — the difference is the ecosystem."*

---

### Q31: "What's your experience with Terraform? The role requires it."

**Answer:**
> *"I've used Terraform for infrastructure provisioning on AWS (VPC, EC2, RDS, S3). I'm familiar with:*
> - Terraform CLI (init, plan, apply, destroy)
> - HCL syntax (resources, data sources, variables, outputs, modules)
> - State management (remote state in S3 with DynamoDB locking)
> - Module composition (reusable infrastructure patterns)
> - Workspaces for environment separation (dev, staging, prod)
>
> *I haven't used the azurerm provider in production, but I've studied it for this role. The Terraform patterns are provider-agnostic — the HCL is the same, only the resource types and their properties differ. I'd be productive within a week of hands-on work with the Azure provider."*

---

### Q32: "What API gateways have you worked with directly? Have you used Kong?"

**Answer:**
> *"I've used Kong in production at Dish for the My Dish platform. I configured:*
> - Routes and services (path-based routing, host-based routing)
> - Plugins (JWT authentication, rate limiting, CORS, logging, IP restriction)
> - Upstreams and health checks (load balancing, circuit breaking)
> - Declarative configuration (YAML in Git, version-controlled, deployed via CI/CD)
>
> *I'm familiar with Kong Konnect conceptually — it's the SaaS control plane for Kong Gateway. I haven't used it in production, but I understand the model: a cloud-managed control plane with local data plane proxies. The operational benefit is reduced infrastructure overhead for managing the gateway configuration.*"

---

## 11. QUICK REFERENCE: Resume Claims → Questions

| Resume Claim | Likely Question | Confidence |
|---|---|---|
| "Architected My Dish platform, 10M+ subscribers, 99.9% uptime" | "Walk me through the architecture in detail" | Guaranteed |
| "Spring Boot 3 migration, 60% productivity gain" | "What broke? What was automated vs manual?" | Guaranteed |
| "Promoted from Lead to Staff" | "What made it Staff-level work?" | Guaranteed |
| "Sling TV — reverse-engineered 400K+ lines, 2M+ lines generated" | "What did Amazon Q actually output?" | Very High |
| "70% productivity gain" | "How did you measure it?" | Very High |
| "Custom Dynatrace MCP server" | "How does it work? Security model?" | High |
| "Snyk MCP server, same-day fixes" | "How do you prevent new vulnerabilities?" | High |
| "Used by 5+ teams" | "How did you drive adoption?" | High |
| "50% faster delivery" (Sling TV) | **"Which is it — 50% or 70%?"** | **Fix this discrepancy** |
| "Multi-Cloud Architecture (Azure/AKS)" | "Which Azure services have you used in production?" | **Keyword flag** |
| "Kiro Mobile showcased at Dish Ignite 2026" | "What was the most surprising feedback?" | Medium |
| "Asset Management — Codefest 2023 winner" | "What did you build? How did it scale?" | Medium |
| "5x Best Performer of the Year" | "What made you stand out?" | Medium |
| "85%+ JUnit/Postman coverage" | "How do you enforce quality gates?" | Medium |
| "GCP Professional Data Engineer" | "Why GCP for an Azure role?" | Medium |
| "Mentor engineers" | "Describe a time you mentored someone who disagreed with you" | High |
| "Architecture reviews" | "What does an architecture review look like?" | Medium |
| "Incident response" | "Describe a major incident and your role" | Medium |
| "Pivot3 — 60% reduction in manual provisioning" | "What exactly did you build?" | Medium |
| "Offline-first Android app" | "How did you handle conflict resolution on sync?" | Medium |
| "10 years at MSys" | "Why did you stay so long?" | Medium |
| "Award: Spot Award, CPAW, Technical Excellence" | "What were these awards for specifically?" | Low-Medium |
| "Kong" | "Which Kong features did you configure?" | Medium |
| "Terraform" | "Terraform state management, modules, Azure provider?" | Medium |
| "Confluent Platform" | "Schema Registry, Kafka Connect, Flink?" | Medium |
| "Flink" | "What's your experience with stream processing?" | High (JD gap) |
| "Azure DevOps" | "Your CI/CD is GitLab. How transferable?" | Medium |

---

## Quick Prep: How to Use This Document

1. **Fix the discrepancy first** — The "50% faster" vs "70% productivity gain" conflict on Sling TV will be the first thing an interviewer sees. Resolve the resume text before the interview.

2. **Prepare the Azure gap answer** — Memorize the honest answer for "you have no Azure production experience." Practice it until it sounds natural, not defensive.

3. **Practice the Sling TV answers aloud** — This is your most auditable claim. The Amazon Q output quality question will come. Have a specific, honest answer.

4. **Practice the Spring Boot 3 migration details** — This is your promotion story. Know the specific breaking changes, what was automated, what was manual.

5. **For each Principal-altitude question (Section 8)** — Practice the framework, not the script. The exact question will vary, but the framework (understand → data → options → decision) stays the same.