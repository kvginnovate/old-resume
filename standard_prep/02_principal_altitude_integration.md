# Principal Altitude Integration Guide

> **How to reframe every existing answer from Staff to Principal level.** Your existing `interview_prep.md`, `interview_workbook.md`, and `principal_interview_prep.md` already have strong Staff-level answers. This document shows the Principal altitude shift for each category.
>
> **The difference:** Staff answers focus on *what* you did and *how* you did it. Principal answers focus on *why* you chose that approach, *how* you influenced the org, *what* business outcomes it drove, and *what* you'd do differently with the same problem today.

---

## The Principal Lens — One Paragraph

> **Staff → Principal shift in one sentence:**
>
> _Staff asks: "Did I build the right system?" Principal asks: "Did I make the right investment for the organization and did I enable others to build?"_

---

## Category-by-Category Reframe

### 1. Architecture Stories (Subscriber Platform, Sling TV, STB Health)

| Your current answer focuses on... | Principal altitude reframe |
|---|---|
| "I architected the platform" | "I identified that the org had no shared integration patterns, which was the bottleneck to velocity. I defined the patterns, made them self-service through a shared library and documented playbooks, and drove adoption across teams — not by mandate, but by showing measurable time savings." |
| "I built the system with X tech stack" | "I chose this tech stack knowing the tradeoff: Kafka for event durability at the cost of operational complexity, GemFire for cache speed at the cost of learning curve. The decision was informed by our incident history — we needed replay capability and audit trails." |
| "I led the migration" | "I sequenced the migration by business risk, not technical convenience. Sling TV's billing domain first — highest risk, highest isolation — then content catalog. The sequencing decision determined whether we could maintain business continuity, not just technical quality." |

### 2. AI & Automation Stories (Spring Boot 3, Agent Skills, MCP)

| Your current answer focuses on... | Principal altitude reframe |
|---|---|
| "I used AI to accelerate migration" | "I saw that we were bottlenecked on manual labor for a problem that was fundamentally mechanical — text replacement, config conversion, test regeneration. The AI decision was 20% technical tooling and 80% organizational: building the dashboard to prove the approach, writing the playbook so others could self-serve, and letting data drive adoption." |
| "I built MCP servers for Dynatrace/Snyk" | "The architecture decision wasn't the MCP protocol — it was the security boundary. I designed every MCP server with scoped permissions (read-only traces, write-PR-never-merge) because I knew the security team would flag autonomous agents. By anticipating that concern, I got approval in weeks, not months." |
| "5+ teams use my agent skills" | "The adoption number is lagging indicator. The leading indicator was: I made the skills customizable. The first version failed because it was too rigid. When I redesigned it as a configurable playbook — teams choose their phases, approval gates, notification preferences — adoption took off. The lesson: platform thinking means designing for what you can't predict." |

### 3. Business Alignment Stories (Metrics, Build vs Buy, Roadmap)

| Your current answer focuses on... | Principal altitude reframe |
|---|---|
| "60% productivity gain" | "The business outcome: unblocked quarterly releases that had been stalled for 6 months. The 60% is a technical metric. The business metric is: 'features that were stuck on the dependency upgrade backlog started shipping again.' Always translate technical metrics to business outcomes." |
| "99.9% uptime" | "99.9% isn't an ops number — it's a customer trust number. Every minute of unplanned downtime during bill cycle costs us support calls, escalations, and churn risk. That's why I invested in circuit breakers and bulkheads — not to hit a technical SLA, but to protect customer experience." |
| "I chose the tech stack" | "When I chose the stack, I considered: how hard is it to hire for? How hard is it to operate? What's the migration cost if we're wrong? The technical choice is the easy part. The organizational choice — can we staff this, operate this, replace this? — is the actual decision." |

### 4. Organizational Influence Stories (Adoption, Mentoring, Conflict)

| Your current answer focuses on... | Principal altitude reframe |
|---|---|
| "I got 5 teams to adopt" | "I didn't sell them a tool. I solved their problem first — paired with one early adopter, showed measurable time savings, then made it customizable so they didn't have to change their workflow. The adoption was the outcome of trust, not a sales pitch." |
| "I mentored senior engineers" | "I don't frame it as mentoring. I ask: 'I'm working on X — can I run my design by you?' This turns mentoring into collaboration. The senior engineer brings their experience, I bring mine, and we both grow." |
| "I disagreed with my manager's approach" | "I didn't say 'your approach is wrong.' I said 'let me prove a different approach on a small scope.' I built the prototype for one Sling API, showed the data, and let the results speak. The manager wasn't wrong — they just hadn't seen AI work. My job was to de-risk the decision, not win the argument." |

### 5. Strategy & Vision Stories (Roadmap, Future of AI, Org Design)

| Your current answer focuses on... | Principal altitude reframe |
|---|---|
| "The next step for our platform" | "In 3 years, the platform needs to be: (a) service-mesh-enabled so traffic management is declarative, (b) multi-cloud capable so we aren't locked into one provider, (c) AI-native so agents are first-class participants in our SDLC. Year 1: migrate to service mesh. Year 2: add multi-cloud escape hatches. Year 3: ship the shared AI agent platform. Each phase has a checkpoint: if the metric doesn't improve, we stop and reassess." |
| "How I see AI evolving" | "The shift from 'AI as autocomplete' to 'AI as autonomous agent' is real, but the bottleneck isn't the model — it's the governance framework that lets agents operate safely at scale. The companies that win will be the ones that solve 'how do I trust an agent to write code that ships to production?' not 'how do I make an agent write code?' The answers are: scoped permissions, auditable actions, human-in-the-loop gates." |
| "How I'd organize teams" | "DDD-driven team boundaries. Each team owns a bounded context end-to-end. A small platform team owns shared concerns (API gateway, observability, CI/CD). Success metric: product team velocity, not platform features shipped. If the platform team is a bottleneck, we've failed." |

---

## Quick Reframe Cheat Sheet

| If they ask about... | Your old frame | Your new frame |
|---------------------|---------------|---------------|
| **Architecture** | "I built it with X" | "I chose X over Y because our incident history showed Z" |
| **Migration** | "We moved from A to B" | "I sequenced the migration by business risk: billing first, then content" |
| **AI adoption** | "They use my tools" | "I made it customizable so teams didn't have to change their workflow" |
| **Metrics** | "60% productivity" | "Unblocked 6 months of stalled releases" |
| **Conflict** | "I proved them wrong" | "I de-risked their concern with a prototype" |
| **Mentoring** | "I taught them" | "I collaborated on their problem and we both grew" |
| **Failure** | "The agent patched the test" | "I trusted automation without a verification layer — now it's standard" |
| **Strategy** | "We should do X" | "Phased: Year 1 quick wins, Year 2 platform, Year 3 differentiation" |
| **Build vs Buy** | "We built it because..." | "We buy solved problems so our team builds what differentiates us" |

---

## The 3 Anchor Stories (Reframed at Principal Altitude)

### Anchor 1: Spring Boot 3 Migration
**Principal frame:** "I saw that the org was bottlenecked on a mechanical problem — 50K lines of repetitive migration work. The technical solution (AI automation) was straightforward. The organizational challenge was: convincing teams that AI-generated code was safe, convincing leadership that the investment would pay off, and building the playbook so the approach scaled beyond me. I solved it by: building the reference implementation first (not asking permission), measuring and publishing the results, and making the playbook self-service. The metric that mattered wasn't 'lines of code migrated' — it was 'time unblocked for the business to ship features.'"

### Anchor 2: Sling TV Modernization
**Principal frame:** "The 80 Rails APIs weren't just a technical problem — they were a business bottleneck. Every feature request went through a 'we need to understand the whole codebase before touching anything' filter. The key decision wasn't tech stack (Java over Rails) — it was data consistency. Splitting a monolith's database without losing ACID transactions was the make-or-break architecture decision. The Saga pattern on Kafka solved it, but it required the entire team to shift their mental model from 'transactions roll back' to 'transactions compensate.' That's the kind of architectural shift that determines whether a migration succeeds or creates a worse system than the one it replaced."

### Anchor 3: AI Agent Skills (Org Adoption)
**Principal frame:** "The first version of my agent skill was a failure — too rigid, fixed 5-phase workflow that didn't fit how other teams operated. Nobody used it after the first try. I had to decide: abandon the idea, or redesign it for adoption. I chose redesign, but not by adding features — by making it configurable. Teams could customize phases, approval gates, skip steps. That's when adoption took off. The lesson: the difference between a tool that stays on one team and a practice that scales across the org is *how easy you make it for others to say yes*. The architecture decision wasn't the MCP protocol — it was the customization framework."

---

## How to Practice This Shift

1. **Record yourself** answering your top 10 questions from `interview_prep.md`
2. **Listen for:** do you sound like a Staff Engineer (technical depth, implementation detail) or a Principal Engineer (org context, business outcomes, strategic tradeoffs)?
3. **If you hear "I built," "I designed," "I implemented"** → reframe to "I chose," "I sequenced," "I influenced," "I de-risked"
4. **If you hear technical metrics** (uptime, latency, coverage) → add business translation ("this meant features unblocked, incidents prevented, revenue protected")

**Litmus test:** Can you explain this decision to a VP of Product without using a single technology name (no Kafka, no Kubernetes, no Spring Boot)? If yes, you're at Principal altitude. If you need the tech names to explain why it matters, keep reframing.
