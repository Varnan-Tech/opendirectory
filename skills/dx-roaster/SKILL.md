---
name: dx-roaster
description: 'Brutally honest developer-experience audit for a GitHub repo. Scores 10 DX dimensions (time-to-first-success, README clarity, visual proof, install, quick-start, docs, examples, community, trust, marketing), writes a shareable roast in the requested tone (brutal/honest/kind), produces a prioritized action plan ranked by impact × effort, and sketches an ideal README. Trigger when user says "roast my repo", "audit my README", "dx audit", "developer experience review", "score my GitHub project", "before launch checklist", or "make my repo shareable".'
compatibility: [claude-code, gemini-cli, github-copilot]
author: OpenDirectory
version: 1.0.0
---

# dx-roaster

Roasts a GitHub repo's developer experience. Produces four files: `roast.md`, `action-plan.md`, `ideal-readme.md`, `score.json`. Built for OSS maintainers and dev-tool founders preparing for Show HN, Product Hunt, or any launch where the first five minutes matter.

---

## Critical rules (read before every run)

1. **Read all three reference files BEFORE scoring.** `references/scoring-rubric.md`, `references/roast-voice-guide.md`, `references/readme-template.md`. The rubric is non-negotiable — use the exact 10 dimensions.

2. **Score every dimension on the 0–10 scale. Never skip.** Missing data = score 0, not "N/A".

3. **Roast must cite specific findings.** Quote bad lines verbatim. Reference file paths. Cite line numbers when possible. Never write generic platitudes like "documentation could be better".

4. **Tone matters.** Default `honest`. Switch voice per `references/roast-voice-guide.md`. Brutal is funny but never personal. Kind is encouraging but still specific.

5. **Action plan is impact-ranked, not severity-ranked.** Use `impact × (1 / effort)`. A 5-minute fix that adds 10 points ranks above a 2-hour fix that adds 12 points.

6. **Never invent URLs.** When writing `ideal-readme.md`, use `<placeholder>` syntax for missing links. Roast will tell maintainer to fill in.

7. **Never name maintainers or contributors.** Roast the work, not the people.

8. **Output exactly four files** in `dx-roast/`. Do not write to other locations. Do not skip files.

---

## Step 1: Intake

**Required:**
- `repo` — local path (default `.`) OR `https://github.com/owner/repo` URL

**Optional:**

| Parameter | Default | Description |
|---|---|---|
| `tone` | `honest` | `brutal` / `honest` / `kind` |
| `output_dir` | `dx-roast/` | Where to write the 4 output files |
| `compare_to` | none | Optional second repo URL for benchmark comparison |

If `repo` is a URL: clone to a temp dir using `git clone <url> /tmp/dx-roast-<short-hash>`. Scan from there. Delete temp dir after run.

If `repo` is `.` or local path: scan in place, do not modify anything.

---

## Step 2: Discover

Read these files (each may be absent — note absence):
- `README.md` — full contents, structure (headings), code blocks, image refs, badge URLs
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`
- `.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/CODEOWNERS`
- `package.json` (description, homepage, repository, license, scripts), `pyproject.toml`, `Cargo.toml`, `go.mod`
- `LICENSE` (existence + type)
- `docs/` folder contents (just file names + sizes)
- `examples/` or `samples/` or `cookbook/` folder
- `.github/workflows/*.yml` (just names + brief CI presence check)

If `repo` is a URL, also fetch via `gh`:
```bash
gh api repos/<owner>/<repo> --jq '{stars: .stargazers_count, forks: .forks_count, watchers: .subscribers_count, pushed_at, description, homepage, topics, default_branch}'
gh api repos/<owner>/<repo>/commits --jq '.[0].commit.author.date' | head -1
gh api repos/<owner>/<repo>/contributors --paginate --jq '[.[] | .login] | length'
```

Catch and continue if any GitHub call fails.

---

## Step 3: Score 10 dimensions

For each of the 10 dimensions in `references/scoring-rubric.md`, output `{score: 0–10, evidence: [...]}` where `evidence` is a list of 1–3 short strings citing what you found.

Example:
```json
"visual_proof": {
  "score": 4,
  "evidence": [
    "Found 1 screenshot at line 89 (below the fold)",
    "No animated demo / gif",
    "No video"
  ]
}
```

Sum scores → total (0–100) → grade (A/B/C/D/F per rubric).

Save to `dx-roast/score.json` with this exact shape:

```json
{
  "repo": "<owner/repo or local path>",
  "scanned_at": "<ISO 8601 timestamp>",
  "dimensions": {
    "time_to_first_success": { "score": 7, "evidence": ["..."] },
    "what_is_this_clarity": { "score": 5, "evidence": ["..."] },
    "visual_proof": { "score": 4, "evidence": ["..."] },
    "install_simplicity": { "score": 9, "evidence": ["..."] },
    "runnable_quick_start": { "score": 8, "evidence": ["..."] },
    "documentation_depth": { "score": 6, "evidence": ["..."] },
    "examples": { "score": 5, "evidence": ["..."] },
    "community_signals": { "score": 3, "evidence": ["..."] },
    "trust_signals": { "score": 7, "evidence": ["..."] },
    "marketing_signals": { "score": 4, "evidence": ["..."] }
  },
  "total": 58,
  "grade": "D",
  "tone": "honest"
}
```

---

## Step 4: Write the roast

Read `references/roast-voice-guide.md`. Apply the requested tone. Write 250–500 words to `dx-roast/roast.md`.

**Required structure:**

```markdown
# DX Roast: <repo name>

**Grade: <letter> (<total>/100)** · Tone: <tone>

<Paragraph 1: the verdict. What works + the big gap.>

<Paragraph 2: cite 2 specific findings with file references.>

<Paragraph 3: cite 2 more findings, tie to dimension scores.>

<Paragraph 4 (optional): a final twist or comparison to a known good repo.>

<Closing paragraph: point to `action-plan.md` for the path forward.>
```

Every roast must reference at least **3 specific findings** from `score.json` evidence arrays.

---

## Step 5: Generate action plan

Compute `priority = impact / effort_minutes` for each candidate fix. Take top 5–10. Sort desc by priority.

For each fix, write to `dx-roast/action-plan.md`:

```markdown
### N. <Fix in imperative voice, one line>

**Why:** <One-sentence justification. Reference which dimension it improves.>

**Impact:** +<X> points · **Effort:** <5min / 30min / 2h / half-day>

**How:**

1. <Concrete step 1>
2. <Concrete step 2>
3. <Concrete step 3>

<Optional code/markdown snippet showing exact change>
```

Open `action-plan.md` with:

```markdown
# Action Plan — <repo name>

Current grade: <letter> (<total>/100)
Top fixes ranked by impact × effort. Do these in order.

---
```

---

## Step 6: Generate ideal README

Read `references/readme-template.md`. Fill the template per "Filling rules" section. Write to `dx-roast/ideal-readme.md`.

Use placeholders `<homepage_url>` etc. for missing values. Length cap: 100 lines.

---

## Step 7: Terminal summary

Print this exact format to the user:

```
DX Roast complete — Grade: <letter> (<total>/100)

Top 3 fixes (impact-ranked):
  1. <fix 1>                                +<X> pts  · <effort>
  2. <fix 2>                                +<X> pts  · <effort>
  3. <fix 3>                                +<X> pts  · <effort>

Files:
  → dx-roast/roast.md          (shareable verdict)
  → dx-roast/action-plan.md    (prioritized fixes)
  → dx-roast/ideal-readme.md   (target state)
  → dx-roast/score.json        (raw scores)
```

If `compare_to` was provided, add a comparison line:

```
Benchmark: <other repo> scores <X>/100 (grade <Y>) — gap of <delta> points.
```

---

## Self-QA (every run, before printing the terminal summary)

- [ ] All 10 dimensions in `score.json` have score + evidence
- [ ] Total equals sum of dimensions
- [ ] Grade letter matches the total per rubric thresholds
- [ ] Roast references at least 3 evidence items from score.json
- [ ] Roast does not name any maintainer / contributor
- [ ] Action plan has 5–10 items, sorted desc by priority
- [ ] Ideal README is < 100 lines
- [ ] Ideal README uses `<placeholder>` for any URL not found in scan
- [ ] All 4 files exist in output_dir
- [ ] No `<TBD>` / `<TODO>` placeholders in roast.md or action-plan.md

If any check fails, fix and re-run that step.

---

## Error handling

These four failure modes get explicit handling — never let the skill silently produce a partial output without surfacing the cause.

| Case | Behavior |
|---|---|
| `repo` doesn't exist OR can't be cloned OR can't be read | Exit immediately with the message `Repo not found or inaccessible: <repo>`. Do not write any output files. |
| `README.md` is missing | Run anyway. Score `what_is_this_clarity`, `visual_proof`, `runnable_quick_start`, and `marketing_signals` near 0. Use the absence as the opening of the roast ("No README is its own statement"). |
| Repo is private + no GitHub auth available | Try a local clone (`git clone <url>`); if it fails, exit with `Repo is private and no authentication is available`. Suggest the user set `GITHUB_TOKEN` or pass a local path. |
| `compare_to` URL fails (network, 404, private, etc.) | Continue without the benchmark. Add a single line to the roast: `Note: requested benchmark against <compare_to> could not be fetched.` Omit the `Benchmark:` line from the terminal summary. |

Any GitHub API error (rate limit, transient 5xx) during Step 2 metadata fetch is caught and logged in `score.json` under `trust_signals.evidence` as `"github metadata unavailable"`. The rest of the run proceeds.

---

## Examples

**Good invocation:**

> "Roast my repo at https://github.com/myorg/mytool — tone: brutal."

→ Skill clones, scans, scores, writes 4 files to `dx-roast/`, prints summary. Total runtime <60s for a typical repo.

**Good comparison:**

> "DX audit on the current dir. Benchmark against https://github.com/vercel/next.js."

→ Scans both, scores current, includes benchmark line in roast and summary.

---

## What this skill does NOT do

- Does not modify the target repo (read-only scan)
- Does not run security audits or dependency scans
- Does not generate marketing copy (action items are concrete, not "rewrite for tone")
- Does not produce images or assets (just placeholders)
- Does not post to social media (writes shareable text only)
