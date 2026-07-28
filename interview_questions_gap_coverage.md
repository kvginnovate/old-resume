# Interview Questions — Gap Coverage

> Your existing `interview_prep.md` covers **62 questions tied to your resume lines**. This file covers **everything else** — generic technical questions, behavioral STAR questions, and strategy questions that aren't tied to a specific resume bullet but WILL come up.

---

## Part 1: Technical / Concept Questions (Resume-Independent)

### System Design — Classic Whiteboard Problems

| Question | Why They Ask | Prep Notes |
|---|---|---|
| **Design a URL shortener** (tinyurl, bit.ly) | Tests: hash function, read/write ratio, DB sharding, caching. Everyone asks this. | Draw: encode/decode flow, base62 vs hash+collision, redirect (301 vs 302), DB shard by hash prefix, cache hot URLs in Redis. |
| **Design a rate limiter** | Tests: algorithms (token bucket, sliding window), distributed counters, Redis. | Say: token bucket per user is simplest. For distributed: Redis sorted sets or sliding window counter. Which algorithm fits your use case depends on accuracy vs memory tradeoff. |
| **Design a chat system** (WhatsApp, Slack) | Tests: real-time vs polling, message ordering, offline delivery, multi-device. | Say: WebSocket for real-time, Kafka for message persistence, message ordering via client-seq numbers, offline via push notification + catch-up sync. |
| **Design a notification system** | Tests: push vs pull, delivery guarantees, batching, templating. | Say: event → template engine → channel router (push/SMS/email) → provider queue → delivery. Dedup by idempotency key. Retry with exponential backoff. |
| **Design real-time collaborative editing** (Google Docs) | Tests: OT vs CRDT, conflict resolution, operational transforms. | Say: CRDTs (Yjs/Automerge) for modern systems — no central server needed for conflict resolution. OT for legacy (Google Docs). Sync via WebSocket with version vectors. |
| **Design a search autocomplete / typeahead** | Tests: trie data structure, top-K queries, real-time vs batch updates. | Say: trie + top-K per prefix. Cache popular prefixes in Redis. Batch update trending queries hourly. Edge: prefix with 2+ words needs suffix trie. |
| **Design a payment system** | Tests: idempotency, exactly-once processing, ledger, reconciliation. | Say: idempotency key on every request, two-phase commit for critical paths, saga pattern for cross-service, reconciliation job compares ledger against PSP reports daily. |
| **Design a logging / telemetry pipeline** | Tests: write-heavy systems, log levels, sampling, hot vs cold storage. | Say: agents ship logs → Kafka → stream processor (normalize, sample) → hot storage (Elasticsearch, 7d) → cold storage (S3, indefinite). Dynatrace for traces, ELK for text search. |
| **Design a feature flag system** | Tests: flag evaluation latency, targeting rules, gradual rollout, A/B. | Say: flag config in Redis (fast path), change propagation via pub/sub, client SDK caches locally, evaluation server-side for security. Gradual rollout via percentage + user cohorts. |

### Core Distributed Systems Concepts

| Concept | What to Say |
|---|---|
| **CAP Theorem** | C (Consistency) — every read gets latest write. A (Availability) — every request gets a non-error response. P (Partition Tolerance) — system works despite network split. You can pick CA or CP or AP, but in a distributed system, P is non-negotiable. So you choose between CP (consistent, may be unavailable during partition) and AP (available, may serve stale data). Real world: most systems relax consistency for availability. |
| **Saga Pattern** | Choreography (each service publishes events, next service reacts) vs Orchestration (central coordinator tells each service what to do). I used orchestration for DPA — Spring Batch as the coordinator. Choreography for simpler flows. |
| **CQRS (Command Query Responsibility Segregation)** | Separate read model from write model. Writes go through command model (events, validation). Reads go through optimized read model (denormalized, cached). Not for every service — use when read/write patterns are significantly different. |
| **Idempotency** | Same request N times = same result. Keyed by idempotency key (client-provided UUID). Server checks if key already processed → return stored result (not re-execute). Used in payment flows, DPA integrations. |
| **Consistency Models** | Strong (linearizability — slow, hard to scale), Eventual (fast, may serve stale data), Read-your-writes (compromise). Choose based on: does the user need to see their own write immediately? |
| **Consensus (Raft/Paxos)** | Algorithms for agreeing on a value across distributed nodes. Raft is simpler (leader-based). Used in etcd, Consul, Zookeeper. You don't implement it — you use the implementation. |
| **Gossip Protocol** | Nodes periodically exchange state with random peers. Eventually all nodes know the state. Used in Cassandra, Dynamo. No single point of failure. |
| **Hinted Handoff** | When a node is down, another node temporarily stores (hints) the write. When the node comes back, hints are replayed. Used in Dynamo-style systems (Cassandra). |

### Observability

| Question | What to Say |
|---|---|
| **Metrics vs Logs vs Traces — when to use each?** | Metrics (Prometheus): "is it slow?" — aggregated counts, latencies, error rates. Logs (ELK): "what happened?" — structured events, searchable. Traces (Dynatrace): "why is it slow?" — request path across services. You need all three. |
| **What metrics would you track for a microservice?** | RED method: Rate (requests/second), Errors (failed requests/second), Duration (latency p50, p95, p99). Plus: CPU, memory, GC pause time, DB connection pool usage, queue depth. |
| **How do you set meaningful alerts?** | Alert on symptoms (p99 latency > 500ms, error rate > 1%), not causes (CPU > 80%). Use dynamic thresholds (3σ from baseline) instead of static numbers. Page humans only when action is required. |

### Database

| Question | What to Say |
|---|---|
| **SQL vs NoSQL — how do you decide?** | SQL when: relations, joins, transactions, reporting, known schema. NoSQL when: flexible schema, high write volume, simple access patterns, horizontal scaling. Default to PostgreSQL. Use NoSQL only when SQL is wrong. |
| **When would you use DynamoDB vs Postgres?** | DynamoDB: single-digit-ms latency at any scale, simple key/value or query patterns, no joins needed, predictable access patterns. PostgreSQL: everything else — complex queries, joins, aggregations, transactions, reporting. |
| **Database migration strategy** | Expand-contract pattern: (1) Add new schema alongside old. (2) Dual-write to both. (3) Backfill old data. (4) Verify consistency. (5) Remove old schema. Never do in-place migration on a live production DB. |
| **Sharding strategies** | Key-based (hash on user ID → shard N), Range-based (users A-M → shard 1, N-Z → shard 2), Directory-based (lookup table maps key → shard). Key-based is most common. Re-sharding is painful — plan for it. |

### Containers & Orchestration

| Question | What to Say |
|---|---|
| **Why Kubernetes?** | Self-healing, auto-scaling, rolling updates, service discovery, secrets management, multi-environment consistency. At Dish: Rancher manages our K8s clusters — deploy, scale, monitor, rollback from one UI. |
| **How does Kubernetes service discovery work?** | Pods get dynamic IPs. Services provide stable endpoints. kube-proxy watches the API server and programs iptables/ipvs rules to route traffic to healthy pods. DNS: `<service>.<namespace>.svc.cluster.local`. |
| **Health checks — liveness vs readiness vs startup** | Liveness: is the app alive? Restart if dead. Readiness: is the app ready to serve traffic? Remove from load balancer if not. Startup: delay liveness checks during slow startup (prevent unnecessary restarts). |
| **ConfigMaps vs Secrets** | ConfigMaps: non-sensitive config (environment, URLs). Secrets: sensitive (passwords, API keys). Both injected as env vars or mounted as files. Secrets are base64 encoded (not encrypted by default — use encryption at rest). |

### Security

| Question | What to Say |
|---|---|
| **OWASP Top 10 — which matter most in microservices?** | #1 Broken Access Control (most common — JWT not validated, no RBAC), #3 Injection (SQLi via dynamic queries), #6 Vulnerable Components (Snyk scans), #7 Auth Failures (JWT expiry, weak secrets), #10 SSRF (internal service abuse). |
| **How do you secure microservice-to-microservice communication?** | mTLS (mutual TLS — both sides verify each other's certs), short-lived tokens (OAuth2 client credentials), service mesh (Istio/Linkerd handles mTLS transparently), API keys for lower-security paths. Inside the cluster: network policies restrict which services can talk to each other. |
| **Zero Trust — what does it mean practically?** | Never trust, always verify. No implicit trust based on network location. Every request is authenticated and authorized regardless of source. At Dish: DMZ gateway validates every request from STB devices, even though requests come from "internal" IPs. |

---

## Part 2: Behavioral / STAR Questions (Not Tied to Resume Lines)

### Classic Behavioral — Prepare These Stories

| Question | Story from Your Career |
|---|---|
| **Tell me about a time you delivered under a tight deadline** | **Codefest 2023** — built Asset Management in 48 hours during a hackathon. Won first place. Later productized company-wide. |
| **Tell me about a conflict with a peer or manager** | **AI agent adoption resistance** — teams skeptical of AI-generated code. Pair-programmed with early adopters, showed working data (time saved, defect rate). Resistance dissolved after results. |
| **Tell me about a time you had to push back on a requirement** | **Spring Boot 3 migration sequencing** — business wanted all 12 services migrated at once. Pushed back: too risky. Sequenced by dependency graph, ran 3 pilots first, then accelerated. |
| **Tell me about a time you made a mistake** | **First agent skill was too rigid** — fixed 5-phase workflow that didn't fit team workflows. Nobody used it after first try. Redesigned as configurable playbook with customization. Second version was adopted. |
| **Tell me about a time you disagreed with your manager** | **Sling TV migration approach** — manager wanted traditional rewrite. I proposed AI-assisted reverse-engineering (Amazon Q). Built a working prototype on one API to prove the approach. Got buy-in. |
| **How do you handle an underperforming team member?** | **Pairing + structure** — not "you're underperforming" but "let's work on this together, then you take the next one solo." Define clear outcomes, check progress frequently, recognize improvement publicly. |
| **Tell me about the most challenging technical problem you solved** | **Sling TV data consistency** — splitting a monolith's database into per-service databases. Lost ACID transactions. Solved with Saga pattern on Kafka + compensation logic. Tested with chaos engineering. |
| **Tell me about a time you had to make a decision with incomplete information** | **MCP server security boundaries** — when building the first MCP server (Dynatrace), had to decide what permissions to grant AI agents without knowing all use cases. Started with read-only + specific scopes. Expanded iteratively as patterns emerged. |
| **What's the most critical feedback you've received?** | *"Your designs are technically correct but you don't bring the team along."* — I started writing ADRs publicly, running design review sessions, and explaining *why* not just *what* before building. |
| **Tell me about a time you owned a failure** | **See: agent skill failure above.** Explained: what the agent did wrong (test fixing), what I missed (need human verification of test assertions), what I changed (always review AI-generated test expectations). |

### Principal-Specific Behavioral

| Question | Story from Your Career |
|---|---|
| **How do you create alignment across multiple teams?** | **Spring Boot 3 migration** — wrote the migration guide, built the first 3 services as reference implementations, showed data (60% productivity gain). Teams adopted because they saw it worked, not because anyone mandated. |
| **How do you handle a team that rejects your architectural guidance?** | No story directly — but approach: (1) Understand their concerns first — usually valid. (2) Offer to pair on the first implementation — guidance is more credible when you write code together. (3) Compromise on non-essentials while holding the line on what matters (security, operability). |
| **Build vs buy — your framework** | Buy when: it's a solved problem (CI/CD, monitoring, auth), not core to your business, switching cost is low, and the vendor is stable. Build when: it gives you competitive advantage, you need deep customization, or the vendor market is immature. MCP servers: I built because the integration with our specific workflow was the value — buying would have been generic. |
| **How do you evaluate new technology for adoption?** | My AI evaluation group process: (1) Define success criteria — what problem are we solving? (2) Run a structured trial — 2 engineers, 2 weeks, real work. (3) Compare against baseline — time, quality, satisfaction. (4) Write a recommendation — adopt, reject, or limited pilot. Don't adopt without data. |
| **How do you measure developer productivity?** | Lead time (commit to production), deploy frequency, change failure rate, time to restore (DORA metrics). Plus qualitative: engineer satisfaction surveys, retention. For AI specifically: time saved per task, defect rate of AI code vs manual code, number of developers using AI tools. |
| **How do you decide what NOT to work on?** | Follow the bottleneck: what's blocking the most teams or the most critical path? If Spring Boot 2 is blocking every security patch, that's the bottleneck. If the CI pipeline is slow, that's the bottleneck. Everything else waits. Saying no is harder than saying yes — but saying yes to everything is saying no to focus. |

---

## Part 3: Strategy / Vision Questions

| Question | Suggested Answer Framework |
|---|---|
| **What's the future of AI in software engineering?** | The shift from "AI as autocomplete" to "AI as autonomous agent." Today: AI suggests code. Tomorrow: AI reads a spec, implements it, tests it, creates a PR, and monitors it in production. The human shifts from writer to specifier + reviewer. The bottleneck becomes: how good are you at specifying intent? That's why I invested in spec-driven development (Kiro). The companies that win will be the ones that figure out how to trust AI agents safely — that's what governance and MCP scoping solve. |
| **Platform vs product engineering — how do you balance?** | Platform teams exist to make product teams faster. If the platform team is a bottleneck, you've failed. Keys: (1) platform team ships self-service tooling, not bespoke solutions. (2) platform team's success metric is product team velocity, not platform features shipped. (3) platform team spends time embedded with product teams. (4) every platform decision can be justified by: "what product velocity does this unlock?" |
| **What's your vision for engineering excellence?** | (1) Quality is non-negotiable — 85% test coverage, Snyk scans, code review. But quality must be automated in CI/CD, not enforced manually. (2) Speed is the multiplier — fast feedback loops, short lead times, small batch sizes. (3) Leverage is the differentiator — build tools and agents that scale your best engineers' impact. (4) Culture is the foundation — blameless post-mortems, continuous learning, mentorship. Excellence isn't a checklist — it's a system that produces good outcomes by default. |
| **How would you reduce cycle time across an engineering org?** | Follow the value stream: (1) Map the path from idea to production — where does time get spent? (2) Identify the biggest bottleneck — is it code review (add automated checks), CI (parallelize), deployment (automate), requirements (tighten scope)? (3) Fix one bottleneck at a time — measure before and after. (4) Repeat. The single biggest lever at most companies: reduce PR size. Small PRs move faster. |
| **How do you think about incident management at scale?** | (1) Prevention — circuit breakers, bulkheads, chaos engineering. (2) Detection — Dynatrace alerting on symptoms, not causes. PagerDuty escalation. (3) Response — documented runbooks, on-call rotation, clear severity definitions (P1 = customer-impacting, P2 = degraded, P3 = cosmetic). (4) Learning — blameless post-mortems within 48 hours, action items tracked, runbooks updated. (5) Automate — the goal is to eliminate the incident response that requires a human. Every runbook that gets executed more than once should be automated. |
| **What do you think is the most underrated skill for a Principal Engineer?** | Communication — specifically, the ability to explain a complex technical decision to a non-technical audience without oversimplifying or condescending. A Principal Engineer who can't communicate with VPs and PMs is a brilliant IC in a Staff role, not a Principal. The second: listening. Before proposing a solution, understand the constraint that the other person sees but you don't. |

---

## Part 4: Company-Specific Questions

| Question | What They Want to Hear |
|---|---|
| **Why do you want to work here?** | Pre-research the company! Generic: *"Because you work at scale and I solve problems at scale."* Better: *"Your platform handles X million users, and you're migrating from Y to Z. That's exactly what I've been doing at Dish — my experience with Spring Boot migration and AI-augmented modernization maps directly to your challenges."* |
| **What do you know about our tech stack?** | Pre-research! If they're a Java shop: *"You use Spring Boot, Kafka, and Kubernetes — that's my primary stack."* If they're a different stack: *"I see you use Go and gRPC. I've primarily worked in Java, but the distributed systems patterns — circuit breakers, event-driven design, observability — are stack-independent. The adaptability is the skill."* |
| **How would you approach [company-specific challenge]?** | Don't solve it on the spot. Show your process: *"I'd need to understand your current architecture, what's blocking you, and your tolerance for risk. But here's the framework I'd apply: [describe your approach — assessment → phased plan → measure → iterate]."* |
| **Why leave Dish?** | Honest answer: *"I've been at Dish for 4+ years and delivered what I set out to do — architected the platform, drove AI adoption, built an agent practice. The next step in my growth is Principal Engineer, where I define technical strategy at the org level. I want to do that at a company where the scale and the problem space are a match for my experience."* |

---

## Quick Prep — What to Practice Before Interview

### Must-Have Stories (Adaptable to Most Questions)

| # | Story | Adapts To |
|---|---|---|
| 1 | **Spring Boot 3 migration** — strategy, execution, AI tooling, measurement, promotion | Tech strategy, migration, influencing without authority, measuring impact |
| 2 | **Sling TV transformation** — legacy modernization, DDD, AI-assisted reverse-engineering | System design, migration, org design, conflict with manager |
| 3 | **Custom AI agent skills** — building from scratch, MCP, governance, scaling to 5+ teams | Innovation, failure/recovery, scaling impact, leadership |
| 4 | **Hackathon → company-wide tool** (Asset Management) | Delivering under deadline, building for adoption, full-stack |
| 5 | **Incident response process** — Dynatrace, runbooks, PagerDuty | Operational excellence, blameless culture, automation |

### Frameworks to Memorize

| Framework | For |
|---|---|
| **Context → Action → Outcome → Lesson** | Every behavioral answer |
| **Clarify → Boundaries → Architecture → Scale → Tradeoffs → Migration → Ops** | Every system design answer |
| **Rate → Errors → Duration** (RED method) | Monitoring questions |
| **Current state → Business alignment → Phased evolution → Exit criteria** | Roadmap/strategy questions |

### Mental Checklist Before Walking In

- [ ] Have I researched this company's tech stack and engineering challenges?
- [ ] Do I have 3 stories ready that show Principal-level scope? (org-wide, not team-wide)
- [ ] Can I explain every term on my resume in 1-2 sentences?
- [ ] Do I have a clear answer for "why this company" and "why now"?
- [ ] Am I ready for a system design whiteboarding round? (notification system, rate limiter, or similar)
- [ ] Do I have a question to ask them that shows strategic thinking?
