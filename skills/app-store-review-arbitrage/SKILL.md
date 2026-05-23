---
name: app-store-review-arbitrage
description: "Fetches low-star App Store and Google Play reviews, clusters them into broken-promise patterns, and generates a ranked copy brief with positioning opportunities."
version: 1.0.0
compatibility: [claude-code, gemini-cli, github-copilot]
---

# app-store-review-arbitrage

Convert a competitor's App Store or Google Play URL into a one-session GTM brief: ranked complaint clusters, a broken promise map, landing page headlines, and ad copy directions — all sourced from verbatim reviews.

---

## Critical Rules (read before Step 1)

These rules apply throughout all steps. Violating any of them fails Self-QA (Step 6).

1. **Every quote must be verbatim.** No paraphrase, no grammar correction, no cleaning. Exact reviewer words only.
2. **No fabricated statistics.** Do not write "40% faster" or "2× more reliable" unless a reviewer explicitly used similar language. The Self-QA step checks for uncited percentages.
3. **Cluster names must use reviewer language.** Study the anti-pattern table in Step 3.
4. **Every headline and ad copy direction must cite its source cluster.** Format: `[cluster: "cluster-name"]`.
5. **Section 2 is always present** in the output — even when degraded. Never skip or omit it.
6. **No banned words** in any generated copy: powerful, robust, seamless, innovative, game-changing, streamline, leverage, revolutionize, transform.

---

## Step 1 — Parse Input and Detect Platform

Accept a natural language prompt containing one app URL. Extract the URL.

**Platform detection:**
- `apps.apple.com` → App Store
- `play.google.com/store/apps/details?id=` → Google Play
- Any other URL → stop and respond: "Please provide a direct App Store or Google Play URL. I can't analyse review data from other sources."

**ID extraction (do this before calling the script):**

| Platform | What to extract | How |
|---|---|---|
| App Store | Numeric `app_id` | Digits after `/id` in the URL |
| App Store | `country` | 2-letter code after `apps.apple.com/` (e.g., `us`, `gb`) |
| Google Play | `package_name` | Value of `id=` query parameter |

Persist the extracted values — you will need them for the output filename in Step 7.

If `product_context` was provided in the user's prompt (what their own product does), store it — used to personalise copy in Step 5.

---

## Step 2 — Collect Reviews & Metadata

Run the full fetch script:

```bash
python3 scripts/fetch_reviews.py "{app_url}" --output {tmpdir}/asr-raw.json
```
*(Note: Replace `{tmpdir}` with your operating system's temp directory, e.g., `/tmp` on macOS/Linux or `C:\Temp` on Windows).*

This fetches both the store description metadata and the reviews.
- **App Store:** iTunes API — free, no auth. App Store reviews are fetched via Apple's public iTunes RSS feed. Some apps return 0 reviews due to Apple's API limitations — in that case the skill continues with available data and logs a warning. Google Play is the primary supported path.
- **Google Play:** `google-play-scraper` package — free, no auth

If the script fails, read the error from stderr. Common causes:
- Package not installed: run `pip install google-play-scraper`
- App not found: verify the URL is a current, live listing
- Google Play API error: run `pip install --upgrade google-play-scraper` and retry

The script will print collection progress to stderr. Wait for it to complete. After completion, read `{tmpdir}/asr-raw.json` and display the collection summary to the user:
```
✓ Collected [N] reviews ([N] low-star 1–3★) from [platform]
  Date range: [oldest] to [newest]
  Package: [iTunes API | google-play-scraper]
```

**Check the exit code:**
- Exit 0 → collection succeeded, check `metadata.store_description`. If null: note this — Section 2 will use the degraded state. Proceed to Step 3.
- Exit 1 → error (read stderr message, surface it to user, stop)
- Exit 2 → **Gate 1 triggered** (< 10 low-star reviews found)

**Gate 1 — Low signal stop:** If the script exits with code 2, read the `gate_message` from `{tmpdir}/asr-raw.json` and surface it to the user verbatim. Do not proceed to Step 3. Do not produce a partial brief.

---

## Step 3 — Complaint Clustering

Load `low_star_reviews` from `{tmpdir}/asr-raw.json`.

Cluster all low-star reviews into **4–6 named complaint themes.** Apply this formula to score each review:

```
complaint_weight = (4 - rating) × recency_factor

recency_factor:
  review age ≤ 90 days  → 1.0
  review age 91–365 days → 0.7
  review age > 365 days  → 0.4
```

`review age` = (today's date) − (review `date` field) in days.

`cluster_score` = sum of `complaint_weight` for all reviews in the cluster.

**Cluster naming — critical rule:**

You will want to write abstract names. Resist. Use the exact verb and noun from reviews.

| ❌ Abstracted (wrong) | ✅ Reviewer language (correct) |
|---|---|
| "Stability issues" | "Crashes when exporting to PDF" |
| "Sync problems" | "Data lost after sync between phone and desktop" |
| "Monetisation friction" | "Paywall appears after 3 days, not 14 as promised" |
| "Performance degradation" | "App freezes every time I search" |
| "Onboarding issues" | "Can't figure out how to invite a teammate" |

**Rules:**
- Each review belongs to exactly one cluster (assign to its dominant theme)
- Discard any cluster with fewer than 3 reviews — log it as noise
- Select 3–4 verbatim quotes per cluster: lowest star rating first, then most recent

**Gate 2 — Minimum cluster size:** After discarding sub-3-review clusters, check how many clusters remain.

**Gate 3 — Low-confidence flag:** If fewer than 3 clusters remain:
- Do NOT stop. Continue to output.
- Prepend this to the brief header immediately after the app metadata:
  > ⚠ **LOW CONFIDENCE:** Only [N] complaint cluster(s) met the minimum evidence threshold (≥ 3 supporting reviews). Output reflects limited data. Consider a competitor with more reviews, or broaden the rating filter.
- Include Medium-tier clusters in the output (score ≥ 5)

**Tier classification** (for the leaderboard table in Section 1):
- Critical: score ≥ 60
- High: score 15–59
- Medium: score 5–14 (include only when Gate 3 applies)
- Noise: score < 5 (discard, do not include)

Write clusters to `{tmpdir}/asr-clusters.json`:
```json
{
  "clusters": [
    {
      "name": "cluster name in reviewer language",
      "score": 34.5,
      "tier": "High",
      "review_count": 14,
      "verbatim_quotes": [
        {"rating": 1, "text": "exact reviewer words", "date": "YYYY-MM-DD"},
        ...
      ]
    }
  ],
  "discarded_noise": 2,
  "gate_3_triggered": false
}
```

---

## Step 4 — Broken Promise Detection

**This is the step that differentiates this skill from every existing tool. It must run as a distinct, named step.**

Load:
- `metadata.store_description` from `{tmpdir}/asr-raw.json`
- All clusters from `{tmpdir}/asr-clusters.json`

**If `store_description` is null:** Set `store_description_available: false`. Write `{tmpdir}/asr-promises.json` with empty `broken_promises` array and `detection_note` as specified below. Proceed to Step 5.

**If store description is available:**

1. **Extract claims.** A claim is any specific, testable assertion about app behavior. See `references/broken-promise.md` for the full definition and examples. Exclude vague superlatives, team descriptions, and press quotes.

2. **Cross-reference.** For each claim, check all cluster names and verbatim quotes. A contradiction exists when the cluster directly documents failure of the promised behavior (minimum 3 reviews).

3. **Produce broken promise records** — one per confirmed contradiction:
   ```json
   {
     "claim_text": "verbatim excerpt from store description",
     "complaint_cluster": "exact cluster name",
     "gap_label": "Claims X; users report Y",
     "evidence_count": 18
   }
   ```

Write to `{tmpdir}/asr-promises.json`:
```json
{
  "store_description_available": true,
  "broken_promises": [...],
  "no_contradictions_found": false,
  "detection_note": null
}
```

**Degraded states:**
- No description: `store_description_available: false`, `detection_note: "Store description unavailable (fetched YYYY-MM-DD, returned empty). Broken promise comparison cannot be performed."`
- No contradictions: `no_contradictions_found: true`, `detection_note: "No broken promises detected. Store description does not appear to overclaim relative to complaint clusters."`

See `references/broken-promise.md` for anti-patterns (what NOT to flag).

---

## Step 5 — Generate Copy

Using clusters from Step 3 and broken promises from Step 4, generate Sections 3–5 of the brief.

**Copy rules (apply to all three sections):**
- Every headline and direction must cite its source cluster: `[cluster: "cluster-name"]`
- No banned words: powerful, robust, seamless, innovative, game-changing, streamline, leverage, revolutionize, transform
- No fabricated statistics — no percentages or numbers unless a reviewer used them
- If `product_context` was provided: make "Say this" directions specific to that product's features. If not: write as positioning templates the user fills in.
- Use reviewer language in headlines — derive from or quote actual review text

**Section 3 — Landing Page H1 Bank** (3–5 headlines):
- Each: `"[headline text]" [cluster: "cluster-name"]`
- ≤ 8 words where possible
- Address the frustrated user directly

**Section 4 — Ad Copy Directions** (exactly 3 pairs):
```
Cluster: [cluster name]
Not that: "[what the competitor claims or a generic weak alternative]"
Say this: "[counter-claim grounded in complaint evidence]"
Evidence: [N] reviewers reported [verbatim complaint summary]
```

**Section 5 — Anti-Claim Warnings:**
- One warning per broken promise from Step 4
- If Section 2 is degraded: single note (see `references/brief-format.md` for exact wording)

---

## Step 6 — Self-QA

Before saving, verify the generated brief against these checks. If any check fails, fix the specific item and re-verify — do not save a failing brief.

| Check | Rule |
|---|---|
| Verbatim quotes present | Every cluster has ≥ 2 verbatim quotes |
| No banned words | None of the 9 banned words appear in Sections 3–5 |
| No uncited percentages | Any `%` in output must trace to a reviewer's actual words |
| All copy cited | Every headline and "Say this" has a `[cluster: "name"]` citation |
| Cluster count ≥ 1 | At least one cluster survived Gates 2/3 |
| Section 2 present | Section 2 appears in the output (in any state) |
| Quote ratings ≤ 3 | All verbatim quotes came from 1–3★ reviews |

**Note on cluster count:** The minimum for a passing brief is 1 cluster (not 3). The Gate 3 low-confidence flag handles cases where < 3 clusters survive — that is a warning, not a failure. Self-QA fails only if 0 clusters exist.

---

## Step 7 — Save Output

Assemble the full brief per the format in `references/brief-format.md`.

Save to:
```
docs/review-briefs/[app-id]-[YYYY-MM-DD].md
```

Create the `docs/review-briefs/` directory if it does not exist.

Print the full brief to the user.

Clean up temp files: `{tmpdir}/asr-raw.json`, `{tmpdir}/asr-clusters.json`, `{tmpdir}/asr-promises.json`.
