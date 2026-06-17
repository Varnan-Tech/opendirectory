# Severity, output format, and false-positive control

## Why severity needs anchoring
LLM reviewers agree with each other on *whether* something is a bug far more than on *how severe* it
is — severity left to feel is the least reliable thing a reviewer produces. So decide severity by the
concrete gate below, not by how bad it sounds. When unsure between two levels, the deciding question
is **"does this block the merge?"** — yes → Critical/High, no → Medium/Low.

| Severity | Gate (concrete) | Action |
|----------|-----------------|--------|
| 🔴 **Critical** | Security hole reachable from untrusted input; data loss/corruption; crash on a normal path. | Block merge. Fix now. |
| 🟠 **High** | A real bug on a plausible path; a contract/API break for existing callers. | Fix before merge. |
| 🟡 **Medium** | Works today but will bite: unhandled edge case, perf cliff at scale, fragile coupling, over-engineered new abstraction. | Fix before merge, or accept with a noted reason. |
| ⚪ **Low** | Genuine but non-blocking improvement (minor cleanup, small simplification). | Optional. Keep these rare. |

Asymmetry to aim for, drawn from how the better tools tune: be effectively 100% thorough on
Critical/High (missing one is the real cost), and accept lower volume on Medium/Low (a missed nitpick
costs nothing, a false one costs trust). Target: zero false positives at the Critical tier.

## Finding format
Each finding carries severity, location, the issue *with its consequence*, the quoted evidence, and a
fix. The fix is the point — a finding the author can apply in one step is worth ten they have to
re-derive.

```
### 🔴 [CRITICAL] SQL injection in user lookup
**File:** api/users.py:42
**Issue:** `user_id` comes straight from the request and is interpolated into the query, so a crafted
value runs arbitrary SQL (auth bypass, full-table read).
**Evidence:**
    query = f"SELECT * FROM users WHERE id = {user_id}"
**Fix:** use a parameterized query:
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

## Report structure
Group findings by dimension (Correctness → Security → Performance → Simplification), most severe
first within each. Then a verdict line and counts.

```
## Code Review: <what was reviewed>

<one-sentence summary: does it do what it intends, and the headline issue if any>

## Correctness
### 🟠 [HIGH] ...
## Security
### 🔴 [CRITICAL] ...
## Performance
(none)
## Simplification
### ⚪ [LOW] ...

---
**Verdict: 🔴 Needs Work** — 🔴 1  🟠 1  🟡 0  ⚪ 1
```

**Verdict rule:** any Critical/High → **Needs Work**. Only Medium → **Needs Attention**. Nothing above
Low → **Ready to Merge**.

## False-positive control (the discipline that makes this skill worth using)
- **Only touched code.** Don't comment on lines the change didn't modify (unless the change makes
  pre-existing code newly reachable/broken — then say how).
- **Evidence or it didn't happen.** Every finding names the concrete failure, input, or cost. "This
  could be problematic" with no scenario is not a finding.
- **No style nits.** Formatting, import order, naming preferences, and "I'd write it differently" are
  not findings unless they cause a bug or real confusion. Linters own that lane.
- **Don't pad.** Do not invent Low findings to look thorough. Three real findings beat three real
  plus seven cosmetic — the seven bury the three.
- **Clean is a valid result.** If nothing meets the bar, say "No blocking issues; behavior matches
  intent" and stop. That is a successful review, not a lazy one.
- **De-dup.** One root cause repeated across several lines is one finding ("same pattern at lines
  X, Y, Z"), not five.

## When to broaden scope
The defaults above are deliberately tight. If the user explicitly asks for a deeper or whole-codebase
pass, a security-only audit, or "be picky about style too," follow that — adjust the bar to what they
asked for and say what you changed.
