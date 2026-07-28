# Principal Engineer Interview Preparation

> Supplement to `interview_prep.md` (Staff-level coverage). This covers the **additional** categories and question types you'll face at Principal level — strategy, org design, executive alignment, and influence without authority.

---

## The Shift: Staff → Principal

| Dimension | Staff | Principal |
|---|---|---|
| Scope | Multiple teams | Organization / company-wide |
| Influence | Cross-team | C-level visible |
| Time horizon | 6–12 months | 2–5 years |
| Decisions | Technical architecture | Technical strategy + org investment |
| Audience | Eng leadership | VP+ |

Your existing `interview_prep.md` covers Staff-level depth. Principal interviews will still ask those but at a **higher altitude** — not "how you did it," but "how you decided to do it, how you measured business impact, and what you'd do differently."

---

## Category 1: Technology Strategy & Roadmap

These test whether you can chart a multi-year evolution path, not just design a system.

### Q: What should our 3-year technical roadmap for this platform look like?

**What they're testing:** Can you sequence engineering direction against business goals in phases, not a Big Bang?

**Framework for your answer:**
1. **Current state assessment** — What works, what's accruing debt, what's blocking velocity
2. **Business alignment** — What does the business need in the next 3 years? (faster delivery, new markets, cost reduction, reliability)
3. **Phased evolution** — Year 1: critical migrations + quick wins. Year 2: platform consolidation. Year 3: differentiation
4. **Exit criteria per phase** — How do you know when to stop a phase vs. continue investing

**For Dish context:**
- What comes after Rancher-managed K8s? (GitOps? Service mesh? Multi-cloud?)
- GemFire → Redis or keep? Criteria: cache hit ratio, operational overhead, licensing
- API governance evolution — from "write OpenAPI specs" to "automated compliance gates"
- AI practice — from agent skills per team to a shared agent platform

---

### Q: How do you decide which technical debt to prioritize?

**What they're testing:** Principled tradeoff framework, not "we always keep it clean."

**Framework:**
1. **Classify debt by risk** — Security (Snyk CVEs), velocity drag (slow CI, hard-to-change code), reliability (frequent incidents), cost (inefficient infra)
2. **Rank by business impact** — A debt blocking a product feature > a debt that makes code ugly
3. **Create a technical debt budget** — X% of each sprint goes to debt. The team decides what
4. **When to carry debt** — Known expiration date, temporary product push, or strategic bet (e.g., "we'll replace this in 12 months anyway")

**Your story:**
- Snyk vulnerability remediation — same-day for critical, weekly for high, quarterly for medium
- Spring Boot 2 → 3 — security debt (EOL) that blocked feature delivery → prioritized over everything else
- ColdFusion DPA — carried debt for years until migration was viable, then paid it off in one project

---

### Q: Your AI practice is used by 5 teams now. What would it take to scale to 20 teams?

**What they're testing:** Can you think about scaling an engineering practice, not just building a tool?

**Framework:**
1. **Platform, not project** — The approach that worked with 5 teams (training, consulting, hand-holding) doesn't scale linearly. Needs to become a platform: reference implementations, self-service onboarding, documentation, office hours
2. **Internal champions** — Identify one engineer per team who becomes the local expert. Train the trainers
3. **Health metrics** — Track per team: agent adoption rate, time saved, defect rate of AI-generated code, engineer satisfaction. Surface which teams are thriving and which are struggling
4. **Governance at scale** — Central team defines guardrails (what agents can/can't do). Teams adapt the playbook to their domain
5. **Feedback loop** — Every team that adopts improves the playbook. Central team curates and redistributes

---

### Q: Where should our infrastructure strategy go next?

**What they're testing:** Can you think beyond the stack you know to see its limits and what comes next?

**Points to have a view on (choose 2-3):**
- **Container orchestration evolution** — Rancher works today. Where does it max out? Would you look at OpenShift? What about moving to managed K8s (EKS, GKE) to reduce operational overhead?
- **Caching strategy** — GemFire served you well. But is it the right long-term choice vs. Redis (lower ops, broader ecosystem) when you don't need GemFire's advanced features (WAN replication, continuous query)?
- **Observability consolidation** — Dynatrace + Athena is your current stack. Any gaps? Cost concerns? Would you add OpenTelemetry as a standard to avoid vendor lock?
- **Multi-cloud / cloud-native** — Dish runs on-prem? Hybrid? Should anything move to cloud? What's the criteria?

---

## Category 2: Organizational Design

### Q: How would you organize engineering teams to scale this platform?

**What they're testing:** Understanding of team topologies, bounded contexts, and platform team dynamics.

**Framework:**
1. **DDD-driven team boundaries** — Each team owns a bounded context (subscriber management, billing, content, entitlements). Team owns the domain end-to-end: API, data store, deployment
2. **Platform team** — A small team that owns shared concerns (API gateway, observability, CI/CD, security scanning). Serves product teams. Success metric: product team velocity, not features shipped
3. **API governance** — Centralized standards, decentralized execution. Platform team maintains the OpenAPI contract repo and enforcement gates. Product teams build the APIs
4. **Team size** — 6-8 engineers per team. More than that = split the domain. Less than that = combine or you're under-invested
5. **Evolution** — When a shared pattern emerges across 3+ teams, the platform team productizes it. When a domain grows too large, split it

---

### Q: Your platform team ships internal services. How do you prevent it from becoming a bottleneck?

**What they're testing:** Understanding of platform team antipatterns and mitigation.

**Key principles:**
1. **Self-service first** — If product teams need to ask the platform team for every change, the platform team is a bottleneck. Invest in self-service tooling (service scaffolds, deployment templates, monitoring dashboards)
2. **SLAs with teeth** — Platform team publishes SLAs for their services. If they can't meet them, product teams have an escalation path
3. **Don't build it if you can buy it** — The platform team shouldn't build what's available as a managed service unless the differentiation is strategic
4. **Metrics** — Product team satisfaction, time-to-first-deploy for a new service, platform uptime, incidents caused by platform changes
5. **Listening tours** — Every quarter, the platform team spends a week embedded with product teams. Fix the top 3 pain points found

---

### Q: Two teams disagree on API design standards. How do you resolve it without authority?

**What they're testing:** Influence without authority, conflict resolution, technical judgment.

**Framework:**
1. **Understand both positions** — Before the meeting, talk to each team lead individually. What's their actual concern? Often the stated position (sync vs. async) hides a deeper concern (operational burden, learning curve)
2. **Bring the right context** — Present data: what's the current pattern across the org? What do other teams do? What's the migration cost of each option?
3. **Focus on principles, not preferences** — "I don't care whether you use Kafka or RabbitMQ. I care about: (a) events are documented in our schema registry, (b) your consumers can handle retries, (c) your producer owns the schema contract. Pick whatever fits your team."
4. **Explicitly tier decisions** — Some things are non-negotiable (security, observability standards). Some are team preference (framework, language). Make the distinction clear
5. **Document the outcome** — Even if you don't get full agreement, write down the decision, the rationale, and the review date. This prevents the same debate from recurring

---

## Category 3: Business & Executive Alignment

### Q: Explain distributed tracing to a non-technical VP.

**Framework:** Start with business impact, then the mechanism.

> "Every customer request — say, loading their bill or activating a device — touches 5-6 different services on the backend. When something fails, we used to spend 30+ minutes manually hopping between logs to find where it broke. Distributed tracing attaches a unique ID to every customer request as it enters the system. That ID follows the request through every service. When something fails, we can pinpoint the exact service and the exact API call within 30 seconds — not 30 minutes.
>
> The business impact: lower mean time to resolution for customer-facing incidents, fewer escalations, and we can proactively detect which services are degrading before customers complain. The investment is moderate — a tracing agent per service and a dashboard. The return is every P1 incident resolved 20x faster."

---

### Q: How do you connect engineering investment to business outcomes?

**Framework for any engineering story:**

Start with the business goal, then show how the work connects.

> "The Spring Boot 2 to 3 migration cost 5 months of engineering time. The business case was: (1) security — Spring Boot 2 was EOL, meaning every missed CVE was a regulatory risk for a telecom company. (2) velocity — new features were blocked because dependencies couldn't upgrade past Boot 2. (3) cost — faster startup times and better GC reduced cloud spend.
>
> The outcome: 60% reduction in migration time across 12 services, unblocked quarterly feature releases that had been stalled for 6 months, and elimination of a growing pile of security tickets. I measured it as: time-to-security-patch went from weeks to hours, and engineering velocity on the platform increased enough that the investment paid for itself within 2 quarters."

**Key numbers from your resume to frame in business terms:**

| Metric | Business Framing |
|---|---|
| Spring Boot 3: 60% productivity | "Unblocked 6 months of stalled releases. Security patches same-day instead of weeks." |
| Sling TV: 5 mo vs 18 mo | "Compressed a 3-quarter rewrite into 2, without stopping feature delivery on the existing system." |
| Vulnerability fixes: hours vs days | "Reduced security risk exposure from a week to same-day. Audit-ready in hours." |
| Incident diagnosis: 30 min → 2 min | "P1 resolution time dropped 15x. Fewer escalation minutes, less customer impact." |

---

### Q: What's the single highest-impact application of AI in engineering for a company like Dish?

**Have a point of view. Pick 1-2.**

> "For a company with 14M+ subscribers running on a mix of modern and legacy systems, I believe the highest-impact application isn't code generation — it's **migration automation and incident response compression**. Code generation saves individual developer time. Migration automation unlocks platform-level velocity — it lets you modernize legacy systems that are blocking the entire business. Incident response compression protects revenue and brand. Both scale across the org without requiring every engineer to be an AI expert.
>
> The next wave that I'm watching is: can agents build agents? If I can create a meta-skill that lets teams create their own domain-specific agent skills without deep prompt engineering, then the AI practice itself becomes self-scaling. That's where I'm investing now."

---

## Category 4: Behavioral — The Ones You'll Get

### Q: Tell me about a time you influenced a decision without authority.

**Your story:** The org-wide Spring Boot 3 migration or the AI practice adoption.

**Structure:**
- **Context:** Different teams owned different services. You had no authority over their engineering decisions.
- **Challenge:** Teams were skeptical of AI-generated code. Security team was skeptical of automated remediation.
- **Action:** You built the reference implementation yourself. You showed working code. You presented the data (time saved, defect rate). You paired with early adopters to build their confidence. You escalated only after you had a proven pattern.
- **Outcome:** 5+ teams adopted. Leadership saw the data and made the practice official.

---

### Q: Tell me about a time an initiative didn't catch on.

**This tests intellectual honesty. Everyone has one.**

> "Early in my AI practice work, I tried to get teams to use my initial agent skill — it was too rigid. It had a fixed 5-phase workflow that didn't account for different team workflows. Teams tried it once, hit friction, and didn't come back. I learned: the first version is never right. I redesigned it as a configurable playbook — teams could customize phases, add approval gates, skip steps. Second version was adopted. The lesson: platform thinking means your users have needs you can't predict. Build for customization, not correctness."

---

### Q: How do you hire for Principal/Staff engineers?

**You're on the hiring panel at Dish. They'll ask.**

- **Signal 1:** Can they articulate a framework, not just a solution? "We used Redis" vs. "We chose Redis over GemFire because our access pattern was simple key-value and we didn't need WAN replication. The criteria were: ops overhead, latency, and team familiarity."
- **Signal 2:** Do they talk about org context? A Senior talks about their code. A Staff talks about their team's architecture. A Principal talks about cross-team patterns and business alignment.
- **Signal 3:** Can they disagree constructively? Offer a counter-point to their design. Do they get defensive or engage with curiosity?
- **Signal 4:** Do they have a point of view on industry trends? Not "I read about this," but "I've formed an opinion based on experience."

---

### Q: What's a technology decision you made that you later reversed?

**Tests intellectual honesty and adaptability.**

> "Early in the My Dish platform, I chose RabbitMQ over Kafka for event-driven communication. RabbitMQ was simpler, the team knew it, and our initial event volume was low. As we scaled — more services, more event types, replay requirements, and the need for a audit trail — RabbitMQ's limitations became clear. We migrated to Kafka. The switch cost us a quarter of engineering time. The lesson: optimize for the problem you're solving today, but have an evolution path. If I had started with Kafka despite the higher initial complexity, we'd have saved the migration cost. But I'd also have slowed initial delivery. I'd make the same choice again — pick the simpler option, but start the Kafka conversation earlier when the signals (growing event volume, replay requests) appear."

---

### Q: How do you mentor someone who doesn't think they need mentoring?

> "I don't frame it as mentoring. I frame it as a problem I want their opinion on. 'I'm thinking about how to structure the API gateway rate limiting — can I run my design by you? You've worked on performance-critical paths.' This turns the conversation into a peer discussion. Once they engage, I can ask follow-ups that naturally stretch their thinking.
>
> The key is: you can't tell someone they need mentoring. You create situations where they experience the growth themselves. Pairing them on a cross-team initiative, having them present an architecture decision to a wider audience, or asking them to review a junior's design — the experience of doing the work at a higher level is the mentor."

---

## Summary: What's Missing from Your Current Prep

| Category | Covered? | Action |
|---|---|---|
| Architecture & system design | Yes — `interview_prep.md` | Review |
| Migration stories (Spring Boot 3, Sling TV) | Yes — strong coverage | Add business framing to each |
| AI/agent technical detail | Yes — strong coverage | Add scaling narrative |
| Multi-year technology strategy | **Missing** | Prepare 2-3 roadmap narratives |
| Org design & team topology | **Missing** | Prepare team topology answer |
| Business alignment & executive framing | **Missing** | Practice translating metrics to business outcomes |
| Scaling an initiative org-wide | **Missing** | Prepare scaling story for AI practice |
| Influence without authority | **Missing directly** | Prepare Sling TV / Spring Boot 3 influence story |
| Failed initiatives / reversals | **Missing** | Prepare one honest failure + lesson |
| Hiring & evaluation | **Missing directly** | Know your signal framework |
| Mentoring resistant engineers | **Missing directly** | Prepare one story |

---

## Final Tips

1. **Don't memorize scripts** — Know the frameworks. Speak naturally, reference your resume events.
2. **Every answer follows:** Context → Framework → Action → Outcome → Lesson.
3. **Have 2-3 anchor stories** you can adapt to any question. Your best candidates:
   - Spring Boot 3 migration (strategy, execution, measurement, influence)
   - Sling TV transformation (org design, migration strategy, business alignment)
   - AI agent skills (innovation, scaling, governance, org adoption)
4. **Principal is about leverage.** Everything you say should signal: "I make the engineers around me better. I remove org-level bottlenecks. I set technical direction that lasts for years."
5. **Have a point of view.** On AI in engineering, on team topology, on platform vs. product. Indecision at the Principal level is a red flag.
