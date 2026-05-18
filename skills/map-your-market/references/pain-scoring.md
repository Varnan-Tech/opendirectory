# Pain Scoring Reference

Used by `scripts/fetch.py` to score pain signals by source, engagement, and recency.

---

## The Problem with Raw Signal Counts

Reddit returns 1,000+ posts for a popular category. Most are:
- Old posts with no engagement (1 upvote, 0 comments)
- Tangentially related discussions
- Vendor promotions disguised as questions
- Solved problems with no recurring pattern

Pain score separates high-signal complaints (hundreds of upvotes, still unresolved) from noise.

---

## Scoring Formula

```python
# Base signal -- weighted by source type
if source == "github_issue":
    base = reactions * 3      # explicit developer vote, hardest to fake
elif source == "reddit":
    base = score + (num_comments * 0.3)   # upvotes + discussion weight
elif source == "hn":
    base = points + (num_comments * 0.3)  # same structure

# Recency decay -- recent pain is more actionable
days_old = (today - created_at).days
if days_old < 30:    recency = 1.0   # full weight
elif days_old < 90:  recency = 0.85  # slight decay
elif days_old < 180: recency = 0.7   # moderate decay
else:                recency = 0.5   # older signals still count, just less

pain_score = round(base * recency, 1)
```

---

## Why GitHub Issues Score 3x Higher

A GitHub issue reaction means:
- A developer went to the effort of finding the issue
- They deliberately clicked +1 to signal "me too"
- They are an active user with a specific production problem
- The signal is public and permanent

A Reddit upvote is one click while scrolling. A GitHub +1 is intentional endorsement from a practitioner.

---

## Score Tiers

| Score | Signal Level | What it means |
|---|---|---|
| >= 200 | Critical | Widespread, high-intensity pain. Top cluster material. |
| 50-199 | High | Clear pain pattern with real engagement. Include in analysis. |
| 10-49 | Medium | Valid signal, lower confidence. Include in counts, use carefully for quotes. |
| 2-9 | Low | Noise floor. Filtered out before clustering. |
| < 2 | Noise | Excluded. |

---

## Cluster Scoring

When clustering pains into themes, the cluster's total score is the sum of all signal pain_scores in the cluster:

```python
cluster_score = sum(signal["pain_score"] for signal in cluster_signals)
```

A cluster with 5 signals of pain_score 100 each (total: 500) outranks a cluster with 30 signals of pain_score 5 each (total: 150).

---

## Source Weights Summary

| Source | What a "vote" means | Weight |
|---|---|---|
| GitHub Issue reactions | Deliberate +1 from a practitioner | 3x |
| Reddit upvotes | Passive scroll vote | 1x |
| HN points | Upvote from a technical audience | 1x |
| Comments (any source) | Discussion signal (includes off-topic) | 0.3x |
