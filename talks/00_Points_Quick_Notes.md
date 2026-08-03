# Talks — Points-Format Quick Notes

**Target:** Principal Software Engineer V — The Standard (IBTE)
**Purpose:** Last-minute revision cheat sheet. One block per talks/ doc: the question it answers, the answer's story essence, and what to remember.

---

## 1. Tell Me About Yourself

**Q:** "Tell me about yourself."
**Answer:**
- Staff Engineer, Dish Network, 14+ years backend architecture & microservices; own end-to-end architecture for subscriber platform (My Dish App): Java/Spring Boot on K8s, 10M+ subscribers, 99.9% uptime, sub-second latency
- Two halves of the job: architecture ownership (patterns, design reviews, ADRs, org-wide standards) + staying hands-on (implement, review code, incident response)
- Biggest contribution: AI spec-driven modernization — agents reverse-engineer legacy code, generate specs, automate breaking-change remediation; MCP servers in Kiro wired to GitLab/Jira for autonomous defect triage/PRs; org-wide adoption; 80+ Rails APIs → Java, 70% faster delivery
- Same playbook: Spring Boot 3 migration (50K+ lines, 60% gain, AI-code dashboard), Snyk MCP (same-day vuln fixes), Dynatrace MCP (30 min → 2 min diagnosis), Crashlytics MCP (mobile debugging), 85% coverage gate
- Sling TV: Amazon Q reverse-engineered 400K+ lines, scaffolded 2M+ lines Java + 10K+ tests, 70% faster
- DPA: ColdFusion → Spring Boot, 23 integrations, 7 SFTP targets; STB Health: Spring Boot 3, 10M+ devices, DMZ gateway, Cognito+Okta
- Personal: git worktrees + parallel AI agents; Kiro Mobile (Dish Ignite 2026); GCP/Firebase MCP POC (spec → provision → deploy → verify, 2-3 days → 5 min, personal project)
- Beyond core role: Field Catalogue (led team, offline-first, +60% on-site sales, Sales VP appreciation); internal tools: Asset Management (Codefest 2023, 70% effort cut), Shift Allowance (HR Spot Award), DISH App Store
- Awards: Technical Excellence 2024 + 2025 (for AI-driven workflows); before Dish: MSys 10 years SE → Technical Architect, 5x Best Performer
- Closer: this Principal role = architecture ownership + org-wide standards, "same pattern, new domain, bigger scope"
**Remember:**
- Three versions: 2 min (floor), 5 min, 10 min (full resume). Start 2-min unless told otherwise; 10-min only when invited
- Numbers are the signal — pause after each; every number has a measurement story ready
- Awards tied to AI workflows, NOT to Field Catalogue/hackathons — keep linkage clean
- GCP POC is personal, not Dish work — frame "on my own time"

## 2. Why The Standard

**Q:** "Why do you want to work here?"
**Answer:**
- Great run at Dish (promoted, awards, org-wide adoption) — leaving for broader scope, not dissatisfaction: one product line (subscriber platform + Sling TV) → multiple (insurance, retirement, investments)
- Reason 1: Bengaluru centre is brand new — founding architecture role, define how things are built from day one
- Reason 2: insurance is event-driven — claims, underwriting, policy = textbook Kafka workflows; already doing exactly that at Dish
- Reason 3: CIO (Greg Chandler) said hardest AI problems first — underwriting, claims, integration — not chatbots; real AI work, not toys
- Closer: "I could have joined any Bangalore GCC, but I chose The Standard"
**Remember:**
- Say "I'm looking because" not "I'm leaving because"; never complain about Dish
- "Do not say IBTE" — keep conversational
- Azure/AKS gap defense: "Kubernetes is Kubernetes, cloud patterns transfer; I've studied Azure for this role"

## 3. Sling TV UMS Modernization

**Q:** "You mentioned the Sling TV modernization and the 80-plus Rails to Java migration — walk me through what you actually did: role, approach, hardest part."
**Answer:**
- UMS = User Management Service: 80+ legacy Ruby on Rails APIs on a monolith; brittle — every deployment high risk, scaling meant vertical scaling, hiring Rails devs harder
- Role = architect + technical lead (led technical direction, did not manage the team); "I proposed" the modernization — defined target architecture, chose stack, designed migration
- Decomposed into 6 bounded contexts via DDD: user profile, authentication, device management, entitlements, user preferences, account settings — each = own microservice + own DB; event-driven over Kafka, REST for sync query flows
- Hardest part: data consistency — splitting a monolith DB loses ACID; Saga pattern (local tx → publish event → downstream updates own state → compensation logic rolls back); took 3 iterations to get right — first compensation bug caught in chaos engineering, not production
- Validation: old + new ran in parallel 2 weeks; feature flags 10% → 50/50 → 100% with instant rollback; data reconciliation job compared both systems per request
- Result: 70% faster delivery per engineer — a 2-week service now takes 3 days
**Remember:**
- 6 contexts: profile, auth, device mgmt, entitlements, preferences, account settings — do NOT say billing/catalog/recommendations (that's the platform, not UMS)
- "Three iterations to get right" on Saga = strongest technical detail — pause before it
- 70% is per-engineer delivery time; scope is UMS only, not the whole platform
- Save Amazon Q / AI details for a follow-up; first answer = architecture + strategy, not tooling

## 4. Influencing Without Authority — AI Spec-Driven Adoption

**Q:** "Tell me about a time you convinced a skeptical team or leader to adopt your approach."
**Answer:**
- Introduced AI spec-driven modernization: agents analyze legacy code, generate OpenAPI specs, scaffold microservices from those specs — "the AI did the mechanical translation, we did the engineering"
- Demoed to VP of Engineering side-by-side: one service manually = 2 weeks; same scope spec-driven = 3 days with fewer defects; VP convinced
- Repeated demo org-wide; within a quarter 5 teams adopted; 80+ Rails APIs → Java, cutting delivery timelines 70%
- Lesson: don't ask people to trust your approach — show the data, let them decide; if it's genuinely better, teams pull it themselves
**Remember:**
- "I didn't argue" — say plainly; VP demo shows you operate at VP level naturally
- 2 weeks vs 3 days + fewer defects = concrete numbers, not opinion; 5 teams in a quarter = organic adoption, no mandate
- Skeptical senior engineer: asked him to try it on his lowest-priority service; he became the biggest advocate
- Keep ~60s — a vignette, not a full migration

## 5. Mentoring — Growing Engineers

**Q:** "Tell me about a time you mentored someone and saw real growth."
**Answer:**
- Mid-level engineer, technically solid but struggled with system thinking — APIs that worked in isolation but caused integration pain downstream
- Paired on architecture reviews; asked guided questions (why is this endpoint here, what if this service goes down, how would you scale this); had him present designs and challenged assumptions
- Progressive ownership: single API endpoint → a whole service → cross-service integration with Kafka + state machine; "each step, I reviewed less and let him own more"
- Within 8 months he independently architected and delivered STB Health Monitor (DMZ gateway + internal service, K8s, Kafka, observability, CI/CD) with minimal oversight
- Promoted mid-level → senior; he started mentoring others — the multiplier effect
**Remember:**
- STB = Set-Top Box; DMZ gateway = security middleman external devices talk to before internal systems
- Proof: 8-month timeline + named deliverable (STB Health Monitor)
- Hardest part was letting him fail safely — productive struggle, no micromanaging
- "He now mentors others" = force multiplier

## 6. Production Incident — itma-auth Memory Leak

**Q:** "Tell me about a production incident — what went wrong, how you handled it, what you changed."
**Answer:**
- itma-auth (central auth, all login + token validation) OOM-killed every 6-8 hours in production on Rancher; ~50,000 req/min; every crash = users couldn't log in; P0
- Detection: pods crash-looping; auto-restart masked it; GC logs showed heap growing steadily with no recovery — classic leak pattern
- Stop the bleeding: doubled heap + daily restart cron — "ugly, but it bought us time"
- Root cause: JMeter (500 concurrent VUs, 30 min) + YourKit heap dump — JWT public key cache: HashMap with zero eviction caching JWKS signing keys; keys rotated every 24h, old keys accumulated; after 7 days 14 stale entries with large cert objects; map grew unbounded until OOM. "The root cause wasn't the cache — no eviction policy and no load testing for memory stability"
- 3 fixes: (1) Guava CacheBuilder — max 50, TTL 6h, LRU; (2) memory stability test — JMeter 30 min peak load asserting heap growth < 10%, now a CI/CD gate; (3) cache checklist — every service documents eviction policy, max size, hit-rate metric, alert on eviction spikes
- Result: zero recurrence in 6 months; checklist caught the same bug class in two other services within a month
**Remember:**
- Numbers: 50K req/min, OOM every 6-8h, 500 VUs, 30 min, heap < 10% gate, cache max 50 / TTL 6h, 14 stale entries, zero recurrence 6 months, 2 services caught
- "The root cause wasn't the cache" = Principal-level insight — pause before it
- Use for: incidents, debugging, RCA, load testing. NOT for: cascading failures/resilience (separate story)

## 7. Disagreement With Leadership — Low-Code Platform

**Q:** "Tell me about a time you disagreed with a decision from above."
**Answer:**
- Leadership wanted a proprietary low-code integration platform after an impressive vendor demo; wanted to standardize across teams
- I disagreed: vendor lock-in, limited customization, wouldn't handle our scale — but didn't just say no; ran a structured evaluation
- Criteria: scalability, team productivity, lock-in risk, TCO, migration path; 2-week POC on a real use case showed clear limits — couldn't handle our Kafka event patterns, limited observability, error handling a black box
- Presented findings objectively with a recommendation matrix; proposed investing in the existing Spring Boot platform: better templates, OpenAPI code generation, shared libraries
- Leadership chose platform-enhancement; delivered starter libraries + OpenAPI code-gen tooling; team velocity +40% (their original goal); trust gained — leadership now involve me earlier in vendor evaluations
**Remember:**
- "I didn't just say no — I ran a structured evaluation" = key reframe; 2-week POC is the credibility
- 40% velocity improvement closes the loop on leadership's original goal; "they now involve me earlier" = trust signal
- Push back only on irreversible consequences (lock-in, security, scaling); reversible decisions — execute, let data speak
- If overruled: document concerns, execute, propose a pilot with clear success criteria; never attack the vendor champion

## 8. Operating Independently — Defining Architecture From Scratch

**Q:** "Tell me about a time you defined things from the ground up with no playbook."
**Answer:**
- Joined the MyDish platform team: no established architecture practice, ad-hoc services, no consistent patterns, no docs; leadership said "make it better" with no direction
- First 2 weeks mapping: listed every service, dependency, pain point, every incident from last 6 months; top 3 problems — no API standards (integration failures), no observability (blind in production), no deployment consistency (all manual)
- Prioritized observability first — "you can't improve what you can't measure": Dynatrace dashboards, structured logging, health endpoint standard; cut incident response time by half
- Built API standards (OpenAPI templates, error formats, pagination); didn't mandate — built the first template, used it on one service, showed integration was faster; teams adopted organically
- "I didn't wait for permission" — started doing and showing results; within 90 days observability on every service, API standards on 3 teams, CI/CD template automating deploys
**Remember:**
- "Showed progress, not proposals" = the key insight; "I didn't wait for permission" = ownership, not defiance
- Deliberate order: observability → API standards → CI/CD; rattle off the "top 3 problems" crisply
- 90-day close makes it concrete; maps directly to the IBTE new-centre role (new GCC, no patterns)

## 9. Cross-Team Initiative — Spring Boot 3 Migration

**Q:** "Tell me about a time you aligned multiple teams to move in the same direction."
**Answer:**
- Divergent Spring Boot versions (some 2.4, some 2.7), different security scanning, inconsistent CI/CD — integration issues, missed vulns, every deploy a different process
- Proposed platform-wide Spring Boot 3 migration + consistent standards; couldn't mandate it — didn't manage those teams
- Migration playbook documenting every breaking change (javax → jakarta, security config, edge cases); automated tooling using AI spec-driven approach across 50,000+ lines
- Weekly migration office hours (drop-in help); no deadline — teams planned around their sprints; dashboard tracking per-service progress — gamification drove adoption; only pushback was scheduling
- Within 3 months all platform services migrated — ahead of the 6-month target; 60% productivity gain; Snyk scanning + same-day vuln fixes became the norm; org-wide adoption; Annual Technical Excellence Award
**Remember:**
- Numbers: versions 2.4/2.7, 50K+ lines, 3 months vs 6-month target, 60% gain, 20+ services
- "I couldn't mandate it — I didn't manage those teams" = key tension line; dashboard + gamification = understanding human behavior
- Hardest automation: javax→jakarta — transitive deps still referencing javax needed a dependency tree analyzer
- 60% measured via before/after time tracking on typical migration tasks, consistent delta across 20+ services

## 10. Balancing Tech Debt vs Feature Delivery

**Q:** "How do you balance paying down tech debt against shipping new capabilities?"
**Answer:**
- Not a binary choice — classify debt by business impact, and that determines the response
- Four categories: security debt (EOL framework, known CVE) — non-negotiable, fixed immediately; scaling debt (breaks under projected growth) — fixed before it blocks; developer productivity debt (slow builds, manual deploys) — quarterly budget; aesthetic debt (ugly but works) — backlog
- Make debt visible: tracked in backlog, tagged, estimated; show correlation between debt and incidents (no circuit breakers → every downstream failure a P0)
- Negotiate a budget: 20% of sprint capacity for platform health, committed with Product; if a feature touches a debt area, include remediation in the estimate; quarterly hardening sprints
- Speak in business terms: not "we need to refactor the billing service" but "the billing service has a 30% error rate during peak traffic, fixing it saves 2 hours of on-call per week"
- 80-20 balance: 80% features, 20% platform health; features-only → brittle, debt-only → ships nothing
**Remember:**
- Rattle off 4 categories deliberately: security, scaling, productivity, aesthetic — each with a different response
- Numbers: 20% sprint capacity, 80-20 split, 30% error rate, 2 hours on-call/week, quarterly hardening sprints
- Process/framework answer, not STAR — conversational; 80-20 is a guideline, flexibility matters
- If Product refuses: show incident correlation first, else compromise 10% for two sprints then review; regret example — over-engineered generic caching layer: "don't fix debt you don't have yet"

## 11. Technical Leadership Across Multiple Teams

**Q:** "How do you provide technical leadership when you don't manage the teams?"
**Answer:**
- Three pillars: architecture guilds (weekly sync, ADRs), shared standards (Spring Boot starter libs, CI/CD templates, API guidelines — built, not mandated), staying hands-on
- "Credibility comes from doing, not just directing"; highlight team wins, nominate engineers, tech talks
- "Consistency, not conformity" — recommended pattern + when it's okay to deviate
**Remember:**
- "Consistency, not conformity" — pause before it
- Measure: voluntary adoption count, ADR references, design-review requests

## 12. Handling a Resistant Team

**Q:** "What if the team still says no?"
**Answer:**
- Diagnose resistance: fear / workload / skepticism / valid objection
- Workload → implement it myself on their service; results drop resistance
- Skepticism → find 1-2 enthusiasts, help them succeed quietly — peer influence beats authority
- Valid objection → accept + document the exception; unwilling → wait for an incident the practice would have prevented
**Remember:**
- "I do the first one myself" — strongest signal; absorb cost, don't delegate
- Follow-up: "don't abstract until you've seen the pattern three times"

## 13. AI Memory Systems — SuperMemory and claude-mem

**Q:** "How do you keep agents from losing context across sessions?"
**Answer:**
- 3-layer memory: (1) markdown knowledgebase (ground truth), (2) SuperMemory MCP (shared cross-agent store), (3) claude-mem (session recorder, AI-compressed summaries injected into future sessions)
- Progressive disclosure: compact index → timeline → full detail only when needed; ~10x token savings
- Result: consistent defect triage, agents carry conventions themselves
**Remember:**
- "Retrieval over context stuffing" — the one-line answer
- claude-mem: 89K+ GitHub stars, Apache 2.0, `npx claude-mem install`
- Honest scope: "I wired in" not "org-wide"

## 14. Kiro and AI-DLC — Spec-Driven Development

**Q:** "How do you actually use AI in day-to-day development?"
**Answer:**
- Anti-"vibe coding": AI-DLC (AI-Driven Development Life Cycle) on Kiro (AWS agentic IDE)
- Plan before you code — spec first (AGENTS.md master spec); three phases: Inception (user stories + acceptance criteria) → Construction (architecture, sequence diagrams, agents write code AND tests) → Operations (IaC + pipelines)
- Features: steering files (conventions), hooks (validations on save/commit), MCP servers (live tools)
- "Same discipline as a traditional SDLC, with the speed of automation"
**Remember:**
- "Plan before you code" — thesis in four words
- Umbrella topic tying all AI stories together

## 15. Enterprise AI Governance — The Agent Control Plane

**Q:** "In an insurance company, how do we trust agents?"
**Answer:**
- Reframe: "the question isn't whether agents can do the work — it's whether you can govern, audit, and control them"
- Three rules: scoped permissions, audit trails (identity/timestamp/params), human approval gates for irreversible actions
- Concrete: GitLab MCP reads/creates PRs but never merges; provisioning creates but never deletes billing resources; 3 tries then escalate
- Output validation: tests pass old AND new code, security rescan, iteration limit — "judged against a contract, not vibes"
**Remember:**
- "Govern, audit, control" — the 2026 enterprise language
- Insurance tie: claims/underwriting regulated → model inventory, risk assessment, auditable logging
- Dish is telecom, not insurance — be honest, pivot to the transferable framework

## 16. Git Worktrees and AI — Parallel Feature Development

**Q:** "How do you keep multiple AI agents from stepping on each other?"
**Answer:**
- Isolation at the branch level: one git worktree per agent — own directory, branch, index; shared history/object store; agents physically cannot overwrite each other
- Workflow: clean baseline → green tests → hand to agent → review another's output while it runs
- Hard part is recombination: conflicts defer to merge time; merge sequentially or rebase before PR
- Failed experiments cost nothing: delete dir + branch in one command
**Remember:**
- Worktree = Git 2.5 (2015), ten-year-old feature AI made essential
- Eliminates 4 failure modes: file overwrites, context contamination, git lock contention, stale code

## 17. AI Glossary — 2026 Key Terms

- **Agent** — perceives, acts, maintains goals, loops autonomously; not a chatbot
- **Agent loop** — bounded perceive → think → act → observe until goal/budget/halt
- **Vibe coding** — accepting AI code without reading it; anti-pattern
- **ReAct** — Reason + Act: interleaved thought + tool calls; default production loop
- **Subagents** — child agents with own context window and tool budget; one level deep
- **MCP** — open JSON-RPC 2.0 standard connecting LLM hosts to tools; 10,000+ public servers
- **A2A** — agent-to-agent protocol; complements MCP (agent↔tool)
- **RAG** — retrieval-augmented generation; complements fine-tuning
- **Context engineering** — designing what loads into the context window; 2026 successor to prompt engineering
- **Prompt caching** — reused prefix segments at ~10% input cost
- **Durable execution** — checkpointed workflows surviving crashes (Temporal, Inngest, Restate)
- **Evals** — test set + rubric grading an agent over time; the agent's unit-test suite
- **Agent control plane** — governance layer: permissions, audit, approval
- **HITL vs HOTL** — human reviews each decision vs monitors without gating every step
- **Prompt injection** — adversarial content in retrieved data manipulates model; LLM01 OWASP 2025 Top 10

## 18. Kafka Event-Driven Architecture for Sling TV

**Q:** "Walk me through the event-driven architecture for Sling TV."
**Answer:**
- Legacy: 80+ Rails APIs, tightly coupled sync REST, failure cascades
- 4-step design: (1) event boundaries — keep REST for immediate responses (auth), move billing/notifications/analytics/recs to Kafka; (2) event contracts — event ID/type/timestamp/payload; (3) partition keys — subscriber ID for ordering (billing sees created before upgraded); (4) topic config — RF 3, 12 partitions, 7-day operational / 30-day audit retention
- Consumers: own consumer group per service, DLQ after 3 retries with exponential backoff, idempotent via event ID
- Result: independent scaling, no failure cascade, event replay
**Remember:**
- Subscriber-ID partition key = strongest technical signal — say it deliberately
- Cold numbers: RF 3, 12 partitions, DLQ after 3 retries
- Consistency follow-up → Saga pattern (from UMS)

## 19. Translating Business Requirements Into Technical Solutions

**Q:** "How do you turn a business requirement into a technical solution?"
**Answer:**
- "I don't start with technology" — understand the problem first: what problem for the customer, what success looks like + how measured, constraints
- Reframe: "subscribers see their bill within one second" may really be about reducing support calls — changes the solution entirely
- Map to technical constraints: p99 < 1000ms → caching/optimized queries/CDN; "never lose a transaction" → exactly-once Kafka, outbox, idempotent APIs, DLQs
- Options with trade-offs (A: 2 sprints limited scale vs B: 4 sprints full scale), recommend with data
- Communicate in business terms: "real-time bill updates, 200ms average" — not "three microservices with Kafka"
**Remember:**
- "I don't start with technology" — say it first
- Bill example is real: support calls dropped after layout/explanation/FAQ fix; page speed was fine

## 20. Principal Question Inventory

**Q:** "Which questions are covered, which are still open?" [inferred]
**Answer:**
- ✅ Covered: resume deep dives (1, 3, 21, 28), AI/Agents (4, 13, 14, 15, 25), leadership/behavioral (2, 4-12, 19), system design (24), Azure gap (26), Flink (27), first 90 days (23)
- OPEN — Resume deep dives: why 12 services/boundaries, defending 99.9% + sub-second, Kong config, measuring the 60% gain
- OPEN — AI: judging AI-code correctness, biggest AI failure
- OPEN — Technical Strategy & Governance (Principal-signature): long-term multi-team strategy, tech selection process, governance/ARB/ADR mechanisms, OKR cascade, API evolution without breaking consumers, platform metrics/SLOs/DORA — ALL 9 still open
- OPEN — System design: notification system, 10x growth, explaining distributed systems to juniors
- OPEN — Cloud: AKS private networking, Terraform/Azure, Key Vault/RBAC/CSI, hardest cloud bug
- OPEN — Career: 10 years at MSys, 5x Best Performer, questions for us
**Remember:**
- Numbers drill: 60% Spring Boot 3 (per-engineer output) vs 70% Sling (delivery) vs 70% Amazon Q (effort) vs 50% NetApp (separate project) — keep separate
- 6 Sling bounded contexts ≠ 12 My Dish services

## 21. Walk Me Through the My Dish Architecture

**Q:** "Walk me through the My Dish architecture."
**Answer:**
- 12 microservices, each owns a domain (subscriber profile, billing, plans, equipment, support tickets, notification prefs) + own PostgreSQL; no shared DBs except read-only analytics replicas
- Hybrid comms: REST for request-response (Kong API Gateway at edge: JWT auth, rate limiting); Kafka for reactions (plan change → billing publishes; entitlements/notifications/analytics consume independently)
- GemFire distributed cache (cache-aside) for hot paths; Rancher-managed K8s
- 10M subscribers, 99.9% uptime, sub-second latency — via redundancy, graceful degradation, Dynatrace anomaly detection paging before users notice
- Role: owned end-to-end — integration patterns, API standards, security gates, observability; made standards self-service
**Remember:**
- Follow-ups: 12 services = friction-driven splits ("change for different reasons → different services"); 99.9% = Dynatrace request-based SLI, 8.7 hrs/yr budget, RCA per incident; 99.9% had a before: ~99.5% → 99.9% via observability
- Kong = open-source, self-hosted, sub-ms, K8s-native
- Say "ninety nine point nine" and "sub second" slowly; name 4-5 domains, not all 12

## 22. STB Health Monitor — DMZ Gateway, Cognito+Okta, Certificates

**Q:** "Walk me through STB Health Monitor. Why Cognito AND Okta? How do you rotate certs on 10M+ devices?"
**Answer:**
- Spring Boot 3 on Rancher K8s; field techs scan QR codes, upload STB telemetry across 10M devices; runs in a DMZ (separate network segment, strict firewalls)
- DMZ gateway = NGINX reverse proxy: JWT auth, rate limiting, routing — the only entry point
- Cognito = consumer IdP (initial login, issues JWT); Okta = enterprise IdP (validates token + permissions); OAuth lifecycle (refresh, revocation, validation) in custom service on Spring Security OAuth2
- Cert rotation: custom service, cron every 30 days, generates cert → signs with internal CA → pushes to devices; revocation + renewal; Spring Cloud Config + distributed lock (one instance at a time)
- Dynatrace end-to-end; GitLab + Jenkins CI/CD; 10,000 req/s at 99.9% SLA
**Remember:**
- Most probe-rich resume bullet — expect OAuth-lifecycle + cert-rotation follow-ups
- Cognito=consumer, Okta=enterprise, two-step = IdP flexibility
- Compromised device → revoke + reissue; distributed lock prevents concurrent rotation

## 23. First 90 Days as a Principal Engineer

**Q:** "Walk me through your ideal first 90 days at The Standard."
**Answer:**
- Mindset: Listen, Align, Deliver — no "hero architect" day-1 refactor declarations
- Days 1-30: map technical (underwriting/claims/policy flows, debt), organizational (1-on-1s with tech leads/PMs/architects), operational (shadow on-call)
- Days 31-60: ship one high-impact, low-risk win with the team (API contract, slow Kafka pipeline, AI guardrails in CI/CD) — prove leadership elevates velocity
- Days 61-90: synthesize multi-quarter roadmap aligned to business goals; governance: lightweight ADR templates, security gates, shared agentic skills
- By day 90: self-service standards + clear vision across multiple squads
**Remember:**
- "Listen before prescribing" — separates Principal from dogmatic architect
- Build trust with squad leads + PMs as priority #1

## 24. System Design — Insurance Claims & Payment Processing on Kafka

**Q:** "Design an event-driven insurance claims and payment processing platform."
**Answer:**
- Event-driven microservices on Apache Kafka + Spring Boot; API Gateway (Kong/Azure APIM) with OAuth2/JWT, rate limiting, payload validation → Claim Ingestion Service → `claims.received`
- Async chain: Adjudication (`claims.adjudicated`) → Payment Processing (`payments.disbursed`) → Audit & Compliance (all topics → immutable S3/Azure Blob, WORM, for HIPAA/financial compliance)
- Schema evolution: Confluent Schema Registry, strict BACKWARD_TRANSITIONAL Avro/Protobuf — breaking changes blocked at CI/CD build
- Ordering: partition by claim_id/policy_number; idempotency: Transactional Outbox (atomic DB commit + Kafka publish) + dedup on event_id; DLQ + alerts; Resilience4j retry exponential backoff
- Result: sub-second routing, guaranteed audit trails, millions of annual claims
**Remember:**
- Key signals: Schema Registry + Outbox = production-grade EDA; WORM immutable audit = insurance-fit compliance
- Spec table: Kafka 3x replication, event_id dedup key, Kong/Azure APIM at edge

## 25. Scaling AI Agent Skills from 5 to 50+ Teams

**Q:** "How would you scale your AI agent skills across an enterprise of 50+ teams?"
**Answer:**
- Shift from ad-hoc scripts to an Enterprise Agent Control Plane — "you can't just share prompt files"
- Pillar 1 — Centralized Hub: skills as versioned artifacts in an internal registry (npm/PyPI-style or GitHub Releases); structured specs (EARS/JSON-schemas) with input/output contracts
- Pillar 2 — Security & Compliance: MCP gateways as proxy boundaries — RBAC + short-lived least-privilege tokens; PII/secret redaction + DLP before data reaches LLM providers; central audit logging
- Pillar 3 — Champion Model: "Agent Guild" of tech leads; community skills must pass automated CI eval suites (accuracy, latency, boundary cases) before promotion
**Remember:**
- 3 pillars: versioned packages / control plane / guild + CI evals — skills as managed software artifacts
- MCP gateway = security proxy boundary

## 26. AWS and GCP to Azure AKS Migration Strategy

**Q:** "Your experience is AWS/GCP, but our platform is Azure/AKS. How do you bridge that?"
**Answer:**
- Principal-level cloud work = abstractions, patterns, operational controls — not provider syntax; primitives map ~1:1
- "Kubernetes is Kubernetes": Rancher/EKS/GKE → AKS (orchestration, ingress, HPA, Helm identical); IAM/GCP Service Accounts → Azure Managed Identities + Entra ID; SQS/Kinesis/Pub-Sub → Event Hubs/Service Bus
- Azure-native: AKS in private VNets with Azure CNI, private endpoints, API server authorized IP ranges; Key Vault via Secrets Store CSI Driver + Workload Identity (eliminate static credentials); Micrometer → Azure Monitor + Dynatrace
- Terraform/cloud-agnostic patterns → Azure ramp-up negligible; focus on governance, compliance, reliability
**Remember:**
- Mapping table: EKS→AKS; IAM→Workload Identity/Entra ID; Secrets Manager→Key Vault CSI; MSK/Kinesis→Event Hubs/Service Bus; CDK→Bicep
- Confidence without defensiveness; private VNets + Workload Identity + Key Vault CSI = enterprise security maturity

## 27. Flink and Stream Processing Experience

**Q:** "We use Apache Flink. What's your experience with real-time stream processing?"
**Answer:**
- Foundation: Apache Kafka + event-driven state processing — sliding-window aggregations, out-of-order handling, DLQ mechanics in Spring Kafka; production via Kafka Streams, Kafka Connect, custom Spring Boot services
- Concepts translate: RocksDB state backend + Kafka changelog ↔ Flink stateful operators; watermarks + windows for late data; exactly-once via two-phase commit across Kafka producers + DB outboxes
- Knows Flink model: JobManager, TaskManager, state checkpointing, dynamic scaling; Flink Kubernetes Operator — "days, not weeks" to ramp
**Remember:**
- Honest alignment: claim Kafka Streams/Spring Kafka directly; NO false Flink production mastery — no bluffing
- Concept map: changelog topics ↔ Chandy-Lamport checkpoints/savepoints

## 28. Validating Amazon Q Modernization — 2M Lines Code Fidelity

**Q:** "What did Amazon Q actually output? Was the 2M lines production-ready?"
**Answer:**
- Lead with honesty: Amazon Q did NOT autonomously generate 2M production-ready lines; 2M = total legacy codebase (Rails + legacy Java) transformed; Q = acceleration engine in a human-in-the-loop harness
- What Q output: boilerplate translation, schema mapping, legacy controllers → Spring Boot 3 DTOs; flaws left: unoptimized DB access, legacy exception patterns, incomplete security filters
- Validation: Kiro + EARS extracted specs/API contracts BEFORE touching code; parallel-run differential testing — shadow traffic (traffic mirroring) against legacy + new in staging, automated diff on API responses; 10K+ generated unit/integration tests, coverage >85%
- Amazon Q cut manual refactoring effort 70% → seniors focused on boundaries, DB isolation, security
**Remember:**
- Biggest resume claim — expect hardest probing; disarm with honesty first
- Fidelity proof = shadow-traffic differential testing + 10K tests at 85%+; keep 60% (Spring Boot 3) vs 70% (Amazon Q) separate

## 29. Team AI Enablement — Figma MCP, Pencil MCP, NotebookLM

**Q:** "How do you actually get a team to adopt AI tooling?"
**Answer:**
- Adoption = engineering problem with two variables: reduce friction to first value + reduce learning cost
- Figma MCP: agents get live design context (Code Connect maps component → code file) — generated code matches design system
- Pencil MCP: design-in-IDE, local-only (nothing leaves machine) — "AI suggests, you approve"
- NotebookLM: fed docs/notes/transcripts → study guides, flashcards, quizzes — grounded with citations
- Pattern: MCP = standard socket (plug in, don't build custom); playbook: prove on real work → integrate → make learning cheap
**Remember:**
- Three tools, three jobs: Figma MCP = design context, Pencil = in-IDE iteration, NotebookLM = learning
- "Tools change, the enablement playbook doesn't"

## 30. Standard Insurance Interview Feedback — Defense & Scripting

**Q:** "What feedback did the Standard interview produce and how do I defend each gap?"
**Answer:**
- Gap: Siloed environment → defense: 7 downstream service teams, InfoSec/Identity (Okta/Cognito), K8s Platform/DevOps, HR/Ops & Field Sales VPs; DPA 23 integrations + 7 SFTP
- Gap: component deep-dive too shallow → defense: STB Health Telemetry Gateway full chain: DMZ API gateway → Okta+Cognito JWT → GemFire (sub-10ms) → Resilience4j Bulkhead/RateLimiter → Kafka async telemetry → HikariCP (max=30, min=10, 250ms) + Liquibase → Dynatrace
- Gap: can't convince team → defense: Spring Boot 3 + Kiro POC → empirical benchmark (60% effort reduction, 85%+ coverage, clean Snyk) → ADR + agent skills + GitLab CI/CD gates → VP+ demo
- Gap: no Confluent Kafka experience → defense: bridge RabbitMQ/JMS/REST to Kafka fundamentals: Schema Registry (Avro, BACKWARD/FULL), partition keys (subscriber_id/claim_id), MANUAL_IMMEDIATE offsets, DLTs with exponential backoff, idempotent consumers
- Gap: rambling answers → fix with BLUF + Signposting (Rule of 3) + STAR + quantified metrics
**Remember:**
- Strength anchors: HR Spot Award (Shift Allowance), Codefest 2023 (Asset Management, 70% cut), Field Catalogue (+60% on-site sales), 10M+ STB
- Never "we made a REST API" — always the full chain (DMZ → Okta → GemFire → Resilience4j → HikariCP/Liquibase → Dynatrace)
- 4-step answer standard: BLUF → "3 areas: X, Y, Z" → exact stack mechanics → metric impact

## Tell Me About Results

**Q:** "Tell me about results."
**Answer:**
- Lead: Asset Management, Codefest 2023 hackathon, adopted company-wide
- Full ownership beyond code: Docker containerized Spring Boot + ReactJS, Portainer on internal VMs, JFrog artifact registry/deployment → self-service deploy, any team spins it up; cut manual tracking effort 70%
- Shift Allowance portal: automated manual Excel workflows for HR/payroll → Spot Award, now used company-wide by every DISH employee
- Pattern: identify manual process → build full-stack → make it deployable/operational so it scales beyond own team
- Backups: 80+ Rails → Java (70% faster); 50K+ lines Spring Boot 3 (60% productivity); 400K+ reverse-engineered / 2M+ scaffolded (Amazon Q, 10K+ tests @ 85%); DPA 23 integrations / 7 SFTP
**Remember:**
- Docker + Portainer detail is the differentiator — most engineers stop at code
- End-to-end ownership framing: code → container → production

---

## Cross-Doc Quick Reference

| Topic | Doc | One-line |
|---|---|---|
| Intro | 1 | 14+ yrs, AI spec-driven modernization, 10M subs, org-wide adoption |
| Why Standard | 2 | Broader scope, founding Bangalore role, event-driven insurance, CIO AI vision |
| Sling UMS | 3 | UMS (User Mgmt Service): 80+ Rails → Java, 6 bounded contexts, Saga (3 iterations), feature flags, 70% faster/engineer |
| Adoption w/o authority | 4 | Show data not arguments; VP demo 2 weeks vs 3 days; 5 teams in a quarter |
| Mentoring | 5 | Guided questions + progressive ownership; 8 months mid→senior |
| Incident | 6 | itma-auth JWT cache HashMap OOM every 6-8h at 50K req/min; Guava CacheBuilder (max 50, TTL 6h) + memory gate; zero recurrence 6 months |
| Disagree w/ leadership | 7 | 2-week POC beat the argument; 40% velocity |
| From scratch | 8 | Observability-first, progress not proposals, 90 days, "didn't wait for permission" |
| Cross-team | 9 | Spring Boot 3: 3 months vs 6 target, 50K+ lines, 60% per-engineer gain, gamified dashboard, award |
| Tech debt | 10 | 4 categories (security/scaling/productivity/aesthetic), 20% sprint, 80-20 |
| Multi-team leadership | 11 | Guilds, shared standards, hands-on; consistency not conformity |
| Resistant team | 12 | Diagnose 4 causes; do the first one yourself |
| AI memory | 13 | 3-layer memory; retrieval over context stuffing |
| Kiro AI-DLC | 14 | Plan before you code; Inception/Construction/Operations |
| AI governance | 15 | Govern, audit, control; scoped perms + approval gates |
| Worktrees | 16 | One worktree per agent; conflicts at merge time |
| AI glossary | 17 | 15 key terms: agent, MCP, ReAct, evals, control plane... |
| Kafka Sling | 18 | RF 3, 12 partitions, subscriber-ID key, DLQ |
| Business→tech | 19 | I don't start with technology |
| Question inventory | 20 | Coverage map + open questions; numbers drill |
| My Dish arch | 21 | 12 services, REST+Kafka hybrid, GemFire, 99.9% |
| STB Health | 22 | DMZ NGINX, Cognito+Okta, 30-day cert rotation |
| First 90 days | 23 | Listen, Align, Deliver |
| Claims system design | 24 | Schema Registry + Outbox + WORM audit |
| 5→50 teams | 25 | Versioned registry, MCP guardrails, Agent Guild |
| AWS/GCP→Azure | 26 | Kubernetes is Kubernetes; mapping table |
| Flink gap | 27 | Kafka Streams foundation, concepts translate, no bluffing |
| Amazon Q fidelity | 28 | Shadow-traffic diff testing, 10K+ tests |
| Team AI enablement | 29 | Reduce friction + learning cost; Figma/Pencil/NotebookLM |
| Interview feedback | 30 | 5 gaps + defenses; 4-step answer standard |
| Results | — | Asset Mgmt + Shift Allowance; code → container → production |
