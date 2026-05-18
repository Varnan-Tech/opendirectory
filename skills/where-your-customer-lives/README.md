# where-your-customer-lives

Give this skill a product utility and ICP. It searches Reddit, Hacker News, and DuckDuckGo to find the specific communities where your customer actually gathers -- then builds a per-channel playbook: evidence your ICP is there, one entry tactic, one content angle, and specific anti-patterns.

Stop guessing which communities to post in. Get signal-traced evidence.

## Install

```bash
npx "@opendirectory.dev/skills" install where-your-customer-lives --target claude
```

## What It Does

- Accepts: product description + ICP role + ICP pain + competitors (any combination)
- Signal-traces: searches Reddit/HN for posts matching your ICP, extracts which communities those posts came from
- Competitor layer: searches where competitors are discussed -- those communities have evaluating ICP
- Discovers 7 channel types: Reddit, Slack, Discord, Newsletter, Podcast, Conference, YouTube
- Fetches actual member counts from Reddit API and DuckDuckGo snippets -- no estimates
- Scores channels: ICP signal count (10x) + size (log scale) + activity + competitor mentions - entry penalty
- Generates per-channel playbook: who is here, entry tactic, content angle, anti-patterns
- Saves to `docs/channel-map/[slug]-[date].md` + JSON snapshot

## Requirements

| Requirement | Purpose | How to Set Up |
|---|---|---|
| GITHUB_TOKEN | Optional -- improves competitor layer rate limit | github.com/settings/tokens (no scopes needed) |

No other API keys required.

## Setup

```bash
cp .env.example .env
# Add GITHUB_TOKEN if you want higher GitHub rate limits for competitor enrichment
```

## How to Use

```
"Where does my customer live? I build observability tools for DevOps engineers."
"Find communities for my ICP: sales leaders at B2B SaaS startups dealing with low reply rates."
"Where should I post? Competitors: Clay, Apollo. ICP: growth engineers."
"What channels does my ICP use? Product: compliance automation for community banks."
"I build payment APIs for marketplaces. Who should I reach out to and where?"
```

Include competitor names for richer channel discovery. Include ICP role + pain for accurate signal-tracing.

## Why This Instead of Googling

A founder doing this manually would:
- Google "devops communities" and get listicles with outdated or generic results
- Post in r/devops without knowing if their ICP is actually there
- Spend a month in the wrong Slack before realizing it's not their market

This skill traces backwards from actual ICP pain posts to their source communities. The channels it returns are the ones where your ICP is already discussing the exact problem you solve.

## Channel Scoring

```
channel_score = (
    icp_signal_count * 10              # signals traced here -- highest weight
    + log10(members) * 15, max 50      # community size (log scale)
    + activity_score, max 30           # posts/week proxy
    + competitor_mentions * 5          # competitor discussed = ICP evaluating
) - entry_penalty                      # -20 paid, -10 invite-only, 0 open
```

Score tiers: top-priority (100+), high (60-99), medium (30-59), low (<30).

## Velocity Tracking

Run the skill every quarter. JSON snapshots in `docs/channel-map/` let you track which communities grow or shrink for your ICP over time.

## Cost Per Run

- Reddit, HN: free, no auth
- DuckDuckGo: free, no auth
- GitHub: free with optional token
- AI analysis: uses the model running the skill
- Total: free

## Standalone Script

Run channel discovery without Claude. Useful when you want raw channel data first, then bring it to any AI for analysis.

```bash
# Basic usage
python3 scripts/fetch.py "devops monitoring" --icp-role "DevOps engineers" --icp-pain "alert fatigue"

# With competitors
python3 scripts/fetch.py "B2B sales" --competitors "Clay,Apollo,HubSpot" --output results.json

# Print to stdout
python3 scripts/fetch.py "startup gtm" --icp-role "technical co-founders" --stdout | jq '.summary'

# With GitHub token
GITHUB_TOKEN=your_token python3 scripts/fetch.py "devops tools" --competitors "Datadog,Grafana"
```

The script writes a JSON file with all discovered channels. Open it with Claude and ask: "Generate a channel playbook from this data."

## Project Structure

```
where-your-customer-lives/
├── SKILL.md
├── README.md
├── .env.example
├── scripts/
│   └── fetch.py           standalone channel discovery script
├── evals/
│   └── evals.json         5 test cases
└── references/
    ├── channel-types.md   7 channel types, discovery methods, scoring notes
    ├── entry-tactics.md   entry tactic templates per channel type
    └── scoring-guide.md   channel scoring formula and tier thresholds
```

## What map-your-market Does vs. This Skill

| | map-your-market | where-your-customer-lives |
|---|---|---|
| Question answered | What does my market care about? | Where does my market gather? |
| Output | Pain clusters, ICP profile, positioning framework | Ranked channel list with per-channel playbook |
| Data sources | Reddit, HN, GitHub Issues, G2, Trends | Reddit, HN, DuckDuckGo (7 channel types) |
| Primary use | Market research, messaging | Distribution, outreach, GTM channels |

Run both for a complete picture: map-your-market tells you what to say, where-your-customer-lives tells you where to say it.

## License

MIT
