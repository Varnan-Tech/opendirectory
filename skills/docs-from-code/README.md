# docs-from-code

![docs-from-code](https://github.com/user-attachments/assets/493c7c61-9aa9-48e9-a71b-7c77c8c6a949)

Automatically generate and maintain README.md, API reference docs, and an Architecture section by reading your codebase. Uses [graphify](https://github.com/safishamsi/graphify) to build a knowledge graph first, then uses AI to write clean documentation grounded in what actually exists.

## Install

```bash
npx "@opendirectory.dev/skills" install docs-from-code --target claude
```

## What It Generates

| Output | When |
|--------|------|
| `README.md` (full) | Project has no README |
| `README.md` (sections) | README exists but API or architecture sections are stale |
| `docs/API.md` | Project has HTTP routes |
| Architecture section | Always, from graphify's god nodes and communities |
| GitHub PR | When you ask it to open one |

## Why graphify?

The skill uses graphify as its extraction engine:
- 20 languages via tree-sitter AST: Python, TypeScript, Go, Rust, Java, and 15 more
- Architecture insight: god nodes and community clusters show what everything connects through
- 71.5x fewer tokens than reading raw files, efficient on large codebases
- SHA256 cache: re-runs only process changed files
- Honest tagging: `EXTRACTED` (found in source) vs `INFERRED` (reasonable inference with confidence score)
- Extracts rationale from `# NOTE:`, `# WHY:`, `# HACK:` comments and docstrings

The bundled `scripts/` (TypeScript and Python AST extractors) serve as a fallback if graphify is unavailable.

## Supported Languages (via graphify)

Python, TypeScript, JavaScript, Go, Rust, Java, C, C++, Ruby, C#, Kotlin, Scala, PHP, Swift, Lua, Zig, PowerShell, Elixir, Objective-C, Julia

## Requirements

- Python 3.10+ (for graphify)
- Node.js 18+ (for fallback TypeScript extractor)
- `gh` CLI (optional, for opening PRs automatically)
- `GITHUB_TOKEN` env var (optional, for PRs)

## Setup

### 1. Install graphify

```bash
pip install graphifyy
```

No API keys needed for extraction. graphify uses your agent's existing model access.

### 2. Configure (Optional)

```bash
cp .env.example .env
# Add GITHUB_TOKEN if you want auto-PR support
```

## How to Use

Be inside your project and ask:

```
"Generate a README for this project"
"My API docs are out of date, update them from the code"
"Create docs/API.md from my FastAPI routes"
"Add an architecture section to our README"
"Document this TypeScript library"
```

The agent will:
1. Run `graphify . --no-viz` to build a knowledge graph of your codebase
2. Read `GRAPH_REPORT.md` for god nodes, communities, and architecture insights
3. Query the graph for routes, types, and data models
4. Read existing docs to understand what needs updating
5. Generate accurate docs grounded in the graph
6. Write files and optionally open a GitHub PR

## Project Structure

```
docs-from-code/
├── SKILL.md                         # Agent instructions
├── README.md                        # This file
├── .env.example                     # Environment variables template
├── scripts/
│   ├── package.json                 # Script dependencies (ts-morph)
│   ├── extract_ts.ts                # TypeScript/JS AST extractor
│   └── extract_py.py                # Python AST extractor
├── references/
│   ├── extraction-guide.md          # Per-framework extraction notes
│   └── output-template.md          # README and API.md templates
└── evals/
    └── evals.json                   # Test prompts
```

## License

MIT

## Installation in Claude Desktop App

### Video Tutorial
Watch this quick video to see how it's done:

https://github.com/user-attachments/assets/ee98a1b5-ebc4-452f-bbfb-c434f2935067

### Step 1: Download the skill from GitHub
1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

### Step 2: Install the Skill in Claude
1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** (plus) icon button to create a new skill.
4. Choose the option to **Upload a skill**, and drag and drop the `.zip` file (or you can extract it and drop the folder, both work).

> **Note:** For some skills (like `position-me`), the `SKILL.md` file might be located inside a subfolder. Always make sure you are uploading the specific folder that contains the `SKILL.md` file!
