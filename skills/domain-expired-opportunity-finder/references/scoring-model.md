# Scoring Model — domain-expired-opportunity-finder

This document defines the transparent, weighted scoring model used to evaluate
expired domain candidates. Every score is explainable — no black-box ranking.

---

## Scoring Dimensions

The skill scores each candidate across 6 dimensions. Each dimension has a
defined weight, maximum point value, and the signals used to compute it.

### 1. Topical Relevance (30 points, weight 30%)

**Purpose:** Does this domain historically align with the user's target niche?

**Signals:**
- Domain string keyword match against `target_niche` and `seed_keywords`
- Historical page titles from Wayback CDX snapshots
- Historical meta descriptions and visible text (when available)
- LLM niche-fit assessment (when LLM API key is configured)

**Scoring Rules:**
- 25–30: Strong keyword match in domain name AND historical content confirms niche
- 18–24: Partial keyword match OR historical content is adjacent to niche
- 10–17: Weak or indirect topical connection
- 0–9: No meaningful topical overlap detected

**Why Highest Weight:** Topical mismatch is the #1 trap in expired domain
acquisition. A high-authority domain in the wrong niche is worse than a
moderate domain in the right niche.

---

### 2. Historical Activity Level (25 points, weight 25%)

**Purpose:** Does the domain have a sustained track record of active use?

**Signals:**
- Wayback CDX snapshot frequency over time
- Density of snapshots during active years
- Absence of prolonged dormant periods (excluding post-expiry)

**Scoring Rules:**
- 20–25: High snapshot frequency spanning multiple years continuously
- 13–19: Moderate activity, some years with lower capture rates
- 6–12: Low overall activity or large multi-year gaps
- 0–5: Barely any snapshots, very sparse activity history

**Key Principle:** A domain with a deep, sustained archive history provides
more evidence of legitimate past use than a domain that only existed briefly.

---

### 3. Historical Content Quality (15 points, weight 15%)

**Purpose:** Does the archived content look natural or keyword-stuffed?

**Signals:**
- Keyword stuffing in historical `<title>` tags
- Unnatural phrasing in meta descriptions
- Language consistency (sudden language shifts in history)

**Scoring Rules:**
- 12–15: Natural titles, branded focus, readable descriptions
- 8–11: Some exact-match keywords but generally readable
- 4–7: Heavy exact-match keywords or boilerplate titles
- 0–3: Predominantly spammy, nonsensical, or foreign-language shifts

**Red Flag:** If historical titles are heavily stuffed with money keywords, the
`spam_content_risk` flag is triggered regardless of score.

---

### 4. History Cleanliness (15 points, weight 15%)

**Purpose:** Was this domain used legitimately before it expired?

**Signals:**
- Wayback CDX snapshot count (more = longer verifiable history)
- First and last capture dates (years of active use)
- HTTP status code consistency across snapshots (200s vs 301s/404s)
- Absence of parking page patterns (e.g., Sedo, GoDaddy parked pages)
- No sudden activity drop-offs suggesting deindexing

**Scoring Rules:**
- 12–15: 5+ years of consistent snapshots, clean status codes, real content
- 8–11: 2–5 years of history, mostly clean, minor gaps
- 4–7: Short history OR significant gaps OR some parking page evidence
- 0–3: Very sparse history, mostly parking pages, or suspicious patterns

---

### 5. Redirect Suitability (10 points, weight 10%)

**Purpose:** If the user wants to redirect this domain, is the historical
topic close enough to the target niche to make that plausible?

**Signals:**
- Topic continuity score (overlap between historical topic and target niche)
- Content type match (was it a blog, tool, company site, etc.)
- Audience overlap estimate (did the historical audience align with target?)

**Scoring Rules:**
- 8–10: Historical topic is the same or very closely adjacent to target niche
- 5–7: Some topic overlap, partially plausible redirect
- 2–4: Weak overlap, redirect would be a stretch
- 0–1: No meaningful topic continuity — redirect not recommended

**Key Constraint:** If `intended_use` is set to `rebuild`, this dimension
is scored but does not penalize the overall opportunity_score. If `intended_use`
is `redirect`, this dimension's weight effectively doubles in the recommendation logic.

---

### 6. Signal Completeness (5 points, weight 5%)

**Purpose:** How much evidence do we actually have for this candidate?

**Signals:**
- Percentage of data sources that returned usable data
- Whether Wayback and RDAP both succeeded
- Whether LLM analysis was available (if API key configured)

**Scoring Rules:**
- 4–5: All available data sources returned data
- 2–3: Most sources returned data, 1–2 gaps
- 0–1: Significant data gaps — multiple sources failed or returned nothing

**Why This Matters:** A domain that looks promising but has almost no
verifiable data should not rank as highly as one with strong evidence.
Missing signals reduce confidence, not boost it.

---

## Total Score Computation

```
opportunity_score = topical_relevance
                  + historical_activity_level
                  + historical_content_quality
                  + history_cleanliness
                  + redirect_suitability
                  + signal_completeness
```

**Range:** 0–100 points.

---

## Confidence Mapping

Confidence reflects how much evidence exists behind the score.

| Condition | Confidence Level |
|---|---|
| ≥ 4 of 6 dimensions have strong data (non-zero signals) | `high` |
| 3 of 6 dimensions have strong data | `medium` |
| ≤ 2 dimensions have strong data | `low` |

**Rule:** A domain with `low` confidence can never receive `high-priority-review`,
regardless of its opportunity_score.

---

## Recommendation Logic

| Score Range | Confidence | Recommended Action |
|---|---|---|
| ≥ 75 | `high` | `high-priority-review` |
| ≥ 55 | `medium` or `high` | `review` |
| ≥ 55 | any, BUT redirect_suitability < 4/10 | `rebuild-only-review` |
| < 55 | any | `reject` |
| any | any, WITH critical risk flag (severity = High) | `reject` (unless override) |

**Override Rule:** A single High-severity risk flag (e.g., `topic_mismatch`,
`spam_content_risk`, `possible_deindex`) automatically caps the recommendation
at `review` or lower, even if the score is ≥ 75.

---

## Example Scoring Walkthrough

**Candidate:** `devtoolsweekly.com` | **Target Niche:** `developer tools`

| Dimension | Score | Rationale |
|---|---|---|
| Topical Relevance | 28/30 | "devtools" in domain, Wayback shows newsletter about dev tools |
| Historical Activity | 18/25 | Consistent snapshot captures across multiple years |
| Content Quality | 12/15 | Natural titles ("DevTools Weekly - Issue #45") |
| History Cleanliness | 14/15 | 6 years of consistent snapshots, no parking pages |
| Redirect Suitability | 9/10 | Direct topic match — dev tools to dev tools |
| Signal Completeness | 5/5 | All sources returned data |

**Total:** 86/100 | **Confidence:** `high` | **Action:** `high-priority-review`
