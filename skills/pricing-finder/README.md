# pricing-finder

Tell it what your product is (URL or description). It finds 5 competitors globally, fetches their actual pricing pages, and returns a complete pricing intelligence report: the dominant pricing model in your space, a benchmark price table, feature gate analysis, a competitive positioning map, and a concrete recommended pricing strategy for your product.

**Zero API keys required.** Runs entirely on free pip dependencies.

## Install

```bash
npx "@opendirectory.dev/skills" install pricing-finder --target claude
```

### Video Tutorial
Watch this quick video to see how it's done:

https://github.com/user-attachments/assets/ee98a1b5-ebc4-452f-bbfb-c434f2935067

### Step 1: Download the skill from GitHub
1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

### Step 2: Install the Skill in Claude
1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** (plus) icon button to create a new skill.
4. Choose the option to **Upload a skill**, and drag and drop the `.zip` file (or you can extract it and drop the folder, both work).

> **Note:** For some skills (like `position-me`), the `SKILL.md` file might be located inside a subfolder. Always make sure you are uploading the specific folder that contains the `SKILL.md` file!

## Setup

```bash
# Install free Python dependencies (required)
pip install ddgs requests beautifulsoup4 html2text
```

No API keys needed. Optionally add keys to `.env` for better quality:

```bash
cp .env.example .env
# Uncomment TAVILY_API_KEY or FIRECRAWL_API_KEY if you have them
```

## Usage

```
Find pricing benchmarks for my startup: https://yourstartup.com
```

Or paste a description if you don't have a live URL:

```
Find pricing benchmarks. We build [what you do] for [who]. [Stage], [geography].
```

## What It Does

1. Fetches your product page to understand what you're building
2. Analyzes your product: category, differentiators, ICP
3. Discovers 5 competitors in your space via DuckDuckGo search
4. **Asks you to confirm the competitor list** before fetching any data
5. Fetches each competitor's pricing page (3-tier fallback: direct fetch → Google cache → search snippet)
6. Extracts structured pricing data: tiers, prices, limits, feature gates
7. Analyzes patterns across all 5 competitors
8. Maps competitive positioning and identifies underserved gaps
9. Recommends a concrete pricing strategy for your product

## Output

A pricing intel report saved to `docs/pricing-intel/[product-slug]-[date].md` containing:

- **Pricing Model Analysis** -- dominant model in your space (per-seat / flat-rate / usage-based / freemium) and why
- **Price Point Benchmark Table** -- every competitor's tiers with exact prices, free tier, free trial
- **Market ranges** -- entry tier median, mid tier median, enterprise floor
- **Feature Gate Analysis** -- what's always free, what's always paid, what varies
- **Competitive Positioning Map** -- who owns cheap+simple, middle market, enterprise, and where the gap is
- **Recommended Pricing Strategy** -- model, entry price, mid price, top price, free tier decision, annual discount, what to gate behind paid

## Cost

**$0.00.** Entirely free using pip dependencies.

Optional API upgrades:
- Tavily API (free tier: 1000 credits/month) -- better search results
- Firecrawl API (free tier: 500 credits/month) -- better JS-heavy page rendering

## Zero-Hallucination Policy

Every price in the output traces to fetched pricing page content or a search snippet. "Contact Sales" is recorded exactly -- never estimated. Fields that could not be sourced are labeled "not found in page data." Low-quality data (search snippets) is explicitly flagged so you know which competitors to verify manually.

## How Pricing Page Fetching Works

The script tries three methods per competitor, in order:

1. **Direct fetch** (`requests` + `beautifulsoup4` + `html2text`) -- works for most pricing pages since companies make them SEO-friendly and server-rendered
2. **Google cache** -- fallback for recently-changed pages or soft blocks
3. **Search snippet** -- last resort; marks data quality as "low" in the output

If you have a Firecrawl API key, it replaces step 1 with a fully JS-rendered fetch.

## Project Structure

```
pricing-finder/
├── SKILL.md                        -- 10-step workflow for Claude Code
├── README.md                       -- this file
├── .env.example                    -- optional API key template
├── requirements.txt                -- free pip dependencies
├── scripts/
│   └── research.py                 -- two-phase data collector
├── evals/
│   └── evals.json                  -- 5 test cases
└── references/
    ├── pricing-models.md           -- per-seat, flat, usage, freemium definitions + signals
    ├── extraction-guide.md         -- how to read a pricing page
    └── positioning-guide.md        -- how to map competitors and find gaps
```

## Standalone Script Usage

```bash
# Phase 1: competitor discovery
python3 scripts/research.py \
    --phase discover \
    --product-analysis /tmp/pf-product-analysis.json \
    --output /tmp/pf-competitors-raw.json

# Phase 2: fetch pricing pages
python3 scripts/research.py \
    --phase fetch-pricing \
    --competitors /tmp/pf-competitors-confirmed.json \
    --output /tmp/pf-pricing-raw.json

# With optional API key upgrades
python3 scripts/research.py \
    --phase fetch-pricing \
    --competitors /tmp/pf-competitors-confirmed.json \
    --firecrawl-key "$FIRECRAWL_API_KEY" \
    --tavily-key "$TAVILY_API_KEY" \
    --output /tmp/pf-pricing-raw.json
```
