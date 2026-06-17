# Codebase mode

Reviewing a whole repo, a directory, or a single file is a different job from reviewing a diff. There's
no change to anchor to, and a large codebase has more lines than you can meaningfully judge in one pass.
Two failure modes to avoid: reading every line and drowning the real issues in a flat list of nitpicks,
or skimming and silently missing the high-risk code. The fix is the same as everywhere else in this
skill — precision over volume — applied with a risk-first plan and an honest coverage report.

## 1. Map the project first
Before reviewing anything, get the shape of it:
- File list: `git ls-files` (or a tree). Note size — number of files, rough lines.
- Languages and frameworks, entry points (`main`, server bootstrap, route definitions, CLI).
- Where the trust boundaries are: anything that takes outside input.

State up front what you'll cover. For a small file or directory, that's "all of it." For a large repo,
that's "the highest-risk surfaces first" — and you name them.

## 2. Prioritize by risk, not by directory order
Spend effort where a bug hurts most. Review these surfaces first; they're where Critical/High live:
- **Auth and authorization** — login, sessions, tokens, ownership checks, role gates on new actions.
- **Input handlers** — HTTP/API routes, form/file/upload handlers, message consumers, anything parsing
  outside input.
- **Data access** — query building, ORM usage, migrations (irreversible/locking changes).
- **Money and critical state** — billing, balances, inventory, anything where a wrong number is a real loss.
- **Dangerous sinks** — shell/exec, file paths, deserialization, template rendering, crypto, secrets.
- **Concurrency** — shared state, locks, background jobs, anything async touching the same data.
Lower-risk code (pure formatting helpers, static config, presentational UI) gets a lighter pass or is
skipped — say which.

## 3. Review each area with the normal method
Apply the same dimensions in the same order (correctness → security → performance → simplification),
the same two-pass filter, the same severity gates, and the same finding format from `output.md`. The
only change is scope: "in scope" means "in the files under review," not "in the diff."

Cross-file checks matter more here than in a diff. Look for the same logic duplicated and drifted
across files, a utility reimplemented instead of reused, and auth/validation applied on some endpoints
but missing on others. Those are invisible when you read one file at a time.

## 4. Group findings and report coverage honestly
- Group findings by file or subsystem, most severe first — not one flat list.
- End with a **coverage report**: which areas you reviewed in full, which you sampled, and which you
  skipped and why. If the repo is too large for one pass, review the highest-risk slice, say so
  plainly, and list what remains for a follow-up. Never imply you covered everything when you sampled.
- A clean subsystem gets one line ("auth: reviewed, no issues"), not silence and not invented findings.

## Calibration
Precision still rules. An "audit" that returns 200 style comments is a failure, not thoroughness. Lead
with Critical/High, keep Medium focused, and let Low be rare. If the user asks you to be exhaustive or
to include style, widen the bar and say what you changed — but the default here is the same high-signal
review as diff mode, spread across files by risk.
