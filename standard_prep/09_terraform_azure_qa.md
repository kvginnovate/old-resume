# Terraform for Azure — Questions & Answers

## Terraform Fundamentals

### Q1: What is Terraform and why use it for Azure infrastructure?

**Answer:**

Terraform is an Infrastructure as Code (IaC) tool by HashiCorp that lets you define, provision, and manage cloud infrastructure using declarative configuration files.

**Why Terraform over Azure-native (ARM/Bicep):**

| Aspect | Terraform | ARM/Bicep |
|--------|-----------|-----------|
| Multi-cloud | Yes (AWS, Azure, GCP) | Azure only |
| Language | HCL (readable, concise) | JSON (ARM) / Bicep |
| State management | Explicit state file | Azure handles |
| Plan/Preview | `terraform plan` (detailed diff) | What-if (less detailed) |
| Modularity | Rich module ecosystem | Limited |
| Community | Huge (providers, modules) | Microsoft only |
| Drift detection | Built-in (plan shows drift) | Limited |

**Core concepts:**

- **Provider:** Plugin for a cloud platform (azurerm for Azure)
- **Resource:** Infrastructure object (VM, VNET, AKS cluster)
- **Data Source:** Read existing infrastructure (lookup existing resources)
- **Module:** Reusable group of resources (like a function)
- **State:** Record of what Terraform manages (maps config to real resources)
- **Plan:** Preview of changes before applying
- **Apply:** Execute changes to reach desired state

**Basic structure:**
```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"
    }
  }
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "stterraformstate"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}
```


---

### Q2: How do you manage Terraform state for team collaboration?

**Answer:**

**Problem:** Terraform state tracks what's deployed. Without shared state, team members would overwrite each other's changes.

**Solution: Remote state backend (Azure Blob Storage):**

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "stterraformstate"
    container_name       = "tfstate"
    key                  = "production/aks.terraform.tfstate"
  }
}
```

**Setup the backend:**
```bash
# Create storage account for state (one-time setup)
az group create --name rg-terraform-state --location eastus
az storage account create \
  --name stterraformstate \
  --resource-group rg-terraform-state \
  --sku Standard_LRS \
  --encryption-services blob
az storage container create \
  --name tfstate \
  --account-name stterraformstate
```

**State locking:**
- Azure Blob Storage supports blob leasing (built-in locking)
- Prevents concurrent `terraform apply` from corrupting state
- Lock is released automatically after apply completes

**State management best practices:**

| Practice | Why |
|----------|-----|
| One state per environment | Isolate blast radius (dev state != prod state) |
| One state per component | Don't put everything in one state (networking, AKS, apps) |
| Enable versioning on blob | Recover from accidental state corruption |
| Restrict access (RBAC) | Only CI/CD service principal can write state |
| Never edit state manually | Use `terraform state mv`, `terraform import` |
| Encrypt at rest | Storage account encryption enabled |

**State file organization:**
```
tfstate container/
├── networking/
│   ├── dev.terraform.tfstate
│   ├── staging.terraform.tfstate
│   └── prod.terraform.tfstate
├── aks/
│   ├── dev.terraform.tfstate
│   └── prod.terraform.tfstate
└── shared/
    └── prod.terraform.tfstate
```

---

### Q3: How do you structure Terraform modules for an enterprise Azure deployment?

**Answer:**

**Module structure:**
```
terraform/
├── modules/                    # Reusable modules
│   ├── aks/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── versions.tf
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── keyvault/
│   ├── postgresql/
│   └── kong/
├── environments/               # Environment-specific configs
│   ├── dev/
│   │   ├── main.tf           # Calls modules with dev values
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── production/
└── shared/                    # Shared infrastructure (DNS, ACR)
    ├── main.tf
    └── terraform.tfvars
```

**AKS module example:**
```hcl
# modules/aks/main.tf
resource "azurerm_kubernetes_cluster" "main" {
  name                = var.cluster_name
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = var.dns_prefix
  kubernetes_version  = var.kubernetes_version

  default_node_pool {
    name                = "system"
    node_count          = var.system_node_count
    vm_size             = var.system_node_size
    vnet_subnet_id      = var.aks_subnet_id
    os_disk_size_gb     = 128
    max_pods            = 50
    enable_auto_scaling = true
    min_count           = var.system_min_nodes
    max_count           = var.system_max_nodes
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    network_policy    = "azure"
    load_balancer_sku = "standard"
    outbound_type     = "userAssignedNATGateway"
  }

  oms_agent {
    log_analytics_workspace_id = var.log_analytics_workspace_id
  }

  key_vault_secrets_provider {
    secret_rotation_enabled  = true
    secret_rotation_interval = "2m"
  }

  tags = var.tags
}

# User node pool
resource "azurerm_kubernetes_cluster_node_pool" "user" {
  name                  = "user"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main.id
  vm_size               = var.user_node_size
  vnet_subnet_id        = var.aks_subnet_id
  enable_auto_scaling   = true
  min_count             = var.user_min_nodes
  max_count             = var.user_max_nodes
  max_pods              = 50

  node_labels = {
    "workload" = "application"
  }

  tags = var.tags
}
```

```hcl
# modules/aks/variables.tf
variable "cluster_name" {
  description = "AKS cluster name"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.28"
}

variable "system_node_size" {
  description = "VM size for system node pool"
  type        = string
  default     = "Standard_D4s_v5"
}

variable "user_min_nodes" {
  description = "Minimum user pool nodes"
  type        = number
  default     = 3
}

variable "user_max_nodes" {
  description = "Maximum user pool nodes"
  type        = number
  default     = 10
}

variable "aks_subnet_id" {
  description = "Subnet ID for AKS nodes"
  type        = string
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
```

```hcl
# modules/aks/outputs.tf
output "cluster_id" {
  value = azurerm_kubernetes_cluster.main.id
}

output "kube_config" {
  value     = azurerm_kubernetes_cluster.main.kube_config_raw
  sensitive = true
}

output "kubelet_identity" {
  value = azurerm_kubernetes_cluster.main.kubelet_identity[0].object_id
}
```

---

### Q4: How do you deploy a full Azure networking stack with Terraform?

**Answer:**

```hcl
# modules/networking/main.tf

# VNET
resource "azurerm_virtual_network" "main" {
  name                = "vnet-${var.environment}-${var.location}"
  location            = var.location
  resource_group_name = var.resource_group_name
  address_space       = [var.vnet_address_space]
  tags                = var.tags
}

# AKS Subnet
resource "azurerm_subnet" "aks" {
  name                 = "snet-aks"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = [var.aks_subnet_cidr]
}

# Application Gateway Subnet
resource "azurerm_subnet" "appgw" {
  name                 = "snet-appgw"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = [var.appgw_subnet_cidr]
}

# Private Endpoint Subnet
resource "azurerm_subnet" "private_endpoints" {
  name                                      = "snet-private-endpoints"
  resource_group_name                       = var.resource_group_name
  virtual_network_name                      = azurerm_virtual_network.main.name
  address_prefixes                          = [var.pe_subnet_cidr]
  private_endpoint_network_policies_enabled = true
}

# NSG for AKS Subnet
resource "azurerm_network_security_group" "aks" {
  name                = "nsg-aks-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name

  security_rule {
    name                       = "AllowAppGateway"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = var.appgw_subnet_cidr
    destination_address_prefix = var.aks_subnet_cidr
  }

  security_rule {
    name                       = "DenyAllInbound"
    priority                   = 4096
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = var.tags
}

resource "azurerm_subnet_network_security_group_association" "aks" {
  subnet_id                 = azurerm_subnet.aks.id
  network_security_group_id = azurerm_network_security_group.aks.id
}

# NAT Gateway
resource "azurerm_nat_gateway" "main" {
  name                = "nat-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name
  sku_name            = "Standard"
}

resource "azurerm_public_ip" "nat" {
  name                = "pip-nat-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_nat_gateway_public_ip_association" "main" {
  nat_gateway_id       = azurerm_nat_gateway.main.id
  public_ip_address_id = azurerm_public_ip.nat.id
}

resource "azurerm_subnet_nat_gateway_association" "aks" {
  subnet_id      = azurerm_subnet.aks.id
  nat_gateway_id = azurerm_nat_gateway.main.id
}
```

---

### Q5: How do you provision Azure Key Vault with Private Endpoint using Terraform?

**Answer:**

```hcl
# Key Vault
resource "azurerm_key_vault" "main" {
  name                       = "kv-${var.environment}-${var.project}"
  location                   = var.location
  resource_group_name        = var.resource_group_name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  soft_delete_retention_days = 90
  purge_protection_enabled   = true

  # Disable public access (private endpoint only)
  public_network_access_enabled = false

  # Use RBAC instead of access policies
  enable_rbac_authorization = true

  network_acls {
    default_action = "Deny"
    bypass         = "AzureServices"
  }

  tags = var.tags
}

# Private Endpoint for Key Vault
resource "azurerm_private_endpoint" "keyvault" {
  name                = "pe-kv-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = var.private_endpoint_subnet_id

  private_service_connection {
    name                           = "psc-kv-${var.environment}"
    private_connection_resource_id = azurerm_key_vault.main.id
    is_manual_connection           = false
    subresource_names              = ["vault"]
  }

  private_dns_zone_group {
    name                 = "dns-zone-group"
    private_dns_zone_ids = [azurerm_private_dns_zone.keyvault.id]
  }
}

# Private DNS Zone
resource "azurerm_private_dns_zone" "keyvault" {
  name                = "privatelink.vaultcore.azure.net"
  resource_group_name = var.resource_group_name
}

# Link DNS Zone to VNET
resource "azurerm_private_dns_zone_virtual_network_link" "keyvault" {
  name                  = "link-kv-${var.environment}"
  resource_group_name   = var.resource_group_name
  private_dns_zone_name = azurerm_private_dns_zone.keyvault.name
  virtual_network_id    = var.vnet_id
  registration_enabled  = false
}

# Grant AKS access to Key Vault
resource "azurerm_role_assignment" "aks_keyvault" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = var.aks_kubelet_identity_object_id
}
```


---

### Q6: How do you handle environment-specific configurations in Terraform?

**Answer:**

**Approach: Same modules, different variable values per environment.**

```hcl
# environments/production/main.tf
module "networking" {
  source = "../../modules/networking"

  environment        = "prod"
  location           = "eastus"
  resource_group_name = azurerm_resource_group.main.name
  vnet_address_space = "10.1.0.0/16"
  aks_subnet_cidr    = "10.1.0.0/20"
  appgw_subnet_cidr  = "10.1.16.0/24"
  pe_subnet_cidr     = "10.1.17.0/24"
  tags               = local.tags
}

module "aks" {
  source = "../../modules/aks"

  cluster_name        = "aks-prod-ibte"
  location            = "eastus"
  resource_group_name = azurerm_resource_group.main.name
  kubernetes_version  = "1.28"
  aks_subnet_id       = module.networking.aks_subnet_id
  system_node_size    = "Standard_D4s_v5"
  system_min_nodes    = 3
  system_max_nodes    = 5
  user_node_size      = "Standard_D8s_v5"
  user_min_nodes      = 3
  user_max_nodes      = 15
  log_analytics_workspace_id = module.monitoring.workspace_id
  tags                = local.tags
}

module "keyvault" {
  source = "../../modules/keyvault"

  environment                    = "prod"
  location                       = "eastus"
  resource_group_name            = azurerm_resource_group.main.name
  private_endpoint_subnet_id     = module.networking.pe_subnet_id
  vnet_id                        = module.networking.vnet_id
  aks_kubelet_identity_object_id = module.aks.kubelet_identity
  tags                           = local.tags
}
```

```hcl
# environments/production/terraform.tfvars
environment    = "prod"
location       = "eastus"
project        = "ibte"
subscription_id = "xxx-xxx-xxx"

tags = {
  environment = "production"
  project     = "ibte"
  team        = "platform"
  cost_center = "engineering"
}
```

**Using tfvars per environment:**
```bash
# Dev deployment
terraform plan -var-file="environments/dev/terraform.tfvars"

# Prod deployment  
terraform plan -var-file="environments/production/terraform.tfvars"
```

---

### Q7: How do you integrate Terraform with Azure DevOps CI/CD?

**Answer:**

**Pipeline stages:**
```
PR: terraform fmt → validate → plan (comment on PR)
Merge: terraform plan → manual approval → apply
```

**Azure DevOps pipeline:**
```yaml
trigger:
  branches:
    include:
      - main
  paths:
    include:
      - terraform/environments/production/**

pool:
  vmImage: 'ubuntu-latest'

variables:
  - group: terraform-secrets  # ARM_CLIENT_ID, ARM_CLIENT_SECRET, etc.
  - name: tfWorkingDir
    value: 'terraform/environments/production'

stages:
  - stage: Plan
    jobs:
      - job: TerraformPlan
        steps:
          - task: TerraformInstaller@1
            inputs:
              terraformVersion: '1.6.x'

          - task: TerraformCLI@1
            displayName: 'Terraform Init'
            inputs:
              command: 'init'
              workingDirectory: '$(tfWorkingDir)'
              backendType: 'azurerm'
              backendServiceArm: 'azure-terraform-sp'
              backendAzureRmResourceGroupName: 'rg-terraform-state'
              backendAzureRmStorageAccountName: 'stterraformstate'
              backendAzureRmContainerName: 'tfstate'
              backendAzureRmKey: 'production.tfstate'

          - task: TerraformCLI@1
            displayName: 'Terraform Plan'
            inputs:
              command: 'plan'
              workingDirectory: '$(tfWorkingDir)'
              environmentServiceArm: 'azure-terraform-sp'
              publishPlanResults: 'tfplan'
              commandOptions: '-out=tfplan'

          - task: PublishBuildArtifacts@1
            inputs:
              pathToPublish: '$(tfWorkingDir)/tfplan'
              artifactName: 'tfplan'

  - stage: Apply
    dependsOn: Plan
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: TerraformApply
        environment: 'production-infra'  # Manual approval gate
        strategy:
          runOnce:
            deploy:
              steps:
                - task: DownloadBuildArtifacts@1
                  inputs:
                    artifactName: 'tfplan'

                - task: TerraformCLI@1
                  displayName: 'Terraform Apply'
                  inputs:
                    command: 'apply'
                    workingDirectory: '$(tfWorkingDir)'
                    environmentServiceArm: 'azure-terraform-sp'
                    commandOptions: 'tfplan'
```

**Security:**
- Service principal with least-privilege RBAC
- Secrets in Azure DevOps variable groups (linked to Key Vault)
- Plan output reviewed before approval
- State file access restricted to pipeline service principal

---

### Q8: How do you handle Terraform drift detection and remediation?

**Answer:**

**What is drift?** When real infrastructure differs from Terraform state (manual changes, Azure auto-updates, etc.)

**Detection:**
```bash
# Regular drift detection (schedule in CI)
terraform plan -detailed-exitcode
# Exit code 0 = no changes (no drift)
# Exit code 2 = changes detected (drift!)
```

**Scheduled drift detection pipeline:**
```yaml
schedules:
  - cron: "0 6 * * *"  # Daily at 6 AM
    branches:
      include: [main]

stages:
  - stage: DriftDetection
    jobs:
      - job: DetectDrift
        steps:
          - script: |
              terraform init
              terraform plan -detailed-exitcode -out=drift.tfplan 2>&1 | tee plan_output.txt
              EXIT_CODE=$?
              if [ $EXIT_CODE -eq 2 ]; then
                echo "##vso[task.logissue type=warning]Infrastructure drift detected!"
                echo "##vso[task.setvariable variable=driftDetected]true"
              fi
            displayName: 'Check for Drift'

          - script: |
              # Send alert to Teams/Slack
              curl -X POST $(WEBHOOK_URL) -d '{"text":"Infrastructure drift detected in production!"}'
            condition: eq(variables['driftDetected'], 'true')
```

**Remediation strategies:**

| Scenario | Action |
|----------|--------|
| Terraform config is correct, someone changed Azure | `terraform apply` to revert drift |
| Azure change was intentional | Update Terraform config to match, then `terraform plan` shows no changes |
| Resource was created outside Terraform | `terraform import` to bring under management |
| Resource should not be managed by Terraform | `terraform state rm` to remove from state |

**Preventing drift:**
- Lock down manual access (RBAC — only CI/CD can modify infra)
- Azure Policy to deny out-of-band changes
- Regular drift checks (daily in CI)
- Tag resources with `managed_by = terraform`

---

### Q9: What are Terraform best practices for production Azure environments?

**Answer:**

**1. Version pinning:**
```hcl
terraform {
  required_version = ">= 1.6.0, < 2.0.0"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"  # Minor version flexibility only
    }
  }
}
```

**2. Use data sources for existing resources:**
```hcl
# Don't hardcode IDs — look them up
data "azurerm_subscription" "current" {}
data "azurerm_client_config" "current" {}

data "azurerm_key_vault" "shared" {
  name                = "kv-shared-prod"
  resource_group_name = "rg-shared"
}
```

**3. Locals for computed values:**
```hcl
locals {
  name_prefix = "${var.project}-${var.environment}"
  tags = merge(var.tags, {
    managed_by  = "terraform"
    environment = var.environment
    last_apply  = timestamp()
  })
}
```

**4. Sensitive values handling:**
```hcl
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true  # Won't show in plan output
}

output "kube_config" {
  value     = module.aks.kube_config
  sensitive = true
}
```

**5. Lifecycle rules for critical resources:**
```hcl
resource "azurerm_kubernetes_cluster" "main" {
  # ...
  
  lifecycle {
    prevent_destroy = true  # Can't accidentally delete AKS
    ignore_changes  = [
      default_node_pool[0].node_count  # Managed by autoscaler
    ]
  }
}
```

**6. Validation on variables:**
```hcl
variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "aks_subnet_cidr" {
  type = string
  validation {
    condition     = can(cidrhost(var.aks_subnet_cidr, 0))
    error_message = "Must be a valid CIDR notation."
  }
}
```

**7. Moved blocks (refactoring without destroy):**
```hcl
# When renaming a resource
moved {
  from = azurerm_key_vault.kv
  to   = azurerm_key_vault.main
}
```

---

### Q10: How do you manage secrets and sensitive data in Terraform?

**Answer:**

**Rule: Never store secrets in Terraform code or state in plain text.**

**Strategies:**

**1. Azure Key Vault for secrets (reference, don't store):**
```hcl
# Read secret from Key Vault
data "azurerm_key_vault_secret" "db_password" {
  name         = "db-password"
  key_vault_id = data.azurerm_key_vault.main.id
}

# Use it
resource "azurerm_postgresql_flexible_server" "main" {
  administrator_password = data.azurerm_key_vault_secret.db_password.value
}
```

**2. Environment variables in CI/CD:**
```bash
# Azure DevOps passes these as env vars
export ARM_CLIENT_ID=$(ARM_CLIENT_ID)
export ARM_CLIENT_SECRET=$(ARM_CLIENT_SECRET)
export ARM_SUBSCRIPTION_ID=$(ARM_SUBSCRIPTION_ID)
export ARM_TENANT_ID=$(ARM_TENANT_ID)
```

**3. Variable files (never commit):**
```
# .gitignore
*.tfvars
!example.tfvars  # Keep example for documentation
```

**4. State file encryption:**
- Azure Blob Storage encrypts at rest by default
- Enable infrastructure encryption for double encryption
- Restrict access to storage account (only CI/CD service principal)

**5. Sensitive outputs:**
```hcl
output "connection_string" {
  value     = azurerm_postgresql_flexible_server.main.fqdn
  sensitive = true
}
```

**What NOT to do:**
- Never commit `.tfvars` with secrets to Git
- Never use `default` values for secrets
- Never output secrets to CI/CD logs
- Never store secrets in state file comments or descriptions

---

### Q11: How do you use Terraform workspaces vs directory-based environments?

**Answer:**

**Two approaches:**

| Approach | How | Pros | Cons |
|----------|-----|------|------|
| Workspaces | `terraform workspace select prod` | Single codebase, DRY | Shared state backend, risky |
| Directory-based | Separate folder per env | Full isolation, explicit | Some duplication |

**My recommendation: Directory-based for production**

Why:
- Complete isolation between environments (can't accidentally apply dev changes to prod)
- Different backends per environment (different RBAC)
- Explicit — no ambient state that depends on which workspace is selected
- Each environment can pin different provider/module versions if needed

**Directory structure:**
```
environments/
├── dev/
│   ├── main.tf        # module "aks" { source = "../../modules/aks" ... }
│   ├── backend.tf     # Points to dev state file
│   └── terraform.tfvars
├── staging/
│   ├── main.tf
│   ├── backend.tf
│   └── terraform.tfvars
└── production/
    ├── main.tf
    ├── backend.tf
    └── terraform.tfvars
```

**When workspaces make sense:**
- Temporary/ephemeral environments (feature branches)
- Dev environments that are identical
- Non-production experimentation

```bash
# Create workspace for feature branch testing
terraform workspace new feature-payment-v2
terraform apply -var-file="dev.tfvars"
# ... test ...
terraform destroy
terraform workspace delete feature-payment-v2
```

---

### Q12: How do you import existing Azure resources into Terraform?

**Answer:**

**Scenario:** Azure resources were created manually (or by another tool) and you want Terraform to manage them.

**Step-by-step:**

**1. Write the resource block first:**
```hcl
resource "azurerm_resource_group" "existing" {
  name     = "rg-legacy-app"
  location = "eastus"
}
```

**2. Import the resource:**
```bash
terraform import azurerm_resource_group.existing /subscriptions/<sub-id>/resourceGroups/rg-legacy-app
```

**3. Run plan to verify:**
```bash
terraform plan
# Should show no changes if config matches reality
# If changes shown, update your .tf file to match actual configuration
```

**4. Bulk import with import blocks (Terraform 1.5+):**
```hcl
import {
  to = azurerm_resource_group.existing
  id = "/subscriptions/xxx/resourceGroups/rg-legacy-app"
}

import {
  to = azurerm_virtual_network.existing
  id = "/subscriptions/xxx/resourceGroups/rg-legacy-app/providers/Microsoft.Network/virtualNetworks/vnet-legacy"
}
```

```bash
# Generate configuration from imports
terraform plan -generate-config-out=generated.tf
# Review generated.tf, clean up, merge into your codebase
```

**5. Using aztfexport (Azure's bulk export tool):**
```bash
# Export entire resource group to Terraform
aztfexport resource-group rg-legacy-app --output-dir ./imported
```

**Common pitfalls:**
- Imported resources may have computed fields that need `ignore_changes`
- Some resources have multiple import ID formats — check provider docs
- Always run `plan` after import to verify zero diff
- Don't forget dependent resources (importing a VNET also needs subnets, NSGs)

---

### Q13: How do you handle Terraform for AKS cluster upgrades and maintenance?

**Answer:**

```hcl
# Kubernetes version upgrade
resource "azurerm_kubernetes_cluster" "main" {
  kubernetes_version = "1.29"  # Change from "1.28" to "1.29"
  
  default_node_pool {
    orchestrator_version = "1.29"  # Must match or be one version behind
    upgrade_settings {
      max_surge = "33%"  # Extra nodes during upgrade
    }
  }

  lifecycle {
    ignore_changes = [
      default_node_pool[0].node_count  # Managed by autoscaler
    ]
  }

  # Maintenance window
  maintenance_window {
    allowed {
      day   = "Saturday"
      hours = [2, 3, 4]  # 2 AM - 4 AM
    }
  }

  maintenance_window_auto_upgrade {
    frequency   = "Weekly"
    interval    = 1
    day_of_week = "Saturday"
    start_time  = "02:00"
    duration    = 4
  }

  auto_upgrade_profile = "patch"  # Auto-upgrade patch versions only
}
```

**Upgrade strategy:**
```
1. terraform plan — shows Kubernetes version change
2. Review: will this cause node restarts? (yes, rolling)
3. Apply to dev first — verify workloads are healthy
4. Apply to staging — run full test suite
5. Apply to production (during maintenance window)
6. Monitor: node readiness, pod health, consumer lag
```

**Blue-green AKS upgrade (for major versions):**
```hcl
# Create new node pool with new version
resource "azurerm_kubernetes_cluster_node_pool" "user_v2" {
  name                  = "userv2"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main.id
  vm_size               = "Standard_D8s_v5"
  orchestrator_version  = "1.29"
  # ...
}

# Cordon old node pool, drain, then remove
# (done via kubectl, not Terraform)
```
