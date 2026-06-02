# competitor-pr-finder

Give it your product URL. It finds your top 5 competitors, researches every press mention, podcast appearance, and community post across all of them, and tells you exactly which channels to pitch -- with the journalist's name, the angle that got your competitors featured, and a ready-to-send cold pitch for your product.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install competitor-pr-finder --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fcompetitor-pr-finder&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Does

1. Fetches your product page (Firecrawl or Tavily extract)
2. Analyzes your product: taxonomy, differentiators, ICP
3. Discovers 5 competitor companies via Tavily search
4. **Asks you to confirm the competitor list** before running research
5. Runs three-track PR research across all 5 competitors:
   - **Track A (Editorial):** News articles, feature pieces, funded announcements
   - **Track B (Podcasts):** Founder interviews, guest appearances, episode mentions
   - **Track C (Communities):** Reddit threads, HN posts, ProductHunt launches
6. Tiers channels by how many competitors appeared in each (Tier 1 = 3+ competitors)
7. Looks up the journalist or host name for each Tier 1 channel
8. Generates a cold pitch draft per Tier 1 channel: subject line + 3-4 sentence body

## Output

A PR intel report saved to `docs/pr-intel/[product-slug]-[date].md` containing:

- **Tier 1 channels** (proven beats for your space) with journalist name, story angle, and cold pitch draft
- **Tier 2 channels** (quick hits table -- channels that covered 2 of 5 competitors)
- **Tier 3 channels** (discovery list -- one mention only)
- **3 bonus hooks** -- pitch angles none of your competitors have used

## Requirements

| Tool | Required | Purpose | Free Tier |
|---|---|---|---|
| Tavily API | Yes | Competitor discovery, PR research, journalist lookup | 1000 credits/month (~40 runs) |
| Firecrawl API | No | Fetch JS-rendered product pages | 500 credits/month |

If Firecrawl is not set, Tavily extract is used as a fallback.

## Setup

```bash
cp .env.example .env
# Add TAVILY_API_KEY (required) and FIRECRAWL_API_KEY (optional)
```

## Usage

```
Find my PR targets: https://yourstartup.com
```

Or paste a description if you don't have a live URL:
```
Find PR targets for my startup. We build [what you do] for [who]. [Stage], [geography].
```

## Cost

| Operation | Searches | Cost |
|---|---|---|
| Product page fetch | 1 Firecrawl or Tavily extract | ~$0.001 |
| Competitor discovery | 2 Tavily searches | ~$0.02 |
| 3-track PR research (5 competitors) | 15 Tavily searches | ~$0.15 |
| Journalist lookup (up to 7 Tier 1 channels) | ~6 Tavily searches | ~$0.06 |
| **Total** | **~23-24 searches** | **~$0.23/run** |

## Zero-Hallucination Policy

Every channel name in the output traces to a URL in the search results. Every journalist name traces to a search result snippet. Story angles are extracted from article titles found by Tavily -- not inferred from AI training knowledge. Fields that could not be sourced are labeled "not found in search data."

## Project Structure

```
competitor-pr-finder/
├── SKILL.md                    -- 10-step workflow for Claude Code
├── README.md                   -- this file
├── .env.example                -- environment variable template
├── scripts/
│   └── research.py             -- two-phase Tavily data collector
├── evals/
│   └── evals.json              -- 5 test cases
└── references/
    ├── pr-channel-types.md     -- how to identify editorial, podcast, community channels
    ├── pitch-guide.md          -- cold pitch structure, forbidden phrases, angle extraction
    └── tier-scoring.md         -- channel tiering rules and frequency map construction
```

## Standalone Script Usage

```bash
# Phase 1: competitor discovery
python3 scripts/research.py \
    --phase discover \
    --product-analysis /tmp/cprf-product-analysis.json \
    --tavily-key "$TAVILY_API_KEY" \
    --output /tmp/cprf-competitors-raw.json

# Phase 2: PR research on confirmed competitors
python3 scripts/research.py \
    --phase pr-research \
    --competitors /tmp/cprf-competitors-confirmed.json \
    --product-analysis /tmp/cprf-product-analysis.json \
    --tavily-key "$TAVILY_API_KEY" \
    --output /tmp/cprf-pr-raw.json
```
