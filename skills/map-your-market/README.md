# map-your-market

Give this skill a product description, category keywords, or competitor names. It searches Reddit, Hacker News, GitHub Issues, G2, and Google Trends for real pain signals from your market -- then builds a complete positioning framework: who your ICP is, what they say out loud, and how to talk to them.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install map-your-market --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fmap-your-market&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Does

- Accepts any combination of: product description, category keywords, competitor names
- Auto-detects relevant subreddits from the category
- Searches Reddit public JSON API for pain posts (top posts, last 12 months)
- Searches Hacker News Algolia API for stories and Ask HN threads
- Searches GitHub Issues on competitor repos for high-reaction complaints
- Scrapes G2 category pages for vendor count and top products
- Fetches Google Trends direction (up / flat / down) for the category
- Scores every signal by source weight and recency (GitHub issues score 3x Reddit -- more deliberate signal)
- Clusters top 60 signals into 5-7 named pain themes
- Extracts ICP from subreddit and post metadata (not just content)
- Generates a positioning framework with messaging angles using verbatim market language
- Saves output to `docs/market-maps/[category]-[date].md` + JSON snapshot

## Requirements

| Requirement | Purpose | How to Set Up |
|---|---|---|
| GITHUB_TOKEN | Optional -- improves GitHub Issues rate limit from 60/hr to 5000/hr | github.com/settings/tokens (no scopes needed for public repos) |

No other API keys required.

## Setup

```bash
cp .env.example .env
# Add GITHUB_TOKEN if you want higher GitHub rate limits
```

## How to Use

```
"Map my market: I build developer observability tools"
"Who is my ICP? Competitors: Datadog, Grafana, New Relic"
"What are the top pains in the HR software market?"
"Find messaging angles for my B2B analytics tool"
"Map the CRM market. What are people complaining about?"
"I build payment APIs. Who should I be selling to?"
```

Include competitor names for richer GitHub Issues data. Include a product description for tailored messaging angles.

## Why This Instead of Manual Research

A founder doing this manually would spend 2-3 days:
- Reading Reddit threads, taking notes
- Scrolling HN "Ask HN" posts
- Checking G2 review counts per vendor
- Looking up Google Trends
- Synthesizing into a document

This skill does the same sweep in 3 minutes and returns verbatim quotes, not paraphrased summaries. The messaging framework uses the exact language your market uses -- not marketing copy you invented.

## The Pain Score

`pain_score = base * recency_factor`

- GitHub issue reactions: `reactions * 3` -- a developer deliberately clicking +1 is the strongest signal
- Reddit: `upvotes + (comments * 0.3)` -- upvotes count more than comments (comments include noise)
- HN: `points + (comments * 0.3)` -- same structure

Score tiers: critical (200+), high (50-199), medium (10-49), noise (<10, filtered out).

## Velocity Tracking

Run the skill every quarter. JSON snapshots in `docs/market-maps/` let you compare pain cluster rankings over time. A pain that was #3 last quarter and is #1 this quarter is accelerating -- a stronger positioning bet.

## Cost Per Run

- Reddit, HN, Google Trends: free, no auth
- GitHub Issues: free with optional token
- G2 scrape: free HTML fetch
- AI analysis: uses the model already running the skill
- Total: free

## Standalone Script

Run data collection without Claude. Useful when you want the raw signals first, then bring them to any AI for analysis.

```bash
# Basic usage
python3 scripts/fetch.py "developer observability"

# With competitors
python3 scripts/fetch.py "developer observability" --competitors "Datadog,Grafana,New Relic"

# With product context
python3 scripts/fetch.py "B2B analytics" --context "We help ops teams track spend"

# Print to stdout
python3 scripts/fetch.py "devops tooling" --stdout | jq '.summary'

# With GitHub token for higher rate limits
GITHUB_TOKEN=your_token python3 scripts/fetch.py "CRM software" --competitors "Salesforce,HubSpot" --output results.json
```

The script writes a JSON file with all raw signals. Open that file with Claude and ask: "Generate a market map and positioning framework from this data."

## Project Structure

```
map-your-market/
├── SKILL.md
├── README.md
├── .env.example
├── scripts/
│   └── fetch.py           standalone data collector
├── evals/
│   └── evals.json
└── references/
    ├── subreddit-map.md   category to subreddit mapping
    ├── pain-scoring.md    scoring formula and tier thresholds
    └── icp-signals.md     how to extract ICP from post metadata
```

## License

MIT
