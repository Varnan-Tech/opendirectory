---
name: api-error-to-faq-builder
description: Pulls open GitHub issues tagged bug or question from any public repo, clusters them by recurring error strings, HTTP status codes, and API endpoints, and generates a structured Markdown troubleshooting FAQ. Use when asked to build a support FAQ from GitHub issues, summarize recurring API errors, or convert issue noise into documentation.
author: ajaycodesitbetter
version: 1.0.0
---

# API Error to FAQ Builder

Fetch open GitHub issues, extract recurring API error patterns, cluster by
signal strength, and render a clean Markdown troubleshooting FAQ with
traceable issue references.

---

## When to Trigger This Skill

Use this skill when the user says any of:
- "Build a FAQ from GitHub issues in owner/repo"
- "What errors are users hitting in this repo?"
- "Generate a troubleshooting doc from open issues"
- "Cluster recurring API errors from GitHub"
- "Turn GitHub issues into a support FAQ"

---

## Step 1: Confirm Input

Ask the user for one thing only:
- **Repository** — `owner/repo` or full GitHub URL (required)

All other settings use smart defaults:
- Labels: `bug,question`
- Max issues: `100`
- Include comments: `false`
- Output path: `FAQ.md`

Only ask about overrides if the user explicitly requests custom behavior
(e.g. "scan 200 issues" or "include all labels").

If no repo is given, ask: "Which GitHub repo should I build the FAQ from?
Share it as owner/repo or a full GitHub URL."

---

## Step 2: Fetch Issues

Run the full pipeline in one command:

```bash
python scripts/run.py OWNER/REPO
```

Optional overrides:

```bash
python scripts/run.py OWNER/REPO \
  [--limit 100] \
  [--labels bug,question] \
  [--comments] \
  [--output FAQ.md]
```

`run.py` orchestrates the full pipeline internally:
1. Fetches issues via GitHub API (`fetch_issues.py`)
2. Normalizes text, extracts signals, clusters by pattern (`build_faq.py` internals)
3. Renders and writes `FAQ.md` (`build_faq.py`)

Progress is printed to stderr. `FAQ.md` is the only output artifact.

If the pipeline fails:
- `401` → Ask user to set `GITHUB_TOKEN` in `.env`
- `404` → Repo not found — confirm the `owner/repo` value
- `403` → Rate limited — add `GITHUB_TOKEN` and retry
- No qualifying issues → Tell user: "No open issues found with labels
  `bug,question`. Try running with `--labels ''` to scan all open issues."

---

## Step 3: Present Results

After generation, report:
- Issues scanned and clusters found
- Output path of `FAQ.md`
- Top 3 FAQ entries by recurrence (titles only)

Then offer:
1. "Open FAQ.md for review"
2. "Run on a different repo to compare"
3. "Drill into a specific cluster"

---

## Step 4: Self-QA Before Output

Before presenting results, check:
- [ ] Each FAQ entry links back to real issue numbers
- [ ] Only clusters with 2+ issues appear in the FAQ (singletons excluded)
- [ ] Suggested fixes use hedged language: "likely", "suggested", "check whether"
- [ ] Output reads like a troubleshooting doc, not a raw issue list
- [ ] Repo name and generation date appear in the FAQ header

---

## Dependencies

```bash
pip install requests python-dotenv "thefuzz[speedup]"
```

Optional: set `GITHUB_TOKEN` in `.env` to avoid rate limits on large repos.

## References

- `references/faq_template.md` — canonical FAQ entry format
- `references/clustering-rules.md` — heuristics explained
- `references/sample-output.md` — example FAQ.md output (TODO: pick real repo)
