---
name: gtm-model-fit-profiler
description: Evaluates whether an AI model is well-suited for a specific GTM workload — market research, pricing/competitor analysis, or outreach personalization. Supports single-model task-fit reports and head-to-head comparisons. Scores on shared criteria (instruction following, specificity, groundedness, structure, confidence discipline, actionability) plus workload-specific criteria. Detects failure patterns (hallucination, generic filler, fake personalization, invented pricing). Use when asked to evaluate a model for GTM work, compare models for outreach, test a model for pricing analysis, assess model fit for market research, or profile a model against a GTM workload.
author: ajaycodesitbetter
version: 1.0.0
---

# GTM Model Fit Profiler

This is a **meta-skill**. Unlike most OpenDirectory skills that perform GTM work directly, this skill helps you choose the right model *before* you perform GTM work.

Evaluate whether a model is well-suited for a specific GTM workload. Score it. Find its failure modes. Recommend whether to deploy.

Use this skill before wiring a model into `linkedin-job-post-to-buyer-pain-map`, `outreach-sequence-builder`, `pricing-page-psychology-audit`, or any other GTM task skill.

---

**North star:** We are not ranking models globally. We are mapping models to GTM work.

**Critical rule:** Never claim a model is "best overall." Always evaluate in the context of a specific workload. Every score must have a one-sentence explanation. Every failure pattern must cite what was observed. Do NOT confuse model rank with model fit. Do NOT over-trust LLM-as-judge scores; explain your reasoning. Always flag input/data quality issues separately from model issues.

**Style rule:** Write like a GTM analyst, not a hype marketer. Use clear language, direct judgment, explicit trade-offs, and operational recommendations. Avoid vague praise, generic AI excitement, benchmark-style bragging, and unsupported claims.

**Language rule:** Use GTM-native language throughout. Never use ML benchmarking jargon such as perplexity, BLEU score, token efficiency, F1, MMLU, or ELO. Speak in terms of GTM fitness, not academic model metrics.

---

## Step 1: Setup Check

Confirm required env vars:

Verify that the LLM evaluator is properly configured in your agent runtime.

**If the LLM evaluator is not configured:**
Stop. Tell the user: "A configured LLM evaluator is required. Please check your agent's configuration."

---

## Step 2: Collect Inputs

Collect these inputs before proceeding.

### 2a: Model(s)

- `model_a` (required): The model to evaluate. Example: "Model X", "GPT-4o", "Claude Opus"
- `model_b` (optional): A second model for comparison mode

**If the user already named the model(s) in their prompt:** Extract them. Confirm: "Model A captured: [name]." and if applicable, "Model B captured: [name]. Running in comparison mode."

**If no model is specified:** Ask: "Which model do you want to evaluate? Optionally name a second model for a head-to-head comparison."

### 2b: Workload

- `workload` (required): One of `market_research`, `pricing_analysis`, or `outreach`

**If the user already specified the workload:** Extract it. Confirm: "Workload: [workload]."

**If the workload does not match one of the 3 supported types:** Stop. Say: "This workload is not supported. Supported workloads are: (1) market_research, (2) pricing_analysis, (3) outreach. Please select one of these."

**If no workload is specified:** Ask: "Which GTM workload are you evaluating for? Options: market_research, pricing_analysis, or outreach."

### 2c: Business Context (optional)

Examples: "B2B SaaS for DevOps teams", "PLG infra product targeting engineering managers", "AI SDR workflow for mid-market security companies"

**If provided:** Capture it. Confirm: "Business context: [summary]."
**If missing:** Continue with a neutral GTM context. Note: "No business context provided. Evaluating against neutral GTM defaults."

### 2d: Source Material (optional)

Examples: pricing page text, LinkedIn job post, Reddit thread, support tickets, competitor notes, ICP notes.

**If provided:** Capture it. Confirm: "Source material captured: [brief description]."
**If missing:** Note: "No source material provided. Using default benchmark prompts for this workload."

---

## Step 3: Route Workload

Based on the captured `workload`, load the correct evaluation context.

### If workload = market_research

Read `references/workload-prompts.md` — Market Research section.

Use evaluation tasks like:
- Extract top pain points from source material
- Cluster repeated market signals into GTM-relevant themes
- Map signals to ICP segments
- Summarize strategic implications

### If workload = pricing_analysis

Read `references/workload-prompts.md` — Pricing / Competitor Analysis section.

Use evaluation tasks like:
- Compare pricing pages and explain strategy differences
- Infer packaging strategy from tier structure
- Analyze trade-offs of a pricing move
- Recommend competitive response with reasoning

### If workload = outreach

Read `references/workload-prompts.md` — Outreach Personalization section.

Use evaluation tasks like:
- Write a short cold email from a buying signal
- Personalize an opener using account context
- Turn a public signal into helpful outreach
- Create a multi-signal email under word limit

**If source_material is provided:** Use it as the evaluation input, replacing or supplementing the default prompts.
**If source_material is missing:** Use the default benchmark prompts from `references/workload-prompts.md`.

---

## Step 4: Evaluate Model(s)

For each model being evaluated, build the LLM request to simulate the model's behavior on the workload tasks and then score the output.

Use your agent's configured LLM integration (this skill uses your agent's configured LLM as the evaluator) to simulate what the named model would produce for each task, then score the output using the rubric.

Instruct the LLM evaluator using this system prompt logic:
"You are a GTM model-fit evaluator. You will be given: (1) a model name, (2) a GTM workload type, (3) evaluation tasks for that workload, and (4) optionally, business context and source material. Your job is to simulate what the named model would produce for each task, then score the output using the provided rubric. Rules: (A) Be honest and specific in your scoring — do not inflate scores. (B) Every score must include a one-sentence explanation. (C) Identify failure patterns with severity ratings. (D) Separate 'looks polished' from 'is actually useful.' (E) Penalize confident nonsense and generic GTM filler. (F) Reward structured, operator-usable outputs. (G) Do NOT over-trust LLM-as-judge scores; explain your reasoning. (H) Flag input/data quality issues separately from model issues. (I) Output valid JSON only."

Replace `EVALUATION_CONTEXT_HERE` with:
- The model name (model_a, and model_b if in comparison mode)
- The workload type
- The evaluation tasks from Step 3
- Business context and source material if provided
- The full scoring rubric from `references/scoring-rubric.md`
- Instructions to output JSON with scores and explanations per criterion

**In comparison mode:** Run the evaluation for both models. Use the same tasks and rubric. Score each model independently — never score relative to the other.

---

## Step 5: Score

Read `references/scoring-rubric.md` for the full scoring model.

Score each model on the 6 shared criteria (60% weight) and the 5 workload-specific criteria (40% weight). 
Explicitly read `references/scoring-rubric.md` to see the exact criteria lists and definitions.

### Calculate

```
shared_subtotal = mean of 6 shared scores
workload_subtotal = mean of 5 workload scores
overall_task_fit = (0.6 × shared_subtotal) + (0.4 × workload_subtotal)
```

Read `references/scoring-rubric.md` for the Task-Fit Interpretation labels.

**Deployment Guidance Logic:**
Compute separately from task-fit score. See `references/scoring-rubric.md` for full decision rules.
- Labels: `external-safe` | `human-reviewed` | `internal-only` | `not recommended`
- High-severity failures cap guidance at `internal-only` regardless of score.
- Weak input data prevents `external-safe`.
- Must include a 1-2 sentence justification.

---

## Step 6: Detect Failure Patterns

Read `references/failure-patterns.md` for the full catalog.

After scoring, scan every model output for failure patterns.

Explicitly read `references/failure-patterns.md` to see the lists of universal and workload-specific failure patterns. Scan the model output for all relevant patterns.

For each failure detected, record:
- Pattern name
- Short explanation of what was observed
- Severity: low / medium / high

**If failure severity is "high":** Cap the deployment guidance at "internal-only" maximum, regardless of the task-fit score.

---

## Step 7: Recommend

Read `references/examples.md` to calibrate your recommendation quality.

### Single-model mode

If only model_a was evaluated, produce:
- **Input/data quality** — separate flag for source material issues (if any)
- **Overall task-fit score** — the calculated number with interpretation label
- **Best for** — what GTM jobs this model handles well
- **Weak at** — where it underperforms
- **Avoid for** — where it should not be used
- **Main risk** — the single biggest operational risk
- **Deployment guidance** — external-safe / human-reviewed / internal-only / not recommended (with a 1-2 sentence justification based on score, failures, data quality, and workload sensitivity)

### Comparison mode

If both model_a and model_b were evaluated, produce:
- **Winner for this workload** — which model and why
- **Why it won** — specific evidence, not generic praise
- **Where the loser still performs better** — honest trade-off
- **Choose A if...** — specific use case where A is better
- **Choose B if...** — specific use case where B is better
- **Operational caution notes** — what to watch for with the winner

Never recommend a model only because it sounds polished. Always explain the trade-off.

---

## Step 8: Self-QA

Run every check and fix violations before presenting:

- [ ] All scores use 1-5 scale with one-sentence explanations
- [ ] Shared subtotal and workload subtotal calculated separately before overall score
- [ ] Overall score formula: `(0.6 × shared_subtotal) + (0.4 × workload_subtotal)` correctly applied
- [ ] Score interpretation label matches the range table
- [ ] If any single criterion scored 1, it is flagged as a critical weakness
- [ ] If any failure pattern severity is "high", deployment guidance is capped at "internal-only"
- [ ] Failure patterns include pattern name, explanation, and severity
- [ ] In comparison mode, both models scored independently (not relative to each other)
- [ ] Output separates task-fit score from deployment guidance
- [ ] Deployment guidance uses allowed labels and includes a clear justification
- [ ] Input/data quality issues are flagged separately from model issues
- [ ] No vague praise, generic AI excitement, or benchmark bragging in the report
- [ ] Confidence note reflects quality and quantity of evidence
- [ ] Workload-specific criteria match the selected workload (not mixed)
- [ ] Unsupported workloads are rejected, not force-fitted

Fix any violation before presenting.

---

## Step 9: Output and Save

### Human-readable output

Present the full report in this format:

Format the output exactly matching the structure shown in `references/examples.md`. 
Ensure you include all required sections: Context, Scorecard, Input/Data Quality, Strengths, Failure Patterns, Recommendation, and Confidence Note.

**For comparison mode**, use side-by-side scorecard columns and the comparison recommendation format exactly as shown in Example 2 of `references/examples.md`.

### Save to file

If your runtime supports file output, attempt to save the report to `docs/model-fit-reports/YYYY-MM-DD-MODEL_SLUG.md`.

Use slugified model name: lowercase, replace spaces and special characters with hyphens.

e.g., "Model X" → `model-x`, "Claude Opus vs GPT-4o" → `claude-opus-vs-gpt-4o`

---

## When to Use

- You want to evaluate whether one model is suitable for a specific GTM task
- You need to compare two candidate models for the same GTM workload
- You want to understand failure patterns before shipping or trusting model outputs
- You need to pick the best model for a workflow with a defensible recommendation
- You want to reduce wasted experimentation and poor model-tool fit

## When NOT to Use

- You want to rank models globally across all tasks (this skill evaluates per-workload only)
- You need to evaluate models for non-GTM work (coding, creative writing, summarization)
- You want live API calls to third-party model endpoints (out of scope for v1)
- You need to evaluate fine-tuned or custom models (this skill profiles general-purpose models)
- You want model cost optimization or dashboarding (not this skill's job)

## Plays Well With

This skill is a **selection layer** — use it before running these GTM skills:

- **linkedin-job-post-to-buyer-pain-map**: Profile model reliability for hiring signal analysis before running pain map generation
- **outreach-sequence-builder**: Assess model fit for outreach personalization before generating sequences
- **pricing-page-psychology-audit**: Evaluate model accuracy for pricing analysis before running audits
- **noise-to-linkedin-carousel**: Test content generation capabilities before carousel creation
