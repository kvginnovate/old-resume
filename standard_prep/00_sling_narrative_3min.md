# "Tell Me About Yourself" — 3-Minute Script for The Standard

> Optimized for this role. Trimmed Dish-detail (STB Health, Field Catalogue, App Store). Prioritizes: architecture ownership → AI-driven migrations → org-wide leverage.

---

## Script (~3 min spoken)

***(breathe)*** I'm a Staff Engineer at Dish Network — 14+ years, currently architecting the subscriber platform serving over 10 million users. I joined Dish as a Lead and was promoted to Staff within two years.

***(breathe)*** My platform runs on Spring Boot 3 microservices, deployed on Kubernetes, with Kafka for event-driven communication between services. I own the full architecture — API design standards, security gates, observability, operational readiness. When something breaks at 2 AM, I'm on the call.

***(breathe)*** Two projects define my impact:

**First, the org-wide Spring Boot 3 migration.** Spring Boot 2 hit end-of-life. Every week we stayed on it, security filed CVEs and new features were blocked. The team estimated 18 months of manual work across 50,000 lines of code. I compressed that to 5 months using AI-driven migration workflows. The tooling I built automatically renamed 50K+ lines from `javax.*` to `jakarta.*`, converted security configs, and generated tests at 85% coverage. I built a dashboard showing leadership the real-time impact — lines changed by AI vs manually, test pass rates, time saved per service. That data convinced the VP to scale the approach. The result: 60% productivity gain, and I was promoted to Staff.

**Second, the Sling TV modernization.** We had 80 legacy Ruby on Rails APIs, 400,000 lines of code, no documentation, and tight coupling across every feature. The business needed to ship streaming features faster. I used Amazon Q to reverse-engineer the entire codebase — it ingested every model, controller, route, and database schema, generated OpenAPI specs from the routes, and scaffolded Java microservice skeletons. I grouped the 80 APIs into bounded contexts using DDD — billing, content catalog, entitlements — each becoming an independent service. We used feature flags for traffic shifting: 10% to new, then 50/50, then 100%. Dynatrace traced every request across both systems. The hardest problem was data consistency — splitting a monolith's database loses ACID transactions. We solved it with the Saga pattern on Kafka: each service publishes an event, downstream services update their own state, and compensation logic rolls back on failure. We delivered in 5 months what was estimated at 18 months.

***(breathe)*** Beyond migrations, I established the engineering practices that make the platform reliable. I built custom MCP servers that give AI agents read-only access to distributed traces — incident diagnosis went from 30 minutes to 2 minutes. I built a Snyk MCP server so AI agents scan for vulnerabilities and create same-day fix PRs — what took 2 to 7 days now takes hours. I mandated 85%+ test coverage as a CI gate. These agent skills are now used by 5 engineering teams at Dish.

***(breathe)*** What I'm looking for next is a role where architecture decisions have a 10-year horizon — where the right design today pays off for a decade. The Standard's platform modernization effort is exactly that kind of challenge. I bring deep experience in event-driven architecture, cloud-native design, and AI-accelerated engineering — and I'm ready to apply it at Principal level.

---

## Timing Breakdown

| Section | Time | Key Message |
|---------|------|-------------|
| Current role + platform | ~30s | I own architecture for 10M+ users |
| Spring Boot 3 migration | ~45s | AI-compressed 18 months → 5 months. Measured. Scaled org-wide. |
| Sling TV modernization | ~60s | 80 Rails APIs → Java microservices. Saga pattern. 18mo estimate → 5mo. |
| AI practice (MCP, agents) | ~30s | Built tooling adopted by 5 teams. Compressed incident time 30min→2min. |
| Why The Standard | ~15s | Ten-year architecture horizon. Event-driven modernization. |

---

## Before/After (what changed)

| Detail | Full Version (existing) | This Version |
|--------|------------------------|--------------|
| DPA ColdFusion migration | Included | Cut — not relevant to this role |
| STB Health / Field Catalogue | Included | Cut — distracts from Principal narrative |
| App Store mobile app | Included | Cut |
| GemFire caching | Mentioned | Folded into platform summary |
| AI agent scaling (5 teams) | Buried at end | Promoted — shows org-wide influence |
| "Why The Standard" hook | Missing | Added — directly addresses this interview |

---

## Delivery Rules

- **Land these numbers exactly:** "10 million subscribers," "5 months vs 18 months," "60% productivity gain," "30 minutes to 2 minutes," "5 teams"
- **Don't stop at the migration story** — bridge to "and I made it stick" via MCP servers, standards, CI gates. That's the Principal difference.
- **Sling story is the anchor** — 40% of follow-ups will probe here (partition math, data consistency, traffic shifting, what broke). Be ready.
