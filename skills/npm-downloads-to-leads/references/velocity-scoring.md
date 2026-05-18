# Velocity Scoring Reference

Used by SKILL.md Step 4 to classify npm packages by growth trajectory. The velocity score identifies packages in the hockey-stick growth phase, not just packages with high download volumes.

---

## The Problem with Raw Downloads

If you rank npm packages by raw weekly downloads, the top results are always React, lodash, TypeScript, and axios. These packages are not leads. Their maintainers are already famous, already overwhelmed with outreach, and already well beyond the "catch them early" window.

The signal is relative growth -- a package going from 1,000 to 8,000 weekly downloads over 8 weeks is more interesting than React at 50 million, because:
1. The maintainer just crossed an inflection point -- they are building an audience now
2. They are not yet famous -- your outreach lands in a less-crowded inbox
3. Their growth signals that developers are finding value in what they built -- that is the same developer segment you are trying to reach

---

## The Velocity Score Formula

```python
recent_4 = sum(weeks[-4:]) / 4    # average of last 4 weeks
prior_4 = sum(weeks[-8:-4]) / 4   # average of prior 4 weeks
recent_2 = sum(weeks[-2:]) / 2    # last 2 weeks (acceleration check)
mid_2 = sum(weeks[-4:-2]) / 2     # previous 2 weeks (acceleration baseline)

growth_ratio = recent_4 / max(prior_4, 1)
acceleration = recent_2 / max(mid_2, 1)

# Sweet spot multiplier
if recent_4 < 500:
    noise_factor = max(recent_4 / 500, 0.1)   # penalize noise floor
elif recent_4 > 500_000:
    noise_factor = max(500_000 / recent_4, 0.1)  # penalize established giants
else:
    noise_factor = 1.0

velocity_score = growth_ratio * acceleration * noise_factor * 100
```

**Why three components:**

- `growth_ratio`: Is the package getting more downloads recently than before? A ratio of 2.0 means double the average downloads in the recent 4 weeks vs the prior 4.
- `acceleration`: Is growth speeding up? A ratio of 1.2 means the last 2 weeks were 20% higher than the 2 weeks before that. This distinguishes a sustained breakout from a one-week spike.
- `noise_factor`: The sweet spot correction. Packages under 500/week are statistically unreliable (one viral tweet can quadruple downloads). Packages over 500K/week grow slowly by necessity -- a 10% growth at that scale represents millions of new downloads but looks small as a ratio.

---

## Score Interpretation

| Velocity Score | What it means |
|---|---|
| > 150 | Exceptional breakout. Growth is fast and accelerating. The maintainer is in a phase they probably have not experienced before. |
| 80-150 | Clear breakout. Consistent multi-week growth with acceleration. Strong lead candidate. |
| 40-80 | Watching. Growing but not at breakout pace. Worth monitoring -- may cross into breakout in 4-8 weeks. |
| 10-40 | Steady. Growing slowly or holding volume. Not a near-term lead from growth signals alone. |
| < 10 | Declining or flat. May have had growth earlier, but current trend is neutral or down. |

---

## Tier Definitions

| Tier | Criteria | Action |
|---|---|---|
| `breakout` | velocity_score > 80 AND 500 < recent_4 < 500,000 | Generate full lead brief + outreach message |
| `watching` | velocity_score > 40 | Generate lead brief, flag as "not yet breakout" |
| `steady` | velocity_score 10-40 | Show in leaderboard, no lead brief |
| `established` | recent_4 >= 500,000 | Show in leaderboard, note scale ceiling on velocity |
| `too_early` | recent_4 < 500 | Note download count, suggest revisiting when above 500/week |
| `insufficient_data` | fewer than 4 weeks of data | Skip velocity calculation entirely |

---

## The Sweet Spot: 500 to 500,000 Weekly Downloads

**Below 500/week:** A single blog post, a tweet from a developer with 10K followers, or a single CI pipeline at a large company can temporarily push a package from 50 to 300 downloads. This is not a trend -- it is a random event. The velocity score for these packages is unreliable and should not drive outreach decisions.

**500 to 10,000/week:** This is where breakout discovery is most valuable. The package has real organic adoption, the maintainer is seeing real growth for possibly the first time, and the audience is still small enough that outreach from a relevant company feels meaningful rather than corporate.

**10,000 to 100,000/week:** Still strong territory. The maintainer is probably getting some attention now but is not yet the subject of conference talks and podcast interviews. Still a good window.

**100,000 to 500,000/week:** The package is well-established. The maintainer likely has some reputation in the ecosystem. Outreach still works but requires a stronger angle -- you are not the first person to notice them.

**Above 500,000/week:** These are the top 0.1% of npm packages. Their maintainers are public figures in the developer ecosystem. The "before they are famous" window has closed.

---

## Acceleration Matters More Than You Expect

A package with `growth_ratio = 2.0` but `acceleration = 0.7` means: it doubled over 8 weeks, but the growth is actually slowing down. The last 2 weeks were slower than the 2 weeks before. This could be:
- A spike fading (viral moment passing)
- Growth plateauing after an initial launch burst
- A product that got attention but is not retaining users who try it

A package with `growth_ratio = 1.5` and `acceleration = 1.4` means: 50% growth over 8 weeks and the last 2 weeks were 40% higher than the prior 2. This is a package that is still accelerating. The inflection may not have happened yet.

The velocity formula weights both. A package that is growing AND accelerating gets a higher score than one that grew quickly but is now decelerating.

---

## Common Misclassifications

**Spike then flat:** A package gets 5,000 downloads in one week (from a tweet or Product Hunt feature) and then returns to 200/week. If the spike is in the recent_4 window, it will inflate the velocity score. Check the weekly trend array -- if it shows a single high spike rather than a steady incline, the breakout classification is unreliable.

**New package (fewer than 8 weeks old):** A new package going from 0 to 800 in its first 4 weeks will have a high growth_ratio (prior_4 is near 0). The formula guards against this with `max(prior_4, 1)`, which keeps the ratio from being infinity but can still produce inflated scores. The insufficient_data tier handles packages with fewer than 4 full weeks.

**Seasonal packages:** Some packages (tax filing tools, holiday card generators) have predictable annual spikes. If the analysis runs during the spike season, the velocity score will be high. The 12-week window partially mitigates this but does not eliminate it.

---

## What a Real Breakout Looks Like (Weekly Trend)

Genuine sustained breakout:
```
Week 1:  1,200
Week 2:  1,400
Week 3:  1,900
Week 4:  2,800
Week 5:  3,900
Week 6:  5,200
Week 7:  6,800
Week 8:  8,900
```

Spike-and-flat (not a breakout):
```
Week 1:    800
Week 2:    850
Week 3: 12,400  <-- viral tweet or HN post
Week 4:    900
Week 5:    950
Week 6:  1,000
Week 7:    980
Week 8:  1,050
```

The trend array in the output lets you visually distinguish these patterns. A good velocity score combined with a consistent upward trend array is the strongest signal.
