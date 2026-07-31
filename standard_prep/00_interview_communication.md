# Interview Communication — Principal Engineer Edition

> Read time: 15 min. Practice time: 45 min. This is your highest-ROI hour today.

---

## The 5 Communication Rules

### Rule 1: Lead with the Conclusion, Then the Evidence

**Wrong:** *"So we had 12 services, Spring Boot 2 was EOL, security was filing CVEs, and I started looking at Kiro, and I tried it on one service, and it took 3 days instead of 2 weeks, so I showed it to the VP, and then..."*

**Right:** *"I compressed an 18-month migration to 5 months using AI. Here's how."*

Answer structure: **Conclusion → Evidence → Context (if needed).** Never the reverse.

### Rule 2: Speak in Business Outcomes, Not Technical Verbs

Replace "I built / I coded / I migrated / I configured" with:

| Don't Say | Say |
|-----------|-----|
| "I migrated 12 services" | "I unblocked 6 months of stalled feature releases" |
| "I built a Dynatrace MCP server" | "I compressed incident diagnosis from 30 minutes to 2 minutes" |
| "I used AI for the migration" | "I achieved 60% productivity gain across the engineering org" |
| "I drove adoption across 5 teams" | "I created a practice that 5+ engineering teams adopted org-wide" |

**Litmus test:** Can you say your answer without using any technology name? (Kafka, Spring Boot, Kubernetes, MCP, Kiro) If yes — you're at Principal altitude. If you need the tech names to explain why it mattered — reframe.

### Rule 3: Use the STAR-F Framework

| Letter | What | Time |
|--------|------|------|
| **S**ituation | The business context. What was at stake? | 15s |
| **T**ask | What you personally owned | 10s |
| **A**ction | The decisions you made (not the code you wrote) | 30s |
| **R**esult | The business outcome, with a number | 15s |
| **F**ramework | The meta-lesson: "Here's what this taught me about [problem class]" | 10s |

**The F is what separates Principal from Staff.** After the result, add a one-sentence framework that shows you generalize:

- *"The lesson: when you're blocked on a mechanical problem, automate the mechanical part and have humans review the judgment calls."*
- *"The pattern I now apply: infrastructure decisions should be reversible, data decisions should be irreversible. Plan accordingly."*

### Rule 4: Bridge Every Question to a Story You Know

When you get a question that catches you off guard:

> *"That's a great question. I haven't faced that exact scenario, but it reminds me of the Sling TV modernization where we had to handle data consistency after splitting a monolith database. Let me tell you how I approached that, and then I'll connect it to your question."*

**Always have 3 anchor stories ready to bridge to:**
1. **Spring Boot 3 migration** — for any "how did you drive change / influence / adopt AI" question
2. **Sling TV** — for any "system design / migration / data consistency" question
3. **AI Agent Skills** — for any "innovation / failure / adoption / influence" question

### Rule 5: Read the Room — Adjust Your Depth

| The Interviewer | What They Want | How You Answer |
|----------------|---------------|---------------|
| **VP / Director** | Business outcomes, org impact, strategy | Lead with the number. Never mention a framework or library by name unless asked. |
| **Peer Engineer** | Technical depth, tradeoffs, edge cases | Go deeper. Be specific. "We chose Saga over 2PC because..." |
| **Product / PM** | Delivery, timelines, tradeoffs, communication | "We sequenced by business risk, not technical convenience." |
| **HR / Recruiter** | Culture fit, growth, motivation | "Why I left Dish," "What I look for in a team," "How I handle conflict." |

**When in doubt, start at the business level and ask: "Do you want me to go deeper on the technical details?"**

---

## Answer Templates for Common Moments

### "Tell me about yourself" (130s)

1. **Current role + scale** (20s): *"I'm a Staff Engineer at Dish Network, 14+ years, architecting the subscriber platform for 10M+ users."*
2. **Biggest impact** (45s): *"Two projects define my impact: I compressed an 18-month migration to 5 months using AI (60% productivity gain), and I led the Sling TV modernization from 80 Rails APIs to Java microservices."*
3. **Org-wide influence** (30s): *"I built custom AI agent skills that are now used by 5+ engineering teams — MCP servers for Dynatrace, Snyk, GitLab. Incident diagnosis went from 30 minutes to 2 minutes."*
4. **Why here** (20s): *"What I'm looking for next is a role where architecture decisions have a 10-year horizon. The Standard's platform modernization is exactly that kind of challenge."*

### "Why do you want to work here?"

**Wrong:** "I've always admired your company."
**Right:** *"The Standard is modernizing its platform with event-driven architecture and cloud-native design — that's exactly what I've been doing at Dish. The IBTE platform needs exactly the kind of architecture ownership, AI-accelerated modernization, and cross-team influence I've been delivering. Plus, the insurance domain has real compliance and regulatory constraints that make the architecture interesting — not just 'move fast and break things.'"*

### "What's your biggest weakness?"

**Wrong:** "I work too hard." (Everyone says this)
**Right:** *"I tend to go deep on the technical solution before bringing the team along. I learned this the hard way — my early AI agent skill was technically correct, but nobody used it because I hadn't involved the teams in the design. Now I write ADRs publicly, run design review sessions, and explain the 'why' before the 'what.' The feedback that changed this was: 'Your designs are technically correct, but you don't bring the team along.'"*

### "Tell me about a time you failed"

**Wrong:** "I don't really fail." (Liar)
**Right:** *"My first AI agent skill was too rigid — a fixed 5-phase workflow that didn't fit how other teams worked. Nobody used it after the first try. I redesigned it as a configurable playbook where teams customize phases, approval gates, and notifications. That version was adopted by 5+ teams. The lesson: platform thinking means designing for what you can't predict."*

### "Do you have any questions for me?"

**Pick 3 from `15_questions_to_ask.md`. Never say "no."**

| Interviewer | Question |
|------------|----------|
| Hiring Manager | *"What's the biggest architectural challenge you're facing on the IBTE platform?"* |
| Peer Engineer | *"How does the team handle technical debt — is it on the roadmap or reactive?"* |
| Director/VP | *"What does success look like for this role in the first 6 months?"* |

---

## Non-Verbal Communication

| Signal | Do | Don't |
|--------|----|-------|
| **Pacing** | Pause 2 seconds before answering. Shows you're thinking, not reciting. | Rush to fill silence. |
| **Eye contact** | Look at the camera (remote) or the interviewer (in-person). | Stare at your notes or the whiteboard while talking. |
| **Hands** | Use gestures to illustrate structure: "On one hand... on the other hand..." | Cross arms, fidget, touch face. |
| **Voice** | Slow down on the number. Pause after it. Let it land. | Trail off at the end of sentences. |
| **Volume** | Slightly louder than normal conversation. Energy signals confidence. | Whisper or monotone. |

---

## The 3 Most Dangerous Communication Traps

### Trap 1: The Data Dump
You get asked a question and you pour everything you know about the topic. The interviewer is lost 30 seconds in.

**Fix:** Say the conclusion first. Then offer one detail. Then ask: *"Is that the level of detail you're looking for, or should I go deeper?"*

### Trap 2: The Humble Brag
*"I'm not saying I'm the best, but..."* or *"I don't want to sound like I'm bragging, but..."*

**Fix:** Just state the fact. *"I led the migration. 18 months compressed to 5 months. 60% productivity gain."* Let the number speak. Don't soften it.

### Trap 3: The Answer That Never Ends
You keep adding details because you're not sure if you've answered the question.

**Fix:** Watch for the interviewer's eyes glazing over or them looking at the clock. When you see it — **stop.** Say: *"In short: [one sentence summary]."*

---

## Communication Drill — 30 Minutes

For each of the 5 questions below, **say your answer aloud**, time it, and refine:

| # | Question | Target Time | Your File |
|---|----------|-------------|-----------|
| 1 | "Tell me about yourself" | 130s | `00_sling_narrative_3min.md` |
| 2 | "Why do you want to work here?" | 60s | `00_company_research_standard.md` |
| 3 | "Tell me about a project you led" | 90s | `01_project_narratives.md` (P0s) |
| 4 | "Tell me about a time you influenced without authority" | 90s | `08_leadership_behavioral_qa.md` |
| 5 | "Do you have any questions for me?" | 30s | `15_questions_to_ask.md` |

**Say them aloud. Not in your head. Aloud.** Your mouth will stumble on words your brain reads smoothly. That's the gap you're closing.

---

## Emergency Phrases

| Situation | Say |
|-----------|-----|
| Need time to think | *"That's a great question. Let me think about it for a moment."* |
| Don't understand the question | *"Can you help me understand what you're looking for? Are you asking about the architecture, the tradeoffs, or the outcome?"* |
| Caught off guard | *"I haven't faced that exact scenario, but here's how I'd approach it..."* |
| Technical gap | *"I haven't worked with that specific technology in production, but I can tell you how I'd evaluate it for our stack."* |
| Need to stop rambling | *"To summarize: [one sentence]."* |
| Interviewer is disengaged | *"Does that answer your question, or would you like me to go deeper on a specific part?"* |