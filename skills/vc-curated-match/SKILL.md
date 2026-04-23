name: vc-curated-match
description: Accepts a product description and URL to algorithmically identify relevant Venture Capital investors targeting exactly that stage, industry, and niche based on a curated static dataset.
author: OpenDirectory
version: 1.0.0
---

# VC Curated Match Skill

Identify targeted VC funds based on a product's description and URL.

---

## When to Trigger This Skill

Use this skill when the user asks to:
- Find investors for their startup or open-source project.
- Get a list of relevant VC funds by stage, industry, or space.
- Match their product built with specific technologies to investor theses.

---

## Step 1: Confirm Input

Ask the user for the product description and the URL. 
Optional parameters:
- Stage: `Pre-Seed`, `Seed`, `Series A` (`--stage`)
- Output: e.g., `vc-matches.md` (`--output`)

---

## Step 2: Fetch Matches & Generate Report

Run the orchestrator script to handle context fetching, VC matching, and Markdown generation in one command.

```bash
python scripts/run.py --description "A fast rust-based web framework" --url "https://example.com"
```

For custom requests, append overrides:
```bash
python scripts/run.py \
  --description "..." \
  --url "..." \
  [--stage Seed] \
  [--output matched-investors.md]
```

---

## Step 3: Present Results

Summarize the closest matches returned. Mention high-confidence matches explicitly. Provide the output path.

---

## Dependencies

Standard Python 3.10+ library (no external packages required).
