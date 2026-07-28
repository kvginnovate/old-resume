# Data & Database Integration — Questions & Answers

## SQL Databases

### Q1: How do you design a database schema for a microservices architecture?

**Answer:**

**Key principle: Database per Service**
Each microservice owns its data. No shared databases.

```
Subscriber Service → subscriber_db (PostgreSQL)
Payment Service   → payment_db (PostgreSQL)
Analytics Service → analytics_db (MongoDB)
Cache Layer       → Redis / GemFire
```

**Why database per service:**
- Independent schema evolution (no cross-team coordination)
- Independent scaling (read replicas where needed)
- Technology freedom (SQL for transactional, NoSQL for flexible)
- Failure isolation (one DB down doesn't break everything)

**Schema design principles:**

1. **Normalize for writes, denormalize for reads:**
   ```sql
   -- Normalized (write path)
   CREATE TABLE subscriber (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       name VARCHAR(100) NOT NULL,
       email VARCHAR(255) UNIQUE NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   
   CREATE TABLE subscription (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       subscriber_id UUID REFERENCES subscriber(id),
       plan_type VARCHAR(50) NOT NULL,
       status VARCHAR(20) DEFAULT 'ACTIVE',
       start_date DATE NOT NULL,
       end_date DATE
   );
   
   -- Denormalized view (read path)
   CREATE MATERIALIZED VIEW subscriber_summary AS
   SELECT s.id, s.name, s.email,
          COUNT(sub.id) as total_subscriptions,
          MAX(sub.start_date) as latest_subscription_date
   FROM subscriber s
   LEFT JOIN subscription sub ON s.id = sub.subscriber_id
   GROUP BY s.id, s.name, s.email;
   ```

2. **Indexing strategy:**
   ```sql
   -- Primary lookup
   CREATE INDEX idx_subscriber_email ON subscriber(email);
   
   -- Foreign key (always index)
   CREATE INDEX idx_subscription_subscriber ON subscription(subscriber_id);
   
   -- Composite for query pattern
   CREATE INDEX idx_subscription_status_date 
       ON subscription(status, start_date DESC);
   
   -- Partial index (only active records)
   CREATE INDEX idx_active_subscriptions 
       ON subscription(subscriber_id) WHERE status = 'ACTIVE';
   ```

3. **Soft deletes for audit:**
   ```sql
   ALTER TABLE subscriber ADD COLUMN deleted_at TIMESTAMP NULL;
   CREATE INDEX idx_subscriber_active ON subscriber(id) WHERE deleted_at IS NULL;
   ```


---

### Q2: How do you write and optimize complex SQL queries?

**Answer:**

**Common query patterns and optimizations:**

**1. Pagination (offset vs cursor):**
```sql
-- Offset-based (simple but slow for large offsets)
SELECT * FROM subscriber 
ORDER BY created_at DESC 
LIMIT 20 OFFSET 1000;  -- Scans 1020 rows!

-- Cursor-based (efficient for large datasets)
SELECT * FROM subscriber 
WHERE created_at < '2024-01-15T10:00:00Z'
ORDER BY created_at DESC 
LIMIT 20;
```

**2. Avoiding N+1 queries:**
```sql
-- BAD: N+1 (1 query for subscribers + N queries for subscriptions)
SELECT * FROM subscriber;  -- Then loop and query subscriptions

-- GOOD: Join in one query
SELECT s.*, sub.plan_type, sub.status
FROM subscriber s
LEFT JOIN subscription sub ON s.id = sub.subscriber_id
WHERE s.status = 'ACTIVE';

-- GOOD: Batch fetch (for JPA/Hibernate)
@EntityGraph(attributePaths = {"subscriptions"})
List<Subscriber> findAllByStatus(String status);
```

**3. Window functions for analytics:**
```sql
-- Running total of subscriptions per month
SELECT 
    DATE_TRUNC('month', start_date) as month,
    COUNT(*) as new_subscriptions,
    SUM(COUNT(*)) OVER (ORDER BY DATE_TRUNC('month', start_date)) as cumulative
FROM subscription
GROUP BY DATE_TRUNC('month', start_date)
ORDER BY month;

-- Rank subscribers by total spend
SELECT 
    s.name,
    SUM(p.amount) as total_spend,
    RANK() OVER (ORDER BY SUM(p.amount) DESC) as spend_rank
FROM subscriber s
JOIN payment p ON s.id = p.subscriber_id
GROUP BY s.id, s.name;
```

**4. Common Table Expressions (CTEs) for readability:**
```sql
WITH active_subscribers AS (
    SELECT id, name, email
    FROM subscriber
    WHERE deleted_at IS NULL
),
recent_payments AS (
    SELECT subscriber_id, SUM(amount) as total_amount
    FROM payment
    WHERE payment_date > CURRENT_DATE - INTERVAL '30 days'
    GROUP BY subscriber_id
)
SELECT a.name, a.email, COALESCE(r.total_amount, 0) as last_30_days_spend
FROM active_subscribers a
LEFT JOIN recent_payments r ON a.id = r.subscriber_id
ORDER BY last_30_days_spend DESC;
```

**5. Query optimization checklist:**
- Run `EXPLAIN ANALYZE` to see actual execution plan
- Check for sequential scans on large tables (missing index?)
- Verify index usage (`Index Scan` vs `Seq Scan`)
- Check for high `rows removed by filter` (wrong index or missing partial index)
- Monitor `shared_buffers` hit rate (should be >99%)
- Use `pg_stat_statements` for top slow queries

---

### Q3: How do you handle database connection pooling in Spring Boot?

**Answer:**

**HikariCP (default in Spring Boot):**
```yaml
spring:
  datasource:
    url: jdbc:postgresql://db:5432/subscriber_db
    username: ${DB_USER}
    password: ${DB_PASSWORD}
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      idle-timeout: 300000        # 5 min
      connection-timeout: 30000   # 30 sec (wait for connection)
      max-lifetime: 1800000       # 30 min (recycle connections)
      leak-detection-threshold: 60000  # Log if connection held > 60s
      pool-name: subscriber-pool
```

**Sizing formula:**
```
pool_size = (core_count * 2) + effective_spindle_count
For cloud (SSD): pool_size ≈ core_count * 2 + 1
Example: 4-core container → pool_size = 9-10
```

**Multiple datasources (read/write split):**
```java
@Configuration
public class DataSourceConfig {

    @Bean
    @Primary
    @ConfigurationProperties("spring.datasource.write")
    public DataSource writeDataSource() {
        return DataSourceBuilder.create().build();
    }

    @Bean
    @ConfigurationProperties("spring.datasource.read")
    public DataSource readDataSource() {
        return DataSourceBuilder.create().build();
    }
}

// Route reads to replica
@Transactional(readOnly = true)  // Routes to read datasource
public Subscriber findById(String id) { ... }

@Transactional  // Routes to write datasource
public Subscriber save(Subscriber subscriber) { ... }
```

**Monitoring connection pool:**
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,metrics
  metrics:
    tags:
      application: subscriber-api
```

Key metrics:
- `hikaricp.connections.active` — currently in use
- `hikaricp.connections.pending` — threads waiting for connection
- `hikaricp.connections.timeout` — connection acquisition timeouts
- Alert: pending > 0 sustained for 30s = pool exhaustion risk

---

### Q4: What is the difference between SQL and NoSQL databases? When do you choose each?

**Answer:**

| Aspect | SQL (PostgreSQL, Oracle) | NoSQL (MongoDB, DynamoDB) |
|--------|-------------------------|---------------------------|
| Schema | Fixed, enforced | Flexible, schema-on-read |
| Transactions | ACID (strong consistency) | BASE (eventual consistency) |
| Relationships | Joins, foreign keys | Embedded documents, denormalized |
| Scaling | Vertical (read replicas for reads) | Horizontal (sharding built-in) |
| Query | Powerful SQL (aggregations, joins) | Limited (key-value, document queries) |
| Use case | Complex queries, transactions | High write volume, flexible schema |

**When to choose SQL:**
- Financial transactions (ACID required)
- Complex reporting and analytics (joins, aggregations)
- Well-defined relationships (subscriber → subscriptions → payments)
- Data integrity is critical
- Moderate scale (millions of rows, not billions)

**When to choose NoSQL:**
- High write throughput (event logs, telemetry)
- Flexible/evolving schema (user profiles with varying attributes)
- Key-based access patterns (cache, session store)
- Horizontal scaling requirement (billions of records)
- Document-oriented data (JSON payloads stored as-is)

**Polyglot persistence in microservices:**
```
Subscriber Service → PostgreSQL (relational, transactions)
Session Service    → Redis (fast key-value, TTL)
Event Store        → Kafka (append-only log)
Search Service     → Elasticsearch (full-text search)
Analytics          → MongoDB (flexible aggregation pipeline)
Configuration      → Azure App Configuration
```

---

### Q5: How do you handle data consistency across microservices (without distributed transactions)?

**Answer:**

**The problem:** Each service has its own DB. No distributed `BEGIN/COMMIT` across services.

**Patterns:**

**1. Saga Pattern (choreography):**
```
Order Service:    Creates order → publishes "order.created"
Payment Service:  Listens → charges card → publishes "payment.completed"
Inventory Service: Listens → reserves stock → publishes "stock.reserved"
Shipping Service: Listens → creates shipment → publishes "shipment.created"

On failure (compensating transaction):
Payment Service: "payment.failed" → Order Service cancels order
```

**2. Saga Pattern (orchestration):**
```java
public class OrderSagaOrchestrator {
    
    public void execute(Order order) {
        try {
            PaymentResult payment = paymentService.charge(order);
            InventoryResult inventory = inventoryService.reserve(order);
            ShippingResult shipping = shippingService.create(order);
            orderService.complete(order);
        } catch (PaymentException e) {
            orderService.cancel(order);
        } catch (InventoryException e) {
            paymentService.refund(order);
            orderService.cancel(order);
        }
    }
}
```

**3. Outbox Pattern (reliable event publishing):**
```sql
-- Within the same transaction:
BEGIN;
  INSERT INTO subscriber (id, name, email) VALUES (...);
  INSERT INTO outbox (id, aggregate_type, event_type, payload) 
      VALUES (uuid(), 'Subscriber', 'Created', '{"id":"...","name":"..."}');
COMMIT;

-- Separate process polls outbox and publishes to Kafka
-- Then marks outbox entry as published
```

**4. Event-carried state transfer:**
- Services listen to events and maintain local copies of needed data
- No synchronous calls for reads
- Eventually consistent but highly available
```
Subscriber Service publishes "subscriber.updated" →
Payment Service stores subscriber name locally (for receipts)
```

**5. Idempotent consumers:**
```java
@KafkaListener(topics = "payment.completed")
public void handlePayment(PaymentEvent event) {
    // Idempotency check
    if (processedEvents.contains(event.getId())) {
        return; // Already processed
    }
    orderService.markPaid(event.getOrderId());
    processedEvents.add(event.getId());
}
```

---

### Q6: How do you implement caching strategies for database performance?

**Answer:**

**Caching layers:**
```
Client → CDN (static) → API Gateway (response cache)
→ Application (L1: Caffeine) → Distributed (L2: Redis/GemFire)
→ Database (connection pool, query cache)
```

**1. Spring Cache abstraction:**
```java
@Service
public class SubscriberService {

    @Cacheable(value = "subscribers", key = "#id", unless = "#result == null")
    public Subscriber findById(String id) {
        return subscriberRepository.findById(id).orElse(null);
    }

    @CachePut(value = "subscribers", key = "#subscriber.id")
    public Subscriber update(Subscriber subscriber) {
        return subscriberRepository.save(subscriber);
    }

    @CacheEvict(value = "subscribers", key = "#id")
    public void delete(String id) {
        subscriberRepository.deleteById(id);
    }

    @CacheEvict(value = "subscribers", allEntries = true)
    @Scheduled(fixedRate = 3600000)  // Invalidate all every hour
    public void evictAllCache() {}
}
```

**2. Multi-level caching:**
```java
@Configuration
public class CacheConfig {

    @Bean
    public CacheManager cacheManager() {
        CaffeineCacheManager caffeine = new CaffeineCacheManager();
        caffeine.setCaffeine(Caffeine.newBuilder()
            .maximumSize(1000)
            .expireAfterWrite(Duration.ofMinutes(5)));
        
        RedisCacheManager redis = RedisCacheManager.builder(redisConnectionFactory)
            .cacheDefaults(RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofMinutes(30)))
            .build();
        
        return new CompositeCacheManager(caffeine, redis);
    }
}
```

**3. Cache patterns:**

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Cache-Aside | App checks cache, on miss reads DB, writes to cache | Most common, general purpose |
| Write-Through | App writes to cache, cache writes to DB | Strong consistency needed |
| Write-Behind | App writes to cache, async batch write to DB | High write throughput |
| Read-Through | Cache loads from DB on miss transparently | Simplify application code |

**4. Cache invalidation strategies:**
- **TTL (Time-to-Live):** Simple, eventual consistency
- **Event-based:** Kafka event triggers cache eviction
- **Version-based:** ETag/version field, invalidate on mismatch
- **Pub/Sub:** Redis pub/sub for multi-instance cache invalidation

**Cache problems to solve:**
- **Thundering herd:** Use cache locks or stale-while-revalidate
- **Cache penetration:** Cache null results with short TTL
- **Hot key:** Replicate hot keys across multiple cache nodes
- **Consistency:** Event-driven invalidation for strong consistency needs

---

### Q7: How do you guide teams on data access patterns and performance?

**Answer:**

**Data access anti-patterns I watch for:**

1. **N+1 queries (most common):**
   ```java
   // BAD: fetch subscribers then loop for each subscription
   List<Subscriber> subs = repo.findAll();
   subs.forEach(s -> s.setSubscriptions(subRepo.findBySubscriberId(s.getId())));
   
   // GOOD: fetch with join or entity graph
   @Query("SELECT s FROM Subscriber s LEFT JOIN FETCH s.subscriptions")
   List<Subscriber> findAllWithSubscriptions();
   ```

2. **Missing pagination:**
   ```java
   // BAD: loads entire table
   List<Subscriber> findAll();
   
   // GOOD: paginated
   Page<Subscriber> findAll(Pageable pageable);
   ```

3. **Unbounded queries:**
   ```java
   // BAD: no limit
   @Query("SELECT s FROM Subscriber s WHERE s.status = :status")
   List<Subscriber> findByStatus(String status);  // Could be millions!
   
   // GOOD: always limit
   @Query("SELECT s FROM Subscriber s WHERE s.status = :status")
   List<Subscriber> findByStatus(String status, Pageable pageable);
   ```

4. **Wrong isolation level:**
   ```java
   // For read-only reporting queries
   @Transactional(readOnly = true, isolation = Isolation.READ_COMMITTED)
   public List<ReportRow> generateReport() { ... }
   ```

5. **Missing indexes (detected via slow query log):**
   ```sql
   -- PostgreSQL: find missing indexes
   SELECT relname, seq_scan, idx_scan
   FROM pg_stat_user_tables
   WHERE seq_scan > idx_scan AND seq_scan > 1000
   ORDER BY seq_scan DESC;
   ```

**Guidelines I provide to teams:**
- Every query must have an execution plan reviewed before merge
- Maximum result set size enforced (pagination mandatory)
- Connection pool metrics monitored per service
- Slow query alerts (> 100ms for OLTP, > 5s for reports)
- Read replicas for reporting/analytics queries
- Database migrations reviewed by DBA/architect

---

### Q8: How does Spring Data JPA/Hibernate work and what are the pitfalls?

**Answer:**

**How JPA works:**
```
Entity (Java object) ↔ Persistence Context (1st level cache) ↔ Database
```

**Key concepts:**
- **Entity Manager:** Manages entity lifecycle (transient → managed → detached → removed)
- **Persistence Context:** First-level cache within a transaction
- **Dirty Checking:** Auto-detects changes to managed entities and flushes to DB
- **Lazy Loading:** Related entities loaded on first access

**Common pitfalls:**

**1. LazyInitializationException:**
```java
// BAD: accessing lazy collection outside transaction
Subscriber sub = subscriberRepo.findById(id); // Transaction ends
sub.getSubscriptions().size(); // LazyInitializationException!

// FIX: Use @EntityGraph or FETCH JOIN
@EntityGraph(attributePaths = {"subscriptions"})
Optional<Subscriber> findById(UUID id);
```

**2. Open Session in View (OSIV):**
```yaml
# Disable in production (causes performance issues)
spring:
  jpa:
    open-in-view: false
```
OSIV keeps persistence context open during entire request — hides N+1 issues and holds DB connections too long.

**3. Batch inserts (not enabled by default):**
```yaml
spring:
  jpa:
    properties:
      hibernate:
        jdbc:
          batch_size: 50
        order_inserts: true
        order_updates: true
```

**4. Projections (don't fetch entire entity for simple queries):**
```java
// BAD: fetches all columns for just id + name
List<Subscriber> findByStatus(String status);

// GOOD: interface projection
public interface SubscriberSummary {
    String getId();
    String getName();
}
List<SubscriberSummary> findByStatus(String status);
```

**5. Native queries for complex/performance-critical paths:**
```java
@Query(value = """
    SELECT s.id, s.name, COUNT(sub.id) as subscription_count
    FROM subscriber s
    LEFT JOIN subscription sub ON s.id = sub.subscriber_id
    WHERE s.created_at > :since
    GROUP BY s.id, s.name
    HAVING COUNT(sub.id) > :minCount
    """, nativeQuery = true)
List<Object[]> findActiveSubscribersWithMinSubscriptions(
    @Param("since") LocalDateTime since, 
    @Param("minCount") int minCount
);
```

---

### Q9: How do you design data access for high availability and disaster recovery?

**Answer:**

**PostgreSQL HA architecture:**
```
                    Application (Spring Boot)
                   /              \
    Primary (Read-Write)    Read Replica(s) (Read-Only)
         |                       |
    Synchronous Replication    Async Replication (cross-region)
         |
    Standby (failover target)
```

**Azure Database for PostgreSQL (Flexible Server):**
- Zone-redundant HA (automatic failover within region)
- Read replicas (up to 5, cross-region possible)
- Point-in-time restore (up to 35 days)
- Automatic backups (daily full, continuous WAL)

**Spring Boot configuration for read/write split:**
```java
@Configuration
public class RoutingDataSourceConfig {
    
    @Bean
    public DataSource routingDataSource() {
        Map<Object, Object> targetDataSources = new HashMap<>();
        targetDataSources.put("write", writeDataSource());
        targetDataSources.put("read", readDataSource());
        
        RoutingDataSource routingDataSource = new RoutingDataSource();
        routingDataSource.setTargetDataSources(targetDataSources);
        routingDataSource.setDefaultTargetDataSource(writeDataSource());
        return routingDataSource;
    }
}

public class RoutingDataSource extends AbstractRoutingDataSource {
    @Override
    protected Object determineCurrentLookupKey() {
        return TransactionSynchronizationManager.isCurrentTransactionReadOnly() 
            ? "read" : "write";
    }
}
```

**Disaster recovery tiers:**

| Tier | RTO | RPO | Strategy |
|------|-----|-----|----------|
| Tier 1 (Critical) | < 1 min | 0 (zero data loss) | Synchronous replica, auto-failover |
| Tier 2 (Important) | < 15 min | < 5 min | Async replica, manual failover |
| Tier 3 (Standard) | < 4 hours | < 1 hour | Backup restore |

---

### Q10: How do you handle data migration and schema changes without downtime?

**Answer:**

**Expand-Contract pattern (zero-downtime migrations):**

```
Phase 1: EXPAND — Add new column/table (backward compatible)
Phase 2: MIGRATE — Backfill data, update application code
Phase 3: CONTRACT — Remove old column/table (cleanup)
```

**Example: Rename column `name` to `full_name`:**

```sql
-- Phase 1: Add new column
ALTER TABLE subscriber ADD COLUMN full_name VARCHAR(100);

-- Phase 2: Backfill (batched to avoid locks)
UPDATE subscriber SET full_name = name 
WHERE full_name IS NULL 
LIMIT 10000;  -- Run in batches

-- Application now writes to BOTH columns
-- Reads from full_name with fallback to name

-- Phase 3: After all reads migrated
ALTER TABLE subscriber DROP COLUMN name;
```

**Liquibase for safe migrations:**
```yaml
databaseChangeLog:
  - changeSet:
      id: add-full-name-column
      author: chokkar
      changes:
        - addColumn:
            tableName: subscriber
            columns:
              - column:
                  name: full_name
                  type: VARCHAR(100)
      rollback:
        - dropColumn:
            tableName: subscriber
            columnName: full_name

  - changeSet:
      id: backfill-full-name
      author: chokkar
      changes:
        - sql:
            sql: UPDATE subscriber SET full_name = name WHERE full_name IS NULL
```

**Rules for safe schema changes:**
- Never rename/drop a column in one step
- Never add a NOT NULL column without a default
- Add indexes CONCURRENTLY (`CREATE INDEX CONCURRENTLY`)
- Run migrations before deploying new application code
- Test migrations against production-size data
- Always include rollback steps
