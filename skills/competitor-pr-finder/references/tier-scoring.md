# Channel Tier Scoring

## Core Tiering Rule

Channels are tiered by how many of the 5 researched competitors appeared in that channel's coverage.

| Tier | Threshold | What it means |
|---|---|---|
| Tier 1 | 3 or more competitors | Proven beat for this space. The journalist/host actively covers this category. Highest-value targets. |
| Tier 2 | Exactly 2 competitors | Warm lead. Some demonstrated interest in the category. Worth pursuing after Tier 1. |
| Tier 3 | Exactly 1 competitor | Discovery list only. May be a one-off or a niche fit. No deep dive or pitch draft required. |

## Counting Rules

- Count each **root domain** once per competitor, regardless of how many articles appeared from that domain.
  - Example: 3 TechCrunch articles about the same competitor = TechCrunch counts as 1 for that competitor.
- Count across all three tracks (editorial, podcast, community).
  - A channel can be Tier 1 through a mix of tracks -- e.g., TechCrunch appears in Track A for 3 different competitors.
- If the same channel appears across multiple tracks for the same competitor, it still counts as 1 for that competitor.

## Override Rules

**Tier 2 -> Tier 1 override:**
If a Tier 2 channel is the dominant podcast for the space (estimated >100k listeners, or the most prominent show in the category), elevate it to Tier 1. This override exists because audience quality matters more than raw frequency for podcasts.

Signals for override eligibility:
- The podcast name is well-known in the category (e.g., "Acquired", "My First Million", "Lenny's Podcast" for B2B SaaS)
- The episode title implies a deep-dive format (1+ hour, not a news brief)
- Search results show a consistent pattern of category founders as guests

**Geography filter:**
- If the product's geography is US: deprioritize EU-only publications (Financial Times, TechCrunch EU section, Sifted). They can appear in Tier 3 but should not be elevated to Tier 1 or 2.
- If the product's geography is Europe: deprioritize US-only niche press. Major US outlets (TechCrunch, Forbes) are still relevant as they cover global companies.
- If geography is Global: no filter applied.

**Community deduplication:**
Reddit and Hacker News count as separate channels. `reddit.com/r/devops` and `reddit.com/r/programming` count as separate channels (different audiences). ProductHunt is its own channel.

## What Goes in Each Tier's Output Section

**Tier 1 -- Deep dives:**
Each Tier 1 channel gets a full section in the output:
- Channel name, type, frequency count, which competitors appeared
- Evidence URLs from search results
- Story angle type extracted from titles
- Journalist/host name + beat (from Step 8 lookup, or "not found in search data")
- Approach method
- Cold pitch draft: subject line + 3-4 sentence body

**Tier 2 -- Quick hits table:**
A summary table: channel name, which competitors appeared, URL.
No journalist lookup. No pitch draft. User can follow up manually.

**Tier 3 -- Discovery list:**
A bullet list: channel name + URL only.
No analysis. Just awareness that coverage exists.

## Channel Frequency Map Construction (Step 7)

To build the frequency map:

1. Collect all result URLs from `/tmp/cprf-pr-raw.json` for all competitors.
2. For each result URL, extract the root domain (normalize per `pr-channel-types.md`).
3. Build a set per competitor: which root domains appeared in their results?
4. Count how many competitors each domain appears in.
5. Sort by count descending. Domains with count >= 3 are Tier 1. Count == 2 are Tier 2. Count == 1 are Tier 3.

**Example frequency map:**
```
techcrunch.com:       4 competitors (Tier 1)
news.ycombinator.com: 4 competitors (Tier 1)
producthunt.com:      3 competitors (Tier 1)
infoq.com:            2 competitors (Tier 2)
thenewstack.io:       2 competitors (Tier 2)
devops.com:           1 competitor  (Tier 3)
reddit.com/r/devops:  1 competitor  (Tier 3)
```

## Maximum Output Limits

To keep the output actionable (not overwhelming):

- Tier 1 deep dives: maximum 7 channels
- Tier 2 quick hits: maximum 10 channels
- Tier 3 discovery: maximum 15 channels (list only)
- Bonus hooks: exactly 3

If more channels qualify for a tier than the limit, prioritize by:
1. Highest frequency count
2. For equal counts: editorial > podcast > community
3. For still-equal: alphabetical by domain name (deterministic)
