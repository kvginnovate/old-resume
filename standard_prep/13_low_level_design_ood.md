# Low-Level Design & OOD Prep Guide

> LLD at Principal level: design a real-world system at the class level, then explain how it scales, handles concurrency, and survives production. Prove you can code the architecture you draw.

---

## The LLD Framework

1. **Clarify scope** — Single-user or multi-tenant? Need persistence?
2. **Identify entities** — Nouns from problem → classes. Group by domain
3. **Define relationships** — 1-to-1, 1-to-many, composition vs aggregation
4. **Apply patterns** — "Classic State pattern — machine behaves differently per state"
5. **Handle edge cases** — Null, empty, concurrent access, resource exhaustion
6. **Principal-level twist** — "Works for single JVM. For 10M users, partition by X and add caching"

**Interviewers watch your process, not the final answer.** Sketch before writing code.

---

## Top 5 OOD Problems

### 1. Parking Lot
**Entities:** `ParkingLot`, `Level`, `Spot` (COMPACT/LARGE/HANDICAPPED/ELECTRIC), `Vehicle` (abstract: `Car`, `Truck`, `Motorcycle`, `EV`), `Ticket`, `Gate`, `Payment`, `DisplayBoard`.
**Patterns:** Factory (vehicles), Strategy (pricing), Observer (display board), Singleton (lot).
**Watch for:** Spot assignment algorithm (nearest vs most-empty), EV charging, full-lot handling.

### 2. Vending Machine
**Entities:** `VendingMachine`, `Shelf`, `Product`, `Coin`/`Note` (enum), `Inventory`, `Transaction`, `Display`.
**Patterns:** **State** (Idle→HasMoney→Dispensing→ChangeReturn — each state owns `insertCoin`/`selectProduct`/`dispense`), Strategy (payment), Command (cancel).
**Watch for:** State transitions are the core test. Sold out, exact change, cancelling mid-flow.

### 3. Library Management System
**Entities:** `Library`, `Member`, `Book` (title, ISBN), `BookItem` (copy — barcode, rack, status), `Rack`, `Reservation`, `Fine`, `Notification`, `Catalog`.
**Patterns:** Factory (BookItem from Book), Observer (notify on available), Strategy (fine by member type), Builder (search).
**Watch for:** Separate `Book` from `BookItem` — the most common miss. Reservation ordering, concurrent booking.

### 4. Elevator System
**Entities:** `ElevatorController`, `ElevatorCar`, `Floor` (up/down buttons), `Request` (INTERNAL/EXTERNAL), `Door`, `Display`, `Alarm`.
**Patterns:** **Strategy** (scheduling: FCFS, SCAN, LOOK, SSTF), **State** (MovingUp/Down, Idle, DoorOpen, Emergency), Observer.
**Watch for:** Algorithm selection — why SCAN beats FCFS under load. Door safety, peak-hour optimization. Multiple cars must not collide.

### 5. ATM / Banking System
**Entities:** `ATM`, `CashDispenser`, `CardReader`, `Screen`, `Keypad`, `Printer`, `Session`, `Transaction` (abstract: Withdrawal, Deposit, Transfer, BalanceInquiry), `Account` (Checking, Savings), `Bank`.
**Patterns:** **State** (Idle→CardInserted→PinEntered→Processing→Complete), Strategy (cash dispensing), Command (each transaction — undoable, loggable), Factory.
**Watch for:** Cash dispense algorithm (minimum bills). PIN 3-attempt retain. Session timeout. Concurrent access. Audit trail.

---

## Design Patterns (Java)

| Pattern | Java Example |
|---------|-------------|
| **Singleton** | `enum ParkingLot { INSTANCE }` — serialization/reflection-safe |
| **Factory** | `Vehicle create(String type) → new Car()` / `new Truck()` |
| **Strategy** | `PricingStrategy` interface → `HourlyPricing`, `EventPricing` |
| **Observer** | `Subject.notifyObservers()`; `DisplayBoard implements Observer` |
| **Builder** | `new Booking.Builder().withMember(m).withBook(b).build()` |
| **Decorator** | `Transaction` wrapped by `AuditableTransaction` |
| **State** | `VendingMachine` delegates to `currentState.insertCoin()` |

**Principal tip:** Explain WHY the pattern fits. "State because the machine has mutually exclusive modes. Adding a state with if-else touches every method."

---

## SOLID Principles

| Principle | One-Liner | Example |
|-----------|-----------|---------|
| **S** | One reason to change per class | `Ticket` shouldn't print itself — that's `Printer` |
| **O** | Open for extension, closed for modification | New `HolidayPricing` without touching `ParkingLot` |
| **L** | Subclass must fulfill parent's contract | `ElectricSpot extends Spot` — no `UnsupportedOperationException` |
| **I** | Don't force unused methods on clients | `Parkable` vs `Chargeable`, not one giant interface |
| **D** | Depend on abstractions, not concretions | `ParkingLot` depends on `PricingStrategy`, not `HourlyPricing` |

---

## Class Relationships (Whiteboard)

| Notation | Meaning | Example |
|----------|---------|---------|
| `◁──` (empty arrow) | Inheritance | `Vehicle ◁── Car` |
| `◁····` (dashed arrow) | Interface | `Comparable ◁···· Ticket` |
| `◂──` (filled diamond) | Composition — owns, dies with | `Car ◂── Engine` |
| `◇──` (open diamond) | Aggregation — has, can exist without | `Car ◇── Wheel` |
| `──▶` (dashed arrow) | Dependency — uses temporarily | `ParkingLot ──▶ Ticket` |

---

## Principal-Level Twist: Beyond the Diagram

**Concurrency:** Parking lot → `ReentrantLock` per level (not per spot). `ConcurrentHashMap` for spot map. Elevator → `Semaphore` per floor prevents two cars opening at same shaft. ATM → optimistic locking: `UPDATE SET balance = balance - ? WHERE version = ?`.

**Caching & Scale:** Library catalog → `Caffeine` cache, TTL 5 min, 10k max. Invalidate on catalog update, not every borrow. Multi-location parking → shard by location ID, one JVM per location. Banking → `requestId` (UUID) for idempotency — prevents double-withdrawal on retry.

**Observability:** Vending machine → every state transition emits `state_transition_duration_seconds` to detect stuck machines. Elevator → log every scheduling decision, replay to tune algorithm.

---

## Quick Practice Checklist

- [ ] Explain the State pattern with a vending machine on the whiteboard
- [ ] Draw the Parking Lot class diagram with all relationships
- [ ] Name 3 SOLID violations you've fixed in production
- [ ] Describe how to make a Parking Lot handle 1000 concurrent requests
- [ ] Write a thread-safe singleton in Java (without double-checked locking pitfalls)