# Scoring Guide

This file defines the priority scoring model used by the agent to rank content and docs clusters.

The agent reads this file during Step 4 of analysis. All weights and formulas are documented here
so maintainers can audit the logic and users can understand why items are ranked as they are.

---

## Formula

```
priority_score = (
  (frequency_score  × 0.35) +
  (engagement_score × 0.30) +
  (recency_score    × 0.15) +
  (unanswered_bonus × 0.10) +
  (clarity_score    × 0.10)
) × 100
```

Round the final result to the nearest integer.

---

## Dimension Definitions

### 1. frequency_score (weight: 35%)

How many threads in this cluster vs. the largest cluster in the analysis.

```
frequency_score = cluster_thread_count / max_threads_in_any_cluster
```

- Range: 0.0 – 1.0
- A cluster with 6 threads where the largest cluster has 8 → 6/8 = 0.75
- Single-thread items score 1 / max_threads (low but non-zero)

**Rationale:** Frequency is the strongest signal that a topic is a real pattern rather than a one-off.

---

### 2. engagement_score (weight: 30%)

Total community engagement (reactions + comments) across all threads in the cluster.

```
engagement_score = min((total_reactions + total_comments) / 50, 1.0)
```

- Range: 0.0 – 1.0
- Cap at 1.0 to prevent a single highly-upvoted thread from dominating all others
- Denominator 50 reflects typical engagement volume on active OSS repos

**Rationale:** Engagement shows the topic resonated with the community beyond the original poster.

---

### 3. recency_score (weight: 15%)

How recently the threads in this cluster were active.

```
If any thread updated within 7 days:   recency_score = 1.0
If any thread updated within 30 days:  recency_score = 0.5
If any thread updated within 90 days:  recency_score = 0.2
Older than days_back window:           recency_score = 0.0
```

**Rationale:** A question asked last week is more pressing than one from 80 days ago.

---

### 4. unanswered_bonus (weight: 10%)

Whether the majority of threads in the cluster lack an accepted answer.

```
If majority of cluster threads have is_answered: false → unanswered_bonus = 1.0
Otherwise → unanswered_bonus = 0.0
```

- "Majority" = more than half of threads in the cluster
- Range: 0.0 or 1.0 (binary)

**Rationale:** Unanswered questions represent active documentation debt — the community asked and got no resolution.

---

### 5. clarity_score (weight: 10%)

How clearly the community articulated their confusion. This is an LLM-assigned qualitative score.

| Score | Meaning |
|---|---|
| 1.0 | The question is specific, reproducible, and clearly stated. The gap is unambiguous. |
| 0.5 | The question is partially clear but requires interpretation. The gap exists but needs inference. |
| 0.0 | The question is vague, off-topic, or the confusion is unclear. Hard to action. |

**Rationale:** A clearly-stated question produces a better docs gap or content brief. Vague complaints are harder to action.

---

## Scoring Honesty Rules

The agent must include this note in `devrel-backlog.md` beneath the run summary:

> **Note on scores:** Priority scores are relative rankings within this analysis run, not absolute quality measures. A score of 84 means this item ranked higher than a score of 71 in this dataset. Scores are not comparable across different repos or different run configurations.

---

## Example Calculation

Cluster: "Custom middleware configuration not documented"
- 6 threads in cluster; max cluster in analysis has 8 threads → frequency_score = 6/8 = 0.75
- Total engagement across cluster: 34 reactions + 41 comments = 75 → engagement_score = min(75/50, 1.0) = 1.0
- Most recent thread updated 3 days ago → recency_score = 1.0
- 5 of 6 threads have is_answered: false → unanswered_bonus = 1.0
- Question is specific and clearly reproducible → clarity_score = 1.0

```
priority_score = (0.75 × 0.35 + 1.0 × 0.30 + 1.0 × 0.15 + 1.0 × 0.10 + 1.0 × 0.10) × 100
              = (0.2625 + 0.30 + 0.15 + 0.10 + 0.10) × 100
              = 0.9125 × 100
              = 91
```
