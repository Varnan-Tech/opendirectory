# vc-finder

Give the skill a product URL or description. It detects the industry and funding stage, identifies 5 comparable funded companies, searches who backed those companies (Track A), finds VCs who publish investment theses about this space (Track B), and returns a ranked sourced investor list with deep-dives and outreach hooks.

## Install

```bash
npx "@opendirectory.dev/skills" install vc-finder --target claude
```

### Video Tutorial
Watch this quick video to see how it's done:

https://github.com/user-attachments/assets/ee98a1b5-ebc4-452f-bbfb-c434f2935067

### Step 1: Download the skill from GitHub
1. Click the **Code** button on this repo's GitHub page.
2. Select **Download ZIP** to download the repository.
3. Extract the ZIP file on your computer.

### Step 2: Install the Skill in Claude
1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** (plus) icon button to create a new skill.
4. Choose the option to **Upload a skill**, and drag and drop the `.zip` file (or you can extract it and drop the folder, both work).

> **Note:** Make sure you are uploading the folder that contains the `SKILL.md` file!

## What It Does

- Fetches the product URL via Firecrawl (handles JS-rendered SPAs) or Tavily extract as fallback
- Detects funding stage from CTA signals on the page (waitlist, free trial, pricing, sales CTAs)
- Uses Gemini to map a 3-level industry taxonomy (L1 > L2 > L3) and identify 5 comparable funded companies
- Track A: 5 Tavily searches to find who invested in each comparable company
- Track B: 3 Tavily searches to find VCs who publish investment theses about this specific niche
- Gemini synthesizes and ranks all found VCs by stage fit and space fit (1-10 scores)
- Produces top 5 deep-dives with fund overview, portfolio evidence, how-to-approach, and outreach hook
- Generates 3 product-specific outreach hooks (not generic advice)
- Saves output to `docs/vc-intel/[product]-[date].md`

## Requirements

| Requirement | Purpose | How to Set Up |
|---|---|---|
| Gemini API key | Product analysis and VC synthesis | aistudio.google.com, Get API key |
| Tavily API key | VC investment research (Track A and Track B) | app.tavily.com, free tier: 1000 credits/month |
| Firecrawl API key | Fetching JS-rendered product pages | firecrawl.dev, free tier: 500 credits/month |

Gemini and Tavily are required. Firecrawl is recommended -- without it, Tavily extract is used as fallback (may miss JS-rendered content).

## Setup

```bash
cp .env.example .env
# Add GEMINI_API_KEY and TAVILY_API_KEY (required)
# Add FIRECRAWL_API_KEY (recommended)
```

## How to Use

```
"Find VCs for my startup: https://example.com"
"Who invests in developer tools at seed stage?"
"Build me a VC target list for https://example.com"
"Which funds should I pitch? https://example.com"
"Find investors for my product: [paste description]"
"Who backed companies like mine? https://example.com"
```

Or paste a product description directly if the URL is behind a login or returns no readable content.

## Why Two Tracks

**Track A (portfolio mapping):** VCs who already wrote a check in your space. These investors have proven they understand the category, the risks, and the buyer. They need less convincing than a generalist fund.

**Track B (thesis matching):** VCs who are actively publishing about your space. An investor who wrote a 2,000-word blog post about why they want to invest in CI/CD tooling is actively looking for deals. Your cold email lands in a much warmer inbox.

Generic "VCs in B2B SaaS" lists skip both signals. This skill produces only VCs with named evidence for each entry.

## Output

Each run produces:

1. **Product analysis**: detected industry taxonomy, stage, ICP, comparable companies used
2. **Track A table**: VCs who backed comparable companies (with evidence)
3. **Track B table**: VCs with published theses about this space (with source)
4. **Top 5 deep-dives**: fund overview, why it fits, portfolio in space, how to approach, outreach hook
5. **3 outreach hooks**: product-specific openers for cold outreach

## Cost per Run

- Firecrawl: ~$0.001 per fetch
- Tavily: 8 searches at ~$0.01 each = ~$0.08
- Gemini: 2 calls at ~$0.015 each = ~$0.03
- Total: ~$0.12 per run

## Project Structure

```
vc-finder/
├── SKILL.md
├── README.md
├── .env.example
├── evals/
│   └── evals.json
└── references/
    ├── stage-signals.md
    └── vc-outreach-guide.md
```

## License

MIT
