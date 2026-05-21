# Channel Scoring Guide

## Formula

```python
channel_score = (
    icp_signal_count * 10                          # ICP posts traced to this channel
    + min(math.log10(max(member_count, 1)) * 15, 50)  # community size (log scale, max 50)
    + min(activity_score, 30)                      # posts/week proxy (max 30)
    + competitor_mention_count * 5                 # competitor discussed here = ICP present
) - entry_difficulty_penalty                       # -20 paid, -10 invite-only, 0 open
```

## Component Breakdown

### icp_signal_count (weight: 10 per signal)

The number of Reddit/HN posts matching ICP queries that were found in this channel. This is the primary driver.

- 10 signals = +100 points (pushes a channel to top-priority on its own)
- 5 signals = +50 points
- 1 signal = +10 points
- 0 signals = 0 (channel found via DDG, not signal-trace)

**Why highest weight:** A developer clicking "post" in r/devops about the exact pain your product solves is the strongest possible channel signal. It means your ICP is not just a member -- they are actively discussing the problem there.

### member_count (log scale, max 50 points)

Log10 of member count * 15, capped at 50 to prevent massive channels from dominating.

| Members | Score contribution |
|---|---|
| 1,000 | 45 |
| 10,000 | 45 |
| 50,000 | 50 (capped) |
| 100,000 | 50 (capped) |
| 500,000 | 50 (capped) |

**Why log scale:** The difference between 1K and 10K members matters. The difference between 200K and 500K members does not -- both are "large enough." Log scale reflects this.

**Why capped:** A 5M-member general subreddit like r/programming would score 65+ on size alone even with 0 ICP signals. The cap prevents this.

### activity_score (max 30 points)

Reddit: `active_user_count / 100` (users currently online = proxy for posts/week frequency), capped at 30.

DuckDuckGo channels: defaults to 5 (DDG doesn't expose activity metrics).

HN: hardcoded to 20 (HN is always active for tech/startup ICPs).

| Active users | Activity score |
|---|---|
| 100 | 1 |
| 500 | 5 |
| 1,000 | 10 |
| 2,000 | 20 |
| 3,000+ | 30 (capped) |

### competitor_mention_count (weight: 5 per mention)

Number of ICP posts in this channel that also mention a competitor product.

**Why this matters:** A post that says "I'm trying to decide between Datadog and New Relic" in r/devops tells you three things: (1) the ICP is in this channel, (2) they are actively evaluating tools, (3) they are reachable at that exact moment of evaluation.

- 5 competitor mentions = +25 points
- 10 competitor mentions = +50 points

### entry_difficulty_penalty

| Entry type | Penalty | When to apply |
|---|---|---|
| Open | 0 | Free to join, no approval needed |
| Invite-only | -10 | Requires invite link or member approval |
| Paid | -20 | Requires paid membership or sponsorship to reach audience |

**Why penalty, not exclusion:** A paid conference with 500 exact-ICP attendees is still worth knowing about. The penalty reduces its score relative to free channels -- it doesn't hide it.

---

## Tier Thresholds

| Tier | Score range | Interpretation |
|---|---|---|
| top-priority | >= 100 | Strong ICP signal + sufficient size + accessible. Start here. |
| high | 60-99 | Good signal or good size. Second tier for outreach. |
| medium | 30-59 | Moderate signal. Worth watching but not the first channel to invest in. |
| low | < 30 | Thin signal or small community. Useful for niche products, not general GTM. |
| excluded | < 5 | Filtered out entirely. DDG noise, irrelevant results. |

---

## Worked Examples

### r/devops with 34 ICP signals

```
icp_signal_count:     34 * 10  = 340
member_count:         234,000 -> min(log10(234000) * 15, 50) = 50
activity_score:       12,000 active_users / 100 = 120 -> capped at 30
competitor_mentions:  12 * 5  = 60
entry_penalty:        0 (open)

Total: 340 + 50 + 30 + 60 - 0 = 480  -> top-priority
```

### DevOps Weekly Newsletter with 0 ICP signals

```
icp_signal_count:     0 * 10   = 0
member_count:         25,000 -> min(log10(25000) * 15, 50) = 44.7 -> ~45
activity_score:       5 (default for DDG channels)
competitor_mentions:  0 * 5    = 0
entry_penalty:        -20 (paid sponsorship)

Total: 0 + 45 + 5 + 0 - 20 = 30  -> medium
```

### r/startups with 2 ICP signals

```
icp_signal_count:     2 * 10   = 20
member_count:         800,000 -> capped at 50
activity_score:       8,000 / 100 = 80 -> capped at 30
competitor_mentions:  0 * 5    = 0
entry_penalty:        0

Total: 20 + 50 + 30 + 0 = 100  -> top-priority (barely)
```

This edge case shows why icp_signal_count is primary: r/startups hits top-priority only because it's enormous + active. In practice, its generic ICP would show in the evidence posts (founders vs. your specific ICP). The AI should note this in who_is_here.

---

## Score Interpretation for AI

When generating the playbook, use the score and tier as a prioritization signal -- not an absolute quality ranking:

- **top-priority:** Recommend the founder invest time here first. Build presence before pitching. Entry tactic should be specific and low-friction.
- **high:** Recommend as second-tier. Good for content distribution or monitoring. Entry tactic can be higher-effort (e.g., guest appearance, newsletter pitch).
- **medium:** Recommend for awareness only. Entry tactic should be lower-effort (e.g., occasional commenting, monitoring for competitor discussions).
- **low:** Report in output for completeness. No entry tactic needed unless it's a competitor forum (high intent despite low score).
