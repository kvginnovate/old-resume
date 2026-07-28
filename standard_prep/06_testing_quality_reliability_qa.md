# Testing, Quality & Reliability — Questions & Answers

## Test Strategy & Automation

### Q1: How do you define a testing strategy for enterprise microservices?

**Answer:**

**Test Pyramid for Microservices:**
```
         /  E2E Tests  \          (few — slow, expensive)
        / Integration    \        (moderate — API contracts, DB)
       / Component Tests   \      (more — service in isolation)
      / Unit Tests           \    (many — fast, cheap)
```

**Layer breakdown:**

| Layer | What | Tools | Coverage Target |
|-------|------|-------|----------------|
| Unit | Business logic, utilities | JUnit 5, Mockito | 85%+ line coverage |
| Component | Single service with mocked deps | Spring Boot Test, Testcontainers | Key flows |
| Integration | Service + real dependencies | Testcontainers (DB, Kafka, Redis) | Data paths |
| Contract | API compatibility between services | Spring Cloud Contract, Pact | All public APIs |
| E2E | Full system flows | Selenium, Postman/Newman, REST Assured | Critical journeys |
| Performance | Load, stress, soak | JMeter, Gatling, k6 | NFR validation |
| Security | Vulnerabilities, pen testing | OWASP ZAP, Snyk, Trivy | Every release |

**My strategy for a new microservice:**
1. Unit tests for all business logic (85%+ coverage gate in CI)
2. Integration tests with Testcontainers for DB/Kafka interactions
3. Contract tests for all API endpoints (OpenAPI validation)
4. Performance baseline in CI (Gatling smoke test)
5. Security scanning (SAST + dependency + container image)


---

### Q2: How do you implement API testing with Postman and Newman?

**Answer:**

**Postman Collection structure:**
```
Subscriber API Collection
├── Auth
│   └── Get Token (pre-request script stores token)
├── Subscribers
│   ├── Create Subscriber (POST)
│   ├── Get Subscriber (GET)
│   ├── Update Subscriber (PUT)
│   ├── List Subscribers (GET with pagination)
│   └── Delete Subscriber (DELETE)
└── Error Scenarios
    ├── Invalid Input (400)
    ├── Unauthorized (401)
    └── Not Found (404)
```

**Postman test scripts:**
```javascript
// Status code validation
pm.test("Status code is 200", () => {
    pm.response.to.have.status(200);
});

// Response schema validation
pm.test("Response has correct schema", () => {
    const schema = {
        type: "object",
        required: ["id", "name", "email", "createdAt"],
        properties: {
            id: { type: "string" },
            name: { type: "string" },
            email: { type: "string" },
            createdAt: { type: "string" }
        }
    };
    pm.response.to.have.jsonSchema(schema);
});

// Response time validation
pm.test("Response time < 500ms", () => {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

// Business logic validation
pm.test("Created subscriber has correct name", () => {
    const body = pm.response.json();
    pm.expect(body.name).to.eql(pm.variables.get("subscriberName"));
});
```

**Newman in CI/CD:**
```bash
# Run collection with environment
newman run subscriber-api.postman_collection.json \
  --environment staging.postman_environment.json \
  --reporters cli,junit,htmlextra \
  --reporter-junit-export results/junit-report.xml \
  --iteration-count 1 \
  --delay-request 100
```

**Azure DevOps integration:**
```yaml
- task: CmdLine@2
  displayName: 'Run API Tests'
  inputs:
    script: |
      npx newman run tests/subscriber-api.postman_collection.json \
        --environment tests/$(environment).postman_environment.json \
        --reporters cli,junit \
        --reporter-junit-export $(System.DefaultWorkingDirectory)/test-results.xml

- task: PublishTestResults@2
  inputs:
    testResultsFiles: '**/test-results.xml'
    testRunTitle: 'API Tests - $(environment)'
```

---

### Q3: How do you perform performance testing with JMeter?

**Answer:**

**JMeter test plan structure:**
```
Test Plan
├── Thread Group (Users simulation)
│   ├── HTTP Header Manager (Content-Type, Authorization)
│   ├── CSV Data Set Config (test data)
│   ├── HTTP Request - Create Subscriber
│   ├── HTTP Request - Get Subscriber
│   ├── Response Assertion
│   └── Duration Assertion (< 500ms)
├── Listeners
│   ├── Summary Report
│   ├── Aggregate Report
│   └── Backend Listener (InfluxDB for Grafana)
└── Config Elements
    └── HTTP Request Defaults (base URL)
```

**Load profiles:**

| Type | Purpose | Configuration |
|------|---------|---------------|
| Smoke | Verify system works under minimal load | 1-5 users, 1 minute |
| Load | Normal expected traffic | Expected concurrent users, 15-30 min |
| Stress | Find breaking point | Ramp up beyond expected, until failures |
| Soak | Memory leaks, resource exhaustion | Normal load, 4-8 hours |
| Spike | Sudden traffic burst | Rapid ramp to 10x, then back down |

**JMeter CLI (CI/CD friendly):**
```bash
jmeter -n -t subscriber-load-test.jmx \
  -Jthreads=100 \
  -Jrampup=60 \
  -Jduration=300 \
  -Jbase_url=https://api-staging.thestandard.com \
  -l results.jtl \
  -e -o report/
```

**Key metrics to capture:**
- Throughput (requests/sec)
- Response time (p50, p95, p99)
- Error rate (% of failed requests)
- Concurrent users at saturation point
- Resource utilization (CPU, memory, connections)

**NFR validation criteria:**
```
✓ p99 latency < 500ms at 1000 RPS
✓ Error rate < 0.1% under normal load
✓ System recovers within 30s after spike
✓ No memory leaks after 4-hour soak test
✓ Horizontal scaling kicks in at 70% CPU
```

---

### Q4: How do you use Gatling for performance testing?

**Answer:**

Gatling is a Scala/Java-based load testing tool with better reporting and code-first approach.

**Gatling simulation (Java DSL):**
```java
public class SubscriberApiSimulation extends Simulation {

    HttpProtocolBuilder httpProtocol = http
        .baseUrl("https://api-staging.thestandard.com")
        .acceptHeader("application/json")
        .header("Authorization", "Bearer ${token}");

    ScenarioBuilder subscriberFlow = scenario("Subscriber CRUD")
        .exec(
            http("Create Subscriber")
                .post("/api/v1/subscribers")
                .body(StringBody("""{"name":"#{name}","email":"#{email}"}"""))
                .check(status().is(201))
                .check(jsonPath("$.id").saveAs("subscriberId"))
                .check(responseTimeInMillis().lt(500))
        )
        .pause(1)
        .exec(
            http("Get Subscriber")
                .get("/api/v1/subscribers/#{subscriberId}")
                .check(status().is(200))
                .check(responseTimeInMillis().lt(200))
        )
        .pause(1)
        .exec(
            http("List Subscribers")
                .get("/api/v1/subscribers?page=0&size=20")
                .check(status().is(200))
                .check(jsonPath("$.totalElements").exists())
        );

    {
        setUp(
            subscriberFlow.injectOpen(
                rampUsers(100).during(Duration.ofSeconds(30)),  // Ramp to 100 users
                constantUsersPerSec(50).during(Duration.ofMinutes(5))  // Sustain 50 RPS
            )
        ).protocols(httpProtocol)
         .assertions(
             global().responseTime().percentile3().lt(500),  // p95 < 500ms
             global().successfulRequests().percent().gt(99.0) // > 99% success
         );
    }
}
```

**Maven integration:**
```xml
<plugin>
    <groupId>io.gatling</groupId>
    <artifactId>gatling-maven-plugin</artifactId>
    <version>4.9.6</version>
    <configuration>
        <simulationClass>com.thestandard.SubscriberApiSimulation</simulationClass>
    </configuration>
</plugin>
```

**Run in CI:**
```bash
mvn gatling:test -Dgatling.simulationClass=com.thestandard.SubscriberApiSimulation
```

**Gatling vs JMeter:**
| Aspect | Gatling | JMeter |
|--------|---------|--------|
| Language | Scala/Java DSL (code) | XML + GUI |
| Version control | Easy (code) | Hard (XML) |
| Reports | Beautiful HTML built-in | Plugin-based |
| Resource usage | Lightweight (Akka) | Heavier (threads) |
| Learning curve | Developers prefer | QA-friendly GUI |
| CI integration | Native Maven/Gradle | CLI mode |

---

### Q5: What are quality gates and how do you implement them in CI/CD?

**Answer:**

Quality gates are automated checkpoints in the CI/CD pipeline that prevent deployment if quality criteria aren't met.

**Quality gate stages:**

```
Code Commit → Build → Quality Gates → Deploy
                         ├── Unit Test Coverage ≥ 85%
                         ├── No Critical/High Snyk vulnerabilities
                         ├── No Sonar blocker/critical issues
                         ├── API contract tests pass
                         ├── Performance baseline within 10% regression
                         ├── Container image scan clean
                         └── All mandatory tests green
```

**Implementation in Azure DevOps:**
```yaml
stages:
  - stage: QualityGates
    jobs:
      - job: CodeQuality
        steps:
          # Unit test coverage gate
          - task: Maven@4
            inputs:
              goals: 'verify'
              options: '-Djacoco.minimum=0.85'
          
          # Publish coverage
          - task: PublishCodeCoverageResults@2
            inputs:
              codeCoverageTool: 'JaCoCo'
              summaryFileLocation: '**/jacoco.xml'

          # SonarQube analysis
          - task: SonarQubeAnalyze@5
          - task: SonarQubePublish@5
          
          # Quality gate check
          - task: sonar-buildbreaker@8
            inputs:
              SonarQube: 'sonarqube-connection'

      - job: SecurityScan
        steps:
          # Dependency vulnerabilities
          - script: snyk test --severity-threshold=high --fail-on=all
          
          # Container image scan
          - script: trivy image --exit-code 1 --severity HIGH,CRITICAL $(imageName):$(tag)

      - job: ContractTests
        steps:
          - script: mvn verify -pl contract-tests
```

**Gate criteria I enforce:**

| Gate | Criteria | Blocks Deploy? |
|------|----------|----------------|
| Unit Coverage | ≥ 85% line, ≥ 80% branch | Yes |
| Sonar | 0 blockers, 0 criticals | Yes |
| Snyk | 0 high/critical vulnerabilities | Yes |
| API Contracts | All contract tests pass | Yes |
| Performance | p99 latency within 10% of baseline | Yes (staging→prod) |
| Container Scan | 0 critical CVEs | Yes |
| Integration Tests | All pass | Yes |

---

### Q6: How do you implement contract testing for microservices?

**Answer:**

Contract testing verifies that service interactions (APIs) remain compatible as services evolve independently.

**Spring Cloud Contract approach:**

**Provider side (API owner):**
```groovy
// contracts/shouldReturnSubscriber.groovy
Contract.make {
    description "should return subscriber by ID"
    request {
        method 'GET'
        url '/api/v1/subscribers/12345'
        headers {
            header('Authorization', 'Bearer valid-token')
        }
    }
    response {
        status 200
        headers {
            contentType(applicationJson())
        }
        body([
            id: "12345",
            name: "John Doe",
            email: "john@example.com",
            createdAt: "2024-01-15T10:00:00Z"
        ])
    }
}
```

**Generated test (auto-generated by plugin):**
```java
// Provider verifies it can fulfill the contract
@Test
public void shouldReturnSubscriber() {
    given()
        .header("Authorization", "Bearer valid-token")
    .when()
        .get("/api/v1/subscribers/12345")
    .then()
        .statusCode(200)
        .body("id", equalTo("12345"))
        .body("name", equalTo("John Doe"));
}
```

**Consumer side (API consumer):**
```java
// Consumer tests against the stub generated from contract
@AutoConfigureStubRunner(
    ids = "com.thestandard:subscriber-api:+:stubs:8080",
    stubsMode = StubRunnerProperties.StubsMode.LOCAL
)
@SpringBootTest
class PaymentServiceConsumerTest {

    @Autowired
    private SubscriberClient subscriberClient;

    @Test
    void shouldGetSubscriber() {
        Subscriber subscriber = subscriberClient.getSubscriber("12345");
        assertThat(subscriber.getName()).isEqualTo("John Doe");
    }
}
```

**Workflow:**
```
Provider publishes contract + stub JAR → Artifact repository
Consumer downloads stubs → Tests against stubs locally
Both sides verified → Safe to deploy independently
```

---

### Q7: How do you test Kafka-based event-driven systems?

**Answer:**

**1. Unit testing producers/consumers:**
```java
@Test
void shouldPublishOrderEvent() {
    // Given
    Order order = new Order("123", "customer-1", BigDecimal.valueOf(99.99));
    
    // When
    orderService.createOrder(order);
    
    // Then
    ConsumerRecord<String, OrderEvent> record = 
        KafkaTestUtils.getSingleRecord(consumer, "order.created");
    assertThat(record.key()).isEqualTo("123");
    assertThat(record.value().getCustomerId()).isEqualTo("customer-1");
}
```

**2. Integration testing with Testcontainers:**
```java
@Testcontainers
@SpringBootTest
class OrderEventIntegrationTest {

    @Container
    static KafkaContainer kafka = new KafkaContainer(
        DockerImageName.parse("confluentinc/cp-kafka:7.5.0")
    );

    @Container
    static GenericContainer<?> schemaRegistry = new GenericContainer<>(
        DockerImageName.parse("confluentinc/cp-schema-registry:7.5.0")
    ).withExposedPorts(8081)
     .withEnv("SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS", kafka.getBootstrapServers());

    @DynamicPropertySource
    static void kafkaProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.kafka.bootstrap-servers", kafka::getBootstrapServers);
    }

    @Test
    void shouldProcessOrderEndToEnd() {
        // Publish event
        kafkaTemplate.send("order.created", "123", orderEvent);
        
        // Verify consumer processed it
        await().atMost(Duration.ofSeconds(10)).untilAsserted(() -> {
            Order saved = orderRepository.findById("123");
            assertThat(saved).isNotNull();
            assertThat(saved.getStatus()).isEqualTo("PROCESSED");
        });
    }
}
```

**3. Schema compatibility testing:**
```java
@Test
void shouldBeBackwardCompatible() {
    // Register schema v1
    schemaRegistryClient.register("order-value", schemaV1);
    
    // Verify v2 is backward compatible
    boolean compatible = schemaRegistryClient.testCompatibility(
        "order-value", schemaV2
    );
    assertThat(compatible).isTrue();
}
```

**4. Testing patterns:**
- Dead letter queue handling (poison pill messages)
- Exactly-once semantics verification
- Consumer lag monitoring during tests
- Idempotency testing (replay same message)
- Ordering guarantees (same partition key)

---

### Q8: How do you implement non-functional testing (scalability, reliability, operational readiness)?

**Answer:**

**Scalability testing:**
```
1. Horizontal scaling test:
   - Start with 3 pods
   - Ramp load until HPA triggers scale-out
   - Verify requests continue without errors during scaling
   - Verify scale-down after load drops

2. Database connection pool test:
   - 100 concurrent requests per pod
   - Monitor HikariCP pool (active, pending, timeout)
   - Verify no connection exhaustion

3. Kafka consumer scaling:
   - Add partitions to topic
   - Verify consumer group rebalances cleanly
   - No message loss during rebalance
```

**Reliability testing:**
```
1. Chaos engineering:
   - Kill random pods → verify service continues
   - Network partition between service and DB → circuit breaker activates
   - Kafka broker down → producer retries, consumer catches up

2. Failover testing:
   - Primary database failover → app reconnects to replica
   - Region failover → traffic routes to DR region
   - Key Vault unavailable → cached secrets still work

3. Recovery testing:
   - Measure MTTR (Mean Time To Recovery)
   - Verify no data loss after crash
   - Verify correct event replay from Kafka
```

**Operational readiness checklist:**
```
□ Health endpoints (liveness + readiness) responding correctly
□ Metrics exported (Prometheus/Dynatrace)
□ Structured logs with correlation IDs
□ Distributed traces connected end-to-end
□ Alerts configured for error rate, latency, resource usage
□ Runbooks documented for common failures
□ Dashboards showing golden signals (rate, errors, duration, saturation)
□ Rollback procedure tested
□ Secret rotation tested
□ Backup/restore procedure validated
□ On-call escalation path defined
□ Capacity planning documented (current usage vs limits)
```

---

### Q9: How do you guide testability in microservice design?

**Answer:**

**Design for testability principles:**

1. **Dependency injection everywhere:**
   - All external dependencies injected (not instantiated)
   - Easy to mock in unit tests
   - Configuration externalized (not hardcoded)

2. **Clear boundaries:**
   ```
   Controller → Service → Repository (each layer testable independently)
   ```

3. **Ports and Adapters (Hexagonal) architecture:**
   ```java
   // Port (interface) — testable with mocks
   public interface PaymentGateway {
       PaymentResult charge(PaymentRequest request);
   }
   
   // Adapter (implementation) — tested with integration tests
   public class StripePaymentGateway implements PaymentGateway { ... }
   
   // Test: mock the port
   @Mock PaymentGateway paymentGateway;
   ```

4. **Idempotent operations:**
   - Same input → same output (easy to verify)
   - Retries don't cause side effects

5. **Observable behavior:**
   - Return meaningful responses (not just 200 OK)
   - Emit events that can be verified
   - Structured logs for behavior verification

6. **Test data management:**
   - Factories/builders for test data
   - Database cleanup between tests (Testcontainers per test)
   - Shared fixtures for common scenarios

**What I look for in code reviews:**
- Can this be unit tested without Spring context?
- Are external calls behind interfaces?
- Are there test-unfriendly patterns (static methods, singletons, hidden state)?
- Is the test covering behavior or implementation details?

---

### Q10: How do you set up Selenium automation for web application testing?

**Answer:**

**Page Object Model (POM) pattern:**
```java
public class SubscriberListPage {
    private WebDriver driver;
    
    @FindBy(id = "search-input")
    private WebElement searchInput;
    
    @FindBy(css = ".subscriber-row")
    private List<WebElement> subscriberRows;
    
    @FindBy(id = "add-subscriber-btn")
    private WebElement addButton;
    
    public SubscriberListPage(WebDriver driver) {
        this.driver = driver;
        PageFactory.initElements(driver, this);
    }
    
    public SubscriberListPage searchByName(String name) {
        searchInput.clear();
        searchInput.sendKeys(name);
        searchInput.sendKeys(Keys.ENTER);
        new WebDriverWait(driver, Duration.ofSeconds(5))
            .until(ExpectedConditions.invisibilityOfElementLocated(By.id("spinner")));
        return this;
    }
    
    public int getResultCount() {
        return subscriberRows.size();
    }
    
    public CreateSubscriberPage clickAdd() {
        addButton.click();
        return new CreateSubscriberPage(driver);
    }
}
```

**Test class:**
```java
@ExtendWith(SeleniumExtension.class)
class SubscriberE2ETest {

    @BeforeEach
    void setup() {
        WebDriverManager.chromedriver().setup();
        driver = new ChromeDriver(new ChromeOptions().addArguments("--headless"));
    }

    @Test
    void shouldCreateAndSearchSubscriber() {
        SubscriberListPage listPage = new SubscriberListPage(driver);
        driver.get("https://app-staging.thestandard.com/subscribers");
        
        CreateSubscriberPage createPage = listPage.clickAdd();
        createPage.fillName("Test User")
                  .fillEmail("test@example.com")
                  .submit();
        
        listPage.searchByName("Test User");
        assertThat(listPage.getResultCount()).isGreaterThan(0);
    }
}
```

**CI integration (headless Chrome in Docker):**
```yaml
- task: CmdLine@2
  inputs:
    script: |
      mvn test -Dselenium.browser=chrome-headless \
        -Dselenium.baseUrl=https://app-staging.thestandard.com \
        -pl e2e-tests
```

---

### Q11: How do you implement performance testing as part of CI/CD (shift-left performance)?

**Answer:**

**Shift-left performance = catch regressions early, not just before release.**

**Strategy:**
```
PR Build:        Gatling smoke test (5 users, 30s) → detect obvious regressions
Dev Deploy:      Gatling load test (50 users, 5 min) → validate feature performance
Staging Deploy:  Full load test (production-like traffic, 30 min) → NFR sign-off
Pre-Prod:        Soak test (sustained load, 4-8 hours) → memory leaks, resource issues
```

**Performance baseline in CI:**
```java
// Gatling assertion — fails build if regression detected
setUp(
    scenario.injectOpen(rampUsers(50).during(60))
).assertions(
    global().responseTime().percentile3().lt(500),       // p95 < 500ms
    global().responseTime().percentile4().lt(1000),      // p99 < 1000ms
    global().successfulRequests().percent().gt(99.5),    // > 99.5% success
    forAll().responseTime().percentile3().lt(800)        // Per-request p95
);
```

**Performance comparison (detect regression):**
```bash
# Compare current run against baseline
gatling-report-compare \
  --baseline results/baseline.json \
  --current results/current.json \
  --threshold 10  # Fail if > 10% slower
```

**Azure DevOps performance gate:**
```yaml
- stage: PerformanceGate
  jobs:
    - job: LoadTest
      steps:
        - script: mvn gatling:test
        - task: PublishBuildArtifacts@1
          inputs:
            pathToPublish: 'target/gatling'
            artifactName: 'performance-report'
        - script: |
            # Parse results and fail if p99 > threshold
            python scripts/check_performance.py \
              --results target/gatling/results \
              --max-p99 500 \
              --max-error-rate 0.5
```
