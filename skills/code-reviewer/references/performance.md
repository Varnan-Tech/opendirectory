# Performance

Report performance only where it bites at **realistic scale** — a slow path that runs on 5 rows once
a day is not a finding, the same path on every request over a growing table is. Always state the
scale assumption ("at thousands of rows / per request"). Micro-optimizations and "this could be a
hair faster" are Pass-B casualties; they're the easiest place to generate noise.

## N+1 queries (the most common real one)
A query to fetch a list, then one more query per item for related data. 100 items → 101 queries,
each with network latency. Degrades silently until the table grows.
- Spot it: a DB/API/`fetch` call **inside a loop** (or inside `.map`/list comprehension), where the
  data could be fetched in one batched query.
- Fix: eager-load / `JOIN` / `select_related`/`include` / `IN (...)` batch / DataLoader.

## Algorithmic blowups
- Nested loops over the same growing input → O(n²) where a set/map lookup makes it O(n). Classic:
  `for x in a: if x in b` with `b` a list (linear scan) instead of a set.
- Repeated work inside a loop that's invariant (recompiling a regex, re-reading a file, re-sorting).
- Accidental quadratic string building in tight loops (where the language makes concatenation O(n)).

## Memory & I/O
- Loading an unbounded result set fully into memory (no pagination/streaming/`LIMIT`) — fine in dev,
  OOM in prod.
- Unbounded growth: a cache/list/map that's appended to forever with no eviction → slow leak.
- Reading a large file/response fully when it could be streamed.
- Chatty network: N sequential awaited calls that could be parallelized or batched.

## Caching / redundant calls
- The same expensive call repeated within one request that could be computed once.
- A cache keyed wrong (too coarse → stale, too fine → never hits) — but only flag if you can show the
  consequence.

## Calibration
Quantify the impact when you can ("each request now does N DB round-trips"). If you can't explain why
it matters at scale, don't report it. Correctness of behavior always outranks speed — if a change is
both wrong and slow, it's a correctness finding first.
