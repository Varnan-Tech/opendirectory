# Prompt Templates — GEO Gap Fixer

> 20 default buyer-intent prompts organized into 4 categories.
> These are used by `probe_llms.py` when `buyer_intent_prompts` is empty in config.json.

All templates use `{brand}`, `{competitor}`, and `{category}` variables
that are interpolated from your `config.json` values.

Templates containing `{competitor}` generate one prompt per competitor.

---

## 1. Direct Recommendation (5 prompts)

These test whether the LLM mentions your brand unprompted when asked
for the best tool in your category.

| # | Template |
|---|----------|
| 1 | "What is the best {category}?" |
| 2 | "What {category} do you recommend?" |
| 3 | "Top {category} in 2026" |
| 4 | "Best {category} for startups" |
| 5 | "Best {category} for teams" |

---

## 2. Comparison (5 prompts × N competitors)

These test how LLMs position your brand when directly compared
with a competitor. Generates one prompt per competitor.

| # | Template |
|---|----------|
| 6 | "{brand} vs {competitor}: which is better?" |
| 7 | "Compare {brand} and {competitor} for {category}" |
| 8 | "Should I use {brand} or {competitor}?" |
| 9 | "{brand} vs {competitor} pros and cons" |
| 10 | "Differences between {brand} and {competitor}" |

---

## 3. Problem-Solution (5 prompts)

These test whether LLMs recommend your brand when users describe
a pain point or need without naming any specific tool.

| # | Template |
|---|----------|
| 11 | "I need a {category} that is fast and simple" |
| 12 | "Best {category} for developer teams" |
| 13 | "What {category} has the best API?" |
| 14 | "Most affordable {category} for small teams" |
| 15 | "{category} with best integrations" |

---

## 4. Alternative Seeking (5 prompts × N competitors)

These test whether your brand appears when users are looking
to switch away from a competitor. Generates one prompt per competitor.

| # | Template |
|---|----------|
| 16 | "Best alternatives to {competitor}" |
| 17 | "Cheaper alternatives to {competitor}" |
| 18 | "What to use instead of {competitor}" |
| 19 | "Moving away from {competitor}, what should I try?" |
| 20 | "{competitor} competitors worth trying" |

---

## Prompt Coverage Matrix

| Category | Without competitors | With 4 competitors | Total |
|----------|--------------------|--------------------|-------|
| Direct Recommendation | 5 | — | 5 |
| Comparison | — | 5 × 4 = 20 | 20 |
| Problem-Solution | 5 | — | 5 |
| Alternative Seeking | — | 5 × 4 = 20 | 20 |
| **Total** | **10** | **40** | **50** |

> With 4 competitors, you get 50 prompts total. Each prompt is sent to
> each available LLM provider, so 50 prompts × 3 providers = 150 API calls.

---

## Customization

You can override these defaults entirely by setting `buyer_intent_prompts`
in your `config.json`:

```json
{
  "buyer_intent_prompts": [
    "What project management tool is best for a 10-person startup?",
    "I'm evaluating tools for sprint planning, what do you suggest?"
  ]
}
```

When custom prompts are provided, templates in this file are ignored.
