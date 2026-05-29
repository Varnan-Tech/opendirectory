---
name: company-radar
description: Competitive intelligence orchestrator tracking companies across 8+ platforms (GitHub, Twitter, Reddit, HN, PH, YC Jobs) with heat scores and AI briefings.
compatibility: [claude-code, gemini-cli, github-copilot]
author: OpenDirectory
version: 1.0.0
---

# Company Radar

**Competitive intelligence orchestrator.** Takes company names, runs parallel research across 8+ platforms, scores each on a 0-100 heat scale, and produces a structured radar report with AI briefings.

This is an orchestration skill. It delegates data collection to existing opendirectory micro-skills and coordinates their output --- it doesn't replace them.

---

## Architecture

```
INPUT: Company name(s) / URL(s)
        |
  [1. Profile Phase] -- Web research to build company profiles
        |
  [2. Signal Collection] -- Parallel platform research (8 channels)
       / | | | | | \ \
      GH TW RD HN PH YC WEB MEDIA
        |
  [3. Scoring Engine] -- 4-dimension heat score (0-100)
        |
  [4. AI Synthesis] -- Executive briefing generation
        |
OUTPUT: Radar Report + Per-Company Deep Dives
```

### Signal Channels and Their Opendirectory Mappings

| Channel | Opendirectory Skill | What It Detects |
|---|---|---|
| GitHub | `gh-issue-to-demand-signal` + web search | Stars, forks, commits, releases, shipping velocity |
| Twitter/X | `twitter-GTM-find-skill` | Tweets, mentions, engagement, founder activity |
| Reddit | `reddit-icp-monitor`, `reddit-post-engine` | Community sentiment, pain points, buzz |
| Hacker News | `hackernews-intel` | Story mentions, points, front-page signals |
| Product Hunt | `producthunt-launch-kit` | Launches, votes, maker activity |
| YC Jobs | `yc-intent-radar-skill` / `yc-jobs-scraper` | Job listings, hiring departments, growth signals |
| Web / Press | Tavily search + `competitor-pr-finder` | News, product announcements, funding |
| Pricing | `pricing-finder` | Pricing changes, tier updates, plan structure |
| Market Position | `map-your-market` | ICP, competitor landscape, messaging gaps |

---

## Common Mistakes

| The agent will want to... | Why that's wrong |
|---|---|
| Run skills sequentially | All 8 signal channels are independent. Must run in parallel. |
| Hallucinate GitHub star counts or hiring numbers | Every data point must trace to a specific search result or skill output. No "approx 500 stars". |
| Skip the heat score computation | The radar report requires scored output, not just raw data dump. Heat score is the core differentiator. |
| Output incomplete reports because a skill failed | One failing channel does not block the full report. Score what you have, note gaps. |
| Use AI training knowledge for company descriptions | Every company description must come from live web research, not memory. |
| Forget to score activity levels from heat scores | Heat score has explicit thresholds: High (60+), Medium (30-59), Low (1-29), Dormant (0). |

---

## Step 1: Setup Check

Check that required API keys are accessible for the channels the user's platform supports:

```bash
if [ -z "$TAVILY_API_KEY" ]; then echo "TAVILY_API_KEY: NOT SET -- required for web enrichment"; else echo "TAVILY_API_KEY: configured"; fi
if [ -z "$GITHUB_TOKEN" ]; then echo "GITHUB_TOKEN: not set -- GitHub API rate limited to 60 req/hr"; else echo "GITHUB_TOKEN: configured"; fi
```

The specific skills being orchestrated have their own API key requirements. Check each skill's SKILL.md for details. Required for full operation:
- `TAVILY_API_KEY` -- web search and company enrichment (get at app.tavily.com)
- `GITHUB_TOKEN` -- GitHub API access (get at github.com/settings/tokens)

If `TAVILY_API_KEY` is missing: stop and tell the user. Without it, company profiling and web enrichment cannot operate.

---

## Step 2: Parse Input

Collect from the conversation:
- `companies`: list of company names/URLs to track (required, min 1, max 10 per run)
- `output_preference`: "full report" (default), "alert-only", "briefing-only", or "heat-score-only" (leaderboard table + scores only, no deep dives)
- `timeframe`: "realtime" (default) or "last-week" or "last-month"

**If the user gives a single company name:** still run full radar pipeline. Single-company radars are valid -- get the full profile.

**If more than 10 companies:** tell the user "Maximum 10 companies per radar scan. I'll run the first 10. Let me know if you want to swap any out."

Ask if any companies have specific known handles:
- GitHub org name (if different from company name)
- Twitter handle
- YC batch (if YC company)
- Product Hunt slug

This saves research time. If unknown, the profile phase will discover them.

---

## Step 3: Company Profile Phase

For each company, build a basic profile before running platform research.

### Step 3a: Initial Web Enrichment

For each company, run a Tavily search to discover:

```text
[company name] official website twitter github linkedin producthunt yc founders
```

Extract from search results:
- Domain / website URL
- Description (2-3 sentences)
- Twitter handle (from twitter.com/X.com URLs in results)
- GitHub org (from github.com URLs in results)
- LinkedIn URL
- Product Hunt slug
- YC batch and URL (if applicable)
- Founder names and Twitter handles

**Output format:** For each company, produce a profile object following `references/company-profile-format.md`.

### Step 3b: Confirm With User

Display the discovered profiles and ask the user to confirm or correct before proceeding.

```markdown
## Discovered Company Profiles

| Company | Domain | Twitter | GitHub | YC Batch | Founders |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

Correct any incorrect handles before I proceed to signal collection?
```

Wait for user confirmation. Do not skip this step -- wrong handles produce wrong signals.

---

## Step 4: Parallel Signal Collection

Now run research across all platforms **in parallel** for all confirmed companies.

### Signal Collection Map

For each platform, use the appropriate method. Run ALL platforms simultaneously -- do not sequence them.

#### GitHub Signal
Use web search (Tavily) to find GitHub org, then search for:
```text
github.com/[org] stars forks commits
```

Extract:
- Total stars across repos
- Total forks
- Recent commits (last 7 days)
- Recent releases (last 30 days)
- Last push date
- Primary language
- Open issue count

**Or** call `gh-issue-to-demand-signal` skill if you want deeper demand signal analysis from GitHub Issues.

#### Twitter/X Signal
Use `twitter-GTM-find-skill` or Tavily search:
```text
twitter.com/[handle] site:twitter.com [company] startup
```

Extract:
- Recent tweet count (last 24h)
- Mention volume
- Founder tweet activity
- Key topics/hashtags

#### Reddit Signal
Use `reddit-icp-monitor` approach or Tavily search:
```text
site:reddit.com [company name] [product category]
```

Extract:
- Mention count
- Post scores (upvotes)
- Sentiment (positive/negative/mixed)
- Key complaints or praises
- Relevant subreddits

#### Hacker News Signal
Use `hackernews-intel` approach or HN Algolia API search:
```text
site:news.ycombinator.com [company name]
```

Extract:
- Story count
- Total points
- Front-page stories
- Key topics

#### Product Hunt Signal
Use `producthunt-launch-kit` approach or Tavily search:
```text
site:producthunt.com [company name] products
```

Extract:
- Recent launches
- Upvote count
- Comments/sentiment
- Launch frequency

#### YC Jobs Signal
Use `yc-intent-radar-skill` / `yc-jobs-scraper` approach or Tavily search:
```text
site:workatastartup.com [company name] OR site:ycombinator.com/companies [company name]
```

Extract:
- Open job count
- Job titles/roles
- Department breakdown (Engineering, Sales, Marketing, etc.)
- Location/remote status

#### Web / Press Signal
Use Tavily search:
```text
[company name] funding announcement product launch news 2026
```

Extract:
- Recent funding rounds
- Product launches
- Key hires announced in press
- Partnership announcements

#### Pricing Signal (optional, run if user wants pricing intel)
Use `pricing-finder` skill or Tavily search:
```text
[company name] pricing plans 2026
```

Extract:
- Pricing tiers
- Plan structure changes
- Free tier vs paid

### Handling Failures

- If any channel returns 0 results, note it in the report as "No signal detected"
- If any skill is not available (API key missing), note as "Channel unavailable"
- Never fabricate data from memory. If you cannot find it, mark it as not found.
- One empty channel does not invalidate the full report.

---

## Step 5: Heat Score Computation

Use the bundled `scripts/heat-score-calc.mjs` to score each company. This script implements the 4-dimension scoring algorithm from `references/heat-score-methodology.md`.

### How to Run

Collect all signal data into a JSON file matching this schema:

```json
{
  "companies": [{
    "name": "CompanyName",
    "signals": {
      "stars": null, "forks": null, "ph_votes": null,
      "commits_week": null, "releases_month": null,
      "active_shipping": false, "last_activity_days": null,
      "tweets_24h": null, "mentions": null,
      "reddit_posts": null, "reddit_score": null,
      "hn_stories": null, "hn_points": null,
      "youtube_videos": null,
      "jobs": null, "dept_count": null,
      "sentiment": null, "traction": null
    }
  }]
}
```

Fill in each field with the discovered value. Leave null for anything not found — the script treats null as 0.

Then run:

```bash
node scripts/heat-score-calc.mjs --file signals.json
```

Or pipe it:

```bash
echo '{"companies":[...]}' | node scripts/heat-score-calc.mjs
```

### What It Returns

The script outputs JSON with per-company results:

```json
{
  "generated_at": "2026-05-29T...",
  "company_count": 3,
  "companies": [
    {
      "name": "Vercel",
      "heat_score": 89,
      "level": "High",
      "dimensions": {
        "authority": { "score": 25, "max": 25, "breakdown": {...} },
        "shipping": { "score": 25, "max": 25, "breakdown": {...} },
        "social": { "score": 17, "max": 25, "breakdown": {...} },
        "growth": { "score": 22, "max": 25, "breakdown": {...} }
      },
      "alerts": [...]
    }
  ]
}
```

Each company includes:
- `heat_score` — total 0-100
- `level` — High (60+), Medium (30-59), Low (1-29), Dormant (0)
- `dimensions` — per-dimension score with max and itemized breakdown
- `alerts` — auto-detected notable signals

### Scoring Rules (implemented in script)

These are the formulas the script applies. They're documented here for transparency:

| Dimension | Signals | Max |
|---|---|---|
| Authority | GitHub stars (`min(15, stars/1000*3)`), forks (`min(5, forks/200*2)`), PH votes (`min(5, votes/100*5)`) | 25 |
| Shipping | Commits/week (`min(10, commits*2)`), releases/month (5 if >0), active flag (5), recency (5 if <7d, 3 if <30d) | 25 |
| Social | Tweets (5), mentions (5), Reddit posts (3) + score (2), HN stories (4) + points (3), YouTube (3) | 25 |
| Growth | Jobs (`min(10, jobs*3)`), dept diversity (`min(5, dept_count*2)`), AI sentiment (5), AI traction (5) | 25 |

- Each dimension caps at 25. Missing signals score 0. Never estimate data.
- Full methodology and edge cases in `references/heat-score-methodology.md`.

---

## Step 6: AI Executive Briefing

For each company scored above 0 (i.e., any signal detected), generate an AI executive briefing using the collected data.

The briefing must cover:

```
**Executive Brief: [Company Name]**

**Context:** 1-2 sentences on what they do and their market position
**Heat Score:** [score]/100 — [Activity Level]

**Recent Activity:**
- Product: key product or launch signals found
- Hiring: hiring status, departments, notable roles
- Community: sentiment summary from Reddit/HN/Twitter

**Threat Assessment:**
- Competitive threat level: [Low / Medium / High]
- Rationale: 2-3 sentences on why

**Key Signal (most important takeaway):**
One sentence on the single most important thing happening with this company.

**Data Confidence:**
What channels had good data vs what was missing.
```

**Rules:**
- Every claim in the briefing must trace to collected data
- "Data Confidence" section is mandatory -- be honest about gaps
- Threat assessment should compare against the other companies in the radar, not in a vacuum
- Keep each briefing under 250 words

---

## Step 7: Assemble and Output the Radar Report

Compile everything into the structured radar report format. Use `references/radar-report-template.md` for the exact output structure.

The report should include:
1. **Executive Summary** — Top-line findings with ranked companies
2. **Heat Score Leaderboard** — Ranked table of all companies
3. **Per-Company Deep Dives** — Each company with full profile, signal data, score breakdown, and AI briefing
4. **Signal Alerts** — Notable events detected (hiring surges, viral moments, launches)
5. **Data Quality Notes** — Which channels had data, which were missing

Output in markdown format, ready to copy into Slack, Notion, Google Docs, or email.

---

## Step 8: Optional — Schedule Recurring Radar

If the user wants ongoing monitoring:

1. Save the company list and API configuration
2. Set up a cron schedule (GitHub Actions or system cron)
3. Each run produces an updated report
4. Configure alerts for score changes (e.g., "alert if any company jumps 20+ points")

This skill is an orchestrator — each run executes the full pipeline fresh.
