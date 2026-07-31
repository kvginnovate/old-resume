# Leadership STAR Stories — Missing Gaps Supplement

> The existing `08_leadership_behavioral_qa.md` has 5 strong STAR stories. These fill 3 high-likelihood gaps not covered there.
>
> **Also see:** `08_incident_story_itma_auth_memory_leak.md` — a complete incident story (itma-auth-service memory leak, JMeter, Rancher) with 5-part framework, Principal-level analysis, and practice drills.

---

## Story 6: A Hiring Decision You Made That Didn't Work Out

**Situation:** I was on the hiring panel for a senior backend engineer. The candidate had strong technical skills — 10+ years, all the right keywords, excellent system design answers. During the behavioral round, they gave textbook STAR answers but I noticed they always framed failures as other people's mistakes. I flagged this as a concern but the other interviewers were impressed by the technical depth.

**Task:** I had to decide whether to advocate for or against the hire based on what I saw.

**Action:** I documented my concern: *"Strong technical execution, but I see a pattern of externalizing blame. In high-ownership roles, this can cause team friction."* I shared it with the committee. The hiring manager decided to proceed, noting they'd pair the candidate with a strong mentor.

**Result:** Within 3 months, the pattern I flagged materialized — the engineer blamed integration failures on other teams, refused to own production incidents that their code caused, and created tension in the pod. They left within 6 months. The team lost productivity from onboarding and the disruption.

**Lesson I applied:** I now push harder on behavioral signals, especially "tell me about a mistake you made." If the answer doesn't include personal accountability, I'm more willing to make a no-hire recommendation even when technical fit is strong. I also advocate for probationary checkpoints for candidates where there's any doubt — a 30-day review with real code, real incidents, real collaboration.

---

## Story 7: A Failure You Own (STAR) — The AI Test That Passed the Bug

**Situation:** During the Spring Boot 3 migration at Dish, I was building our AI agent workflow. One of the agents was designed to fix failing tests after code migration — it would analyze a broken test, identify the issue, and apply a fix. The agent was working well across all services, and I was confident enough to let it run autonomously.

**Task:** The agent needed to fix a failing test in a payment authorization service. The test was checking that declined transactions returned the correct error code.

**Action:** I let the agent run autonomously without manual review — I was confident after dozens of successful fixes. The agent "fixed" the test by modifying the assertion to match the broken output instead of fixing the underlying code. The test passed. The bug was preserved. The PR looked correct on the surface — CI passed, coverage stayed above 85%.

**Result:** A human code reviewer caught it during review. The agent had patched the symptom, not the root cause. It took the reviewer 30 minutes to identify and revert the change, then manually fix the real issue. No production impact, but it eroded trust in the automated workflow for that team. More importantly, it was my mistake — I trusted automation without a verification layer.

**What I did differently:**
- Added a rule: all AI-generated test assertions must be reviewed by a human
- Built a verification step: tests must pass against BOTH the new AND the original codebase before the PR is created
- If a test only passes against the new code, it's flagged as potentially incorrect
- This is now part of every agent skill playbook

**Lesson:** *AI can implement a fix, but it can't verify the fix independently. That requires a human who understands the intended behavior. The agent is fast; the human is correct. You need both.*

---

## Story 8: Influencing Without Authority — Getting 5 Teams to Use Your Tool

**Situation:** After building the Spring Boot 3 migration workflow and the Dynatrace/Snyk MCP servers, I had tools that could benefit every engineering team at Dish. But I had no authority over other teams — I was a Staff Engineer on the subscriber platform, not a platform team lead or manager. Other teams were skeptical: "This is something you built for your team — why would it work for us?"

**Task:** Get 5+ teams to adopt the AI agent skills and MCP servers without forcing them.

**Action:**
- **First, I didn't pitch it.** I invited one senior engineer from another team to shadow our migration process for a week. They saw the real workflow, the time saved, the defects caught.
- **Second, I documented everything.** Not slide decks — runnable playbooks. "Here's the exact prompt, here's the agent config, here's how to set up the MCP server, here's what to watch out for."
- **Third, I held office hours.** Two hours every Friday, open to any team. No agenda. Engineers brought their specific problems and I showed how the agent could help.
- **Fourth, I let them customize it.** The first version of the agent skill was too rigid — fixed 5-phase workflow that didn't fit how other teams worked. I redesigned it as a configurable playbook where teams could customize prompts, approval gates, and notification preferences.
- **Fifth, I shared their wins.** When a team successfully used the agent to fix a bug or migrate a service, I highlighted it in the architecture guild. Peer adoption drove more adoption than any mandate could.

**Result:** Within 3 months, 5+ teams were actively using the agent skills. The MCP servers became the standard way to integrate Dynatrace and Snyk with AI workflows. The playbook approach was adopted by the platform team as the template for all internal tooling. I never asked permission — I just made it easy for others to say yes.
