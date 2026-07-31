> Practical DSA preparation guide for Principal Engineer coding rounds. Focuses on problem-solving structure, communication, and Java-specific patterns over grinding 500 problems.

# Coding & DSA Prep — Principal Software Engineer V (IBTE) at The Standard

## Mindset: Principal-Level Coding

At 14+ years, you are not being tested on LeetCode grinding. The interviewer evaluates:
- **Problem decomposition** — do you clarify constraints before jumping in?
- **Communication** — can you think aloud, explain tradeoffs, and handle feedback?
- **Code quality** — is the code clean, idiomatic Java, production-grade?
- **Optimization instinct** — can you identify the bottleneck and improve it?

The bar is not "solved optimally" — it is "solved methodically with clear reasoning."

---

## Focused Study Plan (2 Weeks)

### Week 1: Core Patterns (3-4 problems/day, 1 hour each)

| Day | Pattern | Key Concept |
|-----|---------|-------------|
| 1 | Arrays & Strings | Two-pointer, in-place reversal, prefix sums |
| 2 | Hash Maps | Frequency counting, complement pairs, sliding window |
| 3 | Two Pointers & Sliding Window | Subarray/ substring problems, O(n) window management |
| 4 | Binary Search | Searching sorted/rotated arrays, boundary conditions |
| 5 | Linked Lists | Fast/slow pointer, reversal, merge |
| 6 | Trees (BFS/DFS) | Recursive traversal, level-order, lowest common ancestor |
| 7 | Recursion & Basic DP | Memoization, bottom-up, Fibonacci, knap-sack variants |

### Week 2: Application & Mock

| Day | Focus |
|-----|-------|
| 1 | Stack & Queue (monotonic stack, calculator problems) |
| 2 | Heaps & PriorityQueue (top-K, median, merge K sorted) |
| 3 | Mixed pattern review — 2 medium problems back-to-back |
| 4 | Mock coding round (45 min, full verbal walkthrough) |
| 5 | Review weak spots, re-solve 2 problems from scratch |

---

## The 3-Step Framework (Every Problem)

### Step 1: Clarify Constraints (2 min)

Ask before writing anything:
- Input size? (n=10 vs n=10^6 changes everything)
- Are elements sorted? Unique? Positive only?
- Output format? Modify in-place or return new?
- Edge cases: empty input, single element, duplicates, overflow?

**Script:** "Before I dive in, I want to confirm — is the input an unsorted array of integers, possibly empty? Can I assume O(1) extra space or is O(n) acceptable?"

### Step 2: Brute Force Then Optimize (3-5 min)

- State the naive solution first (even if obvious): "The straightforward approach is O(n^2) — check every pair."
- Identify the bottleneck: "The inner loop is scanning for a complement. A hash map removes that — O(n) time, O(n) space."
- Never skip this step. It shows you evaluate tradeoffs before coding.

### Step 3: Walk Through an Example (3 min)

- Pick a concrete input. Trace through your algorithm manually.
- Verify you handle the edge at each step.
- This catches bugs before you write a single line.

**Script:** "Let me trace on [1, 2, 3, 4] with target 6. First iteration, map is empty, store 1->0... Okay, we return [1, 3]."

---

## Recommended LeetCode Problems (Medium, Java-Focused)

### Arrays & Strings
- **LC 1** Two Sum (hash map variant)
- **LC 11** Container With Most Water (two-pointer)
- **LC 49** Group Anagrams (hash map keyed by sorted string)
- **LC 238** Product of Array Except Self (prefix/suffix arrays)
- **LC 3** Longest Substring Without Repeating Characters (sliding window)

### Trees & Graphs
- **LC 102** Binary Tree Level Order Traversal (BFS)
- **LC 236** Lowest Common Ancestor of a Binary Tree (recursive DFS)
- **LC 200** Number of Islands (DFS/BFS grid traversal)

### Dynamic Programming (Basic)
- **LC 53** Maximum Subarray (Kadane's algorithm)
- **LC 198** House Robber (linear DP, memoization)
- **LC 322** Coin Change (minimum coins, classic DP)

### Heap & Stack
- **LC 215** Kth Largest Element in an Array (PriorityQueue or QuickSelect)
- **LC 20** Valid Parentheses (stack, must be flawless)
- **LC 155** Min Stack (two-stack or pair stack)

---

## Big-O Cheat Sheet

| Operation | Arrays | ArrayList | HashMap | TreeMap | PriorityQueue | HashSet |
|-----------|--------|-----------|---------|---------|---------------|---------|
| Access | O(1) | O(1) | O(1)* | O(log n) | O(1) (peek) | O(1)* |
| Search | O(n) | O(n) | O(1)* | O(log n) | O(n) | O(1)* |
| Insert | O(n) | O(1) amortized | O(1)* | O(log n) | O(log n) | O(1)* |
| Delete | O(n) | O(n) | O(1)* | O(log n) | O(log n) | O(1)* |

| Algorithm | Time | Space |
|-----------|------|-------|
| Quicksort (average) | O(n log n) | O(log n) |
| Mergesort | O(n log n) | O(n) |
| BFS/DFS (tree) | O(n) | O(h) — height |
| BFS (graph) | O(V+E) | O(V) |
| DFS (graph) | O(V+E) | O(V) |
| Binary Search | O(log n) | O(1) |

*O(1) average, O(n) worst-case for hash collisions.

---

## How to Structure Your Answer Aloud

### Opening (30 sec)
> "I see this as a [pattern] problem. The key constraint is [X]. Let me walk through my approach."

### During Coding (visible narration)
- **Say what you are about to write before writing it:** "I'll use a HashMap to store complements as I iterate."
- **Explain why, not just what:** "HashMap gives O(1) lookup, which removes the nested loop."
- **Verbally check edge cases:** "If the input is empty, we return early."

### When Stuck
- **Verbalize the blocker:** "I'm stuck on handling duplicates. Let me think about using a frequency map instead."
- **State an assumption:** "I'll assume unique elements for now and note that requirement."
- **Ask for guidance:** "Should I optimize for time or space here?"

### After Coding
- **Trace with an example:** "Starting with [3, 2, 4], target 6. First iteration: map is empty, store 3->0..."
- **State complexity unprompted:** "Time is O(n), space is O(n)."
- **Offer to improve:** "If space were constrained, I could sort first and use two pointers — O(n log n) time, O(1) space."

---

## Java-Specific Tips

### Do Use
- **`StringBuilder`** for any string concatenation in a loop. `String +=` creates O(n^2) garbage.
- **`HashMap`** for frequency / complement lookup. Default to `HashMap`, not `TreeMap` (O(log n) vs O(1)).
- **`PriorityQueue`** for top-K / median / merge-K problems. Default min-heap, use `Comparator.reverseOrder()` for max-heap.
- **`Collections.sort(list, Comparator)`** with lambda. Know how to write a custom comparator inline.
- **`Optional`** for null-safe return values in helper methods — but **never** use it as a method parameter.
- **Streams** for one-liner transformations (map, filter, collect). But for loops when performance matters or early exit is needed (streams have no `break`).
- **`Deque` (ArrayDeque)** over `Stack` class. `Stack` is legacy, `Deque` is the modern API.

### Avoid
- **Raw types** — always parameterize (`List<Integer>`, not `List`).
- **`==` on Integer** — use `.equals()`. Integer caching works for -128 to 127 only.
- **`Arrays.asList()` returned list** — it is fixed-size. Use `new ArrayList<>(Arrays.asList(...))` if you need to add/remove.
- **`char` arithmetic for digit conversion** — `Character.getNumericValue(c)` is clearer than `c - '0'`.

### Utility Methods to Memorize
```java
char[] chars = s.toCharArray();
String reversed = new StringBuilder(s).reverse().toString();
int[] freq = new int[256]; // for ASCII character counting
int[] copy = Arrays.copyOfRange(arr, 0, arr.length);
Arrays.sort(arr); // dual-pivot quicksort on primitives
List<Integer> list = Arrays.stream(arr).boxed().collect(Collectors.toList());
```

---

## What NOT to Waste Time On

| Skip | Why |
|------|-----|
| Hard LeetCode problems | Principal coding rounds rarely use them. Focus on mediums. |
| Advanced DP (edit distance, DP on trees, DP with bitmask) | Not asked at this level. Know basic DP (memoization, bottom-up). |
| Graph algorithms beyond DFS/BFS | Dijkstra, Floyd-Warshall, Bellman-Ford are not expected. |
| Segment trees, Fenwick trees | Niche. Not worth the prep time. |
| Trie | Rare. If it comes up, you can adapt on the fly. |
| Competitive programming tricks | Skip monotonic queue, string hashing, rolling hash. |
| Tricky bit manipulation | Know basic XOR, AND, shift. Do not memorize 30 bit tricks. |

**Your time is better spent on:** clean problem-solving structure, verbal communication, Java fluency, and confidence with the 10-15 recommended problems above.

---

## One-Hour Quick Review (Day Before Interview)

1. **Two Sum** (HashMap) — the warm-up, must be flawless
2. **Valid Parentheses** (stack) — classic, tests fundamental data structure
3. **Maximum Subarray** (Kadane) — only DP you need to know cold
4. **Binary Tree Level Order** (BFS queue) — tree traversal pattern
5. **Kth Largest** (PriorityQueue) — heap pattern
6. Write quicksort/mergesort from memory — just once
7. Review Big-O cheat sheet above
8. Say the 3-step framework aloud from memory