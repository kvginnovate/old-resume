# Kafka, Confluent Platform & Apache Flink — Questions & Answers

## Apache Kafka Core

### Q1: Explain Kafka architecture and its core components.

**Answer:**

**Core Components:**

- **Broker:** A Kafka server that stores data and serves clients. A cluster has multiple brokers for fault tolerance.
- **Topic:** A logical category/feed to which records are published. Analogous to a table in a database.
- **Partition:** A topic is split into partitions for parallelism. Each partition is an ordered, immutable log.
- **Producer:** Publishes records to topics. Decides which partition to write to (key-based or round-robin).
- **Consumer:** Reads records from topics. Part of a consumer group for parallel processing.
- **Consumer Group:** Multiple consumers sharing the load of reading a topic. Each partition is consumed by exactly one consumer in a group.
- **ZooKeeper/KRaft:** Cluster metadata management. KRaft (Kafka Raft) replaces ZooKeeper in newer versions.
- **Offset:** Sequential ID for each record in a partition. Consumers track their position via offsets.

**Key guarantees:**
- Ordering within a partition (not across partitions)
- At-least-once delivery (default), exactly-once with transactions
- Durability via replication (configurable replication factor)


---

### Q2: What are Kafka's delivery guarantees and how do you achieve exactly-once semantics?

**Answer:**

**Three delivery semantics:**

| Semantic | Description | How |
|----------|-------------|-----|
| At-most-once | Message may be lost, never redelivered | Auto-commit offsets before processing |
| At-least-once | Message never lost, may be duplicated | Commit offset after processing (default) |
| Exactly-once | Message delivered exactly once | Idempotent producer + transactions |

**Exactly-once implementation:**

1. **Idempotent Producer:**
```properties
enable.idempotence=true
acks=all
retries=Integer.MAX_VALUE
max.in.flight.requests.per.connection=5
```
Kafka assigns a producer ID and sequence number — broker deduplicates.

2. **Transactions (for read-process-write):**
```java
producer.initTransactions();
try {
    producer.beginTransaction();
    producer.send(new ProducerRecord<>("output-topic", key, value));
    producer.sendOffsetsToTransaction(offsets, consumerGroupId);
    producer.commitTransaction();
} catch (Exception e) {
    producer.abortTransaction();
}
```

3. **Consumer isolation level:**
```properties
isolation.level=read_committed
```
Only reads committed messages (ignores aborted transactions).

---

### Q3: How do you design Kafka topics for a microservices architecture?

**Answer:**

**Topic design principles:**

1. **One topic per event type:**
   - `order.created`, `order.updated`, `payment.processed`
   - Not one giant "events" topic

2. **Partition key selection:**
   - Choose key that groups related events: `customerId`, `orderId`
   - Ensures ordering for related events
   - Consider cardinality (avoid hot partitions)

3. **Partition count:**
   - Determines max parallelism (consumers in a group ≤ partitions)
   - Start with: expected throughput / throughput per partition
   - Rule of thumb: max(expected consumers, throughput / 10MB/s)
   - Can only increase, never decrease

4. **Replication factor:**
   - Minimum 3 for production (tolerates 1 broker failure)
   - `min.insync.replicas=2` for durability

5. **Retention policy:**
   - Time-based: `retention.ms=604800000` (7 days)
   - Size-based: `retention.bytes`
   - Compacted topics for state (latest value per key)

6. **Naming convention:**
   ```
   <domain>.<entity>.<event-type>
   e.g., subscriber.account.created
         payment.transaction.completed
   ```


---

### Q4: How does Kafka consumer group rebalancing work? What are the strategies?

**Answer:**

**Rebalancing** is the process of redistributing partitions among consumers in a group when:
- A consumer joins or leaves the group
- A consumer is deemed dead (missed heartbeat)
- Topic partitions change

**Rebalancing strategies:**

| Strategy | Behavior | Use Case |
|----------|----------|----------|
| Eager (Range/RoundRobin) | Revokes ALL partitions, reassigns | Simple, but causes stop-the-world |
| Cooperative (Sticky) | Only revokes partitions that need to move | Minimizes disruption |
| Static Membership | Consumer has fixed `group.instance.id`, no rebalance on short disconnect | Stateful consumers |

**Cooperative Sticky (recommended):**
```properties
partition.assignment.strategy=org.apache.kafka.clients.consumer.CooperativeStickyAssignor
```

**Avoiding unnecessary rebalances:**
```properties
session.timeout.ms=45000       # Time before consumer is considered dead
heartbeat.interval.ms=15000    # Heartbeat frequency
max.poll.interval.ms=300000    # Max time between poll() calls
max.poll.records=500           # Limit records per poll to avoid timeout
```

---

### Q5: What is Kafka Connect and how does it work?

**Answer:**

Kafka Connect is a framework for streaming data between Kafka and external systems without writing custom producer/consumer code.

**Architecture:**
```
Source System → Source Connector → Kafka Topic → Sink Connector → Target System
```

**Components:**
- **Worker:** JVM process that runs connectors (standalone or distributed mode)
- **Connector:** Defines the job (configuration, source/sink type)
- **Task:** Actual unit of work (parallelism within a connector)
- **Converter:** Serialization format (JSON, Avro, Protobuf)
- **Transform (SMT):** Single Message Transforms — lightweight in-flight transformations

**Example — JDBC Source Connector:**
```json
{
  "name": "jdbc-source-subscribers",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
    "connection.url": "jdbc:postgresql://db:5432/subscribers",
    "table.whitelist": "subscriber,subscription",
    "mode": "timestamp+incrementing",
    "timestamp.column.name": "updated_at",
    "incrementing.column.name": "id",
    "topic.prefix": "db.",
    "key.converter": "io.confluent.connect.avro.AvroConverter",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "transforms": "addField",
    "transforms.addField.type": "org.apache.kafka.connect.transforms.InsertField$Value",
    "transforms.addField.static.field": "source",
    "transforms.addField.static.value": "subscriber-db"
  }
}
```

**Single Message Transforms (SMTs):**
- `InsertField` — Add static/dynamic fields
- `ReplaceField` — Rename or drop fields
- `MaskField` — Mask sensitive data
- `TimestampRouter` — Route to topic by timestamp
- `RegexRouter` — Route to topic by regex on topic name
- `Filter` — Drop messages based on condition

**Custom connector development:**
- Implement `SourceConnector` + `SourceTask` (for source)
- Implement `SinkConnector` + `SinkTask` (for sink)
- Package as a JAR, deploy to Connect worker plugin path

---

## Confluent Platform

### Q6: What is Confluent Platform and how does it extend Apache Kafka?

**Answer:**

Confluent Platform is an enterprise distribution of Apache Kafka with additional components:

| Component | Purpose |
|-----------|---------|
| Confluent Server | Enhanced Kafka broker (Self-Balancing, Tiered Storage) |
| Schema Registry | Schema management and evolution for Kafka messages |
| Kafka Connect | Pre-built connectors (200+ certified) |
| ksqlDB | Stream processing with SQL syntax |
| Control Center | GUI for monitoring, topic management, consumer lag |
| Confluent REST Proxy | HTTP interface to Kafka |
| Cluster Linking | Replicate topics across clusters |
| Tiered Storage | Move cold data to object storage (S3/Azure Blob) |

**Key enterprise features not in Apache Kafka:**
- Self-Balancing Clusters (automatic partition rebalancing)
- Tiered Storage (infinite retention without disk cost)
- Multi-Region Clusters (geo-replication)
- RBAC (Role-Based Access Control)
- Audit Logs
- Schema validation at broker level

---

### Q7: What is Schema Registry and why is it critical?

**Answer:**

Schema Registry is a centralized service that stores and manages schemas for Kafka messages, enabling schema evolution without breaking consumers.

**Why it's critical:**
- **Contract enforcement:** Producers must publish data matching the registered schema
- **Evolution:** Schemas can evolve safely (add/remove fields) with compatibility checks
- **Decoupling:** Producer and consumer don't need to be deployed together
- **Serialization efficiency:** Avro/Protobuf much smaller than JSON

**Supported formats:** Avro (most common), Protobuf, JSON Schema

**Compatibility modes:**

| Mode | Rule |
|------|------|
| BACKWARD | New schema can read old data (can add optional fields, remove fields) |
| FORWARD | Old schema can read new data (can remove optional fields, add fields) |
| FULL | Both backward and forward compatible |
| NONE | No compatibility check |

**Example Avro schema evolution (BACKWARD compatible):**
```json
// V1
{
  "type": "record",
  "name": "Subscriber",
  "fields": [
    {"name": "id", "type": "string"},
    {"name": "name", "type": "string"}
  ]
}

// V2 — adding optional field (BACKWARD compatible)
{
  "type": "record",
  "name": "Subscriber",
  "fields": [
    {"name": "id", "type": "string"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": ["null", "string"], "default": null}
  ]
}
```

**Spring Boot integration:**
```yaml
spring:
  kafka:
    producer:
      key-serializer: io.confluent.kafka.serializers.KafkaAvroSerializer
      value-serializer: io.confluent.kafka.serializers.KafkaAvroSerializer
    properties:
      schema.registry.url: http://schema-registry:8081
      auto.register.schemas: false  # Force schema registration in CI/CD
```


---

### Q8: How do you build a custom Kafka Connect connector?

**Answer:**

**Source Connector structure:**

```java
// 1. Connector class — configuration and task creation
public class CustomSourceConnector extends SourceConnector {
    
    @Override
    public void start(Map<String, String> props) {
        // Initialize configuration
    }
    
    @Override
    public Class<? extends Task> taskClass() {
        return CustomSourceTask.class;
    }
    
    @Override
    public List<Map<String, String>> taskConfigs(int maxTasks) {
        // Divide work among tasks
        List<Map<String, String>> configs = new ArrayList<>();
        for (int i = 0; i < maxTasks; i++) {
            Map<String, String> taskConfig = new HashMap<>(this.config);
            taskConfig.put("task.id", String.valueOf(i));
            configs.add(taskConfig);
        }
        return configs;
    }
    
    @Override
    public ConfigDef config() {
        return new ConfigDef()
            .define("api.url", ConfigDef.Type.STRING, ConfigDef.Importance.HIGH, "API endpoint");
    }
}

// 2. Task class — actual data polling
public class CustomSourceTask extends SourceTask {
    
    @Override
    public List<SourceRecord> poll() throws InterruptedException {
        // Fetch data from source system
        List<SourceRecord> records = new ArrayList<>();
        
        Data data = fetchFromExternalAPI();
        
        Map<String, Object> sourcePartition = Map.of("source", "api");
        Map<String, Object> sourceOffset = Map.of("position", data.getOffset());
        
        records.add(new SourceRecord(
            sourcePartition,
            sourceOffset,
            "target-topic",
            Schema.STRING_SCHEMA,
            data.getKey(),
            schema,
            data.getValue()
        ));
        
        return records;
    }
}
```

**Packaging and deployment:**
1. Build as JAR with dependencies
2. Place in Connect worker's `plugin.path` directory
3. Restart Connect worker or use REST API to register

---

## Apache Flink

### Q9: What is Apache Flink and how does it differ from Kafka Streams?

**Answer:**

Apache Flink is a distributed stream processing framework for stateful computations over bounded (batch) and unbounded (stream) data.

| Feature | Apache Flink | Kafka Streams |
|---------|-------------|---------------|
| Deployment | Standalone cluster (JobManager + TaskManagers) | Embedded in application (library) |
| Scaling | Cluster-level, independent of Kafka | Tied to Kafka partitions |
| State management | RocksDB + checkpoints to external storage | RocksDB + Kafka changelog topics |
| Processing model | Full DAG (complex topologies) | Linear topology |
| SQL support | Flink SQL (full SQL engine) | ksqlDB (separate product) |
| Batch + Stream | Unified API for both | Stream only |
| Exactly-once | Checkpointing + 2-phase commit | Kafka transactions |
| Windowing | Advanced (session, tumbling, sliding, custom) | Basic (tumbling, sliding, session) |
| Use case | Complex event processing, large-scale | Lightweight, Kafka-native processing |

**When to use Flink over Kafka Streams:**
- Complex event processing (CEP) with pattern matching
- Need SQL interface for analysts
- Batch + stream unified processing
- Processing data from multiple sources (not just Kafka)
- Very large state that needs external checkpointing
- UDFs and custom processing logic

---

### Q10: Explain Flink's architecture and execution model.

**Answer:**

**Components:**

1. **JobManager (master):**
   - Receives job submission
   - Builds execution graph
   - Coordinates checkpoints
   - Handles failure recovery
   - Manages resource allocation

2. **TaskManager (worker):**
   - Executes tasks (operators)
   - Manages memory and network buffers
   - Reports status to JobManager
   - Multiple task slots per TaskManager

3. **Execution model:**
   ```
   Logical Plan (SQL/DataStream API)
       ↓
   Optimized Plan
       ↓
   Physical Plan (JobGraph)
       ↓
   Execution Graph (distributed across TaskManagers)
   ```

4. **State backends:**
   - `HashMapStateBackend` — in JVM heap (fast, limited by memory)
   - `EmbeddedRocksDBStateBackend` — on disk (larger state, slightly slower)

5. **Checkpointing:**
   - Periodic snapshots of operator state
   - Stored externally (S3, HDFS, Azure Blob)
   - Enables exactly-once recovery
   - Aligned vs unaligned checkpoints

---

### Q11: What is Flink SQL and how do you use it with Kafka?

**Answer:**

Flink SQL allows stream processing using standard SQL syntax.

**Creating a Kafka source table:**
```sql
CREATE TABLE orders (
    order_id STRING,
    customer_id STRING,
    amount DECIMAL(10, 2),
    order_time TIMESTAMP(3),
    WATERMARK FOR order_time AS order_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'orders',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'flink-orders',
    'format' = 'avro-confluent',
    'avro-confluent.url' = 'http://schema-registry:8081',
    'scan.startup.mode' = 'earliest-offset'
);
```

**Creating a sink table:**
```sql
CREATE TABLE order_summary (
    customer_id STRING,
    window_start TIMESTAMP(3),
    window_end TIMESTAMP(3),
    total_orders BIGINT,
    total_amount DECIMAL(10, 2),
    PRIMARY KEY (customer_id, window_start) NOT ENFORCED
) WITH (
    'connector' = 'kafka',
    'topic' = 'order-summary',
    'properties.bootstrap.servers' = 'kafka:9092',
    'format' = 'avro-confluent',
    'avro-confluent.url' = 'http://schema-registry:8081'
);
```

**Windowed aggregation:**
```sql
INSERT INTO order_summary
SELECT
    customer_id,
    window_start,
    window_end,
    COUNT(*) AS total_orders,
    SUM(amount) AS total_amount
FROM TABLE(
    TUMBLE(TABLE orders, DESCRIPTOR(order_time), INTERVAL '1' HOUR)
)
GROUP BY customer_id, window_start, window_end;
```

**Joins:**
```sql
-- Stream-to-stream join (temporal)
SELECT o.order_id, o.amount, p.payment_status
FROM orders o
JOIN payments p
ON o.order_id = p.order_id
WHERE p.payment_time BETWEEN o.order_time AND o.order_time + INTERVAL '30' MINUTE;
```


---

### Q12: What are Flink UDFs (User Defined Functions)? How do you create them?

**Answer:**

UDFs extend Flink SQL with custom logic. Three types:

**1. Scalar Function (one row → one value):**
```java
public class MaskEmail extends ScalarFunction {
    
    public String eval(String email) {
        if (email == null) return null;
        int atIndex = email.indexOf('@');
        if (atIndex <= 1) return email;
        return email.charAt(0) + "***" + email.substring(atIndex);
    }
}

// Register and use:
// CREATE FUNCTION mask_email AS 'com.example.MaskEmail';
// SELECT mask_email(email) FROM subscribers;
```

**2. Table Function (one row → multiple rows):**
```java
public class SplitTags extends TableFunction<Row> {
    
    @DataTypeHint("ROW<tag STRING, position INT>")
    public void eval(String tags) {
        if (tags == null) return;
        String[] parts = tags.split(",");
        for (int i = 0; i < parts.length; i++) {
            collect(Row.of(parts[i].trim(), i));
        }
    }
}

// Usage:
// SELECT order_id, tag, position
// FROM orders, LATERAL TABLE(split_tags(tags));
```

**3. Aggregate Function (multiple rows → one value):**
```java
public class WeightedAvg extends AggregateFunction<Double, WeightedAvgAccumulator> {
    
    @Override
    public WeightedAvgAccumulator createAccumulator() {
        return new WeightedAvgAccumulator();
    }
    
    public void accumulate(WeightedAvgAccumulator acc, Double value, Integer weight) {
        acc.sum += value * weight;
        acc.count += weight;
    }
    
    @Override
    public Double getValue(WeightedAvgAccumulator acc) {
        return acc.count == 0 ? null : acc.sum / acc.count;
    }
    
    public void retract(WeightedAvgAccumulator acc, Double value, Integer weight) {
        acc.sum -= value * weight;
        acc.count -= weight;
    }
}

// Usage:
// SELECT customer_id, weighted_avg(rating, order_count) FROM reviews GROUP BY customer_id;
```

**Registration in Flink SQL:**
```sql
CREATE FUNCTION mask_email AS 'com.example.udf.MaskEmail';
CREATE FUNCTION split_tags AS 'com.example.udf.SplitTags';
CREATE FUNCTION weighted_avg AS 'com.example.udf.WeightedAvg';
```

---

### Q13: Explain Flink windowing concepts.

**Answer:**

Windows group unbounded streams into finite chunks for aggregation.

**Window Types:**

| Type | Description | Use Case |
|------|-------------|----------|
| Tumbling | Fixed-size, non-overlapping | Hourly/daily aggregates |
| Sliding | Fixed-size, overlapping | Moving averages |
| Session | Gap-based, variable size | User activity sessions |
| Global | All elements in one window | Custom triggers |

**Flink SQL examples:**

```sql
-- Tumbling window (1 hour)
SELECT customer_id, COUNT(*) as order_count
FROM TABLE(TUMBLE(TABLE orders, DESCRIPTOR(order_time), INTERVAL '1' HOUR))
GROUP BY customer_id, window_start, window_end;

-- Sliding window (1 hour window, 15 min slide)
SELECT customer_id, COUNT(*) as order_count
FROM TABLE(HOP(TABLE orders, DESCRIPTOR(order_time), INTERVAL '15' MINUTE, INTERVAL '1' HOUR))
GROUP BY customer_id, window_start, window_end;

-- Session window (30 min gap)
SELECT customer_id, COUNT(*) as order_count
FROM TABLE(SESSION(TABLE orders, DESCRIPTOR(order_time), INTERVAL '30' MINUTE))
GROUP BY customer_id, window_start, window_end;

-- Cumulate window (1 day max, 1 hour steps)
SELECT customer_id, SUM(amount) as running_total
FROM TABLE(CUMULATE(TABLE orders, DESCRIPTOR(order_time), INTERVAL '1' HOUR, INTERVAL '1' DAY))
GROUP BY customer_id, window_start, window_end;
```

**Watermarks:**
- Handle late-arriving data
- Define how far behind real-time the processing can be
- `WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND`
- Events arriving after watermark are dropped (or sent to side output)

---

### Q14: How do you integrate Kafka with Flink in a production pipeline?

**Answer:**

**Architecture:**
```
Producers → Kafka Topics → Flink Jobs → Kafka Topics (or sinks)
```

**Production setup:**

1. **Flink Kafka Source:**
```java
KafkaSource<Order> source = KafkaSource.<Order>builder()
    .setBootstrapServers("kafka:9092")
    .setTopics("orders")
    .setGroupId("flink-order-processor")
    .setStartingOffsets(OffsetsInitializer.committedOffsets(OffsetResetStrategy.EARLIEST))
    .setDeserializer(new OrderDeserializationSchema())
    .build();

DataStream<Order> orders = env.fromSource(source, WatermarkStrategy
    .<Order>forBoundedOutOfOrderness(Duration.ofSeconds(5))
    .withTimestampAssigner((order, ts) -> order.getOrderTime().toEpochMilli()),
    "Kafka Orders Source");
```

2. **Flink Kafka Sink:**
```java
KafkaSink<OrderSummary> sink = KafkaSink.<OrderSummary>builder()
    .setBootstrapServers("kafka:9092")
    .setRecordSerializer(KafkaRecordSerializationSchema.builder()
        .setTopic("order-summaries")
        .setValueSerializationSchema(new OrderSummarySerializationSchema())
        .build())
    .setDeliveryGuarantee(DeliveryGuarantee.EXACTLY_ONCE)
    .setTransactionalIdPrefix("flink-order-summary")
    .build();

summaryStream.sinkTo(sink);
```

3. **Checkpointing for exactly-once:**
```java
env.enableCheckpointing(60000); // Every 60 seconds
env.getCheckpointConfig().setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);
env.getCheckpointConfig().setMinPauseBetweenCheckpoints(30000);
env.getCheckpointConfig().setCheckpointStorage("s3://checkpoints/order-processor");
```

4. **Production considerations:**
   - Set parallelism matching Kafka partition count
   - Configure RocksDB state backend for large state
   - Monitor checkpoint duration and size
   - Set up savepoints for job upgrades
   - Handle schema evolution via Schema Registry

---

### Q15: Describe event-driven architecture patterns with Kafka.

**Answer:**

**1. Event Sourcing:**
- Store state changes as a sequence of events (not current state)
- Kafka as the event store (compacted topic for current state)
- Rebuild state by replaying events
- Audit trail for free
```
OrderCreated → ItemAdded → ItemRemoved → OrderSubmitted → PaymentReceived → OrderFulfilled
```

**2. CQRS (Command Query Responsibility Segregation):**
```
Commands → Command Service → Kafka Events → Read Service → Read DB
                                          → Analytics Service → Analytics DB
                                          → Notification Service → Email/Push
```
- Write model and read model are separate
- Events update read models asynchronously
- Optimized query models for each use case

**3. Saga Pattern (distributed transactions):**
```
Order Service → "order.created" →
    Payment Service → "payment.completed" →
        Inventory Service → "inventory.reserved" →
            Shipping Service → "shipment.created"

On failure (compensating transactions):
    "payment.failed" → Order Service → "order.cancelled"
```
- Choreography: services react to events independently
- Orchestration: central orchestrator coordinates the flow

**4. Event-Driven Microservices:**
```
Service A publishes events → Kafka → Service B, C, D consume independently
```
- Loose coupling (producers don't know consumers)
- Easy to add new consumers without modifying producers
- Natural audit trail and replay capability

**5. Change Data Capture (CDC):**
```
Database → Debezium (Kafka Connect) → Kafka → Consumers
```
- Capture database changes as events
- No application code modification needed
- Keeps downstream systems in sync

---

### Q16: How do you monitor and troubleshoot Kafka in production?

**Answer:**

**Key metrics to monitor:**

| Metric | Meaning | Alert Threshold |
|--------|---------|-----------------|
| Consumer Lag | Difference between latest offset and committed offset | > 10K messages |
| Under-Replicated Partitions | Partitions with fewer replicas than configured | > 0 |
| ISR Shrink Rate | In-Sync Replicas shrinking | Any occurrence |
| Request Latency (p99) | Broker response time | > 100ms |
| Disk Usage | Broker disk utilization | > 80% |
| Network I/O | Bytes in/out per broker | Near network capacity |
| Active Controller Count | Should always be 1 | != 1 |

**Troubleshooting common issues:**

1. **High consumer lag:**
   - Increase consumers (up to partition count)
   - Increase `max.poll.records`
   - Optimize processing logic
   - Check for slow downstream calls

2. **Rebalancing storms:**
   - Increase `session.timeout.ms`
   - Use cooperative sticky assignor
   - Use static group membership
   - Check GC pauses

3. **Producer timeouts:**
   - Check broker health
   - Verify network connectivity
   - Check `acks` setting vs replication
   - Monitor broker request queue

**Tools:**
- Confluent Control Center (GUI)
- Kafka CLI: `kafka-consumer-groups.sh --describe`
- Prometheus + Grafana dashboards
- Burrow (LinkedIn's consumer lag monitoring)
