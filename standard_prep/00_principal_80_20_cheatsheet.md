# Principal-Specific Questions — 80/20 Cheatsheet

> Not covered in existing prep. Highest-likelihood for The Standard interview.

---

## 1. What would your first 90 days look like?

**Framework:** Listen → Diagnose → One Win → Plan

| Phase | What | Output |
|-------|------|--------|
| **W1-2** | 1:1s with every lead/architect/PM. Read ADRs, post-mortems, architecture docs. Understand what's hurting. | Org map + pain list |
| **W3-6** | Pick one cross-cutting problem that's blocking velocity (slow CI? no API standards? unowned service?). Fix it end-to-end. Show how you operate. | Tangible artifact (template, ADR, pipeline change) |
| **W7-12** | Synthesize findings into a technical roadmap. Socialize with teams + leadership. Get buy-in for Q3-Q4 priorities. | 6-month roadmap, approved |

**Key line:** *"I don't start by proposing a grand architecture. I start by understanding what's actually breaking for teams — then fix the highest-leverage thing first. That builds trust to make bigger moves later."*

---

## 2. Why The Standard? Why insurance?

**They're testing:** Is this a real interest or just another job? Do you understand the domain constraints?

| Angle | What to Say |
|-------|------------|
| **Platform complexity** | Insurance has real technical depth — policy management, claims processing, regulatory compliance, millions of concurrent users during open enrollment. That's the kind of distributed systems challenge I want. |
| **Modernization opportunity** | The industry is ripe for the same kind of migration I did at Dish — legacy systems → modern event-driven architecture. The JD describes exactly that challenge. |
| **Stability + innovation** | Insurance isn't a 6-month burn-and-churn startup. The products have multi-decade lifetimes. That means architecture decisions matter — the right design today pays off for 10 years. That's where I add value. |

**One thing NOT to say:** *"I want to try something different"* — implies surface-level interest.

---

## 3. Build vs Buy — for THIS role

**Don't give a generic framework. Contextualize to their stack.**

| Decision | Recommendation | Why |
|----------|---------------|-----|
| **Confluent vs open-source Kafka** | Buy Confluent | Schema Registry, Connect, Flink integration reduce ops burden. At enterprise scale, the premium pays for itself in engineer hours saved. Worth it unless compliance requires air-gapped. |
| **Kong Konnect vs self-hosted** | Start with self-hosted, evaluate Konnect at scale | Self-hosted on AKS gives you control while ramping up. Move to Konnect when >5 teams depend on it — the operational savings justify the SaaS cost. |
| **Azure-native vs multi-cloud** | Azure-native, with escape hatches | The Standard runs Azure. Don't fight it. But use OpenTelemetry + Terraform so you're not locked in — standard interfaces give optionality without the complexity of running two clouds. |

**Key line:** *"I bias toward buying solved problems so my team builds what differentiates us. An API gateway isn't our competitive advantage. Our claims processing logic is."*

---

## 4. Disagreeing with your architect/VP on strategy

**They're testing:** Can you disagree without being political? Can you accept a decision and execute?

**Framework:**

1. **Understand their constraints** — Ask: "What outcome are you optimizing for?" Usually there's a pressure you don't see (board deadline, budget cycle, regulatory mandate).
2. **State your concern as risk, not opposition** — "I'm worried about X. Here's what could go wrong and how we'd detect it early."
3. **Propose a middle path** — "Can we do it your way for the first phase, with a checkpoint at 6 weeks to reassess?"
4. **If overruled, commit** — "I disagree but I'll execute. I'll flag early if my concern materializes."

**Your story (from Dish — file 08 has the vendor evaluation story):** Leadership wanted a low-code integration platform. Rather than oppose, you ran a structured POC, documented limitations, proposed the alternative (Spring Boot templates + OpenAPI code gen), and delivered 40% velocity improvement. That's the exact answer.

---

## 5. Stakeholder pushing unrealistic timelines

**They're testing:** Can you negotiate scope without breaking trust?

**Framework:**

| Step | What You Say |
|------|-------------|
| **Validate the need** | "I hear you — this is important. Let me understand the deadline driver." |
| **Don't say "no" immediately** | "Here's what we CAN deliver in that timeline with the team we have." |
| **Offer options** | **Option A:** Full scope, 8 weeks. **Option B:** Core functionality by the deadline, rest later. **Option C:** Full scope by deadline if we descope X and Y. |
| **Make the trade-off explicit** | "If we push for the deadline, we'll carry technical debt in Z area. I'm fine with that if we plan to fix it in the next quarter." |

**Key line:** *"I never say 'it can't be done.' I lay out what's possible with the constraints and let the business decide which trade-off they're comfortable with."*

---

## 6. Regulated industry awareness (insurance-specific)

**The Standard is insurance. Compliance is not optional.**

| Topic | What to Say |
|-------|------------|
| **Data residency** | "Customer data stays in-region. Azure regions give us that. Private Link + Private Endpoints ensure data doesn't traverse the public internet." |
| **Audit trails** | "Kafka gives us a natural append-only log. Every event is an audit record. Retention policies per topic (90 days for financial events, 30 for operational)." |
| **Encryption** | "At rest (Azure Storage Service Encryption), in transit (TLS 1.3). Key rotation via Key Vault. Secrets never in config files." |
| **Change management** | "Architecture reviews before implementation. PR templates with compliance checklists. SOPs for production changes." |
| **Your experience** | "At Dish, we handled PII for millions of subscribers. Same principles — encrypted at rest, strict access control, audit logging. The specifics differ by regulation but the patterns are the same." |

---

## Quick Reference: What to loop back to Sling TV

| This Question | Anchor It To |
|--------------|-------------|
| First 90 days | "When I joined the Sling migration mid-stream, my first 90 days were..." |
| Architecture decision | "When we chose 12 partitions for subscription topics, the trade-off was..." |
| Failure / incident | "The payment gateway timeout incident — lag spiked to 500K, we diagnosed in 20 minutes..." |
| Monitoring | "Three levels: consumer lag, broker health, application metrics. Prometheus + Grafana + Dynatrace." |
| Mentoring | "I set up Kafka office hours — 2 hours a week, any team could ask questions. Within 2 months, 3 teams were running their own consumers." |
