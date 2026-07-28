# Azure Cloud, Networking & DevOps — Questions & Answers

## Azure Kubernetes Service (AKS)

### Q1: What is AKS and how does it differ from self-managed Kubernetes?

**Answer:**

AKS (Azure Kubernetes Service) is a managed Kubernetes offering where Azure handles:
- Control plane (API server, etcd, scheduler, controller manager)
- Upgrades and patching of control plane
- Health monitoring and auto-repair of nodes
- Integration with Azure AD, networking, monitoring

**What you still manage:**
- Worker node pools (size, scaling policies)
- Application deployments and configurations
- Networking policies and ingress
- Monitoring and alerting for applications
- Security policies and RBAC

**Key AKS features:**
| Feature | Description |
|---------|-------------|
| Node Pools | Multiple pools with different VM sizes (system + user pools) |
| Cluster Autoscaler | Automatically adds/removes nodes based on pending pods |
| Virtual Nodes | Burst to Azure Container Instances (serverless) |
| Azure CNI | Native VNET integration (pods get VNET IPs) |
| Azure AD Integration | RBAC backed by Azure AD groups |
| Managed Identity | No service principal secrets needed |
| Azure Policy | Enforce governance (e.g., no privileged containers) |


---

### Q2: How do you design AKS networking? Explain Azure CNI vs Kubenet.

**Answer:**

**Two networking models:**

| Aspect | Kubenet | Azure CNI |
|--------|---------|-----------|
| Pod IP source | Private CIDR (NAT to node IP) | VNET subnet (real IPs) |
| Pod-to-VNET communication | Via NAT | Direct (no NAT) |
| Performance | Slightly lower (extra hop) | Better (native) |
| IP consumption | Low (only node IPs from VNET) | High (pod IPs from VNET) |
| Max pods per node | 110 (default) | 30 (default, configurable to 250) |
| Integration with Azure services | Requires UDR | Direct Private Endpoint access |
| Use case | Small clusters, IP-constrained | Enterprise, Private Link, compliance |

**Azure CNI Overlay (newer option):**
- Pods get IPs from a separate overlay CIDR (not VNET)
- Reduces VNET IP consumption like Kubenet
- But still has native Azure networking features
- Best of both worlds for large clusters

**Network design for enterprise AKS:**
```
VNET: 10.0.0.0/16
├── AKS Subnet: 10.0.0.0/20 (4096 IPs for nodes + pods)
├── App Gateway Subnet: 10.0.16.0/24
├── Private Endpoint Subnet: 10.0.17.0/24
├── Azure Firewall Subnet: 10.0.18.0/26 (AzureFirewallSubnet)
└── Management Subnet: 10.0.19.0/24
```

---

### Q3: What is the difference between Application Gateway and Azure Load Balancer?

**Answer:**

| Feature | Azure Load Balancer | Application Gateway |
|---------|-------------------|---------------------|
| OSI Layer | Layer 4 (TCP/UDP) | Layer 7 (HTTP/HTTPS) |
| Routing | IP + Port based | URL path, hostname, headers |
| SSL Termination | No | Yes |
| WAF | No | Yes (WAF v2) |
| Session Affinity | Hash-based | Cookie-based |
| Health Probes | TCP, HTTP | HTTP, HTTPS with custom paths |
| WebSocket | Pass-through | Full support |
| Autoscaling | N/A (always scaled) | V2 supports autoscaling |
| Use Case | Non-HTTP traffic, internal LB | Web apps, APIs, microservices |

**Application Gateway with AKS (AGIC):**
```yaml
# Kubernetes Ingress using Application Gateway Ingress Controller
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: subscriber-api-ingress
  annotations:
    kubernetes.io/ingress.class: azure/application-gateway
    appgw.ingress.kubernetes.io/ssl-redirect: "true"
    appgw.ingress.kubernetes.io/backend-protocol: "http"
spec:
  tls:
    - hosts:
        - api.thestandard.com
      secretName: api-tls-secret
  rules:
    - host: api.thestandard.com
      http:
        paths:
          - path: /api/v1/subscribers
            pathType: Prefix
            backend:
              service:
                name: subscriber-service
                port:
                  number: 8080
```

---

### Q4: Explain Azure Firewall and its role in enterprise architecture.

**Answer:**

Azure Firewall is a managed, cloud-native network security service that protects Azure Virtual Network resources.

**Key capabilities:**
- Stateful firewall with built-in high availability
- Application FQDN filtering (allow/deny by domain name)
- Network traffic filtering (IP, port, protocol)
- Threat intelligence-based filtering
- TLS inspection (decrypt, inspect, re-encrypt)
- DNS proxy
- Forced tunneling

**Enterprise pattern — Hub-spoke with Azure Firewall:**
```
Internet
    ↓
Azure Firewall (Hub VNET)
    ↓ (VNET Peering)
├── Spoke VNET 1: AKS Cluster
├── Spoke VNET 2: Database Services
└── Spoke VNET 3: Management VMs
```

**UDR (User Defined Route) for AKS egress through Firewall:**
```
Route Table on AKS subnet:
  0.0.0.0/0 → Azure Firewall Private IP

Azure Firewall Rules:
  - Allow AKS required FQDNs (mcr.microsoft.com, *.azmk8s.io)
  - Allow application dependencies (API endpoints, package registries)
  - Deny all other outbound by default
```

**Why use Azure Firewall for AKS:**
- Control and audit all egress traffic
- Prevent data exfiltration
- Compliance requirements (network-level logging)
- Centralized security policy management

---

### Q5: What are Private Link and Private Endpoints? When do you use them?

**Answer:**

**Private Link / Private Endpoint** enables private connectivity to Azure PaaS services over your VNET (instead of public internet).

**How it works:**
```
AKS Pod → VNET → Private Endpoint (NIC with private IP) → Azure Service (e.g., SQL, Key Vault, Storage)
```

**Key concepts:**
| Concept | Description |
|---------|-------------|
| Private Endpoint | A network interface with a private IP in your VNET |
| Private Link Service | Expose your own service via Private Link |
| Private DNS Zone | Resolves service FQDN to private IP |
| Approval | Manual or automatic approval for connections |

**When to use:**
- Accessing Azure SQL, Key Vault, Storage, Event Hubs from AKS without public internet
- Compliance (data never traverses public internet)
- Removing public endpoints from PaaS services
- Cross-tenant private connectivity

**Setup for Azure SQL + AKS:**
```
1. Create Private Endpoint for Azure SQL in the Private Endpoint subnet
2. Create Private DNS Zone: privatelink.database.windows.net
3. Link DNS Zone to VNET
4. AKS pods resolve sql-server.database.windows.net → private IP
5. Disable public access on Azure SQL
```

**Spring Boot configuration (same connection string):**
```yaml
spring:
  datasource:
    url: jdbc:sqlserver://myserver.database.windows.net:1433;database=mydb
    # DNS resolves to private IP automatically via Private DNS Zone
```

---

### Q6: Explain NSG (Network Security Groups) and how you design them for AKS.

**Answer:**

NSGs are Azure's layer 4 firewall — rules that allow/deny traffic based on source/destination IP, port, and protocol.

**NSG rules structure:**
- Priority (100-4096, lower = higher priority)
- Direction (Inbound/Outbound)
- Source (IP, CIDR, Service Tag, ASG)
- Destination (IP, CIDR, Service Tag, ASG)
- Port and Protocol
- Action (Allow/Deny)

**AKS NSG design:**

```
AKS Subnet NSG:
  Inbound:
    100: Allow HTTPS (443) from Application Gateway Subnet
    110: Allow internal traffic from VNET
    200: Allow Azure Load Balancer health probes
    4096: Deny all other inbound

  Outbound:
    100: Allow HTTPS (443) to AzureCloud (Azure services)
    110: Allow DNS (53) to VirtualNetwork
    120: Allow NTP (123)
    200: Allow to Private Endpoints subnet
    4096: Deny all (if using Azure Firewall for egress)
```

**Service Tags (simplify rules):**
- `AzureCloud` — All Azure public IPs
- `AzureKeyVault` — Key Vault IPs
- `Sql` — Azure SQL IPs
- `EventHub` — Event Hubs IPs
- `Internet` — All public internet

**Best practices:**
- Apply NSGs at subnet level (not individual NICs)
- Use Service Tags instead of IP addresses
- Use Application Security Groups (ASG) for grouping
- Log NSG flow logs to Storage Account for auditing
- Never allow 0.0.0.0/0 inbound unless through WAF/Firewall


---

## Azure Key Vault & Security

### Q7: How does Azure Key Vault integrate with AKS?

**Answer:**

**Methods to access Key Vault from AKS:**

**1. CSI Secret Store Driver (recommended):**
```yaml
# SecretProviderClass
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: azure-kv-secrets
spec:
  provider: azure
  parameters:
    usePodIdentity: "false"
    useVMManagedIdentity: "true"
    userAssignedIdentityID: "<managed-identity-client-id>"
    keyvaultName: "my-keyvault"
    objects: |
      array:
        - |
          objectName: db-connection-string
          objectType: secret
        - |
          objectName: api-key
          objectType: secret
    tenantId: "<tenant-id>"

# Pod mounting secrets
apiVersion: v1
kind: Pod
metadata:
  name: subscriber-api
spec:
  containers:
    - name: app
      volumeMounts:
        - name: secrets-store
          mountPath: "/mnt/secrets"
          readOnly: true
  volumes:
    - name: secrets-store
      csi:
        driver: secrets-store.csi.k8s.io
        readOnly: true
        volumeAttributes:
          secretProviderClass: "azure-kv-secrets"
```

**2. Workload Identity (Azure AD):**
- Pod gets an Azure AD identity
- Directly authenticates to Key Vault using federated credentials
- No secrets stored in Kubernetes

**3. Spring Cloud Azure (in-app):**
```yaml
spring:
  cloud:
    azure:
      keyvault:
        secret:
          endpoint: https://my-keyvault.vault.azure.net/
          # Uses managed identity automatically on AKS
```

**Best practices:**
- Use Managed Identity (no credentials to manage)
- Enable soft delete and purge protection
- Separate Key Vaults per environment (dev, staging, prod)
- Enable access logging (diagnostic settings)
- Use RBAC (not access policies) for granular control
- Rotate secrets automatically with expiry notifications

---

### Q8: Explain VNET/Subnet design for an enterprise AKS deployment.

**Answer:**

**Design principles:**
- Separate subnets for different concerns (separation of duty)
- Size subnets for growth (AKS with Azure CNI needs many IPs)
- Use /16 VNET with /20+ for AKS subnet
- Reserve space for future expansion

**Enterprise VNET architecture:**
```
Hub VNET (10.0.0.0/16) — Shared services
├── AzureFirewallSubnet: 10.0.0.0/26 (mandatory name)
├── GatewaySubnet: 10.0.0.64/26 (for VPN/ExpressRoute)
├── ManagementSubnet: 10.0.1.0/24 (jumpboxes, bastion)
└── DNSSubnet: 10.0.2.0/24 (DNS resolvers)

Spoke VNET - Production (10.1.0.0/16) — Peered to Hub
├── AKS System Pool: 10.1.0.0/21 (2048 IPs)
├── AKS User Pool: 10.1.8.0/21 (2048 IPs)
├── AppGateway Subnet: 10.1.16.0/24
├── Private Endpoints: 10.1.17.0/24
├── Azure Bastion: 10.1.18.0/26 (AzureBastionSubnet)
└── Reserved: 10.1.20.0/22

Spoke VNET - Non-Prod (10.2.0.0/16)
├── AKS Dev: 10.2.0.0/22
├── AKS Staging: 10.2.4.0/22
└── Private Endpoints: 10.2.8.0/24
```

**IP planning for AKS (Azure CNI):**
```
IPs needed = (max_pods_per_node + 1) × max_nodes + reserved
Example: (30 + 1) × 50 nodes + 5 reserved = 1555 IPs → use /21 (2048 IPs)
```

**VNET Peering:**
- Hub ↔ Spoke peering for shared services (Firewall, DNS)
- Allow gateway transit from Hub for on-premises connectivity
- Use remote gateways in Spoke for VPN/ExpressRoute access

---

## Azure DevOps & CI/CD

### Q9: How do you design a CI/CD pipeline for Spring Boot on AKS using Azure DevOps?

**Answer:**

**Pipeline architecture:**
```
Code Push → Azure DevOps Pipeline
  ├── Build Stage: Compile, test, build Docker image
  ├── Security Stage: SAST, dependency scan, container scan
  ├── Publish Stage: Push image to ACR (Azure Container Registry)
  ├── Deploy Dev: Helm deploy to dev AKS
  ├── Integration Test: Run API tests against dev
  ├── Deploy Staging: Helm deploy to staging AKS
  ├── Performance Test: Load test against staging
  └── Deploy Prod: Helm deploy to prod AKS (manual approval)
```

**Azure DevOps YAML pipeline:**
```yaml
trigger:
  branches:
    include:
      - main
      - release/*

variables:
  acrName: 'myacr.azurecr.io'
  imageName: 'subscriber-api'
  helmChart: 'charts/subscriber-api'

stages:
  - stage: Build
    jobs:
      - job: BuildAndTest
        pool:
          vmImage: 'ubuntu-latest'
        steps:
          - task: Maven@4
            inputs:
              mavenPomFile: 'pom.xml'
              goals: 'clean verify'
              options: '-DskipITs'
          
          - task: Docker@2
            inputs:
              containerRegistry: 'acr-connection'
              repository: '$(imageName)'
              command: 'buildAndPush'
              Dockerfile: 'Dockerfile'
              tags: |
                $(Build.BuildId)
                latest

  - stage: DeployDev
    dependsOn: Build
    jobs:
      - deployment: DeployToDev
        environment: 'dev'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: HelmDeploy@0
                  inputs:
                    connectionType: 'Azure Resource Manager'
                    azureSubscription: 'azure-sub'
                    azureResourceGroup: 'rg-aks-dev'
                    kubernetesCluster: 'aks-dev'
                    command: 'upgrade'
                    chartType: 'FilePath'
                    chartPath: '$(helmChart)'
                    releaseName: 'subscriber-api'
                    overrideValues: 'image.tag=$(Build.BuildId)'

  - stage: DeployProd
    dependsOn: DeployStaging
    condition: succeeded()
    jobs:
      - deployment: DeployToProd
        environment: 'production'  # Manual approval gate
        strategy:
          runOnce:
            deploy:
              steps:
                - task: HelmDeploy@0
                  inputs:
                    command: 'upgrade'
                    releaseName: 'subscriber-api'
                    overrideValues: 'image.tag=$(Build.BuildId),replicaCount=3'
```

---

### Q10: How do you implement Docker multi-stage builds for Spring Boot?

**Answer:**

```dockerfile
# Stage 1: Build
FROM maven:3.9-eclipse-temurin-21 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src ./src
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# Security: non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Copy only the JAR
COPY --from=builder /app/target/*.jar app.jar

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

# JVM tuning for containers
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -XX:+UseG1GC"
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

**Key practices:**
- Multi-stage to minimize image size (build tools not in final image)
- Non-root user for security
- Container-aware JVM flags (`UseContainerSupport`)
- Health check for Kubernetes probes
- `.dockerignore` to exclude unnecessary files
- Pin base image versions for reproducibility

---

### Q11: What is Kubernetes Helm and how do you structure charts for microservices?

**Answer:**

Helm is a package manager for Kubernetes — templates + values = rendered manifests.

**Chart structure:**
```
charts/subscriber-api/
├── Chart.yaml          # Metadata (name, version, dependencies)
├── values.yaml         # Default values
├── values-dev.yaml     # Dev overrides
├── values-prod.yaml    # Prod overrides
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── hpa.yaml
    ├── configmap.yaml
    ├── secret-provider.yaml
    └── _helpers.tpl     # Template helpers
```

**deployment.yaml (templated):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "subscriber-api.fullname" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ include "subscriber-api.name" . }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - containerPort: {{ .Values.service.port }}
          resources:
            requests:
              memory: {{ .Values.resources.requests.memory }}
              cpu: {{ .Values.resources.requests.cpu }}
            limits:
              memory: {{ .Values.resources.limits.memory }}
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: {{ .Values.service.port }}
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: {{ .Values.service.port }}
```

**values-prod.yaml:**
```yaml
replicaCount: 3
image:
  repository: myacr.azurecr.io/subscriber-api
  tag: "latest"
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "1Gi"
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPU: 70
```


---

### Q12: How do you implement GitOps for AKS deployments?

**Answer:**

**GitOps principles:**
- Git is the single source of truth for infrastructure and application state
- Changes are made via pull requests (not direct kubectl)
- Automated reconciliation ensures cluster matches desired state
- Drift detection and self-healing

**GitOps with Flux (Azure recommended):**
```
Developer → PR to Git → Merge → Flux detects change → Deploys to AKS
```

**Setup:**
```bash
# Enable GitOps extension on AKS
az k8s-configuration flux create \
  --resource-group rg-aks-prod \
  --cluster-name aks-prod \
  --name app-config \
  --namespace flux-system \
  --scope cluster \
  --url https://dev.azure.com/org/project/_git/k8s-manifests \
  --branch main \
  --kustomization name=apps path=./clusters/production
```

**Repository structure:**
```
k8s-manifests/
├── base/                    # Shared manifests
│   ├── subscriber-api/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── kustomization.yaml
│   └── payment-api/
├── clusters/
│   ├── dev/
│   │   └── kustomization.yaml (patches for dev)
│   ├── staging/
│   │   └── kustomization.yaml
│   └── production/
│       └── kustomization.yaml (patches for prod)
```

**Benefits over imperative CI/CD:**
- Cluster self-heals if someone makes manual changes
- Easy rollback (git revert)
- Audit trail (git history)
- Multi-cluster consistency

---

### Q13: How do you handle secrets management across environments in AKS?

**Answer:**

**Strategy: Azure Key Vault + CSI Driver + Environment Separation**

```
Dev Key Vault (kv-dev)     → AKS Dev Cluster
Staging Key Vault (kv-stg) → AKS Staging Cluster
Prod Key Vault (kv-prod)   → AKS Prod Cluster
```

**Principles:**
1. **Never store secrets in Git** (no Kubernetes Secrets in manifests)
2. **Use Managed Identity** (no passwords for accessing Key Vault)
3. **Separate vaults per environment** (blast radius containment)
4. **Rotate secrets regularly** (Key Vault supports auto-rotation)
5. **Audit access** (diagnostic logs enabled on Key Vault)

**Access flow:**
```
Pod (with Workload Identity) → Azure AD Token → Key Vault → Secret Value
```

**Helm values (no secrets, only vault references):**
```yaml
# values-prod.yaml
keyvault:
  name: "kv-prod"
  tenantId: "xxx"
  secrets:
    - name: db-connection-string
    - name: kafka-password
    - name: api-key
```

**Secret rotation without restart:**
```yaml
# CSI driver polls for changes
spec:
  provider: azure
  parameters:
    pollingInterval: "60s"  # Check for rotation every 60s
```

---

### Q14: Explain Azure Monitor and observability for AKS.

**Answer:**

**Azure Monitor stack for AKS:**

| Component | Purpose |
|-----------|---------|
| Container Insights | Node/pod metrics, logs, live data |
| Azure Monitor Metrics | Custom metrics, Prometheus integration |
| Log Analytics Workspace | Centralized log storage and querying (KQL) |
| Application Insights | Application-level APM (traces, dependencies) |
| Azure Managed Grafana | Dashboards |
| Azure Managed Prometheus | Prometheus-compatible metrics store |

**Key metrics to monitor:**

```
Cluster Level:
- Node CPU/Memory utilization
- Node count vs capacity
- Disk pressure, PID pressure

Pod Level:
- Pod restart count
- CPU/Memory requests vs actual usage
- Pod pending (scheduling issues)

Application Level:
- Request rate, error rate, duration (RED)
- Kafka consumer lag
- Database connection pool utilization
- Custom business metrics
```

**KQL query examples:**
```kusto
// Pods restarting frequently
KubePodInventory
| where RestartCount > 5
| summarize MaxRestarts = max(RestartCount) by Name, Namespace
| order by MaxRestarts desc

// Container OOM kills
ContainerLog
| where LogEntry contains "OOMKilled"
| project TimeGenerated, ContainerName, LogEntry

// Application errors
traces
| where severityLevel >= 3
| summarize ErrorCount = count() by operation_Name, bin(timestamp, 5m)
| render timechart
```

---

### Q15: How do you implement zero-downtime deployments on AKS?

**Answer:**

**Strategies:**

**1. Rolling Update (default):**
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%        # Extra pods during update
      maxUnavailable: 0     # Never reduce below desired count
```

**2. Blue-Green Deployment:**
```yaml
# Deploy new version as "green"
# Switch service selector from "blue" to "green"
# Keep blue running for quick rollback
apiVersion: v1
kind: Service
metadata:
  name: subscriber-api
spec:
  selector:
    app: subscriber-api
    version: green  # Switch this label
```

**3. Canary Deployment (with Ingress):**
```yaml
# Canary ingress — 10% traffic to new version
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: subscriber-api-canary
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "10"
spec:
  rules:
    - host: api.thestandard.com
      http:
        paths:
          - path: /api/v1/subscribers
            backend:
              service:
                name: subscriber-api-canary
```

**Essential for zero-downtime:**
- **Readiness probes:** Don't route traffic until app is ready
- **PreStop hook:** Allow in-flight requests to complete
  ```yaml
  lifecycle:
    preStop:
      exec:
        command: ["sleep", "10"]  # Wait for LB to deregister
  ```
- **PodDisruptionBudget:** Ensure minimum replicas during node drains
  ```yaml
  apiVersion: policy/v1
  kind: PodDisruptionBudget
  spec:
    minAvailable: 2
    selector:
      matchLabels:
        app: subscriber-api
  ```
- **Graceful shutdown:** `spring.lifecycle.timeout-per-shutdown-phase=30s`

---

### Q16: What is NAT Gateway and when do you use it with AKS?

**Answer:**

**NAT Gateway** provides outbound internet connectivity for resources in a subnet using a static public IP.

**Why use with AKS:**
- **Predictable egress IP:** External services can whitelist your IP
- **SNAT port exhaustion prevention:** NAT Gateway supports 64K ports per IP (vs limited SNAT ports on Load Balancer)
- **Scalability:** Add multiple public IPs for more ports

**Architecture:**
```
AKS Pod → Node → NAT Gateway (static public IP) → Internet
```

**When to use:**
- External APIs require IP whitelisting
- High outbound connection count (many pods calling external services)
- SNAT exhaustion issues with default Azure LB egress
- Need consistent outbound IP regardless of node count

**Configuration:**
```bash
# Create NAT Gateway
az network nat gateway create \
  --resource-group rg-aks \
  --name nat-aks-egress \
  --public-ip-addresses pip-nat-egress

# Associate with AKS subnet
az network vnet subnet update \
  --resource-group rg-aks \
  --vnet-name vnet-aks \
  --name aks-subnet \
  --nat-gateway nat-aks-egress
```

**AKS outbound type options:**
| Type | Description |
|------|-------------|
| loadBalancer (default) | Standard LB provides SNAT |
| managedNATGateway | Azure-managed NAT Gateway |
| userAssignedNATGateway | Your own NAT Gateway |
| userDefinedRouting | Route through Azure Firewall (no direct internet) |
