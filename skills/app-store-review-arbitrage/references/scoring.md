# Scoring Reference
## `app-store-review-arbitrage`

This file documents the complaint scoring formula used in Step 4 of SKILL.md. The formula is applied by the LLM during clustering — **not** by the fetch script. The script provides raw normalized reviews; the LLM applies this formula to score and rank them.

---

## Complaint Weight Formula (v1 — 2-axis)

```
complaint_weight(review) = (4 - rating) × recency_factor
```

### Severity axis: `(4 - rating)`

| Star rating | Weight |
|---|---|
| 1★ | 3 |
| 2★ | 2 |
| 3★ | 1 |

A 1-star review is 3× more signal than a 3-star review. This reflects the real-world distribution: 1-star reviews describe acute failures, 3-star reviews describe friction or missing features.

### Recency axis: `recency_factor`

| Review age | Factor | Rationale |
|---|---|---|
| ≤ 90 days | 1.0 | Active, current complaint — highest copy relevance |
| 91–365 days | 0.7 | Recent but potentially addressed by a recent update |
| > 365 days | 0.4 | Historical — still signal, but lower weight for ad copy decisions |

**How to compute `days_old`:** `(today's date) − (review date)` in days. Use the `date` field from the normalized schema (YYYY-MM-DD).

### Maximum per-review weight

`3 × 1.0 = 3.0` — a 1-star review posted within the last 90 days.

---

## Cluster Score

```
cluster_score = sum(complaint_weight(r) for r in cluster_reviews)
```

Clusters are ranked by `cluster_score` descending. The top cluster is the strongest ad copy opportunity.

---

## Score Tiers

| Tier | Cluster Score | Approx. min recent 1★ reviews | Output action |
|---|---|---|---|
| Critical | ≥ 60 | ~20 | Include — primary ad copy angle |
| High | 15–59 | ~5 | Include — strong secondary angle |
| Medium | 5–14 | ~2 | Include only if fewer than 3 High/Critical clusters exist; add Gate 3 low-confidence flag |
| Noise | < 5 | — | Discard — insufficient evidence; do not include in output |

**Gate 3 rule:** If Gate 2 (minimum 3 reviews per cluster) leaves fewer than 3 clusters at High tier or above, include Medium-tier clusters and prepend the low-confidence flag to the brief header.

---

## Worked Example

**Setup:** A productivity app with 40 low-star reviews split into three complaint themes.

**Cluster A — "Crashes when exporting to PDF"**
- 18 reviews: 12 at 1★ (< 90 days), 6 at 2★ (< 90 days)
- Weight: (12 × 3×1.0) + (6 × 2×1.0) = 36 + 12 = **48** → High tier

**Cluster B — "Sync stops working after update"**
- 14 reviews: 8 at 1★ (< 90 days), 4 at 1★ (91–365 days), 2 at 2★ (> 365 days)
- Weight: (8×3×1.0) + (4×3×0.7) + (2×2×0.4) = 24 + 8.4 + 1.6 = **34** → High tier

**Cluster C — "Paywall appears after 3 days, not 14 as advertised"**
- 6 reviews: 5 at 1★ (< 90 days), 1 at 2★ (< 90 days)
- Weight: (5×3×1.0) + (1×2×1.0) = 15 + 2 = **17** → High tier

**Cluster D — "Dark mode not available"**
- 2 reviews: 2 at 3★ (< 90 days)
- Weight: (2×1×1.0) = **2** → Noise (discard)

**Output:** Clusters A, B, C in brief. Cluster D discarded. No Gate 3 flag (3 High clusters).

---

## v2 Upgrade Path (3-axis formula)

When `thumbsUpCount` data becomes available from App Store sources, upgrade to:

```
complaint_weight(review) = (4 - rating) × recency_factor × (1 + ln(1 + helpful_votes))
```

Where:
- `ln` = natural logarithm (Python: `math.log`)
- `helpful_votes` = `thumbsUpCount` (Google Play) or equivalent when available
- A review with 0 helpful votes: vote factor = 1.0 (no change)
- A review with 9 helpful votes: vote factor = 1 + ln(10) ≈ 3.30

**Tier thresholds must be recalibrated** when upgrading to 3-axis — they were set for 2-axis weights.

---

## Implementation Note

The LLM must:
1. Compute `complaint_weight` for each low-star review individually
2. Assign each review to exactly one cluster
3. Sum weights within each cluster to get `cluster_score`
4. Rank clusters by `cluster_score` descending
5. Apply tier classification per the table above
6. Write cluster scores into `/tmp/asr-clusters.json`

The fetch script does **not** compute scores. It provides `rating` and `date` fields in the normalized schema, which are the only inputs to this formula.
