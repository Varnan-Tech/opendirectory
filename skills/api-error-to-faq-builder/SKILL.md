---
name: api-error-to-faq-builder
description: Pulls open GitHub issues from any public repo, clusters them by recurring API errors, and generates a structured Markdown troubleshooting FAQ.
author: ajaycodesitbetter
version: 1.0.0
---

# API Error to FAQ Builder

Fetch open GitHub issues, extract API error patterns, and render a Markdown support FAQ with traceable issue references.

---

## When to Trigger This Skill

Use this skill when the user asks to:
- Build a FAQ from GitHub issues for a repo.
- Summarize recurring API errors.
- Turn issue noise into a troubleshooting document.

---

## Step 1: Confirm Input

Ask the user for the target repository as `owner/repo` or a full GitHub URL. Use smart defaults for the rest:
- Max issues: `100` (`--limit`)
- Labels: `bug,question` (`--labels`)
- Include comments: `false` (`--comments`)
- Output: `FAQ.md` (`--output`)

Only ask about overrides if the user explicitly requests custom behavior.

---

## Step 2: Fetch Issues & Generate FAQ

Run the orchestrator script to handle fetching, clustering, and Markdown generation in one command.

```bash
python scripts/run.py OWNER/REPO
```

For custom requests, append the overrides exactly as shown below:
```bash
python scripts/run.py OWNER/REPO \
  [--limit 100] \
  [--labels bug,question] \
  [--comments] \
  [--output FAQ.md]
```

If the pipeline fails, suggest setting a `GITHUB_TOKEN` in `.env` for rate limits or checking the repository name.

---

## Step 3: Present Results

After the script finishes, summarize the findings to the user.
Report the number of issues scanned, the output path, and the top 2-3 FAQ entries generated.

Offer to open `FAQ.md` for review or run it on a different repository.

---

## Step 4: Self-QA

Before presenting results, quickly verify the output quality:
- Output is a clean troubleshooting document, not a raw issue dump.
- FAQ entries include generated links to real GitHub issues.

---

## Dependencies

```bash
pip install requests python-dotenv "thefuzz[speedup]"
```

## References
- `references/faq_template.md` — canonical FAQ entry format
- `references/clustering-rules.md` — heuristics explained
- `references/sample-output.md` — example FAQ output
