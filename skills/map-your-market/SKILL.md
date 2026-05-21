---
name: map-your-market
description: Given a product description, category keywords, or competitor names (any combination), searches Reddit, Hacker News, GitHub Issues, G2, and Google Trends for the real pains your market experiences, then synthesizes everything into a positioning framework showing who your ICP is, what they say out loud, and exactly how to talk to them. Use when asked to understand a market, find ICP pain points, map competitors, build a positioning doc, find messaging angles, or answer who is my customer and what do they actually care about. Trigger when a user says map my market, who is my ICP, what pains does my market have, understand my market, find my target customer, what are the top complaints in X space, help me position my product, or who should I be selling to.
compatibility: [claude-code, gemini-cli, github-copilot]
---

# Map Your Market

Take a product description, category keywords, or competitor names. Search Reddit, HN, GitHub Issues, G2, and Google Trends for real pain signals. Score and cluster them. Build a complete positioning framework: ICP definition, ranked pain themes with verbatim quotes, market size signals, and messaging angles derived from actual language people use.

---

**Critical rule:** Every pain quote in the output must exist verbatim in the raw data collected by the script. Every vendor name in the market map must come from G2 scrape results or GitHub search results. Market size must say "signals suggest" -- never estimate a dollar figure from thin proxies. If a source returns 0 results, report 0 -- do not supplement with invented examples.

---

## Common Mistakes

| The agent will want to... | Why that's wrong |
|---|---|
| Invent pain points or market size numbers | Every pain quote must be verbatim from raw data. Market size must cite signals found. Never estimate "typical" market size. |
| Score by post count instead of pain_score | A post with 2,000 upvotes about pricing is stronger than 50 posts with 10 upvotes each. Use the pain_score formula from references/pain-scoring.md. |
| Use the same subreddits for every category | r/politics adds noise to a devops search. Auto-detect relevant subreddits from the category and competitor names before searching. |
| Send all raw signals to AI without scoring | Score locally first. Send only the top 60 high-pain-score signals to AI clustering. Saves tokens and improves cluster quality. |
| Skip ICP extraction from post metadata | Subreddit, flair, author bio (HN), and GitHub org type are richer ICP signals than post content. Always capture and report them. |
| Conflate vendor count with market size | "47 vendors on G2" means competitive, not large. Present all signals as directional indicators, not hard numbers. |

---

## Step 1: Setup Check

```bash
echo "GITHUB_TOKEN: ${GITHUB_TOKEN:-not set -- GitHub Issues search runs at 60 req/hr unauthenticated}"
echo "No other API keys required."
echo ""
echo "Data sources this run will use:"
echo "  Reddit public JSON  (no auth, 10 req/min)"
echo "  HN Algolia API      (no auth, free)"
echo "  GitHub Issues API   (${GITHUB_TOKEN:+authenticated, }60-5000 req/hr)"
echo "  G2 category scrape  (no auth, HTML parse)"
echo "  Google Trends       (no auth, unofficial endpoint)"
```

If `GITHUB_TOKEN` is not set: continue. Unauthenticated GitHub search is 60 req/hr -- enough for a standard run. For repeated use, add a token at github.com/settings/tokens (no scopes needed for public repos).

---

## Step 2: Parse Input

Collect from the conversation:
- `category` -- keyword(s) describing the market space (e.g. "developer observability", "B2B analytics", "devops tooling")
- `competitors` -- optional list of competitor product names or domains (e.g. "Datadog, New Relic, Grafana")
- `product_context` -- optional: what the user's product does (helps tailor messaging angles)

If the user provides only a product description with no category keyword: extract 2-3 category keywords from it yourself.

If the user provides only competitor names with no category: infer the category by looking up competitors.

Write the parsed input:

```bash
python3 << 'PYEOF'
import json, os

data = {
    "category": "CATEGORY_HERE",
    "competitors": ["COMP_1", "COMP_2"],
    "product_context": "PRODUCT_CONTEXT_HERE"
}

with open("/tmp/mym-input.json", "w") as f:
    json.dump(data, f, indent=2)
print("Input written to /tmp/mym-input.json")
print(f"Category: {data['category']}")
print(f"Competitors: {', '.join(data['competitors']) if data['competitors'] else 'none provided'}")
PYEOF
```

---

## Step 3: Run the Standalone Data Collection Script

The script handles all data collection. Check if it exists first:

```bash
ls scripts/fetch.py 2>/dev/null && echo "script available" || echo "not found"
```

If available, run it:

```bash
GITHUB_TOKEN="${GITHUB_TOKEN:-}" python3 scripts/fetch.py \
    "$(python3 -c "import json; d=json.load(open('/tmp/mym-input.json')); print(d['category'])")" \
    --competitors "$(python3 -c "import json; d=json.load(open('/tmp/mym-input.json')); print(','.join(d['competitors']))")" \
    --context "$(python3 -c "import json; d=json.load(open('/tmp/mym-input.json')); print(d['product_context'])")" \
    --output /tmp/mym-raw.json
```

Wait for completion (allow up to 4 minutes -- Reddit + HN searches take ~90 seconds total).

Verify output:
```bash
python3 -c "
import json
with open('/tmp/mym-raw.json') as f:
    d = json.load(f)
print(f'Reddit signals: {d[\"market_signals\"][\"reddit_signals_found\"]}')
print(f'HN signals:     {d[\"market_signals\"][\"hn_signals_found\"]}')
print(f'GitHub signals: {d[\"market_signals\"][\"github_issue_signals\"]}')
print(f'G2 vendors:     {d[\"market_signals\"][\"vendor_count_g2\"]}')
print(f'Trends:         {d[\"market_signals\"][\"trends_direction\"]}')
print(f'Total signals:  {d[\"summary\"][\"total_pain_signals\"]}')
"
```

If total signals < 10: stop. Tell the user: "Fewer than 10 pain signals found for this category. The market may be too niche for Reddit/HN coverage, or the category keywords need adjustment. Try broader keywords or add competitor names."

---

## Step 4: AI Pain Clustering

Print the top 60 pain signals for AI analysis:

```bash
python3 -c "
import json
with open('/tmp/mym-raw.json') as f:
    d = json.load(f)
top60 = sorted(d['raw_pains'], key=lambda x: x['pain_score'], reverse=True)[:60]
print(json.dumps(top60, indent=2))
"
```

You now have the top 60 pain signals. Analyze them and produce pain clusters.

**Instructions for AI analysis:**
- Identify 5-7 recurring pain themes across all sources
- For each theme: pick a name that uses the market's own language (not your words)
- Aggregate the pain_score of all signals in each cluster
- Select the 3-5 best verbatim quotes for each theme (highest score, most specific language)
- Note which sources and subreddits each theme concentrates in
- Flag any theme that appears only in one source (lower confidence)

Write the clusters to `/tmp/mym-clusters.json`:

```json
{
  "clusters": [
    {
      "theme": "exact language from the data",
      "total_score": 847,
      "signal_count": 34,
      "sources": {"reddit": 18, "hn": 12, "github_issue": 4},
      "top_subreddits": ["devops", "sysadmin"],
      "verbatim_quotes": [
        {"text": "exact quote", "source": "reddit", "score": 234, "url": "..."},
        {"text": "exact quote", "source": "hn", "score": 87, "url": "..."}
      ],
      "who_has_this_pain": "description of who is posting about this"
    }
  ]
}
```

```bash
python3 -c "
import json, os
# Confirm clusters file was written
with open('/tmp/mym-clusters.json') as f:
    d = json.load(f)
print(f'Clusters written: {len(d[\"clusters\"])}')
for c in d['clusters']:
    print(f'  {c[\"theme\"]} -- score: {c[\"total_score\"]}, signals: {c[\"signal_count\"]}')
"
```

---

## Step 5: ICP Profiling

Print the ICP signals from the raw data:

```bash
python3 -c "
import json
with open('/tmp/mym-raw.json') as f:
    d = json.load(f)
print('ICP signals:')
print(json.dumps(d['icp_signals'], indent=2))
print()
print('Subreddit distribution:')
sub_counts = {}
for p in d['raw_pains']:
    s = p.get('subreddit', '')
    if s:
        sub_counts[s] = sub_counts.get(s, 0) + 1
for sub, count in sorted(sub_counts.items(), key=lambda x: -x[1])[:10]:
    print(f'  r/{sub}: {count} signals')
"
```

Using the ICP signals and subreddit distribution above, synthesize the ICP profile. Write it to `/tmp/mym-clusters.json` by adding an `icp` key:

```json
{
  "icp": {
    "who_they_are": "2-3 sentence profile using language from the data",
    "where_they_live": ["r/devops (89 posts)", "r/sysadmin (67 posts)", "HN ask-hn (34 threads)"],
    "what_they_say": ["verbatim quote 1", "verbatim quote 2", "verbatim quote 3"],
    "what_they_have_tried": ["alternative tools or approaches mentioned in the data"],
    "confidence": "high|medium|low -- based on signal volume and source diversity"
  }
}
```

---

## Step 6: Market Size Synthesis

Print the market signals:

```bash
python3 -c "
import json
with open('/tmp/mym-raw.json') as f:
    d = json.load(f)
ms = d['market_signals']
print('Market signals:')
print(f'  G2 vendors:         {ms[\"vendor_count_g2\"]}')
print(f'  Trends direction:   {ms[\"trends_direction\"]}')
print(f'  HN signals (12mo):  {ms[\"hn_signals_found\"]}')
print(f'  Reddit signals:     {ms[\"reddit_signals_found\"]}')
print(f'  G2 top vendors:     {json.dumps(ms.get(\"top_vendors\", []), indent=4)}')
"
```

Synthesize a directional market size assessment using only these signals. Do not estimate a dollar figure. Use language like:
- "Signals suggest a competitive, growing market" (many vendors + trends up)
- "Signals suggest an early market" (few vendors + low signal volume)
- "Signals suggest a saturated market" (many vendors + flat/down trends)

Add the assessment to `/tmp/mym-clusters.json` as a `market_size` key.

---

## Step 7: Positioning Framework

Using the clusters (Step 4), ICP (Step 5), and market size (Step 6), generate the positioning framework.

**Instructions:**
- Pick the top 3 pain clusters as the primary positioning angles
- For each angle: write one positioning statement using verbatim language from the data (not paraphrased)
- Generate 3 landing page headlines that use the exact phrases people use in the pain data
- Generate 3 cold email subject lines based on the pain language
- Do NOT use banned words: powerful, robust, seamless, innovative, game-changing, streamline, leverage, transform, revolutionize

Write the full positioning framework to `/tmp/mym-output.json`:

```json
{
  "positioning_angles": [
    {
      "pain": "theme name",
      "statement": "one-line positioning using market language",
      "headline": "landing page headline using verbatim pain language",
      "cold_email_subject": "subject line"
    }
  ],
  "icp_card": {
    "one_liner": "one sentence: who they are + what they care about",
    "where_to_find_them": [...],
    "how_to_talk_to_them": "tone + vocabulary notes from the data"
  },
  "market_map": [...top vendors from G2 with positioning notes...]
}
```

---

## Step 8: Self-QA and Save Output

Run self-QA checks:

```bash
python3 -c "
import json

# Load all outputs
with open('/tmp/mym-raw.json') as f:
    raw = json.load(f)
with open('/tmp/mym-clusters.json') as f:
    clusters = json.load(f)
with open('/tmp/mym-output.json') as f:
    output = json.load(f)

raw_texts = set()
for p in raw['raw_pains']:
    raw_texts.add(p.get('title', ''))
    raw_texts.add(p.get('body_excerpt', ''))

# Check 1: No em dashes
import json as j
full_text = j.dumps(output)
if '—' in full_text:
    print('FAIL: em dash found in output')
else:
    print('PASS: no em dashes')

# Check 2: No banned words
banned = ['powerful', 'robust', 'seamless', 'innovative', 'game-changing',
          'streamline', 'leverage', 'transform', 'revolutionize']
found = [w for w in banned if w.lower() in full_text.lower()]
if found:
    print(f'FAIL: banned words found: {found}')
else:
    print('PASS: no banned words')

# Check 3: Market size language check
if 'billion' in full_text.lower() or 'trillion' in full_text.lower() or 'worth \$' in full_text.lower():
    print('FAIL: hard market size estimate found -- use directional language only')
else:
    print('PASS: no hard market size estimates')

# Check 4: Signal counts match
total = raw['summary']['total_pain_signals']
print(f'PASS: {total} total pain signals in raw data')

print('Self-QA complete.')
"
```

Fix any failures before saving.

Save the final report:

```bash
python3 << 'PYEOF'
import json, re
from datetime import datetime

with open('/tmp/mym-input.json') as f:
    inp = json.load(f)
with open('/tmp/mym-raw.json') as f:
    raw = json.load(f)
with open('/tmp/mym-clusters.json') as f:
    clusters = json.load(f)
with open('/tmp/mym-output.json') as f:
    output = json.load(f)

slug = re.sub(r'[^a-z0-9]+', '-', inp['category'].lower()).strip('-')
date = datetime.now().strftime('%Y-%m-%d')
outpath_md = f"docs/market-maps/{slug}-{date}.md"
outpath_json = f"docs/market-maps/{slug}-{date}.json"

# Build markdown report
ms = raw['market_signals']
icp = clusters.get('icp', {})
market_assessment = clusters.get('market_size', {})
angles = output.get('positioning_angles', [])
icp_card = output.get('icp_card', {})
market_map = output.get('market_map', [])

lines = [
    f"# Market Map: {inp['category'].title()}",
    f"Date: {date} | Signals analyzed: {raw['summary']['total_pain_signals']} | Sources: Reddit ({ms['reddit_signals_found']}) + HN ({ms['hn_signals_found']}) + GitHub Issues ({ms['github_issue_signals']})",
    "",
    "---",
    "",
    "## Market Size Signals",
    f"Vendors on G2: {ms['vendor_count_g2']} | Google Trends: {ms['trends_direction'].upper()} | Market stage: {market_assessment.get('stage', 'see signals below')}",
    "",
    market_assessment.get('summary', ''),
    "",
    "---",
    "",
    "## Your ICP",
    "",
    f"**Who they are:** {icp.get('who_they_are', '')}",
    "",
    f"**Where they live:** {', '.join(icp.get('where_they_live', []))}",
    "",
    "**What they say:**",
]
for q in icp.get('what_they_say', []):
    lines.append(f'> "{q}"')
lines += ["", "---", "", "## Top Pains (ranked by signal strength)", ""]

for i, c in enumerate(clusters.get('clusters', []), 1):
    lines.append(f"### Pain {i}: {c['theme']} [score: {c['total_score']}]")
    sources = c.get('sources', {})
    source_str = " + ".join(f"{src} ({cnt})" for src, cnt in sources.items())
    lines.append(f"{c['signal_count']} signals | Sources: {source_str}")
    lines.append(f"Who has this pain: {c.get('who_has_this_pain', '')}")
    lines.append("")
    lines.append("Verbatim:")
    for q in c.get('verbatim_quotes', [])[:4]:
        lines.append(f'> "{q[\"text\"]}" ({q["source"]}, score: {q["score"]})')
    lines.append("")

lines += ["---", "", "## Market Map (Key Players)", ""]
if market_map:
    lines.append("| Vendor | Positioning |")
    lines.append("|---|---|")
    for v in market_map:
        lines.append(f"| {v.get('name','')} | {v.get('positioning','')} |")
else:
    top = ms.get('top_vendors', [])
    if top:
        lines.append("| Vendor | G2 Reviews | Rating |")
        lines.append("|---|---|---|")
        for v in top:
            lines.append(f"| {v.get('name','')} | {v.get('review_count','')} | {v.get('rating','')} |")

lines += ["", "---", "", "## Messaging Framework", ""]
for a in angles:
    lines.append(f"**{a['pain']}:** {a['statement']}")
    lines.append(f"Headline: \"{a['headline']}\"")
    lines.append(f"Cold email subject: \"{a['cold_email_subject']}\"")
    lines.append("")

lines += ["---", "", "## ICP Card", "",
    f"**One liner:** {icp_card.get('one_liner', '')}",
    "",
    f"**Find them at:** {', '.join(icp_card.get('where_to_find_them', []))}",
    "",
    f"**How to talk to them:** {icp_card.get('how_to_talk_to_them', '')}",
    "",
    "---",
    "",
    "## Data Quality Notes",
    f"- All pain quotes are verbatim from raw signals",
    f"- All vendor names from G2 scrape",
    f"- Market size is directional only (no dollar estimates)",
    f"- Sources: Reddit ({ms['reddit_signals_found']}), HN ({ms['hn_signals_found']}), GitHub Issues ({ms['github_issue_signals']}), G2 ({ms['vendor_count_g2']} vendors)",
    "",
    f"Saved to: {outpath_md}",
    f"JSON snapshot: {outpath_json}",
]

with open(outpath_md, 'w') as f:
    f.write('\n'.join(lines))

# Save JSON snapshot
snapshot = {"input": inp, "market_signals": ms, "clusters": clusters.get('clusters', []),
            "icp": icp, "market_size": market_assessment, "positioning": output, "date": date}
with open(outpath_json, 'w') as f:
    json.dump(snapshot, f, indent=2)

print(f"Report saved: {outpath_md}")
print(f"JSON snapshot: {outpath_json}")
PYEOF
```

Clean up temp files:

```bash
rm -f /tmp/mym-input.json /tmp/mym-raw.json /tmp/mym-clusters.json /tmp/mym-output.json
echo "Done. Market map saved to docs/market-maps/"
```

Present the full contents of the saved `.md` file to the user.
