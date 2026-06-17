# Simplification (the lazy-senior lens)

Most reviewers only catch what's *broken*. This dimension catches what's *needless* — the abstraction
nobody needed, the config no one will change, the 40 lines that should be 5. The best code is the
code never written, and unnecessary complexity is itself a long-term bug: it's what someone has to
decode at 3am.

But this is the noisiest dimension if you let it be, because "simpler" is subjective and LLMs are
weaker judges of maintainability than of correctness. So two rules gate everything here:

1. **Behavior must not change.** Every simplification you suggest must be exactly behavior-preserving.
   If you're not sure it preserves edge cases, don't suggest it.
2. **Clarity over brevity.** The goal is *less to understand*, not *fewer characters*. Do not suggest
   removing a helpful abstraction, a clarifying intermediate variable, or a guard clause just to
   shrink line count. Collapsing readable code into a dense one-liner is a *worse* review than saying
   nothing — see the over-simplification traps at the bottom.

Only report a simplification when you can name what's not pulling its weight and why removing it is
safe. When in doubt, drop it in Pass B.

## What to flag

**Speculative generality (YAGNI).** Machinery built for a future that isn't here:
- An interface/abstract base/strategy with exactly one implementation, and no second one in sight.
- A factory/builder/wrapper that only ever produces one thing.
- A config value, parameter, or feature flag that's never varied (always the same constant).
- A generic `<T>`/`options` bag where the code only uses one concrete case.
- Fix: inline the single case; add the abstraction back the day the second case actually exists.

**Dead / unreachable code introduced or revealed by the change:**
- A new branch that can't be taken, a parameter passed but never read, an import/helper added but
  unused, code after an unconditional return/throw.

**Reinventing the platform.** A hand-rolled version of something the stdlib, language, or an
*already-installed* dependency does — date math, deep clone, debounce, grouping, UUID, retry. Flag
the few lines and name the built-in. (Don't suggest adding a *new* dependency for something a few
lines do fine — that's the opposite mistake.)

**Doing too much in one unit.** A function whose honest name would need "and" (`validateAndSaveAndNotify`)
is doing several things and is hard to test and reuse. Suggest splitting along the seams.

**Needless control-flow complexity:**
- Nested ternaries — prefer an `if/else` chain or a lookup/switch; they're far easier to read.
- Deep nesting that an early-return / guard clause flattens.
- A boolean built up through several reassignments that one expression captures.
- Re-checking a condition already guaranteed true.

**Comment & duplication smells (low severity, report sparingly):**
- A comment that restates the code, or worse, now contradicts it after the change.
- The same non-trivial block copy-pasted in the diff that should be one helper — but only if the
  duplication is real and the extraction is obviously clean.

## Over-simplification traps — do NOT report these
- Splitting a clear linear function into many tiny ones just to shrink each (over-decomposition).
- Removing a guard clause, validation, or error branch — those are correctness, not clutter.
- Replacing a readable loop with an unreadable clever reduce/comprehension.
- "This whole module could be rewritten" — out of scope; review the change, not the architecture.
- Naming/formatting preferences — not a finding unless the name is actively misleading.

## Calibration
Simplification findings are almost never Critical/High — they're improvements, not bugs. A genuinely
over-engineered new abstraction is Medium; minor cleanups are Low and should be few. If a simpler
form would also fix a bug, report it under Correctness instead.
