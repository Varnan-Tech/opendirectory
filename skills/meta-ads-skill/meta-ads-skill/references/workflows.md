# Meta Ads Workflows

This document outlines complex orchestrations and workflows for common Meta Ads tasks using the `meta-ads` CLI.

## 1. CPA Spike Troubleshooting

When a client or user asks to investigate a spike in Cost Per Action (CPA), follow this systematic approach:

1. **Account Level Overview**
   - **Command:** `meta ads insights get --level account --time-range last_30d --output json`
   - **Action:** Look at overall account performance over the last 7, 14, and 30 days to identify when the spike started.

2. **Campaign Breakdown**
   - **Command:** `meta ads campaign list --output json`
   - **Command:** `meta ads insights get --level campaign --time-range last_7d --output json`
   - **Action:** Identify which specific campaigns are driving the CPA increase. Compare spend and CPA across active campaigns.

3. **Ad Set Deep Dive**
   - **Command:** `meta ads adset list --campaign-id <ID> --output json`
   - **Command:** `meta ads insights get --level adset --time-range last_7d --output json`
   - **Action:** For the offending campaigns, break down by Ad Set to see if specific audiences or placements are underperforming.

4. **Ad & Creative Analysis**
   - **Command:** `meta ads ad list --adset-id <ID> --output json`
   - **Command:** `meta ads insights get --level ad --time-range last_7d --output json`
   - **Action:** Check if specific ads are experiencing ad fatigue (high frequency, dropping CTR) or if recent changes disrupted the learning phase.

5. **Synthesis and Reporting**
   - Use the `CPA Spike Investigation Report` template (found in `report_templates.md`) to structure the findings and recommendations.

## 2. New Audience Discovery

When a user wants to find new audiences or test new targeting:

1. **Review Current Top Performers**
   - **Command:** `meta ads insights get --level adset --time-range last_30d --output json`
   - **Action:** Identify the ad sets currently delivering the best ROAS/CPA.

2. **Generate Audience Ideas**
   - **Action:** Based on the product and past top performers, generate Lookalike (LAL) audience suggestions or new interest-based targeting.

3. **Structure the Test**
   - Recommend a campaign structure for testing (e.g., A/B testing with Campaign Budget Optimization (CBO) or Ad Set Budget Optimization (ABO)).
   - **Command Example:** `meta ads campaign create --name "Test_Audience_X" --status PAUSED --no-input`

4. **Monitoring**
   - Provide the exact metrics to watch (e.g., CTR, CPC, early conversions) over the next 3-7 days.
