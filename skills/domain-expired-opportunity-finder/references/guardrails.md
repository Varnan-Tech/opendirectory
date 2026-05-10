# Guardrails — domain-expired-opportunity-finder

This document defines the ethical, policy, and anti-abuse constraints
that govern how this skill frames its output and recommendations.

---

## Core Principle

This skill is a **research and triage tool**, not an acquisition engine.
It surfaces candidates for human review. It does not make buying decisions,
guarantee SEO outcomes, or encourage manipulative domain practices.

---

## Anti-Abuse Policy

### What This Skill Must NOT Encourage

1. **Private Blog Network (PBN) construction.** The skill must never suggest
   acquiring expired domains to build link networks. If the user's stated
   intent suggests PBN use, the skill should note the risk and decline to
   optimize for that use case.

2. **Deceptive redirects.** The skill must never recommend redirecting an
   expired domain to an unrelated site without clearly flagging this as
   high-risk and likely ineffective. The `redirect_mismatch` flag exists
   specifically to enforce this constraint.

3. **Unrelated domain repurposing.** Acquiring a domain with no topical
   connection to the user's niche purely for its metrics is a pattern
   the skill must actively discourage through scoring (topical relevance
   is the highest-weighted dimension at 30%).

4. **Spam domain recycling.** The skill must flag domains with spammy
   anchor profiles, suspicious registrar history, or deindex signals
   rather than presenting them as opportunities.

---

## Redirect Analysis Constraints

Redirect suitability is only rated `high` or `medium` when:

- The historical topic of the expired domain **closely matches** the
  target niche (topic continuity score ≥ 5/10)
- The content type is compatible (e.g., blog to blog, tool to tool)
- The anchor text profile is primarily branded or generic (not spammy)

If ANY of these conditions fail, redirect suitability is rated `low` or
`not-recommended`, and the `redirect_mismatch` flag is applied.

The skill must explicitly state in output when a domain is better suited
for rebuild than redirect, and explain why.

---

## Framing Rules

### Language to USE in output:
- "This domain appears worth reviewing for..."
- "Based on available evidence, this candidate shows..."
- "Manual due diligence is recommended before any acquisition decision."
- "The historical topic appears adjacent to your niche, but further
  verification is needed."
- "This assessment is based on publicly available signals and may not
  reflect the domain's current state in search engines."

### Language to AVOID in output:
- ~~"Guaranteed rankings"~~
- ~~"Link equity transfer"~~
- ~~"This domain will boost your SEO"~~
- ~~"Safe to redirect"~~ (always qualified)
- ~~"High authority domain"~~ (authority metrics are not our primary signal)
- ~~"Easy win"~~
- ~~"No-brainer acquisition"~~
- ~~"Free backlinks"~~
- ~~"Instant traffic"~~
- ~~"SEO hack"~~

---

## Required Disclaimer

Every output — in both shortlist and audit mode — must include this
disclaimer at the end:

> **Disclaimer:** These results are research recommendations, not guarantees
> of SEO value. Redirect analysis should only be considered when strong
> topic continuity exists between the expired domain and your target site.
> Search engine algorithms change frequently. Always perform manual due
> diligence — including checking current index status, reviewing the full
> backlink profile with a commercial tool, and verifying domain history —
> before making any acquisition decision. This skill does not endorse or
> facilitate manipulative SEO practices.

---

## User Intent Handling

If the user describes an intended use that conflicts with these guardrails:

| User Intent | Skill Response |
|---|---|
| "I want to build a PBN" | Note the SEO risk, explain why PBN patterns are increasingly detected, and proceed with scoring but add a warning to every output. Do not optimize for PBN use. |
| "I want to redirect unrelated domains" | Apply `redirect_mismatch` flag to all candidates where topic continuity is weak. Explain why unrelated redirects are unreliable. Still provide rebuild recommendations if applicable. |
| "I want cheap domains for link building" | Clarify that expired domain acquisition for link building carries inherent risk. Score normally but ensure `why_risky` explanations are thorough. |
| "I want to find domains in my niche to rebuild" | This is the ideal use case. Proceed normally with full scoring. |

---

## Transparency Requirements

1. Every shortlisted domain must include BOTH `why_selected` AND `why_risky`.
   Even the best candidates have some level of risk or uncertainty.

2. The `scoring_mode` field must indicate whether LLM-enhanced or rule-based-only
   scoring was used, so the user understands the depth of analysis.

3. If data sources were unavailable or returned no results for a candidate,
   this must be reflected in the `confidence` level and `signal_completeness`
   dimension.

4. The skill must never present a score without the ability for the user
   to understand how it was computed (by referencing `references/scoring-model.md`).
