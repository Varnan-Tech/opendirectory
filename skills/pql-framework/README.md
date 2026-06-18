# pql-framework

Turn product behavior into a sales motion. Give this skill your product type and current telemetry setup, and it outputs a complete PQL system: pre-scoring exclusion filters, a two-dimensional signal library (behavioral + firmographic), a weighted scoring matrix with decay logic, A/B/C tiering, and Slack/CRM routing — including a founder-day-1 path that requires zero data warehouse infrastructure.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install pql-framework --target claude
```

### Option B: skills.sh

```bash
npx skills add Varnan-Tech/opendirectory --skill pql-framework
```

Requires Node.js. Add `--global` to install to `~/.claude/skills/` instead of the current project.

### Option C: Claude Desktop App

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

### Option D: Claude Code Native

Run these commands inside Claude Code:

```bash
/plugin marketplace add Varnan-Tech/opendirectory
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

### Option E: Manus AI

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fpql-framework&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page.

1. Open the skill you want from the [opendirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Does

- Applies pre-scoring exclusion filters before any scoring runs (paid/no-upsell, expired trials, active escalations, competitors)
- Builds a two-dimensional signal library: behavioral events (activation, depth, expansion, monetization proximity) + firmographic overlays (company size, role, funding stage, tech stack)
- Outputs a weighted scoring matrix with default point values, decay windows (7-day halving, 14-day reset), and disqualifier overrides
- Maps scores to A/B/C tiers with routing plays and SLA targets per tier
- Provides a founder-scale Day 1 path: wire 2-3 events to Slack via PostHog/Mixpanel/Segment webhooks, no data warehouse required
- Includes a measurement loop: conversion rate, time-to-first-touch, false positive rate, and 30-day model compounding cadence
- Cross-references complementary Opendirectory skills: `sdk-adoption-tracker`, `company-radar`, `outreach-sequence-builder`

## Key Insight

Expansion signals (teammate invite → 2+ users, single-team → multi-team growth) outperform arbitrary usage thresholds as PQL triggers for developer-first products. These signals represent permanent organizational adoption state changes — not time-bounded behaviors — and should carry the highest scoring weight in your model.
