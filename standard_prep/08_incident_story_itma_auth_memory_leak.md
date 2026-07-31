# Incident Story — itma-auth-service Memory Leak (JMeter + Rancher)

> A complete 90-second Principal-level incident story with framework, full script, and analysis.

---

## Part 1: The 5-Part Incident Framework

Every incident story follows this structure. Memorize the parts, not the words.

| Part | Time | What It Signals |
|------|------|-----------------|
| **Situation** | 15s | What service, how many users, business impact |
| **Detection** | 15s | Who noticed, how, how fast |
| **Mitigation** | 15s | What you did first to stop the bleeding (not root cause) |
| **Root Cause** | 30s | Why it *really* happened — not the surface symptom |
| **Prevention** | 30s | What systemic change prevented recurrence |

**Rule:** Prevention is the longest section. That's where Principal-level thinking shows.

---

## Part 2: Full Story Script (90 seconds)

### Situation (15s)

> "Our **itma-auth-service** — the central auth service handling all login and token validation — was OOM-killing every 6-8 hours in production on Rancher. ~50K requests/minute, and every crash meant users couldn't log in. This was a P0."

### Detection (15s)

> "First sign: pods crash-looping on Rancher. Auto-restart masked the problem temporarily. GC logs showed heap growing steadily with no recovery after GC — classic memory leak pattern."

### Mitigation (15s)

> "I doubled the heap and added a daily restart cron to stop the bleeding. Ugly, but it bought us time to diagnose without more production outages."

### Root Cause (30s)

> "I set up **JMeter** with 500 concurrent virtual users hitting the token validation endpoint — same load as production. Ran it for 30 minutes, took a heap dump, and opened it in YourKit.
>
> The leak: **JWT public key cache**. The service cached signing keys from the JWKS endpoint in a `HashMap` with zero eviction. Every time the identity provider rotated keys (every 24 hours), the old keys accumulated. After 7 days, the cache had 14 stale entries holding references to large certificate objects. The map grew unbounded until OOM.
>
> The root cause wasn't the cache — it was **no eviction policy and no load testing for memory stability**."

### Prevention (30s)

> "I drove three changes:
>
> 1. **Fixed the code** — replaced the raw `HashMap` with Guava `CacheBuilder` — max size 50, TTL 6 hours, LRU eviction. Keys are now auto-evicted.
>
> 2. **Added a memory stability test** — a JMeter script that runs 30 minutes of peak load and asserts heap growth < 10%. It's now a CI/CD gate. If the heap grows, the build fails.
>
> 3. **Created a 'cache checklist'** — every service on the team now must document: eviction policy, max size, hit-rate metric, and an alert when eviction count spikes. This caught similar issues in two other services within a month.
>
> **Result**: The same class of bug hasn't recurred in 6 months. The team adopted the cache checklist as standard practice."

---

## Part 3: Why This Works at Principal Level

| Signal | Where It Shows |
|--------|---------------|
| **Stayed calm under pressure** | "Doubled heap + daily restart" — bought time, didn't panic |
| **Diagnosed, didn't guess** | JMeter + heap dump — evidence-based root cause |
| **Fixed the system, not the symptom** | Cache checklist → team-wide adoption |
| **Cross-org influence** | "Two other services caught the same bug" |
| **Metrics + alerting** | Eviction-count alert, heap-growth test in CI/CD |

### What's the difference between Staff and Principal in this story?

| Done wrong (Staff level) | Done right (Principal level) |
|---|---|
| "I found the bug and fixed it" | "I triaged under pressure, stopped the bleeding, then found the root cause" |
| Technical details only | **Systemic prevention**: metrics, alerts, process change |
| "We wrote a post-mortem" | "The post-mortem changed how *other teams* do caching" |
| Blameless but vague | Blameless and specific: "HashMap with zero eviction" |

---

## Part 4: Practice Drills

### Drill 1: Say it aloud (3x)
Read the script out loud 3 times. Time yourself:

| Attempt | Time | Notes |
|---------|------|-------|
| 1st | ___s | |
| 2nd | ___s | |
| 3rd | ___s | |

Target: **85-95 seconds**. If you're under 75s, you're rushing — slow down on Prevention. If you're over 105s, cut detection details.

### Drill 2: Tell it without notes (3x)
Cover the script. Re-tell from memory. Goal: hit all 5 parts without losing any.

### Drill 3: The follow-up (practice these)
After you finish, the interviewer may ask:

- **"What was the hardest part of the diagnosis?"**
  > *"Getting the right load profile. The leak only showed under sustained production-like concurrency. Low load tests passed. I had to match the exact production traffic pattern."*

- **"How did you get other teams to adopt the cache checklist?"**
  > *"I didn't mandate it. I showed them the heap dump — two of their services had the same pattern. Once they saw the evidence, they asked for the checklist."*

- **"What would you do differently now?"**
  > *"I'd add a jvm metric for cache size to production dashboards proactively. We caught this when it crashed — I'd rather catch it trending."*

---

## Part 5: Quick Reference (Cheat Sheet)

```
SITUATION:   itma-auth-service | OOM every 6-8h | Rancher | 50K req/min | P0
DETECTION:   Pod crash-loop | GC heap no recovery
MITIGATION:  Double heap + daily restart cron
ROOT CAUSE:  JWK HashMap cache — no eviction | keys accumulated | OOM
             JMeter 500 concurrent users + heap dump → found it
FIX:         Guava CacheBuilder (max=50, TTL=6h, LRU)
PREVENTION:  Memory stability test in CI/CD
             Eviction-count alert
             Cache checklist adopted by all services
RESULT:      Zero recurrence in 6 months | 2 other services caught
```

---

## Related: Compare with Existing Q4 (MyDish Cascading Failure)

The existing `08_leadership_behavioral_qa.md` has a Q4 about a **cascading failure** (payment service timeout → thread pool exhaustion → platform outage). That story is about **resilience patterns** (circuit breakers, bulkheads).

This itma-auth memory leak story is about **memory stability and caching**. They cover different angles:

| Dimension | MyDish (Q4) | itma-auth (this) |
|-----------|-------------|-------------------|
| Type | Cascading failure | Memory leak |
| Tool | Dynatrace | JMeter + heap dump |
| Pattern | Circuit breaker, bulkhead | Cache eviction, load testing |
| Prevention | Chaos engineering, runbooks | CI/CD memory gate, cache checklist |

**Use this story when** the question is specifically about:
- "Tell me about a time you debugged a hard problem"
- "How do you find the root cause of a systemic issue?"
- "Describe your approach to performance optimization"
- "Tell me about a time you used load testing to find a bug"

**Use the MyDish Q4 story when** the question is about:
- "Tell me about a production incident"
- "How do you handle on-call / incident response"
- "How do you design for resilience"