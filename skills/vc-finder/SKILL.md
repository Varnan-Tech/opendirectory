---
name: vc-finder
description: Takes a startup product URL or description, detects the industry and funding stage, identifies 5 comparable funded companies, searches who invested in those companies (Track A), finds VCs who publish investment theses about this space (Track B), and returns a ranked sourced list of relevant investors with deep-dives and outreach hooks. Use when asked to find investors for a startup, identify which VCs fund products like mine, research who backs companies in my space, build a VC target list, or find investor-market fit. Trigger when a user says "find VCs for my startup", "who invests in my space", "build me a VC list", "which funds should I pitch", "find investors for my product", "who backed companies like mine", or "help me find venture capital".
compatibility: [claude-code, gemini-cli, github-copilot]
---

# VC Finder

Take a product URL or description. Detect industry and stage. Find 5 comparable funded companies. Run two research tracks: who invested in those comparables (Track A), and which VCs publish theses about this space (Track B). Return a sourced, ranked investor list with outreach hooks.

---

**Critical rule:** Every VC in Track A must include the specific comparable company they backed as evidence. Every VC in Track B must include the exact article or post title where they stated their thesis. If a VC name did not appear in Tavily search results, do not include them. No hallucinated fund names.

---

## Common Mistakes

| The agent will want to... | Why that's wrong |
|---|---|
| Add a16z or Sequoia because they are famous | A famous VC without evidence is noise. Only include VCs that appear in Tavily search results for this specific product. Name-dropping wastes the founder's time. |
| Continue when all 5 Track A searches return 0 results | Zero Track A results means the comparables were wrong or too obscure. Stop, regenerate comparables with broader known names, and retry. Continuing produces an evidence-free list. |
| Include a Track B VC without citing the article or post | Thesis without a source is indistinguishable from hallucination. The founder cannot verify it and the list loses all credibility. |
| Detect stage from website aesthetics ("site looks polished") | Stage must come from the specific CTA signals detected in Step 4. Aesthetic guessing sends founders to wrong-stage investors. |
| Write generic outreach hooks like "highlight your traction" | Every outreach hook must name this specific product's differentiator and a specific VC portfolio signal. Generic hooks are removed by the QA step. |
| Skip the URL fetch when the user also provides a description | Always fetch the URL. The live page often reveals stage signals (pricing CTAs, customer logos, job openings) that the user's description omits. |

---

## Step 1: Setup Check

```bash
echo "GEMINI_API_KEY: ${GEMINI_API_KEY:+set}"
echo "TAVILY_API_KEY: ${TAVILY_API_KEY:+set}"
echo "FIRECRAWL_API_KEY: ${FIRECRAWL_API_KEY:-not set, Tavily extract will be used as fallback}"
```

**If GEMINI_API_KEY is missing:** Stop. Tell the user: "GEMINI_API_KEY is required for product analysis and VC synthesis. Get it at aistudio.google.com. Add it to your .env file."

**If TAVILY_API_KEY is missing:** Stop. Tell the user: "TAVILY_API_KEY is required to research VC investments and theses. There is no fallback for this. Get it at app.tavily.com. Free tier: 1000 credits/month (about 125 full runs). Add it to your .env file."

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

Parse the fetched markdown with regex before any API call. This gives Gemini anchored evidence rather than asking it to guess from aesthetics.

```bash
python3 << 'PYEOF'
import re, json

content = open('/tmp/vc-product-raw.md').read().lower()
stage_signals = []

# Pre-seed signals
if re.search(r'join\s+(the\s+)?waitlist|sign\s+up\s+for\s+beta|early\s+access|request\s+(an?\s+)?invite|get\s+notified', content):
    stage_signals.append({'signal': 'waitlist or beta CTA', 'stage_hint': 'pre-seed'})

# Seed signals
if re.search(r'start\s+(your\s+)?free\s+trial|try\s+(it\s+)?for\s+free|request\s+a?\s+demo|book\s+a?\s+demo|schedule\s+a?\s+demo', content):
    stage_signals.append({'signal': 'free trial or demo CTA', 'stage_hint': 'seed'})

# Series A signals
if re.search(r'contact\s+sales|talk\s+to\s+(our\s+)?sales|see\s+pricing|view\s+pricing|plans\s+and\s+pricing', content):
    stage_signals.append({'signal': 'pricing or sales CTA', 'stage_hint': 'series-a'})
if re.search(r'case\s+stud(y|ies)|customer\s+stor(y|ies)|trusted\s+by\s+[\d,]+|used\s+by\s+[\d,]+', content):
    stage_signals.append({'signal': 'case studies or customer count', 'stage_hint': 'series-a'})

# Series A/B signals
if re.search(r'enterprise\s+(plan|pricing|tier)|we.?re\s+hiring|join\s+our\s+team|open\s+positions', content):
    stage_signals.append({'signal': 'enterprise tier or job openings', 'stage_hint': 'series-a-or-b'})

# Funding announcement -- extract directly if present
funding_match = re.search(
    r'raised\s+\$[\d,.]+\s*[mk]?|series\s+[abc]\s+round|seed\s+round|(\$[\d,.]+\s*[mk]?\s+(?:seed|series\s+[abc]))',
    content
)
if funding_match:
    stage_signals.append({'signal': f'funding text: {funding_match.group(0).strip()}', 'stage_hint': 'announced'})

# Determine dominant stage
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

## Step 5: Product Analysis with Gemini

```bash
python3 << 'PYEOF'
import json

product_content = open('/tmp/vc-product-raw.md').read()[:6000]
stage_signals = json.load(open('/tmp/vc-stage-signals.json'))

request = {
    "system_instruction": {
        "parts": [{
            "text": "You are a venture capital analyst. Analyze a product page and return structured JSON only. No commentary. No em dashes. Vague category labels like 'technology' or 'software' alone are not acceptable at L2 or L3 -- be specific. Comparable companies must be real funded companies with public funding records, well-known enough to appear in press coverage."
        }]
    },
    "contents": [{
        "parts": [{
            "text": f"""Analyze this product page and return a JSON object with exactly these keys:

1. product_name: string
2. one_line_description: string -- what it does, for whom, core value prop. Under 20 words. No marketing language.
3. industry_taxonomy: object with:
   - l1: top-level (e.g. "software", "fintech", "healthtech", "consumer", "hardware")
   - l2: sector (e.g. "developer tools", "sales technology", "edtech", "logistics software")
   - l3: specific niche (e.g. "CI/CD automation", "outbound prospecting", "last-mile routing")
4. icp: object with:
   - buyer_persona: job title (e.g. "VP Engineering", "founder", "sales ops manager")
   - company_type: (e.g. "B2B SaaS", "e-commerce brand", "enterprise IT team")
   - company_size: (e.g. "5-50 employees", "50-500 employees", "enterprise")
5. detected_stage: one of: pre-seed, seed, series-a, series-b, unknown
6. stage_confidence: one of: high, medium, low
7. stage_evidence: one sentence citing exactly which CTA or text on the page drove this classification. Write "no clear signals found" if unknown.
8. comparable_companies: array of exactly 5 objects, each with:
   - name: real company name (must have public VC funding records)
   - similarity_reason: one sentence why this company is comparable to the product
   - estimated_stage: their funding stage as of your knowledge cutoff
9. geography_bias: one of: US, Europe, global, unclear -- infer from page text

Stage signals detected from the page (use as input to your stage classification):
{json.dumps(stage_signals, indent=2)}

Product page content:
{product_content}"""
        }]
    }],
    "generationConfig": {
        "temperature": 0.2,
        "maxOutputTokens": 3000
    }
}

json.dump(request, open('/tmp/vc-analysis-request.json', 'w'))
PYEOF

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/vc-analysis-request.json \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
text = d['candidates'][0]['content']['parts'][0]['text'].strip()
if text.startswith('\`\`\`'):
    text = '\n'.join(text.split('\n')[1:-1])
analysis = json.loads(text)
json.dump(analysis, open('/tmp/vc-product-analysis.json', 'w'), indent=2)
print('Product analysis complete.')
print('Product:', analysis['product_name'])
print('Industry:', analysis['industry_taxonomy']['l1'], '>', analysis['industry_taxonomy']['l2'], '>', analysis['industry_taxonomy']['l3'])
print('Stage:', analysis['detected_stage'], '(' + analysis['stage_confidence'] + ' confidence)')
print('Comparables:', ', '.join(c['name'] for c in analysis['comparable_companies']))
"
```

**If Gemini returns empty or JSON parsing fails:** Retry once with `maxOutputTokens` reduced to 2000. If retry also fails: Stop. Tell the user: "Product analysis failed. Please paste a direct description (3-5 sentences: what it does, who it is for, current stage) and run again."

---

## Step 6: Track A -- Who Invested in Comparable Companies

Run 5 Tavily searches, one per comparable. Save all results to a single file.

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

**If all 5 Track A searches return 0 results:** Tell the user: "No funding data found for the comparable companies. This usually means the comparables are too early-stage or obscure for public press coverage. I will retry with broader comparable names." Then re-run Step 5 with a note to Gemini to choose "well-funded companies with significant press coverage" and retry Step 6.

If the retry also returns 0 results: proceed to Track B only, and flag this in `data_quality_flags`.

---

## Step 7: Track B -- VCs With Investment Theses About This Space

Run 3 Tavily searches using the L2 and L3 taxonomy from Step 5.

```bash
python3 << 'PYEOF'
import json, os, urllib.request

analysis = json.load(open('/tmp/vc-product-analysis.json'))
l2 = analysis['industry_taxonomy']['l2']
l3 = analysis['industry_taxonomy']['l3']
stage = analysis['detected_stage']
tavily_key = os.environ.get('TAVILY_API_KEY', '')

queries = [
    {
        'name': 'thesis_l3',
        'query': f'venture capital investment thesis "{l3}" investing 2023 OR 2024 OR 2025'
    },
    {
        'name': 'thesis_l2',
        'query': f'VC fund "{l2}" investment thesis portfolio companies'
    },
    {
        'name': 'stage_space',
        'query': f'{stage} investors "{l3}" startup venture capital fund'
    }
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
        all_track_b.append({
            'query_name': q['name'],
            'query': q['query'],
            'answer': '',
            'results': [],
            'error': str(e)
        })

json.dump(all_track_b, open('/tmp/vc-trackb-results.json', 'w'), indent=2)
PYEOF
```

**If all 3 Track B searches return 0 results:** Proceed with Track A results only. Note in `data_quality_flags`: "No thesis-led investors found via public search. Try checking Substack manually for VC newsletters covering this niche."

---

## Step 8: Gemini Synthesis -- Rank and Score All VCs

```bash
python3 << 'PYEOF'
import json

analysis = json.load(open('/tmp/vc-product-analysis.json'))
track_a = json.load(open('/tmp/vc-tracka-results.json'))
track_b = json.load(open('/tmp/vc-trackb-results.json'))

# Compress results to stay within token limits
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

context = {
    'product': {
        'name': analysis['product_name'],
        'description': analysis['one_line_description'],
        'industry': analysis['industry_taxonomy'],
        'icp': analysis['icp'],
        'stage': analysis['detected_stage'],
        'stage_confidence': analysis['stage_confidence'],
        'geography': analysis['geography_bias']
    },
    'track_a_research': track_a_summary,
    'track_b_research': track_b_summary
}

request = {
    "system_instruction": {
        "parts": [{
            "text": """You are a venture capital research analyst. Synthesize investor research into a sourced, ranked list. Follow these rules exactly:
1. Only include VCs whose names appear in the provided Tavily search results. Do not add VCs not mentioned in the data.
2. Every Track A VC must have evidence_company: the specific comparable company they backed (required -- omit the VC if you cannot confirm this).
3. Every Track B VC must have thesis_source_title: the exact article or page title where they stated their thesis (required -- omit the VC if you cannot confirm this).
4. stage_fit_score 1-10: penalize 3 points if the VC's typical stage does not match the product's detected stage.
5. space_fit_score 1-10: only give 9-10 if the VC backed 2+ companies in this specific L3 niche.
6. check_size: use ranges from search result data only. If not found, write "not in search data".
7. approach_method: one of -- cold email, warm intro required, AngelList, application form, Twitter/X DM. Infer from what is publicly known about this fund's intake process.
8. outreach_hook: must reference this specific product's differentiator and a named VC portfolio signal or thesis quote. Generic hooks like 'highlight your traction' are not acceptable.
9. No em dashes anywhere in output.
10. No marketing language."""
        }]
    },
    "contents": [{
        "parts": [{
            "text": f"""Synthesize this VC research for the product below. Return a JSON object with exactly these keys:

1. product_summary: object with name, one_line_description, industry_l1, industry_l2, industry_l3, detected_stage, comparable_companies_used (array of names)

2. track_a_vcs: array of VC objects from Track A research. Each object:
   - fund_name, evidence_company (REQUIRED), evidence_source_url, stage_focus, check_size, thesis_summary (1-2 sentences), stage_fit_score (1-10), space_fit_score (1-10), approach_method

3. track_b_vcs: array of VC objects from Track B research. Each object:
   - fund_name, thesis_source_title (REQUIRED), thesis_source_url, stage_focus, check_size, thesis_summary (1-2 sentences), stage_fit_score (1-10), space_fit_score (1-10), approach_method

4. top_5_deep_dives: array of exactly 5 objects (the 5 highest combined score VCs across both tracks). Each:
   - fund_name, track ("A" or "B"), fund_overview (2-3 sentences), why_fit (2-3 sentences specific to this product's L3 niche), portfolio_in_space (array of 1-3 names from search data only), how_to_approach (specific steps, min 30 chars), outreach_hook (2-3 sentences, product-specific)

5. outreach_hooks: array of exactly 3 objects:
   - hook_type (e.g. "portfolio overlap angle", "thesis language mirror", "comparable exit angle"), hook_text (2-3 sentences a founder would actually send), best_for (which VC type this works for)

6. data_quality_flags: array of strings noting any gaps or low-confidence areas

Research data:
{json.dumps(context, indent=2)}"""
        }]
    }],
    "generationConfig": {
        "temperature": 0.3,
        "maxOutputTokens": 6000
    }
}

json.dump(request, open('/tmp/vc-synthesis-request.json', 'w'))
print('Synthesis request prepared.')
PYEOF

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/vc-synthesis-request.json \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
text = d['candidates'][0]['content']['parts'][0]['text'].strip()
if text.startswith('\`\`\`'):
    text = '\n'.join(text.split('\n')[1:-1])
result = json.loads(text)
json.dump(result, open('/tmp/vc-final-list.json', 'w'), indent=2)
print(f'Synthesis complete. Track A: {len(result.get(\"track_a_vcs\", []))} VCs. Track B: {len(result.get(\"track_b_vcs\", []))} VCs.')
"
```

**If Gemini returns empty or JSON parsing fails:** Retry once with `maxOutputTokens` reduced to 4000. If retry also fails: present whatever partial JSON was returned, mark missing sections `[INCOMPLETE]`, and tell the user: "Synthesis incomplete. The research data may have been too large. Try running again."

---

## Step 9: Self-QA

Run before presenting. Remove non-evidenced VCs structurally.

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

# Check top 5 deep dives
dives = result.get('top_5_deep_dives', [])
if len(dives) < 5:
    failures.append(f'Only {len(dives)} deep dives (expected 5) -- insufficient search data')
for dd in dives:
    if not dd.get('how_to_approach') or len(dd.get('how_to_approach', '')) < 30:
        dd['how_to_approach'] = 'Approach method not determinable from search data. Check the fund website directly for application instructions.'
        failures.append(f"Fixed: '{dd.get('fund_name')}' had missing how_to_approach")

# Check outreach hooks count
if len(result.get('outreach_hooks', [])) != 3:
    failures.append(f"Expected 3 outreach hooks, got {len(result.get('outreach_hooks', []))}")

# Check for em dashes
if ':' in json.dumps(result):
    result_str = json.dumps(result).replace(':', ':')
    result = json.loads(result_str)
    failures.append('Fixed: em dash characters removed from output')

# Check for forbidden words
forbidden = ['powerful', 'robust', 'seamless', 'innovative', 'game-changing', 'streamline', 'leverage', 'transform']
full_text = json.dumps(result).lower()
for word in forbidden:
    if word in full_text:
        failures.append(f"Warning: forbidden word '{word}' found in output -- review before presenting")

# Ensure data_quality_flags exists
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

## Step 10: Save and Present Output

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
Comparable companies used for research: [comma-separated list]

---

### Track A: VCs Who Backed Similar Companies

*These investors have already written a check in this space.*

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

#### [N]. [Fund Name] (Track [A/B])

Overview: [fund_overview]
Why it fits: [why_fit]
Portfolio in this space: [names, or "Not found in search data"]
How to approach: [how_to_approach]
Outreach hook: "[outreach_hook]"

[repeat for all 5]

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
rm -f /tmp/vc-product-raw.md /tmp/vc-stage-signals.json /tmp/vc-analysis-request.json \
      /tmp/vc-product-analysis.json /tmp/vc-tracka-results.json /tmp/vc-trackb-results.json \
      /tmp/vc-synthesis-request.json /tmp/vc-final-list.json /tmp/vc-qa-result.json
```
