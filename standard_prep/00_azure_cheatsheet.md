# Azure — Story-First Cheatsheet (for someone with AWS, new to Azure)

> Don't bluff Azure depth. Acknowledge it's a new provider, then demonstrate you understand the *patterns* — Principal interviews reward transferable architecture judgment over rote config knowledge.

---

## The Opening (when they ask "what's your Azure experience?")

**Don't:** "I'm very proficient in Azure" (they'll probe and you'll sound thin)

**Do:** *"My deep cloud experience is AWS — ECS, EKS, VPC, IAM, Route53. I've been ramping on Azure for this role. The architecture patterns translate directly: VPC → VNET, IAM Roles → Managed Identity, EKS → AKS, ALB → App Gateway. The differences are naming and portal UX, not architectural concepts. Give me 30 days and I'll be productive."*

---

## The 5 Azure Concepts You MUST Own (not config, architecture decisions)

### 1. Hub-Spoke Networking (vs AWS Transit Gateway)

| AWS | Azure |
|-----|-------|
| Transit Gateway | Hub VNET + VNET Peering |
| VPC | VNET |
| Security Groups | NSGs (stateful, applied at subnet level) |

**Decision framework:**
- Hub VNET = shared services (Firewall, DNS, Logging)
- Spoke VNETs = per-domain or per-environment (AKS, Databases, Management)
- Traffic between spokes goes through Azure Firewall (not direct peering) — enables inspection and audit

**Interview answer:**
> *"Hub-spoke with Azure Firewall in the hub — all spoke-to-spoke traffic goes through the firewall for inspection. AWS Transit Gateway does direct routing; Azure forces traffic through the firewall for governance. It's more restrictive but better for regulated environments like insurance."*

---

### 2. AKS Networking — Azure CNI vs Kubenet (the important choice)

| Choice | When |
|--------|------|
| **Azure CNI** | Enterprise with Private Link, compliance needs, direct pod-to-VNET communication |
| **Kubenet** | Small clusters, IP-constrained, development |
| **Azure CNI Overlay** | Large clusters needing IP efficiency + Azure features (best of both) |

**Key constraint to discuss:** *"Azure CNI consumes VNET IPs per pod. For a cluster with 1000 pods at 30 pods/node that's ~35 nodes and 1000+ IPs consumed from the VNET. Plan your subnet size carefully — a /20 (4096 IPs) is the minimum for any production AKS cluster."*

---

### 3. Private Link + Private Endpoints (your compliance story)

**Why they matter for insurance:** Data never traverses the public internet. Every Azure PaaS (SQL, Key Vault, Storage, Event Hubs) gets a private IP in your VNET.

**Interview answer:**
> *"Every Azure service your pods talk to gets a Private Endpoint in the VNET. Private DNS Zones resolve the service FQDN to the private IP automatically. Your Spring Boot connection string stays the same — DNS handles the routing. No public endpoints, no data exfiltration risk. This is table stakes for insurance compliance."*

---

### 4. Key Vault + AKS Integration (your secret management story)

**Two paths:**

| Method | How | Best for |
|--------|-----|----------|
| **CSI Secret Store** | Mounts secrets as files/volumes | Config files, certificates |
| **Workload Identity** | Pod authenticates directly via Azure AD | In-app access (Spring Cloud Azure) |

**Interview answer:**
> *"I'd use CSI Secret Store for secrets at deployment time and Workload Identity for runtime access from Spring Boot. No secrets ever hit Kubernetes etcd. Managed Identity means no service principal secrets to rotate. This follows zero-trust principles — every pod has exactly the permissions it needs, nothing more."*

---

### 5. Azure Firewall + UDR (your egress control story)

**The pattern:** UDR on AKS subnet forces all egress through Azure Firewall. Firewall rules allow only necessary FQDNs (mcr.microsoft.com, API endpoints, etc.). Everything else is denied.

**Why this matters:** *"Without forced tunneling, AKS nodes can reach the internet directly. For insurance, every egress must be auditable. Azure Firewall gives you that audit trail. It's also where you'd block data exfiltration and enforce compliance policies."*

---

## Your Credible Answer for "Tell me about an Azure issue"

You don't have a real Azure incident. That's fine. Don't fake one. Instead, describe a **failure mode you'd prevent** — shows forward thinking:

> *"I haven't had a production Azure incident yet, but here's a failure mode I'd prevent on day one:*
>
> *AKS node pool runs out of IPs in its subnet because Azure CNI assigned pod IPs from the VNET range — a common trap. New pods can't schedule, the cluster degrades silently, and by the time you notice, customer-impacting services are failing.*
>
> *Prevention: Either use Azure CNI Overlay (pods get IPs from a separate CIDR, not the VNET) or allocate a /19 minimum for the AKS subnet. And set a Prometheus alert on IP utilization in the subnet. This exact pattern causes production incidents at scale — I'd catch it in the design review before it reaches prod."*

---

## The Ramp-Up Plan (if they push on lack of Azure experience)

> *"Here's my 30-day plan to be productive:*
> - **Week 1:** Deploy a Spring Boot app on AKS from scratch — VNET, App Gateway, Key Vault, Private Endpoints. Hands-on, not reading docs.
> - **Week 2:** Set up the CI/CD pipeline — Azure DevOps, Terraform provisioning, Snyk scan. Get one service all the way to production.
> - **Week 3:** Shadow the on-call rotation. Understand the observability stack and common failure patterns specific to this Azure environment.
> - **Week 4:** First architecture review — I'd participate, not lead. By the second one, I'd be driving it."

---

## Quick Reference: AWS → Azure Mapping (from aws_to_azure_mapping.md)

| AWS | Azure | Key Difference |
|-----|-------|---------------|
| VPC | VNET | Same concept |
| Subnet | Subnet | Same |
| Security Group | NSG | SG is stateful / instance-level; NSG stateful / subnet-level |
| ALB / NLB | App Gateway / LB | App GW is L7 + WAF built-in |
| IAM Role | Managed Identity | Same purpose, Azure ties it to AAD |
| EKS | AKS | Same — managed K8s |
| ECR | ACR | Container registry |
| RDS | Azure SQL / PostgreSQL | Same |
| KMS | Key Vault | Key Vault also handles secrets + certificates |
| Route53 | Azure DNS / Private DNS Zone | Private DNS Zones for endpoints |
