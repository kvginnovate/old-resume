# Kong / Kong Konnect API Gateway — Questions & Answers

## Kong Gateway Fundamentals

### Q1: What is Kong Gateway and how does it fit in a microservices architecture?

**Answer:**

Kong is an open-source, cloud-native API gateway built on NGINX/OpenResty (Lua). It sits between clients and backend services, handling cross-cutting concerns.

**Role in microservices:**
```
Clients (Web/Mobile/Partners)
       ↓
   Kong Gateway
       ↓ (routing, auth, rate limiting, logging)
├── Subscriber Service
├── Payment Service
├── Notification Service
└── Analytics Service
```

**Why Kong over alternatives:**
| Feature | Kong | AWS API Gateway | Azure APIM |
|---------|------|-----------------|------------|
| Deployment | Self-hosted / Cloud | AWS only | Azure only |
| Latency | Sub-millisecond | Higher | Higher |
| Extensibility | Lua/Go/JS plugins | Limited | Policies |
| Kubernetes native | Kong Ingress Controller | No | Limited |
| Open source | Yes (core) | No | No |
| Multi-cloud | Yes | No | No |

**Core concepts:**
- **Service:** Upstream API (e.g., subscriber-api at port 8080)
- **Route:** Rules that match client requests to a service (path, host, methods)
- **Plugin:** Middleware that adds functionality (auth, rate limiting, logging)
- **Consumer:** An API user/application (for auth and rate limiting)
- **Upstream:** Load balancing target group (multiple instances of a service)


---

### Q2: Explain Kong's architecture — data plane vs control plane.

**Answer:**

Kong supports two deployment modes:

**Traditional (DB mode):**
```
Admin API → Kong Node → PostgreSQL/Cassandra
                ↓
         Proxy (data plane)
```
- Single node handles both config and proxying
- Database stores configuration
- Simple but less scalable

**Hybrid Mode (recommended for production):**
```
Control Plane (CP)                    Data Plane (DP)
├── Admin API                         ├── Proxy traffic
├── Stores config in DB               ├── Stateless (no DB)
├── Pushes config to DPs              ├── Caches config in memory
└── Kong Manager UI                   └── Multiple instances for HA
```

**Benefits of Hybrid Mode:**
- Data planes are stateless → easy horizontal scaling
- Control plane failure doesn't affect running proxies
- Data planes can run in different regions/networks
- Reduced attack surface (no Admin API on data plane)

**DB-less Mode (declarative):**
```yaml
# kong.yaml — declarative config
_format_version: "3.0"
services:
  - name: subscriber-api
    url: http://subscriber-service:8080
    routes:
      - name: subscriber-route
        paths:
          - /api/v1/subscribers
    plugins:
      - name: rate-limiting
        config:
          minute: 100
```
- Config loaded from YAML file
- No database needed
- Ideal for Kubernetes (config as code)

---

### Q3: What is Kong Konnect and how does it differ from self-managed Kong?

**Answer:**

**Kong Konnect** is Kong's SaaS control plane — you get a managed control plane in the cloud while running data planes in your own infrastructure.

| Aspect | Self-Managed Kong | Kong Konnect |
|--------|------------------|--------------|
| Control Plane | You manage (server, DB, backups) | Kong manages (SaaS) |
| Data Plane | Your infrastructure | Your infrastructure |
| Admin UI | Kong Manager (self-hosted) | Cloud UI + API |
| Updates | Manual | Automatic (CP) |
| Analytics | Basic (plugin-based) | Built-in analytics dashboard |
| Dev Portal | Enterprise plugin | Built-in |
| RBAC | Kong Enterprise | Built-in with teams |
| Cost | License (Enterprise) or OSS | Subscription |

**Konnect architecture:**
```
Kong Konnect (cloud.konghq.com)
├── Control Plane (managed)
├── Dev Portal
├── Analytics
├── Service Hub (API catalog)
└── Runtime Manager
       ↓ (pushes config)
Your Infrastructure (AKS, EC2, etc.)
├── Data Plane 1
├── Data Plane 2
└── Data Plane N
```

**When to choose Konnect:**
- Don't want to manage control plane infrastructure
- Need built-in analytics and developer portal
- Multi-region deployments with centralized management
- Enterprise features without managing licenses

---

### Q4: How do you configure Kong for authentication (JWT, OAuth2, OIDC)?

**Answer:**

**1. JWT Plugin:**
```bash
# Enable JWT plugin on a service
curl -X POST http://kong:8001/services/subscriber-api/plugins \
  --data "name=jwt" \
  --data "config.claims_to_verify=exp"

# Create a consumer
curl -X POST http://kong:8001/consumers \
  --data "username=mobile-app"

# Create JWT credentials for consumer
curl -X POST http://kong:8001/consumers/mobile-app/jwt \
  --data "algorithm=RS256" \
  --data "rsa_public_key=@public_key.pem"
```

**2. OAuth2 Plugin (Kong-managed OAuth):**
```bash
curl -X POST http://kong:8001/services/subscriber-api/plugins \
  --data "name=oauth2" \
  --data "config.scopes=read,write" \
  --data "config.mandatory_scope=true" \
  --data "config.enable_client_credentials=true"
```

**3. OpenID Connect (OIDC) — Enterprise/Konnect:**
```bash
curl -X POST http://kong:8001/services/subscriber-api/plugins \
  --data "name=openid-connect" \
  --data "config.issuer=https://login.microsoftonline.com/{tenant}/v2.0" \
  --data "config.client_id=<app-client-id>" \
  --data "config.client_secret=<app-client-secret>" \
  --data "config.auth_methods=bearer" \
  --data "config.scopes=openid,profile,email"
```

**OIDC with Azure AD (common enterprise pattern):**
```
Client → Azure AD (get token) → Request with Bearer token → Kong (validates JWT with Azure AD JWKS) → Backend
```

Kong validates the token by:
1. Fetching JWKS from Azure AD discovery endpoint
2. Verifying signature, expiry, audience, issuer
3. Passing claims to backend via headers (X-Consumer-Username, X-Credential-Identifier)

---

### Q5: Explain Kong's rate limiting capabilities.

**Answer:**

**Rate Limiting Plugin:**
```bash
# Global rate limit
curl -X POST http://kong:8001/plugins \
  --data "name=rate-limiting" \
  --data "config.minute=100" \
  --data "config.hour=10000" \
  --data "config.policy=redis" \
  --data "config.redis_host=redis-cluster" \
  --data "config.redis_port=6379"
```

**Rate limiting levels:**
| Level | Scope | Use Case |
|-------|-------|----------|
| Global | All requests | Protect backend capacity |
| Service | Per service | Different limits per API |
| Route | Per route | Critical endpoints get lower limits |
| Consumer | Per API consumer | Fair usage per client |

**Advanced: Rate Limiting Advanced Plugin (Enterprise):**
```json
{
  "name": "rate-limiting-advanced",
  "config": {
    "limit": [100, 10000],
    "window_size": [60, 3600],
    "strategy": "sliding",
    "sync_rate": 10,
    "namespace": "subscriber-api",
    "identifier": "consumer"
  }
}
```

**Strategies:**
- `local` — Per-node counters (fast, but not precise in multi-node)
- `cluster` — Shared database counters (precise, but slower)
- `redis` — Redis-backed counters (precise and fast, recommended for production)

**Response headers:**
```
X-RateLimit-Limit-Minute: 100
X-RateLimit-Remaining-Minute: 87
Retry-After: 30  (when limited)
```

---

### Q6: How do you deploy Kong as Kubernetes Ingress Controller (KIC)?

**Answer:**

Kong Ingress Controller replaces NGINX Ingress as the Kubernetes ingress, giving you Kong's plugin ecosystem for all ingress traffic.

**Installation (Helm):**
```bash
helm repo add kong https://charts.konghq.com
helm install kong kong/ingress \
  --namespace kong \
  --set controller.ingressController.installCRDs=true \
  --set gateway.env.database=off
```

**Ingress resource:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: subscriber-api
  annotations:
    konghq.com/strip-path: "true"
    konghq.com/plugins: rate-limiting,jwt-auth
spec:
  ingressClassName: kong
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

**Kong CRDs (Custom Resource Definitions):**

```yaml
# KongPlugin — reusable plugin config
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: rate-limiting
config:
  minute: 100
  policy: redis
  redis_host: redis.default.svc.cluster.local
plugin: rate-limiting

---
# KongConsumer
apiVersion: configuration.konghq.com/v1
kind: KongConsumer
metadata:
  name: mobile-app
  annotations:
    kubernetes.io/ingress.class: kong
username: mobile-app
credentials:
  - mobile-app-jwt

---
# KongClusterPlugin — cluster-wide plugin
apiVersion: configuration.konghq.com/v1
kind: KongClusterPlugin
metadata:
  name: global-cors
  labels:
    global: "true"
config:
  origins: ["https://app.thestandard.com"]
  methods: ["GET", "POST", "PUT", "DELETE"]
  headers: ["Authorization", "Content-Type"]
plugin: cors
```


---

### Q7: What are Kong's key plugins and how do you use them?

**Answer:**

**Essential plugins by category:**

| Category | Plugin | Purpose |
|----------|--------|---------|
| Authentication | jwt, oauth2, key-auth, openid-connect | Verify identity |
| Security | cors, ip-restriction, bot-detection | Protect APIs |
| Traffic Control | rate-limiting, request-size-limiting, proxy-cache | Manage load |
| Transformation | request-transformer, response-transformer | Modify requests/responses |
| Logging | http-log, file-log, tcp-log, datadog | Audit and monitoring |
| Analytics | prometheus, opentelemetry | Metrics and tracing |

**Request Transformer example (add headers to backend):**
```json
{
  "name": "request-transformer",
  "config": {
    "add": {
      "headers": ["X-Request-Source:kong-gateway"],
      "querystring": ["version:v1"]
    },
    "remove": {
      "headers": ["X-Internal-Token"]
    },
    "rename": {
      "headers": ["Authorization:X-Auth-Token"]
    }
  }
}
```

**Proxy Cache (response caching at gateway):**
```json
{
  "name": "proxy-cache",
  "config": {
    "response_code": [200],
    "request_method": ["GET"],
    "content_type": ["application/json"],
    "cache_ttl": 300,
    "strategy": "memory"
  }
}
```

**OpenTelemetry (distributed tracing):**
```json
{
  "name": "opentelemetry",
  "config": {
    "endpoint": "http://otel-collector:4318/v1/traces",
    "resource_attributes": {
      "service.name": "kong-gateway"
    }
  }
}
```

---

### Q8: How do you implement API versioning and traffic splitting with Kong?

**Answer:**

**1. Path-based versioning:**
```yaml
# Route for v1
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: subscriber-api-v1
spec:
  rules:
    - host: api.thestandard.com
      http:
        paths:
          - path: /api/v1/subscribers
            backend:
              service:
                name: subscriber-service-v1
                port:
                  number: 8080

# Route for v2
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: subscriber-api-v2
spec:
  rules:
    - host: api.thestandard.com
      http:
        paths:
          - path: /api/v2/subscribers
            backend:
              service:
                name: subscriber-service-v2
                port:
                  number: 8080
```

**2. Header-based versioning:**
```bash
# Route matches on header
curl -X POST http://kong:8001/services/subscriber-api-v2/routes \
  --data "name=v2-route" \
  --data "paths[]=/api/subscribers" \
  --data "headers.X-API-Version=v2"
```

**3. Traffic splitting (canary):**
```bash
# Kong Upstream with weighted targets
curl -X POST http://kong:8001/upstreams \
  --data "name=subscriber-upstream"

# 90% to stable
curl -X POST http://kong:8001/upstreams/subscriber-upstream/targets \
  --data "target=subscriber-v1:8080" \
  --data "weight=90"

# 10% to canary
curl -X POST http://kong:8001/upstreams/subscriber-upstream/targets \
  --data "target=subscriber-v2:8080" \
  --data "weight=10"
```

**4. Canary Release Plugin (Enterprise):**
```json
{
  "name": "canary",
  "config": {
    "percentage": 10,
    "upstream_host": "subscriber-v2.default.svc.cluster.local",
    "upstream_port": 8080
  }
}
```

---

### Q9: How do you handle API gateway high availability and disaster recovery?

**Answer:**

**HA Architecture:**
```
                    Azure Traffic Manager (DNS-based failover)
                   /                          \
    Region 1 (Primary)                Region 2 (DR)
    ├── Load Balancer                  ├── Load Balancer
    ├── Kong DP Node 1                 ├── Kong DP Node 1
    ├── Kong DP Node 2                 ├── Kong DP Node 2
    └── Kong DP Node 3                 └── Kong DP Node 3
           ↑                                  ↑
    Kong Control Plane (shared or per-region)
```

**AKS-based HA:**
```yaml
# Kong deployment with anti-affinity (spread across nodes)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kong-proxy
spec:
  replicas: 3
  template:
    spec:
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: kong-proxy
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: kong-proxy
                topologyKey: kubernetes.io/hostname
```

**Key HA considerations:**
- Deploy Kong data planes across availability zones
- Use HPA (Horizontal Pod Autoscaler) for auto-scaling
- Health checks at load balancer level
- Hybrid mode: DP continues working if CP is temporarily unavailable
- Redis cluster for shared rate limiting state
- Database HA (PostgreSQL with read replicas) for control plane

---

### Q10: How do you monitor and troubleshoot Kong in production?

**Answer:**

**Metrics (Prometheus plugin):**
```bash
curl -X POST http://kong:8001/plugins \
  --data "name=prometheus"

# Scrape from :8100/metrics
```

**Key metrics:**
| Metric | Meaning |
|--------|---------|
| `kong_http_requests_total` | Total requests by service, route, status |
| `kong_request_latency_ms` | Request latency histogram |
| `kong_upstream_latency_ms` | Backend service latency |
| `kong_kong_latency_ms` | Kong's own processing latency |
| `kong_bandwidth_bytes` | Bandwidth by direction |
| `kong_upstream_target_health` | Backend health status |

**Grafana dashboard queries:**
```promql
# Request rate per service
rate(kong_http_requests_total{service="subscriber-api"}[5m])

# Error rate (5xx)
rate(kong_http_requests_total{code=~"5.."}[5m])
/ rate(kong_http_requests_total[5m])

# p99 latency
histogram_quantile(0.99, rate(kong_request_latency_ms_bucket{service="subscriber-api"}[5m]))
```

**Troubleshooting common issues:**

1. **High latency:** Check `kong_upstream_latency_ms` vs `kong_kong_latency_ms`
   - High upstream = backend issue
   - High kong = plugin processing or DNS resolution

2. **5xx errors:** Check upstream health
   ```bash
   curl http://kong:8001/upstreams/subscriber-upstream/health
   ```

3. **Rate limiting issues:** Check Redis connectivity and counter values

4. **Plugin execution order:**
   Kong plugins execute in this order:
   Certificate → Rewrite → Access (auth, rate-limit) → Response → Log

---

### Q11: How do you implement a developer portal with Kong?

**Answer:**

**Kong Developer Portal (Enterprise/Konnect):**
- Self-service API registration for consumers
- Auto-generated documentation from OpenAPI specs
- API key provisioning
- Usage analytics per consumer

**Setup in Konnect:**
1. Upload OpenAPI spec to Service Hub
2. Publish service to Dev Portal
3. Developers self-register and get credentials
4. Portal shows documentation, code samples, and analytics

**Custom Dev Portal workflow:**
```
1. Developer signs up → Creates consumer in Kong
2. Browses API catalog → OpenAPI specs rendered as docs
3. Requests API access → Admin approves (or auto-approve)
4. Gets credentials (API key / OAuth2 client) → KongConsumer created
5. Makes API calls → Kong enforces rate limits per consumer
6. Views usage dashboard → Analytics per consumer
```

**API catalog with Kong:**
```yaml
# Register a service with documentation
_format_version: "3.0"
services:
  - name: subscriber-api
    url: http://subscriber-service:8080
    tags: ["production", "subscriber-domain"]
    routes:
      - name: subscriber-route
        paths:
          - /api/v1/subscribers
        tags: ["v1"]
```

---

### Q12: What is the role of Kong in a zero-trust architecture?

**Answer:**

In zero-trust, Kong acts as the **Policy Enforcement Point (PEP)** — every request is authenticated, authorized, and validated regardless of network location.

**Zero-trust capabilities via Kong:**

1. **mTLS (mutual TLS):**
   ```json
   {
     "name": "mtls-auth",
     "config": {
       "ca_certificates": ["<ca-cert-id>"],
       "revocation_check_mode": "IGNORE_CA_ERROR",
       "skip_consumer_lookup": false
     }
   }
   ```

2. **Request validation (no blind trust):**
   ```json
   {
     "name": "request-validator",
     "config": {
       "body_schema": "{\"type\":\"object\",\"required\":[\"name\",\"email\"]}",
       "allowed_content_types": ["application/json"]
     }
   }
   ```

3. **IP restriction (per route):**
   ```json
   {
     "name": "ip-restriction",
     "config": {
       "allow": ["10.0.0.0/16"],
       "deny": ["0.0.0.0/0"]
     }
   }
   ```

4. **OPA (Open Policy Agent) integration:**
   - External authorization decisions
   - Fine-grained attribute-based access control
   - Policies written in Rego

**Zero-trust flow with Kong:**
```
Client → mTLS → Kong
Kong → Validate JWT (Azure AD) → Check permissions (OPA)
Kong → Rate limit → Request validation
Kong → Forward to backend (with identity headers)
Backend → Trusts only Kong-forwarded headers
```
