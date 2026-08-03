# Day-of One-Pager — The Standard (Principal V, IBTE)

**30-second scan before the interview. Full detail in `00_Points_Quick_Notes.md` and each talks/ doc.**

---

## Cross-Doc Quick Reference

| Topic | Doc | One-line |
|---|---|---|
| Intro | 1 | 14+ yrs, AI spec-driven modernization, 10M subs, org-wide adoption |
| Why Standard | 2 | Broader scope, founding Bangalore role, event-driven insurance, CIO AI vision |
| Sling UMS | 3 | UMS (User Mgmt Service): 80+ Rails → Java, 6 bounded contexts, Saga (3 iterations), feature flags, 70% faster/engineer |
| Adoption w/o authority | 4 | Show data not arguments; VP demo 2 weeks vs 3 days; 5 teams in a quarter |
| Mentoring | 5 | Guided questions + progressive ownership; 8 months mid→senior; STB Health Monitor |
| Incident | 6 | itma-auth JWT cache HashMap OOM every 6-8h at 50K req/min; Guava CacheBuilder (max 50, TTL 6h) + memory gate; zero recurrence 6 months |
| Disagree w/ leadership | 7 | 2-week POC beat the argument; 40% velocity; trust gained |
| From scratch | 8 | Observability-first, progress not proposals, 90 days, "didn't wait for permission" |
| Cross-team | 9 | Spring Boot 3: 3 months vs 6 target, 50K+ lines, 60% per-engineer gain, gamified dashboard, award |
| Tech debt | 10 | 4 categories (security/scaling/productivity/aesthetic), 20% sprint, 80-20 |
| Multi-team leadership | 11 | Guilds, shared standards, hands-on; consistency not conformity |
| Resistant team | 12 | Diagnose 4 causes; do the first one yourself |
| AI memory | 13 | 3-layer memory; retrieval over context stuffing; ~10x token savings |
| Kiro AI-DLC | 14 | Plan before you code; Inception/Construction/Operations |
| AI governance | 15 | Govern, audit, control; scoped perms + approval gates; 3 tries then escalate |
| Worktrees | 16 | One worktree per agent; conflicts at merge time; Git 2.5 (2015) |
| AI glossary | 17 | 15 key terms: agent, MCP, ReAct, evals, control plane... |
| Kafka Sling | 18 | RF 3, 12 partitions, subscriber-ID key, DLQ after 3 retries |
| Business→tech | 19 | I don't start with technology |
| Question inventory | 20 | Coverage map + open questions; numbers drill |
| My Dish arch | 21 | 12 services, REST+Kafka hybrid, GemFire, 99.9% (before: 99.5%) |
| STB Health | 22 | DMZ NGINX, Cognito+Okta, 30-day cert rotation, 10K req/s @ 99.9% |
| First 90 days | 23 | Listen, Align, Deliver |
| Claims system design | 24 | Schema Registry + Outbox + WORM audit; event_id dedup |
| 5→50 teams | 25 | Versioned registry, MCP guardrails, Agent Guild + CI evals |
| AWS/GCP→Azure | 26 | Kubernetes is Kubernetes; EKS→AKS, IAM→Workload Identity, Secrets→Key Vault CSI |
| Flink gap | 27 | Kafka Streams foundation, concepts translate, no bluffing |
| Amazon Q fidelity | 28 | Shadow-traffic diff testing, 10K+ tests @ 85%+; Q ≠ 2M lines alone |
| Team AI enablement | 29 | Reduce friction + learning cost; Figma/Pencil/NotebookLM |
| Interview feedback | 30 | 5 gaps + defenses; 4-step answer standard |
| Results | — | Asset Mgmt + Shift Allowance; code → container → production |

---

## Top 20 Numbers (keep cold, pause after each)

1. **14+ years** total; **10 years** MSys (SE → Technical Architect), **4 years** Dish (Lead → Staff)
2. **10M+ subscribers**, **99.9% uptime** (8.7 hrs/yr budget), **sub-second** latency; before-story: ~99.5% → 99.9%
3. **80+ Rails APIs** → Java microservices, **70% faster delivery per engineer** (2-week task → 3 days)
4. **6 DDD bounded contexts** (Sling UMS) ≠ **12 microservices** (My Dish) — keep separate
5. **50K+ lines** Spring Boot 3 migration, **60% productivity gain** (per-engineer output), **3 months vs 6-month target**, 20+ services
6. **400K+ lines** reverse-engineered, **2M+ lines** scaffolded, **10K+ tests @ 85%+** coverage (Amazon Q, effort -70%)
7. **Numbers drill:** 60% (Spring Boot 3, output) / 70% (Sling, delivery) / 70% (Amazon Q, effort) / 50% (NetApp regression) — separate projects
8. **2 weeks → 3 days** for one service via AI spec-driven (VP demo); **5 teams in a quarter** (organic adoption)
9. **2-3 days → 5 minutes** service setup (GCP/Firebase MCP POC, personal project)
10. **30 min → 2 min** incident diagnosis (Dynatrace MCP); **same-day** vuln fixes (Snyk MCP)
11. **OOM every 6-8h** at **50K req/min** (itma-auth); fix: cache **max 50 / TTL 6h / LRU**; **heap < 10%** CI gate; zero recurrence 6 months
12. **500 concurrent VUs** (JMeter), **30-min** heap runs (YourKit) — the load-test story
13. **2-week POC** (low-code vs Spring Boot) → **40% velocity** improvement
14. **90 days** from-scratch: observability on every service, API standards on 3 teams
15. **20% sprint capacity** for tech debt; **80-20** balance; 4 debt categories
16. **8 months** mid-level → senior (mentoring); he now mentors others
17. **23 integrations**, **7 SFTP targets** (DPA); **10K req/s @ 99.9%** (STB Health); **RF 3 / 12 partitions / DLQ after 3 retries** (Kafka)
18. **Codefest 2023** win (Asset Management, **70% manual-effort cut**); **HR Spot Award** (Shift Allowance); **+60% on-site sales** (Field Catalogue)
19. **Pivot3**: **60% provisioning cut**, **1000+ volumes**; **NetApp**: **100+ Selenium scenarios**, **50% regression cut**; **5x Best Performer**
20. **Awards:** Technical Excellence 2024 + 2025 (AI workflows — not tied to Field Catalogue/hackathons); Spot 2023+2025; CPAW

---

## Power One-Liners (Principal signals)

- "I don't start with technology." (business → tech)
- "Show data, not arguments. Let them decide." (influence)
- "Plan before you code." (AI-DLC)
- "Retrieval over context stuffing." (AI memory)
- "Govern, audit, control." (agent governance)
- "Consistency, not conformity." (multi-team standards)
- "Progress, not proposals." (from-scratch ownership)
- "Listen, Align, Deliver." (first 90 days)
- "Automate the mechanical part; humans keep the judgment." (AI modernization)
- "The root cause wasn't the cache — no eviction policy." (incident insight)
- "Don't abstract until you've seen the pattern three times." (restraint)
- "Same pattern, new domain, bigger scope." (the close)

---

## 4-Step Answer Standard (from feedback doc 30)

1. **BLUF** — conclusion first ("I compressed an 18-month migration to 5 months.")
2. **Signpost** — "Three areas: X, Y, Z."
3. **Stack mechanics** — exact chain (DMZ → Okta → GemFire → Resilience4j → HikariCP/Liquibase → Dynatrace)
4. **Metric impact** — the number with its measurement story

Never: "we made a REST API." Always: the full chain + the number.

---

## Do / Don't

- ✅ Pause after every number; say "ninety nine point nine" and "sub second" slowly
- ✅ Dish is telecom, not insurance — pivot to the transferable framework honestly
- ✅ GCP POC = personal project ("on my own time"), not Dish work
- ❌ Don't tie Technical Excellence Awards to Field Catalogue/hackathons
- ❌ Don't say "IBTE" in conversation; don't complain about Dish ("I'm looking because...")
- ❌ Don't claim Flink production mastery or "Amazon Q autonomously wrote 2M lines" — disarm with honesty first
- ❌ Don't list all 12 My Dish services — name 4-5 domains
