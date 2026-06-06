# Scoring Rubric — GEO Gap Fixer

> How `analyze_results.py` scores brand visibility across LLM responses.

---

## Metrics Overview

| # | Metric | Range | What It Measures |
|---|--------|-------|-----------------|
| 1 | Mention Rate | 0–100% | How often the brand appears in LLM responses |
| 2 | Average Rank | 1.0–3.0+ | Where the brand is positioned when mentioned |
| 3 | Sentiment Score | -1.0 to +1.0 | How positively/negatively the brand is framed |
| 4 | Citation Score | 0–100% | How often the brand's domain is cited vs competitors |
| 5 | Win Rate | 0–100% | How often the brand is mentioned first (ranked #1) |

---

## 1. Mention Rate

**Formula**: `(responses with brand mention / total responses) × 100`

| Range | Interpretation |
|-------|---------------|
| 80–100% | Excellent — LLMs consistently recommend you |
| 50–79% | Good — present but not dominant |
| 20–49% | Weak — significant gaps in visibility |
| 0–19% | Critical — LLMs rarely mention you |

**Detection method**: Case-insensitive word-boundary match (`\b{brand}\b`).
This prevents false positives like "linear" matching "linear algebra".

---

## 2. Average Rank

**Formula**: Mean position across responses where brand IS mentioned.

| Rank | Meaning |
|------|---------|
| 1.0 | Always mentioned first — you're the top recommendation |
| 1.5–2.0 | Usually in top 2 — strong but not dominant |
| 2.0–3.0 | Mid-pack — often mentioned after competitors |
| 3.0+ | Afterthought — rarely the primary recommendation |

**Calculation**: First occurrence position compared to all tracked names.
If brand appears before all competitors → rank 1.
If one competitor appears before brand → rank 2. And so on.

---

## 3. Sentiment Score

**Formula**: `(positive_keywords − negative_keywords) / total_keywords`

Scored within ±200 characters of each brand mention (proximity-based).

### Positive Keywords (weight: +1 each)
`best`, `recommend`, `excellent`, `leading`, `top`, `popular`,
`powerful`, `intuitive`, `fast`, `modern`, `innovative`, `reliable`,
`robust`, `preferred`, `standout`, `impressive`, `superior`,
`seamless`, `elegant`, `efficient`

### Negative Keywords (weight: -1 each)
`limited`, `lacks`, `however`, `downside`, `expensive`, `complex`,
`steep learning curve`, `missing`, `outdated`, `slow`, `clunky`,
`basic`, `restrictive`, `difficult`, `confusing`, `poor`,
`frustrating`, `buggy`, `unreliable`, `overpriced`

### Labels

| Score | Label |
|-------|-------|
| > 0.2 | Positive |
| -0.2 to 0.2 | Neutral |
| < -0.2 | Negative |

---

## 4. Citation Score

**Formula**: `(brand domain citations / total domain citations) × 100`

| Range | Interpretation |
|-------|---------------|
| 20%+ | Strong — your domain is a trusted source |
| 5–19% | Moderate — some presence but competitors dominate |
| 0–4% | Weak — LLMs rarely cite your domain |

**Detection method**: URL regex extraction from response text,
domain normalization (strip `www.`, lowercase).

---

## 5. Win Rate

**Formula**: `(responses where brand is ranked #1 / total responses) × 100`

| Range | Interpretation |
|-------|---------------|
| 50%+ | Dominant — you're the primary recommendation |
| 25–49% | Competitive — winning roughly half the time |
| 10–24% | Weak — rarely the first recommendation |
| 0–9% | Critical — almost never recommended first |

---

## Overall Health Assessment

The report uses these combined thresholds:

| Mention Rate | Win Rate | Assessment |
|-------------|----------|------------|
| ≥60% | ≥30% | 🟢 Healthy — maintain and optimize |
| 30–59% | 10–29% | 🟡 At Risk — targeted content fixes needed |
| <30% | <10% | 🔴 Critical — major GEO overhaul needed |
