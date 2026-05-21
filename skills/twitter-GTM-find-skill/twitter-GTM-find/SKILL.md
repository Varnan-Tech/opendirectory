---
name: twitter-GTM-find-Skill
description: End-to-end pipeline for scraping X/Twitter for GTM/DevRel tech startup jobs using Apify, or optionally TweetClaw for OpenClaw and Hermes Tweet for Hermes Agent, then validating them against an Ideal Customer Profile (ICP) using Gemini's native Google Search Grounding. Use this skill when OpenClaw needs to find developer-first, funded startups actively hiring for GTM, DevRel, or Growth roles.
---

# Twitter GTM Find Skill

This skill provides an automated pipeline to scrape Twitter for Developer-First startups hiring GTM/DevRel roles, followed by an automatic web-search verification step to validate them against our Ideal Customer Profile (ICP).

## Using the Pipeline

You can run the full pipeline using the executable Node.js project bundled in `scripts/`. 

```bash
cd scripts
npm install
npx ts-node src/index.ts
```

**Requirements:**
A `.env` file must be present at the workspace root with:
- `APIFY_API_TOKEN` (Apify account access)
- `GEMINI_API_KEY` (Gemini 3 Flash Preview with Search Grounding)
- `MAX_POSTS=20` (Optional limit)

## Optional Native X/Twitter Plugin Inputs

If the user is running OpenClaw with
[TweetClaw](https://github.com/Xquik-dev/tweetclaw), you may use it as a native
OpenClaw plugin for the discovery stage while keeping the ICP validation stage
unchanged.

Install it when needed:

```bash
openclaw plugins install @xquik/tweetclaw
```

With `XQUIK_API_KEY` configured, use:

- `explore` to find tweet search, reply search, user lookup, follower export,
  monitor, and webhook endpoints
- `tweetclaw` to scrape tweets, search tweets and replies, look up promising
  founders or company accounts, export followers, and monitor leads during this
  workflow

If the user is running Hermes Agent with
[Hermes Tweet](https://github.com/Xquik-dev/hermes-tweet), you may use it as a
native X/Twitter plugin for the discovery stage while keeping the ICP validation
stage unchanged.

Install it when needed:

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

With `XQUIK_API_KEY` configured, use:

- `tweet_explore` to scrape/search tweets and search Twitter/X for GTM, DevRel,
  growth, and startup hiring signals
- `tweet_read` to read tweet replies, look up users, and monitor tweets from
  promising companies or founders
- `tweet_action` only for read-side exports such as export followers in this
  discovery workflow

Convert the findings into the same candidate shape used by the pipeline, then
run the ICP checklist before ranking leads. Do not post tweets, post replies,
send DMs, or automate X actions without explicit human confirmation.

## Outputs

The script handles two primary JSON files:
1. `radar-jobs.json`: The initial raw batch of tech jobs identified by the scraper.
2. `openclaw-icp-jobs.json`: The **final validated file** OpenClaw should ingest, containing only companies that passed the strict web-search evaluation.

## References

For deeper context on how the evaluation works or modifying the pipeline, read these files as needed:

- **ICP Checklist**: See [references/icp-checklist.md](references/icp-checklist.md) for the exact strict evaluation criteria (Developer-first + $100K minimum funding).
- **Gemini Search Grounding**: The pipeline (`scripts/src/icp-filter.ts`) natively uses Google Search Grounding via the `@google/generative-ai` SDK (`gemini-3-flash-preview` / `gemini-flash-latest`) to look up live funding and product data.
