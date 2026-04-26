# Scoring Rubric

This file defines the scoring model used by the linkedin-job-post-to-buyer-pain-map skill. The agent reads this file during Step 4 to evaluate each account.

---

## Three Scoring Dimensions

### Signal Strength (1–10)

Measures how many and how specific the hiring signals are that relate to the user's product area.

**Scoring rules:**

| Condition | Modifier |
|-----------|----------|
| Multiple related hires on the same team or problem area | +3 |
| Explicit language about a pain area the user's product addresses | +2 |
| Senior role (Head / Director / VP) in a relevant function | +1 |
| Role responsibilities reference building, replacing, or fixing a system in the product's category | +1 |
| "First X hire" or "0→1" language indicating new team formation | +1 |
| Generic "nice-to-have" requirements with no clear pain signal | −1 |
| Job post is mostly a list of perks and culture statements with minimal responsibilities | −2 |

**Floor:** 1. **Ceiling:** 10. Clamp after summing.

**Base:** Start at 3 for any post that mentions a function relevant to the user's ICP.

---

### Urgency (1–10)

Measures how time-sensitive the hiring need appears from the text.

**Scoring rules:**

| Condition | Modifier |
|-----------|----------|
| Explicit urgency language: "immediate", "ASAP", "critical hire", "backfill" | +3 |
| Multiple open roles in the same function at the same company | +2 |
| Language suggesting firefighting: "stabilize", "fix", "unblock", "reduce downtime" | +2 |
| Role described as replacement for a departing leader | +1 |
| "Nice to have" tone, exploratory language ("we're thinking about...") | −2 |
| No urgency indicators at all | −1 |

**Floor:** 1. **Ceiling:** 10. Clamp after summing.

**Base:** Start at 4 for any role at IC-Senior or higher that has a defined scope.

---

### ICP Fit (1–10)

Measures how closely the company profile in the job post matches the user's `icp_description`.

**Scoring rules:**

| Condition | Modifier |
|-----------|----------|
| Industry matches ICP exactly | +3 |
| Company size indicators match (headcount, "Series X", "enterprise") | +2 |
| Tech stack or tool references overlap with ICP tech stack | +2 |
| Role function matches ICP target persona function | +1 |
| Industry is adjacent but not exact match | +1 |
| Industry is clearly outside ICP (e.g., government when ICP is B2B SaaS) | −3 |
| Company size indicators suggest a segment the user does not serve | −2 |

**Floor:** 1. **Ceiling:** 10. Clamp after summing.

**Base:** Start at 3 for any post where industry cannot be determined.

---

## Overall Score (10–100)

```
overall = round((0.4 × signal_strength + 0.3 × urgency + 0.3 × icp_fit) × 10)
```

Each dimension is 1–10, so the raw weighted sum ranges from 1.0 to 10.0. Multiply by 10 to get 10–100 scale.

**Interpretation guide:**

| Range | Label | Recommendation |
|-------|-------|---------------|
| 80–100 | Strong signal | Prioritize immediately. Build pain map and outreach angles. |
| 60–79 | Moderate signal | Worth analyzing. Pain map likely has actionable pains. |
| 40–59 | Weak signal | Low priority. Limited pain signal. |
| 1–39 | Noise | Skip or deprioritize. Post is too generic or outside ICP. |

---

## Buy-vs-Build Inference

The skill infers the company's likely posture toward buying vs building based on language patterns in the job description.

| Language Pattern | Inferred Posture |
|-----------------|-----------------|
| "Build from scratch", "0→1", "greenfield", "design and implement new" | **Leaning build** |
| "Evaluate and implement", "select vendor", "integrate third-party" | **Leaning buy** |
| "Replace legacy", "migrate from", "modernize" | **Leaning buy** (replacing existing) |
| "Own end-to-end", "build and maintain" + "integrate tools" | **Hybrid (buy-and-build)** |
| "Scale existing", "optimize current" | **Hybrid** — already built, may buy to augment |
| No clear signals | **Unknown** — do not guess |

Output as a text label, not a numeric score.

---

## Stage Guess

Inferred from company context clues in the job description.

| Clue | Stage Guess |
|------|------------|
| "Series A", "seed", "early stage", &lt; 50 employees | Pre-PMF or Early |
| "Series B/C", "scaling", "hypergrowth", 50–500 employees | Scaling post-PMF |
| "Enterprise", "Fortune 500", "publicly traded", &gt; 500 employees | Mature / Enterprise |
| "First [role] hire", "founding team" | Very early |
| No clues available | "Unknown" |
