# vc-finder

Give the skill a product URL or description. It detects the industry and funding stage, identifies 5 comparable funded companies, searches who backed those companies (Track A), finds VCs who publish investment theses about this space (Track B), and returns a ranked sourced investor list with deep-dives and outreach hooks.

## Install

```bash
npx "@opendirectory.dev/skills" install vc-finder --target claude
```

### Step 1: Download the skill from GitHub
1. Click the **Code** button on this repo's GitHub page.
2. Select **Download ZIP** to download the repository.
3. Extract the ZIP file on your computer.

### Step 2: Install the Skill in Claude

<video src="https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c" controls width="100%"></video>

1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** (plus) icon button to create a new skill.
4. Choose the option to **Upload a skill**, and drag and drop the `.zip` file (or you can extract it and drop the folder, both work).

> **Note:** Make sure you are uploading the folder that contains the `SKILL.md` file!



### Step 3: Install in Manus AI

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.

## What It Does

- Fetches the product URL via Firecrawl (handles JS-rendered SPAs) or Tavily extract as fallback
- Detects funding stage from CTA signals on the page (waitlist, free trial, pricing, sales CTAs)
- Maps a 3-level industry taxonomy (L1 > L2 > L3) from the product page
- **Curated pre-match (Step 5b):** Scores product against a verified dataset of 25 VC funds (sourced from fund websites) -- instant zero-hallucination matches with no Tavily credits consumed
- **Discovers comparable companies:** Curated portfolio companies from matched funds + Tavily live search for L3-niche specifics
- Track A: 5 Tavily searches to find who invested in each comparable company
- Track B: 3 Tavily searches to find VCs who publish investment theses about this specific niche
- Synthesizes and ranks all found VCs -- curated matches labeled "verified", Tavily matches labeled by track
- Produces top 5 deep-dives with fund overview, portfolio evidence, how-to-approach, and outreach hook
- Generates 3 product-specific outreach hooks (not generic advice)
- Saves output to `docs/vc-intel/[product]-[date].md`

**Zero-hallucination guarantee:** Every VC name, fund detail, check size, portfolio company, and thesis source in the output must trace to either (a) the curated `data/vc_funds.json` dataset (sourced from fund websites) or (b) a specific Tavily search result. The AI does not draw from training knowledge for any factual claim.

## Requirements

| Requirement | Purpose | How to Set Up |
|---|---|---|
| Tavily API key | VC investment research (Track A and Track B) | app.tavily.com, free tier: 1000 credits/month |
| Firecrawl API key | Fetching JS-rendered product pages (optional) | firecrawl.dev, free tier: 500 credits/month |

Tavily is required. Firecrawl is recommended -- without it, Tavily extract is used as fallback (may miss JS-rendered content).

## Setup

```bash
cp .env.example .env
# Add TAVILY_API_KEY (required)
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
- Tavily: 10 searches at ~$0.01 each = ~$0.10 (2 comparable discovery + 5 Track A + 3 Track B)
- Curated pre-match (Step 5b): $0.00 -- local scoring against `data/vc_funds.json`, no API calls
- Total: ~$0.10 per run

## Project Structure

```
vc-finder/
├── SKILL.md
├── README.md
├── .env.example
├── data/
│   └── vc_funds.json          (25 verified funds, sourced from fund websites)
├── scripts/
│   └── match_funds.py         (standalone scoring script for testing)
├── evals/
│   └── evals.json
└── references/
    ├── stage-signals.md
    └── vc-outreach-guide.md
```

## License

MIT
