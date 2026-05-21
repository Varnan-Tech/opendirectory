# Output Brief Format Reference
## `app-store-review-arbitrage`

This file is the authoritative specification for the output brief produced in Steps 6–8 of SKILL.md. The LLM must follow this format exactly. Five sections, always present. No additions, no optional sections.

---

## File naming

```
docs/review-briefs/[app-slug]-[YYYY-MM-DD].md
```

- App Store: `app-slug` = the slug segment extracted from the URL (e.g., `notion-notes-tasks-ai`)
- Google Play: `app-slug` = last segment of the package name (e.g., `com.robinhood.android` → `robinhood`)
- Date = the date the skill was run

---

## Brief Header

```markdown
# App Store Review Brief: [App Name]

**Platform:** [App Store | Google Play]
**URL:** [original app URL]
**Reviews collected:** [N] total | [N] low-star (1–3★)
**Date range:** [oldest review date] to [newest review date]
**Generated:** [YYYY-MM-DD]
```

If Gate 3 (low-confidence) was triggered, prepend this block immediately after the header:

```markdown
> ⚠ **LOW CONFIDENCE:** Only [N] complaint cluster(s) met the minimum evidence threshold (≥ 3 supporting reviews). Output reflects limited data. Consider analyzing a competitor with more reviews, or broaden the rating filter to include 4-star reviews.
```

---

## Section 1: Complaint Cluster Leaderboard

Always present. Always first.

```markdown
---

## Section 1: Complaint Cluster Leaderboard

| Rank | Cluster | Reviews | Score | Tier |
|---|---|---|---|---|
| 1 | [cluster name] | [N] | [score] | Critical/High/Medium |
| 2 | ... | ... | ... | ... |

### Cluster 1: [cluster name]
**Score:** [N] | **Reviews in cluster:** [N]

> ★☆☆☆☆ "[exact reviewer text]" — [YYYY-MM-DD]
> ★★☆☆☆ "[exact reviewer text]" — [YYYY-MM-DD]
> ★☆☆☆☆ "[exact reviewer text]" — [YYYY-MM-DD]

[Repeat for each qualifying cluster — Critical and High tier, plus Medium if Gate 3 applies]
```

**Rules:**
- Cluster names must use the language reviewers actually used. "Crashes when exporting" not "export stability issues."
- 3–4 verbatim quotes per cluster, ordered by: lowest star rating first, then most recent
- Quotes must be the reviewer's exact words — no paraphrase, no grammar correction
- If a quote contains profanity or PII: replace with `[redacted]` and add `*(redacted — contains [profanity/PII])*` inline

---

## Section 2: Broken Promise Map

Always present. Content is conditional on three states.

**State A — Normal (description available, contradictions found):**

```markdown
---

## Section 2: Broken Promise Map

| Competitor Claims | Users Report | Gap | Evidence |
|---|---|---|---|
| "[verbatim store description excerpt]" | [cluster name] | [gap label] | [N] reviews |
| "[verbatim store description excerpt]" | [cluster name] | [gap label] | [N] reviews |
```

**State B — Degraded (no store description):**

```markdown
---

## Section 2: Broken Promise Map

Store description unavailable (fetched [YYYY-MM-DD], returned empty). Broken promise comparison cannot be performed.
```

**State C — Degraded (description available, no contradictions):**

```markdown
---

## Section 2: Broken Promise Map

No broken promises detected. The competitor's store description does not appear to overclaim relative to their complaint clusters. Copy directions in Sections 3–4 are based on raw complaint patterns only.
```

---

## Section 3: Landing Page H1 Bank

Always present.

```markdown
---

## Section 3: Landing Page H1 Bank

1. "[headline]" [cluster: "cluster-name"]
2. "[headline]" [cluster: "cluster-name"]
3. "[headline]" [cluster: "cluster-name"]
4. "[headline]" [cluster: "cluster-name"]  ← optional, up to 5
```

**Rules:**
- Minimum 3 headlines, maximum 5
- Each headline must cite its source cluster in brackets — `[cluster: "name"]`
- Use a phrase that appears in or is directly derived from review language — not invented
- Address the frustrated user directly ("Export without crashing") not describe them ("For users who export")
- 8 words or fewer where possible
- No banned words: powerful, robust, seamless, innovative, game-changing, streamline, leverage, revolutionize, transform
- No fabricated statistics — do not write "40% faster" unless a reviewer actually said something equivalent

---

## Section 4: Ad Copy Directions

Always present. Always exactly 3 pairs.

```markdown
---

## Section 4: Ad Copy Directions

**Direction 1**
Cluster: [cluster name]
Not that: "[phrase that mirrors what the competitor claims or a generic alternative]"
Say this: "[counter-claim grounded in the complaint evidence]"
Evidence: [N] reviewers reported [verbatim complaint summary using reviewer language]

**Direction 2**
Cluster: [cluster name]
Not that: "..."
Say this: "..."
Evidence: ...

**Direction 3**
Cluster: [cluster name]
Not that: "..."
Say this: "..."
Evidence: ...
```

**Rules:**
- Exactly 3 directions — no more, no fewer
- Each "Say this" must be traceable to a specific cluster (cite it in the `Cluster:` line)
- "Say this" is a counter-claim, not just the opposite of "Not that" — it must be grounded in evidence
- If `product_context` was provided by the user, make "Say this" specific to that product's features
- No banned words in either "Not that" or "Say this"

---

## Section 5: Anti-Claim Warnings

Always present. Content is conditional.

**Normal state (broken promises found in Section 2):**

```markdown
---

## Section 5: Anti-Claim Warnings

**Do not claim:** "[verbatim store description claim]"
Reason: [N] of their users explicitly say this is false.
They say: > "[best verbatim quote from the cluster]"

[Repeat for each broken promise from Section 2]
```

**Degraded state (Section 2 was in a degraded state):**

```markdown
---

## Section 5: Anti-Claim Warnings

No store description was available for comparison. Anti-claim warnings require broken promise data from Section 2. Run the skill on an app with a visible store description to generate this section.
```

---

## Data Quality Notes

Always appended after Section 5. Not a numbered section — a plain footer.

```markdown
---

## Data Quality Notes

- All complaint quotes are verbatim from collected reviews — no paraphrase, no editing
- Store description fetched: [YYYY-MM-DD] | Status: [available/unavailable]
- Collection package: [itunes-rss-api | google-play-scraper]
- Reviews collected: [N] total | [N] low-star (1–3★) used for analysis
- Complaint weight formula: `(4 - rating) × recency_factor` — see references/scoring.md
- [If Gate 3 triggered]: LOW CONFIDENCE — only [N] clusters met minimum evidence threshold
```
