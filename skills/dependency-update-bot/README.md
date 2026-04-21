# dependency-update-bot

<img width="1280" height="640" alt="dependency-update-bot" src="https://github.com/user-attachments/assets/08939280-bba2-4ac9-a349-2ca8c25ca328" />


Weekly scan for outdated npm or pip packages. Fetches changelogs for each. Summarizes breaking changes with Gemini. Opens one PR per risk group.

## Install

```bash
npx "@opendirectory.dev/skills" install dependency-update-bot --target claude
```

## What It Does

- Runs `npm outdated --json` or `pip list --outdated` to find outdated packages
- Classifies each update as patch (low risk), minor (medium risk), or major (high risk) using semver
- Fetches changelogs from GitHub Releases, CHANGELOG.md, or npm/PyPI registry as fallback
- Uses Gemini to summarize what changed between old and new versions, flagging breaking changes
- Creates a branch per risk group, updates the package file, and opens a PR with the changelog summary
- Opens one PR per major update (since each major bump needs individual review)

## Requirements

| Requirement | Purpose | How to Set Up |
|------------|---------|--------------|
| Gemini API key | Changelog summarization | aistudio.google.com, Get API key |
| GitHub CLI authenticated | PR creation | `gh auth login` |
| GitHub token (optional) | Higher rate limit for changelog fetching | github.com/settings/tokens, read-only scope |

## Setup

```bash
cp .env.example .env
```

Fill in:
- `GEMINI_API_KEY` (required)
- `GITHUB_TOKEN` (optional, increases GitHub API rate limit from 60 to 5,000 requests/hour)

## How to Use

Scan npm dependencies:
```
"Check for outdated packages"
"Update my dependencies and open PRs"
"Run the dependency update bot"
```

Scan pip dependencies:
```
"Check my Python packages for updates"
"Scan requirements.txt for outdated dependencies"
```

Specific risk level only:
```
"Only open PRs for patch updates today"
"Show me which packages have major version updates"
```

## PR Structure

Each PR includes:
- Risk level label (patch / minor / major)
- For each package: version bump, changelog summary (3-5 bullets), breaking changes flagged with BREAKING prefix
- How to verify section

**One PR per risk group** for patch and minor updates. **One PR per package** for major updates (since each breaking change needs individual review).

## Risk Classification

| Level | Version Change | Example | Action |
|-------|---------------|---------|--------|
| Patch | Z in X.Y.Z | 4.17.19 to 4.17.21 | Safe to merge after CI passes |
| Minor | Y in X.Y.Z | 4.17.x to 4.18.x | Review changelog before merging |
| Major | X in X.Y.Z | 4.x.x to 5.x.x | Read changelog carefully, test thoroughly |

If a patch or minor update's changelog contains BREAKING CHANGE keywords, the bot escalates it to major automatically.

## Changelog Sources

The bot tries these sources in order for each package:

1. GitHub Releases API (best)
2. Raw CHANGELOG.md from the repo
3. npm registry README (fallback)
4. PyPI project description (last resort)

If no changelog is found, the PR still includes the version bump with a note to review manually.

## Project Structure

```
dependency-update-bot/
├── SKILL.md
├── README.md
├── .env.example
├── evals/
│   └── evals.json
└── references/
    └── changelog-patterns.md
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
