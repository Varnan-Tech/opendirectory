# hackernews-intel

<img width="1280" height="640" alt="hackernews-intel" src="https://github.com/user-attachments/assets/8d75cba9-7c2b-4693-8365-00779ed2b3d3" />


Monitor Hacker News for keywords. Get a Slack alert every time a new post matches your topics, without duplicates. Run it manually, on a cron schedule, or via GitHub Actions.

## Install

```bash
npx "@opendirectory.dev/skills" install hackernews-intel --target claude
```

## What It Does

- Fetches new posts from HN using the free Algolia search API (no API key needed)
- Checks each match against a local SQLite cache and never alerts on the same post twice
- Sends a Slack notification with title, URL, points, and comment count
- Supports dry-run mode to preview matches without sending alerts
- Configurable lookback window, minimum points threshold, and comment inclusion

## Requirements

| Requirement | Purpose | Where to Get It |
|------------|---------|-----------------|
| HN_KEYWORDS | Keywords to monitor | Set in .env, comma-separated list |
| SLACK_WEBHOOK | Slack alerts | https://api.slack.com/apps, Incoming Webhooks |
| Node.js 20+ | Running the script | https://nodejs.org |

No API key needed for Hacker News. The HN Algolia API is free and public.

## Setup

### 1. Install dependencies

```bash
cd hackernews-intel
npm install
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```bash
HN_KEYWORDS=claude code,LLM agents,deno runtime
SLACK_WEBHOOK=https://hooks.slack.com/services/your/webhook/url
HN_MIN_POINTS=0
```

### 3. Create a Slack webhook

1. Go to https://api.slack.com/apps and create or select your app
2. Enable "Incoming Webhooks" in the app settings
3. Add a webhook to your workspace and select the target channel
4. Copy the webhook URL (starts with `https://hooks.slack.com/services/`)
5. Set it as `SLACK_WEBHOOK` in `.env`

## How to Use

Preview the last 7 days without sending alerts:

```bash
npm run dry-run:week
# or
node scripts/monitor-hn.js --dry-run --days=7
```

Live run:

```bash
npm run monitor
# or
node scripts/monitor-hn.js
```

Schedule via cron (every 4 hours):

```bash
crontab -e
# Add:
0 */4 * * * cd /path/to/hackernews-intel && node scripts/monitor-hn.js >> /tmp/hn-intel.log 2>&1
```

Schedule via GitHub Actions:

```yaml
name: HN Intel Monitor
on:
  schedule:
    - cron: '0 */4 * * *'
  workflow_dispatch:
jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm install
      - run: node scripts/monitor-hn.js
        env:
          HN_KEYWORDS: ${{ secrets.HN_KEYWORDS }}
          SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
```

Add `HN_KEYWORDS` and `SLACK_WEBHOOK` as repository secrets.

## Slack Alert Format

Each alert looks like:

```
Story Title Here
47 points  23 comments  authorname
Keyword: claude code  |  HN discussion
```

## Options

| Variable | Default | Purpose |
|----------|---------|---------|
| `HN_KEYWORDS` | required | Comma-separated keywords |
| `SLACK_WEBHOOK` | required | Slack Incoming Webhook URL |
| `HN_MIN_POINTS` | `0` | Minimum points to alert |
| `HN_INCLUDE_COMMENTS` | `false` | Also monitor HN comments |
| `HN_DB_PATH` | `./hn-intel.db` | SQLite cache file path |

## CLI Flags

| Flag | Purpose |
|------|---------|
| `--dry-run` | Preview matches without sending Slack alerts |
| `--days=N` | Lookback window for the first run (default: 1) |
| `--reset` | Clear the cache and start fresh |

## GitHub Actions Note

GitHub Actions does not persist files between workflow runs. The SQLite cache resets on each run, and the script re-fetches the last 1 day of posts every time. Posts from the previous run will be alerted again.

To fix this, either:
- Store `hn-intel.db` in an S3 bucket and download/upload it around the script run
- Use a self-hosted runner with persistent storage
- Use a cron job on your own machine instead

## Project Structure

```
hackernews-intel/
├── SKILL.md
├── README.md
├── .env.example
├── package.json
├── evals/
│   └── evals.json
└── scripts/
    └── monitor-hn.js
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
