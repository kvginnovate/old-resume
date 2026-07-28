# API Engineering & Spring Boot — Questions & Answers

## Core Spring Boot & REST API Design

### Q1: What is API-first development and why is it important?

**Answer:**
API-first means designing the API contract (OpenAPI/Swagger spec) before writing any implementation code.

**Why it matters:**
- **Parallel development:** Frontend and backend teams can work simultaneously using the contract
- **Contract as documentation:** Always up-to-date, machine-readable API docs
- **Code generation:** Generate server stubs, client SDKs, and test mocks from the spec
- **Consistency:** Enforce naming conventions, error formats, and pagination patterns upfront
- **Early feedback:** Stakeholders review the API contract before expensive implementation

**How I practice it:**
1. Write OpenAPI 3.0 spec in YAML
2. Review with consumers (frontend, mobile, partner teams)
3. Generate Spring Boot controller interfaces using `openapi-generator-maven-plugin`
4. Implement the generated interfaces
5. CI validates implementation matches spec (contract testing)

---

### Q2: How do you design a RESTful API for enterprise use?

**Answer:**

**Key principles:**

1. **Resource-oriented URLs:**
   ```
   GET    /api/v1/subscribers/{id}
   POST   /api/v1/subscribers
   PUT    /api/v1/subscribers/{id}
   PATCH  /api/v1/subscribers/{id}
   DELETE /api/v1/subscribers/{id}
   ```

2. **Versioning strategy:**
   - URL path versioning (`/api/v1/`) for breaking changes
   - Header versioning for minor variations (Accept-Version)

3. **Consistent error response:**
   ```json
   {
     "error": {
       "code": "SUBSCRIBER_NOT_FOUND",
       "message": "Subscriber with ID 12345 not found",
       "timestamp": "2024-01-15T10:30:00Z",
       "traceId": "abc-123-def-456",
       "details": []
     }
   }
   ```

4. **Pagination:**
   ```
   GET /api/v1/subscribers?page=0&size=20&sort=createdAt,desc
   ```
   Response includes: `totalElements`, `totalPages`, `number`, `size`

5. **HATEOAS (where appropriate):** Links for discoverability

6. **Idempotency:** POST with idempotency keys for safe retries

7. **Rate limiting headers:** `X-RateLimit-Limit`, `X-RateLimit-Remaining`

---

### Q3: Explain Spring Boot auto-configuration. How does it work internally?

**Answer:**

Spring Boot auto-configuration automatically configures beans based on:
1. Classes on the classpath
2. Existing bean definitions
3. Property values

**How it works internally:**

1. `@SpringBootApplication` includes `@EnableAutoConfiguration`
2. Spring reads `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` (Spring Boot 3) or `META-INF/spring.factories` (Spring Boot 2)
3. Each auto-configuration class uses conditional annotations:
   - `@ConditionalOnClass` — only if class is on classpath
   - `@ConditionalOnMissingBean` — only if user hasn't defined their own
   - `@ConditionalOnProperty` — only if property is set
4. Spring evaluates conditions and registers matching beans

**Example:**
```java
@AutoConfiguration
@ConditionalOnClass(DataSource.class)
@ConditionalOnProperty(name = "spring.datasource.url")
public class DataSourceAutoConfiguration {
    
    @Bean
    @ConditionalOnMissingBean
    public DataSource dataSource(DataSourceProperties properties) {
        return properties.initializeDataSourceBuilder().build();
    }
}
```

**Key point:** User-defined beans always take precedence over auto-configured ones (`@ConditionalOnMissingBean`).

---

### Q4: How do you handle exception handling in a Spring Boot REST API?

**Answer:**

**Use `@RestControllerAdvice` for global exception handling:**

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex, WebRequest request) {
        ErrorResponse error = ErrorResponse.builder()
            .code("RESOURCE_NOT_FOUND")
            .message(ex.getMessage())
            .timestamp(Instant.now())
            .traceId(MDC.get("traceId"))
            .path(((ServletWebRequest) request).getRequest().getRequestURI())
            .build();
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }

    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<ErrorResponse> handleValidation(ConstraintViolationException ex) {
        List<FieldError> details = ex.getConstraintViolations().stream()
            .map(v -> new FieldError(v.getPropertyPath().toString(), v.getMessage()))
            .toList();
        ErrorResponse error = ErrorResponse.builder()
            .code("VALIDATION_ERROR")
            .message("Request validation failed")
            .details(details)
            .build();
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneric(Exception ex) {
        log.error("Unexpected error", ex);
        ErrorResponse error = ErrorResponse.builder()
            .code("INTERNAL_ERROR")
            .message("An unexpected error occurred")
            .build();
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
```

**Best practices:**
- Never expose stack traces to clients
- Always include correlation/trace IDs
- Use problem-specific error codes (not just HTTP status)
- Log full details server-side, return sanitized response to client
- Map domain exceptions to appropriate HTTP status codes

---

### Q5: What is Resilience4j and how do you implement resilience patterns?

**Answer:**

Resilience4j is a lightweight fault tolerance library for Java, designed for functional programming. It provides:

**1. Circuit Breaker:**
```java
@CircuitBreaker(name = "paymentService", fallbackMethod = "paymentFallback")
public PaymentResponse processPayment(PaymentRequest request) {
    return paymentClient.charge(request);
}

private PaymentResponse paymentFallback(PaymentRequest request, Exception ex) {
    // Queue for retry or return cached response
    return PaymentResponse.pending(request.getId());
}
```

Configuration:
```yaml
resilience4j:
  circuitbreaker:
    instances:
      paymentService:
        slidingWindowSize: 10
        failureRateThreshold: 50
        waitDurationInOpenState: 30s
        permittedNumberOfCallsInHalfOpenState: 3
```

**2. Retry:**
```java
@Retry(name = "paymentService", fallbackMethod = "paymentFallback")
public PaymentResponse processPayment(PaymentRequest request) {
    return paymentClient.charge(request);
}
```

**3. Rate Limiter:**
```java
@RateLimiter(name = "apiRateLimit")
public Response handleRequest(Request request) { ... }
```

**4. Bulkhead (isolation):**
```java
@Bulkhead(name = "paymentService", type = Bulkhead.Type.THREADPOOL)
public PaymentResponse processPayment(PaymentRequest request) { ... }
```

**5. Time Limiter:**
```java
@TimeLimiter(name = "paymentService")
public CompletableFuture<PaymentResponse> processPayment(PaymentRequest request) { ... }
```

**Combining patterns (order matters):**
Retry → CircuitBreaker → RateLimiter → TimeLimiter → Bulkhead

---

### Q6: Explain Spring Boot 3 major changes from Spring Boot 2.

**Answer:**

**Key changes:**

| Area | Spring Boot 2 | Spring Boot 3 |
|------|--------------|--------------|
| Java | Java 8+ | Java 17+ (minimum) |
| Jakarta EE | javax.* namespace | jakarta.* namespace |
| Spring Framework | 5.x | 6.x |
| Native | Experimental | First-class GraalVM native support |
| Observability | Micrometer + Sleuth | Micrometer + Micrometer Tracing (Sleuth deprecated) |
| Auto-config | spring.factories | AutoConfiguration.imports file |
| HTTP Client | RestTemplate (deprecated) | RestClient (new), WebClient |
| Security | WebSecurityConfigurerAdapter | SecurityFilterChain bean |
| AOT | Not available | Ahead-of-Time compilation |

**Migration challenges I've handled:**
1. `javax.*` → `jakarta.*` package rename (50K+ lines affected)
2. Security configuration rewrite (adapter → lambda DSL)
3. Observability migration (Sleuth → Micrometer Tracing)
4. Property changes (e.g., `spring.redis.*` → `spring.data.redis.*`)
5. Deprecated API replacements

---

### Q7: What are Virtual Threads (Project Loom) and how do they affect Spring Boot?

**Answer:**

**What are Virtual Threads?**
- Lightweight threads managed by the JVM (not OS threads)
- Millions of virtual threads possible (vs ~thousands of platform threads)
- Designed for I/O-bound workloads (database calls, HTTP calls, messaging)

**Impact on Spring Boot:**
```yaml
# Enable virtual threads in Spring Boot 3.2+
spring:
  threads:
    virtual:
      enabled: true
```

This makes Tomcat use virtual threads for request handling — each request gets a virtual thread instead of a platform thread from the pool.

**Benefits:**
- No more thread pool sizing for I/O-bound services
- Simpler programming model (blocking code scales like async)
- No need for reactive (WebFlux) just for scalability
- Better resource utilization under high concurrency

**When to use:**
- I/O-bound microservices (most enterprise services)
- Services with many concurrent database/HTTP calls
- Replacing thread pool tuning complexity

**When NOT to use:**
- CPU-bound workloads (no benefit, slight overhead)
- Code using `synchronized` blocks with I/O inside (causes thread pinning)
- ThreadLocal-heavy code (virtual threads discourage long-lived ThreadLocals)

**Trade-off articulation:**
> "For our subscriber API handling 10K concurrent requests, virtual threads eliminate thread pool sizing concerns. We don't need reactive WebFlux — blocking Spring MVC with virtual threads gives us the same scalability with simpler debugging and stack traces."

---

### Q8: How do you design APIs for performance and scalability?

**Answer:**

**1. Response optimization:**
- Pagination (cursor-based for large datasets)
- Field selection (`?fields=id,name,email`)
- Compression (gzip/brotli)
- ETags for conditional requests (304 Not Modified)

**2. Caching strategy:**
```java
@Cacheable(value = "subscribers", key = "#id", unless = "#result == null")
public Subscriber getSubscriber(String id) { ... }

@CacheEvict(value = "subscribers", key = "#id")
public void updateSubscriber(String id, SubscriberUpdate update) { ... }
```
- L1: In-memory (Caffeine) for hot data
- L2: Distributed (Redis/GemFire) for shared state
- HTTP caching headers (Cache-Control, ETag)

**3. Connection pooling:**
```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
```

**4. Async processing:**
- Offload heavy work to Kafka/queues
- Return 202 Accepted for long-running operations
- Webhook/polling for result notification

**5. Database optimization:**
- Read replicas for read-heavy endpoints
- Denormalization for query performance
- Indexed queries, avoid N+1 problems
- Batch operations for bulk endpoints

**6. Horizontal scaling:**
- Stateless services (no session affinity)
- Kubernetes HPA (Horizontal Pod Autoscaler) based on custom metrics
- Load balancing (round-robin or least-connections)

---

### Q9: What is OpenAPI/Swagger and how do you use it in enterprise projects?

**Answer:**

**OpenAPI Specification (OAS)** is a standard for describing REST APIs in a machine-readable format (YAML/JSON).

**How I use it:**

1. **Contract-first design:**
```yaml
openapi: 3.0.3
info:
  title: Subscriber API
  version: 1.0.0
paths:
  /api/v1/subscribers/{id}:
    get:
      operationId: getSubscriber
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Subscriber found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Subscriber'
        '404':
          description: Subscriber not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
```

2. **Code generation (Maven plugin):**
```xml
<plugin>
    <groupId>org.openapitools</groupId>
    <artifactId>openapi-generator-maven-plugin</artifactId>
    <configuration>
        <inputSpec>${project.basedir}/src/main/resources/api/subscriber-api.yaml</inputSpec>
        <generatorName>spring</generatorName>
        <configOptions>
            <interfaceOnly>true</interfaceOnly>
            <useSpringBoot3>true</useSpringBoot3>
        </configOptions>
    </configuration>
</plugin>
```

3. **Runtime documentation (SpringDoc):**
```java
@Bean
public OpenAPI customOpenAPI() {
    return new OpenAPI()
        .info(new Info().title("Subscriber API").version("1.0"))
        .addSecurityItem(new SecurityRequirement().addList("bearerAuth"));
}
```

4. **Contract testing:** Validate implementation matches spec in CI

---

### Q10: How do you handle API versioning in a large microservices ecosystem?

**Answer:**

**Strategies:**

| Strategy | Pros | Cons |
|----------|------|------|
| URL path (`/v1/`, `/v2/`) | Simple, explicit, cacheable | URL pollution, harder to sunset |
| Header (`Accept-Version: v2`) | Clean URLs | Hidden, harder to test |
| Query param (`?version=2`) | Simple | Pollutes query string |
| Content negotiation (`Accept: application/vnd.api.v2+json`) | RESTful | Complex |

**My preferred approach: URL path versioning**

**Rules:**
- Only bump version for **breaking changes**
- Non-breaking changes (new optional fields, new endpoints) don't need a version bump
- Support at most N-1 versions (current + one previous)
- Deprecation timeline: announce → deprecate header → sunset

**Breaking vs Non-Breaking:**
- Breaking: removing a field, changing a field type, removing an endpoint, changing required params
- Non-breaking: adding optional field, adding new endpoint, adding optional query param

**Implementation:**
```java
// Version-specific controllers
@RestController
@RequestMapping("/api/v1/subscribers")
public class SubscriberControllerV1 { ... }

@RestController
@RequestMapping("/api/v2/subscribers")
public class SubscriberControllerV2 { ... }

// Shared service layer — versioning is at the API layer only
```

---

## Advanced Spring Boot Topics

### Q11: How do you implement distributed tracing in Spring Boot 3?

**Answer:**

Spring Boot 3 uses **Micrometer Tracing** (replacing Spring Cloud Sleuth).

**Setup:**
```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing-bridge-otel</artifactId>
</dependency>
<dependency>
    <groupId>io.opentelemetry</groupId>
    <artifactId>opentelemetry-exporter-otlp</artifactId>
</dependency>
```

**Configuration:**
```yaml
management:
  tracing:
    sampling:
      probability: 1.0  # 100% in dev, lower in prod
  otlp:
    tracing:
      endpoint: http://otel-collector:4318/v1/traces
```

**Custom spans:**
```java
@Observed(name = "payment.process", contextualName = "process-payment")
public PaymentResponse processPayment(PaymentRequest request) {
    // Automatically creates a span
    return paymentGateway.charge(request);
}
```

**Kafka trace propagation:**
```java
// Trace context is automatically propagated via Kafka headers
// when using Spring Kafka with Micrometer Tracing on classpath
@KafkaListener(topics = "orders")
public void handleOrder(ConsumerRecord<String, Order> record) {
    // Trace context extracted from headers automatically
    processOrder(record.value());
}
```

**Key points:**
- Trace ID propagated automatically across REST calls (via headers)
- Kafka propagation via record headers
- W3C Trace Context format (traceparent header)
- Export to Jaeger, Zipkin, or OTLP-compatible backends (Dynatrace, Azure Monitor)

---

### Q12: How do you secure a Spring Boot REST API?

**Answer:**

**1. Authentication (Spring Security + OAuth2/JWT):**
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .requestMatchers("/api/v1/**").authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt.jwtAuthenticationConverter(jwtAuthConverter()))
            )
            .csrf(csrf -> csrf.disable())  // Disable for stateless API
            .sessionManagement(session -> 
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS));
        return http.build();
    }
}
```

**2. Authorization (method-level):**
```java
@PreAuthorize("hasRole('ADMIN') or #subscriberId == authentication.principal.subscriberId")
public Subscriber getSubscriber(String subscriberId) { ... }
```

**3. Input validation:**
```java
@PostMapping
public ResponseEntity<Subscriber> create(@Valid @RequestBody CreateSubscriberRequest request) { ... }

public record CreateSubscriberRequest(
    @NotBlank @Size(max = 100) String name,
    @Email String email,
    @Pattern(regexp = "^\\+[1-9]\\d{1,14}$") String phone
) {}
```

**4. Additional security measures:**
- Rate limiting (Resilience4j or API gateway)
- CORS configuration
- Security headers (CSP, X-Frame-Options, HSTS)
- Input sanitization (prevent injection)
- Audit logging for sensitive operations
- Secrets in vault (Azure Key Vault / AWS Secrets Manager)

---

### Q13: How do you handle database migrations in Spring Boot?

**Answer:**

**Using Liquibase (my preference for enterprise):**

```yaml
# application.yml
spring:
  liquibase:
    change-log: classpath:db/changelog/db.changelog-master.yaml
```

```yaml
# db/changelog/db.changelog-master.yaml
databaseChangeLog:
  - include:
      file: db/changelog/changes/001-create-subscriber-table.yaml
  - include:
      file: db/changelog/changes/002-add-email-index.yaml
```

```yaml
# 001-create-subscriber-table.yaml
databaseChangeLog:
  - changeSet:
      id: 001
      author: chokkar
      changes:
        - createTable:
            tableName: subscriber
            columns:
              - column:
                  name: id
                  type: UUID
                  constraints:
                    primaryKey: true
              - column:
                  name: name
                  type: VARCHAR(100)
                  constraints:
                    nullable: false
              - column:
                  name: email
                  type: VARCHAR(255)
              - column:
                  name: created_at
                  type: TIMESTAMP
                  defaultValueComputed: CURRENT_TIMESTAMP
```

**Best practices:**
- One changeset per logical change
- Never modify executed changesets (add new ones)
- Include rollback statements for critical changes
- Test migrations against production-like data volumes
- Run migrations as part of CI/CD (separate step before app deployment)
- Use `preconditions` for safety checks

---

### Q14: How do you design integration patterns between frontend (React) and backend (Spring Boot)?

**Answer:**

**1. BFF (Backend for Frontend) pattern:**
- Dedicated API layer optimized for frontend needs
- Aggregates data from multiple microservices
- Handles frontend-specific concerns (pagination format, field naming)

**2. API contract between React and Spring Boot:**
```
React App → API Gateway (Kong) → BFF Service → Downstream Microservices
```

**3. Real-time updates:**
- Server-Sent Events (SSE) for one-way streaming
- WebSockets for bidirectional communication
- Polling as fallback

**4. Authentication flow:**
```
React → OIDC Provider (Azure AD) → JWT token
React → API call with Bearer token → Spring Boot validates JWT
```

**5. Error handling contract:**
- Consistent error format across all APIs
- Frontend maps error codes to user-friendly messages
- Retry logic for transient errors (5xx)
- Graceful degradation for partial failures

**6. Performance:**
- GraphQL or field selection for over-fetching problems
- Response compression
- CDN for static assets
- API response caching (ETags)

**Guidance I provide to frontend teams:**
- Define the API contract together (consumer-driven)
- Mock APIs using OpenAPI spec during parallel development
- Handle loading/error states consistently
- Implement retry with exponential backoff for network failures

---

### Q15: What is the difference between Spring WebFlux (reactive) and Spring MVC? When would you choose one over the other?

**Answer:**

| Aspect | Spring MVC | Spring WebFlux |
|--------|-----------|----------------|
| Programming model | Imperative (blocking) | Reactive (non-blocking) |
| Thread model | Thread-per-request | Event loop (few threads) |
| Return types | Object, ResponseEntity | Mono<T>, Flux<T> |
| Server | Tomcat, Jetty | Netty, Undertow |
| Backpressure | No | Yes |
| Debugging | Easy (linear stack traces) | Hard (async stack traces) |
| Ecosystem | Mature, broad | Growing, some gaps |

**When to choose Spring MVC (my default):**
- Most enterprise CRUD services
- Team familiarity with blocking I/O
- When virtual threads (Loom) solve the scalability need
- Integration with blocking libraries (JDBC, JPA)

**When to choose WebFlux:**
- Streaming data (SSE, WebSocket)
- Very high concurrency with limited resources
- Non-blocking all the way down (R2DBC, reactive Kafka, WebClient)
- Gateway/proxy services

**My recommendation for this role:**
> "Spring MVC with virtual threads (Spring Boot 3.2+) gives enterprise services the scalability of reactive with the simplicity of blocking code. Reserve WebFlux for streaming use cases or API gateways where the reactive model truly shines."
