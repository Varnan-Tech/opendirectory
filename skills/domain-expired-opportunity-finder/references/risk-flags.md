# Risk Flags — domain-expired-opportunity-finder

This document defines the risk flags that the skill can attach to any
candidate domain. Risk flags serve two purposes:

1. They explain WHY a domain may be risky despite looking attractive.
2. They influence the recommendation logic (high-severity flags cap recommendations).

---

## Flag Definitions

### `topic_mismatch`
- **Severity:** High
- **Trigger:** Historical topic and target niche overlap score < 30% (based on
  Wayback content analysis and anchor text review)
- **Effect:** Caps recommendation at `reject` for redirect use cases.
  For rebuild use cases, caps at `review` (never `high-priority-review`).
- **Why It Matters:** Acquiring a domain with no topical connection to your
  niche is the most common and most damaging expired domain mistake. Search
  engines increasingly detect and devalue unrelated redirects.

---

### `spam_content_risk`
- **Severity:** High
- **Trigger:** Historical page titles or meta descriptions consist predominantly of
  exact-match money keywords, nonsensical text, or foreign-language spam unrelated to the
  domain's apparent topic
- **Effect:** Caps recommendation at `review` (never `high-priority-review`).
  Adds explicit warning in `why_risky` field.
- **Why It Matters:** Spammy historical content suggests the domain was used
  for link schemes or low-quality affiliate sites. The historical value is unreliable.

---

### `weak_historical_activity`
- **Severity:** Medium
- **Trigger:** Wayback snapshot count is extremely low (e.g., < 10 total snapshots
  across its lifetime) but avoids the `unclear_history` threshold.
- **Effect:** Lowers `historical_activity_level` score. Does not automatically
  reject but reduces overall opportunity_score.
- **Why It Matters:** Expired domains with very low historical activity have had
  less time to build natural authority. While not inherently spammy, they offer
  less evidence of sustained value.

---

### `unclear_history`
- **Severity:** Medium
- **Trigger:** Fewer than 3 Wayback CDX snapshots exist for the domain,
  OR all available snapshots resolve to parking pages (Sedo, GoDaddy parked,
  domain-for-sale pages)
- **Effect:** Reduces `history_cleanliness` score. Lowers confidence level
  by one step (e.g., `high` → `medium`).
- **Why It Matters:** Without verifiable history, there is no way to confirm
  what the domain was previously used for. It could have been legitimate,
  or it could have been a spam site that was cleaned. Ambiguity should
  reduce confidence, not be ignored.

---

### `possible_deindex`
- **Severity:** High
- **Trigger:** Wayback CDX data shows years of regular snapshots followed by a
  sudden complete stop (no snapshots for 2+ years before expiry), suggesting the
  domain may have been deindexed or penalized before it expired
- **Effect:** Caps recommendation at `review`. Adds explicit warning about
  potential search engine penalties in `why_risky` field.
- **Why It Matters:** A domain that was deindexed carries legacy penalties
  that may transfer even after acquisition. This is one of the highest-risk
  scenarios in expired domain acquisition.

---

### `redirect_mismatch`
- **Severity:** Medium
- **Trigger:** Redirect suitability score is below 4/10 (weak topic continuity
  between historical use and intended target)
- **Effect:** Changes recommendation from `review` to `rebuild-only-review`.
  Explicitly notes in output that redirect analysis is not recommended.
- **Why It Matters:** Redirecting a domain to an unrelated site is increasingly
  treated as manipulative by search engines. Even when done with good intentions,
  a topic-mismatched redirect is unlikely to pass meaningful value.

---

### `short_history`
- **Severity:** Low
- **Trigger:** Domain was actively used for less than 1 year before expiring
  (based on Wayback first and last capture dates)
- **Effect:** Minor reduction to `history_cleanliness` score. No recommendation
  cap.
- **Why It Matters:** Domains with very short histories have had less time to
  build natural authority. They are not necessarily bad, but they offer less
  evidence of sustained value.

---

### `suspicious_registrar`
- **Severity:** Medium
- **Trigger:** Registration data (RDAP) shows the domain was registered through a registrar
  commonly associated with bulk domain spam operations (pattern-matched against
  a known list of high-spam registrars)
- **Effect:** Lowers confidence by one step. Adds note in `why_risky`.
- **Why It Matters:** Domains registered through bulk-spam registrars have a
  higher probability of having been used for link schemes, PBNs, or other
  manipulative purposes, even if the current signals look clean.

---

## Severity Interaction Rules

1. **Any High-severity flag** → recommendation is capped at `review` or lower.
   A domain can never be `high-priority-review` with an active High flag.

2. **Two or more Medium-severity flags** → treated as equivalent to one High
   flag for recommendation capping purposes.

3. **Low-severity flags** → informational only. They appear in output but do
   not cap recommendations.

4. **Flag stacking** → multiple flags of the same severity do not compound
   further than the rules above. Two High flags are treated the same as one
   High flag for capping purposes (the cap is already at `review`).

---

## Flag Presentation in Output

Every flagged domain includes:
- The flag name in the `risk_flags` array
- A human-readable explanation in `why_risky`
- The severity level is documented here but not repeated in output
  (to keep output compact — operators can reference this file for severity details)
