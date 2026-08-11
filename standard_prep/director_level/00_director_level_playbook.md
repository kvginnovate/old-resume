# Director-Level Playbook — The Standard (Principal V, BenTech Integrations)

> **Context:** One technical round with the US team is done. Feedback: *"mostly fit for Staff Engineer, not Principal."* This round (in-person, Bangalore GCC, 11 Aug 10 AM) is where that verdict gets flipped. The director assesses **org-wide altitude, business judgment, influence, and ambiguity tolerance** — NOT another technical depth test.
>
> Companion docs: `01_director_qa_scripts.md` (full answer scripts), `02_questions_to_ask_director.md` (questions to ask). Cross-references: `../02_principal_altitude_integration.md`, `../00_principal_80_20_cheatsheet.md`, `../15_questions_to_ask.md`, `../../talks/30. Standard Insurance Interview Feedback - Defense and Scripting Guide.md`.

---

## 1. What This Round Actually Tests

The US team already verified you can architect. The director is checking five things:

| # | What the director tests | How you prove it |
|---|--------------------------|------------------|
| 1 | **Org-building** — define patterns for an org, not just systems | Guilds, ADRs, self-service playbooks, quality gates, "consistency, not conformity" |
| 2 | **Influence without authority** — India-US operating model, teams that don't report to you | Spring Boot 3 story: data not arguments, VP demo, 5 teams in a quarter |
| 3 | **Ambiguity tolerance** — 4-month-old GCC, no playbook yet | First-90-days answer; "progress, not proposals" |
| 4 | **Executive communication** — business outcomes, not tech names | Litmus test below; BLUF + Rule of 3 + metric |
| 5 | **Worth the Principal V band** — the leveling question | Altitude shifts in section 2; promotion + 2 Technical Excellence Awards as evidence |

**The trap:** answering this round like a technical round. Depth is verified; altitude is not.

---

## 2. The 4 Shifts That Kill the "Staff" Label

From `../02_principal_altitude_integration.md` — the failure mode under pressure is reverting to staff altitude. The verb shifts:

| Staff (what got the feedback) | Principal (what the director wants) |
|---|---|
| "I built/architected X with Y" | "The org was bottlenecked on X. The decision was Y. The outcome was Z **business** metric." |
| "60% productivity gain" | "Unblocked 6 months of stalled releases; features started shipping again" |
| "5+ teams use my tools" | "I made it configurable so teams didn't change their workflow — adoption was the lagging indicator of trust" |
| "I chose Kafka/GemFire" | "I chose Kafka for replay/audit because our incident history showed we needed it — the decision was informed by ops reality, not fashion" |
| "I mentored senior engineers" | "I collaborated on their problem and we both grew — 'can I run my design by you?'" |
| "I proved them wrong" | "I de-risked their concern with a small-scope prototype" |

**Litmus test (from `02_principal_altitude_integration.md`):** can you explain every key story to a VP of Product without a single technology name? If you need "Kafka" to explain why it matters, keep reframing.

**Pattern to self-check while speaking:** if you hear "I built / I designed / I implemented" → swap to "I chose / I sequenced / I influenced / I de-risked."

---

## 3. The 3 Anchor Stories — Director Cut

Open with the frame, not the build:

1. **Spring Boot 3 migration**
   > "18-month estimate, 5-month delivery. The technical part was easy; the organizational part was convincing teams AI-generated code was safe. I built the reference first, showed the data, made the playbook self-service. The metric that mattered wasn't lines migrated — it was time unblocked for the business to ship features."

2. **Sling TV modernization**
   > "80 Rails APIs were a business bottleneck, not a tech problem. The make-or-break decision was data consistency — teams had to shift from 'transactions roll back' to 'transactions compensate.' That's an org-wide mental-model change, not a code change. Sequencing by business risk, not technical convenience: billing first, then content catalog."

3. **AI agent skills (org adoption)**
   > "First version failed — too rigid, nobody used it. I redesigned for adoption: configurable phases, approval gates. The architecture decision wasn't the MCP protocol — it was the customization framework. The difference between a tool that stays on one team and a practice that scales across the org is how easy you make it for others to say yes."

---

## 4. The Business Numbers Set (for this round)

The director cares about **business** numbers, not technical ones:

| Number | Business translation |
|---|---|
| 18 months → 5 months | 3 quarters compressed into 1; stalled feature releases unblocked |
| 2 weeks → 3 days per service | 60% per-engineer output; the VP-demo number |
| 5+ teams in a quarter | Organic adoption without mandate |
| 40% velocity (low-code POC) | Influence story: 2-week POC beat the argument |
| 30 min → 2 min incident diagnosis | Ops cost reduction, customer trust protection |
| Promotion Lead → Staff + Technical Excellence 2024, 2025 | Org-level recognition of the practice, not just the code |

---

## 5. Tonight's Drill (time-boxed; interview is 10 AM)

| Block | Action |
|---|---|
| 30 min | Re-read `../02_principal_altitude_integration.md` + `../00_principal_80_20_cheatsheet.md` — the whole game is those two files |
| 30 min | Say the 3 anchors aloud in reframed form, 2 min each, timer on. Record once; listen for "I built" |
| 15 min | Business numbers drill (section 4), cold |
| 15 min | Pick your 3 questions from `02_questions_to_ask_director.md` |
| 10 min | Reply to the interview mail confirming attendance |

---

## 6. Two Cautions

1. **Don't overcorrect into vision-without-substance.** The JD says hands-on coding expected. If the director goes technical, go mechanically deep (doc 30 chain: DMZ → Okta JWT → GemFire → Resilience4j → HikariCP/Liquibase → Dynatrace), but **end every answer with the business translation**.
2. **Don't argue the leveling.** "Staff, not principal" is likely invisible to the panel. If someone probes scope, demonstrate altitude; never say "I was told I'm staff." The promotion + awards are your evidence — let them speak.

---

## 7. Logistical Reminders (11 Aug, 10 AM IST)

- StanCorp Global Services India Pvt. Ltd. — show the email at the entrance
- Walk to Hibiscus building, tower 2 & 3, lift to 6th floor
- Call Nivedha (9500201398) once on the floor
- Carry government photo ID; arrive 15–20 min early; phone charged
- Org naming: mail says **BenTech Integrations** (JD said IBTE) — the panel likely = the integrations team; skew P0 stories toward integration-heavy (Sling UMS/Saga, My Dish integration patterns, agent-skills adoption)
