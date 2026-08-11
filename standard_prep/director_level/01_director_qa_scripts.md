# Director Q&A Scripts — The Standard (Principal V)

> Full answer scripts for the highest-likelihood director questions. Each follows the 4-step answer standard from `../../talks/30. Standard Insurance Interview Feedback - Defense and Scripting Guide.md`: **BLUF → Signpost (Rule of 3) → Stack mechanics → Metric impact**.
>
> Directors test **judgment, org sense, and business translation** — not recall. Adapt the scripts to the conversation; never recite.

---

## 1. "What would your first 90 days look like in this role?"

**Framework:** Listen → Diagnose → One Win → Plan

| Phase | What | Output |
|---|---|---|
| W1-2 | 1:1s with every lead/architect/PM. Read ADRs, post-mortems, architecture docs. Understand what's hurting. | Org map + pain list |
| W3-6 | Pick one cross-cutting problem blocking velocity (slow CI? no API standards? unowned service?). Fix it end-to-end. | Tangible artifact (template, ADR, pipeline change) |
| W7-12 | Synthesize into a technical roadmap. Socialize with teams + leadership. Get buy-in for Q3-Q4 priorities. | 6-month roadmap, approved |

**Script (BLUF):** "I don't start by proposing a grand architecture. I start by understanding what's actually breaking for teams — then fix the highest-leverage thing first. That builds trust to make bigger moves later."

**Anchor:** "When I joined the Sling migration mid-stream, my first 90 days were exactly that: map the pain, fix one bottleneck end-to-end, then earn the right to set direction."

**Watchpoints:** They may push "but we need architecture direction now" — answer: "You get a diagnosis in 2 weeks, not 90 days. The roadmap comes from evidence, not assumptions."

---

## 2. "How do you influence teams that don't report to you? / How will you work in the India-US model?"

**Framework:** Data not arguments → make it self-service → let them decide

**Script (BLUF):** "I don't mandate; I make it easy to say yes. Show data, not arguments, and let the teams decide — adoption follows trust."

**The story (Spring Boot 3 + Kiro adoption):**
1. Built the reference implementation on one service — didn't ask permission, showed a working result
2. Presented benchmark data: 2 weeks → 3 days per service, 85% test coverage, zero incidents (2-week POC → 40% velocity in the low-code story)
3. Published ADRs + reusable playbook + GitLab CI/CD quality gates so teams self-serve
4. Result: 5+ teams in a quarter, invited to demo live spec-driven SDLC to VP+

**Key line:** *"The adoption number is the lagging indicator. The leading indicator was making it customizable — teams choose their phases, approval gates, and notification preferences. Platform thinking means designing for what you can't predict."*

**India-US angle:** "The CIO's model is shared accountability — the tools and ways of working are identical across India and US. My role is to make the patterns consistent so a service built in Bengaluru is indistinguishable in quality from one built in Portland."

**Watchpoints:** If asked about pushback specifically → use the "resistant team" story (diagnose the 4 causes, do the first one yourself). Never say "I told them it was a good idea."

---

## 3. "Why are you the founding architecture hire for this center?"

**Framework:** Founding-scope hunger → proven pattern → 10-year horizon

**Script (BLUF):** "I want to be the person who defines the patterns, not the one who inherits them. Same pattern, new domain, bigger scope."

1. **Scope:** At Dish I own architecture for a 10M-subscriber platform — and I've hit the ceiling of a single-product company. This role spans insurance, retirement, investments — portfolio breadth, not single-platform depth.
2. **Pattern:** I've already built the playbook this role needs — API-led integration, event-driven backbone, AI-augmented SDLC with governance. It's proven at 10M scale; it transfers to insurance.
3. **Horizon:** Insurance systems live 30+ years. The architecture decisions I make today will outlast me at the company — that's the responsibility I want, not a two-year project.

**Watchpoints:** "Why leave Dish?" → growth frame, never dissatisfaction. "I've delivered two consecutive Technical Excellence Awards and a promotion — but the decisions I make affect one platform. I want portfolio breadth."

---

## 4. "Where should BenTech Integrations be in 3 years?"

**Framework:** Phased with checkpoints — Year 1 quick wins, Year 2 platform, Year 3 differentiation

**Script:**
- **Year 1 — Integration standards + quality gates:** API-first contracts in a versioned repository, OpenAPI mandates, shared auth/observability library, Snyk/Dynatrace gates in CI. Outcome: no more "integration by Slack message."
- **Year 2 — Event-driven backbone:** Kafka/Confluent with Schema Registry for claims, policy, underwriting event streams; Saga for cross-domain consistency; DLQ + replay for regulatory audit.
- **Year 3 — AI-native SDLC + differentiation:** agents as first-class participants — defect-fix, test-gen, vuln-remediation skills with scoped permissions and human gates. The Standard's CIO said "solve the hardest problems of AI first" — underwriting and claims, not chatbots.

**Key line:** *"Each phase has a checkpoint: if the metric doesn't improve, we stop and reassess."*

**Flink honesty (if probed):** "I haven't run Flink in production — my stream-processing foundation is Kafka Streams, and the concepts translate. I'd come up to speed on Flink UDFs and statements in the first weeks; I won't pretend mastery." (Disarm first — credibility play, per the one-pager.)

---

## 5. "Build vs Buy?" (contextualized to their stack)

**Framework:** Buy solved problems; build what differentiates you

| Decision | Recommendation | Why |
|---|---|---|
| Confluent vs open-source Kafka | Buy Confluent | Schema Registry, Connect, Flink integration reduce ops burden; premium pays for itself at enterprise scale |
| Kong Konnect vs self-hosted | Start self-hosted, evaluate Konnect at scale | Control while ramping; move when >5 teams depend on it |
| Azure-native vs multi-cloud | Azure-native, with escape hatches | OpenTelemetry + Terraform give optionality without dual-cloud complexity |

**Key line:** *"I bias toward buying solved problems so my team builds what differentiates us. An API gateway isn't our competitive advantage. Our claims processing logic is."*

---

## 6. Regulated industry awareness (insurance)

They WILL test compliance fluency. Evidence-first, no hand-waving:

| Topic | Anchor |
|---|---|
| Data residency | "Customer data stays in-region. Private Link + Private Endpoints ensure data never traverses the public internet." |
| Audit trails | "Kafka is a natural append-only log — every event is an audit record. Retention per topic: 90 days financial, 30 operational." |
| Encryption | "At rest (Azure SSE), in transit (TLS 1.3). Key rotation via Key Vault. Secrets never in config files." |
| Change management | "Architecture reviews before implementation, PR templates with compliance checklists, SOPs for production changes." |
| Your experience | "At Dish we handled PII for millions of subscribers — same principles: encrypted at rest, strict access control, audit logging. The regulations differ; the patterns don't." |

---

## 7. "Tell me about a time you disagreed with leadership on strategy"

**Framework (from `../00_principal_80_20_cheatsheet.md`):**
1. Understand their constraints — "What outcome are you optimizing for?"
2. State concern as risk, not opposition — "I'm worried about X; here's how we'd detect it early"
3. Propose a middle path — "Your way for phase 1, checkpoint at 6 weeks"
4. If overruled, commit — "I disagree but I'll execute, and I'll flag early if my concern materializes"

**Your story:** Leadership wanted a low-code integration platform. You ran a structured POC, documented limitations, proposed Spring Boot templates + OpenAPI codegen, delivered **40% velocity improvement**. The POC beat the argument.

**Key line:** *"The manager wasn't wrong — they just hadn't seen it work. My job was to de-risk the decision, not win the argument."*

---

## 8. "Stakeholder pushing unrealistic timelines"

**Framework:** Validate the need → never say "no" → offer options → make the trade-off explicit

**Script:**
1. "I hear you — this is important. Let me understand the deadline driver."
2. "Here's what we CAN deliver in that timeline with the team we have."
3. Option A: full scope, realistic timeline. Option B: core by the deadline, rest later. Option C: full scope by the deadline if we descope X and Y.
4. "If we push for the deadline, we'll carry technical debt in Z area. I'm fine with that if we plan to fix it next quarter."

**Key line:** *"I never say 'it can't be done.' I lay out what's possible with the constraints and let the business decide which trade-off they're comfortable with."*

---

## 9. "What does Principal mean to you?" (the leveling question, if it surfaces)

**Script (BLUF):** "Staff asks: did I build the right system? Principal asks: did I make the right investment for the organization, and did I enable others to build?"

1. **Right investment:** choices measured in business outcomes — unblocked releases, protected revenue, reduced risk — not lines of code.
2. **Enable others:** patterns, playbooks, guardrails, mentoring — my output scales through other engineers' hands.
3. **Own the ambiguity:** the org doesn't know the answer yet; that's my job — decide, communicate, and stand behind the trade-off.

**Never:** argue the leveling or reference the US round's feedback. Demonstrate, don't defend.

---

## Quick Reference: What to Loop Back to Sling TV

| This Question | Anchor To |
|---|---|
| First 90 days | "When I joined the Sling migration mid-stream..." |
| Architecture decision | "When we chose 12 partitions for subscriber topics, the trade-off was..." |
| Failure / incident | "The payment gateway timeout incident — lag spiked to 500K, diagnosed in 20 minutes..." |
| Monitoring | "Three levels: consumer lag, broker health, application metrics. Prometheus + Grafana + Dynatrace." |
| Mentoring | "I set up Kafka office hours — 2 hours a week. Within 2 months, 3 teams ran their own consumers." |

---

# Part 2 — Role-Specific & Curveball Questions (from research + JD reading)

> Sections 10-20 are the questions a director asks when probing THIS role's specifics — BenTech integration, the India-US model, and the staff-vs-principal leveling. The 9 above cover the general director set.

## 10. "How would you design the BenTech integration layer?" (the flagship design question)

**Framework:** Clarify scope → Contracts → Gateway → Events → Identity → Resilience → Governance

**Script (BLUF):** "I'd design it as a contract-first integration platform with three layers: an API gateway for partner traffic, an event backbone for asynchronous flows, and a governance layer that makes change safe. One partner's outage must never take down enrollment."

1. **Contracts first:** OpenAPI + Schema Registry as the single source of truth. Versioned, backward-compatible by policy.
2. **Gateway:** Kong for per-partner auth (OAuth2/mTLS), rate limiting, transformation — declarative, DB-less config.
3. **Events:** Confluent topics per domain (enrollment, eligibility, claims) with DLQ + replay for audit.
4. **Identity:** OAuth2 client credentials per partner; SCIM for entitlement sync.
5. **Resilience:** Circuit breakers + bulkheads per partner.
6. **Governance:** Consumer-driven contracts, sandbox tiers, sunset policy for breaking changes.

**Anchor:** "This is the pattern I ran on My Dish — 12 services, REST + Kafka hybrid, gateway + BFF — and DPA taught me the config-not-code lesson across 23 integrations."

## 11. "How do you handle integration governance with external partners?"

**BLUF:** "External partners can't be forced to upgrade — so governance is by contract, not by decree."

- Semver + **sunset policy**: breaking changes get notice + dual-run period
- **Consumer-driven contracts** (Pact-style): partners register expectations
- Compatibility by default: BACKWARD/FULL in Schema Registry
- **Sandbox tiers + certification** before prod access
- Metric: contract-drift rate, partner onboarding time

**Key line:** *"Each integration becomes a config entry, not a code path — that's how 23 integrations stayed manageable."* (DPA)

## 12. "How would you approach EDI-to-API/events modernization?" (834/820 legacy)

**BLUF:** "I'd bridge, not boil the ocean — run EDI and APIs in parallel, translate at the edge, migrate partner by partner."

1. Canonical data model first
2. EDI → canonical → API translation layer
3. Partner-by-partner migration: parallel run + **hourly reconciliation job** (old vs new outputs — the Sling pattern)
4. Sunset EDI per partner when parity is proven

**Anchor:** DPA (ColdFusion → Spring Boot, 23 integrations, 7 SFTP targets, zero downtime).

## 13. "How do you work with US teams across time zones?" (PST overlap — JD preferred experience)

**BLUF:** "Async-first with structured overlap — decisions in writing, meetings only for what needs them."

- **ADRs + recorded design reviews** — the CIO's model: same tools, same ways of working
- 2-3 hours of PST overlap for sync windows; everything else async
- **Guilds + office hours** cadence (Kafka office hours: 3 teams running consumers in 2 months)
- My agent skills execute while the US sleeps: Jira/GitLab MCP runs defect-fix, test-gen, PR prep async

**Key line:** *"Shared accountability means the decision record is the product — not the meeting."*

## 14. "What's the biggest risk in our BenTech strategy?" (identify-the-risk test)

**BLUF:** "Three risks, in order: contract drift across a growing partner ecosystem, legacy EDI debt, and identity federation on sensitive benefits data."

1. **Contract drift** (N partners × N formats) → Schema Registry + consumer-driven contracts
2. **EDI debt** → bridge pattern, not rewrite (canonical model + translation layer)
3. **Identity/data** (benefits data is HIPAA-adjacent) → federated identity, least privilege, immutable audit trail

**Key line:** *"The risk isn't the technology — it's the ecosystem growing faster than the contracts. That's why governance is the first deliverable, not the last."*

## 15. "What would your first architecture decision be here?"

**BLUF:** "Audit the integration surface, then standardize contracts and gateway governance as the first visible deliverable."

- W1-2: inventory partners, formats, SLAs, failure history
- W3-6: contract repository + OpenAPI mandate + gateway governance + **one pilot partner end-to-end**

**Key line:** *"A small, visible win builds the credibility for the bigger moves."*

## 16. "How is this role different from what you do today?" (the leveling probe in disguise)

**BLUF:** "Same discipline, bigger scope — today I define patterns for one platform; here I define them for an ecosystem."

- Dish: single-product company, one platform, internal teams
- Here: external ecosystem (HCMs, brokers, intermediaries), portfolio breadth, **founding patterns for a new center**

**Key line:** *"Same pattern, new domain, bigger scope."* (the one-pager close — say it slowly)

## 17. "How do you grow engineers / how would you build the team here?"

**BLUF:** "Progressive ownership with guided questions — I grow people by giving them the hard problem slightly ahead of their comfort."

- Story: 8 months mid→senior, he now mentors others; STB Health ownership transfer
- Guilds + office hours as the growth mechanism
- Hiring: senior/staff panels; bar = ownership + judgment, not years

## 18. "Tell me about a failure / the hardest decision you've made"

- **Failure:** the agent patched the test instead of the bug → I built the verification layer: tests must pass against old AND new code, human review of AI assertions, max 3 iterations before escalation. *"I trusted automation without a verification layer — now it's standard."*
- **Hardest decision:** sequencing Sling by business risk — billing first, knowing the pressure was on the first cutover.

## 19. "Where do you see yourself in 3-5 years?"

**BLUF:** "Building this center's integration architecture into the industry reference — and growing the engineers who maintain it."

- The CoE the CIO chartered; the 3-year vision (Year 1 standards, Year 2 event backbone, Year 3 AI-native)
- *"Insurance systems live 30+ years — the architecture I define here will outlast me. That's the responsibility I'm signing up for."*
- NOT a promotion-path answer — signal terminal-level commitment to the IC track.

## 20. "If we hire you and 6 months in, teams aren't adopting your patterns — what went wrong?"

**BLUF:** "Adoption is design, not mandate — if patterns don't stick, I failed the design, and I'd fix the friction first."

- The agent-skills lesson: first version failed because it was rigid → redesign for configurability → adoption took off
- Diagnose: too complex / not solving a real pain / no quick wins / no sponsor → then do the first fix yourself

**Key line:** *"The difference between a tool that stays on one team and a practice that scales is how easy you make it for others to say yes."*

## 21. "Tell me about a time you disagreed with product management and how you resolved it"

**Story:** the low-code platform dispute (80/20 cheatsheet #4 — POC beat the argument).

**Script:**
> "The best example was when product leadership wanted to adopt a **low-code integration platform** to speed up our delivery. They had a real problem — integration work was slow, and they were measured on feature velocity. My concern: a low-code platform handles the happy path beautifully, but it creates long-term integration debt — custom code escapes the platform, testing gets harder, and you get vendor lock-in on the one layer you can least afford it.
>
> So here's what I did. **First, I validated the need before challenging the solution** — I agreed the problem was real: integrations took too long. **Second**, instead of arguing, I ran a **structured two-week POC on one of their actual use cases** — not a cherry-picked demo, their real problem. **Third**, I documented the limitations **empirically** — what the platform handled well, where it broke down: complex transformations, error handling, testability. **Fourth**, I proposed the alternative — Spring Boot service templates with OpenAPI code generation — which delivered the same speed they were chasing. **Fifth**, I presented both options with the data and let the business decide.
>
> **The outcome:** we went with the alternative, and it delivered a **40% velocity improvement** — product got exactly what they wanted, speed — on a foundation that scaled. And the bigger win was trust: after that, product started bringing decisions to me earlier, because they knew I'd respect their goals and come with data, not opinions.
>
> **The lesson:** the product manager wasn't wrong — they just hadn't seen the alternative work. My job was to **de-risk the decision, not win the argument**. When you win, you win on data — so nobody loses face, and the decision sticks."

**What the director listens for:**
1. Understood the PM's constraints first ("measured on feature velocity")
2. Escalated to evidence, not opinion (POC on *their* use case)
3. The other side got their goal (speed) — not a win at their expense
4. The relationship after ("they bring decisions to me earlier") — durable trust

**Timeline variant** (if the dispute was scope/deadline — 80/20 cheatsheet #5):
> "I never say 'it can't be done.' I validate the deadline driver, then lay out what's possible: Option A — full scope on a realistic timeline. Option B — core by the deadline, rest later. Option C — full scope by the deadline if we descope X and Y. I make the trade-off explicit — 'if we push for the deadline, we carry debt in Z area, and I'm fine with that if we fix it next quarter' — and let the business choose."

**Pitfalls:** never "I won the argument" (data decided); never dismiss their constraint; make the dispute the exception, not the norm; always land the relationship-after.

---

## 22. "How do you handle disputes?" — 3 scripts from your projects

> Same spine for every variant: **validate the need → evidence not opinion → explicit trade-off → relationship after.**

### Variant A — Dispute with leadership/PM (low-code platform, 40% velocity)
*Use when: "tell me about a disagreement with leadership / product management."*

> "Product leadership wanted to adopt a low-code integration platform. They had a real problem — integrations were slow, and they were measured on feature velocity. My concern: low-code handles the happy path beautifully, but it creates long-term integration debt — custom code escapes the platform, testing gets harder, and you get vendor lock-in on the one layer you can least afford it.
>
> So first, I validated the need before challenging the solution — I agreed the problem was real. Second, instead of arguing, I ran a two-week POC on one of their actual use cases — not a cherry-picked demo, their real problem. Third, I documented the limitations empirically — what it handled well, where it broke: complex transformations, error handling, testability. Fourth, I proposed the alternative — Spring Boot templates with OpenAPI code generation — and presented both options with data, and let the business decide.
>
> We went with the alternative, and it delivered a **40% velocity improvement** — product got exactly what they wanted, speed, on a foundation that scaled. The bigger win was trust: after that, product started bringing decisions to me earlier, because they knew I'd respect their goals and come with data, not opinions.
>
> The lesson: the PM wasn't wrong — they just hadn't seen the alternative work. My job was to **de-risk the decision, not win the argument**. When you win on data, nobody loses face, and the decision sticks."

### Variant B — Dispute with Security/Compliance (AI agent skills, "what stops the agent?")
*Use when: "a stakeholder blocked you / how do you handle a dispute with a control function."* Shows you pre-empted the dispute — solved it before it started.

> "When I started wiring AI agents to our internal tools — Jira, GitLab, Dynatrace, Snyk — security came back with exactly the question you'd expect: *'what stops an agent from deleting production data?'* It was a fair dispute, and I could have treated it as a blocker. I treated it as a design requirement.
>
> I had already defined the security boundary before anyone asked: every MCP server gets scoped permissions — GitLab can read code and create PRs but **never merge**; Dynatrace can read traces but **never modify** monitoring; Snyk can read vulnerabilities but **never dismiss** findings. On top of that, playbook gates stop the agent before any destructive operation and escalate to a human, and every AI-generated PR needs human approval.
>
> So when security asked, I didn't argue the philosophy — I walked them through the three enforcement layers, and I invited them into the design. They became a reviewer of the model, not an opponent of the project.
>
> The outcome: the agents run autonomously today across 5+ teams — same-day vulnerability fixes instead of 2–7 days — and security is the one who champions it. The lesson: a dispute with a control function is usually a sign you haven't made your safety model visible yet. Answer the question they'd ask before they ask it, and the blocker becomes a sponsor."

### Variant C — Technical dispute with a peer (Saga vs ACID during Sling)
*Use when: "a disagreement with another engineer / an architecture dispute."*

> "During the Sling monolith split, we hit a real architecture dispute: my team wanted to split the monolith database into per-service databases for isolation, and a peer architect pushed back hard — 'you're throwing away ACID transactions, this is going to corrupt data.' He wasn't wrong; losing ACID is a genuine risk.
>
> I didn't argue the theory. I acknowledged the risk was real, then proposed the middle path: the Saga pattern on Kafka with compensation logic — each service publishes an event when its local transaction completes, downstream services update their own state, and compensation rolls back on failure. And the decisive move: we didn't just write it up, we **chaos-tested it before go-live** — injected failures in staging to prove the rollback path.
>
> The data from the chaos tests settled it, and we moved on together — he ended up reviewing the Saga implementation, because it had his fingerprints on the failure design. The lesson: in a technical dispute, seniority shouldn't decide — **evidence decides**, and the fastest way to evidence is to break it on purpose in a safe place."

### Pick-the-variant cheat sheet

| Director says | Script |
|---|---|
| "Disagreed with leadership/PM" | A — low-code, 40% velocity |
| "Someone blocked your initiative / control function" | B — security boundary, blocker→sponsor |
| "Architecture disagreement with a peer" | C — Saga vs ACID, chaos test settles it |

**Backup leadership-dispute story (if pushed for a second example):** Spring Boot 3 migration — leadership estimated 18 months of manual migration; instead of a proposal, I built the first service myself with AI (3 days vs 2 weeks, 85% coverage, zero incidents), showed the data at the guild, and leadership scaled it org-wide. Delivered in 5 months. Same spine: POC on a real case, evidence beat opinion, no one lost face.

**Common closer for any variant:** *"The pattern is the same every time — understand their constraint, make the trade-off visible, let evidence decide. If I'm overruled anyway, I commit and flag early if my concern materializes."*
