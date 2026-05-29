# Company Radar

Competitive intelligence orchestrator for opendirectory. Takes company names, researches them across 8+ platforms in parallel, computes a 0-100 heat score, and outputs structured radar reports with AI briefings.

---

## Install

```bash
npx "@opendirectory.dev/skills" install company-radar --target claude
```

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


## What It Does

Given a list of companies to track, Company Radar:

1. **Builds a profile** for each company (domain, social handles, founders, YC batch)
2. **Scans 8 channels in parallel** — GitHub, Twitter/X, Reddit, Hacker News, Product Hunt, YC Jobs, Web/Press, Pricing
3. **Computes a heat score** (0-100) across 4 dimensions: Authority, Shipping, Social, Growth
4. **Generates an AI executive briefing** per company and a landscape-level summary
5. **Outputs a structured radar report** with leaderboard, deep dives, and alerts

---

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Main orchestration skill — entry point for the AI agent |
| `README.md` | Install and usage docs |
| `scripts/heat-score-calc.mjs` | Standalone heat score engine — run on collected signal data |
| `references/heat-score-methodology.md` | Full scoring formulas and examples |
| `references/radar-report-template.md` | Report output structure |
| `references/company-profile-format.md` | Company data schema |
| `references/skill-integration-map.md` | How to call each opendirectory skill for channel data |

---

## Prerequisites

- **opencode** with the opendirectory skill set installed
- The following skills available in your opendirectory config:
  - `reddit-icp-monitor` (optional; falls back to Tavily)
  - `twitter-GTM-find-skill` (optional; falls back to Tavily)
  - `hackernews-intel` (optional; falls back to HN Algolia)
  - `yc-jobs-scraper` (required for YC job signals)
  - `producthunt-launch-kit` (optional; falls back to Tavily)
  - `competitor-pr-finder` (optional)
  - `map-your-market` (optional, for landscape analysis)
- **Tavily API key** (for web search fallbacks)
- **GitHub CLI** (`gh`) installed and authenticated (for GitHub signal collection)

---

## Usage

### Basic Radar Run

```text
/company-radar

Companies to track: Vercel, Netlify, Railway
```

The skill walks through all steps: Parse input → Build profiles → Collect signals (parallel) → Heat score via `scripts/heat-score-calc.mjs` → Generate briefing → Assemble report

### Using the Heat Score Script Directly

After collecting signal data, you can run the scorer standalone:

```bash
# From the skill directory
node scripts/heat-score-calc.mjs --file signals.json

# Or pipe raw JSON
cat signals.json | node scripts/heat-score-calc.mjs
```

Input is a JSON file with `companies[]` containing signal data. Output is scored JSON with per-dimension breakdowns and auto-generated alerts.

### Quick Heat Score Only

```text
/company-radar

Companies to track: Supabase
Mode: heat-score-only
```

Returns just the heat score with minimal context -- no full report.

### Recurring Radar

```text
/company-radar

Companies: Vercel, Netlify, Railway, Supabase
Schedule: daily
```

Runs the radar and compares scores with the previous run to show deltas.

---

## Output

The skill produces a single structured markdown report containing:

- **Executive Summary** -- landscape-level synthesis, ranked companies, key alerts
- **Heat Score Leaderboard** -- table of all tracked companies sorted by score
- **Per-Company Deep Dives** -- full signal detail per channel, heat score breakdown, AI executive briefing
- **Alerts Summary** -- notable signals grouped by severity
- **Data Quality Notes** -- which channels returned data per company

---

## Heat Score Dimensions

| Dimension | Max | Measures |
|---|---|---|
| Authority | 25 | GitHub stars/forks, Product Hunt validation |
| Shipping | 25 | Commit velocity, release frequency, recency |
| Social | 25 | Twitter, Reddit, HN, YouTube activity |
| Growth | 25 | Hiring volume, sentiment, traction indicators |

Total: **0-100**

Activity levels: **High** (60+), **Medium** (30-59), **Low** (1-29), **Dormant** (0)

---

## Customization

### Add a New Channel

1. Add the signal formulas to `references/heat-score-methodology.md`
2. Add the skill mapping to `references/skill-integration-map.md`
3. Add the data fields to the report template in `references/radar-report-template.md`
4. Update the orchestration flow in `SKILL.md` Step 4

### Adjust Scoring Weights

Edit the formula tables in `SKILL.md` Steps 5-8 and `references/heat-score-methodology.md`. Each dimension caps at 25 points max.
