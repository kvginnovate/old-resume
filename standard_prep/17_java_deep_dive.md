> Java deep-dive for Principal Engineer interview at The Standard. JVM internals, concurrency, GC troubleshooting, Spring Boot internals, and modern Java features.

# Java Deep Dive — Principal Engineer Prep

## JVM Memory Model

- **Stack** (per-thread, `-Xss` 256k–1M): primitives + refs. StackOverflowError = deep recursion.
- **Heap** (shared): Young (Eden + S0/S1) → Old on promotion. **Metaspace** (native): class metadata. `-XX:MaxMetaspaceSize` to cap.
- **GC pick**: G1GC (default JDK 9+, 95% of apps), ZGC (sub-ms pauses), Shenandoah (concurrent compaction).
- **Tune when**: frequent Full GCs, SLA violations, throughput regressions.

---

## GC Troubleshooting

- **Logging**: `-Xlog:gc*:file=gc.log:time,uptime,level,tags`. `Pause Full` = bad (heap exhaustion or humongous allocation failure).
- **Heap dump**: `-XX:+HeapDumpOnOutOfMemoryError` or `jmap -dump:live,...`. Analyze with **Eclipse MAT**.
- **Common OOM patterns**: `char[]`/`byte[]` → I/O buffers; `HashMap$Node` → cache without eviction; `Finalizer` backlog → `finalize()` not collected.
- **Symptom map**: heap space OOM = leak/small heap. GC overhead limit = 98%+ in GC. Metaspace OOM = classloader leak (hot redeploy).

---

## Concurrency

**ThreadPoolExecutor**: `core → max` grows only when queue is **full**. Unbounded `LinkedBlockingQueue` = max never used. `CallerRunsPolicy` for back-pressure.

**ForkJoinPool**: work-stealing. `commonPool()` = `CPU - 1`. **Pitfall**: blocking ops starve the pool — use `ManagedBlocker`.

**CompletableFuture**: `thenApply`/`thenCompose` (transform), `thenCombine`/`allOf` (fan-in), `exceptionally`/`handle` (error recovery). **Avoid** `get()`.

**Virtual threads (JDK 21+)**: thread-per-request without OS overhead. **Limitations**: `synchronized` pins carrier (use `ReentrantLock`), `ThreadLocal` carries retained cost, CPU-bound gains nothing. Use for IO-bound only.

---

## Concurrency Bugs — Detection

- **Race**: `synchronized`, `Atomic*`, immutables. Detect via jstack + code review.
- **Deadlock**: jstack: `Found one Java-level deadlock`. Prevent with consistent lock ordering, `tryLock` timeout.
- **Livelock**: CPU 100%, no progress. Prevent with exponential backoff.
- **Starvation**: threads never get CPU. Prevent with fair locks, bounded pools.

**jstack**: `jstack -l <pid>`. Look for `BLOCKED`, `WAITING (parking)`, matching `owning`/`waiting to lock`.

---

## JVM Tuning

- `-Xms`/`-Xmx` equal (avoid resizing pauses). `-Xss` 256k–1M. `-XX:MaxGCPauseMillis=200`.
- `-XX:+HeapDumpOnOutOfMemoryError`, `-XX:+ExitOnOutOfMemoryError` — always in production. Enable GC logging.

---

## Spring Boot Internals

- **Auto-configuration**: `@EnableAutoConfiguration` scans `AutoConfiguration.imports`. `@ConditionalOnClass`/`@ConditionalOnMissingBean`/`@ConditionalOnProperty` drive conditions.
- **Key actuator endpoints**: `/health` (K8s probes), `/metrics` (Micrometer), `/threaddump`/`/heapdump` (on-demand), `/beans` (conditional results).
- **Startup optimization**: `spring.main.lazy-initialization=true`, `spring.jmx.enabled=false`, exclude unused auto-configs. GraalVM native-image (SB3) for AOT.
- **Graceful shutdown**: `server.shutdown: graceful` + `spring.lifecycle.timeout-per-shutdown-phase: 30s`.
- **Reactive vs imperative**: "Imperative (Tomcat) unless 1000+ concurrent connections or streaming. Reactive pays off only when the whole stack is reactive."

---

## Build Tools: Maven vs Gradle

- **Maven**: lifecycle phases, `dependencyManagement` + BOMs, parent POM for multi-module. XML, verbose but predictable.
- **Gradle**: task DAG (parallel), `platform()` + version catalog, `settings.gradle.kts` + `include(...)`. 2-10x faster.
- **Decision**: Gradle for new projects. Maven for existing enterprise — don't fight the build system.

---

## Java 17+ Features

- **Records** (JDK 16): DTOs, value objects. Replace Lombok `@Data`. Compact constructor for validation.
- **Sealed classes** (JDK 17): domain models, exhaustive switch. Compiler-enforced completeness — no `default` branch.
- **Pattern matching** (JDK 16+): `instanceof` + switch. No casts. Combine with sealed for exhaustive dispatch.
- **Text blocks** (JDK 15): `"""..."""` for multi-line SQL/JSON. No `+` concatenation.
- **Switch expressions** (JDK 14): `yield` + arrow syntax over traditional switch.

**Take**: "Records and sealed classes encode invariants the compiler enforces — fewer unit tests, fewer runtime bugs. Not syntactic sugar."