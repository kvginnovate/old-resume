# Project 14: GCP + Firebase MCP — Zero-Touch Infrastructure Auto-Provisioning POC

> **Proof of Concept:** An AI agent that provisions GCP infrastructure, Firebase projects, and backend services end-to-end through MCP servers — no console clicks, no manual config, no Terraform apply. The agent takes a spec and delivers a running environment.

---

## Headline

*"I built a proof of concept where an AI agent, through Google Cloud MCP and Firebase MCP, provisions a complete cloud environment from a single spec — GCP project, Firestore collections, Authentication config, Cloud Functions, API Gateway, and Cloud Run services — without any human touching the console. The agent handles everything: infrastructure, auth, backend, and deployment."*

---

## The Problem (Business Context)

Every new microservice at Dish followed the same cycle: open a ticket to the platform team, wait for a GCP project to be created, wait for Firestore to be configured, wait for Auth to be set up, wait for CI/CD pipelines, then finally start coding. The setup process took **2-3 days per service** — all manual, all repetitive, and the platform team was the bottleneck.

I had already automated code generation (Spring Boot 3 migration, Sling TV) and defect remediation (Dynatrace/Snyk MCP). The next frontier: **infrastructure itself.** If an AI agent could provision cloud infrastructure from a spec, the same pattern that compressed bug fixes from days to hours could compress service setup from days to minutes.

Additionally, I hold a **Google Cloud Professional Data Engineer** certification. I wanted to prove that the MCP + agent playbook I built for Dish's internal tooling (Dynatrace, Snyk, GitLab, Jira) was stack-agnostic — it works on GCP too.

---

## What I Did (Strategy, Not Just Code)

**1. I designed the MCP server mesh for GCP.** The POC used two MCP servers in concert:

- **Firebase MCP:** Reads/writes Firestore collections, manages Firebase Auth (users, custom claims, providers), deploys Cloud Functions, configures Firebase App Hosting.
- **Google Cloud MCP:** Queries and provisions GCP resources — Cloud Storage buckets, BigQuery datasets, Cloud Run services, IAM policies, Cloud Scheduler jobs, Secret Manager entries.

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

---

## The Outcome

- **Service setup: 2-3 days → 5 minutes** from spec input to running environment
- **Zero console clicks** — everything provisioned through MCP-scoped agent calls
- **Repeatable, auditable, version-controlled** — the spec IS the infrastructure definition
- Proved that the MCP + agent playbook works on **any cloud** (Dish's AWS + internal → GCP)
- Leveraged my **Google Cloud Professional Data Engineer** certification for deep GCP knowledge
- **Iteration loop** (validate → diff → update → rollback) made the POC production-ready in concept, not just a one-shot demo

---

## Principal Signal

*Infrastructure is the next automation frontier. I already proved that AI agents can fix bugs, remediate vulnerabilities, and migrate code. This POC proves they can provision the infrastructure **before the code is written.** The pattern is the same: spec → agent → MCP server → environment. The difference is the domain, not the architecture. The MCP security model I designed for Dynatrace/Snyk generalizes to any cloud service — that's the Principal-level insight: solve the automation pattern once, apply it everywhere.*

---

## Bridge to Any Company

*"Your company probably has a platform team that's bottlenecked on service setup — every new microservice requires 2-3 days of manual infrastructure provisioning. The GCP/Firebase MCP POC proves that an AI agent can do this from a spec in 5 minutes, with full audit trails and rollback capability. The same pattern works on Azure, AWS, or any cloud with an API. The question isn't 'can this work?' — the POC already answers that. The question is 'how do you make the spec the source of truth and the agent the executor?' That's the architecture conversation I want to have."*

---

## Watchpoints

| Question | Your Anchor |
|----------|------------|
| "What stops the agent from provisioning something expensive?" | "Same security model as Dynatrace/Snyk — scoped MCP permissions. The agent can create but never delete billing resources, never modify billing alarms, never escalate its own permissions. The spec itself is version-controlled and reviewed before execution." |
| "How does this differ from Terraform or Pulumi?" | "Terraform/Pulumi are Infrastructure-as-Code — a human writes the config, a human runs the apply. The MCP agent is **AI-driven infrastructure-as-code** — the agent writes the config from a spec, validates it, provisions it, and verifies it. The human reviews the plan, not the code. It's the same shift from 'AI writes code, human reviews' to 'AI provisions infra, human reviews the plan.'" |
| "Did you use this in production?" | "It was a POC — not production. The purpose was to prove the pattern works. The next step would be adding approval gates: agent generates the plan, human reviews and approves, agent executes. That's the same governance model I used for the Spring Boot 3 migration." |
| "What about state management and drift detection?" | "The iteration loop handles this. Validate compares current state against spec. Diff shows what's drifted. Update applies only the delta. This is the same pattern as Kubernetes reconciliation — the spec is the desired state, the agent is the reconciler." |
| "Why GCP when Dish uses AWS?" | "Two reasons: (1) I hold a GCP Professional Data Engineer certification — I wanted to prove the MCP pattern is cloud-agnostic. (2) The Standard runs on Azure. The POC demonstrates that the agent + MCP pattern works on any cloud, and I can adapt it to Azure within weeks." |
| "How long did the POC take to build?" | "About 2 weeks — the MCP server infrastructure was already proven from Dynatrace/Snyk. The new work was writing the Firebase MCP and Google Cloud MCP tool definitions, and the agent orchestration logic. The hard part was the security scoping, which was already solved." |
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
| **What** | AI agent provisions GCP + Firebase from a single spec YAML |
| **Why** | Service setup took 2-3 days manually — compressed to 5 minutes |
| **How** | Firebase MCP + Google Cloud MCP with scoped permissions |
| **Key insight** | The same MCP security model (read-only, scoped, auditable) generalizes from monitoring to infrastructure |
| **Principal signal** | Solve the automation pattern once, apply it across domains |
| **Bridge to The Standard** | Same pattern on Azure — AKS, Key Vault, Azure Functions via a custom Azure MCP |