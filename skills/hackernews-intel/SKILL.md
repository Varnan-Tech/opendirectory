---
name: hackernews-intel
description: Monitors Hacker News for user-configured keywords, deduplicates against a local SQLite cache, and sends Slack alerts for new matching posts. Use when asked to monitor Hacker News for mentions, track keywords on HN, get alerts when something is posted about a topic on Hacker News, or set up HN keyword monitoring. Trigger when a user mentions Hacker News alerts, HN monitoring, keyword tracking on HN, or wants to know when a topic appears on Hacker News.
author: OpenDirectory
version: 1.0.0
---

# Hacker News Intel

Monitor Hacker News for keywords. On each run, fetch new posts via the HN Algolia API, deduplicate against a local SQLite cache, and send Slack alerts for unseen matches. Run manually or schedule via cron or GitHub Actions.

---

## Step 1: Check Setup

**1a. Verify required environment variables**

Check that these are set:
- `HN_KEYWORDS` (required): comma-separated list of keywords to monitor
- `SLACK_WEBHOOK` (required): Slack Incoming Webhook URL for alerts

If either is missing, stop and tell the user:
- `HN_KEYWORDS`: list the topics you want to monitor, comma-separated. Example: `claude code,LLM agents,deno runtime`
- `SLACK_WEBHOOK`: create an Incoming Webhook at https://api.slack.com/apps. Select your workspace, enable Incoming Webhooks, and copy the URL.

**1b. Verify script dependencies**

```bash
ls /Users/ksd/Desktop/Varnan_skills/hackernews-intel/node_modules/better-sqlite3 2>/dev/null
```

If missing:

```bash
cd /Users/ksd/Desktop/Varnan_skills/hackernews-intel && npm install
```

---

## Step 2: Run the Monitor

```bash
cd /Users/ksd/Desktop/Varnan_skills/hackernews-intel && node scripts/monitor-hn.js
```

**Flags:**
- `--dry-run`: print matches to stdout without sending any Slack alerts. Use this to preview what would be alerted before committing.
- `--days=N`: on the first run, look back N days (default: 1). Only applies when the SQLite cache is empty.
- `--reset`: clear the cache and start fresh. Use when you change your keyword list significantly.

**What the script does:**
1. Reads `HN_KEYWORDS` from environment, splits by comma, trims whitespace
2. Opens (or creates) a SQLite database at the path in `HN_DB_PATH` (default: `./hn-intel.db`)
3. For each keyword, calls `https://hn.algolia.com/api/v1/search_by_date` with `numericFilters=created_at_i>lastSeen`
4. For each result, checks if the `objectID` is already in `seen_posts` — skips if yes
5. If `HN_MIN_POINTS` is set, skips posts below that threshold
6. For new matching posts, sends a Slack alert and inserts the `objectID` into the cache
7. Updates `poll_log` with the run summary
8. Prints a summary to stdout

---

## Step 3: Review Results

After the script runs, read its stdout output. It will report:

```
Run complete.
  Keywords checked: N
  Posts found: N
  Posts alerted: N
  Posts skipped (already seen): N
  Errors: N
```

If `Posts found: 0` and you expect results, check:
- Are the keywords specific enough? Very broad terms (e.g. "AI") may return 0 results if HN Algolia returns too many and the time window is narrow
- Is the `--days` window large enough for the first run? Try `--days=7`
- Is the DB cache too aggressive? Try `--reset` to clear it and rerun

If `Posts alerted: 0` but `Posts found: N`, the deduplication is working — those posts were seen in a previous run.

---

## Step 4: Schedule the Monitor

**Option A: cron (macOS/Linux)**

Add to crontab to run every 4 hours:

```bash
crontab -e
```

Add this line (adjust the path to match your install):

```
0 */4 * * * cd /Users/ksd/Desktop/Varnan_skills/hackernews-intel && node scripts/monitor-hn.js >> /tmp/hn-intel.log 2>&1
```

**Option B: GitHub Actions (recommended for teams)**

Create `.github/workflows/hn-intel.yml` in any repo:

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
      - name: Install dependencies
        run: npm install
        working-directory: hackernews-intel
      - name: Run monitor
        run: node scripts/monitor-hn.js
        working-directory: hackernews-intel
        env:
          HN_KEYWORDS: ${{ secrets.HN_KEYWORDS }}
          SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
          HN_MIN_POINTS: ${{ secrets.HN_MIN_POINTS }}
```

Add `HN_KEYWORDS`, `SLACK_WEBHOOK`, and optionally `HN_MIN_POINTS` as repository secrets.

Note: GitHub Actions does not persist files between runs, so the SQLite cache resets each run. This means every run will find all posts within the default 1-day lookback window again. For persistent dedup on GitHub Actions, store the DB in a persistent location (S3, artifact cache, or a dedicated branch).

---

## Step 5: Tune Keywords and Thresholds

**Adding or changing keywords:**
Update `HN_KEYWORDS` in your `.env` or environment. No restart needed — the script reads it fresh each run.

**Setting a minimum points threshold:**
Set `HN_MIN_POINTS=10` to only alert on posts with 10 or more points. This cuts noise for broad keywords.

**Including comments (not just stories):**
Set `HN_INCLUDE_COMMENTS=true` to also monitor comments mentioning the keyword. Off by default — comments generate significantly more volume.

**Resetting the cache:**
Run `node scripts/monitor-hn.js --reset` to clear `seen_posts` and `poll_log`. The next run fetches fresh from the lookback window.

**Testing a new keyword:**
Run `node scripts/monitor-hn.js --dry-run --days=7` to see the last 7 days of matching posts without alerting anyone.


