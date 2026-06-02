# sdk-adoption-tracker

Give this skill an SDK or library name. It searches GitHub for public repos that import it, scores each repo by company signal and activity, identifies who is building on you in production, and outputs a ranked adoption report with outreach context for high-signal company repos.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install sdk-adoption-tracker --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fsdk-adoption-tracker&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Does

- Searches GitHub code for all public repos that import or require the SDK
- Supports npm, Python, Go, Ruby, and generic import patterns -- auto-detected from the SDK name
- Filters forks, tutorials, examples, and archived repos from results
- Classifies each repo: company org, affiliated developer, solo developer, or tutorial noise
- Scores by adoption signal: org type, company field, stars, recency, fork status
- Fetches owner profile and top contributor for each high-signal repo
- Tracks adoption velocity: new repos in last 7, 14, and 30 days
- Compares to previous snapshot for exact new-adopter count on repeat runs
- Generates an outreach brief per high-signal company repo: what they are building, who introduced the SDK, and what to say
- Saves output to `docs/sdk-adopters/[sdk-name]-[date].md`

## Requirements

| Requirement | Purpose | How to Set Up |
|---|---|---|
| GitHub token | Required for code search (unauthenticated limit is 3 req/min, too low to run) | github.com/settings/tokens (no scopes needed for public repos) |

## Setup

```bash
cp .env.example .env
# Add GITHUB_TOKEN
```

## How to Use

```
"Who is using my SDK on GitHub? @company/my-sdk"
"Find companies building on my library: stripe"
"Track adoption of my Python package: requests"
"Which orgs import my SDK: @clerk/nextjs"
"Show me who uses my library and rank by company signal"
"Find warm leads from SDK adopters: my-package"
```

Include a short description of your product and the skill will tailor the outreach message to your context.

## Why Score Instead of Just List

A raw GitHub code search for a popular SDK returns tutorials, forks, abandoned side projects, and examples mixed in with real production users. The adoption score separates them:

- A company org repo with recent commits and 200 stars scores 130+
- A tutorial named "learn-stripe-payments" scores below 20 and is excluded

The person who added the import in a company repo is the warmest possible lead. They chose the SDK, they understand what it does, and they have an active production use case.

## The Adoption Score

`score = org_signal + company_field + stars_capped + recency + quality_flags`

- Org type (50 points): GitHub Organization accounts are almost always a company or serious team
- Company field (20 points): user has a company listed on their GitHub profile
- Stars (up to 50 points): capped at 500 stars to prevent established open-source from dominating
- Recency (up to 50 points): pushed in last 7 or 30 days
- Quality (up to 40 points): not a fork, not archived, not a tutorial

Score >= 80: full outreach brief generated. Score 40-79: listed in report. Score < 40: counted in breakdown only.

## Velocity Tracking

Run the skill weekly and save the JSON snapshot. On each subsequent run, the skill compares the current repo list to the previous snapshot and tells you exactly how many new teams adopted the SDK since last time.

```
New repos last 7 days: 3
New repos last 30 days: 11
New since last run (7 days ago): 3
```

## Cost Per Run

- GitHub Code Search API: free with token
- GitHub User, Org, Contributors API: free with token
- AI analysis: uses the model already running the skill; no additional cost
- Total: free

## Standalone Script

Run the data-fetching step directly from the terminal without Claude. Useful for scheduled jobs or CI pipelines.

```bash
# Basic usage
python3 scripts/fetch.py stripe

# Python SDK
python3 scripts/fetch.py requests --ecosystem python

# With product context for outreach
python3 scripts/fetch.py @company/my-sdk --context "We build observability for DevTools"

# Exclude the SDK publisher's own repos
python3 scripts/fetch.py stripe --exclude stripe

# Print to stdout
python3 scripts/fetch.py stripe --stdout | jq '.summary'
```

The script handles Steps 3-5 (code search, scoring, enrichment) and writes a JSON file. Open that file with Claude and ask: "Generate adoption briefs from this SDK data."

```bash
GITHUB_TOKEN=your_token python3 scripts/fetch.py stripe --output results.json
```

## Project Structure

```
sdk-adoption-tracker/
├── SKILL.md
├── README.md
├── .env.example
├── scripts/
│   └── fetch.py           standalone fetcher (Steps 3-5, no Claude needed)
├── evals/
│   └── evals.json
└── references/
    ├── import-patterns.md
    └── scoring-guide.md
```

## License

MIT
