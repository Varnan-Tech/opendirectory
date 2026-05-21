---
name: pricing-finder
description: 'Tell it what your product is (URL or description) and it finds 5 competitors globally, fetches their actual pricing pages, extracts every tier and price point, and returns a complete pricing intelligence report: the dominant pricing model in your space, a benchmark price table, feature gate analysis, competitive positioning map, and a concrete recommended pricing strategy for your product. Use when asked to research competitor pricing, find pricing benchmarks, decide how to price a product, understand pricing models in a space, or build a pricing strategy.'
compatibility: [claude-code, gemini-cli, github-copilot]
---

# Pricing Finder

Tell it your product URL or description. It finds 5 competitors, fetches their actual pricing pages, and returns a complete pricing intelligence report: dominant model in your space, benchmark price table, feature gate analysis, positioning map, and a concrete pricing recommendation for your product.

**Zero required API keys.** Runs entirely on free pip dependencies. Optional API keys improve quality.

---

**Zero-hallucination policy:** Every price point, tier name, and feature gate in the output must trace to fetched pricing page content or a DuckDuckGo search snippet. This applies to:
- Competitor prices: extracted verbatim from fetched page content only
- "Contact Sales": recorded as-is, never estimated or replaced with a number
- Tier names: copied exactly from the page, not paraphrased
- Feature lists: extracted from page content, not inferred from product knowledge
- Positioning observations: derived from the benchmark table data only

---

## Common Mistakes

| The agent will want to... | Why that's wrong |
|---|---|
| Fill in "Contact Sales" with an estimated price | Never estimate enterprise pricing. Record it as "Contact Sales" exactly. |
| Use training knowledge for competitor prices | Every price must trace to fetched page content or a search snippet. |
| Skip the competitor confirmation step | Always show discovered competitors and wait for confirmation. Wrong competitors = wrong benchmarks. |
| Recommend a price without referencing benchmark data | Every price recommendation must cite a specific number from the benchmark table. |
| Mark a page as high quality when content < 500 chars | < 500 chars means the page was not fetched -- mark data_quality as 'low' and use search snippet fallback. |
| Use em dashes in output | Replace all em dashes with hyphens. |

---

## Read Reference Files Before Each Run

```bash
cat references/pricing-models.md
cat references/extraction-guide.md
cat references/positioning-guide.md
```

---

## Step 1: Setup Check

```bash
echo "TAVILY_API_KEY:    ${TAVILY_API_KEY:+set (search quality enhanced)}${TAVILY_API_KEY:-not set, DuckDuckGo will be used (free)}"
echo "FIRECRAWL_API_KEY: ${FIRECRAWL_API_KEY:+set (JS rendering enhanced)}${FIRECRAWL_API_KEY:-not set, requests+BS4 will be used (free)}"
echo ""
python3 -c "from ddgs import DDGS; import requests, bs4, html2text; print('Dependencies OK')" 2>/dev/null \
  || echo "ERROR: Missing dependencies. Run: pip install ddgs requests beautifulsoup4 html2text"
```

**If dependencies are missing:** Stop immediately. Tell the user: "Missing Python dependencies. Run this to install them: `pip install ddgs requests beautifulsoup4 html2text` -- all free, no accounts needed. Then try again."

**If only API keys are missing:** Continue. DuckDuckGo and requests+BS4 are the free defaults.

Derive product slug:

```bash
PRODUCT_SLUG=$(python3 -c "
from urllib.parse import urlparse
import sys, re
url = 'URL_HERE'
if url.startswith('http'):
    host = urlparse(url).netloc.replace('www.', '')
    print(host.split('.')[0])
else:
    print(re.sub(r'[^a-z0-9]', '-', url[:30].lower()).strip('-'))
")
echo "Product slug: $PRODUCT_SLUG"
```

---

## Step 2: Parse Input

Collect from the conversation:
- `product_url`: the URL to fetch (required, unless user pastes a description directly)
- `geography`: optional -- US / Europe / India / global. Default: US

**If the user provides only a pasted description (no URL):** Skip Steps 3 and 4. Go directly to Step 4 (product analysis) using the pasted text as `product_content`. Set `page_source` to `user_description` and note in `data_quality_flags`.

**If neither URL nor description:** Ask: "What is the URL of your product or startup? Or paste a short description: what it does, who it's for, and what makes it different."

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
print(f'Fetched via Firecrawl: {len(content)} characters')
open('/tmp/pf-product-raw.md', 'w').write(content)
"
```

**Fallback: requests + BS4 (free, always available)**

```bash
python3 << 'PYEOF'
import requests, html2text, random

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]
headers = {"User-Agent": random.choice(USER_AGENTS), "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8"}
resp = requests.get("URL_HERE", headers=headers, timeout=20, allow_redirects=True)
converter = html2text.HTML2Text()
converter.ignore_images = True
converter.body_width = 0
content = converter.handle(resp.text)[:8000]
print(f'Fetched via requests+BS4: {len(content)} characters')
open('/tmp/pf-product-raw.md', 'w').write(content)
PYEOF
```

**Checkpoint:**

```bash
python3 -c "
content = open('/tmp/pf-product-raw.md').read()
if len(content) < 200:
    print('ERROR: fewer than 200 characters fetched -- page may be JS-rendered')
else:
    print(f'Content OK: {len(content)} characters')
"
```

**If content < 200 characters:** Tell the user: "The product page returned too little content -- the site may be JavaScript-rendered. Please paste a short description: what your product does, who it's for, and what makes it different from competitors."

---

## Step 4: Product Analysis (AI)

Print page content:

```bash
python3 -c "
content = open('/tmp/pf-product-raw.md').read()[:5000]
print('=== PRODUCT PAGE (first 5000 chars) ===')
print(content)
"
```

**AI instructions:** Analyze the product page above and extract:

- `product_name`: the product or company name
- `one_line_description`: what it does, for whom, core value prop. Under 20 words. No marketing language.
- `industry_taxonomy`: `l1` (top-level: developer tools / fintech / healthtech / consumer / etc.), `l2` (sector: devops / payments / hr / etc.), `l3` (specific niche: CI/CD automation / embedded payments / async video / etc.)
- `differentiators`: exactly 2-3 specific things that distinguish this product. These feed the recommendation -- be specific. Generic answers like "easy to use" are not acceptable.
- `icp`: `buyer_persona` (job title), `company_type`, `company_size`
- `geography_bias`: US / Europe / India / global
- `page_source`: "live_page" or "user_description"

Write to `/tmp/pf-product-analysis.json`:

```bash
python3 << 'PYEOF'
import json

analysis = {
    # FILL from your analysis above
    "product_name": "",
    "one_line_description": "",
    "industry_taxonomy": {"l1": "", "l2": "", "l3": ""},
    "differentiators": [],
    "icp": {"buyer_persona": "", "company_type": "", "company_size": ""},
    "geography_bias": "US",
    "page_source": "live_page"
}

json.dump(analysis, open('/tmp/pf-product-analysis.json', 'w'), indent=2)
print('Product analysis written.')
PYEOF
```

Verify:

```bash
python3 -c "
import json
a = json.load(open('/tmp/pf-product-analysis.json'))
print('Product:', a['product_name'])
print('Industry:', a['industry_taxonomy']['l1'], '>', a['industry_taxonomy']['l2'], '>', a['industry_taxonomy']['l3'])
print('Differentiators:')
for d in a['differentiators']:
    print(f'  - {d}')
"
```

---

## Step 4b: Phase 1 -- Competitor Discovery

```bash
ls scripts/research.py 2>/dev/null && echo "script found" || echo "ERROR: scripts/research.py not found -- cannot continue"
```

```bash
python3 scripts/research.py \
  --phase discover \
  --product-analysis /tmp/pf-product-analysis.json \
  --output /tmp/pf-competitors-raw.json
```

Print results for AI review:

```bash
python3 -c "
import json
data = json.load(open('/tmp/pf-competitors-raw.json'))
print(f'Searches run: {len(data[\"competitor_searches\"])}')
for s in data['competitor_searches']:
    print(f'\nQuery: {s[\"query\"]}')
    for r in s.get('results', [])[:6]:
        print(f'  - {r[\"title\"]} | {r[\"url\"]}')
        print(f'    {r.get(\"snippet\",\"\")[:150]}')
"
```

**AI instructions:** Read the search results above. Pick exactly 5 competitor companies that:
1. Are named in the search result titles or snippets
2. Are in the same L3 niche as the product being analyzed
3. Are actual software products (not agencies, list articles, or review sites)
4. Are distinct from each other

For each competitor write: `name`, `url`, `pricing_url` (their pricing page -- infer as `[url]/pricing` if not found in snippets), `description` (one sentence from snippet), `source_url`.

---

## Step 5: Competitor Confirmation

```bash
python3 << 'PYEOF'
import json

analysis = json.load(open('/tmp/pf-product-analysis.json'))

# FILL: 5 competitors from the search results above
candidates = [
    # {"name": str, "url": str, "pricing_url": str, "description": str, "source_url": str}
]

print(f"\nFound 5 competitors for {analysis['product_name']} in {analysis['industry_taxonomy']['l3']}:\n")
for i, c in enumerate(candidates, 1):
    print(f"  {i}. {c['name']} -- {c['description']}")
    print(f"     Product: {c['url']}")
    print(f"     Pricing: {c['pricing_url']}")

data = json.load(open('/tmp/pf-competitors-raw.json'))
data['competitor_candidates'] = candidates
json.dump(data, open('/tmp/pf-competitors-raw.json', 'w'), indent=2)
PYEOF
```

Tell the user: "These are the 5 competitors I'll fetch pricing data from. Add, remove, or swap any -- or say 'looks good' to continue."

**Wait for confirmation.** If the user edits the list, update candidates accordingly. Then write the confirmed list:

```bash
python3 << 'PYEOF'
import json

# FILL: confirmed competitor list (after user review)
confirmed = [
    # {"name": str, "url": str, "pricing_url": str}
]

json.dump({"confirmed_competitors": confirmed}, open('/tmp/pf-competitors-confirmed.json', 'w'), indent=2)
print(f"Confirmed {len(confirmed)} competitors for pricing research.")
for c in confirmed:
    print(f"  - {c['name']} | pricing: {c['pricing_url']}")
PYEOF
```

---

## Step 6: Phase 2 -- Fetch Pricing Pages

```bash
python3 scripts/research.py \
  --phase fetch-pricing \
  --competitors /tmp/pf-competitors-confirmed.json \
  --output /tmp/pf-pricing-raw.json
```

This fetches each competitor's pricing page using a 3-tier fallback:
1. Direct fetch: `requests` + `beautifulsoup4` + `html2text`
2. Google cache: `webcache.googleusercontent.com/search?q=cache:[url]`
3. DuckDuckGo search: `"[competitor]" pricing plans cost per month` (snippet fallback)

Print fetch summary:

```bash
python3 -c "
import json
data = json.load(open('/tmp/pf-pricing-raw.json'))
print(f'Competitors fetched: {data[\"competitors_fetched\"]}')
print()
for r in data['results']:
    quality_label = {'high': 'GOOD', 'medium': 'OK', 'low': 'SNIPPET ONLY'}.get(r['data_quality'], r['data_quality'])
    print(f'  {r[\"name\"]:20} {r[\"source\"]:15} {r[\"content_length\"]:5} chars  [{quality_label}]')
"
```

**If a competitor has `data_quality: low`:** This means the pricing page was blocked or JS-rendered. The analysis will proceed using search snippets but confidence for that competitor will be noted as low.

---

## Step 7: Pricing Extraction (AI)

Print all raw pricing content:

```bash
python3 -c "
import json
data = json.load(open('/tmp/pf-pricing-raw.json'))
for r in data['results']:
    print(f'\n=== {r[\"name\"]} (source: {r[\"source\"]}, quality: {r[\"data_quality\"]}) ===')
    print(f'Pricing URL: {r[\"pricing_url\"]}')
    print(r['content'][:4000])
    print('---')
"
```

**AI instructions:** For each competitor, extract structured pricing data from the content above. Follow `references/extraction-guide.md` for how to identify tiers, prices, limits, and CTAs.

Zero-hallucination rules:
1. Extract prices verbatim from content only. If a price is not in the content, write `null`.
2. Record "Contact Sales" exactly as-is. Never replace with an estimated number.
3. `data_quality: low` means data came from search snippets -- extract what's there but do not fill gaps from training knowledge.
4. For any field not present in the content: write `"not found in page data"`.
5. Annual prices: always record the per-month equivalent alongside the annual total.

Write to `/tmp/pf-pricing-extracted.json`:

```bash
python3 << 'PYEOF'
import json

# FILL: one object per competitor, following the schema below
extracted = [
    # {
    #   "competitor": str,
    #   "pricing_url": str,
    #   "data_quality": "high" | "medium" | "low",
    #   "pricing_model": "per-seat" | "flat-rate" | "usage-based" | "freemium" | "tiered-flat" | "hybrid",
    #   "billing_cadence": ["monthly"] | ["annual"] | ["monthly", "annual"],
    #   "annual_discount": str,           # e.g. "20%" or "not found in page data"
    #   "free_tier": true | false,
    #   "free_trial": true | false,
    #   "free_trial_days": int | null,
    #   "tiers": [
    #     {
    #       "name": str,
    #       "price_monthly": float | null,       # null if Contact Sales
    #       "price_annual_monthly": float | null, # per-month equivalent when billed annually
    #       "price_note": str,                   # "Contact Sales", "Free", or empty
    #       "seats": str,                        # "per seat", "unlimited", "up to 5", etc.
    #       "key_limits": [str],                 # storage, API calls, projects, etc.
    #       "key_features": [str]                # top 3-5 features in this tier
    #     }
    #   ],
    #   "enterprise_tier": true | false,
    #   "enterprise_pricing": str,               # "Contact Sales" or actual price
    #   "regional_pricing": str | null           # e.g. "India: ₹999/mo" or null
    # }
]

json.dump(extracted, open('/tmp/pf-pricing-extracted.json', 'w'), indent=2)
print(f'Extracted pricing for {len(extracted)} competitors.')
for c in extracted:
    tier_count = len(c.get('tiers', []))
    print(f"  {c['competitor']:20} model={c['pricing_model']:15} tiers={tier_count} quality={c['data_quality']}")
PYEOF
```

---

## Step 8: Pattern Analysis (AI)

Print all extracted pricing data:

```bash
python3 -c "
import json
data = json.load(open('/tmp/pf-pricing-extracted.json'))
for c in data:
    print(f'\n{c[\"competitor\"]} ({c[\"pricing_model\"]}, quality={c[\"data_quality\"]})')
    for t in c.get('tiers', []):
        price = t.get('price_monthly')
        label = t.get('price_note', '')
        print(f'  {t[\"name\"]:15} \${price}/mo' if price is not None else f'  {t[\"name\"]:15} {label}')
"
```

**AI instructions:** Analyze all extracted pricing data and synthesize patterns. Follow `references/positioning-guide.md` for positioning analysis.

Write to `/tmp/pf-patterns.json`:

```bash
python3 << 'PYEOF'
import json

patterns = {
    # FILL from analysis

    # Dominant model across 5 competitors
    "dominant_model": "",                         # the most common model
    "model_breakdown": {},                        # {"per-seat": 3, "flat-rate": 1, "freemium": 1}
    "model_explanation": "",                      # 2 sentences: why this model dominates this space

    # Price benchmarks (USD/mo, monthly billing)
    "entry_tier": {
        "min": None, "max": None, "median": None,
        "currency": "USD/mo",
        "note": ""                                # e.g. "based on 4/5 competitors (1 was search snippet only)"
    },
    "mid_tier": {
        "min": None, "max": None, "median": None,
        "currency": "USD/mo",
        "note": ""
    },
    "enterprise_floor": "",                       # e.g. "$99+/mo" or "Contact Sales (4/5 competitors)"

    # Billing patterns
    "annual_discount_typical": "",                # e.g. "15-20%"
    "billing_cadence_dominant": "",               # "monthly + annual", "monthly only", "annual only"

    # Free tier / trial prevalence
    "free_tier_count": 0,                         # how many of 5 offer free tier
    "free_trial_count": 0,                        # how many of 5 offer free trial
    "free_tier_typical_limits": [],               # what's typically in a free tier

    # Feature gates
    "always_free_features": [],                   # features present in all free/entry tiers
    "always_paid_features": [],                   # features locked behind paid in all competitors
    "variable_features": [],                      # features that vary most across competitors

    # Regional pricing
    "regional_pricing_flags": [],                 # competitors with region-specific pricing

    # Data quality
    "high_quality_count": 0,                      # competitors with fetched page data
    "low_quality_count": 0,                       # competitors with snippet-only data
    "data_quality_flags": []
}

json.dump(patterns, open('/tmp/pf-patterns.json', 'w'), indent=2)
print('Patterns written.')
print(f"Dominant model: {patterns['dominant_model']}")
print(f"Entry tier: ${patterns['entry_tier']['min']}-${patterns['entry_tier']['max']}/mo (median ${patterns['entry_tier']['median']})")
print(f"Free tier: {patterns['free_tier_count']}/5 | Free trial: {patterns['free_trial_count']}/5")
PYEOF
```

---

## Step 9: Positioning Map + Recommendation (AI)

Print consolidated data:

```bash
python3 -c "
import json

analysis  = json.load(open('/tmp/pf-product-analysis.json'))
extracted = json.load(open('/tmp/pf-pricing-extracted.json'))
patterns  = json.load(open('/tmp/pf-patterns.json'))

print('=== PRODUCT ===')
print(f'Name: {analysis[\"product_name\"]}')
print(f'What it does: {analysis[\"one_line_description\"]}')
print('Differentiators:')
for d in analysis['differentiators']:
    print(f'  - {d}')

print()
print('=== PATTERNS ===')
print(f'Dominant model: {patterns[\"dominant_model\"]}  breakdown: {patterns[\"model_breakdown\"]}')
print(f'Entry tier: \${patterns[\"entry_tier\"][\"min\"]}-\${patterns[\"entry_tier\"][\"max\"]}/mo (median \${patterns[\"entry_tier\"][\"median\"]})')
print(f'Mid tier:   \${patterns[\"mid_tier\"][\"min\"]}-\${patterns[\"mid_tier\"][\"max\"]}/mo (median \${patterns[\"mid_tier\"][\"median\"]})')
print(f'Enterprise: {patterns[\"enterprise_floor\"]}')
print(f'Free tier: {patterns[\"free_tier_count\"]}/5 | Free trial: {patterns[\"free_trial_count\"]}/5')

print()
print('=== COMPETITOR PRICING SUMMARY ===')
for c in extracted:
    print(f'{c[\"competitor\"]} ({c[\"pricing_model\"]}):')
    for t in c.get('tiers', []):
        p = t.get('price_monthly')
        print(f'  {t[\"name\"]}: \${p}/mo' if p is not None else f'  {t[\"name\"]}: {t.get(\"price_note\",\"\")}')
"
```

**AI instructions -- zero-hallucination rules:**

1. **Positioning map:** Name specific competitors from the extracted data. No invented observations.
2. **Underserved gap:** Must reference a specific price range or model type absent from the data.
3. **Every price recommendation:** Must cite a specific number from the patterns JSON (entry_tier.median, mid_tier.median, etc.).
4. **Free tier recommendation:** Must reference `free_tier_count` from patterns (e.g., "3/5 competitors offer a free tier, so not offering one is a risk").
5. **Differentiator gate:** Choose from the product's `differentiators` list in the analysis -- not invented features.
6. No em dashes. No banned words (powerful, seamless, game-changing, revolutionary, cutting-edge, leverage).

**Generate:**

1. Positioning map: who owns each quadrant (cheap+simple, middle, enterprise), and the underserved gap
2. Recommended pricing strategy: model + all tier prices + free tier decision + annual discount + what to gate

Write to `/tmp/pf-final.json`:

```bash
python3 << 'PYEOF'
import json

result = {
    "product_summary": {
        # FILL from analysis
        "product_name": "",
        "one_line_description": "",
        "differentiators": []
    },
    "competitors_researched": [],  # FILL: list of competitor names

    # Filled from patterns
    "pricing_model_analysis": {
        "dominant_model": "",
        "model_breakdown": {},
        "model_explanation": "",
        "free_tier_count": 0,
        "free_trial_count": 0,
        "annual_discount_typical": ""
    },

    # Benchmark table (filled from extracted data)
    "benchmark_table": [
        # Per competitor:
        # {"name": str, "model": str, "entry_price": str, "mid_price": str,
        #  "top_price": str, "free_tier": bool, "free_trial": bool, "data_quality": str}
    ],

    # Market ranges
    "market_ranges": {
        "entry": {"min": None, "max": None, "median": None},
        "mid":   {"min": None, "max": None, "median": None},
        "enterprise": ""
    },

    # Feature gate analysis
    "feature_gates": {
        "always_free": [],
        "always_paid": [],
        "most_variable": []
    },

    # Positioning map
    "positioning_map": {
        "cheap_simple": {"competitor": "", "price": ""},
        "middle_market": [],
        "enterprise": {"competitor": "", "note": ""},
        "underserved_gap": ""
    },

    # Recommendation
    "recommendation": {
        "model": "",
        "model_justification": "",       # references specific data from model_breakdown
        "entry_price": "",               # e.g. "$12/mo"
        "entry_justification": "",       # references entry_tier.median
        "mid_price": "",
        "mid_justification": "",
        "top_price": "",                 # price or "Contact Sales"
        "top_justification": "",
        "free_tier": True,               # bool
        "free_tier_justification": "",   # references free_tier_count
        "annual_discount": "",           # e.g. "17%"
        "annual_justification": "",
        "gate_behind_paid": "",          # specific differentiator from product analysis
        "gate_justification": ""
    },

    "data_quality_flags": []
}

json.dump(result, open('/tmp/pf-final.json', 'w'), indent=2)
print('Synthesis written.')
print(f'Benchmark table: {len(result.get("benchmark_table", []))} competitors')
print(f'Recommendation model: {result.get("recommendation", {}).get("model", "--")}')
PYEOF
```

---

## Step 10: Self-QA, Present, and Save

**Self-QA:**

```bash
python3 << 'PYEOF'
import json

result = json.load(open('/tmp/pf-final.json'))
failures = []

# Check 1: em dashes
full_text = json.dumps(result)
if '—' in full_text:
    result = json.loads(full_text.replace('—', '-'))
    failures.append('Fixed: em dashes replaced with hyphens')

# Check 2: banned words
banned = ['powerful', 'seamless', 'innovative', 'game-changing', 'revolutionize',
          'cutting-edge', 'best-in-class', 'world-class', 'leverage', 'disrupt', 'transform']
for word in banned:
    if word.lower() in json.dumps(result).lower():
        failures.append(f'Warning: banned word "{word}" found in output')

# Check 3: recommendation completeness
rec = result.get('recommendation', {})
required = ['model', 'entry_price', 'mid_price', 'top_price', 'free_tier',
            'entry_justification', 'mid_justification', 'gate_behind_paid']
for field in required:
    if not rec.get(field) and rec.get(field) is not False:
        failures.append(f'Warning: recommendation missing field: {field}')

# Check 4: no Contact Sales replaced with numbers
for row in result.get('benchmark_table', []):
    for field in ['entry_price', 'mid_price', 'top_price']:
        val = str(row.get(field, ''))
        if 'contact' in val.lower():
            pass  # correct
        elif row.get('data_quality') == 'low' and '$' in val:
            failures.append(f'Warning: {row["name"]} has dollar prices from low-quality source')

# Check 5: benchmark table populated
if len(result.get('benchmark_table', [])) < 3:
    failures.append(f'Warning: benchmark table has only {len(result.get("benchmark_table", []))} competitors -- need at least 3 for reliable benchmarks')

# Check 6: "not found in page data" count
nf = json.dumps(result).count('not found in page data')
if nf > 0:
    failures.append(f'INFO: {nf} field(s) marked "not found in page data"')

if 'data_quality_flags' not in result:
    result['data_quality_flags'] = []
result['data_quality_flags'].extend(failures)

json.dump(result, open('/tmp/pf-final.json', 'w'), indent=2)
print(f'QA complete. {len(failures)} issues.')
for f in failures:
    print(f'  - {f}')
if not failures:
    print('All QA checks passed.')
PYEOF
```

**Present the output:**

```
## Pricing Intel: [product_name]
Date: [today] | Competitors: [list] | Geography: [geography]

---

### Your Product
[one_line_description]
Differentiators: [list]

---

### 1. Pricing Model Analysis
Dominant model: [dominant_model] ([N]/5 competitors)
[model_explanation -- 2-3 sentences on why this model dominates the space]

Free tier: [N]/5 competitors | Free trial: [N]/5 | Annual discount: typical [X]%

---

### 2. Price Point Benchmark Table
| Competitor | Model | Entry | Mid | Top | Free tier | Free trial | Data quality |
|---|---|---|---|---|---|---|---|
[one row per competitor from benchmark_table]

Market ranges:
- Entry tier: $[min]-$[max]/mo (median $[median])
- Mid tier:   $[min]-$[max]/mo (median $[median])
- Enterprise: [enterprise_floor]

---

### 3. Feature Gate Analysis
Always free: [always_free list]
Always behind paid: [always_paid list]
Most variable across competitors: [most_variable list]

---

### 4. Competitive Positioning Map
Cheap + simple: [competitor] at $[X]/mo
Middle market:  [competitors] at $[X]-$[Y]/mo
Enterprise:     [competitor] (Contact Sales)
Underserved gap: [underserved_gap -- specific observation]

---

### 5. Recommended Pricing for [product_name]
Model: [model] -- [model_justification]
Entry: [entry_price] -- [entry_justification]
Mid:   [mid_price] -- [mid_justification]
Top:   [top_price] -- [top_justification]
Free tier: [Yes/No] -- [free_tier_justification]
Annual discount: [annual_discount] -- [annual_justification]
Gate behind paid: [gate_behind_paid] -- [gate_justification]

---
Data notes: [data_quality_flags or "None"]
Saved to: docs/pricing-intel/[PRODUCT_SLUG]-[DATE].md
```

**Save to file and clean up:**

```bash
DATE=$(date +%Y-%m-%d)
OUTPUT_FILE="docs/pricing-intel/${PRODUCT_SLUG}-${DATE}.md"
mkdir -p docs/pricing-intel
echo "Saved to: $OUTPUT_FILE"
```

```bash
rm -f /tmp/pf-product-raw.md /tmp/pf-product-analysis.json \
      /tmp/pf-competitors-raw.json /tmp/pf-competitors-confirmed.json \
      /tmp/pf-pricing-raw.json /tmp/pf-pricing-extracted.json \
      /tmp/pf-patterns.json /tmp/pf-final.json
echo "Temp files cleaned up."
```
