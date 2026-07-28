# Study & Preparation Plan — Principal Software Engineer V (IBTE) at The Standard

## Target Role Summary
- **Company:** The Standard
- **Role:** Principal Software Engineer V – IBTE
- **Location:** On-site, Bengaluru, India (Hybrid)
- **Experience Required:** 14+ years

---

## Priority Matrix

| # | Topic | Priority | Effort | Current Level |
|---|-------|----------|--------|---------------|
| 1 | Azure Cloud, AKS & Networking | HIGH | 2-3 weeks | Low — needs significant study |
| 2 | Confluent Platform & Apache Flink | HIGH | 2 weeks | Medium — Kafka yes, Flink/Confluent gaps |
| 3 | Kong / Kong Konnect | MEDIUM | 1 week | None — new area |
| 4 | Architecture Case Studies & Whiteboarding | MEDIUM | 1 week | High — needs structured prep |
| 5 | Terraform for Azure | MEDIUM | 1 week | Medium — new provider |
| 6 | Leadership Stories (STAR format) | MEDIUM | 3-4 days | High — needs structuring |
| 7 | Spring Boot Advanced (Loom, native, Azure) | LOW | 3-4 days | High — minor gaps |
| 8 | Testing & Quality Gates | LOW | 2-3 days | High — review only |
| 9 | Database Integration | LOW | 2 days | High — review only |

---

## Week-by-Week Study Plan

### Week 1-2: Azure Cloud & Networking (Foundation)
- Azure fundamentals (if not certified)
- AKS deep dive: deployment, scaling, networking, ingress
- Azure Networking: VNET, Subnet, NSG, NAT, Private Link, Private Endpoint
- Application Gateway vs Load Balancer
- Azure Firewall, Private DNS Zones
- Azure Key Vault: secrets, certificates, RBAC
- Azure DevOps Pipelines (YAML CI/CD)
- Hands-on: Deploy Spring Boot on AKS with VNET

### Week 3: Confluent Platform & Apache Flink
- Confluent Platform architecture
- Schema Registry (Avro, Protobuf, compatibility modes)
- Kafka Connect (source/sink connectors, SMTs, custom connectors)
- Apache Flink SQL, DataStream API
- Flink UDFs (Scalar, Table, Aggregate)
- Flink + Kafka integration
- Hands-on: Flink SQL job consuming Kafka topic

### Week 4: Kong, Terraform & Architecture Prep
- Kong Gateway architecture, plugins, routes, services
- Kong Konnect (SaaS control plane)
- Kong Ingress Controller on Kubernetes
- Terraform azurerm provider
- Terraform modules for AKS, VNET, Key Vault
- Remote state management (Azure Blob)
- Architecture whiteboarding practice

### Week 5: Leadership, Behavioral & Mock Interviews
- Structure STAR stories from Dish experience
- Practice system design problems (45-min format)
- Mock behavioral interviews
- Review Spring Boot advanced topics
- Final review of all Q&A documents

---

## Recommended Resources

| Topic | Resource |
|-------|----------|
| Azure | Microsoft Learn (free), AZ-305 Learning Path |
| AKS | Microsoft Learn AKS modules |
| Confluent | Confluent Developer tutorials, Confluent Certified Developer |
| Flink | Apache Flink official docs, Ververica Flink Training |
| Kong | Kong Academy (free courses) |
| Terraform | HashiCorp Learn, azurerm provider docs |
| System Design | "Designing Data-Intensive Applications" — Martin Kleppmann |
| Behavioral | "The Staff Engineer's Path" — Tanya Reilly |

---

## Document Index

| File | Topic |
|------|-------|
| `01_architecture_ownership_qa.md` | Architecture Ownership Q&A |
| `02_api_engineering_springboot_qa.md` | API Engineering & Spring Boot Q&A |
| `03_kafka_confluent_flink_qa.md` | Kafka, Confluent Platform & Flink Q&A |
| `04_azure_networking_devops_qa.md` | Azure Cloud, Networking & DevOps Q&A |
| `05_kong_api_gateway_qa.md` | Kong / Kong Konnect Q&A |
| `06_testing_quality_reliability_qa.md` | Testing, Quality & Reliability Q&A |
| `07_data_database_integration_qa.md` | Data & Database Integration Q&A |
| `08_leadership_behavioral_qa.md` | Leadership & Behavioral Q&A |
| `09_terraform_azure_qa.md` | Terraform for Azure Q&A |
