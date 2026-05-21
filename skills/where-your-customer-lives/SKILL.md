---
name: where-your-customer-lives
description: Given a product utility and ICP, researches the internet to find the specific channels. Where your customer actually lives, ranked by reachability with a full per-channel playbook. Returns evidence that your ICP is there, one entry tactic, one content angle, and specific anti-patterns per channel. Use when asked where my customer hangs out, what communities should I post in, where is my ICP, find channels for outreach, what forums does my ICP use, where should I spend time for distribution, or which communities are right for my product.
compatibility: [claude-code, gemini-cli, github-copilot]
---

# Where Your Customer Lives

Given a product utility and ICP, trace real ICP pain posts back to their source communities. Layer in competitor discussion signals. Discover Slack/Discord/newsletter/podcast/conference channels via DuckDuckGo. Score every channel by ICP signal count, size, activity, and competitor presence. Output a ranked playbook: evidence, entry tactic, content angle, anti-patterns -- one per channel. No guessing. Signal-traced channels only.

---

**Critical rule:** Every channel name in the output must exist in either the Reddit API response or DuckDuckGo search results from this run. Every member count must come from the `about.json` API or a search snippet -- never estimated. Every ICP signal count must match the raw data. If a channel type returns 0 results, report 0 -- do not fabricate channels.

---

## Common Mistakes

| The agent will want to... | Why that's wrong |
|---|---|
| Recommend generic channels ("LinkedIn", "Twitter") | Every channel must be specific with a name, member count, and URL. "LinkedIn Group: DevOps for Enterprise Teams (45K members)" -- not just "LinkedIn". |
| Use the same channels for every ICP | Signal-trace is ICP-specific. A DevOps ICP and a Finance ICP produce entirely different channel lists. Run the script fresh per ICP. |
| Invent member counts or community names | Every channel name must come from DuckDuckGo results or Reddit API. Every member count must come from the API or a search snippet. If unavailable, write "member count not found". |
| Skip the competitor layer | Where competitors are discussed = your ICP is evaluating alternatives = hottest outreach context. Always run competitor search even if the user did not ask. |
| Write entry tactics that are product pitches | "Post about your product in r/devops" is not an entry tactic. Entry tactics name the specific thread type, content format, and community norm. |
| Treat Reddit as the only channel type | The output must include at least 3 channel types. If only Reddit is found, explicitly search DuckDuckGo for Slack/Discord/newsletter/conference before stopping. |

---

## Step 1: Setup Check

```bash
echo "GITHUB_TOKEN: ${GITHUB_TOKEN:-not set -- competitor layer runs at 60 req/hr unauthenticated}"
echo ""
echo "Data sources this run will use:"
echo "  Reddit public JSON   (no auth, signal-trace)"
echo "  Reddit about.json    (no auth, subreddit metadata)"
echo "  HN Algolia API       (no auth, signal-trace)"
echo "  DuckDuckGo HTML      (no auth, channel discovery)"
echo "  GitHub API           (${GITHUB_TOKEN:+authenticated, }optional for competitor enrichment)"
```

If `GITHUB_TOKEN` is not set: continue. All core channel discovery works without it.

---

## Step 2: Parse ICP

Collect from the conversation:
- `product` -- what the product does (one sentence)
- `icp_role` -- who the ICP is (e.g. "technical co-founders", "DevOps engineers at Series A")
- `icp_pain` -- their primary problem (e.g. "customer acquisition", "alert fatigue")
- `category` -- market category keywords (e.g. "startup gtm sales", "devops monitoring")
- `competitors` -- optional competitor names (e.g. "Clay, Apollo, HubSpot")

**ICP cascade:**
1. If the user's prompt contains product + icp_role + icp_pain: extract them directly and proceed.
2. If the prompt is thin (only category or only product name): check `docs/icp.md` for a saved ICP profile. Merge with prompt details.
3. If still insufficient (missing icp_role or icp_pain): ask these 3 questions, one at a time:
   - "What does your product do in one sentence?"
   - "Who is your ideal customer? (role, company type, team size)"
   - "What is their primary problem before they find your product?"
4. Save the final ICP to `docs/icp.md` so other skills can reuse it.

Save ICP file if docs/icp.md does not already contain this product:

```bash
python3 << 'PYEOF'
import json, os

icp = {
    "product": "PRODUCT_HERE",
    "icp_role": "ICP_ROLE_HERE",
    "icp_pain": "ICP_PAIN_HERE",
    "competitors": ["COMP_1", "COMP_2"],
    "category": "CATEGORY_HERE"
}

os.makedirs("docs", exist_ok=True)
with open("/tmp/wcl-input.json", "w") as f:
    json.dump(icp, f, indent=2)

# Update docs/icp.md
icp_md_path = "docs/icp.md"
new_block = f"""## {icp['product']}
- **ICP role:** {icp['icp_role']}
- **ICP pain:** {icp['icp_pain']}
- **Competitors:** {', '.join(icp['competitors']) if icp['competitors'] else 'none'}
- **Category:** {icp['category']}
"""
existing = open(icp_md_path).read() if os.path.exists(icp_md_path) else ""
if icp['product'] not in existing:
    with open(icp_md_path, "a") as f:
        f.write(new_block)
    print(f"ICP saved to {icp_md_path}")
else:
    print(f"ICP already in {icp_md_path}")

print(f"Product: {icp['product']}")
print(f"ICP role: {icp['icp_role']}")
print(f"ICP pain: {icp['icp_pain']}")
print(f"Competitors: {', '.join(icp['competitors']) if icp['competitors'] else 'none'}")
PYEOF
```

---

## Step 3: Run the Standalone Data Collection Script

Check if the script exists:

```bash
ls scripts/fetch.py 2>/dev/null && echo "script available" || echo "not found"
```

Run channel discovery:

```bash
GITHUB_TOKEN="${GITHUB_TOKEN:-}" python3 scripts/fetch.py \
    "$(python3 -c "import json; d=json.load(open('/tmp/wcl-input.json')); print(d['category'])")" \
    --icp-role "$(python3 -c "import json; d=json.load(open('/tmp/wcl-input.json')); print(d['icp_role'])")" \
    --icp-pain "$(python3 -c "import json; d=json.load(open('/tmp/wcl-input.json')); print(d['icp_pain'])")" \
    --product "$(python3 -c "import json; d=json.load(open('/tmp/wcl-input.json')); print(d['product'])")" \
    --competitors "$(python3 -c "import json; d=json.load(open('/tmp/wcl-input.json')); print(','.join(d['competitors']))")" \
    --output /tmp/wcl-raw.json
```

Wait for completion (allow up to 5 minutes -- Reddit + DuckDuckGo searches take ~120 seconds total).

Verify output:

```bash
python3 -c "
import json
with open('/tmp/wcl-raw.json') as f:
    d = json.load(f)
print(f'Reddit posts found: {d[\"reddit_posts_found\"]}')
print(f'HN signals found:   {d[\"hn_signals_found\"]}')
print(f'Channels discovered: {d[\"summary\"][\"total_channels\"]}')
print(f'Top priority:        {len(d[\"summary\"][\"top_priority\"])}')
print(f'By type:             {d[\"summary\"][\"by_type\"]}')
print(f'Competitor layer ran: {d[\"summary\"][\"competitor_layer_ran\"]}')
"
```

If total_channels < 3: tell the user: "Fewer than 3 channels found. The ICP description may be too narrow for Reddit/DDG coverage. Try broader category keywords, or add competitor names to activate the competitor layer." Then attempt one retry with broader category keywords before stopping.

---

## Step 4: Print Channel Summary

Load the raw data and print a ranked summary table:

```bash
python3 -c "
import json
with open('/tmp/wcl-raw.json') as f:
    d = json.load(f)
channels = d['channels_discovered']
print(f'Channels found: {len(channels)}')
print()
print(f'{'#':<4} {'Channel':<35} {'Type':<14} {'Members':<12} {'ICP signals':<13} {'Score':<8} Tier')
print('-' * 100)
for i, ch in enumerate(channels[:15], 1):
    members = ch.get('members', 0)
    m_str = f'{members//1000}K' if members >= 1000 else str(members) if members else '?'
    print(f'{i:<4} {ch[\"name\"]:<35} {ch[\"type\"]:<14} {m_str:<12} {ch.get(\"icp_signal_count\",0):<13} {ch.get(\"channel_score\",0):<8} {ch.get(\"tier\",\"\")}')
"
```

Print the top 3 evidence posts from the highest-scoring channel:

```bash
python3 -c "
import json
with open('/tmp/wcl-raw.json') as f:
    d = json.load(f)
channels = d['channels_discovered']
if channels:
    top = channels[0]
    print(f'Top channel: {top[\"name\"]}')
    print(f'Evidence posts:')
    for ep in top.get('evidence_posts', [])[:3]:
        print(f'  [{ep.get(\"score\",0):.0f}] {ep.get(\"title\",\"\")}')
        print(f'       {ep.get(\"url\",\"\")}')
"
```

---

## Step 5: AI Channel Enrichment

You now have the raw channel data. For each channel in the top-priority and high tiers, generate a playbook entry.

Load all channels:

```bash
python3 -c "
import json
with open('/tmp/wcl-raw.json') as f:
    d = json.load(f)
top_channels = [ch for ch in d['channels_discovered'] if ch.get('tier') in ('top-priority', 'high')]
print(json.dumps(top_channels, indent=2))
"
```

For each channel above, generate:

**who_is_here:** 2 sentences describing the specific type of ICP present in this channel. Derive from the evidence posts, subreddit description, and ICP profile. Do NOT write "your target audience" -- be specific. Example: "DevOps engineers at companies of 50-500 who own the infra stack without a dedicated SRE team. They post about on-call burnout, Kubernetes sprawl, and choosing between cloud-native and self-hosted observability."

**entry_tactic:** One specific, actionable entry move. Name the thread type, posting format, and community norm. NOT "engage with the community." Example: "Find the weekly 'What are you working on?' thread (posted every Monday by automoderator). Reply with a 3-sentence technical challenge you solved -- what broke, what you tried, what worked. No product mention. Build karma before posting standalone content."

**content_angle:** The content format that gets highest engagement in this specific channel, derived from evidence post titles and scores. Example: "Technical post-mortems outperform product announcements 5:1 here. Format: 'We migrated 200K users from X to Y -- here is what broke and why.' Concrete numbers + what failed = most upvotes."

**anti_patterns:** 2-3 specific behaviors that get posts removed or reputation destroyed in this community. Derive from subreddit rules (if available in description) and evidence post patterns. Example: ["Posting product links in non-promotional threads -- moderators remove within hours", "Asking 'what tools do you use?' without specific context -- flagged as market research farming"]

Write the enriched playbook to `/tmp/wcl-channels.json`:

```json
{
  "playbook": [
    {
      "channel": "r/devops",
      "evidence": "34 ICP signals traced here, avg pain score 180",
      "who_is_here": "...",
      "entry_tactic": "...",
      "content_angle": "...",
      "anti_patterns": ["...", "..."]
    }
  ]
}
```

```bash
python3 -c "
import json
with open('/tmp/wcl-channels.json') as f:
    d = json.load(f)
print(f'Playbook entries: {len(d[\"playbook\"])}')
for p in d['playbook']:
    print(f'  {p[\"channel\"]}')
"
```

---

## Step 6: Generate Full Ranked Output

Write the complete ranked playbook to `/tmp/wcl-output.json`:

```bash
python3 << 'PYEOF'
import json
from datetime import datetime

with open('/tmp/wcl-input.json') as f:
    inp = json.load(f)
with open('/tmp/wcl-raw.json') as f:
    raw = json.load(f)
with open('/tmp/wcl-channels.json') as f:
    enriched = json.load(f)

playbook_by_channel = {p['channel']: p for p in enriched['playbook']}
channels = raw['channels_discovered']

output = {
    "date": raw['date'],
    "product": inp['product'],
    "icp_role": inp['icp_role'],
    "icp_pain": inp['icp_pain'],
    "competitors": inp.get('competitors', []),
    "total_channels": raw['summary']['total_channels'],
    "channels": []
}

for ch in channels:
    name = ch['name']
    playbook = playbook_by_channel.get(name, {})
    output['channels'].append({
        "rank": channels.index(ch) + 1,
        "name": name,
        "type": ch['type'],
        "url": ch['url'],
        "members": ch.get('members', 0),
        "active_users": ch.get('active_users', 0),
        "icp_signal_count": ch.get('icp_signal_count', 0),
        "competitor_mentions": ch.get('competitor_mentions', 0),
        "channel_score": ch.get('channel_score', 0),
        "tier": ch.get('tier', ''),
        "entry_type": ch.get('entry_type', 'open'),
        "evidence_posts": ch.get('evidence_posts', []),
        "who_is_here": playbook.get('who_is_here', ''),
        "entry_tactic": playbook.get('entry_tactic', ''),
        "content_angle": playbook.get('content_angle', ''),
        "anti_patterns": playbook.get('anti_patterns', []),
    })

with open('/tmp/wcl-output.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"Output written: /tmp/wcl-output.json")
print(f"Total channels: {len(output['channels'])}")
PYEOF
```

---

## Step 7: Self-QA

```bash
python3 -c "
import json

with open('/tmp/wcl-raw.json') as f:
    raw = json.load(f)
with open('/tmp/wcl-output.json') as f:
    output = json.load(f)

full_text = json.dumps(output)
raw_channel_names = {ch['name'].lower() for ch in raw['channels_discovered']}
passes = 0
fails = 0

# Check 1: No em dashes
if chr(8212) in full_text:
    print('FAIL: em dash found in output -- replace with hyphen')
    fails += 1
else:
    print('PASS: no em dashes')
    passes += 1

# Check 2: No banned words
banned = ['powerful', 'robust', 'seamless', 'innovative', 'game-changing',
          'streamline', 'leverage', 'transform', 'revolutionize']
found = [w for w in banned if w.lower() in full_text.lower()]
if found:
    print(f'FAIL: banned words: {found}')
    fails += 1
else:
    print('PASS: no banned words')
    passes += 1

# Check 3: At least 3 channel types
types = {ch['type'] for ch in output['channels']}
if len(types) < 3:
    print(f'FAIL: only {len(types)} channel type(s) in output: {types}')
    fails += 1
else:
    print(f'PASS: {len(types)} channel types: {types}')
    passes += 1

# Check 4: All channel names exist in raw data
for ch in output['channels']:
    if ch['name'].lower() not in raw_channel_names:
        print(f'FAIL: channel not in raw data: {ch[\"name\"]}')
        fails += 1

if fails == 0:
    print('PASS: all channel names verified in raw data')
    passes += 1

# Check 5: No generic entry tactics
generic_phrases = ['engage with the community', 'post about your product', 'share your content']
for ch in output['channels']:
    tactic = ch.get('entry_tactic', '').lower()
    for phrase in generic_phrases:
        if phrase in tactic:
            print(f'FAIL: generic entry tactic in {ch[\"name\"]}: contains \"{phrase}\"')
            fails += 1

if fails == 0:
    print('PASS: entry tactics are channel-specific')

print()
print(f'Result: {passes} passed, {fails} failed')
if fails > 0:
    print('Fix failures before saving.')
else:
    print('All checks passed. Ready to save.')
"
```

Fix any failures before proceeding to Step 8.

---

## Step 8: Save Output and Clean Up

```bash
python3 << 'PYEOF'
import json, os, re
from datetime import datetime

with open('/tmp/wcl-input.json') as f:
    inp = json.load(f)
with open('/tmp/wcl-raw.json') as f:
    raw = json.load(f)
with open('/tmp/wcl-output.json') as f:
    output = json.load(f)

slug = re.sub(r'[^a-z0-9]+', '-', (inp.get('icp_role') or inp['category']).lower()).strip('-')[:40]
date = datetime.now().strftime('%Y-%m-%d')
os.makedirs('docs/channel-map', exist_ok=True)

outpath_md = f"docs/channel-map/{slug}-{date}.md"
outpath_json = f"docs/channel-map/{slug}-{date}.json"

channels = output['channels']
by_type = {}
for ch in channels:
    by_type.setdefault(ch['type'], []).append(ch)

lines = [
    f"# Where Your Customer Lives: {inp['product'] or inp['category'].title()}",
    f"ICP: {inp['icp_role']} | Date: {date} | Channels found: {len(channels)}",
    "",
    "---",
    "",
    "## Channel Ranking",
    "",
]

tier_labels = {"top-priority": "TOP PRIORITY", "high": "HIGH", "medium": "MEDIUM", "low": "LOW"}

for ch in channels:
    members = ch.get('members', 0)
    m_str = f"{members//1000}K" if members >= 1000 else str(members) if members else "member count not found"
    tier_label = tier_labels.get(ch.get('tier', ''), ch.get('tier', '').upper())
    
    lines.append(f"### #{ch['rank']}: {ch['name']} [score: {ch['channel_score']}] -- {tier_label}")
    
    active = ch.get('active_users', 0)
    active_str = f" | Active: {active//1000}K/day" if active >= 1000 else f" | Active: {active}/day" if active else ""
    lines.append(f"Type: {ch['type'].title()} | Members: {m_str}{active_str} | {ch.get('entry_type', 'open').title()} to join")
    
    evidence_str = f"{ch['icp_signal_count']} ICP signals traced here" if ch['icp_signal_count'] > 0 else "Discovered via DuckDuckGo search"
    lines.append(f"Evidence: {evidence_str}")
    
    if ch.get('competitor_mentions', 0) > 0 and inp.get('competitors'):
        lines.append(f"Competitor mentions: {ch['competitor_mentions']} across {', '.join(inp['competitors'][:3])}")
    
    lines.append("")
    
    if ch.get('who_is_here'):
        lines.append(f"**Who is here:** {ch['who_is_here']}")
        lines.append("")
    
    if ch.get('entry_tactic'):
        lines.append(f"**Entry tactic:** {ch['entry_tactic']}")
        lines.append("")
    
    if ch.get('content_angle'):
        lines.append(f"**Content angle:** {ch['content_angle']}")
        lines.append("")
    
    if ch.get('anti_patterns'):
        lines.append("**Anti-patterns:**")
        for ap in ch['anti_patterns']:
            lines.append(f"- {ap}")
        lines.append("")
    
    lines.append("---")
    lines.append("")

lines += [
    "## Channel Summary by Type",
    "",
    "| Type | Count | Best channel | Score |",
    "|---|---|---|---|",
]
for ch_type, chs in sorted(by_type.items(), key=lambda x: -max(c['channel_score'] for c in x[1])):
    best = max(chs, key=lambda x: x['channel_score'])
    lines.append(f"| {ch_type.title()} | {len(chs)} | {best['name']} | {best['channel_score']} |")

lines += [
    "",
    "---",
    "",
    "## Data Quality Notes",
    f"- All channel names exist in Reddit API response or DuckDuckGo search results",
    f"- Member counts from Reddit about.json API or search snippets",
    f"- ICP signal counts match raw data ({raw['reddit_posts_found']} Reddit posts, {raw['hn_signals_found']} HN signals)",
    f"- Competitor layer ran: {raw['summary']['competitor_layer_ran']}",
    f"- Sources: Reddit signal-trace, HN signal-trace, DuckDuckGo channel discovery",
    "",
    f"Saved to: {outpath_md}",
    f"JSON snapshot: {outpath_json}",
]

with open(outpath_md, 'w') as f:
    f.write('\n'.join(lines))

# JSON snapshot
snapshot = {
    "input": inp,
    "channels": channels,
    "summary": raw['summary'],
    "date": date,
}
with open(outpath_json, 'w') as f:
    json.dump(snapshot, f, indent=2)

print(f"Report saved: {outpath_md}")
print(f"JSON snapshot: {outpath_json}")
PYEOF
```

Clean up temp files:

```bash
rm -f /tmp/wcl-input.json /tmp/wcl-raw.json /tmp/wcl-channels.json /tmp/wcl-output.json
echo "Done. Channel map saved to docs/channel-map/"
```

Present the full contents of the saved `.md` file to the user.
