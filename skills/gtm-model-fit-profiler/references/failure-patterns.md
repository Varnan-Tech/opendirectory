# GTM Model Fit Profiler — Failure Pattern Catalog

This document defines all failure patterns the skill checks after scoring. Every evaluation must include a failure-pattern scan.

---

## Severity Scale

| Severity | Definition | Impact on Recommendation |
|----------|------------|--------------------------|
| Low | Minor issue, does not materially affect usability | Note in report, no score adjustment |
| Medium | Noticeable issue that reduces reliability for GTM use | Flag in report, consider downgrading recommendation by one tier |
| High | Critical issue that makes output unsafe or misleading for GTM decisions | Flag prominently, cap recommendation at "usable with review" or lower |

---

## Universal Failure Patterns

These apply to every workload evaluation.

### Hallucinated claims
The model states facts, statistics, company details, or market data that are not present in the input and cannot be verified.

Detection heuristics:
- Claims about specific revenue, funding, employee count not in the source material
- Named competitor comparisons not grounded in input
- Statistics or percentages with no source

Default severity: **High**

### Generic filler language
The model pads output with vague, non-specific statements that add no information.

Detection heuristics:
- Phrases like "in today's fast-paced market", "companies are increasingly looking to"
- Statements that could apply to any company in any industry
- Repetition of the same idea in different words

Default severity: **Medium**

### Unsupported certainty
The model expresses high confidence about conclusions that lack sufficient evidence.

Detection heuristics:
- Definitive claims ("this proves", "clearly shows", "undeniably") based on limited data
- Predictions stated as facts
- Recommendations without caveats when evidence is thin

Default severity: **High**

### Weak reasoning chain
The model reaches conclusions without showing logical steps from evidence to insight.

Detection heuristics:
- Jumps from observation to recommendation without intermediate reasoning
- Conclusions that don't follow from the evidence presented
- Missing "because" or "since" connectors in analytical sections

Default severity: **Medium**

### Format drift
The model ignores the requested output structure and produces its own format.

Detection heuristics:
- Missing required sections from the output template
- Reordered sections without reason
- Narrative paragraphs where structured output was requested

Default severity: **Low**

### Context drift
The model starts addressing topics or workloads not specified in the evaluation request.

Detection heuristics:
- Advice about workloads not under evaluation
- Tangential recommendations outside the stated business context
- Scope creep into adjacent but unrequested analysis

Default severity: **Medium**

---

## Market Research Failure Patterns

### Fake themes from thin evidence
The model fabricates market themes or trends based on minimal or ambiguous input signals.

Detection heuristics:
- Themes claimed from a single data point
- Trend language ("growing trend", "emerging pattern") without supporting evidence
- Themes that contradict the source material

Default severity: **High**

### Generic persona statements
The model describes buyer personas in vague, universally applicable terms.

Detection heuristics:
- Persona descriptions with no industry or role specificity
- Pain points that apply to every B2B buyer ("wants to save time", "needs better data")
- No connection between persona and the source material's specifics

Default severity: **Medium**

### Shallow clustering
The model groups findings into clusters that are too broad, too narrow, or overlapping to be actionable.

Detection heuristics:
- Clusters like "technology challenges" or "growth issues" that are too broad
- Single-item clusters that aren't meaningfully distinct
- Significant overlap between cluster definitions

Default severity: **Medium**

### No ICP mapping
The model summarizes findings without connecting them to the user's ideal customer profile or buyer segments.

Detection heuristics:
- Analysis that never references the business context or ICP
- Findings presented in isolation from the target market
- No segment-level recommendations

Default severity: **Medium**

---

## Pricing / Competitor Analysis Failure Patterns

### Invented pricing details
The model fabricates specific pricing tiers, feature lists, or pricing amounts not present in the source material.

Detection heuristics:
- Specific dollar amounts not in the input
- Feature-tier mappings not supported by the source
- Competitor pricing details stated as fact without source

Default severity: **High**

### Surface-level comparison only
The model lists feature differences without analyzing strategic implications.

Detection heuristics:
- Pure feature matrix without "so what" analysis
- No mention of target segments, positioning, or market strategy
- Comparison reads like a spec sheet, not strategic analysis

Default severity: **Medium**

### Missing strategic interpretation
The model describes what the pricing is but not why it exists or what it signals.

Detection heuristics:
- No discussion of pricing strategy (penetration, skimming, value-based)
- No mention of competitive positioning intent
- No connection between packaging and target segment

Default severity: **Medium**

### Weak pricing recommendation logic
The model makes pricing recommendations without clear reasoning or trade-off analysis.

Detection heuristics:
- "You should lower your price" without explaining impact
- Recommendations that ignore competitive dynamics
- No acknowledgment of risks or trade-offs in recommended moves

Default severity: **Medium**

---

## Outreach Personalization Failure Patterns

### Fake personalization
The model includes the company name or role title but the message body is generic and interchangeable.

Detection heuristics:
- Remove the company name — does the message still make sense for any company? If yes, it is fake personalization.
- Personalization limited to "[Company] is doing great things"
- No reference to specific signals, events, or context from the source material

Default severity: **High**

### Templated opener
The opening line follows a recognizable AI outreach template.

Detection heuristics:
- "I noticed that your company is...", "I came across your profile and..."
- "Hope this finds you well", "I was impressed by..."
- Any opener that could be generated without knowing anything about the recipient

Default severity: **Medium**

### Overlong copy
The outreach message is too long for the channel and context.

Detection heuristics:
- Cold email exceeding 150 words
- LinkedIn message exceeding 100 words
- Multiple paragraphs where 2-3 sentences would suffice

Default severity: **Low**

### Awkward or pushy CTA
The call-to-action feels forced, overly aggressive, or mismatched with the relationship stage.

Detection heuristics:
- "Let me know when you're free for a 30-minute demo" in a cold first touch
- Multiple CTAs competing for attention
- CTA assumes a level of interest or relationship that doesn't exist

Default severity: **Medium**

---

## Reporting Format

When a failure pattern is detected, include in the report:

```
- **[Pattern name]** — [one-sentence explanation of what was observed]
  Severity: [low / medium / high]
```

List all detected patterns. If no patterns are detected for a category, state: "No failure patterns detected."
