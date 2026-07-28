# Deep Technical Narrative — How AI-Powered Modernization Improved the Product

> **Use this when:** They ask "How did modernization actually help the product?" or "Tell me the technical depth of your AI work" or "Walk me through exactly how it works."
> This is your technical deep-dive. Not a script — know the flow, tell it in your own words.

---

## The Core Thesis

Legacy code isn't just a technical debt problem — it's a product delivery problem. When your codebase is 400K lines of undocumented Ruby on Rails, adding a feature takes weeks because you can't predict what will break. When your Spring Boot services are stuck on version 2 with known CVEs, you can't ship until you patch. Modernization doesn't just make the code cleaner — it **unblocks the product team** to ship faster, more reliably, and more securely.

AI is the multiplier. Without AI, modernization is a 2-year manual rewrite. With AI, it's a 5-month validated migration with better quality than human-written code.

---

## Part 1: The My Dish Subscriber Platform — Spring Boot 3 Migration

### The Problem

The subscriber platform had 12 services running Spring Boot 2. Spring Boot 2 reached end-of-life. Every week it stayed on 2, the security team filed CVE tickets. New features were blocked because dependencies couldn't be upgraded. The team estimated 18 months of manual migration — every breaking change had to be identified, coded, tested, and validated by hand across 50K+ lines of code.

### How AI Was Used

**Step 1 — Spec-driven analysis with Kiro:**
I fed each service's codebase into Kiro with a structured prompt: "Identify all Spring Boot 2 patterns that break in 3 — security config, Hibernate annotations, Jakarta namespace, actuator endpoints, deprecated APIs." Kiro produced a structured migration plan: which files change, what the breaking patterns are, what the fix is for each one. This was the migration spec.

**Step 2 — Automated remediation:**
The Kiro agent executed the spec against the codebase. For the mechanical changes:
- `javax.*` → `jakarta.*` across 50K+ lines: fully automated, zero human intervention
- `WebSecurityConfigurerAdapter` → `SecurityFilterChain` bean configuration: automated with human review on the security logic
- Actuator endpoint path changes: automated, verified by existing test suite
- `@Type` annotation updates for Hibernate 6: automated, but flagged for human review on custom type mappings

**Step 3 — Test generation and validation:**
The agent generated test cases from the OpenAPI specs and the migrated code. I enforced a rule: every migration PR had to pass the existing test suite AND maintain 85% coverage. The agent auto-generated tests from the spec — Postman collections for contract testing, JUnit for implementation testing. Any test that failed was a signal that the migration broke something — the agent would analyze the failure, identify the root cause, and fix it.

**Step 4 — AI code change dashboard:**
I built a React dashboard that pulled data from GitLab and Kiro's output. It showed for each service: lines changed automatically vs manually, test pass rate, time saved, and defect rate. Leadership could see the real numbers — not a slide deck, but live data. This dashboard was what convinced the VP to scale the approach across all platform services.

**Step 5 — Iteration loop:**
The first few services were slow — the agent struggled with Hibernate query migrations because the old code used dynamic queries that don't translate cleanly. I updated the skill playbook to include Hibernate-specific patterns:识别 `createQuery` with string concatenation → rewrite as `CriteriaBuilder` or JPQL with parameterized queries. After 3 services, the playbook was mature enough that the remaining 9 services went through in about 3 weeks.

### Product Impact

| Before | After |
|---|---|
| Known CVEs in Spring Boot 2, security team filing weekly tickets | All services on Spring Boot 3, CVEs resolved, Snyk gate enforces no new CVEs |
| New features blocked on dependency upgrades | Dependencies always current, features ship without upgrade delays |
| 18-month manual migration estimate | 5-month migration with AI — 12 services |
| 60% less engineering effort per service | Engineers freed up for feature work instead of migration |
| Manual security config, error-prone | Automated, validated security configuration across all services |

---

## Part 2: Sling TV — Rails to Java Modernization

### The Problem

Sling TV's backend was a Ruby on Rails monolith — 80+ APIs, 400K+ lines of code, no documentation. Adding a new feature meant understanding the entire codebase because everything was tightly coupled. Deployment was risky — a change in the billing module could break content delivery. The business needed to ship streaming features faster to compete, but the monolith was the bottleneck. Estimated rewrite: 18 months, 12 engineers.

### How AI Was Used

**Step 1 — Reverse-engineering with Amazon Q:**
I ingested the entire Rails codebase into Amazon Q. The AI analyzed models, controllers, routes, views, and the database schema. It identified:
- Every API endpoint and its HTTP method, URL pattern, and response shape
- Database queries and their relationships
- Business logic flows — which endpoints called which, what the data transformations were
- Implicit behavior — Rails callbacks, `before_save` hooks, `after_create` triggers

Amazon Q generated OpenAPI specs from the routes and Java microservice skeletons from those specs. It also generated unit tests by analyzing the existing test patterns.

**Step 2 — Bounded context decomposition:**
I used DDD principles to group the 80+ APIs into bounded contexts: billing, content catalog, entitlements, recommendations, user management. Each bounded context became a candidate for an independent microservice. The AI helped identify which endpoints belonged to which context by analyzing the database schema and the call graphs.

**Step 3 — Scaffold and validate:**
For each bounded context:
1. Amazon Q generated the Java microservice skeleton with controllers, services, repositories, and tests
2. I reviewed the generated code — particularly the business logic translation (Ruby callbacks → Java Spring events)
3. The agent ran the test suite against both old (Rails) and new (Java) services simultaneously
4. Contract tests verified that both systems returned identical responses for the same inputs
5. Any discrepancy was flagged — either the migration missed something, or the AI misinterpreted the Rails logic

**Step 4 — Parallel run and cutover:**
We ran old and new in parallel for 2 weeks per bounded context. API Gateway routed traffic via feature flags — 10% to new, 90% to old initially, then 50/50, then 100% new. Dynatrace traced every request across both systems. We had a data reconciliation job that compared responses hourly.

**Step 5 — The hardest part: data consistency:**
When you split a monolith's database, you lose ACID transactions. A customer's billing status and content entitlement were in the same DB — now they're in separate services. We solved this with the Saga pattern: each service publishes an event when its local transaction completes. Kafka delivered events. Downstream services listened and updated their own state. Compensation logic rolled back if a step failed.

### Product Impact

| Before | After |
|---|---|
| Adding a feature took weeks (understand entire monolith) | Adding a feature takes days (bounded context, one service) |
| Deployment risk: one change could break unrelated features | Independent deployment per service, blast radius isolated |
| 18-month manual rewrite estimate | 5-month AI-assisted migration |
| 70% productivity gain | 12 engineers × 13 months saved = massive capacity freed for features |
| 85% test coverage (new), fewer bugs than original | Higher quality than the legacy code it replaced |
| Delivery timeline 50% faster | Sling TV ships features faster to compete in streaming market |

---

## Part 3: Custom AI Agent Skills — The Defect Lifecycle

### The Problem

Even after modernization, defects happen. A typical vulnerability remediation flow:
1. Snyk scans a service and reports a vulnerability (hours to days to review)
2. Engineer reads the advisory, understands the impact (hours)
3. Engineer identifies the affected code, implements the fix (hours to days)
4. Engineer writes tests to verify the fix (hours)
5. Engineer creates a PR, waits for review (hours to days)
6. Reviewer reviews, requests changes, re-review (hours to days)

Total: 2-7 days per vulnerability. At Dish's scale (12+ platform services, weekly Snyk scans), the backlog grew faster than it shrank.

### How AI Was Built to Solve This

**Custom agent skill — "defect-fix":**

The skill is a codified playbook with 5 phases:

**Phase 1 — Read and analyze:**
The agent connects to Jira via MCP, reads the bug report or Snyk advisory. It extracts: what the vulnerability is, which service is affected, what the fix recommendation is (for Snyk), what the CVE impact is. It then connects to GitLab via MCP and searches the codebase for the affected code patterns.

**Phase 2 — Reproduce and verify:**
The agent checks out the branch, runs the existing test suite to establish a baseline. If the bug is reproducible (a failing test exists or can be created), it confirms the issue. If the bug can't be reproduced, it pauses and asks the engineer for clarification.

**Phase 3 — Implement the fix:**
The agent applies the fix. For Snyk vulnerabilities, Snyk provides the exact remediation — the agent applies the patch mechanically. For code defects, the agent analyzes the root cause and implements a fix following the team's coding patterns. It never touches files outside the affected service.

**Phase 4 — Validate:**
The agent runs the test suite. If tests pass, it runs Snyk rescan to verify the vulnerability is resolved. If tests fail, it analyzes the failure, adjusts the fix, and reruns. This loop has a maximum of 3 iterations — if it can't fix it in 3 tries, it escalates to a human.

**Phase 5 — Create PR:**
The agent commits the changes with a conventional commit message, pushes to GitLab, and creates a PR with a description of what was fixed, why, and what tests were run. The PR is tagged as AI-generated so reviewers know to look for AI-specific patterns (overly broad changes, missing edge cases).

### MCP Servers — The Security Boundary

The agent doesn't have shell access or direct database access. Every interaction goes through MCP servers:

**GitLab MCP:** Create branches, push code, create MRs, read pipeline status. Read-only on production data. Write access only on feature branches.

**Jira MCP:** Read tickets, post comments, update status. No ability to delete tickets or modify sprint assignments.

**Snyk MCP:** Read vulnerability advisories, read fix recommendations, trigger rescans. No ability to dismiss vulnerabilities or modify security policies.

**Dynatrace MCP:** Read traces, read error rates, read service health. No ability to modify alert rules or dashboards.

Each MCP server enforces scoped permissions. The agent operates within guardrails — it can create a PR but never merge it, it can read traces but never modify monitoring, it can read vulnerability data but never dismiss a finding.

### Product Impact

| Before (Manual) | After (AI-Assisted) |
|---|---|
| 2-7 days per vulnerability fix | Hours from detection to PR |
| Engineer context-switches between features and security fixes | Engineer reviews pre-made PRs, stays focused on features |
| Vulnerability backlog grows weekly | Vulnerability backlog shrinks — same-day resolution |
| Inconsistent fix quality across engineers | Consistent, spec-driven fixes following the playbook |
| Security team waits days for fixes, blocks releases | Security team gets same-day fixes, releases unblocked |

---

## Part 4: How Modernization Compounds

The real insight isn't that AI migrated code faster. It's that each improvement compounds:

1. **Spring Boot 3 migration** → services are on a supported version → security team stops filing CVE tickets → releases aren't blocked by upgrades

2. **Snyk MCP + AI agents** → vulnerabilities get fixed same-day → security posture improves → compliance audits pass faster → fewer emergency patches

3. **Dynatrace MCP + AI agents** → incident diagnosis goes from 30 minutes to 2 minutes → mean time to resolve drops → uptime improves → subscriber satisfaction goes up

4. **Custom agent skills adopted by 5+ teams** → the fix playbook scales → every team gets the same speed and quality → the platform as a whole becomes more reliable

5. **Spec-driven AI workflows** → every new service starts with an OpenAPI spec → the spec drives code generation, test generation, documentation → new features ship with contracts, tests, and docs from day one

Each layer builds on the previous one. Modernization isn't a one-time event — it's a flywheel that makes every subsequent delivery faster and more reliable.

---

## Key Numbers to Have Ready

| Metric | Value | Context |
|---|---|---|
| Spring Boot 3 migration | 50K+ lines, 12 services | 60% productivity gain, promoted to Staff |
| Sling TV migration | 400K lines reverse-engineered | 5 months vs 18 months, 70% gain |
| Test coverage | 85%+ mandated in CI | 10K+ unit tests generated |
| Vulnerability fix time | Same-day (hours vs days) | Snyk MCP + AI agent skill |
| Incident diagnosis | 30 min → 2 min | Dynatrace MCP + AI agent |
| Platform uptime | 99.9% | 10M+ subscribers |
| Teams using AI skills | 5+ | Training sessions + playbooks |
| Awards | Technical Excellence (2024, 2025) | For modernization + AI work |

---

## Questions They'll Follow Up With

After you tell this story, expect:

- **"How did you measure 60%?"** → Time-to-complete per service: 2 weeks manual → 3 days with AI. Tracked across 12 services.
- **"What about the 20% the AI can't handle?"** → Human reviews Hibernate queries, business logic callbacks, performance-critical paths. AI handles the 80% mechanical work.
- **"How did you get other teams to adopt it?"** → Demoed on one team, showed the metrics, held training sessions, documented playbooks. Adoption came from demand, not mandate.
- **"What's the failure rate of the AI agent?"** → About 5-10% of runs need human intervention — usually complex business logic or ambiguous bug reports. The skill's exit criteria catch these and escalate.
- **"Isn't this just prompt engineering?"** → No. A prompt is a single instruction. A skill is a multi-phase playbook with decision gates, validation steps, MCP integrations, and escalation paths. It's closer to a CI/CD pipeline than a ChatGPT prompt.
