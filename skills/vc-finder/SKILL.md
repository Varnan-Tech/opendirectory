---
name: vc-finder
description: 'Takes a startup product URL or description, detects the industry and funding stage, identifies 5 comparable funded companies, searches who invested in those companies (Track A), finds VCs who publish investment theses about this space (Track B), and returns a ranked sourced list of relevant investors with deep-dives and outreach hooks. Use when asked to find investors for a startup, identify which VCs fund products like mine, research who backs companies in my space, build a VC target list, or find investor-market fit.'
compatibility: [claude-code, gemini-cli, github-copilot]
---

# VC Finder

Take a product URL or description. Detect industry and stage. Find 5 comparable funded companies. Run two research tracks: who invested in those comparables (Track A), and which VCs publish theses about this space (Track B). Return a sourced, ranked investor list with outreach hooks.

---

**Zero-hallucination policy:** Every fact in the output must be traceable to a specific Tavily search result or the fetched product page. This applies to:
- Comparable company names: must appear in Tavily search results, not AI training knowledge
- VC fund names: must appear verbatim in Tavily search results
- Check sizes, stage focus, portfolio companies: must come from search snippets, not AI knowledge
- Fund overviews and thesis summaries: extracted from search snippets only. If a detail is not in the search data, write "not found in search data" -- do not fill from training knowledge.

---

## Common Mistakes

| The agent will want to... | Why that's wrong |
|---|---|
| Add a16z or Sequoia because they are famous | A famous VC without evidence is noise. Only include VCs that appear in Tavily search results for this specific product. Name-dropping wastes the founder's time. |
| Generate comparable companies from training knowledge | Comparables must come from Tavily search results (Step 6). AI knowledge of companies is not evidence -- a company suggested from memory may have wrong funding status or may not be a true comparable. |
| Continue when all 5 Track A searches return 0 results | Zero Track A results means the comparables were wrong or too obscure. Stop, re-run Step 6 with broader search queries, and retry. |
| Include a Track B VC without citing the article or post | Thesis without a source is indistinguishable from hallucination. The founder cannot verify it and the list loses all credibility. |
| Fill in fund overview from training knowledge | Fund overviews must come from Tavily snippet text only. If the snippets don't describe the fund, write "not found in search data". |
| Detect stage from website aesthetics | Stage must come from the specific CTA signals detected in Step 4. |
| Write generic outreach hooks | Every outreach hook must name this specific product's differentiator and a specific VC portfolio signal or thesis quote from the search data. |
| Skip the URL fetch when the user also provides a description | Always fetch the URL. The live page often reveals stage signals that the user's description omits. |

---

## Step 1: Setup Check

```bash
echo "TAVILY_API_KEY:    ${TAVILY_API_KEY:+set}"
echo "FIRECRAWL_API_KEY: ${FIRECRAWL_API_KEY:-not set, Tavily extract will be used as fallback}"
```

**If TAVILY_API_KEY is missing:** Stop. Tell the user: "TAVILY_API_KEY is required to research VC investments and theses. There is no fallback for this. Get it at app.tavily.com -- free tier: 1000 credits/month (about 125 full runs). Add it to your .env file."

**If only FIRECRAWL_API_KEY is missing:** Continue silently. Tavily extract will be used for the URL fetch.

---

## Step 2: Gather Input

You need:
- Product URL (required, unless user pastes a product description directly)
- Optional: target stage hint (pre-seed, seed, series-a, series-b) -- if provided, use it and skip stage detection
- Optional: geography preference (US, Europe, global) -- defaults to US if not specified

**If the user provides only a pasted description (no URL):** Skip Steps 3-4. Go directly to Step 5 with the pasted text as `product_content`. Set `stage_source` to `user_description`.

**If neither URL nor description is provided:** Ask: "What is the URL of your product or startup? Or paste a short description: what it does, who it is for, and what stage you are at (pre-seed, seed, Series A)."

Derive product slug from URL for the output filename:

```bash
PRODUCT_SLUG=$(python3 -c "
from urllib.parse import urlparse
url = 'URL_HERE'
host = urlparse(url).netloc.replace('www.', '')
print(host.split('.')[0])
")
```

---

## Step 3: Fetch Product Page

**Primary: Firecrawl (if FIRECRAWL_API_KEY is set)**

```bash
curl -s -X POST https://api.firecrawl.dev/v1/scrape \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "URL_HERE", "formats": ["markdown"], "onlyMainContent": true}' \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
content = d.get('data', {}).get('markdown', '') or d.get('markdown', '')
print(f'Fetched: {len(content)} characters')
open('/tmp/vc-product-raw.md', 'w').write(content)
"
```

**Fallback: Tavily extract (if FIRECRAWL_API_KEY is not set)**

```bash
curl -s -X POST https://api.tavily.com/extract \
  -H "Content-Type: application/json" \
  -d "{\"api_key\": \"$TAVILY_API_KEY\", \"urls\": [\"URL_HERE\"]}" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
content = d.get('results', [{}])[0].get('raw_content', '')
print(f'Fetched via Tavily extract: {len(content)} characters')
open('/tmp/vc-product-raw.md', 'w').write(content)
"
```

**Step-level checkpoint:**

```bash
python3 -c "
content = open('/tmp/vc-product-raw.md').read()
if len(content) < 200:
    print('ERROR: Page returned fewer than 200 characters.')
else:
    print(f'Content OK: {len(content)} characters')
"
```

**If content < 200 characters:** Stop fetching. Tell the user: "The product page returned no readable content. This usually means the site is JavaScript-rendered and requires a browser. Please paste your product description directly: what it does, who it is for, and what stage you are at."

Proceed to Step 5 using the pasted description as `product_content`.

---

## Step 4: Detect Stage Signals Locally (No API)

Parse the fetched markdown with regex before the analysis step.

```bash
python3 << 'PYEOF'
import re, json

content = open('/tmp/vc-product-raw.md').read().lower()
stage_signals = []

if re.search(r'join\s+(the\s+)?waitlist|sign\s+up\s+for\s+beta|early\s+access|request\s+(an?\s+)?invite|get\s+notified', content):
    stage_signals.append({'signal': 'waitlist or beta CTA', 'stage_hint': 'pre-seed'})

if re.search(r'start\s+(your\s+)?free\s+trial|try\s+(it\s+)?for\s+free|request\s+a?\s+demo|book\s+a?\s+demo|schedule\s+a?\s+demo', content):
    stage_signals.append({'signal': 'free trial or demo CTA', 'stage_hint': 'seed'})

if re.search(r'contact\s+sales|talk\s+to\s+(our\s+)?sales|see\s+pricing|view\s+pricing|plans\s+and\s+pricing', content):
    stage_signals.append({'signal': 'pricing or sales CTA', 'stage_hint': 'series-a'})
if re.search(r'case\s+stud(y|ies)|customer\s+stor(y|ies)|trusted\s+by\s+[\d,]+|used\s+by\s+[\d,]+', content):
    stage_signals.append({'signal': 'case studies or customer count', 'stage_hint': 'series-a'})

if re.search(r'enterprise\s+(plan|pricing|tier)|we.?re\s+hiring|join\s+our\s+team|open\s+positions', content):
    stage_signals.append({'signal': 'enterprise tier or job openings', 'stage_hint': 'series-a-or-b'})

funding_match = re.search(
    r'raised\s+\$[\d,.]+\s*[mk]?|series\s+[abc]\s+round|seed\s+round|(\$[\d,.]+\s*[mk]?\s+(?:seed|series\s+[abc]))',
    content
)
if funding_match:
    stage_signals.append({'signal': f'funding text: {funding_match.group(0).strip()}', 'stage_hint': 'announced'})

if not stage_signals:
    dominant = 'unknown'
elif any(s['stage_hint'] == 'announced' for s in stage_signals):
    dominant = 'announced'
elif any(s['stage_hint'] == 'series-a-or-b' for s in stage_signals):
    dominant = 'series-a'
elif any(s['stage_hint'] == 'series-a' for s in stage_signals):
    dominant = 'series-a'
elif any(s['stage_hint'] == 'seed' for s in stage_signals):
    dominant = 'seed'
else:
    dominant = 'pre-seed'

confidence = 'high' if len(stage_signals) >= 2 else ('medium' if len(stage_signals) == 1 else 'low')

result = {'signals': stage_signals, 'dominant_stage': dominant, 'confidence': confidence}
json.dump(result, open('/tmp/vc-stage-signals.json', 'w'), indent=2)
print(f'Stage: {dominant} ({confidence} confidence) from {len(stage_signals)} signal(s)')
for s in stage_signals:
    print(f'  - {s["signal"]} -> {s["stage_hint"]}')
PYEOF
```

---

## Step 5: Product Analysis (Taxonomy, Stage, ICP)

Print the product content and stage signals:

```bash
python3 -c "
import json
content = open('/tmp/vc-product-raw.md').read()[:6000]
signals = json.load(open('/tmp/vc-stage-signals.json'))
print('=== PRODUCT PAGE (first 6000 chars) ===')
print(content)
print()
print('=== DETECTED STAGE SIGNALS ===')
print(json.dumps(signals, indent=2))
"
```

**AI instructions:** Analyze the product page content above. Generate the taxonomy, ICP, and stage classification only -- do NOT generate comparable companies yet (that is done via live search in Step 6).

Write to `/tmp/vc-product-analysis.json`:

- `product_name`: from the page
- `one_line_description`: what it does, for whom, core value prop. Under 20 words. No marketing language.
- `industry_taxonomy`: `l1` (top-level: fintech / healthtech / developer tools / consumer / etc.), `l2` (sector: sales technology / logistics software / etc.), `l3` (specific niche: outbound prospecting / last-mile routing / etc.). Vague labels like "technology" or "software" alone are not acceptable.
- `icp`: `buyer_persona` (job title), `company_type`, `company_size`
- `detected_stage`: pre-seed / seed / series-a / series-b / unknown
- `stage_confidence`: high / medium / low
- `stage_evidence`: one sentence citing exactly which CTA or text on the page drove this. Write "no clear signals found" if unknown.
- `geography_bias`: US / Europe / global / unclear
- `comparable_companies`: leave as empty array `[]` -- will be filled in Step 6

```bash
python3 << 'PYEOF'
import json

analysis = {
    # FILL from your analysis above
    "comparable_companies": []
}

json.dump(analysis, open('/tmp/vc-product-analysis.json', 'w'), indent=2)
print('Product analysis written.')
PYEOF
```

Verify:

```bash
python3 -c "
import json
a = json.load(open('/tmp/vc-product-analysis.json'))
print('Product:', a['product_name'])
print('Industry:', a['industry_taxonomy']['l1'], '>', a['industry_taxonomy']['l2'], '>', a['industry_taxonomy']['l3'])
print('Stage:', a['detected_stage'], '(' + a['stage_confidence'] + ' confidence)')
"
```

---

## Step 5b: Curated Pre-Match Against Verified Fund Dataset

Run the product taxonomy against a curated dataset of 25 verified VC funds (sourced from fund websites). Produces zero-hallucination fund matches and seed comparables for Track A -- no Tavily credits consumed.

Print product analysis for tag mapping:

```bash
python3 -c "
import json
a = json.load(open('/tmp/vc-product-analysis.json'))
print('Taxonomy:', a['industry_taxonomy']['l1'], '>', a['industry_taxonomy']['l2'], '>', a['industry_taxonomy']['l3'])
print('Stage:', a['detected_stage'])
print('Geography:', a['geography_bias'])
"
```

**AI instructions:** Map the product taxonomy to the standard tags used in the fund dataset. Available tags:
`DevTools`, `Infrastructure`, `Open Source`, `B2B SaaS`, `AI`, `Data`, `FinTech`, `HealthTech`, `Enterprise`, `Consumer`, `Marketplaces`, `E-commerce`, `Crypto`, `DeepTech`, `Cybersecurity`, `Generalist`

Pick 2-4 tags that describe this product. Map `detected_stage` to: `Pre-seed`, `Seed`, `Series A`, or `Growth`. Map `geography_bias` to: `US`, `Europe`, `India`, or `Global`.

Write product context:

```bash
python3 << 'PYEOF'
import json

# FILL based on taxonomy analysis above
context = {
    "extracted_tags": ["TagA", "TagB"],  # 2-4 tags from the list above
    "stage_hint": "Seed",               # Pre-seed / Seed / Series A / Growth
    "geography_hint": "US"              # US / Europe / India / Global
}
json.dump(context, open('/tmp/vc-product-context.json', 'w'), indent=2)
print('Product context:', context)
PYEOF
```

Run scoring against the embedded curated dataset:

```bash
python3 << 'PYEOF'
import json

context = json.load(open('/tmp/vc-product-context.json'))

VC_FUNDS = [
  {"fund_name":"Y Combinator","thesis":"We provide seed funding for startups. We invest in deeply technical teams building massive companies across all domains.","check_size":"$500k","stage_focus":["Pre-seed","Seed"],"industry_tags":["Generalist","B2B SaaS","DevTools","AI"],"geography_focus":["Global"],"notable_portfolio":["Stripe","Airbnb","GitLab"],"website":"https://www.ycombinator.com"},
  {"fund_name":"boldstart ventures","thesis":"Day one partner for developer first, crypto, and SaaS founders. We love deeply technical founders solving hard infrastructure problems.","check_size":"$1M - $3M","stage_focus":["Pre-seed","Seed"],"industry_tags":["DevTools","Infrastructure","Crypto"],"geography_focus":["Global","US"],"notable_portfolio":["Snyk","Blockdaemon","Superhuman"],"website":"https://boldstart.vc"},
  {"fund_name":"Heavybit","thesis":"The leading investor in developer-first startups. We help technical founders launch, gain traction, and build enterprise-ready companies.","check_size":"$1M - $5M","stage_focus":["Seed","Series A"],"industry_tags":["DevTools","Infrastructure","Open Source"],"geography_focus":["Global","US"],"notable_portfolio":["PagerDuty","Sanity","Netlify"],"website":"https://www.heavybit.com"},
  {"fund_name":"Amplify Partners","thesis":"We invest in technical founders building the next generation of IT infrastructure, developer tools, and data platforms.","check_size":"$2M - $8M","stage_focus":["Seed","Series A"],"industry_tags":["DevTools","Infrastructure","AI","Data"],"geography_focus":["US"],"notable_portfolio":["Datadog","OCTO","dbt Labs"],"website":"https://www.amplifypartners.com"},
  {"fund_name":"OSS Capital","thesis":"We exclusively back early-stage founders building Commercial Open Source Software (COSS) companies.","check_size":"$500k - $2M","stage_focus":["Pre-seed","Seed","Series A"],"industry_tags":["Open Source","DevTools"],"geography_focus":["Global"],"notable_portfolio":["Cal.com","Appsmith","Hoppscotch"],"website":"https://oss.capital"},
  {"fund_name":"Sequoia Capital","thesis":"We help the daring build legendary companies, from idea to IPO and beyond. Sequoia is an early-stage and growth-stage investor.","check_size":"$1M - $10M+","stage_focus":["Seed","Series A","Growth"],"industry_tags":["Generalist","Enterprise","Consumer","AI"],"geography_focus":["Global"],"notable_portfolio":["Apple","Google","WhatsApp"],"website":"https://www.sequoiacap.com"},
  {"fund_name":"Andreessen Horowitz (a16z)","thesis":"We invest in software eating the world. We back bold entrepreneurs building the future through technology.","check_size":"$1M - $50M+","stage_focus":["Seed","Series A","Growth"],"industry_tags":["Generalist","Crypto","Enterprise","Consumer","AI"],"geography_focus":["Global","US"],"notable_portfolio":["Facebook","Coinbase","Figma"],"website":"https://a16z.com"},
  {"fund_name":"Point Nine Capital","thesis":"We are a seed-stage venture capital firm focused on B2B SaaS and B2B marketplaces globally.","check_size":"$1M - $3M","stage_focus":["Seed"],"industry_tags":["B2B SaaS","Marketplaces"],"geography_focus":["Europe","Global"],"notable_portfolio":["Zendesk","Typeform","Docplanner"],"website":"https://www.pointnine.com"},
  {"fund_name":"Cherry Ventures","thesis":"We champion founders in Europe from their earliest days. We are generalist seed investors.","check_size":"$1M - $4M","stage_focus":["Pre-seed","Seed"],"industry_tags":["Generalist","Consumer","B2B SaaS"],"geography_focus":["Europe"],"notable_portfolio":["FlixBus","Auto1 Group","Forto"],"website":"https://www.cherry.vc"},
  {"fund_name":"First Round Capital","thesis":"We are the seed-stage firm that builds the most supportive community for founders.","check_size":"$1M - $4M","stage_focus":["Pre-seed","Seed"],"industry_tags":["Generalist","B2B SaaS","Consumer"],"geography_focus":["US"],"notable_portfolio":["Uber","Notion","Roblox"],"website":"https://firstround.com"},
  {"fund_name":"Bessemer Venture Partners","thesis":"BVP helps entrepreneurs lay strong foundations to build and forge long-standing companies.","check_size":"$1M - $20M+","stage_focus":["Seed","Series A","Growth"],"industry_tags":["Generalist","Enterprise","Consumer","FinTech"],"geography_focus":["Global"],"notable_portfolio":["LinkedIn","Twilio","Shopify"],"website":"https://www.bvp.com"},
  {"fund_name":"Index Ventures","thesis":"We back the best and most ambitious entrepreneurs across all stages to build category-defining businesses.","check_size":"$1M - $20M+","stage_focus":["Seed","Series A","Growth"],"industry_tags":["Generalist","FinTech","Consumer","B2B SaaS"],"geography_focus":["Europe","US","Global"],"notable_portfolio":["Dropbox","Slack","Figma"],"website":"https://www.indexventures.com"},
  {"fund_name":"Lightspeed Venture Partners","thesis":"We invest globally in enterprise, consumer, and health founders who are shaping the future.","check_size":"$1M - $25M+","stage_focus":["Seed","Series A","Growth"],"industry_tags":["Generalist","Enterprise","Consumer","FinTech"],"geography_focus":["Global"],"notable_portfolio":["Snap","Rippling","MuleSoft"],"website":"https://lsvp.com"},
  {"fund_name":"Accel","thesis":"We partner with exceptional founders from inception through all phases of private company growth.","check_size":"$1M - $20M+","stage_focus":["Seed","Series A","Growth"],"industry_tags":["Generalist","B2B SaaS","Consumer","DevTools"],"geography_focus":["Global"],"notable_portfolio":["Facebook","Atlassian","Spotify"],"website":"https://www.accel.com"},
  {"fund_name":"Bain Capital Ventures","thesis":"From seed to growth, we back founders building legendary infrastructure, fintech, application, and commerce companies.","check_size":"$1M - $50M+","stage_focus":["Seed","Series A","Growth"],"industry_tags":["Generalist","Infrastructure","FinTech","B2B SaaS"],"geography_focus":["US","Global"],"notable_portfolio":["DocuSign","SendGrid","Redis"],"website":"https://www.baincapitalventures.com"},
  {"fund_name":"Greylock Partners","thesis":"We partner with early-stage founders to build enterprise and consumer software companies that define new categories.","check_size":"$1M - $10M","stage_focus":["Seed","Series A"],"industry_tags":["Enterprise","Consumer","Cybersecurity","AI"],"geography_focus":["US"],"notable_portfolio":["Workday","Palo Alto Networks","LinkedIn"],"website":"https://greylock.com"},
  {"fund_name":"Unusual Ventures","thesis":"We provide a breakthrough level of support for early-stage founders building enterprise tech.","check_size":"$1M - $5M","stage_focus":["Pre-seed","Seed"],"industry_tags":["Enterprise","DevTools","B2B SaaS"],"geography_focus":["US"],"notable_portfolio":["Arctic Wolf","Harness","Vivun"],"website":"https://www.unusual.vc"},
  {"fund_name":"Crane Venture Partners","thesis":"We back deep tech and enterprise founders in Europe solving hard problems with data and code.","check_size":"$1M - $4M","stage_focus":["Seed"],"industry_tags":["Enterprise","DeepTech","Data","AI"],"geography_focus":["Europe"],"notable_portfolio":["Onfido","Tessian","Forto"],"website":"https://crane.vc"},
  {"fund_name":"Founder Collective","thesis":"We are a seed-stage venture capital fund, built by founders, for founders. We back weird, wonderful, and wild startups.","check_size":"$500k - $2M","stage_focus":["Seed"],"industry_tags":["Generalist","Consumer","B2B SaaS"],"geography_focus":["US","Global"],"notable_portfolio":["Uber","Airtable","BuzzFeed"],"website":"https://www.foundercollective.com"},
  {"fund_name":"Benchmark","thesis":"We are a partnership of equal partners. We back mission-driven founders at the earliest stages and walk beside them for the long haul.","check_size":"$1M - $10M","stage_focus":["Seed","Series A"],"industry_tags":["Generalist","Marketplaces","Enterprise","Consumer"],"geography_focus":["US","Global"],"notable_portfolio":["Uber","Twitter","eBay","Snapchat"],"website":"https://www.benchmark.com"},
  {"fund_name":"Accel India","thesis":"We partner with exceptional founders from inception through all phases of private company growth in the Indian ecosystem.","check_size":"$1M - $15M","stage_focus":["Seed","Series A","Growth"],"industry_tags":["Generalist","B2B SaaS","Consumer","FinTech","E-commerce"],"geography_focus":["India"],"notable_portfolio":["Flipkart","Swiggy","Freshworks"],"website":"https://www.accel.com/india"},
  {"fund_name":"Blume Ventures","thesis":"We are a seed and pre-seed venture fund that backs startups with both funding and active mentoring.","check_size":"$500k - $3M","stage_focus":["Pre-seed","Seed"],"industry_tags":["Generalist","B2B SaaS","Consumer","DeepTech","HealthTech"],"geography_focus":["India"],"notable_portfolio":["Unacademy","Purplle","GreyOrange"],"website":"https://blume.vc"},
  {"fund_name":"Elevation Capital","thesis":"We partner with visionary founders in India across early stages to help them build category-defining businesses.","check_size":"$1M - $10M","stage_focus":["Seed","Series A"],"industry_tags":["Generalist","Consumer","FinTech","B2B SaaS","HealthTech"],"geography_focus":["India"],"notable_portfolio":["Paytm","Swiggy","Meesho"],"website":"https://elevationcapital.com"},
  {"fund_name":"Peak XV Partners","thesis":"Formerly Sequoia India & SEA, we partner with founders across early, growth, and public stages to build enduring companies.","check_size":"$1M - $20M+","stage_focus":["Seed","Series A","Growth"],"industry_tags":["Generalist","Consumer","FinTech","B2B SaaS","DevTools","AI"],"geography_focus":["India","South Asia"],"notable_portfolio":["Zomato","Pine Labs","Cred"],"website":"https://www.peakxv.com"},
  {"fund_name":"Nexus Venture Partners","thesis":"We are a US-India venture capital firm backing extraordinary founders building product-first companies.","check_size":"$1M - $10M","stage_focus":["Seed","Series A"],"industry_tags":["B2B SaaS","Enterprise","DevTools","Consumer"],"geography_focus":["India","US"],"notable_portfolio":["Postman","Hasura","Zepto"],"website":"https://nexusvp.com"}
]

STAGE_ORDER = {"Pre-seed": 0, "Seed": 1, "Series A": 2, "Growth": 3}

def score_fund(fund, ctx):
    score = 0
    fund_tags = fund.get("industry_tags", [])
    extracted_tags = ctx.get("extracted_tags", ["Generalist"])
    tag_points = 0
    matched_tags = []
    for tag in extracted_tags:
        if tag in fund_tags:
            tag_points += 5 if tag == "Generalist" else 20
            matched_tags.append(tag)
    tag_points = min(tag_points, 60)
    score += tag_points
    stage_hint = ctx.get("stage_hint")
    fund_stages = fund.get("stage_focus", [])
    if not stage_hint:
        score += 10
    elif fund_stages:
        if stage_hint in fund_stages:
            score += 20
        elif stage_hint in STAGE_ORDER:
            hint_idx = STAGE_ORDER[stage_hint]
            if any(f in STAGE_ORDER and abs(STAGE_ORDER[f] - hint_idx) == 1 for f in fund_stages):
                score += 10
    geo_hint = ctx.get("geography_hint")
    fund_geo = fund.get("geography_focus", ["Global"])
    if not geo_hint or geo_hint == "Global":
        score += 10
    elif fund_geo == ["India"] and geo_hint == "US":
        pass
    elif geo_hint in fund_geo:
        score += 20
    elif "Global" in fund_geo:
        score += 15
    if geo_hint == "US" and "India" in fund_geo and "US" not in fund_geo and "Global" not in fund_geo:
        score = max(0, score - 30)
    if fund_tags and extracted_tags and fund_tags[0] not in extracted_tags and tag_points <= 20:
        score = max(0, score - 15)
    return score, matched_tags

scored = []
for fund in VC_FUNDS:
    score, matched_tags = score_fund(fund, context)
    tier = "High" if score >= 70 else ("Medium" if score >= 40 else "Low")
    scored.append({
        "fund_name": fund["fund_name"],
        "thesis": fund["thesis"],
        "check_size": fund["check_size"],
        "stage_focus": fund["stage_focus"],
        "industry_tags": fund["industry_tags"],
        "geography_focus": fund["geography_focus"],
        "notable_portfolio": fund["notable_portfolio"],
        "website": fund["website"],
        "source": "verified (fund website)",
        "score": score,
        "confidence": tier,
        "matched_tags": matched_tags
    })

scored.sort(key=lambda x: (-x["score"], x["fund_name"]))
relevant = [m for m in scored if m["confidence"] in ("High", "Medium")]

curated_comparables = []
for m in relevant:
    for company in m.get("notable_portfolio", []):
        if company not in curated_comparables:
            curated_comparables.append(company)

output = {
    "high_medium_matches": relevant,
    "curated_comparables": curated_comparables[:6]
}
json.dump(output, open('/tmp/vc-curated-matches.json', 'w'), indent=2)
print(f'Curated matches: {len(relevant)} High/Medium confidence funds')
for m in relevant[:8]:
    print(f'  {m["confidence"]:6} ({m["score"]:3}) {m["fund_name"]}')
print(f'Seed comparables from portfolio: {curated_comparables[:6]}')
PYEOF
```

---

## Step 6: Discover Comparable Companies via Tavily

Load curated portfolio companies from Step 5b as seed comparables:

```bash
python3 -c "
import json
matches = json.load(open('/tmp/vc-curated-matches.json'))
curated = matches.get('curated_comparables', [])
print(f'Curated portfolio comparables ({len(curated)}): {curated}')
need = max(0, 5 - len(curated))
print(f'Tavily will supplement with up to {need} more')
"
```

**Do not use AI training knowledge to generate comparable companies.** Curated portfolio companies (above) are already zero-hallucination comparables from verified fund data. Tavily supplements with L3-niche-specific companies.

```bash
python3 << 'PYEOF'
import json, os, urllib.request

analysis = json.load(open('/tmp/vc-product-analysis.json'))
l2 = analysis['industry_taxonomy']['l2']
l3 = analysis['industry_taxonomy']['l3']
tavily_key = os.environ.get('TAVILY_API_KEY', '')

queries = [
    f'"{l3}" startup raised funding venture capital seed series',
    f'"{l2}" companies venture backed funded startup'
]

all_results = []
for query in queries:
    payload = json.dumps({
        "api_key": tavily_key,
        "query": query,
        "search_depth": "advanced",
        "max_results": 8,
        "include_answer": True
    }).encode()

    req = urllib.request.Request(
        'https://api.tavily.com/search',
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            all_results.append({
                'query': query,
                'answer': result.get('answer', ''),
                'results': [
                    {'title': r.get('title',''), 'url': r.get('url',''), 'content': r.get('content','')[:500]}
                    for r in result.get('results', [])
                ]
            })
            print(f'Comparable search: {len(result.get("results", []))} results for "{query[:60]}"')
    except Exception as e:
        print(f'Comparable search FAILED: {e}')
        all_results.append({'query': query, 'answer': '', 'results': [], 'error': str(e)})

json.dump(all_results, open('/tmp/vc-comparable-search.json', 'w'), indent=2)
PYEOF
```

Print results for AI selection:

```bash
python3 -c "
import json
results = json.load(open('/tmp/vc-comparable-search.json'))
for r in results:
    print(f'Query: {r[\"query\"]}')
    print(f'Answer: {r.get(\"answer\",\"\")[:400]}')
    for item in r.get('results', []):
        print(f'  - {item[\"title\"]} | {item[\"url\"]}')
        print(f'    {item[\"content\"][:200]}')
    print()
"
```

**AI instructions:** Combine the curated portfolio companies from `/tmp/vc-curated-matches.json` with the Tavily search results above. Pick exactly 5 comparable companies. Prioritize curated portfolio companies (already verified -- they are real portfolio companies of matched VC funds). Supplement with Tavily-discovered companies to reach 5 if needed.

For each comparable write:
- `name`: company name
- `similarity_reason`: one sentence explaining the fit (for curated: reference the fund that backed them; for Tavily: cite the snippet)
- `source_url`: portfolio fund website for curated companies, Tavily result URL for discovered ones
- `estimated_stage`: from curated data or snippet text -- write "not in search data" if unknown
- `source_type`: `"curated_portfolio"` or `"tavily_discovered"`

Update `/tmp/vc-product-analysis.json` with the `comparable_companies` array:

```bash
python3 << 'PYEOF'
import json

analysis = json.load(open('/tmp/vc-product-analysis.json'))

analysis['comparable_companies'] = [
    # FILL 5 companies -- curated_portfolio first, then tavily_discovered
    # Each: {"name": str, "similarity_reason": str, "source_url": str, "estimated_stage": str, "source_type": str}
]

json.dump(analysis, open('/tmp/vc-product-analysis.json', 'w'), indent=2)
print('Comparables written:', ', '.join(c['name'] for c in analysis['comparable_companies']))
PYEOF
```

**If fewer than 3 comparable companies appear in the search results:** Broaden the queries. Run a third search: `"[l1] startup" funding round venture capital`. If still thin, proceed with what is available and flag in `data_quality_flags`.

---

## Step 7: Track A -- Who Invested in Comparable Companies

Run 5 Tavily searches, one per comparable.

```bash
python3 << 'PYEOF'
import json, os, urllib.request

analysis = json.load(open('/tmp/vc-product-analysis.json'))
comparables = analysis['comparable_companies']
tavily_key = os.environ.get('TAVILY_API_KEY', '')
all_track_a = []

for comp in comparables:
    company = comp['name']
    query = f'"{company}" investors funding venture capital backed seed series'

    payload = json.dumps({
        "api_key": tavily_key,
        "query": query,
        "search_depth": "advanced",
        "max_results": 5,
        "include_answer": True
    }).encode()

    req = urllib.request.Request(
        'https://api.tavily.com/search',
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            all_track_a.append({
                'comparable_company': company,
                'similarity_reason': comp['similarity_reason'],
                'query': query,
                'answer': result.get('answer', ''),
                'results': result.get('results', [])
            })
            print(f'Track A - {company}: {len(result.get("results", []))} results')
    except Exception as e:
        print(f'Track A - {company}: FAILED ({e})')
        all_track_a.append({
            'comparable_company': company,
            'similarity_reason': comp['similarity_reason'],
            'query': query,
            'answer': '',
            'results': [],
            'error': str(e)
        })

json.dump(all_track_a, open('/tmp/vc-tracka-results.json', 'w'), indent=2)
print(f'Track A complete. Comparables with results: {sum(1 for r in all_track_a if r.get("results"))}')
PYEOF
```

**If all 5 Track A searches return 0 results:** Re-run Step 6 with broader queries. Retry with well-covered companies (those with significant press coverage). If still 0: proceed to Track B only and flag in `data_quality_flags`.

---

## Step 8: Track B -- VCs With Investment Theses About This Space

Run 3 Tavily searches using L2 and L3 taxonomy from Step 5.

```bash
python3 << 'PYEOF'
import json, os, urllib.request

analysis = json.load(open('/tmp/vc-product-analysis.json'))
l2 = analysis['industry_taxonomy']['l2']
l3 = analysis['industry_taxonomy']['l3']
stage = analysis['detected_stage']
tavily_key = os.environ.get('TAVILY_API_KEY', '')

queries = [
    {'name': 'thesis_l3', 'query': f'venture capital investment thesis "{l3}" investing 2023 OR 2024 OR 2025'},
    {'name': 'thesis_l2', 'query': f'VC fund "{l2}" investment thesis portfolio companies'},
    {'name': 'stage_space', 'query': f'{stage} investors "{l3}" startup venture capital fund'}
]

all_track_b = []

for q in queries:
    payload = json.dumps({
        "api_key": tavily_key,
        "query": q['query'],
        "search_depth": "advanced",
        "max_results": 7,
        "include_answer": True
    }).encode()

    req = urllib.request.Request(
        'https://api.tavily.com/search',
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            all_track_b.append({
                'query_name': q['name'],
                'query': q['query'],
                'answer': result.get('answer', ''),
                'results': result.get('results', [])
            })
            print(f"Track B - {q['name']}: {len(result.get('results', []))} results")
    except Exception as e:
        print(f"Track B - {q['name']}: FAILED ({e})")
        all_track_b.append({'query_name': q['name'], 'query': q['query'], 'answer': '', 'results': [], 'error': str(e)})

json.dump(all_track_b, open('/tmp/vc-trackb-results.json', 'w'), indent=2)
PYEOF
```

**If all 3 Track B searches return 0 results:** Proceed with Track A results only. Note in `data_quality_flags`: "No thesis-led investors found via public search."

---

## Step 9: Synthesize -- Rank and Score All VCs

Print the research data:

```bash
python3 -c "
import json

analysis = json.load(open('/tmp/vc-product-analysis.json'))
track_a = json.load(open('/tmp/vc-tracka-results.json'))
track_b = json.load(open('/tmp/vc-trackb-results.json'))
curated = json.load(open('/tmp/vc-curated-matches.json'))

track_a_summary = []
for item in track_a:
    snippets = [{'title': r.get('title',''), 'url': r.get('url',''), 'content': r.get('content','')[:400]}
                for r in item.get('results', [])[:3]]
    track_a_summary.append({
        'comparable_company': item['comparable_company'],
        'similarity_reason': item['similarity_reason'],
        'answer': item.get('answer', '')[:500],
        'top_results': snippets
    })

track_b_summary = []
for item in track_b:
    snippets = [{'title': r.get('title',''), 'url': r.get('url',''), 'content': r.get('content','')[:400]}
                for r in item.get('results', [])[:4]]
    track_b_summary.append({
        'query_name': item['query_name'],
        'answer': item.get('answer', '')[:500],
        'top_results': snippets
    })

curated_summary = []
for m in curated.get('high_medium_matches', []):
    curated_summary.append({
        'fund_name': m['fund_name'],
        'confidence': m['confidence'],
        'score': m['score'],
        'matched_tags': m['matched_tags'],
        'thesis': m['thesis'],
        'check_size': m['check_size'],
        'stage_focus': m['stage_focus'],
        'notable_portfolio': m['notable_portfolio'],
        'website': m['website'],
        'source': 'verified (fund website)'
    })

print(json.dumps({
    'product': {
        'name': analysis['product_name'],
        'description': analysis['one_line_description'],
        'industry': analysis['industry_taxonomy'],
        'icp': analysis['icp'],
        'stage': analysis['detected_stage'],
        'stage_confidence': analysis['stage_confidence'],
        'geography': analysis['geography_bias']
    },
    'curated_matches': curated_summary,
    'track_a_research': track_a_summary,
    'track_b_research': track_b_summary
}, indent=2))
"
```

**AI instructions -- zero-hallucination rules:**

Every field in the output must be traceable to the printed data above. Rules:

1. **curated_vcs:** Use the `curated_matches` data directly. These are pre-verified -- no Tavily evidence required. `fund_overview` comes from the `thesis` field in the curated data. `check_size` and `stage_focus` come from the curated data fields. Do NOT fill from training knowledge even for these funds.
2. **VC names (Track A / B):** Only include a fund if its name appears verbatim in the snippet text or title. No exceptions.
3. **evidence_company (Track A):** The comparable company they backed -- must be stated in the snippet text, not inferred.
4. **thesis_source_title (Track B):** The exact title of the article or post as it appears in the search results.
5. **fund_overview (Track A / B):** Extract from snippet text only. Max 2 sentences. If the snippets do not describe the fund, write "not found in search data".
6. **thesis_summary:** Close paraphrase of the snippet text. Do not add context from training knowledge.
7. **check_size (Track A / B):** From snippet data only. Write "not in search data" if not mentioned.
8. **portfolio_in_space:** Only companies that appear in the search snippets. Write "not found in search data" if none.
9. **stage_fit_score 1-10:** Penalize 3 points if the VC's stated stage does not match the product's detected stage.
10. **space_fit_score 1-10:** 9-10 only if the VC backed 2+ companies in the L3 niche per the snippets or curated data.
11. **approach_method:** one of -- cold email / warm intro required / AngelList / application form / Twitter/X DM. Infer from snippets or fund website.
12. **outreach_hook:** Must name a specific portfolio signal or thesis quote. Generic hooks like "highlight your traction" are not acceptable.
13. No em dashes. No marketing language.

Write to `/tmp/vc-final-list.json`:

- `product_summary`: name, one_line_description, industry_l1, industry_l2, industry_l3, detected_stage, comparable_companies_used (names only)
- `curated_vcs`: fund_name, confidence ("High"/"Medium"), matched_tags, fund_overview (from thesis field), check_size, stage_focus, website, source ("verified (fund website)"), stage_fit_score, space_fit_score
- `track_a_vcs`: fund_name, evidence_company (REQUIRED), evidence_source_url, stage_focus, check_size, fund_overview, thesis_summary, stage_fit_score, space_fit_score, approach_method
- `track_b_vcs`: fund_name, thesis_source_title (REQUIRED), thesis_source_url, stage_focus, check_size, fund_overview, thesis_summary, stage_fit_score, space_fit_score, approach_method
- `top_5_deep_dives`: fund_name, track ("Curated"/"A"/"B"), fund_overview, why_fit, portfolio_in_space, how_to_approach (min 30 chars), outreach_hook
- `outreach_hooks`: 3 objects -- hook_type, hook_text (2-3 sentences), best_for
- `data_quality_flags`: gaps, missing fields, low-confidence areas

```bash
python3 << 'PYEOF'
import json

result = {
    # FILL from synthesis above
    # Must include: product_summary, curated_vcs, track_a_vcs, track_b_vcs, top_5_deep_dives, outreach_hooks, data_quality_flags
}

json.dump(result, open('/tmp/vc-final-list.json', 'w'), indent=2)
print(f'Synthesis written. Curated: {len(result.get("curated_vcs", []))} VCs. Track A: {len(result.get("track_a_vcs", []))} VCs. Track B: {len(result.get("track_b_vcs", []))} VCs.')
PYEOF
```

---

## Step 10: Self-QA

```bash
python3 << 'PYEOF'
import json

result = json.load(open('/tmp/vc-final-list.json'))
failures = []

# Remove Track A VCs missing evidence_company
original_a = len(result.get('track_a_vcs', []))
result['track_a_vcs'] = [v for v in result.get('track_a_vcs', []) if v.get('evidence_company')]
removed_a = original_a - len(result['track_a_vcs'])
if removed_a > 0:
    failures.append(f'Removed {removed_a} Track A VC(s) missing evidence_company')

# Remove Track B VCs missing thesis_source_title
original_b = len(result.get('track_b_vcs', []))
result['track_b_vcs'] = [v for v in result.get('track_b_vcs', []) if v.get('thesis_source_title')]
removed_b = original_b - len(result['track_b_vcs'])
if removed_b > 0:
    failures.append(f'Removed {removed_b} Track B VC(s) missing thesis_source_title')

# Remove deep dives for VCs that were stripped from all tracks
valid_funds = (
    {v['fund_name'] for v in result.get('curated_vcs', [])} |
    {v['fund_name'] for v in result.get('track_a_vcs', [])} |
    {v['fund_name'] for v in result.get('track_b_vcs', [])}
)
original_dives = len(result.get('top_5_deep_dives', []))
result['top_5_deep_dives'] = [d for d in result.get('top_5_deep_dives', []) if d.get('fund_name') in valid_funds]
removed_dives = original_dives - len(result['top_5_deep_dives'])
if removed_dives > 0:
    failures.append(f'Removed {removed_dives} deep dive(s) for funds stripped during QA')

# Check top 5 deep dives
dives = result.get('top_5_deep_dives', [])
if len(dives) < 5:
    failures.append(f'Only {len(dives)} deep dives (expected 5) -- insufficient search data')
for dd in dives:
    if not dd.get('how_to_approach') or len(dd.get('how_to_approach', '')) < 30:
        dd['how_to_approach'] = 'Approach method not determinable from search data. Check the fund website directly for application instructions.'
        failures.append(f"Fixed: '{dd.get('fund_name')}' had missing how_to_approach")
    if not dd.get('fund_overview') or dd.get('fund_overview') == '':
        dd['fund_overview'] = 'not found in search data'

# Check outreach hooks count
if len(result.get('outreach_hooks', [])) != 3:
    failures.append(f"Expected 3 outreach hooks, got {len(result.get('outreach_hooks', []))}")

# Check for em dashes
full_text = json.dumps(result)
if '—' in full_text:
    result = json.loads(full_text.replace('—', '-'))
    failures.append('Fixed: em dash characters replaced with hyphens')

# Check for forbidden words
forbidden = ['powerful', 'robust', 'seamless', 'innovative', 'game-changing', 'streamline', 'leverage', 'transform']
full_text_lower = json.dumps(result).lower()
for word in forbidden:
    if word in full_text_lower:
        failures.append(f"Warning: forbidden word '{word}' found in output -- review before presenting")

# Flag any "not found in search data" entries so user knows coverage is incomplete
not_found_count = json.dumps(result).count('not found in search data')
if not_found_count > 0:
    failures.append(f'INFO: {not_found_count} field(s) marked "not found in search data" -- verify directly before outreach')

if 'data_quality_flags' not in result:
    result['data_quality_flags'] = []
result['data_quality_flags'].extend(failures)

json.dump(result, open('/tmp/vc-final-list.json', 'w'), indent=2)
print(f'QA complete. Issues addressed: {len(failures)}')
for f in failures:
    print(f'  - {f}')
if not failures:
    print('All QA checks passed.')
PYEOF
```

---

## Step 11: Save and Present Output

```bash
DATE=$(date +%Y-%m-%d)
OUTPUT_FILE="docs/vc-intel/${PRODUCT_SLUG}-${DATE}.md"
mkdir -p docs/vc-intel
```

Present the final output:

```
## VC Finder: [product_name]
Date: [today] | Stage: [detected_stage] ([stage_confidence] confidence) | Geography: [geography_bias]

---

### Product Analysis

What it does: [one_line_description]
Industry: [l1] > [l2] > [l3]
Buyer: [buyer_persona] at [company_type], [company_size]
Comparable companies used: [comma-separated list, noting source_type for each]

---

### Curated Matches (Verified)

*Funds matched from a verified dataset of 25 VC funds sourced from fund websites. Zero hallucination -- details come directly from the dataset.*

| Fund | Confidence | Stage Focus | Check Size | Matched Tags |
|---|---|---|---|---|
[one row per curated VC, sorted by confidence then score]

---

### Track A: VCs Who Backed Similar Companies

*These investors have already written a check in this space. Evidence from live Tavily search.*

| Fund | Backed Comparable | Stage Focus | Check Size | Fit Score | Approach |
|---|---|---|---|---|---|
[one row per Track A VC, sorted by space_fit_score descending]

---

### Track B: Thesis-Led Investors

*These investors are actively publishing about this space.*

| Fund | Thesis Source | Stage Focus | Check Size | Fit Score | Approach |
|---|---|---|---|---|---|
[one row per Track B VC, sorted by space_fit_score descending]

---

### Top 5 Deep Dives

#### [N]. [Fund Name] (Track [Curated/A/B])

Overview: [fund_overview -- from dataset or search data only]
Why it fits: [why_fit]
Portfolio in this space: [from dataset or search data, or "not found in search data"]
How to approach: [how_to_approach]
Outreach hook: "[outreach_hook]"

[repeat for all available deep dives]

---

### 3 Outreach Hooks for This Product Type

**1. [hook_type]**
[hook_text]
Best for: [best_for]

[repeat for all 3]

---
Data quality notes: [data_quality_flags, or "None"]
Saved to: docs/vc-intel/[PRODUCT_SLUG]-[DATE].md
```

Clean up temp files:

```bash
rm -f /tmp/vc-product-raw.md /tmp/vc-stage-signals.json /tmp/vc-product-analysis.json \
      /tmp/vc-product-context.json /tmp/vc-curated-matches.json /tmp/vc-comparable-search.json \
      /tmp/vc-tracka-results.json /tmp/vc-trackb-results.json /tmp/vc-final-list.json
```
