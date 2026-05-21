---
name: competitor-pr-finder
description: 'Give it your product URL or description. It finds your top 5 competitors, runs three-track PR research across all of them (editorial, podcasts, communities), identifies which channels appear most frequently, looks up the journalist or host for each, and returns a tiered outreach list with story angles and ready-to-send cold pitch drafts tailored to your product. Use when asked to find PR opportunities, discover where competitors got featured, build a media outreach list, find which journalists cover my space, or get pitch templates for press coverage.'
compatibility: [claude-code, gemini-cli, github-copilot]
---

# Competitor PR Finder

Give it your product URL. It finds your competitors, researches every PR channel they used (news, podcasts, communities), surfaces the channels that appear across multiple competitors (your proven targets), finds the journalist or host for each, and drafts a personalized cold pitch for your product at every tier-1 channel.

---

**Zero-hallucination policy:** Every channel, journalist name, story angle, and pitch detail in the output must trace to a specific Tavily search result or the fetched product page. This applies to:
- Competitor names: must appear in Tavily search results, not AI training knowledge
- Channel names: must have a URL in the search results
- Journalist/host names: must appear verbatim in a Tavily snippet
- Story angles: extracted from article/episode titles in search results only
- Pitch drafts: reference specific evidence from search data + product analysis

---

## Common Mistakes

| The agent will want to... | Why that's wrong |
|---|---|
| Name a journalist from training knowledge | Every journalist name must trace to a search result snippet. Writing "Sarah Perez covers startups at TechCrunch" from memory is hallucination. |
| List channels without evidence URLs | Every channel in the output must have at least one URL from the PR search results proving a competitor was featured there. |
| Skip the competitor confirmation step | Always show discovered competitors and wait for the user to confirm. Wrong competitors = wasted searches and a useless output. |
| Generate generic pitches ("We'd love to be featured") | Every pitch must reference a specific angle from the evidence AND a specific differentiator from the product analysis. |
| Mark a channel as Tier 1 with only 1 competitor occurrence | Tier 1 = 3+ competitors. Tier 2 = exactly 2. Tier 3 = 1. Do not promote channels that haven't proven themselves. |
| Use em dashes in output | Replace all em dashes (--) with hyphens. |

---

## Read Reference Files Before Each Run

```bash
cat references/pr-channel-types.md
cat references/pitch-guide.md
cat references/tier-scoring.md
```

---

## Step 1: Setup Check

```bash
echo "TAVILY_API_KEY:    ${TAVILY_API_KEY:+set}${TAVILY_API_KEY:-NOT SET -- required}"
echo "FIRECRAWL_API_KEY: ${FIRECRAWL_API_KEY:+set}${FIRECRAWL_API_KEY:-not set, Tavily extract will be used as fallback}"
```

**If TAVILY_API_KEY is missing:** Stop immediately. Tell the user: "TAVILY_API_KEY is required to research competitors and find PR coverage. There is no fallback. Get it at app.tavily.com -- free tier: 1000 credits/month (about 43 full runs at ~23 searches/run). Add it to your .env file."

**If only FIRECRAWL_API_KEY is missing:** Continue. Tavily extract will be used for the URL fetch.

---

## Step 2: Parse Input

Collect from the conversation:
- `product_url`: the URL to fetch (required, unless user pastes a description directly)
- `product_name`: optional, derived from page if not provided
- `geography`: optional -- US / Europe / global. Default: US

**If the user provides only a pasted description (no URL):** Skip Steps 3 and 4. Go directly to Step 4 (product analysis) using the pasted text as `product_content`. Set `page_source` to `user_description` and note in `data_quality_flags`.

**If neither URL nor description:** Ask: "What is the URL of your product or startup? Or paste a short description: what it does, who it is for, and what makes it different from competitors."

Derive product slug:

```bash
PRODUCT_SLUG=$(python3 -c "
from urllib.parse import urlparse
import sys
url = 'URL_HERE'
if url.startswith('http'):
    host = urlparse(url).netloc.replace('www.', '')
    print(host.split('.')[0])
else:
    import re
    print(re.sub(r'[^a-z0-9]', '-', url[:30].lower()).strip('-'))
")
echo "Product slug: $PRODUCT_SLUG"
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
print(f'Fetched via Firecrawl: {len(content)} characters')
open('/tmp/cprf-product-raw.md', 'w').write(content)
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
open('/tmp/cprf-product-raw.md', 'w').write(content)
"
```

**Checkpoint:**

```bash
python3 -c "
content = open('/tmp/cprf-product-raw.md').read()
if len(content) < 200:
    print('ERROR: fewer than 200 characters fetched')
else:
    print(f'Content OK: {len(content)} characters')
"
```

**If content < 200 characters:** Stop fetching. Tell the user: "The product page returned no readable content -- the site is likely JavaScript-rendered and blocked the fetch. Please paste a short description directly: what it does, who it is for, and what makes it different."

---

## Step 4: Product Analysis (AI)

Print page content:

```bash
python3 -c "
content = open('/tmp/cprf-product-raw.md').read()[:5000]
print('=== PRODUCT PAGE (first 5000 chars) ===')
print(content)
"
```

**AI instructions:** Analyze the product page above and extract:

- `product_name`: the product or company name
- `one_line_description`: what it does, for whom, core value prop. Under 20 words. No marketing language. Example: "CI/CD automation for developer teams that self-host their pipelines."
- `industry_taxonomy`: `l1` (top-level: e.g. developer tools / fintech / healthtech / consumer), `l2` (sector: e.g. devops / payments / telemedicine), `l3` (specific niche: e.g. CI/CD automation / embedded payments / async video consultation). Vague labels like "technology" alone are not acceptable.
- `differentiators`: exactly 2-3 specific things that distinguish this product from generic competitors. These feed directly into the pitch drafts -- be specific. Example: ["Self-hosted pipeline runner -- no data leaves your infra", "Native support for monorepos with dynamic step generation"]
- `icp`: `buyer_persona` (job title), `company_type`, `company_size`
- `geography_bias`: US / Europe / global / unclear
- `page_source`: "live_page" or "user_description"

Write to `/tmp/cprf-product-analysis.json`:

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

json.dump(analysis, open('/tmp/cprf-product-analysis.json', 'w'), indent=2)
print('Product analysis written.')
PYEOF
```

Verify:

```bash
python3 -c "
import json
a = json.load(open('/tmp/cprf-product-analysis.json'))
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
  --product-analysis /tmp/cprf-product-analysis.json \
  --tavily-key "$TAVILY_API_KEY" \
  --output /tmp/cprf-competitors-raw.json
```

Print results for AI review:

```bash
python3 -c "
import json
data = json.load(open('/tmp/cprf-competitors-raw.json'))
print(f'Searches run: {len(data[\"competitor_searches\"])}')
for s in data['competitor_searches']:
    print(f'\nQuery: {s[\"query\"]}')
    print(f'Answer: {s.get(\"answer\",\"\")[:400]}')
    for r in s.get('results', [])[:5]:
        print(f'  - {r[\"title\"]} | {r[\"url\"]}')
        print(f'    {r.get(\"content\",\"\")[:200]}')
"
```

**AI instructions:** Read the search results above. Pick exactly 5 competitor companies that:
1. Are named in the search result titles, answers, or snippets
2. Are in the same L3 niche as the product being analyzed
3. Are actual competing products (not agencies, consultancies, or list articles)
4. Are distinct from each other (not the same company under different names)

For each competitor write: `name`, `url` (from the search result where they appeared), `description` (one sentence from snippet), `source_url` (the search result URL where they were found).

---

## Step 5: Competitor Confirmation

**Show the discovered competitors to the user:**

```bash
python3 << 'PYEOF'
import json

analysis = json.load(open('/tmp/cprf-product-analysis.json'))

# FILL: 5 competitors from the search results above
candidates = [
    # {"name": str, "url": str, "description": str, "source_url": str}
]

print(f"\nFound 5 competitors for {analysis['product_name']} in {analysis['industry_taxonomy']['l3']}:\n")
for i, c in enumerate(candidates, 1):
    print(f"  {i}. {c['name']} -- {c['description']}")
    print(f"     {c['url']}")

data = json.load(open('/tmp/cprf-competitors-raw.json'))
data['competitor_candidates'] = candidates
json.dump(data, open('/tmp/cprf-competitors-raw.json', 'w'), indent=2)
PYEOF
```

Tell the user: "These are the 5 competitors I'll research for PR coverage. Add, remove, or swap any -- or say 'looks good' to continue."

**Wait for confirmation.** If the user edits the list (adds/removes/swaps), update the candidates accordingly. Then write the confirmed list:

```bash
python3 << 'PYEOF'
import json

# FILL: confirmed competitor list (after user review)
confirmed = [
    # {"name": str, "url": str}
]

json.dump({"confirmed_competitors": confirmed}, open('/tmp/cprf-competitors-confirmed.json', 'w'), indent=2)
print(f"Confirmed {len(confirmed)} competitors for PR research.")
for c in confirmed:
    print(f"  - {c['name']} ({c['url']})")
PYEOF
```

---

## Step 6: Three-Track PR Research (Phase 2)

```bash
python3 scripts/research.py \
  --phase pr-research \
  --competitors /tmp/cprf-competitors-confirmed.json \
  --product-analysis /tmp/cprf-product-analysis.json \
  --tavily-key "$TAVILY_API_KEY" \
  --output /tmp/cprf-pr-raw.json
```

This runs 3 searches per competitor (15 total):
- **Track A (Editorial):** `"[competitor]" featured press coverage TechCrunch Forbes Wired article interview`
- **Track B (Podcasts):** `"[competitor]" founder CEO podcast interview appeared on episode`
- **Track C (Communities):** `"[competitor]" site:reddit.com OR site:news.ycombinator.com OR site:producthunt.com`

Print coverage summary:

```bash
python3 -c "
import json
data = json.load(open('/tmp/cprf-pr-raw.json'))
print(f'Competitors researched: {data[\"competitors_researched\"]}')
print()
for r in data['results']:
    print(f'{r[\"competitor\"]}:')
    for track, tdata in r['tracks'].items():
        n = len(tdata.get('results', []))
        print(f'  {track:12}: {n} results')
"
```

**If all 3 tracks for a competitor return 0 results:** This competitor has very low press coverage. Note in `data_quality_flags` and proceed -- the cross-competitor pattern will still work with the remaining 4.

---

## Step 7: Pattern Analysis (AI)

Print all raw PR results:

```bash
python3 -c "
import json
data = json.load(open('/tmp/cprf-pr-raw.json'))
for r in data['results']:
    print(f'\n=== {r[\"competitor\"]} ===')
    for track, tdata in r['tracks'].items():
        print(f'\n--- Track {track.upper()} ---')
        print(f'Query: {tdata[\"query\"]}')
        print(f'Answer: {tdata.get(\"answer\",\"\")[:400]}')
        for item in tdata.get('results', [])[:5]:
            print(f'  Title: {item[\"title\"]}')
            print(f'  URL:   {item[\"url\"]}')
            print(f'  Snippet: {item.get(\"content\",\"\")[:200]}')
"
```

**AI instructions:** Read ALL search results above. Build a channel frequency map.

**Step 1 -- Normalize URLs to root domain:** `https://techcrunch.com/2023/06/article-title` → `techcrunch.com`. `https://open.spotify.com/episode/...` → identify as podcast (spotify episode). `https://www.reddit.com/r/devops/` → `reddit.com/r/devops`.

**Step 2 -- Count occurrences:** How many different competitors appeared in results from each channel root? A channel that shows up in Competitor A's Track A AND Competitor B's Track A counts as frequency 2.

**Step 3 -- Tier channels** (follow `references/tier-scoring.md`):
- Tier 1: appeared in 3+ competitors
- Tier 2: appeared in exactly 2 competitors
- Tier 3: appeared in 1 competitor

**Step 4 -- Extract story angles** from article/episode titles in the results. Classify each as: funding-announcement / product-launch / founder-story / trend-piece / category-creation / how-to / comparison / award. Do not infer -- only classify angles visible in the titles.

**Step 5 -- Classify channel type** for each: editorial / podcast / community / newsletter.

Write to `/tmp/cprf-pr-patterns.json`:

```bash
python3 << 'PYEOF'
import json

patterns = {
    "tier_1_channels": [
        # FILL -- channels appearing in 3+ competitors
        # Each: {"channel_name": str, "channel_url": str, "channel_type": str,
        #        "frequency": int, "found_in_competitors": [str],
        #        "evidence_urls": [str], "story_angles_used": [str],
        #        "journalist_name": "", "journalist_beat": ""}
    ],
    "tier_2_channels": [
        # FILL -- channels appearing in exactly 2 competitors
        # Each: {"channel_name": str, "channel_url": str, "channel_type": str,
        #        "frequency": 2, "found_in_competitors": [str], "evidence_urls": [str],
        #        "story_angles_used": [str]}
    ],
    "tier_3_channels": [
        # FILL -- channels appearing in only 1 competitor (name + URL only)
        # Each: {"channel_name": str, "channel_url": str, "found_in_competitor": str}
    ],
    "data_quality_flags": []
}

json.dump(patterns, open('/tmp/cprf-pr-patterns.json', 'w'), indent=2)
PYEOF
```

Verify:

```bash
python3 -c "
import json
p = json.load(open('/tmp/cprf-pr-patterns.json'))
print(f'Tier 1 channels: {len(p[\"tier_1_channels\"])}')
for ch in p['tier_1_channels']:
    print(f'  {ch[\"frequency\"]}x {ch[\"channel_name\"]} ({ch[\"channel_type\"]}) -- {ch[\"found_in_competitors\"]}')
print(f'Tier 2 channels: {len(p[\"tier_2_channels\"])}')
print(f'Tier 3 channels: {len(p[\"tier_3_channels\"])}')
"
```

**If fewer than 3 Tier 1 channels:** This is normal for niche markets. Promote the top Tier 2 channels (highest frequency) to get to at least 3 total channels with deep dives. Note the promotion in `data_quality_flags`.

---

## Step 8: Journalist / Host Lookup

For each Tier 1 channel (up to 7), run one targeted Tavily search:

```bash
python3 << 'PYEOF'
import json, os, urllib.request

patterns = json.load(open('/tmp/cprf-pr-patterns.json'))
analysis = json.load(open('/tmp/cprf-product-analysis.json'))
l2 = analysis['industry_taxonomy']['l2']
l3 = analysis['industry_taxonomy']['l3']
tavily_key = os.environ.get('TAVILY_API_KEY', '')

lookup_results = []

for channel in patterns.get('tier_1_channels', [])[:7]:
    name = channel['channel_name']
    ctype = channel['channel_type']

    if ctype == 'editorial':
        query = f'"{name}" journalist reporter writer covers {l2} {l3} startups technology'
    elif ctype == 'podcast':
        query = f'"{name}" podcast host interviewer {l2} {l3} founders'
    else:
        query = f'"{name}" moderator community manager {l2} {l3}'

    payload = json.dumps({
        "api_key": tavily_key,
        "query": query,
        "search_depth": "basic",
        "max_results": 5
    }).encode()

    req = urllib.request.Request(
        'https://api.tavily.com/search',
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
            lookup_results.append({
                'channel': name,
                'channel_type': ctype,
                'query': query,
                'answer': data.get('answer', ''),
                'results': [
                    {'title': r['title'], 'url': r['url'], 'content': r.get('content', '')[:400]}
                    for r in data.get('results', [])[:3]
                ]
            })
            print(f'Journalist lookup -- {name}: {len(data.get("results", []))} results')
    except Exception as e:
        lookup_results.append({
            'channel': name, 'channel_type': ctype,
            'query': query, 'answer': '', 'results': [], 'error': str(e)
        })
        print(f'Journalist lookup -- {name}: FAILED ({e})')

json.dump(lookup_results, open('/tmp/cprf-journalist-results.json', 'w'), indent=2)
print(f'Journalist lookups complete: {len(lookup_results)} channels')
PYEOF
```

Print results for AI extraction:

```bash
python3 -c "
import json
results = json.load(open('/tmp/cprf-journalist-results.json'))
for r in results:
    print(f'\n=== {r[\"channel\"]} ({r[\"channel_type\"]}) ===')
    print(f'Answer: {r.get(\"answer\",\"\")[:400]}')
    for item in r.get('results', []):
        print(f'  {item[\"title\"]}')
        print(f'  {item.get(\"content\",\"\")[:300]}')
"
```

**AI instructions:** For each Tier 1 channel, extract from the search results above:
- `journalist_name`: the person's name verbatim from a snippet. Write "not found in search data" if absent -- do NOT fill from training knowledge.
- `journalist_beat`: what topics they cover, extracted from snippet text. Write "not found in search data" if absent.

Update `/tmp/cprf-pr-patterns.json` with `journalist_name` and `journalist_beat` populated for each Tier 1 channel:

```bash
python3 << 'PYEOF'
import json

patterns = json.load(open('/tmp/cprf-pr-patterns.json'))

# FILL: update journalist_name and journalist_beat for each tier_1 channel
# journalist_name and journalist_beat come from search snippet text only
# Write "not found in search data" if the snippets don't name a person

# Example:
# patterns['tier_1_channels'][0]['journalist_name'] = 'Ingrid Lunden'
# patterns['tier_1_channels'][0]['journalist_beat'] = 'enterprise software and developer tools'

json.dump(patterns, open('/tmp/cprf-pr-patterns.json', 'w'), indent=2)
print('Journalist data updated.')
for ch in patterns['tier_1_channels']:
    print(f"  {ch['channel_name']}: {ch.get('journalist_name','--')} | {ch.get('journalist_beat','--')}")
PYEOF
```

---

## Step 9: Synthesis -- Generate Outreach Packages (AI)

Print consolidated data:

```bash
python3 -c "
import json

analysis = json.load(open('/tmp/cprf-product-analysis.json'))
patterns = json.load(open('/tmp/cprf-pr-patterns.json'))

print('=== PRODUCT ===')
print(f'Name: {analysis[\"product_name\"]}')
print(f'What it does: {analysis[\"one_line_description\"]}')
print(f'Differentiators:')
for d in analysis['differentiators']:
    print(f'  - {d}')
print(f'ICP: {analysis[\"icp\"]}')
print(f'Geography: {analysis[\"geography_bias\"]}')
print()
print('=== TIER 1 CHANNELS ===')
for ch in patterns['tier_1_channels']:
    print(f'\n{ch[\"channel_name\"]} ({ch[\"channel_type\"]}, freq={ch[\"frequency\"]})')
    print(f'  Found in: {ch[\"found_in_competitors\"]}')
    print(f'  Evidence URLs: {ch[\"evidence_urls\"][:3]}')
    print(f'  Story angles: {ch[\"story_angles_used\"]}')
    print(f'  Journalist: {ch.get(\"journalist_name\",\"not found\")} | {ch.get(\"journalist_beat\",\"\")}')
print()
print('=== TIER 2 CHANNELS ===')
for ch in patterns['tier_2_channels']:
    print(f'  {ch[\"channel_name\"]} ({ch[\"channel_type\"]}) -- found in {ch[\"found_in_competitors\"]}')
"
```

**AI instructions -- zero-hallucination rules:**

1. **Channel names:** Only include channels from `/tmp/cprf-pr-patterns.json`. No invented channels.
2. **Journalist/host names:** Use only what was populated in Step 8. Write "not found in search data" if blank. Do NOT substitute from training knowledge.
3. **Story angles:** Use only angles extracted from article/episode titles in the search results. Do not infer from training knowledge.
4. **Cold pitch drafts:** Must reference (a) a specific story angle from the evidence, (b) at least one specific differentiator from the product analysis, (c) the journalist's beat if found. No generic "we'd love to be featured" or "our product is revolutionary" language.
5. **Channel overview:** 1-2 sentences from search snippets only. Write "not found in search data" if the snippets don't describe the channel's coverage focus.
6. **Bonus hooks:** 3 angles that your competitors did NOT use in their coverage. These must be grounded in the product's actual differentiators from Step 4 -- not generic advice.
7. No em dashes. No banned words (powerful, seamless, game-changing, revolutionary, cutting-edge, leverage, transform).

**Per Tier 1 channel generate:**
- `channel_overview`: 1-2 sentences about coverage focus (from snippets)
- `why_they_covered_competitors`: specific angle extracted from evidence titles
- `journalist_name` + `journalist_beat`
- `approach_method`: cold email / podcast pitch form / community post / LinkedIn DM (based on channel type)
- `cold_pitch_draft`:
  - `subject`: "[Journalist name]: [their beat] + [your specific angle]"
  - `body`: 3-4 sentences. Structure: hook (reference their past coverage of a competitor) + what you do (one sentence) + why it fits their beat (tie to a specific differentiator) + ask (clear, low-friction CTA)

**Also generate `bonus_hooks`**: 3 pitch angles not used by any competitor in the search results. Base each on a specific product differentiator.

Write to `/tmp/cprf-final.json`:

```bash
python3 << 'PYEOF'
import json

result = {
    "product_summary": {
        # FILL from analysis
    },
    "competitors_researched": [],  # FILL: names of confirmed competitors
    "tier_1_deep_dives": [
        # FILL per tier 1 channel:
        # {
        #   "channel_name": str,
        #   "channel_type": str,  # editorial / podcast / community
        #   "frequency": int,
        #   "found_in_competitors": [str],
        #   "evidence_urls": [str],
        #   "channel_overview": str,
        #   "why_they_covered_competitors": str,
        #   "story_angles_used": [str],
        #   "journalist_name": str,
        #   "journalist_beat": str,
        #   "approach_method": str,
        #   "cold_pitch_draft": {"subject": str, "body": str}
        # }
    ],
    "tier_2_channels": [
        # FILL: {channel_name, channel_type, frequency, found_in_competitors, evidence_urls}
    ],
    "tier_3_channels": [
        # FILL: {channel_name, found_in_competitor}
    ],
    "bonus_hooks": [
        # FILL: 3 strings -- pitch angles not used by competitors
    ],
    "data_quality_flags": []
}

json.dump(result, open('/tmp/cprf-final.json', 'w'), indent=2)
print(f'Synthesis written.')
print(f'Tier 1 deep dives: {len(result.get("tier_1_deep_dives", []))}')
print(f'Bonus hooks: {len(result.get("bonus_hooks", []))}')
PYEOF
```

---

## Step 10: Self-QA, Present, and Save

**Self-QA:**

```bash
python3 << 'PYEOF'
import json

result = json.load(open('/tmp/cprf-final.json'))
failures = []

# Check 1: em dashes
full_text = json.dumps(result)
if '—' in full_text:
    result = json.loads(full_text.replace('—', '-'))
    failures.append('Fixed: em dashes replaced with hyphens')

# Check 2: banned words
banned = ['powerful', 'seamless', 'innovative', 'game-changing', 'revolutionize',
          'excited to announce', 'cutting-edge', 'best-in-class', 'world-class',
          'leverage', 'transform', 'disrupt']
for word in banned:
    if word.lower() in json.dumps(result).lower():
        failures.append(f'Warning: banned word "{word}" found in output -- review before presenting')

# Check 3: cold pitch subjects exist
for dd in result.get('tier_1_deep_dives', []):
    pitch = dd.get('cold_pitch_draft', {})
    if not pitch.get('subject') or len(pitch.get('subject', '')) < 10:
        dd['cold_pitch_draft']['subject'] = 'not generated'
        failures.append(f'Fixed: missing subject line for {dd.get("channel_name")}')
    if not pitch.get('body') or len(pitch.get('body', '')) < 50:
        failures.append(f'Warning: very short pitch body for {dd.get("channel_name")}')

# Check 4: bonus hooks count
if len(result.get('bonus_hooks', [])) != 3:
    failures.append(f'Expected 3 bonus hooks, got {len(result.get("bonus_hooks", []))}')

# Check 5: "not found in search data" count
nf_count = json.dumps(result).count('not found in search data')
if nf_count > 0:
    failures.append(f'INFO: {nf_count} field(s) marked "not found in search data" -- verify before outreach')

# Check 6: tier 1 channels have evidence URLs
for ch in result.get('tier_1_deep_dives', []):
    if not ch.get('evidence_urls'):
        failures.append(f'Warning: {ch["channel_name"]} has no evidence_urls')

if 'data_quality_flags' not in result:
    result['data_quality_flags'] = []
result['data_quality_flags'].extend(failures)

json.dump(result, open('/tmp/cprf-final.json', 'w'), indent=2)
print(f'QA complete. {len(failures)} issues addressed.')
for f in failures:
    print(f'  - {f}')
if not failures:
    print('All QA checks passed.')
PYEOF
```

**Present the output:**

```
## PR Intel: [product_name]
Date: [today] | Competitors researched: [N] | Tier 1 channels: [N] | Tier 2 channels: [N]

---

### Your Product
[one_line_description]
Differentiators: [list]
Competitors researched: [names]

---

### Tier 1 Channels (Proven Beats -- Found in 3+ Competitors)

*These channels have already covered multiple companies in your space.*

| Channel | Type | Found in | Journalist/Host | Approach |
|---|---|---|---|---|
[one row per tier 1 channel]

---

### Deep Dives + Cold Pitches

#### 1. [Channel Name] (Tier 1 -- [Type], found in [N] competitors)

Covers: [channel_overview]
Covered competitors: [found_in_competitors with evidence URLs]
Story angle they used: [why_they_covered_competitors]
Journalist/Host: [journalist_name] | Beat: [journalist_beat]
How to reach: [approach_method]

**Cold pitch:**
Subject: [subject]

[body -- 3-4 sentences]

---

[repeat for each tier 1 channel]

---

### Tier 2 Channels (Warm -- Found in 2 Competitors)

| Channel | Type | Found in | URL |
|---|---|---|---|
[one row per tier 2 channel]

---

### Tier 3 Channels (Discovery -- Found in 1 Competitor)

[comma-separated list of channel names with URLs]

---

### 3 Bonus Hooks (Angles Your Competitors Didn't Use)

1. [hook_text]
2. [hook_text]
3. [hook_text]

---
Data notes: [data_quality_flags, or "None"]
Saved to: docs/pr-intel/[PRODUCT_SLUG]-[DATE].md
```

**Save to file and clean up:**

```bash
DATE=$(date +%Y-%m-%d)
OUTPUT_FILE="docs/pr-intel/${PRODUCT_SLUG}-${DATE}.md"
mkdir -p docs/pr-intel
echo "Saved to: $OUTPUT_FILE"
```

```bash
rm -f /tmp/cprf-product-raw.md /tmp/cprf-product-analysis.json \
      /tmp/cprf-competitors-raw.json /tmp/cprf-competitors-confirmed.json \
      /tmp/cprf-pr-raw.json /tmp/cprf-pr-patterns.json \
      /tmp/cprf-journalist-results.json /tmp/cprf-final.json
echo "Temp files cleaned up."
```
