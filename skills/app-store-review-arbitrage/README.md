# app-store-review-arbitrage

Give this skill a competitor's App Store or Google Play URL. It collects their public low-star reviews, detects where their store description's claims break against real complaints, and outputs a one-session brief: ranked complaint clusters, a broken promise map, landing page headline variants, and ad copy you can use tomorrow.

No API key. No paid tools. One URL in, one ready-to-use brief out.

---

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install app-store-review-arbitrage --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fapp-store-review-arbitrage&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Does

1. Collects up to 200 public reviews from App Store or Google Play — free, no API key, no login required. *(Note: App Store apps may sometimes return 0 reviews due to Apple RSS API limitations; Google Play is the primary supported path.)*
2. Filters to 1–3 star reviews and scores each by severity (star rating) and recency — the most recent failures get the highest weight
3. Clusters complaints into 4–6 named themes using the reviewers' own language — no abstracted labels like "stability issues"
4. Detects broken promises: cross-references the competitor's own store description against the complaint clusters and flags where their marketing overclaims reality
5. Outputs a copy-ready brief: complaint leaderboard with verbatim quotes, broken promise map, landing page H1 variants, ad copy directions, and anti-claim warnings

---

## Prerequisites

- Python 3.9+
- One pip package (free, open source, no API key):
  ```bash
  pip install google-play-scraper
  ```
- An AI agent: Claude Code, Gemini CLI, GitHub Copilot, or any compatible tool

---

## Usage

Pass any of these prompts to your agent:

```
Analyze competitor reviews: https://apps.apple.com/us/app/notion-notes-tasks-ai/id1232780281
```

```
Run app-store-review-arbitrage on https://play.google.com/store/apps/details?id=com.robinhood.android
```

```
Scan this competitor's reviews and give me ad copy angles:
https://apps.apple.com/us/app/todoist-to-do-list-tasks/id572688855

My product does: offline-first task management that syncs without a subscription.
```

The `product_context` line (what your product does) is optional. If provided, ad copy directions will reference your specific product features. If absent, directions are phrased as positioning templates.

---

## Output

One markdown file saved to `docs/review-briefs/[app-slug]-[YYYY-MM-DD].md`.

Five sections, always present:

| Section | Contents |
|---|---|
| 1. Complaint Cluster Leaderboard | Ranked complaint themes with scores, review counts, and verbatim quotes |
| 2. Broken Promise Map | Competitor's store claims cross-referenced against complaint clusters |
| 3. Landing Page H1 Bank | 3–5 headline variants derived from reviewer language |
| 4. Ad Copy Directions | 3 "say this / not that" pairs grounded in complaint evidence |
| 5. Anti-Claim Warnings | What not to claim in your own marketing, and why |

---

## When NOT to Use

- **Need to map a whole market category?** Use [`map-your-market`](../map-your-market) instead
- **Need to find what features users want built next?** Use [`gh-issue-to-demand-signal`](../gh-issue-to-demand-signal) instead
- **Need to write outreach emails after reading the brief?** Use [`outreach-sequence-builder`](../outreach-sequence-builder) next
- **Need to analyze your own app's reviews?** This skill is for competitor analysis only — the workflow is different
- **App has fewer than 10 low-star reviews?** The skill will stop and tell you — that's by design

---

## Plays Well With

| Skill | How |
|---|---|
| [`map-your-market`](../map-your-market) | Run first to understand the category; run this skill to extract copy from the top competitor |
| [`outreach-sequence-builder`](../outreach-sequence-builder) | Feed complaint cluster themes as "pain points your product solves" context when building cold outreach angles |
| [`noise-to-linkedin-carousel`](../noise-to-linkedin-carousel) | Use the complaint cluster themes as slide content for a "why we built this" carousel |

---

## Cost per Run

| Component | Cost |
|---|---|
| App Store collection | Free — uses direct iTunes RSS JSON API (no package, no API key) |
| Google Play collection | Free — uses `google-play-scraper` (pip, open source, no API key) |
| LLM analysis | Uses the model already running the skill — no additional cost |
| **Total** | **Free** |

---

## Data Quality Notes

- All quotes in the output are verbatim from collected reviews — no paraphrase, no editing
- Broken promise detection is only as good as the competitor's store description. If the description is sparse, Section 2 will note this rather than fabricating comparisons
- Collection is capped at 200 reviews. For apps with very high review volumes, this is a sample — the most recent reviews by default
- The scoring formula weights recent 1-star reviews most heavily: `complaint_weight = (4 - rating) × recency_factor`
- See [`references/scoring.md`](references/scoring.md) for the full formula and tier thresholds
