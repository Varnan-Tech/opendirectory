---
name: newsletter-digest
description: Aggregates RSS feeds from the past week, synthesizes the top stories using Gemini, and publishes a newsletter digest to Ghost CMS. Optionally outputs formatted Markdown for Substack or any other platform. Use when asked to generate a newsletter, create a weekly digest, summarize RSS feeds, compile top stories for a newsletter, or publish a digest to Ghost. Trigger when a user mentions newsletter digest, weekly roundup, RSS digest, compile top stories, or publish to Ghost.
author: OpenDirectory
version: 1.0.0
---

# Newsletter Digest

Aggregate content from RSS feeds, synthesize the week's top stories with Gemini, and publish a digest to Ghost CMS. Supports weekly digests, topic-focused roundups, and curated picks formats.

## Writing Style

Apply to all generated digest content:

- Active voice only
- Short sentences, one idea per sentence
- No em dashes — use a period or comma instead
- No semicolons
- No markdown or asterisks in the final newsletter body
- No hashtags

Banned words — do not use any of these in the digest:
incredible, amazing, leveraging, synergize, game-changing, game changer, delve, harness, unlock, groundbreaking, cutting-edge, remarkable, paradigm, revolutionize, disruptive, transformative, thrilled, excited to share, powerful, innovative, comprehensive, actionable, crucial, vital, pivotal, elucidate, utilize, dive deep, tapestry, illuminate, revolutionize

## CRITICAL RULE

Every claim, statistic, and summary in the digest must come from the fetched articles. Never fabricate data points, quotes, or facts. If a source article has no meaningful content, skip it.

---

## Step 1: Check Setup

**1a. Verify feeds are configured**

Check if `feeds.json` exists in the skill directory:

```bash
ls /Users/ksd/Desktop/Varnan_skills/newsletter-digest/feeds.json 2>/dev/null
```

If missing, ask the user: "Which RSS feeds should I monitor? Share a list of URLs and I'll create feeds.json."

The format is:
```json
[
  { "url": "https://example.com/feed", "name": "Source Name" },
  { "url": "https://another.com/rss", "name": "Another Source" }
]
```

**1b. Verify required environment variables**

Check that these are set:
- `GEMINI_API_KEY` (required): for synthesis
- `GHOST_URL` and `GHOST_ADMIN_KEY` (required for Ghost publishing, optional if output-only)

If GEMINI_API_KEY is missing, stop and ask the user to set it.

GHOST config is optional. If not set, the skill outputs formatted Markdown instead of publishing.

**1c. Verify script dependencies**

```bash
ls /Users/ksd/Desktop/Varnan_skills/newsletter-digest/node_modules 2>/dev/null | head -1
```

If missing:

```bash
cd /Users/ksd/Desktop/Varnan_skills/newsletter-digest && npm install
```

---

## Step 2: Fetch and Parse Feeds

Run the fetch script:

```bash
node /Users/ksd/Desktop/Varnan_skills/newsletter-digest/scripts/fetch-feeds.js
```

The script:
- Reads `feeds.json` for the list of feeds
- Fetches each feed using `rss-parser`
- Filters items published in the last 7 days
- Deduplicates by URL
- Sorts by publish date, newest first
- Saves results to `/tmp/newsletter-digest-articles.json`

If the script errors on a specific feed, it logs a warning and continues. One bad feed does not stop the run.

After the script completes, verify the output:

```bash
node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('/tmp/newsletter-digest-articles.json', 'utf8'));
console.log('Total articles:', data.articles.length);
console.log('From feeds:', data.feedsSummary.map(f => f.name + ': ' + f.count).join(', '));
console.log('Date range:', data.dateRange.from, 'to', data.dateRange.to);
"
```

If fewer than 3 articles are found, warn the user and ask if they want to extend the date range to 14 days. Pass `--days=14` to the script to widen the window.

---

## Step 3: Read Format Rules

Read `references/digest-format.md` in full before generating any content. Internalize:
- Three digest formats (Weekly Roundup, Topic Deep Dive, Curated Picks) and when to use each
- Section structure and length requirements per format
- Attribution rules (every claim links to a source)
- Tone and voice guidelines

Read `references/output-template.md` and select the template matching the requested format.

If the user did not specify a format, default to Weekly Roundup.

---

## Step 4: Synthesize with Gemini

Read `/tmp/newsletter-digest-articles.json` and build a synthesis prompt.

**Prompt structure:**

```
You are a newsletter editor writing a digest of this week's top stories.

Sources (use ONLY these — do not invent facts):
[For each article: Title | Source | Date | Summary]

Task:
Write a [FORMAT] digest following this structure:
[Paste the selected template from references/output-template.md]

Rules:
- Every claim, statistic, and quote must come from the sources above
- Write in active voice, short sentences, contractions allowed
- Do not use: incredible, amazing, leveraging, game-changing, delve, groundbreaking, cutting-edge, revolutionize
- No em dashes, no semicolons, no hashtags
- Include [Source: Name](URL) attribution after each major claim
- Output plain text with HTML heading tags only (no markdown asterisks)
```

Call Gemini with this prompt. Target model: `gemini-2.0-flash` or the latest available.

If the response contains any banned words or invented statistics not present in the source articles, regenerate with a stricter prompt.

---

## Step 5: Self-QA

Run every check before presenting. Fix violations first.

- [ ] Every claim, statistic, and quote traces to a source article
- [ ] No banned words in any section
- [ ] No em dashes in the text
- [ ] No semicolons in the text
- [ ] Every section has at least one source attribution with URL
- [ ] Word count is within the format's target range (see references/digest-format.md)
- [ ] No section repeated the same story twice
- [ ] Title is specific (includes the date range or issue number, not just "Weekly Digest")
- [ ] HTML output is valid (no unclosed tags if Ghost publishing)

Fix all violations before presenting to the user.

---

## Step 6: Format and Preview

Present the digest to the user in this order:

1. **Title** — Issue date range or topic
2. **Digest content** — Full formatted text
3. **Source list** — All articles used, with URLs
4. **Word count and article count**

Ask: "Ready to publish to Ghost as a draft, or would you like to edit first?"

---

## Step 7: Publish to Ghost or Output

**If GHOST_URL and GHOST_ADMIN_KEY are set and user confirms:**

Run the publish script:

```bash
node /Users/ksd/Desktop/Varnan_skills/newsletter-digest/scripts/ghost-publish.js \
  --title "DIGEST_TITLE" \
  --status "draft"
```

The script reads `/tmp/newsletter-digest-output.json` (written by the agent in Step 6) and posts to Ghost.

After posting, the script returns the Ghost admin URL for the draft. Present this to the user: "Draft saved at: [URL]. Review and publish from your Ghost dashboard."

If the user wants to publish immediately, pass `--status "published"` to the script.

**If Ghost is not configured or user says "output only":**

Output the digest in three formats:

1. **HTML** — ready to paste into any CMS
2. **Markdown** — for Substack, Notion, or Hashnode
3. **Plain text** — for email clients

Add: "Substack does not offer a public API. Copy the Markdown version into your Substack editor directly."

---

## Notes on Substack

Substack has no public API. Programmatic posting is not possible without reverse-engineering internal endpoints, which violates their terms. The skill outputs a formatted Markdown digest ready to paste into the Substack editor. This is the correct approach.


