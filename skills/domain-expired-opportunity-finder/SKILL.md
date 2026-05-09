---
name: domain-expired-opportunity-finder
description: Evaluates expired domain candidates against a target niche, scores them by topical relevance, historical activity level, and history cleanliness, then outputs a ranked shortlist with explainable reasoning and risk flags.
compatibility: [claude-code, gemini-cli, github-copilot]
author: ajaycodesitbetter
version: 1.0.0
---

# Expired Domain Opportunity Finder

Evaluate expired domain candidates for a specific niche. Score them on topical
fit, historical activity level, history cleanliness, and redirect suitability. Output a
conservative, explainable shortlist for human review.

---

**Critical rule:** Every recommendation must include BOTH a positive rationale
(`why_selected`) AND a caution rationale (`why_risky`). Never output a bare
score without explanation.

**Conservative-by-default rule:** When signals are incomplete or contradictory,
lower the confidence level. Do not surface ambiguous candidates as strong
opportunities. Missing data reduces confidence, never inflates it.

**Anti-abuse rule:** Never encourage unrelated redirects, PBN construction, or
domain repurposing where the historical topic does not match the target niche.
Read `references/guardrails.md` for the full anti-abuse policy.

---

## Step 1: Setup Check

Check the environment before doing anything else.

Verify that `curl` and `python3` (or `python`) are available:
```bash
curl --version > /dev/null 2>&1 && echo "curl: available" || echo "curl: MISSING"
python3 --version 2>/dev/null || python --version 2>/dev/null || echo "python: MISSING"
```

Check for an optional LLM API key for enhanced niche-relevance scoring:
```bash
echo "LLM_API_KEY: ${LLM_API_KEY:+set}"
```

**If `curl` or `python` is missing:**
Stop. Tell the user: "This skill requires curl and Python 3.10+. Please install them and try again."

**If `LLM_API_KEY` is not set:**
Continue. The skill will use rule-based scoring only (domain string matching,
Wayback title analysis, keyword overlap). Note to the user: "Running in
rule-based-only mode. Set LLM_API_KEY for enhanced niche-relevance scoring."

**If `LLM_API_KEY` is set:**
The skill will use LLM-enhanced scoring for topical relevance analysis.
This provides deeper contextual assessment of niche fit.

QA: State the scoring mode (llm-enhanced or rule-based-only) and confirm tools are available.

---

## Step 2: Input Collection

Collect the required and optional inputs from the user.

**Required:**
- `target_niche` (string): The core niche to evaluate against. Examples: "developer tools", "AI SaaS", "cybersecurity", "fintech".

**Optional (ask only if not provided):**
- `seed_keywords` (array): Keywords to refine topical matching. If not provided, extract 3–5 keywords from the niche name automatically.
- `candidate_domains` (array): Specific domains to evaluate. If not provided, prompt the user.
- `discovery_source` (string): Where candidates came from — `manual`, `expireddomains-net`, `external-feed`.
- `min_snapshots` (integer): Minimum historical snapshot threshold. Default: 10.
- `max_risk_level` (string): `low`, `medium`, or `high`. Controls how aggressively risky candidates are filtered. Default: `medium`.
- `intended_use` (string): `rebuild`, `redirect`, or `either`. Default: `either`.

**If no `candidate_domains` are provided:**
Ask: "Please provide a list of expired domain candidates to evaluate. You can:
1. Paste domain names (one per line or comma-separated)
2. Provide a file path to a text file with one domain per line
3. Say 'example' to run with a built-in demo set for the 'developer tools' niche"

**If the user says 'example':**
Use this demo set:
```
devtoolsweekly.com
codeshipnews.io
stackforgeapp.com
quickseorank.net
bestcheaphosting247.com
cloudbuildpro.dev
reactwidgetlib.com
megadealsshop.xyz
```

After collecting all inputs, confirm:
"Target niche: [niche]. Evaluating [N] candidate domains. Scoring mode: [mode]. Intended use: [use]."

---

## Step 3: Candidate Normalization

Clean and validate the candidate list before scoring.

```bash
python3 -c "
import sys, re

domains = '''CANDIDATE_LIST_HERE'''.strip().split('\n')
seen = set()
valid = []
invalid = []

for d in domains:
    d = d.strip().lower()
    # Strip protocols and paths
    d = re.sub(r'^https?://', '', d)
    d = d.split('/')[0]
    d = d.strip('.')

    if not d:
        continue

    # Basic TLD validation
    if '.' not in d or len(d) < 4:
        invalid.append(d)
        continue

    # Deduplicate
    if d in seen:
        continue
    seen.add(d)
    valid.append(d)

print(f'Valid candidates: {len(valid)}')
print(f'Removed (invalid/duplicate): {len(invalid)}')
for v in valid:
    print(f'  ✓ {v}')
for i in invalid:
    print(f'  ✗ {i} (invalid format)')
"
```

Replace `CANDIDATE_LIST_HERE` with the actual domain list from Step 2.

State: "[N] valid candidates after normalization. [M] removed (invalid/duplicate)."

If 0 valid candidates remain, stop and tell the user: "No valid domain candidates found. Please provide domain names in the format 'example.com'."

---

## Step 4: Signal Collection

For each valid candidate, collect signals from free public sources.
Run these checks sequentially per domain.

### 4a: Wayback CDX API — History Snapshots

Query the Wayback Machine for all historical snapshots. We use `limit=100000`
and explicit `from`/`to` parameters are intentionally omitted so that CDX
returns snapshots from the full lifetime of the domain. The results are sorted
ascending by timestamp (oldest first) so `first_capture` and `last_capture`
are accurate:

```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=DOMAIN_HERE&output=json&fl=timestamp,statuscode&collapse=timestamp:6&limit=100000" \
  | python3 -c "
import sys, json

try:
    data = json.load(sys.stdin)
    if len(data) <= 1:
        print(json.dumps({'domain': 'DOMAIN_HERE', 'snapshots': 0, 'first_capture': None, 'last_capture': None, 'status_codes': {}, 'years_active': 0}))
    else:
        rows = data[1:]  # skip header row
        timestamps = [r[0] for r in rows]  # already ascending (oldest first)
        statuses = [r[1] for r in rows]
        status_counts = {}
        for s in statuses:
            status_counts[s] = status_counts.get(s, 0) + 1
        first_year = int(timestamps[0][:4])
        last_year = int(timestamps[-1][:4])
        print(json.dumps({
            'domain': 'DOMAIN_HERE',
            'snapshots': len(rows),
            'first_capture': timestamps[0],
            'last_capture': timestamps[-1],
            'status_codes': status_counts,
            'years_active': last_year - first_year + 1
        }))
except:
    print(json.dumps({'domain': 'DOMAIN_HERE', 'snapshots': 0, 'error': 'wayback_api_failed'}))
"
```

**Rate limiting:** Wait 2 seconds between Wayback API calls to be polite to the service.

### 4b: Wayback Content Sampling — Historical Page Titles

For candidates with > 0 snapshots, fetch the most recent snapshot to extract
the page title (used for topical relevance scoring):

```bash
curl -s -L "https://web.archive.org/web/LATEST_TIMESTAMP/http://DOMAIN_HERE" \
  | python3 -c "
import sys, re
html = sys.stdin.read()[:50000]
title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
title = title_match.group(1).strip() if title_match else 'no title found'
# Extract meta description too
meta_match = re.search(r'<meta[^>]*name=[\"']description[\"'][^>]*content=[\"'](.*?)[\"']', html, re.IGNORECASE)
desc = meta_match.group(1).strip() if meta_match else 'no description found'
print(f'Title: {title}')
print(f'Description: {desc}')
"
```

Replace `LATEST_TIMESTAMP` with the most recent timestamp from Step 4a.

### 4c: RDAP Lookup — Registration Status

Use the cross-platform HTTP-based RDAP standard (replaces OS-dependent WHOIS).
An HTTP 404 from RDAP means the domain is not registered (i.e. it is genuinely
available or untracked) — that is distinct from a network failure. Handle both
cases explicitly:

```bash
python3 -c "
import urllib.request, urllib.error, json

domain = 'DOMAIN_HERE'
try:
    req = urllib.request.Request(
        f'https://rdap.org/domain/{domain}',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode())

    registrar = 'unknown'
    created = 'unknown'

    for entity in data.get('entities', []):
        if 'registrar' in entity.get('roles', []):
            try:
                registrar = entity.get('vcardArray', [[]])[1][0][3]
            except Exception:
                pass

    for event in data.get('events', []):
        if event.get('eventAction') == 'registration':
            created = event.get('eventDate', 'unknown')

    print(json.dumps({
        'domain': domain,
        'status': 'registered',
        'registrar': registrar,
        'created': created
    }))
except urllib.error.HTTPError as e:
    if e.code == 404:
        # Domain has no RDAP object — likely unregistered or not in RDAP coverage
        print(json.dumps({'domain': domain, 'status': 'unregistered_or_no_rdap_object'}))
    else:
        print(json.dumps({'domain': domain, 'error': f'rdap_http_error_{e.code}'}))
except Exception:
    print(json.dumps({'domain': domain, 'error': 'rdap_lookup_failed'}))
"
```

### 4d: Domain String Analysis — Keyword Matching

Score keyword overlap between the domain name and the target niche / seed keywords:

```bash
python3 -c "
import re, json

domain = 'DOMAIN_HERE'
niche = 'NICHE_HERE'
seeds = SEEDS_JSON_HERE  # e.g., ['devops', 'ci/cd', 'code editor']

# Extract words from domain
domain_base = domain.rsplit('.', 1)[0]  # remove TLD
domain_words = re.split(r'[-_.]', domain_base.lower())

# Check niche words
niche_words = niche.lower().split()
all_keywords = set(niche_words + [s.lower() for s in seeds])

matches = [w for w in domain_words if any(kw in w or w in kw for kw in all_keywords)]
match_ratio = len(matches) / max(len(domain_words), 1)

print(json.dumps({
    'domain': domain,
    'domain_words': domain_words,
    'keyword_matches': matches,
    'match_ratio': round(match_ratio, 2)
}))
"
```

### 4e: Gemini LLM Niche-Relevance Assessment (if LLM_API_KEY is set)

If the LLM API key is configured, batch all candidates with their collected
signals and ask for a contextual niche-relevance assessment.

**Note:** The request/response format below uses the **Gemini API** (`generateContent`
format). It is not compatible with OpenAI-style endpoints without modification.
If you use a different provider, you must adapt the JSON body and response parsing.

```bash
cat > /tmp/domain-relevance-request.json << 'ENDJSON'
{
  "system_instruction": {
    "parts": [{
      "text": "You are an SEO research analyst. For each expired domain candidate provided, assess its topical relevance to the specified target niche. Consider the domain name, historical page title, and meta description. For each domain, output a JSON object with: domain (string), relevance_score (integer 1-10), relevance_rationale (one sentence explaining the score), redirect_plausibility (integer 1-10), redirect_rationale (one sentence). Output only a JSON array. No commentary before or after."
    }]
  },
  "contents": [{
    "parts": [{
      "text": "DOMAIN_SIGNALS_AND_NICHE_CONTEXT_HERE"
    }]
  }],
  "generationConfig": {
    "temperature": 0.2,
    "maxOutputTokens": 2048
  }
}
ENDJSON
```

Replace `DOMAIN_SIGNALS_AND_NICHE_CONTEXT_HERE` with:
- The target niche and seed keywords
- For each candidate: domain name, historical title, description, keyword match data

Send the request to the Gemini API:

```bash
curl -s -X POST \
  "${LLM_API_ENDPOINT:-https://generativelanguage.googleapis.com/v1beta}/models/${LLM_MODEL:-gemini-2.0-flash}:generateContent?key=$LLM_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/domain-relevance-request.json \
  | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    text = d['candidates'][0]['content']['parts'][0]['text']
    print(text)
except (KeyError, IndexError, json.JSONDecodeError) as e:
    print(json.dumps({'error': 'llm_response_parse_failed', 'detail': str(e)}))
"
```

If the LLM call or response parsing fails, log the error and continue with
rule-based scoring only. Do not stop the workflow.

After all signal collection, state:
"Signal collection complete for [N] candidates. [M] Wayback hits, [K] RDAP lookups succeeded."

---

## Step 5: Scoring & Classification

Read `references/scoring-model.md` for the full scoring framework.

For each candidate, compute scores across the 6 dimensions:

1. **Topical Relevance (0–30):** Combine domain keyword match ratio, historical
   title/description analysis, and LLM relevance score (if available). Without
   LLM: use keyword match ratio × 15 + title keyword overlap × 15. With LLM:
   use LLM relevance_score × 3.

2. **Historical Activity Level (0–25):** Based on Wayback snapshot diversity and
   frequency. More snapshots consistently captured across multiple years indicates
   higher sustained activity and inferred legitimacy.

3. **Historical Content Quality (0–15):** Derived from historical page title and
   meta description analysis, checking for natural phrasing versus keyword
   stuffing. Without LLM: base score of 8/15 adjusted by exact-match density.

4. **History Cleanliness (0–15):** Based on Wayback snapshot count, years active,
   status code consistency, and absence of parking page indicators.

5. **Redirect Suitability (0–10):** Based on topic continuity between historical
   content and target niche. Use LLM redirect_plausibility score if available;
   otherwise use keyword overlap ratio.

6. **Signal Completeness (0–5):** Count how many data sources returned usable
   data (Wayback, RDAP, domain analysis, LLM if configured).

**Compute:**
- `opportunity_score` = sum of all dimension scores (0–100)
- `confidence` = based on how many dimensions have strong data (see scoring-model.md)
- `recommended_action` = based on score + confidence + risk flags (see Step 6)

---

## Step 6: Risk Flagging & Filtering

Read `references/risk-flags.md` for the complete flag definitions.

Apply risk flags to each candidate:

| Check | Flag Applied |
|---|---|
| Historical topic overlap < 30% with target niche | `topic_mismatch` |
| Domain active < 1 year before expiry | `short_history` |
| < 3 Wayback snapshots or all parking pages | `unclear_history` |
| Sudden Wayback drop-off after years of activity | `possible_deindex` |
| Snapshot count below `min_snapshots` | `weak_historical_activity` |
| Redirect suitability < 4/10 | `redirect_mismatch` |

**Apply recommendation logic:**

| Score + Flags | Recommendation |
|---|---|
| Score ≥ 75 AND confidence `high` AND no High-severity flags | `high-priority-review` |
| Score ≥ 55 AND confidence ≥ `medium` | `review` |
| Score ≥ 55 BUT redirect_suitability < 4/10 | `rebuild-only-review` |
| Score < 55 OR any critical High-severity flag | `reject` |

**Apply `max_risk_level` filter:**
- If `max_risk_level` = `low`: exclude any candidate with Medium or High flags
- If `max_risk_level` = `medium`: exclude candidates with High flags only
- If `max_risk_level` = `high`: include all candidates (no filter)

---

## Step 7: Output & Save

Read `references/output-format.md` for the exact JSON schema.
Read `references/guardrails.md` for the required disclaimer text.

**Default: Shortlist mode.** Show only candidates with `recommended_action`
of `high-priority-review`, `review`, or `rebuild-only-review`.

If the user requested audit mode, show ALL candidates with full dimension
breakdowns including rejection reasons.

### Present the output:

```
## Expired Domain Opportunity Finder — [YYYY-MM-DD]

**Target niche:** [niche]
**Seed keywords:** [keywords]
**Intended use:** [rebuild/redirect/either]
**Candidates evaluated:** [N]
**Shortlisted:** [M]
**Rejected:** [K]
**Scoring mode:** [llm-enhanced / rule-based-only]

---

### 1. [domain.com] — Score: [N]/100 | Confidence: [level] | Action: [recommendation]

**Topical fit:** [summary]
**Activity level:** [summary]
**Content quality:** [summary]
**History:** [summary]
**Redirect suitability:** [level]
**Risk flags:** [flags or "none"]

**Why selected:** [rationale]
**Why risky:** [rationale]

---

[repeat for each shortlisted domain, ranked by opportunity_score descending]

---

**Disclaimer:** These results are research recommendations, not guarantees
of SEO value. Redirect analysis should only be considered when strong
topic continuity exists between the expired domain and your target site.
Search engine algorithms change frequently. Always perform manual due
diligence — including checking current index status, reviewing the full
backlink profile with a commercial tool, and verifying domain history —
before making any acquisition decision. This skill does not endorse or
facilitate manipulative SEO practices.
```

**Save the structured JSON output:**
```bash
mkdir -p docs/expired-domain-intel
OUTFILE="docs/expired-domain-intel/$(date +%Y-%m-%d).json"
cat > "$OUTFILE" << 'EOF'
JSON_OUTPUT_HERE
EOF
echo "Saved to $OUTFILE"
```

**If 0 candidates pass the shortlist:**
"No candidates met the shortlist criteria for the '[niche]' niche with the
current risk tolerance. This is a normal outcome — it means the evaluated
domains were not strong enough matches. Try:
1. Providing different candidate domains
2. Widening seed keywords
3. Setting max_risk_level to 'high' to see borderline candidates
4. Running in audit mode to see why candidates were rejected"

---

## Self-QA Checklist

Run every check before presenting output:

- [ ] Every shortlisted domain has both `why_selected` AND `why_risky`
- [ ] No shortlisted domain has a High-severity risk flag AND `high-priority-review` action
- [ ] Domains with `redirect_mismatch` are labeled `rebuild-only-review` (not `review`)
- [ ] The guardrails disclaimer is present at the end of output
- [ ] No hype language: no "guaranteed", "easy win", "safe to redirect", "SEO hack"
- [ ] `scoring_mode` correctly reflects whether LLM was used
- [ ] Candidates are ranked by `opportunity_score` descending
- [ ] JSON output saved to `docs/expired-domain-intel/YYYY-MM-DD.json`
- [ ] All Wayback API calls were rate-limited (2s between calls)

Fix any violation before presenting.

---

## What Good Output Looks Like

- Every domain has a score, confidence, action, and risk assessment
- Summaries are 1–2 sentences each, specific to the candidate (not generic)
- Risk flags are present and explained in `why_risky`
- The shortlist is small (quality over quantity) — typically 2–5 domains from a batch of 10–20
- Conservative: when in doubt, reject or lower confidence
- The user can understand exactly why each domain was selected or rejected

## What Bad Output Looks Like

- Bare scores without explanation
- Generic summaries like "this domain has good metrics" (must be specific)
- High-priority recommendations for domains with serious risk flags
- Redirect recommendations for topic-mismatched domains
- No disclaimer at the end
- Hype language promising SEO outcomes
- Too many shortlisted domains (the skill should be selective, not permissive)
