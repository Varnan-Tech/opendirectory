---
name: docs-from-code
description: Generates and updates README.md and API reference docs by reading your codebase's functions, routes, types, schemas, and architecture. Uses graphify to build a knowledge graph first, then writes accurate docs from it. Use when asked to write docs, generate a README, document an API, update stale docs, create an API reference from code, add an architecture section, or document a project in any language. Trigger when a user says their docs are missing, outdated, or wants to document their codebase without writing it manually.
author: OpenDirectory
version: 1.0.0
---

# docs-from-code

You are a technical writer. Your job is to generate accurate, developer-friendly docs by first building a knowledge graph of the codebase with graphify, then using that graph to write docs grounded in what actually exists.

**DO NOT invent code.** If you cannot find a clear description for something, write `[Description needed]`. Accurate but sparse docs are better than confident but wrong docs.

**Before starting:** Confirm you are inside a codebase directory. If the user pointed you at a remote repo, clone it first. If neither, ask: "Can you point me to the project directory or repository URL?"

---

## Workflow

### Step 1: Install graphify and Build the Knowledge Graph

graphify uses tree-sitter AST (20 languages, no LLM) for code structure and Claude subagents for semantic understanding of docs and comments.

```bash
pip install graphifyy
graphify . --no-viz
```

`--no-viz` skips HTML output. You only need `GRAPH_REPORT.md` and `graph.json`.

This produces `graphify-out/` in the project root:
- `GRAPH_REPORT.md` — god nodes, community clusters, surprising connections, suggested questions
- `graph.json` — full queryable knowledge graph (persistent, SHA256-cached)

**QA:** Did `graphify-out/GRAPH_REPORT.md` get created? How many nodes and edges? If graphify fails, go to Step 1B.

#### Step 1B: Fallback (if graphify unavailable)

```bash
# TypeScript/JS projects:
cd <skill-directory>/scripts && npm install
npx ts-node extract_ts.ts <project-root> <project-root>/.docs-extract.json

# Python projects:
python3 <skill-directory>/scripts/extract_py.py <project-root> <project-root>/.docs-extract.json
```

Read `references/extraction-guide.md` for framework-specific notes on the fallback output.

---

### Step 2: Read the Graph Report

Read `graphify-out/GRAPH_REPORT.md` in full. This gives you:
- **God nodes** — highest-degree concepts (what everything connects through). Use these for the Architecture section.
- **Community clusters** — logical groupings of related code. Use these for module documentation.
- **Surprising connections** — non-obvious cross-file relationships. Note these in Architecture.
- **Suggested questions** — graphify's assessment of what is worth documenting.

Then run targeted queries for specific doc sections:

```bash
# API routes
graphify query "show all API routes and endpoints" --graph graphify-out/graph.json

# Data models
graphify query "what are the main data models and types?" --graph graphify-out/graph.json

# Auth flow
graphify query "how does authentication work?" --graph graphify-out/graph.json

# Entry points
graphify query "what is the entry point and how is the app initialised?" --graph graphify-out/graph.json
```

Each query returns a focused subgraph. Relationships are tagged `EXTRACTED` (found in source) or `INFERRED` (with confidence score). Trust `EXTRACTED` fully. Use `INFERRED` but flag uncertainty.

**QA:** Cross-check 2-3 routes from the query against actual source files before writing docs.

---

### Step 3: Read Existing Documentation

Before writing anything new, check what already exists:

1. Read `README.md` if present. Note which sections exist and which are stale or missing.
2. Read `docs/API.md`, `docs/api.md`, or `API.md` if present.
3. Read `CHANGELOG.md` for context on recent changes worth noting.

Decide what to generate:
- **No README** — generate a full README from Template 1 in `references/output-template.md`
- **README exists, API section stale** — update only that section (Template 3)
- **README exists, fully outdated** — ask: "Your README exists but appears outdated. Rewrite fully or update specific sections?"

**QA:** List exactly what you will write or update before starting.

---

### Step 4: Generate Documentation

Read `references/output-template.md` for the exact templates to use.

**README — Project Description:**
From `package.json` or `pyproject.toml` description + god nodes summary from `GRAPH_REPORT.md`.

**README — Architecture Section:**
Use god nodes and community clusters to write a plain-English architecture overview. Example:
> "The system is organised around 3 core modules: `AuthService` (god node, connects to 14 other components), `DatabaseAdapter` (bridges all data access), and `EventBus` (central to async flows). The auth and request-handling modules are tightly coupled; the analytics module is independent."

**README — Installation and Quick Start:**
From the entry point file + `scripts` in `package.json` or `Makefile`.

**API Reference (`docs/API.md`):**
From the `graphify query "show all API routes"` output. One section per resource, grouped by path prefix. For each route: method, path, description (from docstring or rationale node), request/response shape (from linked type nodes), curl example.

Flag anything without a docstring as `[Description needed]`. Do not invent behaviour.

**QA:** Check 3 random routes in the generated `docs/API.md` against the actual source file. Do the paths and descriptions match?

---

### Step 5: Write Files, Clean Up, and Open PR

1. Write `README.md` to the project root (full file or updated sections only).
2. Write `docs/API.md` if routes were found. Create `docs/` if needed.
3. Clean up: `rm -rf graphify-out/ .docs-extract.json`

Ask the user: "Docs written. Should I open a GitHub PR with these changes?"

If yes:
```bash
git checkout -b docs/auto-generated-$(date +%Y%m%d)
git add README.md docs/
git commit -m "docs: auto-generate README and API reference from codebase"
gh pr create \
  --title "docs: auto-generated README and API reference" \
  --body "Generated by docs-from-code skill using graphify knowledge graph. All routes and types verified against source."
```

**QA:** Did the files write? Do paths exist? Did the PR open cleanly?

---

## What Good Output Looks Like

- Architecture section explains god nodes and module relationships in plain English
- Every route in `docs/API.md` matches a real path from the graphify query output
- README Quick Start has a runnable snippet from tests or the entry point
- INFERRED relationships that influenced descriptions are noted as "likely" or "appears to"
- Missing descriptions are flagged `[Description needed]`, not fabricated

## What Bad Output Looks Like

- Routes or functions that do not appear in the graphify query results
- Architecture section that is generic ("the app has controllers, services, and models")
- Examples using wrong function names or parameter types
- INFERRED edges described as definite facts without a confidence qualifier


