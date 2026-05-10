# Output Format — domain-expired-opportunity-finder

This document defines the exact output schema for both Shortlist and Audit modes.
All output must follow this structure precisely.

---

## Output Modes

### Shortlist Mode (default)
Returns only candidates with `recommended_action` of `high-priority-review`,
`review`, or `rebuild-only-review`. Rejected candidates are excluded.
Optimized for operator review — compact, decision-ready.

### Audit Mode
Returns ALL candidates, including rejected ones. Each candidate includes
full dimension breakdowns. Use this mode to understand why candidates were
rejected or down-ranked.

To request audit mode, the user says: "run in audit mode" or "show all candidates including rejects."

---

## JSON Schema — Shortlist Mode

```json
{
  "skill": "domain-expired-opportunity-finder",
  "run_date": "YYYY-MM-DD",
  "target_niche": "string — the niche used for scoring",
  "seed_keywords": ["array of seed keywords used, if any"],
  "intended_use": "rebuild | redirect | either",
  "candidates_evaluated": 0,
  "candidates_shortlisted": 0,
  "candidates_rejected": 0,
  "scoring_mode": "llm-enhanced | rule-based-only",
  "shortlist": [
    {
      "domain": "example.com",
      "opportunity_score": 81,
      "confidence": "high | medium | low",
      "recommended_action": "high-priority-review | review | rebuild-only-review",
      "redirect_suitability": "high | medium | low | not-recommended",
      "topical_fit_summary": "One or two sentences on niche alignment evidence.",
      "activity_level_summary": "One or two sentences on historical snapshot density.",
      "content_quality_summary": "One or two sentences on historical title/meta quality.",
      "history_summary": "One or two sentences on prior use and cleanliness.",
      "risk_flags": ["topic_mismatch", "spam_content_risk"],
      "why_selected": "Human-readable rationale for why this domain made the shortlist.",
      "why_risky": "Human-readable rationale for caution, even for selected domains."
    }
  ],
  "guardrails_disclaimer": "These results are research recommendations, not guarantees of SEO value. Redirect analysis should only be considered when strong topic continuity exists between the expired domain and your target site. Search engine algorithms change frequently. Always perform manual due diligence — including checking current index status, reviewing the full backlink profile with a commercial tool, and verifying domain history — before making any acquisition decision. This skill does not endorse or facilitate manipulative SEO practices."
}
```

---

## JSON Schema — Audit Mode

Includes all fields from Shortlist Mode, plus:

```json
{
  "all_candidates": [
    {
      "domain": "example.com",
      "opportunity_score": 34,
      "confidence": "low",
      "recommended_action": "reject",
      "redirect_suitability": "not-recommended",
      "dimension_breakdown": {
        "topical_relevance": { "score": 5, "max": 30, "notes": "No keyword match, historical content unrelated" },
        "historical_activity_level": { "score": 12, "max": 25, "notes": "Consistent snapshots but large gap in 2021" },
        "historical_content_quality": { "score": 3, "max": 15, "notes": "Heavy exact-match money keywords in titles" },
        "history_cleanliness": { "score": 8, "max": 15, "notes": "3 years of snapshots, some gaps" },
        "redirect_suitability": { "score": 2, "max": 10, "notes": "Historical topic does not match target niche" },
        "signal_completeness": { "score": 4, "max": 5, "notes": "RDAP lookup failed" }
      },
      "risk_flags": ["topic_mismatch", "spam_content_risk"],
      "rejection_reason": "Topic mismatch (High severity) combined with spammy historical content.",
      "topical_fit_summary": "...",
      "activity_level_summary": "...",
      "content_quality_summary": "...",
      "history_summary": "...",
      "why_selected": null,
      "why_risky": "Domain has no topical overlap with target niche and titles show signs of keyword stuffing."
    }
  ]
}
```

---

## Field Reference

| Field | Type | Required | Description |
|---|---|---|---|
| `domain` | string | Yes | Candidate domain name (no protocol, no trailing slash) |
| `opportunity_score` | integer | Yes | Final weighted score, 0–100 |
| `confidence` | enum | Yes | `high`, `medium`, or `low` — reflects evidence completeness |
| `recommended_action` | enum | Yes | `high-priority-review`, `review`, `rebuild-only-review`, or `reject` |
| `redirect_suitability` | enum | Yes | `high`, `medium`, `low`, or `not-recommended` |
| `topical_fit_summary` | string | Yes | 1–2 sentence explanation of niche alignment |
| `activity_level_summary` | string | Yes | 1–2 sentence explanation of snapshot/activity density |
| `content_quality_summary` | string | Yes | 1–2 sentence explanation of historical title quality |
| `history_summary` | string | Yes | 1–2 sentence explanation of prior use and cleanliness |
| `risk_flags` | array | Yes | Array of flag strings (empty array if none) |
| `why_selected` | string | Yes* | Rationale for inclusion. *Null for rejected candidates in audit mode. |
| `why_risky` | string | Yes | Rationale for caution, present even for selected domains |
| `dimension_breakdown` | object | Audit only | Per-dimension score, max, and notes |
| `rejection_reason` | string | Audit only | Why the candidate was rejected |

---

## Redirect Suitability Mapping

| Score (out of 10) | Label |
|---|---|
| 8–10 | `high` |
| 5–7 | `medium` |
| 2–4 | `low` |
| 0–1 | `not-recommended` |

---

## Example Complete Output — Shortlist Mode

```json
{
  "skill": "domain-expired-opportunity-finder",
  "run_date": "2026-05-10",
  "target_niche": "developer tools",
  "seed_keywords": ["devops", "CI/CD", "code editor", "IDE"],
  "intended_use": "either",
  "candidates_evaluated": 8,
  "candidates_shortlisted": 3,
  "candidates_rejected": 5,
  "scoring_mode": "llm-enhanced",
  "shortlist": [
    {
      "domain": "devtoolsweekly.com",
      "opportunity_score": 86,
      "confidence": "high",
      "recommended_action": "high-priority-review",
      "redirect_suitability": "high",
      "topical_fit_summary": "Domain name contains 'devtools'. Wayback snapshots confirm it was a weekly newsletter covering developer tools and IDE plugins from 2019 to 2024.",
      "activity_level_summary": "High snapshot frequency across 6 consecutive years, indicating sustained active use.",
      "content_quality_summary": "Historical page titles are predominantly branded ('DevTools Weekly') and natural. No keyword stuffing detected.",
      "history_summary": "6 years of consistent Wayback snapshots (2019–2024). All snapshots show real content. No parking pages or sudden drop-offs detected.",
      "risk_flags": [],
      "why_selected": "Strong topical match to developer tools niche with a healthy activity history. Suitable for both rebuild and redirect analysis.",
      "why_risky": "No significant risk signals detected. Standard due diligence recommended before acquisition."
    },
    {
      "domain": "codeshipnews.io",
      "opportunity_score": 63,
      "confidence": "medium",
      "recommended_action": "review",
      "redirect_suitability": "medium",
      "topical_fit_summary": "Domain suggests CI/CD or shipping code. Wayback shows a blog about deployment automation, adjacent to developer tools.",
      "activity_level_summary": "Moderate activity. Captures exist but are clustered rather than continuous.",
      "content_quality_summary": "Titles are somewhat generic but generally readable. Not alarming but worth noting.",
      "history_summary": "3 years of snapshots (2020–2023). Clean content, no parking pages. Relatively short history.",
      "risk_flags": ["short_history"],
      "why_selected": "Adjacent to developer tools with a reasonable history. Worth manual review for rebuild potential.",
      "why_risky": "Relatively short active history (3 years). Some boilerplate titles present."
    },
    {
      "domain": "stackforgeapp.com",
      "opportunity_score": 58,
      "confidence": "medium",
      "recommended_action": "rebuild-only-review",
      "redirect_suitability": "low",
      "topical_fit_summary": "Domain suggests a developer platform. Wayback shows a SaaS landing page for a project management tool — partially related to dev tools but not a direct match.",
      "activity_level_summary": "Consistent snapshots over a 4-year period.",
      "content_quality_summary": "Mostly branded ('StackForge') titles. Clean pattern.",
      "history_summary": "4 years of snapshots. Clean, real product pages throughout.",
      "risk_flags": ["redirect_mismatch"],
      "why_selected": "Clean history makes it worth reviewing as a rebuild candidate in the developer tools space.",
      "why_risky": "Historical topic (project management SaaS) does not closely match developer tools. Redirect not recommended — topic continuity is weak."
    }
  ],
  "guardrails_disclaimer": "These results are research recommendations, not guarantees of SEO value. Redirect analysis should only be considered when strong topic continuity exists between the expired domain and your target site. Search engine algorithms change frequently. Always perform manual due diligence — including checking current index status, reviewing the full backlink profile with a commercial tool, and verifying domain history — before making any acquisition decision. This skill does not endorse or facilitate manipulative SEO practices."
}
```

---

## Save Location

Output is saved to:
```
docs/expired-domain-intel/YYYY-MM-DD.json
```

Create the directory if it does not exist:
```bash
mkdir -p docs/expired-domain-intel
```
