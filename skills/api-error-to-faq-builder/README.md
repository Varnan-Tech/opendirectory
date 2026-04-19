# api-error-to-faq-builder

<!-- TODO: Insert custom dark technical cover banner here -->

> Given a public GitHub repo, this skill reads open issues, finds recurring API errors, and writes a troubleshooting FAQ in Markdown.

[![opendirectory](https://img.shields.io/badge/opendirectory-skill-blue)](https://opendirectory.dev)
[![version](https://img.shields.io/badge/version-1.0.0-green)](https://github.com/Varnan-Tech/opendirectory)
[![license](https://img.shields.io/badge/license-MIT-orange)](https://opensource.org/licenses/MIT)

---

## Overview

Convert fragmented issue noise into a reusable support document. This skill pulls open issues, extracts context like HTTP status codes and endpoint paths, and groups them into API troubleshooting questions.

* No web UI, vector databases, or heavy ML models.
* Returns a clean Markdown file ready for public docs.
* Uses fuzzy matching and clustering confidence metrics to filter out noise.

## Prerequisites
- Python 3.10+
- `requests`, `python-dotenv`, `thefuzz`

## Installation

### Option A: Install as an OpenDirectory Skill (Agent Users)
Install the skill directly into supported agent targets (Anti-Gravity, Claude Code, OpenCode, Codex, Gemini CLI, OpenClaw, Hermes):
```bash
npx "@opendirectory.dev/skills" install api-error-to-faq-builder --target anti-gravity
```

### Option B: Local Repository Development
Clone the OpenDirectory repo and install dependencies manually to edit and run the scripts locally:
```bash
# From the repo root
pnpm install
pnpm build

# Navigate to the skill and install Python dependencies
cd skills/api-error-to-faq-builder
pip install requests python-dotenv "thefuzz[speedup]"
```

## Usage
Run the CLI against any public GitHub repository. Set `GITHUB_TOKEN` in `.env` to avoid rate limits.

### Examples

**Standard Run:**
```bash
python scripts/run.py vercel/next.js --limit 100
```
*Output:* Generates `FAQ.md` with entries like "Why do requests frequently fail with a 404 status code?" and "How can I resolve recurring timeout errors?"

**Broad Scan with Comments:**
```bash
python scripts/run.py openai/openai-python --labels "" --comments --limit 200
```
*Output:* Scans 200 open issues including their comment threads to find deeper nested auth and rate-limiting configurations, generating `FAQ.md`.

**Custom Output File:**
```bash
python scripts/run.py supabase/supabase --output docs/SUPPORT.md
```

## Sample Output
Preview how clusters are generated in [references/sample-output.md](references/sample-output.md).

## Limitations

- **Best for API-focused repos**: This skill is designed for repositories
  where issues predominantly contain HTTP status codes, endpoint paths,
  and error strings (e.g., `openai/openai-python`, `stripe/stripe-python`).
- **Noisy on general product trackers**: Running on repos like
  `openclaw/openclaw` (a general product bug tracker) will produce lower
  accuracy because issues mix infrastructure bugs, logic bugs, network
  issues, and feature requests in the same tracker.
- **Dynamic pricing pages**: Some issues may not contain error messages
  at all — the skill works best when issues have structured error output
  in their bodies.
- **Confidence scores**: Clusters with confidence < 0.7 are flagged as
  low confidence. Review them manually before adding to production docs.
