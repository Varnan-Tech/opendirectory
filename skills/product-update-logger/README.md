# product-update-logger

Tell the skill what your product shipped. It writes a polished, living `docs/changelog.md` entry and hands you a ready-to-use content package: tweet thread, LinkedIn post, email snippet, and one-liner.

Run it after every deploy. Over quarters, `docs/changelog.md` becomes a complete, shareable product history.

## Install

```bash
npx "@opendirectory.dev/skills" install product-update-logger --target claude
```

### Video Tutorial
Watch this quick video to see how it's done:

https://github.com/user-attachments/assets/ee98a1b5-ebc4-452f-bbfb-c434f2935067

### Step 1: Download the skill from GitHub
1. Click the **Code** button on this repo's GitHub page.
2. Select **Download ZIP** to download the repository.
3. Extract the ZIP file on your computer.

### Step 2: Install the Skill in Claude
1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** (plus) icon button to create a new skill.
4. Choose the option to **Upload a skill**, and drag and drop the `.zip` file (or you can extract it and drop the folder, both work).

> **Note:** For some skills (like `position-me`), the `SKILL.md` file might be located inside a subfolder. Always make sure you are uploading the specific folder that contains the `SKILL.md` file!

## What It Does

- Accepts: free text items, git commits (auto-read), GitHub PRs -- any combination
- Filters noise: merge commits, version bumps, CI/CD, typos excluded automatically
- Transforms: technical commit language -> user-facing benefit language
- Categorizes: New / Improved / Fixed / Under the hood
- Generates a content package: one-liner, tweet thread, LinkedIn post, email snippet
- Appends a new dated entry to `docs/changelog.md` (living log, newest entry first)
- Saves the content package to `docs/product-updates/[date]-content.md`

## Requirements

| Requirement | Purpose | How to Set Up |
|---|---|---|
| GITHUB_TOKEN | Optional -- enables GitHub PR fetching for richer context | github.com/settings/tokens (no scopes needed) |

No other API keys required. Free text + git auto-read work with no configuration.

## Setup

```bash
cp .env.example .env
# Add GITHUB_TOKEN if you want to pull from GitHub PRs
```

## How to Use

```
"We shipped dark mode and fixed the export bug this week."
"Log my product updates. I'm in a git repo."
"We launched 3 things: dark mode, faster search, fixed mobile login."
"Log updates from last 14 days. Repo: acme/dashboard"
"We shipped the onboarding redesign. Version: v2.1.0"
```

Include competitor names for richer channel discovery. Include ICP role + pain for accurate signal-tracing.

## What Gets Generated

### docs/changelog.md (living log)

```markdown
# Changelog

## Week of April 23, 2026

### New
- **Dark mode** -- Toggle in Settings > Appearance. Works across all views.

### Improved
- **Search** -- Results now load in under half a second.

### Fixed
- **CSV export** -- Exports no longer drop the last row.

---

## Week of April 14, 2026
...
```

### docs/product-updates/[date]-content.md (content package)

```
## One-liner
Dark mode, faster search, and a fix for the export bug.

## Tweet Thread
[1/4] We shipped 3 things this week.
[2/4] Dark mode is live. Toggle it in Settings > Appearance.
...

## LinkedIn Post
We shipped 3 updates this week.
...

## Email Snippet
Subject: What shipped this week: dark mode + faster search
...
```

## Input Sources

The skill pulls from all three sources automatically:

| Source | When used | How to trigger |
|---|---|---|
| Free text | Always first | Just describe what shipped in your message |
| Git commits | Auto-read when in a git repo | Run the skill from your project directory |
| GitHub PRs | When GITHUB_TOKEN + repo provided | Mention "repo: owner/repo" in your message |

All three can be combined. Overlapping items are deduplicated.

## Changelog Entry Format

Each entry follows a consistent structure:

```
## [Version label]

### New
- **Feature** -- Benefit sentence.

### Improved
- **Feature** -- Benefit sentence.

### Fixed
- **Feature** -- What was broken, now fixed.

### Under the hood
- **Component** -- Developer-relevant change only.
```

Version labels default to `Week of [Month Day, Year]`. Detected semver format is preserved and incremented automatically.

## Content Rules

- **Tweets**: Under 280 chars each, no hashtags, no em dashes, active voice
- **LinkedIn**: No markdown formatting, no hashtags, founder voice ("We shipped" not "We are excited to announce")
- **Email**: 50-100 word body, subject line formula, casual and direct
- **One-liner**: Max 20 words, covers top 1-2 items

## Standalone Script

Run data collection without Claude. Useful for raw item discovery before analysis.

```bash
# Git auto-read
python3 scripts/gather.py --since 7 --output /tmp/pul-raw.json

# Free text items
python3 scripts/gather.py --items "Add dark mode|Fix CSV bug" --output /tmp/pul-raw.json

# With GitHub PRs
GITHUB_TOKEN=your_token python3 scripts/gather.py --repo owner/repo --since 14

# Print to stdout
python3 scripts/gather.py --since 7 --stdout | jq '.items'
```

## Project Structure

```
product-update-logger/
├── SKILL.md
├── README.md
├── .env.example
├── scripts/
│   └── gather.py               git + GitHub + free text collector
├── evals/
│   └── evals.json              5 test cases
└── references/
    ├── changelog-format.md     entry structure, category rules, transformation examples
    ├── content-rules.md        tweet/LinkedIn/email writing rules + banned words
    └── noise-filter.md         git commit patterns to skip
```

## Cost Per Run

- Git, free text: free, no auth
- GitHub PRs: free with optional token
- AI analysis: uses the model running the skill
- Total: free

## License

MIT
