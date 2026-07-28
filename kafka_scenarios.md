# Kafka — Critical Scenario-Based Questions for Principal Engineer

> Not definitions. Real-world scenarios, tradeoffs, design decisions. Each question is something a Principal Engineer is expected to have an answer for.

---

## Topic: Scaling & Throughput

### Q: Your Kafka topic has 3 partitions, 3 consumers, and you're hitting throughput limits. What do you do?

**Bad answer:** "Increase partitions."

**Good answer:** "First, I need to understand where the bottleneck is — producer-side or consumer-side?"

**Producer bottleneck:**
- Batching: are producers sending one message at a time? `linger.ms` and `batch.size` control batching.
- Compression: `snappy` or `lz4` at the producer level reduces network and storage.
- Async vs sync: async producer with a callback is much higher throughput.

**Consumer bottleneck:**
- Partition count is the parallelism ceiling. More partitions = more consumers can process in parallel. But partition count is set at topic creation and changing it after the fact re-partitions keys.
- Key consideration: if ordering matters per key, adding partitions doesn't change that — messages for the same key still go to the same partition. The throughput gain comes from distributing *different* keys across more partitions.
- If a single consumer is falling behind (lag growing), check: processing time per message, network latency to the consumer, consumer group rebalancing frequency.

**Decision:** "If the bottleneck is consumer-side and keys are well distributed, I'd increase partitions and scale consumers. If the bottleneck is producer-side, I'd tune batching and compression before adding infrastructure."

---

### Q: You have a topic with 50 partitions and 5 consumers. A sudden traffic spike causes consumer lag to grow unbounded. How do you respond?

**Immediate (firefighting):**
- Add more consumer instances — but wait, with only 5 consumers and 50 partitions, you already have spare partitions. Adding consumers up to 50 will distribute load.
- If 50 consumers isn't enough, you have a problem with processing *per message* being too slow.
- Suspend non-critical processing on consumers (e.g., stop writing to analytics DB, focus on core flow).
- Increase `max.poll.records` to fetch more per poll, but be careful of `max.poll.interval.ms` timeout.

**Medium-term:**
- Can messages be processed asynchronously within the consumer? Fetch + enqueue to an internal thread pool, commit offsets after processing.
- But watch out for: crash → messages in the internal queue are lost. Need to handle that.

**Long-term:**
- If the spike is sustained, the topology is wrong. A single topic with 50 partitions might need to be split — is this one event type that genuinely needs 50-way parallelism, or are there multiple event types that should be separate topics?
- Could a stream processor (KSQL/KS) sit between the raw topic and consumers to aggregate/filter before consumption?

---

### Q: How many partitions should a topic have? Walk me through your decision framework.

> "There's no magic number. Here's how I decide:"

1. **Throughput target** — what's the peak messages/second you need to consume? A single partition can handle ~10 MB/s (measured, but varies). If you need 100 MB/s, you need at least 10 partitions.
2. **Consumer parallelism** — how many consumers will you run? Partitions = max parallelism. If you plan 20 consumers, you need at least 20 partitions.
3. **Key-based ordering** — if you need order per key (e.g., all events for customer X in order), more partitions = fewer keys per partition = less chance of head-of-line blocking. But too many partitions with few keys means most partitions are idle.
4. **Operational overhead** — more partitions means more files on brokers (for segments), more memory for partition leaders, longer rebalance times when consumers join/leave.
5. **Future growth** — partitions can be increased, but not decreased. Better to start higher than you need. I usually target: `max(throughput_in_MBs, consumer_count * 2)`.

**Rule of thumb:** Start with `number_of_consumers * 2` to allow for future consumer scaling, and don't exceed `(broker_count * broker_cores * 2)` across all topics for total partition count.

---

## Topic: Message Ordering

### Q: A downstream system requires messages for a given customer ID to be processed in order. How do you guarantee this with Kafka?

**Answer:**
- Use the customer ID as the message key. Kafka guarantees order **per partition** — all messages with the same key go to the same partition.
- Set partition count appropriately. If you have 10,000 customers, 50 partitions means each partition serves ~200 customers. Order is preserved per customer *within* that partition.
- **Critical caveat:** If you change the partition count later, the key → partition mapping changes. Customers may land on a different partition, and you lose ordering guarantees for in-flight messages during the repartition.
- The consumer must process messages within a partition sequentially — don't spawn parallel threads per partition.

**What if a single customer produces faster than a consumer can process?**
- That's a head-of-line blocking problem. The partition can't make progress past the slow customer's messages.
- Solution: (a) separate hot customers into their own partition, (b) use a priority queue downstream, or (c) accept ordering relaxation for that customer and parallelize.

---

### Q: Your consumer processes messages in order within a partition. One message fails to process. Do you stop the entire partition?

**The dilemma:** If you commit the offset (skip the bad message), you lose ordering — subsequent messages from that customer are processed before the failed one. If you don't commit (stop processing), the entire partition stalls.

**Answer:**
> "This is a common design decision. There's no universal answer — it depends on the cost of delayed processing vs the cost of out-of-order processing."

**Approach 1: Dead letter queue (preferred for most systems)**
- Catch the exception, log the message to a DLQ topic, commit the offset, continue.
- DLQ consumer processes failed messages with manual review or a different retry strategy.
- Accept: ordering is technically lost for that specific customer's messages across the retry. But in practice, the retry happens fast enough that it doesn't matter.

**Approach 2: Blocking retry with backoff**
- Retry the message N times with exponential backoff inside the consumer.
- Problem: the entire partition is blocked during retries. Only acceptable if retries are fast (sub-second) and failures are rare.
- Usually the wrong choice.

**Approach 3: Pause + alert**
- Pause the partition, alert the on-call, and wait for human intervention.
- Only for systems where out-of-order processing is catastrophic (financial transactions, audit trails).
- Expect: production incidents.

---

## Topic: Exactly-Once Semantics (EOS)

### Q: You need exactly-once processing — consume from Kafka, process, write to a database. How do you achieve it?

**Answer:**
> "First, let me clarify what 'exactly-once' means here — exactly-once *delivery* to the consumer, or exactly-once *processing* (the end-to-end pipeline)?"

**Kafka exactly-once delivery (producer side):**
- `enable.idempotence=true` on the producer — prevents duplicate produces within a producer session.
- `acks=all` — wait for all in-sync replicas to acknowledge.
- Combined: guarantees the producer won't introduce duplicates due to retries.

**End-to-end exactly-once (consume-process-produce):**
- Use Kafka's transactional API or **idempotent writes** to the database.
- The standard pattern: store the Kafka offset in the same database transaction as the processing result.
  ```
  BEGIN TRANSACTION
    process message (update account balance)
    store topic, partition, offset in offsets table
  COMMIT
  ```
- On restart, consumer reads the last committed offset from the offsets table and seeks to that position.
- Downside: couples your processing logic to your database schema.

**Alternative: Idempotent consumer**
- Make the processing side idempotent. Processing the same message twice produces the same result.
- Example: `UPDATE accounts SET balance = 100 WHERE account_id = X AND version = 5`. If replayed, version check prevents double-apply.
- Simpler, works for most real-world systems. Highly recommended.

**My preference:** Idempotent consumer. The transactional API adds complexity (coordinator, timeouts, zombie fencing) that most systems don't need. Start with idempotent, only add transactions if you prove you need them.

---

### Q: What's the difference between at-least-once, at-most-once, and exactly-once in Kafka? When would you use each?

| Guarantee | Configuration | Risk | Use Case |
|---|---|---|---|
| **At-most-once** | `enable.auto.commit=true` with low interval, no retries | Messages may be lost (consumer crashes before processing) | Telemetry, logging, metrics — missing one data point is acceptable |
| **At-least-once** | `enable.auto.commit=false`, commit after processing | Messages may be duplicated (consumer crashes after processing but before commit) | **Default for most systems.** Payment events, notifications. Dedup downstream or tolerate duplicates. |
| **Exactly-once** | Idempotent producer + transactional API or idempotent consumer | Higher latency, operational complexity | Financial transactions, audit trails, inventory |

**Principal-level take:** "Most systems should run at-least-once with an idempotent consumer. Exactly-once is usually a solution in search of a problem — the complexity cost is real. I've only used it when financial reconciliation audits required it."

---

## Topic: Consumer & Offset Management

### Q: A consumer group rebalance happens frequently, disrupting all consumers. What could be wrong?

**Common causes:**
1. **`session.timeout.ms` too low** — consumers are being kicked out for not sending heartbeats. If processing takes longer than the session timeout, the broker thinks the consumer is dead and triggers rebalance.
   - Fix: Either increase `session.timeout.ms` or run heartbeats in a separate thread (`heartbeat.interval.ms`).

2. **`max.poll.interval.ms` exceeded** — consumer takes too long processing a batch of `max.poll.records`. The broker considers the consumer stuck.
   - Fix: Reduce `max.poll.records`, increase `max.poll.interval.ms`, or move processing to a background thread.

3. **Consumer instance flapping** — the consumer is crashing and restarting (OOM, network issues, deployment rolling update).
   - Fix: Stabilize the deployment. Use cooperative rebalancing (Kafka 3.1+) to reduce impact.

4. **Static group membership** — If consumer instances have stable IDs, use `group.instance.id` to prevent unnecessary rebalances when a consumer restarts.

**Debuggable:** Check consumer group status with `kafka-consumer-groups --describe --group <group>` — look for the rebalance rate and consumer state.

---

### Q: A consumer has been running for weeks. Today it started processing the same messages it processed yesterday. What happened?

**Answer:** The consumer committed its offset backward. Possible causes:

1. **`auto.offset.reset` behavior** — if the consumer group is reset or the committed offset is deleted (offsets retention `offsets.retention.minutes`), the consumer picks the earliest or latest offset based on the config.
2. **Offset retention exhausted** — if a consumer group is inactive longer than `offsets.retention.minutes` (default 7 days in Kafka 3+), its offsets are deleted. On restart, it falls back to `auto.offset.reset`.
3. **Consumer manually seeking** — someone (or code) called `consumer.seek()` to an earlier offset, maybe for reprocessing.
4. **Consumer group ID changed** — a new deployment changed the `group.id` → new group starts from the beginning.

**Fix:** Check the consumer group offset details. If offsets are deleted due to retention, either increase retention or maintain the offset externally.

---

## Topic: Schema & Evolution

### Q: Your production topic has messages with a known schema. You need to add a new field. How do you safely evolve the schema?

**Answer:**
> "Use Schema Registry with Avro/Protobuf/JSON Schema. Never evolve without schema management."

**Forward-compatible evolution (what Schema Registry enforces):**
- Add optional fields with defaults.
- Never remove required fields.
- Never change field types.
- Old consumers can read new messages (they ignore unknown fields).
- New consumers can read old messages (missing optional fields get defaults).

**The actual rollout:**
1. Add the field as optional with a default in the schema.
2. Register the new schema (compatibility check passes — it's backward and forward compatible).
3. Producers start writing messages with the new field.
4. Old consumers continue working — they see new messages, ignore the new field.
5. Old messages with the old schema are still readable by new consumers — the new field gets the default value.
6. After all consumers are updated, you can make the field required in the next schema version.

**Without Schema Registry (JSON on Kafka):**
- Add the field as optional. Producers populate it. Consumers that don't know about it ignore it.
- But: you lose the enforcement. Someone could change the field type accidentally and break downstream consumers silently.
- Schema Registry catches this at registration time.

---

## Topic: Error Handling & Dead Letter Queues

### Q: Design a retry mechanism for Kafka consumers. A message fails because a downstream API is temporarily down. How do you handle retries without blocking the partition?

**Answer:**
> "The pattern is: separate the retry from the main consumption path."

**Pattern: Retry topic + DLQ**
1. **Main consumer** subscribes to the source topic. Tries to process. If it fails:
   - Check the `retry_count` header.
   - If `retry_count < max_retries`: publish to a **retry topic** with `retry_count + 1` and a `retry_at` timestamp.
   - If `retry_count >= max_retries`: publish to a **DLQ topic** with the error details.
2. **Retry consumer** subscribes to the retry topic. For each message:
   - If `retry_at > now`: pause the partition, wait, resume. (Or: re-publish to a future-dated retry topic with `retention.ms` matching the delay.)
   - If `retry_at <= now`: try processing. Success → commit. Failure → iterate.
3. **DLQ consumer** subscribes to the DLQ topic. Logs, alerts on-call, or stores for manual replay.

**Alternative (simpler):** Use Kafka's own retry topic pattern — create a retry topic with `retention.ms` equal to the retry delay. Publish the failed message there. The retry consumer reads from it after the retention period expires. No timestamps needed.

**The key design decision:** "Should retries live in the same consumer group or a different one?" Same group = retry messages don't impact main consumption parallelism. Different group = retries can be processed by separate infrastructure. I prefer the same group with a separate subscription for most cases.

---

### Q: Messages start failing consistently in a Kafka consumer. Half the messages go to DLQ. How do you diagnose?

**Answer:**
> "I'd look at three things in parallel."

1. **Check the DLQ message content** — are failing messages structurally different? A schema change on the producer side that wasn't evolved through Schema Registry would cause consistent failures.
2. **Check consumer logs** — what error are they throwing? Deserialization error → schema mismatch. Timeout → downstream dependency issue. Business logic error → code change broke assumptions.
3. **Check the timing** — did a new consumer version deploy recently? Did a downstream API change? Correlate the failure start time with changes.

**Most common cause:** A producer added a required field or changed a field type without schema coordination. Schema Registry prevents this — which is why I mandate it.

---

## Topic: Performance Tuning

### Q: Kafka is slow. How do you identify and fix the bottleneck?

**Systematic approach:**

| Symptom | Likely Cause | Fix |
|---|---|---|
| Producer send() blocks | `max.block.ms` hit — buffer full | Increase `buffer.memory`, reduce `max.request.size`, check broker load |
| High producer latency | `acks=all` waiting for replicas | Check if min.insync.replicas is met. Are brokers overloaded? |
| Consumer lag growing | Processing too slow per message | Profile processing code. Partition count may be too low |
| High network utilization | Large messages or no compression | Enable `snappy` compression. Consider splitting large payloads |
| High disk I/O on brokers | Retention or segment settings | Tune `log.retention.bytes` and `log.segment.bytes` |
| Rebalances disrupting consumers | `session.timeout.ms` too low | Increase timeout or use cooperative rebalancing |

**Principal-level: "Before tuning any knob, I check the consumer lag graph and the broker's request metrics. The bottleneck is almost never what you guess — measure first, tune second."**

---

### Q: You have messages larger than 1 MB. Kafka defaults max message size to 1 MB. What do you do?

**Options (in order of preference):**

1. **Don't put large messages in Kafka.** Store the payload in S3/Blob storage, put the reference in Kafka. Kafka is optimized for many small messages, not few large ones. Large messages increase latency, memory pressure, and storage costs.
2. **Compress the payload** — 1 MB of JSON may compress to 100 KB with snappy.
3. **Increase `max.message.bytes`** on the broker, and `max.request.size` on the producer + `fetch.max.bytes` on the consumer. But this impacts every producer and consumer on the cluster — the broker holds larger messages in memory during replication.

**My take:** "Option 1, always. If a message is > 1 MB, the payload belongs in object storage. The reference in Kafka keeps everything fast. I've seen teams increase message size and regret it when memory pressure on brokers caused cascading failures."

---

## Topic: Operations & Reliability

### Q: A Kafka broker goes down. What happens to producers and consumers?

**Answer:**
> "Depends on the topic configuration."

- **If the broker was the partition leader** for some partitions: another broker with an in-sync replica becomes the new leader (controlled by `unclean.leader.election.enable`).
  - `unclean.leader.election.enable=false` (default) — only ISR replicas can become leader. Partition may be unavailable if no ISR exists.
  - `unclean.leader.election.enable=true` — any replica can become leader. Partition stays available but may lose data.
- **Producers with `acks=all`** wait for the new leader. If `min.insync.replicas` can't be met after the broker loss, producers get `NOT_ENOUGH_REPLICAS` errors.
- **Consumers** get a `NOT_LEADER_FOR_PARTITION` error during the leader election, retry, and find the new leader via metadata refresh.
- **No data loss** if the dead broker had an in-sync replica on another broker.
- **Recovery:** when the broker comes back, it catches up as a follower, then becomes an ISR again.

---

### Q: How do you configure replication factor and min.insync.replicas for a production cluster?

> "This is a risk calculation. Let me walk through the options."

| Replication Factor | min.insync.replicas | Tolerated Failures | Write Availability |
|---|---|---|---|
| 3 | 2 | 1 broker | Writes succeed if 2/3 replicas are up |
| 3 | 3 | 0 brokers (1 replica down = writes fail) | Writes fail if any broker is down |
| 3 | 1 | 1 broker (but may lose data) | Writes always succeed |

**Standard production setup:** `replication.factor=3`, `min.insync.replicas=2`. This is the sweet spot.
- Tolerates 1 broker failure without data loss.
- Writes succeed as long as 2 of 3 replicas are available (the surviving ISR).
- Producer must also set `acks=all` to get this guarantee.

**When to increase:** If you have more critical data (financial events), `replication.factor=5`, `min.insync.replicas=3`. Tolerates 2 broker failures.

**When to decrease:** Never on a production cluster for a replicated topic. Use 3.

---

### Q: Kafka consumer lag is growing. A new consumer instance joins the group. What happens during rebalancing, and how do you minimize disruption?

**Answer:**
> "This is where the type of rebalance matters."

**Eager rebalancing (old behavior, default before Kafka 3.1):**
- All consumers in the group stop reading.
- The group coordinator revokes all partitions.
- Consumers rejoin, partitions are reassigned.
- During the rebalance: **zero consumption** from all consumers.
- If lag is already growing, the rebalance window creates a spike.

**Cooperative rebalancing (Kafka 3.1+, incremental rebalance):**
- Only a subset of consumers stop. Specifically: the consumers that need to surrender partitions to the new joiner.
- The new consumer takes over some partitions; most consumers keep processing.
- **Much lower disruption** — lag doesn't spike.

**Minimizing rebalance impact:**
1. Use cooperative rebalancing (`partition.assignment.strategy=CooperativeStickyAssignor`).
2. Set `group.initial.rebalance.delay.ms` to give new consumers time to register before the rebalance starts.
3. Use static group membership (`group.instance.id`) — the broker identifies the consumer by ID, not just by session. A consumer restart doesn't trigger a full rebalance.
4. Increase `session.timeout.ms` — less false-positive rebalances from heartbeat timing issues.

---

## Topic: Migration & Dual-Write

### Q: You're migrating from RabbitMQ to Kafka. How do you do it without downtime or missed messages?

**Answer:**
> "Dual-write + parallel consumption + cutover."

**Phase 1: Dual-write**
- Producers write to **both** RabbitMQ (existing) and Kafka (new).
- Consumers continue reading from RabbitMQ. Kafka consumers start in parallel, but their output is not authoritative yet.
- Run reconciliation: compare RabbitMQ consumer output vs Kafka consumer output for the same messages. Fix discrepancies.

**Phase 2: Parallel consumption**
- Both RabbitMQ and Kafka consumers are live. The Kafka consumer becomes the new source of truth for downstream systems.
- RabbitMQ consumer runs as a fallback.
- Monitor: Kafka consumer lag, message loss, data inconsistency.

**Phase 3: Cutover**
- Switch producers to Kafka-only (stop writing to RabbitMQ).
- Stop RabbitMQ consumers after all pending messages are drained.
- Validate: check that downstream systems see no data gap.

**Phase 4: Decommission**
- Remove RabbitMQ infrastructure. (Don't rush this — keep it as a fallback for 1-2 weeks.)

**Critical detail:** The dual-write must be **transactional** or **idempotent**. If the Kafka write succeeds and the RabbitMQ write fails, the application should either fail the operation or handle the inconsistency. In practice, I make the Kafka write the primary and RabbitMQ a best-effort fallback.

---

### Q: You need to migrate Kafka topics from an old cluster to a new cluster. How?

**Options:**

1. **MirrorMaker 2 (recommended for most cases)** — built-in Kafka tool. Replicates topics from source to destination cluster in near real-time. Supports active-active, active-standby. You can fail over by pointing consumers to the new cluster.

2. **Cluster Linking (Confluent)** — Confluent-specific. Simpler than MirrorMaker, handles offset translation automatically.

3. **Custom replication** — read from source, write to destination. Full control but you own the reliability.

**Principal-level take:** "MirrorMaker 2 is the safest option for a Kafka-to-Kafka migration without Confluent. The key is: run MM2 long enough to validate data consistency before cutting over. And during the cutover, drain the source consumer's lag completely before switching — you don't want consumers jumping between clusters with offset gaps."

---

## Topic: Advanced Scenarios

### Q: You need Kafka to handle a 10x traffic spike during a flash sale. Your cluster is provisioned for normal load. What's your plan?

**Answer:**
> "There are three levers — producer throttling, consumer scaling, and broker capacity."

**Producer side (what you can control before the event):**
- Increase producer buffer size (`buffer.memory`) to absorb bursts.
- Enable compression if not already.
- Set `max.in.flight.requests.per.connection=1` with `enable.idempotence=true` to avoid duplicates during retries on overload.

**Consumer side:**
- Pre-scale consumers to their maximum partition count (can't exceed partitions).
- If consumers are already at max partitions: optimize processing (batch DB writes, use async processing with an internal queue).
- Accept that consumer lag will grow during the spike. Don't panic. Plan to catch up after.

**Broker side:**
- This is usually where the bottleneck hits. Options:
  a) **Auto-scaling** — if your K8s-based Kafka (Strimzi, Confluent Operator) supports broker auto-scaling, let it add brokers during the spike.
  b) **Over-provision** — run the cluster at 30-40% capacity during normal load, so it handles spikes without scaling.
  c) **Throttle producers** — if the cluster can't handle the load, the brokers will start rejecting produce requests. The producer's retry mechanism handles this, but the backpressure propagates to your services.

**The honest answer:** "Kafka doesn't auto-scale well for traffic spikes because partition leaders can't be rebalanced instantly. The best approach is over-provisioning for known events (flash sales) and accepting that the cluster will throttle during unexpected spikes. I'd run a load test at target traffic to confirm the cluster doesn't fall over."

---

### Q: You're designing an event-sourced system with Kafka as the event store. What are the tradeoffs vs a dedicated event store?

**Answer:**
> "Kafka is a great event stream, but it's not a database. Here are the tradeoffs:"

| Criteria | Kafka as Event Store | Dedicated Event Store (EventStoreDB) |
|---|---|---|
| **Event replay** | Excellent — retention + offset management | Native — stream-based |
| **Point-in-time state** | Not native — need KTable or external state store | Built-in |
| **Query events by business key** | Not efficient — Kafka is optimized for sequential read | Indexed by stream ID |
| **Deleting events** | Not designed for it — compaction *removes* old keys, not delete | Supports event deletion |
| **Exactly-once** | Requires idempotent consumers + transactions | Native |
| **Operational simplicity** | Most teams already run Kafka | Additional infrastructure |

**My take:** "Use Kafka as the event stream for event sourcing when you already run Kafka and the use case is append-only event history with replay. Don't use Kafka as the source of truth for current state — use KTable + a database for that. If you need to query events by business key frequently, Kafka is the wrong choice — you need a dedicated event store."

---

### Q: Kafka vs Pulsar — when would you choose one over the other?

**Answer:**
> "Kafka is the industry standard with the largest ecosystem. Pulsar is architecturally superior in some ways but has less adoption."

**Choose Kafka when:**
- You need the ecosystem — Schema Registry, Kafka Connect, KSQL, MirrorMaker.
- Your team already knows Kafka operations.
- Your throughput requirements fit within Kafka's model (most use cases do).
- You want managed services (Confluent, MSK, Aiven).

**Choose Pulsar when:**
- You need geo-replication with low latency across regions (Pulsar's segment-based architecture handles this better).
- You have many topics that are sparsely used (Pulsar separates storage from compute — a topic doesn't need a broker).
- You need multi-tenancy with strict resource isolation as a first-class feature.
- You anticipate extreme scale (Pulsar has less overhead per partition).

**My take:** "Kafka is the safe default. Choose Pulsar only if you've proven Kafka can't meet your requirements — and measure first before switching. An infrastructure migration is expensive."

---

## Quick Reference — Kafka Cheat Sheet

### Configs to Know

| Config | Default | What It Does |
|---|---|---|
| `acks` | 1 | `0` = fire-and-forget, `1` = leader writes, `all` = all ISRs write |
| `enable.idempotence` | false | `true` prevents duplicate produces from retries |
| `min.insync.replicas` | 1 | Min ISRs for `acks=all` to succeed |
| `session.timeout.ms` | 45000 ms | How long before broker declares consumer dead |
| `max.poll.interval.ms` | 300000 ms | Max time between polls before consumer considered stuck |
| `max.poll.records` | 500 | Max records per poll. Lower = more frequent commits |
| `linger.ms` | 0 | Max time to wait for batching. Higher = better throughput |
| `batch.size` | 16384 bytes | Max batch size before sending. Larger = better compression |
| `compression.type` | none | `snappy` for speed, `gzip` for ratio, `lz4` for balanced |
| `auto.offset.reset` | latest | `latest` (start from now) or `earliest` (start from beginning) |
| `replication.factor` | 1 | Set to 3 in production |
| `unclean.leader.election.enable` | false | Set to false unless you accept data loss for availability |

### Kafka Tools

| Tool | What it does |
|---|---|
| `kafka-consumer-groups` | Check lag, describe group state, reset offsets |
| `kafka-topics` | Create, alter, describe topics. Partition count, replication |
| `kafka-configs` | Override configs per topic or broker |
| `kafka-dump-log` | Read log segments directly for debugging |
| `kafka-reassign-partitions` | Move partitions between brokers (rebalancing) |
| `MirrorMaker 2` | Cross-cluster replication |

### Monitoring Metrics

| Metric | What It Tells You |
|---|---|
| **Consumer lag** | How far behind consumers are from producers |
| **Request rate (broker)** | Overall cluster throughput |
| **Produce request time (p99)** | Broker-side latency for writes |
| **Fetch request time (p99)** | Broker-side latency for reads |
| **Under-replicated partitions** | Replicas not catching up — replication issue |
| **Active controller count** | Should be 1. >1 means a split-brain scenario |
| **Bytes in/out per broker** | Network utilization vs capacity |
| **Partition count per broker** | More partitions = more leader election overhead |
| **Segment count** | Too many small segments = poor I/O |

### Decision Framework for Kafka Questions

When asked any Kafka scenario:

1. **Clarify the constraints** — throughput, ordering, consistency, latency, budget, operational maturity
2. **Identify the bottleneck** — producer, consumer, broker, or network
3. **Pick the simplest config change first** — batching, compression, timeout tuning, partition count
4. **Escalate to architecture change** — split topic, add DLQ, change streaming topology, add Schema Registry
5. **Name the tradeoff** — every choice gives up something. Be explicit.
6. **If you don't know, say so** — "I haven't hit that scenario. Here's how I'd approach it..."
