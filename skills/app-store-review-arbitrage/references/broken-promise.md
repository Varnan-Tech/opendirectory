# Broken Promise Detection Reference
## `app-store-review-arbitrage`

This file documents the logic for Step 5 of SKILL.md — cross-referencing the competitor's store description against complaint clusters to identify broken promises.

---

## What Is a Broken Promise?

A broken promise exists when:
1. The competitor's store description makes an **explicit, testable claim** about a behavior or feature
2. A complaint cluster documents **users directly experiencing failure** of that exact behavior or feature

A broken promise is **not**:
- A vague superlative ("world's best notes app") that is contradicted by general dissatisfaction
- A feature complaint about something the competitor never claimed to offer
- A mismatch in degree ("they said it was fast; some users found it slow") without direct failure

**The precision test:** If a user experienced the opposite of this claim and left a 1-star review citing it specifically, would that review be a direct counter-example? If yes → it is a claim worth checking.

---

## Step 1: Extract Claims from Store Description

Read `metadata.store_description`. Extract a list of specific claims.

### What counts as a claim

| Claim type | Example |
|---|---|
| Feature availability | "Export your data in any format, anytime" |
| Reliability promise | "Syncs instantly across all your devices" |
| Pricing transparency | "No hidden fees — cancel anytime" |
| Speed / performance | "Opens in under a second" |
| Completeness | "Everything you need to run your business in one place" |

### What does NOT count as a claim

| Non-claim type | Example | Why excluded |
|---|---|---|
| Marketing superlative | "The most powerful notes app" | Not testable; not a behavioral promise |
| Team/company description | "Built by a team of designers" | No user-facing behavioral implication |
| Press quote | '"AI's everything app" — Forbes' | Third-party attribution; not the developer's promise |
| Category description | "A productivity app where you can write, plan, and organize" | Describes the category, not a specific promise |
| Aspirational language | "Achieve your goals" | Too vague to falsify |

---

## Step 2: Cross-Reference Claims Against Clusters

For each extracted claim, scan all complaint cluster names and their top verbatim quotes.

**A contradiction is confirmed when:**
- The cluster name or quotes directly describe failure of the behavior the claim promises
- The failure is stated as a fact by reviewers, not as a preference ("I wish it had X")
- At least 3 reviews in the cluster support the failure

**A contradiction is NOT confirmed when:**
- The cluster is about a missing feature the claim did not promise
- The cluster describes a preference mismatch ("I prefer X approach")
- Only 1–2 isolated reviews mention the failure

---

## Step 3: Output Format

For each confirmed broken promise, produce:

```json
{
  "claim_text": "verbatim excerpt from store description — keep it short (1 sentence)",
  "complaint_cluster": "exact cluster name from /tmp/asr-clusters.json",
  "gap_label": "one phrase: Claims X; users report Y",
  "evidence_count": 18
}
```

`gap_label` format: **"Claims [what the description promises]; users report [what the cluster documents]"**

Examples:
- "Claims instant sync across devices; users report data loss after sync"
- "Claims no hidden fees; users report unexpected charges after trial"
- "Claims offline access; users report content unavailable without connection"

---

## Degraded State Handling

### No store description available
Set `"store_description_available": false` in `/tmp/asr-promises.json`.
Section 2 of the output brief must contain exactly this note:
> `Store description unavailable (fetched YYYY-MM-DD, returned empty). Broken promise comparison cannot be performed.`

Do not speculate about what the description might have claimed.

### Store description available, no contradictions found
Set `"no_contradictions_found": true`.
Section 2 of the output brief must contain exactly this note:
> `No broken promises detected. The competitor's store description does not appear to overclaim relative to their complaint clusters. Copy directions in Sections 3–4 are based on raw complaint patterns only.`

This is a valid and honest result. Do not force-find contradictions that are not there.

---

## Anti-Patterns: What the LLM Must NOT Do

| Anti-pattern | Why it's wrong |
|---|---|
| Flag vague superlatives as broken promises | "Powerful app" is not a testable claim |
| Flag feature gaps as broken promises | If the description never promised a feature, its absence is not a broken promise |
| Combine two separate claims into one broken promise | Each claim must map to one cluster; no bundling |
| Generate broken promises when `store_description` is null | Detection cannot run without a description |
| Paraphrase the store description claim | Use verbatim excerpt — the founder may cite it directly in their ad copy |
| Flag a single-review complaint as a broken promise | Minimum 3 reviews in the cluster required |

---

## Worked Example

**App:** Notion iOS (illustrative — actual reviews may differ)

**Store description excerpt:**
> "Syncs instantly across all devices. Pick up on mobile where you left off on desktop."

**Complaint cluster:** "Sync failures and data loss" (score: 48, 18 reviews)

**Top verbatim quotes:**
- ★☆☆☆☆ "I lost 3 hours of work because it didn't sync between my phone and laptop. This happens constantly." — 2026-03-12
- ★☆☆☆☆ "Sync is completely broken. My mobile shows old content even after force-closing and reopening." — 2026-04-01
- ★★☆☆☆ "Love the app but the sync is unreliable. Had to start keeping local backups." — 2026-02-20

**Broken promise record:**
```json
{
  "claim_text": "Syncs instantly across all devices.",
  "complaint_cluster": "Sync failures and data loss",
  "gap_label": "Claims instant sync; users report data loss and stale content across devices",
  "evidence_count": 18
}
```

**Resulting Anti-Claim Warning (Section 5):**
```
Do not claim: "Syncs instantly across all devices."
Reason: 18 of their users explicitly report sync failures.
They say: > "I lost 3 hours of work because it didn't sync between my phone and laptop. This happens constantly."
```
