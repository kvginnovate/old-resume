> SQL & NoSQL interview prep for Principal Engineer at The Standard. Covers core query patterns, window functions, optimization, isolation levels, migration patterns, and the SQL-vs-NoSQL decision framework at Principal altitude.

## Core Query Patterns

### SELECT & JOINs

```sql
-- INNER JOIN — only matching rows
SELECT e.name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id;

-- LEFT JOIN — all employees, departments optional
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id;

-- RIGHT JOIN — all departments, employees optional
SELECT e.name, d.dept_name
FROM employees e
RIGHT JOIN departments d ON e.dept_id = d.id;

-- FULL OUTER JOIN — everything
SELECT e.name, d.dept_name
FROM employees e
FULL OUTER JOIN departments d ON e.dept_id = d.id;
```

### GROUP BY / HAVING

```sql
-- Filter groups after aggregation (HAVING, not WHERE)
SELECT d.dept_name, COUNT(*) AS headcount, AVG(e.salary) AS avg_salary
FROM employees e
JOIN departments d ON e.dept_id = d.id
GROUP BY d.dept_name
HAVING AVG(e.salary) > 80000;
```

### Subqueries vs CTEs

```sql
-- Subquery (inline)
SELECT name FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- CTE (preferred for readability + recursion)
WITH dept_avg AS (
  SELECT dept_id, AVG(salary) AS avg_sal
  FROM employees GROUP BY dept_id
)
SELECT e.name, d.dept_name, e.salary, da.avg_sal
FROM employees e
JOIN departments d ON e.dept_id = d.id
JOIN dept_avg da ON e.dept_id = da.dept_id
WHERE e.salary > da.avg_sal;
```

---

## 5 Practice Queries with Solutions

**Schema 1: Employee-Department**
```sql
-- Q1: Find departments with no employees
SELECT d.dept_name FROM departments d
LEFT JOIN employees e ON d.id = e.dept_id
WHERE e.id IS NULL;

-- Q2: Top 3 highest-paid employees per department
SELECT name, dept_id, salary FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rn
  FROM employees
) ranked WHERE rn <= 3;
```

**Schema 2: Order-Customer**
```sql
-- Q3: Customers who have not placed an order in 2025
SELECT c.name FROM customers c
WHERE c.id NOT IN (
  SELECT DISTINCT customer_id FROM orders
  WHERE order_date >= '2025-01-01' AND order_date < '2026-01-01'
);

-- Q4: Running total of orders per customer
SELECT customer_id, order_date, amount,
       SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS running_total
FROM orders;
```

**Schema 3: Product-Sales**
```sql
-- Q5: Month-over-month sales change by product
SELECT product_id,
       DATE_TRUNC('month', sale_date) AS month,
       SUM(amount) AS monthly_sales,
       LAG(SUM(amount)) OVER (PARTITION BY product_id ORDER BY DATE_TRUNC('month', sale_date)) AS prev_month,
       SUM(amount) - LAG(SUM(amount)) OVER (PARTITION BY product_id ORDER BY DATE_TRUNC('month', sale_date)) AS change
FROM sales
GROUP BY product_id, DATE_TRUNC('month', sale_date);
```

---

## Window Functions Deep-Dive

```sql
-- ROW_NUMBER — unique rank, no ties
ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC)

-- RANK — ties share rank, next skips (1,1,3)
RANK()       OVER (PARTITION BY dept_id ORDER BY salary DESC)

-- DENSE_RANK — ties share rank, next does not skip (1,1,2)
DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC)

-- LAG — previous row's value
LAG(salary) OVER (PARTITION BY dept_id ORDER BY hire_date)

-- LEAD — next row's value
LEAD(salary) OVER (PARTITION BY dept_id ORDER BY hire_date)

-- Moving aggregate
AVG(amount) OVER (PARTITION BY product_id ORDER BY sale_date
                  ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
```

**Principal-level insight:** Window functions avoid self-joins and subqueries, reducing planner complexity. `RANGE BETWEEN` vs `ROWS BETWEEN` matters for ties — `RANGE` includes peers, `ROWS` is exact.

---

## Query Optimization

### Use EXPLAIN PLAN

```sql
EXPLAIN ANALYZE SELECT ...;  -- PostgreSQL
EXPLAIN PLAN FOR SELECT ...; -- Oracle
```

Look for: **Seq Scan** on large tables (needs index), **Nested Loop** vs **Hash Join** (join order), **Sort** (can index cover it).

### Index Strategies

| Index Type | When | Principal Note |
|-----------|------|----------------|
| B-tree | Equality + range queries | Default, covers `=`, `>`, `BETWEEN`, `LIKE 'foo%'` |
| Composite | Multi-column filters | Order matters: `(dept_id, salary)` supports `WHERE dept_id=X` but not `WHERE salary>Y` alone |
| Covering | All columns in query | Index-only scans — no heap access |
| Partial | Filtered subset | `CREATE INDEX ON employees(salary) WHERE active=true` |
| DESC | ORDER BY DESC | Avoids reverse-scan overhead |

### When to Denormalize

**Denormalize when:** Read-heavy dashboards, reporting queries joining 5+ tables, caching layer can't absorb latency, or the query runs in a critical user path.

**Keep normalized when:** Write throughput matters, data integrity is paramount, or the team can't maintain sync logic.

---

## SQL vs NoSQL (Principal-Level Decision Framework)

| Dimension | SQL | NoSQL |
|-----------|-----|-------|
| **Relationships** | Complex joins, referential integrity | Embedded documents, denormalized refs |
| **Schema** | Rigid, migrations required | Flexible, schema-on-read |
| **Consistency** | ACID, strong | Eventual (tunable per operation) |
| **Scaling** | Vertical-primary, read replicas | Horizontal by default, sharding native |
| **Query** | Declarative, joined, ad-hoc | Key-based, limited scan patterns |

**Principal answer framework:**

1. **Start with the data shape.** Deeply relational (financial, inventory) → SQL. Document-shaped (profiles, content) → NoSQL.
2. **Check the consistency contract.** Funds transfer needs ACID. User activity feed can tolerate eventual consistency.
3. **Consider the access pattern.** Known queries, aggregated reporting → SQL. Key-value lookups, high-velocity writes → NoSQL.
4. **Polyglot persistence is the norm.** Use SQL for the ledger, Redis for session cache, Elasticsearch for search — not one hammer.

---

## Transaction Isolation Levels

| Level | Dirty Read | Non-Repeatable Read | Phantom Read | When It Matters |
|-------|-----------|---------------------|-------------|-----------------|
| **READ UNCOMMITTED** | Possible | Possible | Possible | Never in production |
| **READ COMMITTED** | Safe | Possible | Possible | Default in PG/SQL Server. Safe for most apps |
| **REPEATABLE READ** | Safe | Safe | Possible | Financial reports, balance checks mid-transaction |
| **SERIALIZABLE** | Safe | Safe | Safe | Ledger operations, inventory allocation, concurrent inserts |

**Principal answer:** "READ COMMITTED is the sensible default — it prevents dirty reads without the performance tax of snapshot isolation. Escalate to REPEATABLE READ only when a transaction reads the same row twice and must see the same values (e.g., debiting from balance, then checking the balance). Use SERIALIZABLE when business logic assumes a row doesn't exist and a concurrent insert would break it — but be prepared for serialization failures and retry logic."

---

## Expand-Contract Migration Pattern

For schema changes on a live system without downtime:

```
Phase 1 — EXPAND
  Add the new column/table alongside the old one.
  Application writes to both. Reads from old.

Phase 2 — MIGRATE
  Backfill the new structure for existing data.
  Dual-write remains; reads switch to new.

Phase 3 — CONTRACT
  Remove the old column/table.
  Application reads and writes only the new structure.
```

**Example:** Renaming `orders.status` to `orders.order_state`:

1. `ALTER TABLE orders ADD COLUMN order_state VARCHAR(20);` — app writes to both
2. Backfill: `UPDATE orders SET order_state = status;` — app reads from `order_state`
3. `ALTER TABLE orders DROP COLUMN status;` — app code cleans up references

**Principal-level insight:** "The expand-contract pattern is how we deliver zero-downtime schema changes. Every PR touching a schema must include the rollback plan — you can't roll back a column drop. Always coordinate with the deploy pipeline: the app code change that stops writing to the old column ships in a separate deploy from the drop."