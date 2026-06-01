# app-store-review-arbitrage

Give this skill a competitor's App Store or Google Play URL. It collects their public low-star reviews, detects where their store description's claims break against real complaints, and outputs a one-session brief: ranked complaint clusters, a broken promise map, landing page headline variants, and ad copy you can use tomorrow.

No API key. No paid tools. One URL in, one ready-to-use brief out.

---

## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install app-store-review-arbitrage --target claude
```

### Option D: Manus AI

<video src="https://www.opendirectory.dev/ManusAI-one-click-installation-demo.webm" controls style="width: 100%"></video>

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fapp-store-review-arbitrage&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.

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
