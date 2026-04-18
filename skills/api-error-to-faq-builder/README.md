# api-error-to-faq-builder

<!-- TODO: Insert custom dark technical cover banner here -->

> Pulls open GitHub issues from a public repository, clusters them by recurring API errors, and generates a clean troubleshooting FAQ.

[![opendirectory](https://img.shields.io/badge/opendirectory-skill-blue)](https://opendirectory.dev)
[![version](https://img.shields.io/badge/version-1.0.0-green)](https://github.com/Varnan-Tech/opendirectory)
[![license](https://img.shields.io/badge/license-MIT-orange)](https://opensource.org/licenses/MIT)

---

## Overview

Convert fragmented issue noise into a reusable support artifact. This skill pulls issues tagged `bug` or `question`, extracts contextual signals (HTTP status codes, endpoint paths, error strings), and deterministically groups them into meaningful API troubleshooting questions.

* No web UI, no vector databases, no massive dependencies.
* Returns a robust Markdown artifact suitable for public docs.
* Uses safe fuzzy matching and clustering confidence metrics.

## Prerequisites
- Python 3.10+
- Dependencies: `requests`, `python-dotenv`, `thefuzz`

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

# Navigate to the skill and install python dependencies
cd skills/api-error-to-faq-builder
pip install requests python-dotenv "thefuzz[speedup]"
```

## Usage
Run the orchestrated CLI against any public repository.
*(Note: Set `GITHUB_TOKEN` in `.env` to prevent rate limiting.)*

```bash
# Standard run (fetches 100 open bugs/questions)
python scripts/run.py openai/openai-python

# Scan broader issue types and include comment scanning
python scripts/run.py supabase/supabase --labels '' --comments --limit 200

# Specify custom output destination
python scripts/run.py vercel/next.js --output docs/SUPPORT.md
```

## Sample Output
Preview how clusters are generated in [references/sample-output.md](references/sample-output.md).

## Limitations (v1)
- Evaluates public GitHub repositories only.
- Relies primarily on REST API-centric hints (HTTP status codes, URIs).
- Processing is done sequentially on the local machine; massive issue counts combined with heavy comment parsing may be slow.
- Does not cross-post or deploy replies back to live GitHub issues automatically.
