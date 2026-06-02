# claude-md-generator

<img width="1280" height="640" alt="claude-md-generator" src="https://github.com/user-attachments/assets/0e295271-2216-47f7-828f-845c98ef0298" />


Reads your codebase and writes a CLAUDE.md that gives Claude Code the context it needs: build commands, code conventions, architecture notes, and gotchas. Stays under 200 lines.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install claude-md-generator --target claude
```

### Option B: Claude Desktop App

<video src="https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c" controls width="100%"></video>

**Step 1: Download the skill from GitHub**

1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

**Step 2: Install in Claude**

1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** button to create a new skill.
4. Choose **Upload a skill**, then drag and drop the `.zip` file or extracted folder.

> **Note:** For some skills, the `SKILL.md` file might be located inside a subfolder. Always upload the specific folder that contains the `SKILL.md` file.

### Option C: Claude Code Native

Run these commands inside Claude Code:

```bash
/plugin marketplace add Varnan-Tech/opendirectory
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

### Option D: Manus AI

<video src="https://www.opendirectory.dev/ManusAI-one-click-installation-demo.webm" controls width="100%"></video>

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fclaude-md-generator&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Does

- Scans project files: package.json, tsconfig.json, linter configs, Makefile, directory structure
- Extracts all build, test, lint, and dev commands
- Identifies code style conventions that differ from defaults (path aliases, export patterns, naming)
- Maps non-obvious architecture decisions
- Finds gotchas: auto-generated files, required env var setup, test dependencies
- Generates CLAUDE.md using Gemini, then verifies it stays under 200 lines
- If CLAUDE.md already exists, improves it without discarding custom content

## Requirements

| Requirement | Purpose | How to Set Up |
|------------|---------|--------------|
| Gemini API key | CLAUDE.md generation from codebase analysis | aistudio.google.com, Get API key |

## Setup

```bash
cp .env.example .env
# Add GEMINI_API_KEY
```

## How to Use

From the project root you want to document:
```
"Generate a CLAUDE.md for this project"
"Create a CLAUDE.md"
"Write Claude configuration for this repo"
"Help Claude understand this codebase"
```

To update an existing CLAUDE.md:
```
"Update my CLAUDE.md: we added Vitest and changed the build system"
"Improve my existing CLAUDE.md"
```

## What Goes in CLAUDE.md

| Section | Include | Skip |
|---------|---------|------|
| Commands | Exact runnable commands, flags needed, env vars required | `npm install` and other obvious ones |
| Architecture | Non-obvious structure, auto-generated directories | "src contains source files" |
| Code Style | Path aliases, export conventions, non-default settings | Indent size (formatter handles it) |
| Testing | Required setup, how to run one test | "we use Jest" (visible from package.json) |
| Gotchas | Auto-generated files, env var order, known intentional issues | Things derivable from the code |

## Why Under 200 Lines

Long CLAUDE.md files get ignored. Claude loads the full file into context every session: a bloated CLAUDE.md with obvious content trains Claude to skim it. A tight 100-150 line CLAUDE.md with only non-obvious facts gets read and used.

The skill cuts aggressively: if a section says only things Claude can infer from the code, it removes it.

## Project Structure

```
claude-md-generator/
├── SKILL.md
├── README.md
├── .env.example
├── evals/
│   └── evals.json
└── references/
    └── section-guide.md
```

## License

MIT
