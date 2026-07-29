# Kafka for Sling TV Project — Beginner-Friendly Q&A with Scenarios

> This document bridges the gap: you understand Kafka concepts but need to articulate how you *used* Kafka in the Sling TV migration context. Every answer is crafted so you can speak confidently about event-driven patterns in your project.

---

## Part 1: Your Story — How Kafka Fits in Sling TV Migration

### The Narrative (memorize this)

> "At Dish, I led the migration of 80+ legacy Ruby on Rails APIs to Java microservices for Sling TV. The legacy system used synchronous REST calls between services, creating tight coupling and cascading failures. As part of the new architecture, we introduced Apache Kafka as the event backbone for inter-service communication. This decoupled services, enabled independent scaling, and gave us event replay capability for debugging production issues. I designed the event-driven patterns, defined topic naming conventions, chose partition strategies based on key cardinality, and established consumer group configurations across teams."

---

## Part 2: Fundamental Concepts (Learn These First)

### Q1: In simple terms, what is Kafka and why did you use it at Sling TV?

**Answer:**

Think of Kafka as a **distributed commit log** — like a never-ending, append-only file that multiple systems can write to and read from independently.

**Why we used it:**
```
BEFORE (Ruby on Rails monolith):
  User subscribes → API calls billing (sync) → calls notification (sync) → calls analytics (sync)
  If billing is slow → EVERYTHING is slow → cascading failures

AFTER (Java microservices + Kafka):
  User subscribes → Subscription Service publishes "subscription.created" event to Kafka
  Billing Service → reads event, processes payment (at its own pace)
  Notification Service → reads event, sends email (at its own pace)
  Analytics Service → reads event, updates dashboard (at its own pace)
```

**Benefits we got:**
- Services don't wait for each other (async)
- If Billing is down for 5 minutes, messages queue up in Kafka — no data loss
- Adding a new consumer (e.g., Fraud Detection) doesn't require changing the producer
- We can replay events to debug issues or rebuild state

---

### Q2: Explain the key Kafka components using your project as an example.

**Answer:**

| Component | What It Is | Our Sling Example |
|-----------|-----------|-------------------|
| **Topic** | A category of messages | `subscription.created`, `payment.processed`, `user.updated` |
| **Partition** | A topic is split into partitions for parallel processing | `subscription.created` has 12 partitions (one per consumer instance) |
| **Producer** | Service that publishes events | Subscription Service publishes when a user subscribes |
| **Consumer** | Service that reads events | Billing Service reads subscription events |
| **Consumer Group** | Multiple instances of the same service sharing the work | 4 instances of Billing Service form group "billing-consumer-group" |
| **Offset** | Position marker — how far a consumer has read | Billing has read up to offset 15,234 on partition 3 |
| **Broker** | A Kafka server | We had 3 brokers for fault tolerance |
| **Key** | Determines which partition a message goes to | We used `subscriberId` as key so all events for a subscriber are ordered |

---

### Q3: What does "event-driven architecture" mean in the context of your migration?

**Answer:**

Instead of services calling each other directly (request-response), services communicate by **publishing events about what happened** and other services **react to those events**.

**The shift I drove:**

```
Synchronous (old Rails):
  POST /subscribe → Rails controller → calls BillingAPI.charge() → calls NotificationAPI.send() → returns 200

Event-Driven (new Java):
  POST /subscribe → SubscriptionService saves to DB → publishes "subscription.created" to Kafka → returns 202 Accepted
  
  Independently:
  BillingService listens → charges card → publishes "payment.completed"
  NotificationService listens → sends welcome email
  AnalyticsService listens → increments subscriber count
```

**Key patterns I implemented:**
1. **Event Notification** — lightweight event with just IDs, consumer fetches full data if needed
2. **Event-Carried State Transfer** — event contains all data needed, no callback required
3. **Event Sourcing** — for subscription lifecycle tracking (created → trial → active → cancelled)

---

## Part 3: Interview Questions They'll Ask About Your Sling Project

### Q4: Walk me through how you designed the event-driven architecture for Sling TV.

**Answer (use this narrative):**

"When I took over the Sling TV migration, the 80+ Rails APIs were tightly coupled with synchronous REST calls. A failure in one service would cascade across the system.

**My design approach was:**

1. **Identified event boundaries:** Mapped every synchronous call and asked — 'Does this caller need an immediate response, or is it just notifying?'
   - Needed immediate: authentication, content authorization → kept as REST
   - Didn't need immediate: billing, notifications, analytics, recommendations → moved to Kafka events

2. **Defined event contracts:**
   ```json
   // Topic: subscription.created
   {
     "eventId": "uuid",
     "eventType": "subscription.created",
     "timestamp": "2024-01-15T10:30:00Z",
     "data": {
       "subscriberId": "sub-12345",
       "planId": "sling-orange",
       "startDate": "2024-01-15",
       "channel": "web"
     }
   }
   ```

3. **Chose partition keys for ordering:**
   - `subscriberId` as key → all events for same subscriber go to same partition → ordering preserved
   - This ensures billing sees 'subscription.created' before 'subscription.upgraded' for the same subscriber

4. **Set topic configurations:**
   - Replication factor: 3 (tolerate 1 broker failure)
   - Partitions: 12 per topic (matched our consumer scaling target)
   - Retention: 7 days for operational topics, 30 days for audit topics

5. **Established consumer patterns:**
   - Each downstream service has its own consumer group
   - Dead Letter Queue (DLQ) for messages that fail processing after 3 retries
   - Idempotent consumers (using eventId to prevent duplicate processing)"

---

### Q5: How did you decide which interactions should be synchronous (REST) vs asynchronous (Kafka)?

**Answer:**

**My decision framework:**

| Criteria | Use REST (sync) | Use Kafka (async) |
|----------|----------------|-------------------|
| Client needs response immediately? | Yes (auth, content fetch) | No (billing, notifications) |
| Can tolerate seconds of delay? | No | Yes |
| Failure of downstream is critical? | Yes (can't proceed without it) | No (can retry later) |
| Multiple consumers need the same data? | No (1:1 call) | Yes (fan-out) |
| Need replay/audit trail? | Not critical | Yes |

**Sling examples:**

| Interaction | Choice | Why |
|-------------|--------|-----|
| User login → Auth service | REST | Need token immediately |
| User plays video → Content auth | REST | Can't play without authorization |
| User subscribes → Billing | Kafka | Can confirm subscription and charge async (within seconds) |
| User subscribes → Send welcome email | Kafka | Not time-critical |
| Payment succeeds → Activate subscription | Kafka | Event triggers state change |
| User cancels → Analytics tracking | Kafka | Fan-out to many consumers |

---

### Q6: How did you handle message ordering for subscriber events?

**Answer:**

"Ordering was critical for us. Consider this scenario:
```
Event 1: subscription.created (subscriberId: 12345)
Event 2: subscription.upgraded (subscriberId: 12345)
Event 3: subscription.cancelled (subscriberId: 12345)
```

If Billing processes event 3 before event 1, it would try to cancel a subscription that doesn't exist yet.

**My solution:**
- Used `subscriberId` as the Kafka message key
- Kafka guarantees: all messages with the same key go to the same partition
- Within a partition, messages are strictly ordered
- So all events for subscriber 12345 are always processed in order

**Trade-off I accepted:**
- This means if subscriber 12345 has a slow event, it blocks other subscribers on the same partition
- With 12 partitions and millions of subscribers, the distribution is good enough that hot-partition issues are rare
- For the rare 'whale' subscriber with massive activity, we could move them to a dedicated partition — but never needed to

**What I told the team:**
- Never process messages from the same partition in parallel (breaks ordering)
- If you need to parallelize, you can parallelize *across* partitions (each consumer instance handles different partitions)"


---

### Q7: What happens when a consumer fails to process a message? How did you handle errors?

**Answer:**

"This was one of the first things I designed — because in a distributed system, failures are normal.

**Our error handling strategy:**

```
Message arrives at consumer
    ↓
Try processing
    ↓ (success) → commit offset, move on
    ↓ (failure)
Retry up to 3 times (with exponential backoff: 1s, 5s, 15s)
    ↓ (still failing)
Send to Dead Letter Queue (DLQ) topic: subscription.created.dlq
    ↓
Commit offset on original topic (don't block other messages)
    ↓
Alert on-call via PagerDuty if DLQ messages exceed threshold
```

**Spring Kafka implementation:**
```java
@Configuration
public class KafkaConsumerConfig {

    @Bean
    public DefaultErrorHandler errorHandler(KafkaTemplate<String, Object> kafkaTemplate) {
        // Retry 3 times with backoff
        BackOff backOff = new ExponentialBackOff(1000L, 3.0); // 1s, 3s, 9s
        
        // After retries exhausted, send to DLQ
        DeadLetterPublishingRecoverer recoverer = 
            new DeadLetterPublishingRecoverer(kafkaTemplate);
        
        return new DefaultErrorHandler(recoverer, backOff);
    }
}
```

**Why this approach:**
- We don't block the partition (other subscribers' events keep flowing)
- Failed messages are preserved in DLQ (we can replay them after fixing the issue)
- We have visibility into failure rate (monitoring on DLQ topic size)
- On-call can investigate and replay DLQ messages after fixing root cause"

---

### Q8: How did you ensure no duplicate processing when a consumer restarts?

**Answer:**

"Duplicate processing is the most common issue in Kafka. It happens because:
- Consumer processes message → crashes before committing offset → restarts → processes same message again

**Our approach — idempotent consumers:**

```java
@KafkaListener(topics = "subscription.created")
public void handleSubscriptionCreated(SubscriptionEvent event) {
    // Idempotency check using eventId
    if (processedEventRepository.existsByEventId(event.getEventId())) {
        log.info("Event {} already processed, skipping", event.getEventId());
        return;  // Already processed, skip
    }
    
    // Process the event
    billingService.createBillingAccount(event.getData());
    
    // Record that we've processed this event
    processedEventRepository.save(new ProcessedEvent(event.getEventId(), Instant.now()));
}
```

**Alternatively, for database operations — use upserts:**
```sql
-- Instead of INSERT (which fails on duplicate)
INSERT INTO billing_account (subscriber_id, plan_id, status)
VALUES ('sub-12345', 'sling-orange', 'ACTIVE')
ON CONFLICT (subscriber_id) DO UPDATE SET plan_id = EXCLUDED.plan_id;
```

**Key principle I taught the team:**
> 'Design your consumers to be safely called twice with the same message. If you can't make it idempotent, you need exactly-once semantics — which is more complex.'

For Sling, idempotent consumers solved 99% of our cases."

---

### Q9: How did you monitor Kafka health in production?

**Answer:**

"We had three levels of monitoring:

**1. Consumer lag (most critical metric):**
```
consumer_lag = latest_offset (what producer wrote) - committed_offset (what consumer has processed)
```
- If lag is growing → consumer can't keep up
- Alert threshold: > 10,000 messages for 5 minutes
- Dashboard showed lag per consumer group, per partition

**2. Broker health:**
- Under-replicated partitions → broker is struggling
- Active controller count (should always be 1)
- Request latency (p99)
- Disk usage per broker

**3. Application-level metrics:**
- Events published per second (per topic)
- Events consumed per second (per consumer group)
- DLQ message count (should be near zero)
- Processing time per message (p95)

**Tools we used:**
- Prometheus + Grafana for Kafka metrics (JMX exporter)
- Dynatrace for application-level tracing (seeing events flow through services)
- PagerDuty alerts for consumer lag and DLQ spikes

**Real incident example:**
One day, Billing consumer lag spiked to 500K messages. Investigation:
- Billing service was making a sync call to a payment gateway per message
- Payment gateway had a timeout issue (5s per call)
- Fix: batch payment calls + increase consumer instances from 4 to 12
- Lag recovered in 20 minutes once we deployed the fix"

---

### Q10: How many partitions did you use and why?

**Answer:**

"For the Sling TV topics, I used this reasoning:

**Step 1 — Consumer parallelism:**
- We planned for 12 consumer instances per service (based on Kubernetes pod count)
- Partitions ≥ consumers, so minimum 12 partitions

**Step 2 — Throughput:**
- Peak during Sunday NFL: ~5,000 events/sec on subscription topics
- Each partition handles ~10MB/s easily
- 12 partitions was more than enough for throughput

**Step 3 — Key distribution:**
- We had millions of subscriber IDs as keys
- With 12 partitions, each partition gets roughly equal distribution
- No hot partition risk with high-cardinality keys

**Final decision: 12 partitions for high-traffic topics, 6 for low-traffic.**

**Why not more?**
- More partitions = more files on broker disk = more memory overhead
- More partitions = longer consumer group rebalances
- More partitions = more leader elections on broker failure
- 12 was the sweet spot for our scale

**Important lesson I learned:**
- You can increase partitions later, but you can NEVER decrease them
- Increasing partitions breaks key ordering temporarily (key→partition mapping changes)
- So start conservative, scale up only when needed"

---

## Part 4: Deep-Dive Scenarios (What Interviewers Will Push On)

### Q11: Scenario — Your Kafka consumer is processing slowly. Consumer lag is growing. Walk me through how you diagnose and fix.

**Answer:**

"I'd approach this systematically:

**Step 1 — Identify which consumer group and partition:**
```bash
kafka-consumer-groups --bootstrap-server kafka:9092 --describe --group billing-consumer-group
```
Output shows lag per partition. Is it one partition or all?

**Step 2 — Diagnose based on pattern:**

| Pattern | Likely Cause | Fix |
|---------|-------------|-----|
| All partitions lagging equally | Processing is slow per message | Optimize processing code |
| One partition lagging, others fine | Hot partition (one key dominates) | Check key distribution |
| Lag appeared suddenly | New deployment, downstream slow | Check recent changes, downstream health |
| Lag growing during peak only | Under-provisioned consumers | Add more consumer instances |

**Step 3 — Common fixes I've applied:**

1. **Processing too slow (most common):**
   - Found: Billing made a synchronous HTTP call per message (200ms each)
   - Fix: Batch messages and make one bulk call, or use async processing
   - Result: 10x throughput improvement

2. **Too few consumers:**
   - Had 4 consumers for 12 partitions → each handles 3 partitions
   - Scaled to 12 consumers → each handles 1 partition → 3x throughput
   
3. **Consumer doing too much work:**
   - Consumer was writing to DB + calling API + sending notification
   - Fix: consumer only writes to DB, publishes new event for downstream actions
   - Single Responsibility Principle for consumers

4. **max.poll.interval.ms exceeded:**
   - Consumer took too long processing a batch → broker kicked it out → rebalance → lag spikes
   - Fix: reduce `max.poll.records` from 500 to 100, increase `max.poll.interval.ms`"

---

### Q12: Scenario — You deployed a new version of a consumer. After deployment, you notice some messages were processed twice. What happened and how do you prevent it?

**Answer:**

"This is a classic scenario during rolling deployments. Here's what happened:

**Root cause:**
```
Old consumer instance (pod-1):
  - Polls messages (offsets 100-150)
  - Starts processing offset 100...
  - Kubernetes terminates pod-1 (rolling update)
  - Processing was in progress — offset 100 NOT committed
  
New consumer instance (pod-2):
  - Joins consumer group → rebalance
  - Gets assigned the same partition
  - Starts from last committed offset (99)
  - Processes offset 100 AGAIN → duplicate!
```

**How I prevented this:**

1. **Graceful shutdown in Spring Boot:**
```java
@PreDestroy
public void onShutdown() {
    // Stop accepting new messages
    kafkaListenerEndpointRegistry.stop();
    // Wait for in-flight messages to finish (up to 30s)
    // Spring's DefaultKafkaConsumerFactory handles this
}
```

```yaml
# application.yml
spring:
  kafka:
    listener:
      ack-mode: MANUAL  # Commit only after processing
  lifecycle:
    timeout-per-shutdown-phase: 30s
```

2. **Kubernetes graceful termination:**
```yaml
# Pod spec
terminationGracePeriodSeconds: 60
lifecycle:
  preStop:
    exec:
      command: ["sleep", "10"]  # Let LB deregister first
```

3. **Idempotent consumers (defense in depth):**
Even with graceful shutdown, network issues can cause duplicates. So every consumer is idempotent — processing the same message twice has no side effect.

**Key takeaway:** 'Duplicates are inevitable in distributed systems. Design consumers to handle them gracefully rather than trying to prevent them entirely.'"

---

### Q13: Scenario — A producer starts publishing messages with a new field that consumers don't expect. Some consumers start failing. What went wrong and how do you prevent it?

**Answer:**

"This is a **schema evolution** problem. Here's what happened and how I'd prevent it:

**What went wrong:**
- Producer team added a new required field to the event JSON
- Old consumers tried to deserialize → failed because field was missing in their model
- Result: consumer errors, messages going to DLQ

**How I prevent this (the rules I set for our team):**

1. **Never add required fields — always optional with defaults:**
   ```json
   // BAD — breaks old consumers
   { "subscriberId": "123", "planId": "orange", "billingCycle": "monthly" }  // new required field!
   
   // GOOD — backward compatible
   { "subscriberId": "123", "planId": "orange", "billingCycle": "monthly" }  // field exists but consumers that don't know about it simply ignore it
   ```

2. **Consumer rule — ignore unknown fields:**
   ```java
   @JsonIgnoreProperties(ignoreUnknown = true)  // ALWAYS add this
   public class SubscriptionEvent {
       private String subscriberId;
       private String planId;
       // If 'billingCycle' comes in, we just ignore it until we update our model
   }
   ```

3. **Schema Registry (ideal state):**
   - Enforce schema compatibility at registration time
   - Before a producer can publish with a new schema, Schema Registry checks compatibility
   - If the change would break consumers → registration is rejected

4. **Versioned topics (alternative):**
   - `subscription.created.v1` → old format
   - `subscription.created.v2` → new format
   - Both run in parallel during migration
   - Consumers migrate at their own pace

**My rule for the team:** 'You can ADD optional fields. You can NEVER remove or rename fields. You can NEVER change field types. Violations break consumers in production.'"

---

### Q14: Scenario — You need to replay all events from the last 24 hours because a bug in the consumer caused incorrect data in the database. How?

**Answer:**

"This is one of the biggest advantages of Kafka — event replay. Here's how I'd do it:

**Step 1 — Stop the consumer (prevent further bad processing):**
```bash
# Scale consumer pods to 0
kubectl scale deployment billing-consumer --replicas=0
```

**Step 2 — Fix the bug and deploy corrected code:**
```bash
# Deploy fixed version but with 0 replicas
kubectl set image deployment/billing-consumer app=billing-consumer:v2-fixed
```

**Step 3 — Reset consumer offset to 24 hours ago:**
```bash
kafka-consumer-groups --bootstrap-server kafka:9092 \
  --group billing-consumer-group \
  --topic subscription.created \
  --reset-offsets \
  --to-datetime 2024-01-14T10:00:00.000 \
  --execute
```

**Step 4 — Clean up bad data (if needed):**
```sql
-- Remove records created by the buggy consumer
DELETE FROM billing_account WHERE created_at > '2024-01-14 10:00:00' AND source = 'kafka-consumer';
```

**Step 5 — Restart consumers:**
```bash
kubectl scale deployment billing-consumer --replicas=12
```

**Step 6 — Monitor:**
- Watch consumer lag decrease back to 0
- Verify data correctness in the database
- Check DLQ for any messages that still fail with the fix

**Why this works:**
- Kafka retains messages for 7 days (our config)
- Consumer offsets are movable — we can go back in time
- Our consumers are idempotent — replaying doesn't create duplicates (uses upserts)

**Key design decision that enabled this:**
- 7-day retention (not 1 hour) gives us a safety net
- Idempotent consumers mean replay is always safe
- Separate consumer groups per service means resetting one doesn't affect others"

---

### Q15: Scenario — Two services both need to react to "subscription.created" events but at different speeds. Billing needs real-time, Analytics can be delayed. How do you design this?

**Answer:**

"This is the beauty of Kafka's consumer group model.

**Design:**
```
Subscription Service (Producer)
        ↓ publishes to
   Topic: subscription.created (12 partitions)
        ↓                           ↓
Consumer Group: billing-cg    Consumer Group: analytics-cg
(4 instances, real-time)      (2 instances, batch-like)
```

**Key insight:** Each consumer group gets its own copy of every message. They don't compete — they each read the entire topic independently.

**Configuration differences:**

| Setting | Billing Consumers | Analytics Consumers |
|---------|------------------|---------------------|
| Instances | 12 (one per partition) | 2 (each handles 6 partitions) |
| `max.poll.records` | 50 (process quickly) | 500 (batch for efficiency) |
| Processing style | One at a time, low latency | Batch insert to analytics DB |
| Error handling | DLQ + alert | DLQ + low-priority alert |
| Lag tolerance | Alert at > 100 messages | Alert at > 100,000 messages |

**Why this works:**
- Billing runs fast with more instances → processes events within milliseconds
- Analytics can fall behind (lag) without affecting Billing at all
- If Analytics consumer crashes, Billing is unaffected
- If we need a third consumer (Fraud Detection), we add a new consumer group — zero changes to producer or existing consumers

**This is what I explained to the team as the 'pub-sub' power of Kafka — one event, multiple independent consumers.'"

---

### Q16: Scenario — You're designing topics for the Sling TV subscription lifecycle. What topics do you create and why?

**Answer:**

"Here's my topic design for the subscription domain:

**Option 1 — One topic per event type (what I chose):**
```
subscription.created
subscription.upgraded
subscription.downgraded
subscription.paused
subscription.resumed
subscription.cancelled
payment.initiated
payment.completed
payment.failed
```

**Why I chose this:**
- Each consumer can subscribe to only the events it cares about
- Billing only reads `subscription.created` and `payment.*`
- Analytics reads all of them
- Simpler consumer logic (no filtering)
- Each topic can have different retention and partition counts

**Option 2 — Single topic with event types (rejected):**
```
subscription.events  (all lifecycle events in one topic)
```

**Why I rejected this:**
- Consumers must filter events they don't care about (wasteful)
- Can't have different retention per event type
- High-volume events (like analytics pings) would share a topic with critical events (payment)
- Harder to monitor — lag on one topic doesn't tell you which event type is slow

**Naming convention I established:**
```
<domain>.<entity>.<action>
subscription.created
payment.completed
user.profile.updated
content.playback.started
```

**Topic configuration:**

| Topic | Partitions | Retention | Key | Why |
|-------|-----------|-----------|-----|-----|
| subscription.created | 12 | 7 days | subscriberId | High volume, order matters |
| subscription.cancelled | 6 | 30 days | subscriberId | Lower volume, audit needed |
| payment.completed | 12 | 30 days | subscriberId | Financial audit |
| payment.failed | 6 | 90 days | subscriberId | Long retention for investigation |
"

---

## Part 5: Spring Boot + Kafka Integration (Code You Should Know)

### Q17: Show me how you implemented a Kafka producer in Spring Boot.

**Answer:**

```java
// Configuration
@Configuration
public class KafkaProducerConfig {

    @Bean
    public ProducerFactory<String, Object> producerFactory() {
        Map<String, Object> config = new HashMap<>();
        config.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka:9092");
        config.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        config.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, JsonSerializer.class);
        config.put(ProducerConfig.ACKS_CONFIG, "all");  // Wait for all replicas
        config.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);  // No duplicates
        config.put(ProducerConfig.RETRIES_CONFIG, 3);
        return new DefaultKafkaProducerFactory<>(config);
    }

    @Bean
    public KafkaTemplate<String, Object> kafkaTemplate() {
        return new KafkaTemplate<>(producerFactory());
    }
}

// Service that publishes events
@Service
@RequiredArgsConstructor
public class SubscriptionEventPublisher {

    private final KafkaTemplate<String, Object> kafkaTemplate;

    public void publishSubscriptionCreated(Subscription subscription) {
        SubscriptionEvent event = SubscriptionEvent.builder()
            .eventId(UUID.randomUUID().toString())
            .eventType("subscription.created")
            .timestamp(Instant.now())
            .subscriberId(subscription.getSubscriberId())
            .planId(subscription.getPlanId())
            .build();

        // Key = subscriberId ensures ordering per subscriber
        kafkaTemplate.send("subscription.created", subscription.getSubscriberId(), event)
            .whenComplete((result, ex) -> {
                if (ex != null) {
                    log.error("Failed to publish event for subscriber {}", 
                        subscription.getSubscriberId(), ex);
                    // Handle failure: retry, dead letter, alert
                } else {
                    log.info("Published subscription.created for {} to partition {} offset {}",
                        subscription.getSubscriberId(),
                        result.getRecordMetadata().partition(),
                        result.getRecordMetadata().offset());
                }
            });
    }
}
```

---

### Q18: Show me how you implemented a Kafka consumer in Spring Boot.

**Answer:**

```java
@Component
@RequiredArgsConstructor
@Slf4j
public class BillingEventConsumer {

    private final BillingService billingService;
    private final ProcessedEventRepository processedEventRepo;

    @KafkaListener(
        topics = "subscription.created",
        groupId = "billing-consumer-group",
        containerFactory = "kafkaListenerContainerFactory"
    )
    public void handleSubscriptionCreated(
            @Payload SubscriptionEvent event,
            @Header(KafkaHeaders.RECEIVED_PARTITION) int partition,
            @Header(KafkaHeaders.OFFSET) long offset,
            Acknowledgment ack) {

        log.info("Received subscription.created: subscriberId={}, partition={}, offset={}",
            event.getSubscriberId(), partition, offset);

        // Idempotency check
        if (processedEventRepo.existsByEventId(event.getEventId())) {
            log.warn("Duplicate event {}, skipping", event.getEventId());
            ack.acknowledge();
            return;
        }

        try {
            // Business logic
            billingService.createBillingAccount(event);

            // Record successful processing
            processedEventRepo.save(new ProcessedEvent(
                event.getEventId(), "subscription.created", Instant.now()
            ));

            // Manually acknowledge (commit offset)
            ack.acknowledge();

        } catch (RetryableException e) {
            // Don't ack — will be retried by error handler
            throw e;
        } catch (Exception e) {
            log.error("Non-retryable error processing event {}", event.getEventId(), e);
            // Error handler will send to DLQ after retries exhausted
            throw e;
        }
    }
}

// Consumer configuration
@Configuration
public class KafkaConsumerConfig {

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, SubscriptionEvent> kafkaListenerContainerFactory() {
        ConcurrentKafkaListenerContainerFactory<String, SubscriptionEvent> factory =
            new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory());
        factory.setConcurrency(3);  // 3 threads per instance
        factory.getContainerProperties().setAckMode(AckMode.MANUAL);
        factory.setCommonErrorHandler(errorHandler());
        return factory;
    }

    @Bean
    public DefaultErrorHandler errorHandler() {
        // Retry 3 times, then send to DLQ
        BackOff backOff = new FixedBackOff(1000L, 3L);
        DeadLetterPublishingRecoverer recoverer = new DeadLetterPublishingRecoverer(kafkaTemplate());
        return new DefaultErrorHandler(recoverer, backOff);
    }
}
```

---

### Q19: How did you test Kafka integration in your project?

**Answer:**

```java
@SpringBootTest
@EmbeddedKafka(
    partitions = 3,
    topics = {"subscription.created", "subscription.created.DLT"},
    brokerProperties = {"listeners=PLAINTEXT://localhost:9092"}
)
class BillingEventConsumerTest {

    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;

    @Autowired
    private BillingRepository billingRepository;

    @Test
    void shouldCreateBillingAccountOnSubscriptionCreated() {
        // Given
        SubscriptionEvent event = SubscriptionEvent.builder()
            .eventId(UUID.randomUUID().toString())
            .subscriberId("sub-123")
            .planId("sling-orange")
            .build();

        // When — publish event
        kafkaTemplate.send("subscription.created", "sub-123", event);

        // Then — verify consumer processed it
        await().atMost(Duration.ofSeconds(10)).untilAsserted(() -> {
            BillingAccount account = billingRepository.findBySubscriberId("sub-123");
            assertThat(account).isNotNull();
            assertThat(account.getPlanId()).isEqualTo("sling-orange");
            assertThat(account.getStatus()).isEqualTo("ACTIVE");
        });
    }

    @Test
    void shouldHandleDuplicateEventsIdempotently() {
        // Given — same event sent twice
        SubscriptionEvent event = SubscriptionEvent.builder()
            .eventId("same-event-id")
            .subscriberId("sub-456")
            .planId("sling-blue")
            .build();

        // When — publish same event twice
        kafkaTemplate.send("subscription.created", "sub-456", event);
        kafkaTemplate.send("subscription.created", "sub-456", event);

        // Then — only one billing account created
        await().atMost(Duration.ofSeconds(10)).untilAsserted(() -> {
            List<BillingAccount> accounts = billingRepository.findAllBySubscriberId("sub-456");
            assertThat(accounts).hasSize(1);  // Not 2!
        });
    }
}
```


---

## Part 6: Quick-Fire Questions (Likely Follow-ups)

### Q20: What is consumer lag and why do you care?

**Answer:** Consumer lag = how many messages the consumer hasn't processed yet. It's the difference between the latest produced offset and the last committed consumer offset.
- Growing lag = consumer can't keep up = data is stale for downstream systems
- Zero lag = real-time processing
- At Sling: Billing had a strict SLA of < 100 messages lag (near real-time). Analytics tolerated up to 100K lag.

---

### Q21: What happens if a Kafka broker goes down?

**Answer:** With replication factor 3:
- Other brokers have copies of all data
- Kafka automatically elects new partition leaders from in-sync replicas
- Producers get a brief error, then auto-discover new leaders via metadata refresh
- Consumers get NOT_LEADER error, refresh metadata, connect to new leader
- Zero data loss (if min.insync.replicas was met)
- At Sling: We had 3 brokers. Lost one broker during a maintenance window — zero impact on consumers.

---

### Q22: What's the difference between a topic and a partition?

**Answer:**
- **Topic** = logical name for a stream of events (like a table name). Example: `subscription.created`
- **Partition** = physical division of a topic for parallelism. A topic with 12 partitions has 12 ordered logs.
- You publish to a topic; Kafka decides which partition based on the message key.
- Ordering is guaranteed within a partition, not across partitions.

---

### Q23: Why did you choose Kafka over RabbitMQ for Sling?

**Answer:**
| Factor | Kafka | RabbitMQ |
|--------|-------|----------|
| Message retention | Yes (days/weeks) | No (consumed = deleted) |
| Replay capability | Yes (seek to offset) | No |
| Throughput | Millions/sec | Tens of thousands/sec |
| Consumer model | Pull (consumer controls pace) | Push (broker pushes to consumer) |
| Ordering | Per partition | Per queue |
| Use case | Event streaming, audit trail | Task queues, RPC |

"We chose Kafka because:
1. We needed event replay for debugging and recovery
2. Multiple consumers needed the same events (fan-out)
3. We needed to retain events for 7-30 days for auditing
4. Our scale (millions of events/day) needed Kafka's throughput
5. We were building an event-driven architecture, not a task queue"

---

### Q24: What is a consumer group and why is it important?

**Answer:**
A consumer group is a set of consumers that cooperate to consume a topic.
- Each partition is assigned to exactly ONE consumer in the group
- If you have 12 partitions and 4 consumers → each consumer handles 3 partitions
- If you have 12 partitions and 12 consumers → each handles 1 partition (max parallelism)
- If you have 12 partitions and 15 consumers → 3 consumers are idle (wasted)

**Why important:**
- Enables horizontal scaling (add consumers to handle more load)
- Guarantees each message is processed exactly once per group
- Different services use different group IDs → each gets its own copy of all messages

---

### Q25: What is the Outbox Pattern and did you use it?

**Answer:**
The Outbox Pattern solves the "dual write" problem: how do you save to DB AND publish to Kafka atomically?

**Problem:**
```java
// What if step 2 fails? DB has data, Kafka doesn't.
// What if step 1 fails after step 2? Kafka has event, DB doesn't.
subscriptionRepo.save(subscription);  // Step 1: write to DB
kafkaTemplate.send("subscription.created", event);  // Step 2: publish to Kafka
```

**Outbox solution:**
```java
@Transactional  // Both happen in ONE database transaction
public void createSubscription(Subscription subscription) {
    subscriptionRepo.save(subscription);  // Save entity
    outboxRepo.save(new OutboxEvent(       // Save event to outbox table
        "subscription.created", 
        subscription.getSubscriberId(),
        toJson(event)
    ));
}

// Separate scheduled job reads outbox table and publishes to Kafka
// After successful Kafka publish, marks outbox entry as "sent"
```

"At Sling, we used this for critical paths like payment events where we couldn't afford inconsistency between our database and Kafka. For less critical paths (analytics, notifications), we accepted the small risk of the dual-write approach with at-least-once delivery."

---

## Part 7: Cheat Sheet — Numbers to Memorize

| What | Value at Sling |
|------|----------------|
| Number of Kafka brokers | 3 |
| Replication factor | 3 |
| min.insync.replicas | 2 |
| Partitions per high-traffic topic | 12 |
| Partitions per low-traffic topic | 6 |
| Consumer instances (Billing) | 12 |
| Consumer instances (Analytics) | 2-4 |
| Retention for operational topics | 7 days |
| Retention for audit/payment topics | 30 days |
| Message format | JSON (with @JsonIgnoreProperties) |
| Peak events/sec (NFL Sunday) | ~5,000 |
| Average events/sec (normal) | ~500-1,000 |
| Consumer lag SLA (Billing) | < 100 messages |
| DLQ retry attempts | 3 |
| Producer acks setting | all |
