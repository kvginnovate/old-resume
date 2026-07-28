# AWS → Azure Service Mapping — Principal Engineer Quick Reference

> Your resume lists AWS (S3, DynamoDB) and GCP. If the role requires Azure, they may ask about equivalents or expect you to adapt. This covers what **actually comes up** in interviews.

---

## The 15 Most Common AWS → Azure Mappings

| Category | AWS | Azure | What it is | Interview One-Liner |
|---|---|---|---|---|
| **Compute** | EC2 | Virtual Machines (VMs) | Virtual servers in the cloud | "EC2 → Azure VMs. Same concept — provision VMs, choose OS, scale up/down." |
| **Compute (containers)** | ECS / EKS | AKS (Azure Kubernetes Service) | Managed Kubernetes | "EKS → AKS. Managed K8s. I've used Rancher on-prem — same K8s concepts apply." |
| **Serverless** | Lambda | Azure Functions | Event-driven, pay-per-execution | "Lambda → Functions. Write code, trigger on events, no servers to manage." |
| **Object Storage** | S3 | Blob Storage | Store files, images, backups, logs | "S3 → Blob Storage. Object storage with tiered access tiers — hot, cool, archive." |
| **NoSQL Database** | DynamoDB | Cosmos DB | Fully managed NoSQL, single-digit-ms latency | "DynamoDB → Cosmos DB. Multi-model — key-value, document, graph, column-family. Supports Cassandra/MongoDB APIs." |
| **Relational DB** | RDS (PostgreSQL/MySQL) | Azure SQL / PostgreSQL Flexible Server | Managed relational databases | "RDS → Azure SQL or PostgreSQL Flexible Server. Managed, auto-backup, read replicas." |
| **Caching** | ElastiCache (Redis) | Azure Cache for Redis | In-memory cache | "ElastiCache → Azure Redis Cache. Same Redis — different management plane." |
| **Message Queue** | SQS | Azure Queue Storage | Simple message queuing | "SQS → Queue Storage. At-least-once delivery, visibility timeout, dead-letter queue." |
| **Event Streaming** | Kinesis | Event Hubs | High-throughput event ingestion | "Kinesis → Event Hubs. Millions of events per second, partitioned, Kafka-compatible protocol." |
| **Pub/Sub** | SNS | Azure Service Bus / Event Grid | Publish-subscribe messaging | "SNS → Service Bus (enterprise) or Event Grid (event routing). Topics, subscriptions, filtering." |
| **API Gateway** | API Gateway | Azure API Management (APIM) | Manage, secure, and monitor APIs | "API Gateway → API Management. Route, throttle, authenticate, version APIs." |
| **Load Balancer** | ALB / NLB | Azure Load Balancer / Application Gateway | Distribute traffic across instances | "ALB → Application Gateway. Layer 7 routing, SSL termination, WAF." |
| **DNS** | Route 53 | Azure DNS / Traffic Manager | DNS management and traffic routing | "Route 53 → Azure DNS + Traffic Manager. DNS hosting + global traffic routing." |
| **Monitoring** | CloudWatch | Azure Monitor | Metrics, logs, alerts | "CloudWatch → Monitor. Metrics, logs, alerts, dashboards. Dynatrace sits on top for APM." |
| **CI/CD** | CodePipeline / CodeBuild | Azure DevOps / GitHub Actions | Build and deploy pipelines | "CodePipeline → Azure DevOps. Git repos, CI/CD pipelines, artifact management." |
| **Auth / Identity** | Cognito / IAM | Azure AD (Entra ID) / Managed Identity | Authentication and authorization | "Cognito → Azure AD (now Entra ID). For apps. IAM → Managed Identity or RBAC." |

---

## If They Ask About Your Cloud Experience (and You Know AWS, Not Azure)

**Don't pretend you know Azure deeply. Say this:**

> *"My hands-on experience is primarily with AWS and some GCP. But I understand cloud architecture at the pattern level — compute, storage, networking, IAM, monitoring — and those patterns map directly to Azure. The service names change, but the concepts don't. Give me two weeks and I'll be productive on Azure."*

This is honest and shows adaptability. At Principal level, they're hiring for architecture thinking, not service-name memorization.

---

## If They Ask Azure-Specific Questions — What to Expect

### Q: Tell me what you know about Azure DevOps.

> *"Azure DevOps is the equivalent of GitLab CI/CD. It has Boards (backlog/kanban), Repos (git), Pipelines (CI/CD), Test Plans, and Artifacts (package manager). I've used GitLab — the CI/CD concepts are the same: trigger pipeline on commit, run tests, scan, deploy. The YAML syntax is different but the logic is identical."*

### Q: How does Azure handle IAM compared to AWS?

> *"AWS has IAM policies attached to users, groups, or roles. Azure uses RBAC (Role-Based Access Control) with built-in or custom roles attached to managed identities or service principals. The concept is the same — least privilege, scoped permissions. Azure also has Azure AD for human identity, which is deeper than AWS Cognito."*

### Q: Azure Functions vs AWS Lambda — have you used either?

> *"I've used Lambda in a small project (DISH App Store). Functions and Lambda are nearly identical — trigger-based, auto-scale, pay-per-execution. The main difference is Azure Functions have more built-in bindings (Cosmos DB, Blob, Queue) and better integration with the Azure ecosystem."*

### Q: How would you design a microservices deployment on Azure?

> *"AKS for orchestration (exactly like EKS/Rancher K8s). Azure API Management for the gateway. Cosmos DB for NoSQL needs. Azure SQL for relational. Service Bus for event-driven communication. Azure Monitor + Dynatrace for observability. Azure DevOps for CI/CD. The patterns — API gateway, circuit breakers, event-driven, BFF — are the same regardless of cloud provider."*

---

## Comparison — Service-by-Service

### Compute

| AWS | Azure | What to Say |
|---|---|---|
| EC2 | Virtual Machines (VMs) | "Same thing. Provision VMs, manage OS, scale sets for availability." |
| EC2 Auto Scaling | VM Scale Sets | "Auto-scale VMs based on load. Same concept." |
| ECS (Docker) | Container Instances | "Run containers without K8s. Simpler, less flexible." |
| EKS (Kubernetes) | AKS (Azure Kubernetes Service) | "Managed K8s — same Kubernetes API, different management plane." |
| Lambda | Azure Functions | "Serverless functions. Same — trigger on event, auto-scale, pay per execution." |
| Elastic Beanstalk | App Service | "PaaS — deploy code, Azure manages the infra. For simpler apps." |

### Storage

| AWS | Azure | What to Say |
|---|---|---|
| S3 | Blob Storage | "Object storage. Same tiers: hot, cool, archive. Different naming (bucket → container)." |
| EBS (block) | Managed Disks | "Block storage attached to VMs. Same — SSD, HDD tiers." |
| EFS (file) | Azure Files | "Managed file share accessible via SMB/NFS. Same." |
| S3 Glacier | Blob Archive Tier | "Cold storage for backups. Lower cost, slower retrieval." |

### Databases

| AWS | Azure | What to Say |
|---|---|---|
| RDS | Azure SQL / PostgreSQL Flexible Server | "Managed relational DB. Same — backups, replicas, automated patching." |
| DynamoDB | Cosmos DB | "NoSQL. DynamoDB is simpler. Cosmos DB is multi-model — supports Document, Graph, Key-Value, Column-Family. Also has Cassandra and MongoDB API compatibility." |
| ElastiCache (Redis) | Azure Cache for Redis | "Same Redis. Different management console. Same `SET`/`GET` commands." |
| Aurora | Azure Database for MySQL/PostgreSQL | "High-performance managed SQL. Aurora is AWS-specific. Azure has equivalent performance tiers." |

### Messaging

| AWS | Azure | What to Say |
|---|---|---|
| SQS | Queue Storage | "Simple queue — at-least-once, visibility timeout, DLQ. Same pattern." |
| SNS | Service Bus Topics / Event Grid | "Pub/sub. SNS is simpler. Service Bus has more enterprise features (sessions, transactions, dedup)." |
| Kinesis | Event Hubs | "High-throughput event ingestion. Kinesis is shard-based. Event Hubs is partition-based. Both support Kafka protocol now." |
| MQ | Service Bus | "Message broker for enterprise patterns. Queues, topics, dead-letter, scheduled delivery." |

### Networking

| AWS | Azure | What to Say |
|---|---|---|
| VPC | VNet | "Virtual network. Subnets, route tables, network security groups. Same concepts." |
| CloudFront | CDN (Azure Front Door) | "CDN + global load balancer. CloudFront serves content. Front Door adds WAF, SSL termination, routing." |
| Route 53 | Azure DNS / Traffic Manager | "DNS hosting + global traffic routing. Route 53 does both. Azure separates DNS from Traffic Manager." |
| ALB / NLB | App Gateway / Load Balancer | "Application Gateway = ALB (Layer 7). Load Balancer = NLB (Layer 4)." |
| Direct Connect | ExpressRoute | "Dedicated private connection from on-prem to cloud. Same." |
| VPN Gateway | VPN Gateway | "Site-to-site VPN over the internet. Same." |

### Monitoring & DevOps

| AWS | Azure | What to Say |
|---|---|---|
| CloudWatch | Azure Monitor | "Metrics, logs, alerts. CloudWatch has Logs and Metrics together. Monitor has Log Analytics + Metrics." |
| X-Ray | Application Insights | "Distributed tracing. Same as Dynatrace APM. Azure's native option." |
| CloudTrail | Azure Activity Log | "Audit log of all API calls made on your account. Who did what, when." |
| CodePipeline / CodeBuild | Azure DevOps Pipelines | "CI/CD. YAML or visual editor. Same workflow: trigger → build → test → deploy." |
| CloudFormation | ARM Templates / Bicep | "Infrastructure as Code. CloudFormation (JSON/YAML). ARM (JSON) or Bicep (simpler DSL)." |
| Secrets Manager | Key Vault | "Store secrets, keys, certificates. Managed rotation, access policies." |

### Identity

| AWS | Azure | What to Say |
|---|---|---|
| IAM | Azure RBAC + Managed Identity | "IAM for service permissions. Azure has RBAC for role assignments + Managed Identities for automatic credential management." |
| Cognito | Azure AD B2C / Entra ID | "Cognito for app user management. Azure AD B2C for customer identity. Entra ID for employee identity." |
| Organizations | Management Groups | "Multi-account/management. Root → OUs → Accounts = Root → Management Groups → Subscriptions." |

---

## The Three Azure Concepts Most Interviews Ask

### 1. Azure AD / Entra ID

> *"Azure AD is the identity and access management service. It's not just a directory — it handles authentication (OAuth2, SAML, OpenID Connect), authorization (RBAC), and conditional access policies. At Dish, I used Okta + Cognito. Azure AD (now Entra ID) is the Azure equivalent — deeper integration with the Azure ecosystem."*

### 2. Azure DevOps

> *"It's a full SDLC platform: Boards (backlog/kanban), Repos (git), Pipelines (CI/CD), Test Plans, Artifacts (package feeds). I've used GitLab CI/CD extensively — same concepts. The YAML-based pipeline syntax is similar. Key difference: Azure DevOps has built-in integration with AKS, Azure Functions, and App Service for deployment."*

### 3. Azure Resource Manager (ARM / Bicep)

> *"ARM templates are the IaC tool for Azure — JSON-based, declarative, idempotent. Bicep is the newer DSL that compiles to ARM — looks more readable, like Terraform for Azure. I'm familiar with the concept from CloudFormation. At Principal level, what matters is understanding that resources should be defined declaratively, version-controlled, and deployed via CI/CD."*

---

## Quick Reference Card

| Need | AWS | Azure |
|---|---|---|
| VM | EC2 | Virtual Machines |
| Serverless | Lambda | Functions |
| Containers | EKS | AKS |
| Object Storage | S3 | Blob Storage |
| NoSQL | DynamoDB | Cosmos DB |
| SQL | RDS | Azure SQL / Postgres Flexible |
| Cache | ElastiCache | Redis Cache |
| Queue | SQS | Queue Storage |
| Event Stream | Kinesis | Event Hubs |
| Pub/Sub | SNS | Service Bus / Event Grid |
| API Gateway | API Gateway | API Management |
| Load Balancer | ALB | App Gateway |
| CI/CD | CodePipeline | Azure DevOps |
| Monitoring | CloudWatch | Monitor |
| Auth | Cognito / IAM | Entra ID / RBAC |
| IaC | CloudFormation | ARM / Bicep |
| Secrets | Secrets Manager | Key Vault |

---

## The One-Liner for "You Only Know AWS"

> *"My cloud architecture experience is on AWS and GCP. But cloud patterns are cloud patterns — compute, storage, networking, IAM, monitoring. The service name changes, but the architecture doesn't. I've mapped the AWS services I know to their Azure equivalents as part of my preparation for this interview, and the concepts transfer directly."*

This turns a potential weakness into evidence of preparation and adaptability.
