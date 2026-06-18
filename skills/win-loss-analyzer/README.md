# win-loss-analyzer

Run a structured win/loss program that surfaces real buyer reasoning instead of CRM-recorded excuses. Give this skill your deal situation and it outputs a buyer-direct interview guide, a driver tagging taxonomy, a data capture schema, and a founder-scale cadence with routing rituals for product, sales, and marketing.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install win-loss-analyzer --target claude
```

### Option B: skills.sh

```bash
npx skills add Varnan-Tech/opendirectory --skill win-loss-analyzer
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fwin-loss-analyzer&utm_source=opendirectory)

1. Open the skill from the [opendirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI**.
4. Confirm the import inside Manus AI.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Does

- Explains the CRM self-report bias problem (50-70% divergence from real buyer reasoning) and why buyer-direct interviews are the only reliable source
- Provides deal selection criteria: which deals to interview, what ACV floor and stage filter to apply, and the 30-60 day recall window
- Outputs a full interview guide: narrative openers, four core topic areas (product, sales, pricing, competitive), follow-up probe patterns, and the 5 Whys technique for going deeper
- Defines a driver tagging taxonomy with six categories and sentiment tracking per interview
- Provides a deal metadata capture schema ready to use in Notion, Airtable, or a Google Sheet
- Covers a PLG-specific track for trial conversion losses that never appear in CRM deal records
- Sets up a founder-scale cadence (5 interviews per month, no analyst required) with routing rituals: weekly sales digests, monthly product readouts, quarterly exec reports
- Explains pattern detection by outcome, segment, competitor, and deal stage

## Key Insight

CRM loss reasons are wrong 50-70% of the time. Sales reps default to "price" as a face-saving explanation, and buyers self-censor when talking to internal stakeholders. The 5 Whys technique applied to a buyer-direct interview moves "price was too high" to "per-seat model doesn't fit our headcount spikes" to "CFO needs predictable fixed costs" — three steps to an actionable pricing structure decision.
