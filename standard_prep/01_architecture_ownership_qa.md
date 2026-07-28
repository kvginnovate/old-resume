# Architecture Ownership — Questions & Answers

## Concepts & Theory

### Q1: What does "owning end-to-end solution architecture" mean in practice?

**Answer:**
It means being responsible for the entire technical solution lifecycle — from requirements gathering through design, implementation guidance, deployment, and operational readiness. Specifically:

- **Design:** Defining component boundaries, communication patterns (sync vs async), data flows, and integration points
- **Documentation:** Creating architecture diagrams (C4 model), ADRs (Architecture Decision Records), integration contracts
- **Governance:** Ensuring all teams follow the defined patterns, reviewing PRs for architectural compliance
- **Quality:** Defining non-functional requirements (NFRs) like latency budgets, throughput targets, availability SLAs
- **Operational Readiness:** Ensuring observability (metrics, logs, traces), alerting, runbooks, and disaster recovery plans are in place

---

### Q2: What are Architecture Decision Records (ADRs)? How do you use them?

**Answer:**
ADRs are lightweight documents that capture important architectural decisions along with their context and consequences.

**Structure:**
```
# ADR-001: Use Kafka for inter-service communication

## Status: Accepted

## Context
- We have 15+ microservices that need async communication
- Current REST-based sync calls create tight coupling and cascade failures
- We need guaranteed delivery and replay capability

## Decision
Use Apache Kafka as the primary inter-service messaging backbone.

## Consequences
- (+) Decoupled services, independent scaling
- (+) Event replay capability for debugging and recovery
- (+) Natural audit trail
- (-) Added infrastructure complexity
- (-) Eventual consistency — need to handle stale reads
- (-) Team needs Kafka training
```

**How I use them:**
- Every significant architectural decision gets an ADR
- Stored in the repo (docs/adrs/) so they evolve with code
- Referenced during architecture reviews
- Help new team members understand "why" behind decisions

---

### Q3: How do you define and enforce design guardrails across multiple teams?

**Answer:**
Design guardrails are constraints that prevent teams from making harmful architectural decisions while allowing freedom within boundaries.

**My approach:**

1. **Document guardrails clearly:**
   - API design standards (naming conventions, error formats, pagination)
   - Security requirements (authentication method, data classification)
   - Technology choices (approved databases, messaging systems, languages)
   - Performance budgets (max latency per tier, connection pool sizes)

2. **Automate enforcement:**
   - CI/CD pipeline checks (linting for API specs, dependency scanning)
   - Architecture fitness functions (automated tests that verify architectural properties)
   - PR templates requiring architecture review for certain changes

3. **Review processes:**
   - Architecture review board for cross-cutting concerns
   - Design reviews before sprint starts for significant features
   - Post-implementation reviews for learning

4. **Communication:**
   - Internal tech radar (adopt, trial, assess, hold)
   - Engineering blog posts explaining rationale
   - Regular architecture guild meetings

---

### Q4: How do you lead an architecture review? What do you look for?

**Answer:**

**Process:**
1. Author presents design document (problem, proposed solution, alternatives considered)
2. Review against NFRs: scalability, security, reliability, maintainability, cost
3. Identify risks and mitigations
4. Decision: approve, approve with conditions, or redesign

**What I look for:**
- **Coupling:** Are services appropriately decoupled? Can they evolve independently?
- **Data ownership:** Is each service the single owner of its data? No shared databases?
- **Failure modes:** What happens when downstream services are down? Circuit breakers? Fallbacks?
- **Scalability:** Can the design handle 10x traffic? What's the bottleneck?
- **Security:** Authentication, authorization, data encryption (at rest and in transit)
- **Observability:** How will we monitor this? What alerts do we need?
- **Operational cost:** Cloud resource estimation, scaling policies
- **Migration path:** How do we roll this out without downtime?

---

### Q5: How do you make architectural trade-off decisions?

**Answer:**

**Framework I use:**

1. **Identify the dimensions in tension** (e.g., consistency vs availability, simplicity vs flexibility, cost vs performance)

2. **Quantify impact:**
   - What's the cost of being wrong?
   - Is this reversible?
   - What's the timeline impact?

3. **Consider constraints:**
   - Team capability and learning curve
   - Timeline and budget
   - Existing infrastructure
   - Organizational goals

4. **Document the trade-off** (in ADR):
   - What we're optimizing for
   - What we're accepting as a trade-off
   - Under what conditions we'd revisit

**Example:**
> "We chose eventual consistency (Kafka-based async) over strong consistency (synchronous REST calls) because our SLA allows 5-second staleness, but requires 99.9% availability. Synchronous calls would create a cascade failure risk across 15 services."

---

### Q6: What is the C4 model and how do you use it for architecture documentation?

**Answer:**
C4 is a hierarchical approach to diagramming software architecture at 4 levels of zoom:

1. **Context (Level 1):** System boundary — how the system interacts with users and external systems
2. **Container (Level 2):** High-level technology choices — applications, databases, message brokers
3. **Component (Level 3):** Inside a container — major structural building blocks (controllers, services, repositories)
4. **Code (Level 4):** Class-level detail (rarely needed)

**How I use it:**
- Level 1 & 2 for stakeholder communication and onboarding
- Level 2 & 3 for engineering design discussions
- Maintained as code (PlantUML/Structurizr) in the repo
- Updated as part of feature development

---

### Q7: How do you ensure implementation aligns with enterprise architecture?

**Answer:**

1. **Alignment checks:**
   - Map solution to enterprise reference architecture
   - Verify technology choices against enterprise tech radar
   - Ensure security patterns match enterprise security framework (zero-trust, OAuth2 provider)

2. **Integration patterns:**
   - Use enterprise-standard API gateway (Kong)
   - Follow enterprise event schema standards (Schema Registry)
   - Integrate with enterprise observability stack

3. **Governance:**
   - Present designs to enterprise architecture board for cross-domain impacts
   - Flag deviations early with justification
   - Contribute back patterns that could benefit other teams

4. **Compliance:**
   - Data residency requirements
   - Audit logging standards
   - Encryption standards (TLS 1.3, AES-256)

---

## Scenario-Based Questions

### Q8: You inherit a system with no architecture documentation, 20+ microservices, and frequent production issues. How do you approach this?

**Answer:**

**Phase 1 — Understand (Week 1-2):**
- Map all services from deployment configs (Kubernetes manifests, CI/CD pipelines)
- Identify communication patterns from service mesh/logs (who calls whom)
- Document current state as-is architecture (C4 Level 2)
- Interview team leads for tribal knowledge
- Analyze production incidents for patterns (which services fail, correlation)

**Phase 2 — Stabilize (Week 3-4):**
- Add observability where missing (distributed tracing, health checks)
- Identify the top 3 reliability issues and fix them
- Introduce circuit breakers for fragile integrations
- Set up on-call runbooks for common failures

**Phase 3 — Govern (Month 2+):**
- Write ADRs for existing decisions (document the "why")
- Define target architecture and migration roadmap
- Introduce architecture reviews for new work
- Gradually refactor highest-risk areas

---

### Q9: Two teams want to solve the same problem differently (e.g., one wants REST, other wants Kafka). How do you handle it?

**Answer:**

1. **Understand the context:** Each team may have different constraints (latency requirements, data volumes, team expertise)

2. **Facilitate a joint design session:**
   - Define the problem clearly (what are the actual requirements?)
   - Evaluate both options against NFRs
   - Identify if both can coexist or if we need one standard

3. **Decision criteria:**
   - Does the enterprise already have a standard for this pattern?
   - What's the operational cost of supporting both?
   - Is this a one-way door (hard to reverse) or two-way door?

4. **Document and communicate:**
   - ADR explaining the decision and rationale
   - If we choose one, provide migration support to the other team
   - If both are valid for different contexts, document when to use which

**Key principle:** Consistency has value, but not infinite value. Sometimes two solutions are correct for genuinely different contexts.

---

### Q10: How do you balance innovation (new tech) vs stability (proven tech) in architecture decisions?

**Answer:**

**Framework:**
- **Core path (must work):** Use proven, boring technology. This is where reliability matters most.
- **Edge/experimental (can fail gracefully):** Okay to try new tech with proper fallback.

**Evaluation criteria for new technology:**
1. Is it solving a real problem our current stack can't?
2. Does the team have capacity to learn and support it?
3. Is it production-ready (not just POC/alpha)?
4. What's the exit strategy if it doesn't work?
5. Does it align with enterprise direction?

**Practical approach:**
- Maintain a tech radar (Adopt / Trial / Assess / Hold)
- Time-boxed POCs before committing
- One team pilots, then broader rollout
- Never introduce new tech on a critical path without a fallback

---

### Q11: How do you design for observability from the start?

**Answer:**

**Three pillars + extras:**

1. **Metrics (Prometheus/Dynatrace):**
   - RED method for services: Rate, Errors, Duration
   - USE method for resources: Utilization, Saturation, Errors
   - Business metrics: orders/sec, conversion rate

2. **Logs (ELK/Azure Monitor):**
   - Structured logging (JSON)
   - Correlation IDs across service boundaries
   - Log levels enforced (no INFO spam in production)

3. **Traces (distributed tracing):**
   - OpenTelemetry instrumentation
   - Trace context propagation across REST and Kafka
   - Span annotations for business context

4. **Alerting:**
   - SLO-based alerting (burn rate)
   - Runbook links in every alert
   - Escalation policies

5. **Dashboards:**
   - Service-level dashboard (golden signals)
   - Business dashboard (KPIs)
   - Infrastructure dashboard (cluster health)

**Architecture decisions for observability:**
- Standardize on OpenTelemetry across all services
- Centralized logging with retention policies
- Service mesh for automatic metrics/tracing (where applicable)
- Health check endpoints (liveness + readiness) in every service

---

### Q12: A new feature requires changes across 5 microservices. How do you coordinate the architecture?

**Answer:**

1. **Design phase:**
   - Create a cross-service design document showing the full data flow
   - Identify API contract changes needed (OpenAPI specs)
   - Define rollout order (which service changes first?)
   - Plan for backward compatibility during transition

2. **Coordination:**
   - Single architecture owner (me) for the cross-cutting concern
   - Feature flags to enable incremental rollout
   - Contract-first development (agree on APIs before implementation)
   - Shared integration test environment

3. **Rollout strategy:**
   - Deploy changes behind feature flags (dark launch)
   - Roll out producer before consumer (for Kafka)
   - Roll out backward-compatible API changes first, then clients
   - Canary deployment for each service

4. **Validation:**
   - End-to-end integration tests covering the full flow
   - Monitoring for error rate spikes during rollout
   - Rollback plan for each service independently
