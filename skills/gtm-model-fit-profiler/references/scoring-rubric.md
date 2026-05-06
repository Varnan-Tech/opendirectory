# GTM Model Fit Profiler — Scoring Rubric

This document defines the complete scoring model used to evaluate model fit for GTM workloads.

---

## Scale

All criteria are scored 1–5:

| Score | Label | Definition |
|-------|-------|------------|
| 1 | Very weak | Output fails the criterion almost entirely |
| 2 | Weak | Output partially meets the criterion but has major gaps |
| 3 | Acceptable | Output meets basic expectations but nothing more |
| 4 | Strong | Output clearly meets the criterion with minor issues |
| 5 | Excellent | Output exceeds expectations with no meaningful gaps |

---

## Shared Criteria (60% weight)

These apply to every evaluation regardless of workload.

### Instruction following
Did the model follow the requested format, task boundaries, and constraints?

Scoring guide:
- 5: Every instruction followed precisely, format correct, constraints respected
- 4: Minor format deviation but all constraints met
- 3: Some instructions missed or partially followed
- 2: Multiple instructions ignored, output drifts from request
- 1: Output largely ignores the prompt structure

### Specificity
Did the model provide concrete details and useful observations instead of generic filler?

Scoring guide:
- 5: Every claim is specific, named, and grounded in detail
- 4: Mostly specific with occasional generic statements
- 3: Mix of specific and generic content
- 2: Mostly generic with occasional specifics
- 1: Entirely generic, could apply to any context

### Groundedness
Did the model stay tied to the input material instead of inventing unsupported claims?

Scoring guide:
- 5: Every claim traceable to input, no fabrication
- 4: Nearly all claims grounded, one minor unsupported statement
- 3: Some claims grounded, some unsupported but plausible
- 2: Multiple fabricated or unsupported claims
- 1: Output largely invented or disconnected from input

### Structure
Was the output organized and easy for a GTM operator to use immediately?

Scoring guide:
- 5: Clear sections, logical flow, immediately usable
- 4: Well organized with minor navigation issues
- 3: Adequate structure but requires some reorganization to use
- 2: Poorly organized, hard to extract key information
- 1: Unstructured wall of text

### Confidence discipline
Did the model express uncertainty appropriately when evidence was limited?

Scoring guide:
- 5: Explicitly flags uncertainty, hedges proportional to evidence
- 4: Mostly appropriate confidence, one minor overstatement
- 3: Generally confident but occasionally overstates
- 2: Frequently overstates conclusions with weak evidence
- 1: Presents speculation as fact throughout

### Actionability
Could a GTM user take action from the output without heavy rewriting?

Scoring guide:
- 5: Output is directly usable as-is in a GTM workflow
- 4: Usable with minor edits or additions
- 3: Provides direction but needs significant rework
- 2: Gives ideas but not in actionable form
- 1: No actionable content

---

## Market Research Criteria (40% weight)

Use these additional criteria when workload = market_research.

### Signal extraction
Can the model identify real pains, themes, and repeated market signals?

Scoring guide:
- 5: Identifies non-obvious signals with clear market relevance
- 4: Catches most key signals, misses one minor theme
- 3: Catches obvious signals only
- 2: Misses important signals, catches superficial ones
- 1: Fails to identify meaningful signals

### Clustering quality
Does it group findings into sensible GTM buckets?

Scoring guide:
- 5: Clusters are mutually exclusive, collectively exhaustive, strategically useful
- 4: Clusters are logical with minor overlap
- 3: Clusters exist but are somewhat arbitrary
- 2: Clusters are unclear or heavily overlapping
- 1: No meaningful clustering

### ICP relevance
Does it connect the findings to the right buyer type or segment?

Scoring guide:
- 5: Findings mapped precisely to buyer segments with reasoning
- 4: Good ICP mapping with minor segment confusion
- 3: Generic buyer references without clear segmentation
- 2: Weak or incorrect buyer mapping
- 1: No ICP connection

### Insight depth
Does it go beyond summary into useful GTM insight?

Scoring guide:
- 5: Surfaces non-obvious implications and strategic recommendations
- 4: Provides useful insights beyond basic summary
- 3: Summarizes well but stays surface-level
- 2: Mostly restates input without insight
- 1: No insight beyond raw data

### Evidence discipline
Does it avoid overgeneralizing from limited evidence?

Scoring guide:
- 5: Claims scaled precisely to evidence strength
- 4: Mostly disciplined with one minor overgeneralization
- 3: Occasionally overgeneralizes but acknowledges limitations
- 2: Frequently overgeneralizes
- 1: Draws sweeping conclusions from thin evidence

---

## Pricing / Competitor Analysis Criteria (40% weight)

Use these additional criteria when workload = pricing_analysis.

### Comparative accuracy
Does the model compare plans, pricing, and features correctly?

Scoring guide:
- 5: All comparisons factually accurate, no invented details
- 4: Mostly accurate with one minor error
- 3: Generally correct but some imprecise comparisons
- 2: Multiple inaccuracies in comparison
- 1: Comparisons are largely incorrect or fabricated

### Packaging reasoning
Can it explain why the competitor structured pricing that way?

Scoring guide:
- 5: Provides strategic reasoning grounded in market dynamics
- 4: Good reasoning with minor gaps
- 3: Basic reasoning without strategic depth
- 2: Shallow or speculative reasoning
- 1: No reasoning attempted or entirely speculative

### Positioning insight
Can it infer the market strategy behind packaging or pricing choices?

Scoring guide:
- 5: Identifies non-obvious strategic intent with supporting logic
- 4: Good strategic inference with minor gaps
- 3: Surface-level positioning observations
- 2: Vague or generic positioning statements
- 1: No positioning insight

### Trade-off reasoning
Can it explain what a move improves, what it harms, and who it affects?

Scoring guide:
- 5: Clear multi-dimensional trade-off analysis with stakeholder impact
- 4: Good trade-off reasoning with one dimension missing
- 3: Acknowledges trade-offs but doesn't fully analyze them
- 2: One-sided analysis ignoring trade-offs
- 1: No trade-off awareness

### Recommendation quality
Are the recommended actions realistic, specific, and strategically coherent?

Scoring guide:
- 5: Recommendations are specific, actionable, and strategically sound
- 4: Good recommendations with minor feasibility gaps
- 3: Generic recommendations that could apply to any company
- 2: Vague or unrealistic recommendations
- 1: No useful recommendations

---

## Outreach Personalization Criteria (40% weight)

Use these additional criteria when workload = outreach.

### Personalization relevance
Does the message truly use the account/context signal?

Scoring guide:
- 5: Personalization is specific, relevant, and demonstrates real research
- 4: Good personalization with one generic element
- 3: Surface-level personalization (company name only)
- 2: Fake personalization — mentions context but doesn't use it
- 1: No personalization, fully generic

### Message sharpness
Is the message concise and clear without padding?

Scoring guide:
- 5: Every sentence earns its place, no filler
- 4: Mostly sharp with one unnecessary sentence
- 3: Some padding but core message is clear
- 2: Significant padding dilutes the message
- 1: Bloated, unclear, or rambling

### Non-generic tone
Does it avoid boilerplate AI outreach language?

Scoring guide:
- 5: Sounds like a human who did their homework
- 4: Mostly natural with one AI-sounding phrase
- 3: Mix of natural and templated language
- 2: Mostly boilerplate with occasional human touches
- 1: Obvious AI-generated template

### Hook quality
Does the opener create genuine reason to keep reading?

Scoring guide:
- 5: Hook is specific, relevant, and creates genuine curiosity
- 4: Good hook with minor generic element
- 3: Adequate opener but not compelling
- 2: Generic opener that could be anyone
- 1: No hook or immediately signals spam

### CTA quality
Is the ask natural, low-friction, and context-appropriate?

Scoring guide:
- 5: CTA is specific, low-pressure, and naturally follows the message
- 4: Good CTA with minor awkwardness
- 3: Generic CTA (e.g., "would love to chat")
- 2: Pushy or mismatched CTA
- 1: No CTA or aggressive sales ask

---

## Score Calculation

### Formula

```
shared_subtotal = mean(instruction_following, specificity, groundedness, structure, confidence_discipline, actionability)
workload_subtotal = mean(workload_criterion_1, ..., workload_criterion_5)
overall_task_fit = (0.6 × shared_subtotal) + (0.4 × workload_subtotal)
```

### Task-Fit Interpretation

| Range | Label | Meaning |
|-------|-------|---------|
| 4.5–5.0 | Excellent fit | Highly capable for this specific workload |
| 3.8–4.4 | Strong fit | Reliable but may need minor corrections |
| 3.0–3.7 | Usable with review | Requires human-in-the-loop validation |
| 2.0–2.9 | Weak fit | Struggles significantly with this workload |
| Below 2.0 | Poor fit | Fails at core workload tasks |

### Scoring Rules

1. Always calculate and display both subtotals before the overall score.
2. If any single criterion scores 1, flag it as a critical weakness regardless of overall score.
3. Do not round intermediate scores for internal calculations. Subtotals may be displayed rounded to 1 decimal for readability in the scorecard, but calculate the overall score using full precision before rounding.
4. In comparison mode, calculate scores independently — never score relative to the other model.

---

## Deployment Guidance Logic

Deployment guidance must be computed separately from the task-fit score. A model with a high average score can still be unsafe for external use if it has one high-severity hallucination or weak evidence discipline.

**Labels:** `external-safe` | `human-reviewed` | `internal-only` | `not recommended`

### Decision Rules

1. **Failure Severity Caps:** Any high-severity hallucination, invented pricing detail, or fake personalization caps the deployment guidance at `internal-only` or worse, regardless of the overall score.
2. **Input/Data Quality:** Weak or incomplete source material prevents an `external-safe` recommendation. Input data issues must be flagged separately from model issues.
3. **Workload Sensitivity:** Outreach and pricing analysis require stricter caution than internal market synthesis.
4. **External-Safe is Rare:** `external-safe` should be rare and must be explicitly justified by high scores, zero high-severity failures, and strong input quality.
5. **Justification Required:** Every deployment guidance label must include a 1-2 sentence justification explaining why it was assigned, citing score, failures, data quality, and workload.
