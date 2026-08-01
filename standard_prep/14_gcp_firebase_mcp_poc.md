# Project 14: GCP + Firebase + DevTools MCP — Full-Stack Agentic Development POC (Personal Project)

> **Proof of Concept (personal project):** An AI agent that runs the full development loop through MCP servers — provisions GCP infrastructure and Firebase backend from a spec, deploys the app, then inspects the running UI through Google DevTools MCP and auto-generates test cases. No console clicks, no manual config, no hand-written tests. The agent takes a spec and delivers a tested, running environment.

---

## Headline

*"I built a proof of concept where an AI agent, through Google Cloud MCP, Firebase MCP, and Google DevTools MCP, runs the complete development loop from a single spec — provisions the GCP project, Firestore collections, Authentication config, Cloud Functions, API Gateway, and Cloud Run services, deploys the app, then inspects the running web UI through DevTools and auto-generates test cases. The agent handles everything: infrastructure, auth, backend, deployment, and verification."*

---

## The Problem (Business Context)

This was a **personal project** — my own stack, my own time, not a Dish deliverable. But the motivation came from the cycle every organization has: open a ticket to the platform team, wait for a project to be created, wait for the database to be configured, wait for Auth to be set up, wait for CI/CD pipelines, then finally start coding. The setup process takes **2-3 days per service** — all manual, all repetitive. And after a service ships, verification is manual too — someone clicks through the UI and writes tests by hand.

I had already automated code generation (Spring Boot 3 migration, Sling TV) and defect remediation (Dynatrace/Snyk MCP). The next frontier: **the full loop** — infrastructure AND verification. If an AI agent could provision cloud infrastructure from a spec, the same pattern that compressed bug fixes from days to hours could compress service setup from days to minutes. And if it could then inspect its own running UI and generate tests, the loop was closed: spec in, tested environment out.

Additionally, I hold a **Google Cloud Professional Data Engineer** certification. I wanted to prove that the MCP + agent playbook I built for Dish's internal tooling (Dynatrace, Snyk, GitLab, Jira) was stack-agnostic — it works on GCP too.

---

## What I Did (Strategy, Not Just Code)

**1. I designed the MCP server mesh for GCP.** The POC used three MCP servers in concert:

- **Firebase MCP:** Reads/writes Firestore collections, manages Firebase Auth (users, custom claims, providers), deploys Cloud Functions, configures Firebase App Hosting.
- **Google Cloud MCP:** Queries and provisions GCP resources — Cloud Storage buckets, BigQuery datasets, Cloud Run services, IAM policies, Cloud Scheduler jobs, Secret Manager entries.
- **Google DevTools MCP:** Drives the browser against the running app — captures the accessibility tree, inspects rendered UI state, reads console errors, and observes network requests. This is the verification half of the loop.

Each MCP server has scoped permissions following the same security model I built for Dynatrace/Snyk: the agent can read and provision, but never delete or modify production billing.

**2. The agent workflow was a single spec input.** The POC took a single YAML spec as input:

```yaml
service: user-notifications
runtime: nodejs-20
firestore:
  collections:
    - notifications: { ttl: 30d, indexes: [userId, type, createdAt] }
    - templates: { read: public, write: admin }
auth:
  providers: [email, google]
  customClaims: [admin, user, manager]
functions:
  - name: sendNotification
    trigger: firestore.onCreate("notifications")
    memory: 256MB
  - name: aggregateStats
    trigger: schedule("0 */6 * * *")
    memory: 512MB
cloudRun:
  - name: api-gateway
    container: us.gcr.io/project/notifications-api
    cpu: 1
    memory: 512MiB
    env:
      FIRESTORE_DB: notifications
      AUTH_PROVIDER: firebase
```

The agent read this spec, then:
1. Created the GCP project (or validated existing)
2. Provisioned Firestore with the specified collections, indexes, and TTL policies
3. Configured Firebase Auth with the specified providers and custom claims
4. Deployed Cloud Functions wired to the specified triggers
5. Deployed Cloud Run services with the specified environment variables
6. Created Secret Manager entries for secrets referenced in the spec
7. Generated a Cloud Scheduler job for the `aggregateStats` function
8. Applied IAM policies — service accounts, function invokers, Firestore readers
9. Output a summary: endpoints, service accounts, deployment status

**3. The real innovation was the MCP orchestration pattern.** The agent didn't call GCP APIs directly — it routed every action through the MCP servers:

```
Agent → Firebase MCP → Firestore collections, Auth config, Cloud Functions
Agent → Google Cloud MCP → Cloud Run, IAM, Secret Manager, Cloud Scheduler
```

Each call was logged, scoped, and auditable. The same security model that made the Dynatrace/Snyk MCP servers enterprise-viable applied here: the agent could provision but never delete billing-critical resources, could read secrets but never expose them in plaintext, could create IAM policies but never grant itself admin access.

**4. The iteration loop was built in.** The agent didn't run once and stop. Output included a deployment manifest. The agent could:
- **Validate:** Check if the running environment matches the spec
- **Diff:** Show what's different between spec and current state
- **Update:** Apply only the delta — no unnecessary reprovisioning
- **Rollback:** Restore the previous state if the update failed

**5. The verification loop closed the cycle — UI inspection + auto test cases via Google DevTools MCP.** Once the app was deployed, the agent didn't stop at "it's running." It opened the app in the browser through Google DevTools MCP and verified what it built:

- **UI inspection:** Captured the page's accessibility tree and rendered state, checked that the flows described in the spec actually exist in the running UI, and read console errors and network failures.
- **Auto-generated test cases:** From what it observed in the UI — elements, flows, state transitions — the agent generated test cases covering the spec's user journeys, then ran them against the deployed app.
- **Loop back on failure:** If a test failed, the agent inspected the failing state, diagnosed whether it was a UI bug or a backend bug, fixed the code, redeployed, and re-ran the tests until green.

This is the part that made the POC more than provisioning: the agent didn't just create infrastructure, it **verified its own work end to end** — the same discipline I enforce for human engineers, now applied to the agent.

**6. The bigger pattern — AI SDLC, spec driven development across the whole lifecycle.** This POC is one instance of a pattern I apply everywhere: **spec driven development as an AI SDLC**. The spec is the source of truth, and the work is generated from it, then validated against it. I use the same spec driven approach in feature development too, not just migrations and infrastructure. The Spring Boot 3 migration, the Sling TV modernization, the defect fixing skills, feature development, and this POC are all the same loop — spec in, verified output out. The difference is only the domain: framework upgrade, legacy migration, bug fix, feature, infrastructure. The architecture of the automation is identical.

---

## The Outcome

- **Service setup: 2-3 days → 5 minutes** from spec input to running environment
- **Zero console clicks** — everything provisioned through MCP-scoped agent calls
- **Test generation automated** — UI inspected via DevTools MCP, test cases generated and run against the deployed app, failures looped back into fixes
- **Repeatable, auditable, version-controlled** — the spec IS the infrastructure definition
- Proved that the MCP + agent playbook works on **any cloud** — my production stack (Rancher-managed Kubernetes, GCP, AWS) → GCP for the POC
- Leveraged my **Google Cloud Professional Data Engineer** certification for deep GCP knowledge
- **Iteration loop** (validate → diff → update → rollback) made the POC production-ready in concept, not just a one-shot demo

---

## Principal Signal

*Infrastructure is the next automation frontier. I already proved that AI agents can fix bugs, remediate vulnerabilities, migrate code, and build features. This POC proves they can provision the infrastructure **before the code is written** — and then verify their own work by inspecting the running UI and generating tests. The pattern is the same everywhere: spec → agent → MCP server → environment → verification. That's what I mean by AI SDLC — spec driven development applied to the whole lifecycle, from feature request to tested, running software. The difference is the domain, not the architecture. The MCP security model I designed for Dynatrace/Snyk generalizes to any cloud service — that's the Principal-level insight: solve the automation pattern once, apply it everywhere.*

---

## Bridge to Any Company

*"Your company probably has a platform team that's bottlenecked on service setup — every new microservice requires 2-3 days of manual infrastructure provisioning. The GCP/Firebase MCP POC proves that an AI agent can do this from a spec in 5 minutes, with full audit trails and rollback capability. The same pattern works on Azure, AWS, or any cloud with an API. The question isn't 'can this work?' — the POC already answers that. The question is 'how do you make the spec the source of truth and the agent the executor?' That's the architecture conversation I want to have."*

---

## Watchpoints

| Question | Your Anchor |
|----------|------------|
| "What stops the agent from provisioning something expensive?" | "Same security model as Dynatrace/Snyk — scoped MCP permissions. The agent can create but never delete billing resources, never modify billing alarms, never escalate its own permissions. The spec itself is version-controlled and reviewed before execution." |
| "How does this differ from Terraform or Pulumi?" | "Terraform/Pulumi are Infrastructure-as-Code — a human writes the config, a human runs the apply. The MCP agent is **AI-driven development** — the agent writes the config from a spec, validates it, provisions it, deploys the app, then verifies it by inspecting the running UI and generating tests. The human reviews the plan, not the code. It's the same shift from 'AI writes code, human reviews' to 'AI builds and verifies, human reviews the plan.'" |
| "Did you use this in production?" | "It was a POC — my own personal project, not a Dish deliverable. The purpose was to prove the pattern works. The next step would be adding approval gates: agent generates the plan, human reviews and approves, agent executes. That's the same governance model I used for the Spring Boot 3 migration." |
| "How does the DevTools UI inspection actually work?" | "Google DevTools MCP gives the agent a browser handle on the running app. It captures the accessibility tree and rendered DOM, checks the flows from the spec actually exist, reads console errors and network failures, then generates test cases from what it observes and runs them. If a test fails, the agent inspects the state, fixes the code, redeploys, and re-runs until green." |
| "Are the generated tests any good?" | "They're spec-driven — they cover the user journeys the spec describes, which means they test the contract we promised. They don't have the judgment of a human tester on edge cases, so a human reviews them. But they catch regressions on every deploy, which is where most teams spend their time." |
| "What about state management and drift detection?" | "The iteration loop handles this. Validate compares current state against spec. Diff shows what's drifted. Update applies only the delta. This is the same pattern as Kubernetes reconciliation — the spec is the desired state, the agent is the reconciler." |
| "Why GCP when your production stack is Rancher/GCP-based and the role is Azure?" | "Two reasons: (1) I hold a GCP Professional Data Engineer certification — I wanted to prove the MCP pattern is cloud-agnostic. (2) The Standard runs on Azure. The POC demonstrates that the agent + MCP pattern works on any cloud, and I can adapt it to Azure within weeks." |
| "Why was it a personal project and not Dish work?" | "Honest answer: it started as my own exploration of the MCP pattern — I didn't need approval to experiment on my own stack, and it was the fastest way to prove the loop end to end. It also let me use GCP, which Dish doesn't standardize on. The pattern is what matters, and that's transferable." |
| "How long did the POC take to build?" | "About 2 weeks — the MCP server infrastructure was already proven from Dynatrace/Snyk. The new work was writing the Firebase MCP and Google Cloud MCP tool definitions, and the agent orchestration logic. The hard part was the security scoping, which was already solved." |
| "How is feature development spec driven?" | "Same discipline as everything else: the requirement is written down as a spec first — what the feature does, the contract, the acceptance criteria — and the implementation is generated from it, then validated against it. No guessing, no implicit requirements. The spec is the contract, and the work either satisfies it or it's not done." |
| "What would you do differently for production?" | "Add cost estimation before provisioning — the agent should estimate monthly cost from the spec before creating anything. Add dependency ordering — some resources depend on others (Firestore must exist before Cloud Functions). Add a human-in-the-loop approval gate for any resource that changes billing." |

---

## Relationship to Other Projects

| Connection | How It Fits |
|-----------|-------------|
| **Project 4: AI Agent Skills & MCP** | This POC extends the same MCP pattern to cloud infrastructure — the fourth domain after code, monitoring, and security |
| **Spring Boot 3 Migration** | Both projects use the same pattern: spec → AI agent → automated execution → human validation |
| **Google Cloud Certification** | This POC validates the certification at a practical level — not just passing a test, but building working infrastructure |
| **The Standard (Azure-focused)** | The POC demonstrates cloud-agnostic MCP automation. The same pattern maps to Azure MCP for AKS, Key Vault, Azure Functions |

---

## Quick Reference for Interviews

| Element | Soundbite |
|---------|-----------|
| **What** | AI agent runs the full AI SDLC loop from a spec: provisions GCP + Firebase, deploys, inspects the UI via DevTools MCP, generates and runs tests |
| **Why** | Service setup took 2-3 days manually — compressed to 5 minutes; verification automated too |
| **How** | Firebase MCP + Google Cloud MCP + Google DevTools MCP with scoped permissions |
| **Key insight** | The same MCP security model (read-only, scoped, auditable) generalizes from monitoring to infrastructure to verification |
| **Principal signal** | AI SDLC — solve the automation pattern once (spec → agent → verify), apply it across every domain |
| **Bridge to The Standard** | Same pattern on Azure — AKS, Key Vault, Azure Functions, plus UI verification via a DevTools-style MCP |