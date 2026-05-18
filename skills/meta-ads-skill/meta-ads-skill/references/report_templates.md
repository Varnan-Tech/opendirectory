# Meta Ads Report Templates

Use these markdown templates when generating reports and summaries for users. These templates are designed to be populated using the structured data from the `meta-ads` CLI's JSON output (`--output json`).

## 1. Executive Summary Template

```markdown
#  Meta Ads Performance Analysis: [Timeframe]

##  Executive Summary
[2-3 sentences summarizing the overall performance. E.g., "Account performance remained stable this week with a 5% increase in ROAS, primarily driven by the new Retargeting campaign. However, top-of-funnel CPA has started to rise."]

##  Key Metrics (Source: `meta ads insights get`)
- **Spend:** $[Amount] ([+/-]% vs previous period)
- **Revenue/Conversions:** [Amount] ([+/-]% vs previous period)
- **CPA:** $[Amount] ([+/-]% vs previous period)
- **ROAS:** [Amount]x ([+/-]% vs previous period)
- **CTR:** [Amount]% ([+/-]% vs previous period)

##  Key Findings
- **Highlight 1:** [E.g., Campaign X is driving 60% of total conversions at a very efficient CPA.]
- **Highlight 2:** [E.g., Ad fatigue is visible in Ad Set Y; frequency has exceeded 4.0 and CTR has dropped by 20%.]
- **Highlight 3:** [E.g., The weekend flash sale was highly successful, accounting for a temporary spike in ROAS.]

##  Recommendations
1. **[Actionable Item 1]:** [E.g., Pause underperforming ads in Ad Set Y and introduce 3 new creative variations.]
2. **[Actionable Item 2]:** [E.g., Scale budget on Campaign X by 20% over the next 3 days.]
3. **[Actionable Item 3]:** [E.g., Launch a new test targeting Lookalike 1% of recent purchasers.]
```

## 2. CPA Spike Investigation Report

```markdown
#  CPA Spike Investigation: [Campaign/Account Name]

##  The Issue
[Briefly state the problem. E.g., "CPA increased from $20 to $35 starting on [Date]."]

##  Root Cause Analysis (Source: `meta ads insights get --level [level]`)
- **Campaign Level:** [Identify which campaign(s) caused the spike.]
- **Ad Set Level:** [Identify specific ad sets. Did a lookalike audience degrade? Did a specific placement get expensive?]
- **Ad Level:** [Identify ad fatigue, drop in CTR, increase in CPM, or decrease in conversion rate.]

##  Action Plan
- [Immediate Action 1]
- [Immediate Action 2]
- [Monitoring Plan]
```
