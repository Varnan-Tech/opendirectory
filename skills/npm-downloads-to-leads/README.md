# npm-downloads-to-leads

Give this skill a list of npm packages. It fetches 12 weeks of download data, scores each package by growth velocity, maps maintainers to GitHub and Twitter, and outputs a ranked lead brief per breakout package: who built it, how to reach them, and what to say.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install npm-downloads-to-leads --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fnpm-downloads-to-leads&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Does

- Fetches 12 weeks of daily download data per package from the npm Downloads API
- Aggregates to weekly buckets and computes a velocity score: recent growth x acceleration x sweet-spot multiplier
- Classifies each package as BREAKOUT, WATCHING, steady, established, or too early
- Fetches maintainer profiles from the npm registry and GitHub API
- Extracts GitHub followers, Twitter handle, bio, and company from each maintainer's GitHub profile
- Generates a lead brief per breakout package: growth story, contact signals, why to reach out now, and a suggested first message
- Saves output to `docs/npm-leads/[date].md`

## Requirements

| Requirement | Purpose | How to Set Up |
|---|---|---|
| GitHub token | Raises rate limit from 60/hr to 5000/hr for maintainer profile lookups | github.com/settings/tokens (no scopes needed for public user profiles) |

No external AI API key needed. The npm and npm registry APIs are fully public with no auth. GitHub token is optional but recommended for lists larger than 10 packages.

## Setup

```bash
cp .env.example .env
# Add GITHUB_TOKEN (optional, recommended for larger package lists)
```

## How to Use

```
"Find leads from these npm packages: esbuild, vite, @hono/hono, zod"
"Track download trends for competitor packages: turbo, nx, lerna"
"Who maintains these breakout npm packages? bun, oxc-parser, biome"
"Find evangelists before they are famous: @effect-ts/core, fp-ts, zod"
"Analyze npm momentum for my space: my-package, competitor-a, competitor-b"
"Map npm maintainers to Twitter for these packages: ..."
```

Include a short description of your product and the skill will tailor the outreach message to your context.

## Why Velocity Score, Not Raw Downloads

React gets 50 million downloads a week. Its maintainers are already famous, already inundated with outreach, and already aligned with a framework you are likely building on.

The velocity score finds the package going from 1K to 8K weekly downloads over 8 weeks. That maintainer just crossed a growth inflection. They are building an audience, they are not yet overwhelmed, and they are in a phase where your product makes a difference to their workflow.

The formula: `velocity_score = growth_ratio x acceleration x sweet_spot_multiplier`

- `growth_ratio`: recent 4-week average divided by prior 4-week average
- `acceleration`: last 2 weeks vs mid 2 weeks (is growth speeding up?)
- `sweet_spot_multiplier`: 1.0 for 500 to 500K weekly downloads, lower for noise floor or established giants

Breakout threshold: velocity score above 80 AND 500 to 500K weekly downloads.

## The Lead Brief

For each breakout and watching package:

- **Growth story**: exact download numbers, 8-week comparison, weekly trend
- **Maintainer profile**: GitHub handle, Twitter, bio, company, follower count
- **Why reach out now**: specific to this package's growth inflection point
- **Suggested first message**: names the package, its growth, and connects to your product context

## Cost Per Run

- npm Downloads API: free, no auth, no rate limit concerns
- npm Registry API: free, no auth
- GitHub API: free (60 req/hr unauthenticated, 5000/hr with token)
- AI analysis: uses the model already running the skill; no additional cost
- Total: free

## Standalone Script

Run the data fetching step directly from the terminal without Claude. Useful for scheduled jobs, CI pipelines, or exploring data before generating lead briefs.

```bash
# Basic usage
python3 scripts/fetch.py esbuild zod @hono/hono

# With product context
python3 scripts/fetch.py esbuild zod --context "We build a TypeScript DX platform"

# From a file (one package per line)
python3 scripts/fetch.py --file packages.txt --output results.json

# Print to stdout
python3 scripts/fetch.py esbuild zod --stdout | jq '.summary'
```

The script handles Steps 3 to 5 (download fetch, velocity scoring, maintainer enrichment) and writes a JSON file. Open that file with Claude and ask: "Generate lead briefs from this npm data."

```bash
GITHUB_TOKEN=your_token python3 scripts/fetch.py esbuild zod @hono/hono
```

Script output fields per package:

- `velocity_score`, `growth_pct`, `recent_4_avg`, `prior_4_avg`, `tier`
- `weeks`: array of 12 weekly download counts, oldest to newest
- `profile.description`, `profile.keywords`, `profile.npm_maintainers`
- `profile.github_users`: array with `username`, `twitter_username`, `followers`, `bio`, `company`

## Project Structure

```
npm-downloads-to-leads/
├── SKILL.md
├── README.md
├── .env.example
├── scripts/
│   └── fetch.py           standalone data fetcher (Steps 3 to 5, no Claude needed)
├── evals/
│   └── evals.json
└── references/
    ├── velocity-scoring.md
    └── outreach-timing.md
```

## License

MIT
