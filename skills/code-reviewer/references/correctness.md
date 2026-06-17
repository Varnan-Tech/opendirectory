# Correctness

The primary dimension. Most production incidents are correctness bugs, and most correctness bugs are
the code doing something *other than what the change intended* — not exotic algorithm errors. Judge
the diff against its stated intent (PR/ticket/commit), then against reality (nulls, empties, retries,
concurrency). Patterns below are language-agnostic; the examples just illustrate the shape.

## Intent vs. implementation
The highest-value check. The code can be internally clean and still wrong.
- Does the change actually do what the PR says? Off-by-one in a "fix the boundary" PR, a filter that
  excludes the wrong side, a flag wired backwards.
- Did it change a function/endpoint/type signature, return shape, or error contract that **callers
  rely on**? Check the callers. A contract changed on one side only is a real bug even if both files
  compile.

## Error handling
- **Swallowed errors.** Bare `catch {}` / `except: pass` / ignored error returns hide failures until
  data is already corrupt. Errors should be handled or propagated, with enough context to debug.
- **Unchecked results.** Using a lookup/parse/fetch result without checking it succeeded → null deref,
  `IndexError`, reading a field off `undefined`. New external calls especially.
- **Wrong-layer handling.** Catching everything at the top and logging "error occurred" loses which
  operation failed and why. Catch specific, near the cause.
- Go/Rust-style: an ignored `err` / unhandled `Result` is the same bug in different clothes.

## Edge cases
Walk the new code with the inputs nobody tested: empty collection, single element, zero/negative,
absent optional field, duplicate, very large input, unicode, timezone/DST for dates. The "happy path
works" demo hides these.

## Concurrency & races
Flag when changed code touches shared state without protection:
- Check-then-act on shared data (TOCTOU): `if not exists: create` racing another caller.
- Read-modify-write without a lock/transaction/atomic (counters, balances, `i++` on shared state).
- `async`/await that assumes ordering it doesn't have; promises not awaited; missing `await` on a
  call whose result or side-effect the next line depends on.
- Shared mutable state captured by a closure or goroutine/thread.

## Data flow & validation
- Untrusted input reaching a sink without validation (overlaps Security — note it once, in whichever
  dimension is more severe).
- Type/unit confusion: seconds vs. ms, cents vs. dollars, 0-indexed vs. 1-indexed, string `"0"` truthy.
- State that can desync: two fields that must move together but are updated in separate steps with a
  failure point between them.

## Tests (report only when the change clearly warrants them)
New non-trivial logic, a bug fix, or a money/security/auth path should carry a test — ideally one
that fails without the change. Don't demand tests for trivial or mechanical edits; that's noise.
Frame as: "this branch has no test and would regress silently," not "coverage is low."

## Calibration
- Correctness findings are almost always worth reporting — this is the dimension to be thorough on.
- Still require evidence: name the input or interleaving that triggers the failure. "This might break
  with weird input" without a concrete case is a Pass-B casualty, not a finding.
