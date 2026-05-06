# GTM Model Fit Profiler — Calibration Examples

These examples show the expected output quality and depth for each evaluation mode.

---

## Example 1: Single-Model Market Research Report

### GTM Model Fit Report — Gemini 2.0 Flash

#### Context
- **Workload tested:** Market research
- **Business context:** B2B SaaS DevOps platform targeting engineering managers at Series B+ companies
- **Source material:** 5 customer support tickets about CI/CD pain points

#### Scorecard

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Shared Criteria** | | |
| Instruction following | 4 | Followed format, missed one clustering constraint |
| Specificity | 5 | Named specific tools, roles, and pain language |
| Groundedness | 4 | All claims tied to tickets except one generalization about market trends |
| Structure | 5 | Clear sections, scannable, immediately usable |
| Confidence discipline | 4 | Appropriately hedged most claims, one "clearly shows" overstatement |
| Actionability | 4 | Recommendations usable with minor GTM context additions |
| **Shared subtotal** | **4.3** | |
| **Market Research Criteria** | | |
| Signal extraction | 5 | Identified non-obvious permission pain as enterprise blocker |
| Clustering quality | 4 | 4 clusters, slight overlap between "integration" and "reliability" |
| ICP relevance | 3 | Mapped to "engineering teams" broadly, didn't segment by company stage |
| Insight depth | 4 | Connected template gap to onboarding cost, useful for positioning |
| Evidence discipline | 4 | Scaled claims to ticket volume, one minor overgeneralization |
| **Workload subtotal** | **4.0** | |

**Overall task-fit score:** (0.6 × 4.3) + (0.4 × 4.0) = **4.2 — Strong fit**

#### Input/Data Quality
- **Source material:** 5 customer support tickets. Good volume, but lacks direct competitive context which limited the model's ability to do deep ICP segmentation. No critical data issues.

#### Strengths
- Extracted specific pain language verbatim from tickets
- Connected permission model limitation to enterprise deal risk
- Identified the "template library" gap as an onboarding cost multiplier
- Output was structured for immediate use in a positioning doc

#### Failure Patterns
- **Generic filler language** — One paragraph about "the growing importance of DevOps" added no value. Severity: low
- **Shallow clustering** — "Integration reliability" and "platform reliability" clusters overlap significantly. Severity: medium
- No other failure patterns detected.

#### Recommendation
- **Best for:** Internal market synthesis from qualitative data (tickets, reviews, forum posts)
- **Weak at:** ICP segmentation — tends to map to broad roles instead of buyer segments
- **Avoid for:** Customer-facing market reports where the generic filler would undermine credibility
- **Main risk:** May overgeneralize from small sample sizes without sufficient hedging
- **Deployment guidance:** **human-reviewed**. While the task-fit score is strong (4.2), the model tends to overgeneralize ICP segments and requires human sign-off before these insights are used to shape outbound strategy.

#### Confidence Note
Medium confidence. Based on a single workload evaluation with provided source material. Would increase to high confidence with 2-3 additional source material tests.

---

## Example 2: Comparison Mode — Outreach

### GTM Model Fit Report — Model A vs Model B

#### Context
- **Workload tested:** Outreach personalization
- **Business context:** API monitoring tool for engineering teams
- **Source material:** Job post for Senior SRE role at StreamData (Series B)

#### Scorecard

| Criterion | Model A | Model B |
|-----------|---------|---------|
| **Shared Criteria** | | |
| Instruction following | 4 | 5 |
| Specificity | 3 | 5 |
| Groundedness | 4 | 4 |
| Structure | 4 | 5 |
| Confidence discipline | 4 | 4 |
| Actionability | 3 | 5 |
| **Shared subtotal** | **3.7** | **4.7** |
| **Outreach Criteria** | | |
| Personalization relevance | 2 | 5 |
| Message sharpness | 3 | 4 |
| Non-generic tone | 2 | 4 |
| Hook quality | 3 | 5 |
| CTA quality | 3 | 4 |
| **Workload subtotal** | **2.6** | **4.4** |

**Model A task-fit:** (0.6 × 3.7) + (0.4 × 2.6) = **3.3 — Usable with review**
**Model B task-fit:** (0.6 × 4.7) + (0.4 × 4.4) = **4.6 — Excellent fit**

#### Input/Data Quality
- **Source material:** Single job post for Senior SRE. Clear signal, but lacks broader account context (e.g., recent news or tech stack data). Sufficient for this specific test.

#### Model A Failure Patterns
- **Fake personalization** — Mentioned "StreamData" but the email body was interchangeable with any SaaS company. Severity: high
- **Templated opener** — Used "I noticed that your company is expanding its SRE team." Severity: medium
- **Overlong copy** — 180 words for a cold email. Severity: low

#### Model B Failure Patterns
- **No critical failure patterns detected.**
- Minor: One sentence could be tightened. Severity: low

#### Recommendation

**Winner for this workload:** Model B

**Why it won:** Model B used the specific SRE job requirements (distributed tracing, API observability) to craft a relevant opener. The personalization was real — removing "StreamData" from the email would break the message because it referenced their specific hiring needs.

**Where Model A still performs better:** Model A produced a more detailed follow-up sequence structure. For multi-touch campaigns where the first email is human-written and follow-ups are automated, Model A's sequence logic is stronger.

- **Choose Model A if:** You need sequence logic and will rewrite the individual emails yourself
- **Choose Model B if:** You need send-ready first-touch emails with real personalization

**Deployment guidance:**
- **Model A:** **internal-only**. The high-severity fake personalization failure caps this at internal-only, despite a usable task-fit score (3.3).
- **Model B:** **external-safe**. Achieved an excellent task-fit score (4.6) with zero high-severity failures and produced highly relevant copy grounded strictly in the provided job post.

**Operational caution:** Even for external-safe models, the first batch of emails should always be reviewed for tone match with your brand voice.

---

## Example 3: Low-Fit Result

### GTM Model Fit Report — Model C

#### Context
- **Workload tested:** Pricing / competitor analysis
- **Business context:** B2B data pipeline tool, $500/mo team plan
- **Source material:** Competitor pricing page with 4 tiers

#### Scorecard

| Criterion | Score | Notes |
|-----------|-------|-------|
| **Shared Criteria** | | |
| Instruction following | 3 | Followed format but drifted into unsolicited product advice |
| Specificity | 2 | Mostly generic observations about SaaS pricing |
| Groundedness | 1 | Invented competitor features not on the pricing page |
| Structure | 3 | Adequate sections but disorganized within sections |
| Confidence discipline | 1 | Stated fabricated pricing details with full confidence |
| Actionability | 2 | Recommendations too vague to act on |
| **Shared subtotal** | **2.0** | |
| **Pricing Criteria** | | |
| Comparative accuracy | 1 | Invented a "Growth tier" the competitor doesn't have |
| Packaging reasoning | 2 | Surface-level "they want to attract more users" |
| Positioning insight | 2 | No strategic interpretation of pricing moves |
| Trade-off reasoning | 2 | One-sided "you should lower your price" with no downsides |
| Recommendation quality | 1 | "Consider a freemium model" with no supporting analysis |
| **Workload subtotal** | **1.6** | |

**Overall task-fit score:** (0.6 × 2.0) + (0.4 × 1.6) = **1.8 — Poor fit**

#### Input/Data Quality
- **Source material:** Competitor pricing page with 4 tiers. Clear, structured, and factual input; the hallucination failure patterns are entirely model-driven, not data-driven.

#### Failure Patterns
- **Invented pricing details** — Fabricated a "Growth tier at $39/mo" not present in source material. Severity: high
- **Unsupported certainty** — "This pricing structure clearly shows they are pivoting to enterprise." No evidence. Severity: high
- **Weak pricing recommendation logic** — Recommended price cuts without analyzing margin impact. Severity: medium
- **Context drift** — Spent a paragraph advising on product features unrelated to pricing. Severity: medium

#### Recommendation
- **Best for:** Nothing in this workload. The hallucination rate makes it unsafe.
- **Weak at:** Comparative accuracy and evidence-based reasoning
- **Avoid for:** Any pricing or competitive analysis where factual accuracy matters
- **Main risk:** Will confidently present fabricated pricing details as fact
- **Deployment guidance:** **not recommended**. The task-fit score is poor (1.8), and the high-severity hallucination of pricing details makes this model unsafe for any competitive analysis workload.

#### Confidence Note
High confidence in this negative recommendation. The hallucination pattern was consistent across multiple sections and represents a fundamental reliability issue for this workload.
