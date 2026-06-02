# gh-issue-to-demand-signal

Give the skill a competitor's public GitHub repo URL. It fetches their open issues, filters noise locally, clusters into 6 demand categories using the AI already running the skill, scores by real engagement (reactions), detects ignored demand (high reactions + no response = your opportunity), and outputs a ranked demand gap report with a GTM messaging brief.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install gh-issue-to-demand-signal --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fgh-issue-to-demand-signal&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Does

- Fetches up to 200 open issues from any public GitHub repo (no auth required)
- Filters noise locally: removes PRs, bot issues, zero-engagement issues, and chore-pattern titles
- Computes a demand score per issue: `(reactions["+1"] x 2) + (comments x 0.5)`
- Detects "ignored demand": issues with 10+ reactions, open 6+ months, no planned label
- Clusters issues into 6 categories using the AI running the skill (no external API key needed): feature gaps, bug patterns, UX complaints, performance issues, missing integrations, missing docs
- Generates 5-8 cluster themes with total demand scores
- Messaging brief: 3 positioning angles + 3 outreach hooks + cluster-specific headlines
- Saves output to `docs/demand-signals/[owner]-[repo]-[date].md`

## Requirements

| Requirement | Purpose | How to Set Up |
|---|---|---|
| GitHub token | Raises rate limit from 60/hr to 5000/hr | github.com/settings/tokens (no scopes needed for public repos) |

No external AI API key needed. The skill uses the AI assistant running it (Claude, Gemini, Copilot) to do the clustering and messaging brief. GitHub token is optional but recommended for repeated use.

## Setup

```bash
cp .env.example .env
# Add GITHUB_TOKEN (optional, recommended for repeated use)
```

## How to Use

```
"Scan competitor GitHub issues: https://github.com/vercel/next.js"
"What are users asking for in facebook/react?"
"Find demand gaps in linear-app/linear"
"Turn GitHub complaints into messaging: https://github.com/supabase/supabase"
"What should I build based on competitor issues? vercel/next.js"
"Which features are users begging for in this repo?"
```

## Why This Matters

A busy product team cannot read 500 open issues. This skill does the work: ranks by real user demand (reaction counts), clusters into actionable GTM categories, detects ignored demand (where competitors have been silent the longest), and translates raw complaints into positioning language.

**The demand score formula:** `(reactions["+1"] x 2) + (comments x 0.5)`. Reactions are weighted higher than comments because reactions are pure signal -- a thumbs-up means "I want this." Comments include maintainer responses, off-topic discussion, and spam.

**Ignored demand is your opportunity:** An issue with 50 reactions that has been open for 2 years with no planned label means their users have been waiting. That is your product's first billboard.

## The 6 Demand Categories

| Category | What it captures |
|---|---|
| `feature_gap` | Functionality that does not exist yet |
| `bug_pattern` | Recurring broken behavior that erodes trust |
| `ux_complaint` | Friction, confusion, or workflow problems |
| `performance` | Slowness, timeouts, resource usage |
| `integration_missing` | Requests to connect with other tools or APIs |
| `docs_missing` | Confusion caused by absent or wrong documentation |

## Output

Each run produces:

1. **Demand Gap Leaderboard**: clusters ranked by total demand score
2. **Ignored Demand section**: issues open 6+ months with 10+ reactions and no response
3. **Top 10 Highest-Demand Issues**: verbatim titles, reaction counts, direct GitHub links
4. **Cluster Deep Dives**: top 3 clusters with theme name, pain summary, top 3 verbatim issues
5. **Messaging Brief**: 3 positioning angles citing exact demand evidence
6. **GTM Angles**: 3 outreach hooks using verbatim issue language

## Cost per Run

- GitHub API: 2 calls -- free (unauthenticated: 60/hr limit, token: 5000/hr)
- AI analysis: uses the model already running the skill -- no additional cost
- Total: free

## Project Structure

```
gh-issue-to-demand-signal/
├── SKILL.md
├── README.md
├── .env.example
├── evals/
│   └── evals.json
└── references/
    ├── demand-categories.md
    └── gtm-translation.md
```

## License

MIT
