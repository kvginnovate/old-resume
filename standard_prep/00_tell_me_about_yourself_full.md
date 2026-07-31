# "Tell Me About Yourself" — Full Version (3 min)
## Arc: Mobile → UI → Backend → Full-Stack

> Written for general Principal/Staff interviews. Emphasizes breadth-to-depth arc: how each layer you touched made you a better architect.

---

## Script

---

***(breathe)*** I'm a Staff Engineer at Dish Network in Bangalore — 14 years in the industry working across mobile, frontend, backend, and now full-stack. My career arc is a deliberate expansion: I started at the user-facing layer, moved deeper into the stack with each role, and today I own architecture from the mobile screen to the database.

***(breathe)*** Let me walk you through that arc.

---

### Phase 1: Mobile — "Where I learned to ship"

I started my career at MSys Technologies in 2012 — an IT services firm. My first real project was building enterprise Android apps for US clients. I led a team of 3 engineers to ship Nasuni — a cloud storage client — and Spree Wearables, a fitness companion app, both on the Google Play Store. I handled everything: UI, local caching, REST API integration, analytics.

I also built Mobitaz — a mobile test automation framework from scratch. It did record-and-playback across multiple Android devices simultaneously. That framework later became part of MSys's QA service offering and was used in client demos.

**Lesson from mobile:** I learned that a beautiful API is worthless if the mobile client has bad connectivity. I developed a deep appreciation for offline-first design, battery-aware networking, and the gap between "it works on my machine" and "it works in a field technician's van with spotty signal."

---

### Phase 2: UI / Frontend — "Where I learned to think in API contracts"

After a few years, I wanted to move beyond Android-specific code and build for the web. I took on the role of technical lead for Pivot3 — a VMware hyper-converged infrastructure product. I built a ReactJS plugin for VMware's vSphere management console — enterprise UI that had to match the look and feel of VMware's own interface. I also built a vRealize Orchestrator plugin for automating bulk volume provisioning.

This phase taught me something critical: **my job wasn't just writing React components — it was defining the API contracts that both the UI and the backend would agree on.** I started writing OpenAPI specs before writing code, which became a habit I carry to this day.

---

### Phase 3: Backend — "Where I learned scale"

The UI work naturally pulled me deeper into the backend. I was already defining API contracts, so it was a small step to owning the services behind them. At Pivot3, I architected REST APIs for HCI volume management. I learned event-driven patterns.

When I moved to Dish Network in 2022, I went all-in on backend. I architected distributed microservices for the subscriber platform — Spring Boot 3, Kafka for event-driven communication between services, GemFire for distributed caching. The platform serves 10 million subscribers at 99.9% uptime.

**Two projects defined my backend phase:**

**First, the Spring Boot 3 migration.** Spring Boot 2 hit end-of-life. Security filed CVEs, new features were blocked. The team estimated 18 months of manual work across 50,000 lines of code to migrate from `javax.*` to `jakarta.*`. I wrote a migration guide, built AI-driven automation tooling and agent skills that renamed code, converted security configs, and regenerated tests at 85% coverage. I compressed 18 months to 5 months — a 60% productivity gain — and was promoted from Lead to Staff Engineer as a result.

**Second, the Sling TV modernization.** We had 80 legacy Ruby on Rails APIs — 400,000 lines of undocumented code. The business needed to ship streaming features faster. I used Amazon Q to reverse-engineer the entire codebase — ingested models, controllers, routes, database schemas — and scaffolded Java microservice skeletons. I grouped the 80 APIs into bounded contexts using DDD: billing, content catalog, entitlements. I designed the migration using feature flags and traffic shifting — 10% to new, then 50/50, then 100%. Dynatrace traced every request across both systems. The project delivered 70% faster delivery timelines.

**Lesson from backend:** Scale is not just about throughput. It's about operational readiness — incident response, runbooks, post-mortems, observability. I set up Dynatrace dashboards, PagerDuty alerting, and built custom MCP servers that give AI agents read-only access to distributed traces. Incident diagnosis went from 30 minutes to 2 minutes. I established 85%+ test coverage as a CI gate and integrated Snyk security scanning across all teams.

---

### Phase 4: Full-Stack — "Where it all came together"

Today, I'm full-stack by design, not by accident. I still own backend microservices, but I also build mobile and web frontends because I know the constraints at every layer.

- **Kiro Mobile** — a React Native app that lets developers trigger and monitor AI coding tasks from their phones. Real-time WebSocket updates, GitLab MR status, Dynatrace alerts. I designed the custom MCP servers for GitLab and Jira integration. Presented at Dish Ignite 2026.
- **In-Home Service Catalogue** — an offline-first React Native app for field technicians with local content caching. Eliminated the need for cellular connectivity during customer visits. The sales team reported a measurable increase in on-site upsells.
- **Set-Top-Box Health Monitor** — a real-time monitoring dashboard and REST APIs capturing payload data from 10 million subscriber devices.

I also built 3 internal tools (Asset Management, Shift Allowance, Seat Booking) — full-stack with Next.js frontends, containerized, with Dynatrace dashboards. Asset Management won Codefest 2023 and was adopted company-wide.

Beyond shipping code, I established engineering practices that scale across teams: wrote Dish's Spring Boot 3 migration guide, defined API design standards, set up security scanning processes, built agent skills that are now used by 5 engineering teams. I mentor senior developers, participate in hiring panels, and lead incident response.

---

### Why I'm here

After 4 years at Dish with two consecutive Technical Excellence Awards, I've delivered significant impact on the subscriber platform. But I've outgrown a single-product scope. I want a Principal role where I drive technical strategy across multiple product lines — the kind of role where architecture decisions have a 5 to 10-year horizon.

I bring full-stack breadth with backend depth, experience building systems at 10-million-user scale, and a track record of AI-accelerated delivery and org-wide influence. I'm ready to apply all of that at Principal level.

---

## Timing Breakdown

| Section | Time | Key Message |
|---------|------|-------------|
| Hook (current role) | ~15s | 14 years, full-stack, 10M users |
| Phase 1: Mobile | ~30s | Shipped Android apps. Offline-first mindset. |
| Phase 2: UI/Frontend | ~30s | API contracts. OpenAPI specs. |
| Phase 3: Backend | ~60s | Spring Boot 3 migration. Sling TV modernization. Incident response. |
| Phase 4: Full-Stack | ~45s | Kiro Mobile. Field Catalogue. MCP servers. Org-wide influence. |
| Why here | ~15s | Outgrown single-product scope. Principal trajectory. |

## Power Numbers to Hit

| Number | Where it lands |
|--------|----------------|
| 14 years | Total experience |
| 10M subscribers | Scale of your platform |
| 80 legacy APIs → Java microservices | Sling TV modernization |
| 18 months → 5 months (60% gain) | Spring Boot 3 migration |
| 400K lines reverse-engineered, 2M+ lines scaffolded | Amazon Q Sling project |
| 85%+ test coverage | Quality gate you established |
| 30 min → 2 min incident diagnosis | MCP-driven observability |
| 5 engineering teams using your agent skills | Org-wide influence |
| Technical Excellence Award (2024, 2025) | Two consecutive years |

---

## Delivery Tips

1. **Don't rush Phase 1-2** — the first two phases show breadth that 99% of backend-only candidates can't claim. Let them land.
2. **Phase 3 (Backend) is the anchor** — expect 50% of follow-up questions here. Have the Spring Boot 3 and Sling stories ready for deeper probing.
3. **Phase 4 (Full-Stack) closes the loop** — it proves the arc was intentional, not accidental.
4. **End with "why this role"** — tailor the last 15 seconds to the specific company you're interviewing with.
