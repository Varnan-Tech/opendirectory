---
name: win-loss-analyzer
description: "Build and run a structured win/loss analysis program for B2B SaaS and developer-first companies. Use this skill whenever someone asks why deals are being lost, how to run win/loss interviews, what questions to ask buyers after a deal closes, how to stop relying on CRM loss reasons, how to capture competitive intelligence from real buyer conversations, how to set up a win/loss program without a dedicated analyst, or how to route competitive insights to product and sales teams. Covers the full program: CRM bias problem, buyer-direct interview design, driver tagging taxonomy, data capture schema, founder-scale cadence, and insight routing rituals."
compatibility: [claude-code, gemini-cli, github-copilot]
author: Varnan
version: 1.0.0
---

# Win/Loss Analyzer

Your CRM loss reasons are wrong. Sales reps default to "price" as a face-saving explanation. Buyers tell internal stakeholders what is socially acceptable, not what is true. Research across 100,000+ B2B purchase decisions shows CRM-recorded loss reasons diverge from actual buyer reasoning 50-70% of the time. A structured win/loss program with buyer-direct interviews is the only way to surface real drivers.

## When to Use

- You keep losing to the same competitor but don't know why
- Your CRM says "price" for 40%+ of losses
- You want to understand what actually moves buyers to choose you or a competitor
- You need competitive intelligence for product roadmap or sales enablement
- You want to start a win/loss program without a dedicated analyst or RevOps team
- You're a PLG/developer-first company where trial conversion losses don't show up in CRM at all

---

## The CRM vs. Buyer-Direct Gap

**Why CRM loss reasons fail:**

| Who reports | What they say | Why it's wrong |
|---|---|---|
| Sales rep | "Price was too high" | Avoids admitting sales execution failure or product gap |
| Buyer (to internal team) | "We went with the market leader" | Saves face; avoids conflict with stakeholders who lobbied for you |
| Buyer (to third party) | Real answer | No social pressure; nothing to lose |

**For PLG and developer-first companies:** Trial conversion losses are an additional blind spot. A free user who tries your product and never upgrades never creates a CRM opportunity. Your formal win/loss data misses the entire self-serve funnel. You need a separate interview track for high-fit churned trial users.

---

## Step 1: Deal Selection

Pick deals with the most signal. Consistency in selection criteria matters more than volume.

**High-signal deal types:**
- Late-stage losses: prospect evaluated deeply, had a real budget, chose someone else
- Competitive wins: understand why you beat a specific competitor
- Surprise losses: internal team expected to win; buyer chose differently
- Large deals (any size relative to your ACV): enough at stake to get a real conversation

**Filters to apply consistently:**
- Same stage filter every cycle (e.g., "deals that reached demo or proposal")
- Same ACV floor (e.g., "deals over $X")
- Time window: interview within 30-60 days of deal close while recall is fresh
- Exclude: deals lost due to budget freeze or company shutting down (no useful signal)

**Minimum to spot patterns:** 5 interviews per month at founder scale. You need 8-10 interviews sharing the same characteristic (same competitor, same segment, same deal size) before a pattern is reliable.

---

## Step 2: Interview Design

### Opening (broad, narrative)

Let the buyer tell their story. Do not lead. The first 5-10 minutes should be almost entirely the buyer speaking.

**Recommended openers:**
- "What prompted you to start evaluating solutions?"
- "Tell me how this decision started."
- "How did you structure your evaluation process?"
- "Walk me through how you ended up where you did."

These surface context you never would have thought to ask about: internal politics, an incident that triggered the search, a budget cycle, a failed previous solution.

### Core topic areas (probe in whatever order the conversation leads)

Cover all four areas. Sequence follows the buyer's narrative, not a script.

**1. Product and capability**
- What features or capabilities mattered most in your evaluation?
- Were there things you needed that you couldn't find in any of the options?
- What gaps did you find in the products you evaluated?

**2. Sales experience**
- How was the buying process for each vendor?
- Was there anything that made one vendor easier or harder to work with?
- What would you have changed about how any vendor engaged with you?

**3. Pricing and packaging**
- How did pricing factor into your decision?
- Was the pricing model itself a factor, or just the number?
- What would "right-priced" have looked like for your situation?

**4. Competitive and alternative landscape**
- Which other solutions did you seriously evaluate?
- What made you choose the one you did?
- Was there a moment when your thinking shifted?

### Follow-up probes (use throughout)

When a buyer gives a surface answer, go one level deeper:
- "Can you tell me more about that?"
- "What made that important to you specifically?"
- "Was there a moment when your thinking shifted on that?"
- "If that one thing had been different, would the outcome have changed?"

The 5 Whys technique works here: keep asking "why" to move from "price was too high" to "per-seat model doesn't fit our headcount spikes" to "CFO needs predictable fixed costs" — which is an actionable pricing structure insight, not a price objection.

### Interview mechanics

- **Duration:** 30-45 minutes is the right range. Longer loses focus; shorter misses depth.
- **Timing:** Within 30-60 days of deal close. Recall decays fast.
- **Speaking ratio:** Buyer speaks 80-90% of the time. Your job is to probe, not present.
- **Recording:** Ask permission. Record if possible; transcript is more reliable than memory.
- **Who conducts it:** Not the rep who worked the deal. Bias is structural. Founder, PM, or neutral colleague works. Third-party interviewer gets more candid responses but adds cost.

---

## Step 3: Driver Tagging Taxonomy

Tag every interview with 3-5 primary decision drivers. Consistent taxonomy is what converts one-off anecdotes into patterns.

### Standard driver categories

| Category | Sub-driver examples |
|---|---|
| **Pricing** | Total cost, per-seat vs. flat, packaging structure, contract terms, discount offered |
| **Product** | Missing feature, reliability/performance, integrations, UX/ease of use, security/compliance |
| **Sales Experience** | Responsiveness, demo quality, proposal clarity, pushing too hard, champion support |
| **Support and Service** | Onboarding, implementation complexity, support SLA, documentation quality |
| **Competitive** | Existing vendor relationship, brand/reputation, specific competitor feature advantage |
| **Value and Fit** | Timing/urgency mismatch, wrong stage for the product, use case doesn't align |

### Sentiment per driver

After each interview, mark each driver as:
- **Positive**: increased likelihood of winning
- **Negative**: increased likelihood of losing

Patterns emerge by aggregating sentiment across the full interview set. "Product: Missing feature" appearing as a top negative driver in 7 of 10 late-stage losses is a product roadmap signal. "Sales Experience: Responsiveness" appearing negative in enterprise segment losses is a sales process signal.

### Deal metadata to capture alongside tags

```
Deal ID:
Date closed:
Outcome: Win / Loss / No decision
Competitor(s) evaluated:
Segment:
ACV:
Deal stage reached:
Interview date:
Interviewee role:
Primary driver (1):
Primary driver (2):
Primary driver (3):
Sentiment per driver: [Positive / Negative]
Key quote(s):
Confidence: [High / Medium / Low]
```

Store in a Notion database, Airtable, or a CRM custom field. A shared Google Sheet works fine at founder scale.

---

## Step 4: Founder-Scale Program (No Analyst)

**Month 1: Launch with minimum viable structure**

1. Pick your deal selection criteria and write them down (stage, ACV floor, time window)
2. Write a 10-question interview guide covering the 4 core topic areas
3. Set up a simple Notion database or Airtable table with the deal metadata fields above
4. Book 2-3 interviews from recent losses. Founder runs them.
5. Tag drivers after each call using the standard taxonomy

**Month 2-3: Build the cadence**

1. Aim for 5 interviews/month total (3 losses, 2 wins minimum)
2. After each interview, tag and log immediately while memory is fresh
3. At 10 interviews, look for patterns: which driver categories appear most often? Which segments? Which competitors?

**Month 3+: Add routing rituals**

Build these in before you need them:

| Ritual | Frequency | Audience | Format |
|---|---|---|---|
| Competitive digest | Weekly | Sales team | 2-3 bullet summary of new competitive signals |
| Insight readout | Monthly | Product, marketing | 5-10 min walkthrough of top driver themes |
| Quarterly report | Quarterly | Exec/founders | Win rate by segment, top drivers, competitor movement |

---

## Step 5: Insight Routing

Not all insights belong to the same team. Route to the right owner or it sits in a doc no one reads.

| Insight type | Route to | Action |
|---|---|---|
| Missing feature cited in 3+ losses | Product | Add to roadmap discussion with win/loss evidence |
| Competitor advantage in specific capability | Product + Sales | Update competitive battlecard; add to demo script |
| Sales process friction (slow responses, weak proposal) | Sales leadership | Sales coaching or process change |
| Pricing model confusion or resistance | Founder + Marketing | Pricing page update or packaging review |
| Onboarding cited as blocker after win | Customer Success | Onboarding flow improvement |
| ICP mismatch (wrong stage, wrong use case) | Marketing + Sales | Tighten ICP definition, adjust targeting |

**Developer-first routing addition:** Trial conversion losses (free users who churned without buying) route to Product as activation/onboarding signal, not to sales. These are separate from CRM deal losses and need a separate tagging track.

---

## Step 6: Pattern Detection

After 10+ interviews with consistent tagging, run these checks:

**By outcome:** Do wins and losses share different dominant drivers? If "Sales Experience" is positive in 80% of wins but neutral in losses, your sales team is a differentiator. If "Product: Missing feature" is the top negative driver in losses, it's a roadmap problem.

**By segment:** Filter to one segment (enterprise, SMB, a specific vertical). Do the drivers shift? Late-stage losses in enterprise with "Support: Implementation complexity" as top negative driver points to a different problem than SMB losses with "Pricing: Per-seat model" as the top driver.

**By competitor:** Group losses to a specific competitor. What driver clusters appear consistently? That is your competitive battlecard for that competitor.

**By deal stage:** Losses at demo stage vs. losses at proposal stage have different root causes. Early-stage losses are often ICP or messaging problems. Late-stage losses are often product, pricing, or sales execution.

---

## Tips

- Don't ask leading questions. "Would better pricing have changed your decision?" pushes toward pricing as the answer. "What would have changed the outcome?" lets the buyer tell you.
- Tag immediately after the call. Memory of nuance degrades within 24 hours.
- Wins are as important as losses. Understanding why you won prevents you from accidentally changing what's working.
- CRM "price" losses are almost always something else. When you see it, book an interview. It's rarely price.
- 5 interviews are not enough for patterns. Start tracking from interview 1, but don't draw conclusions until you have 8-10 sharing the same filter.

---

## Complementary Opendirectory Skills

| Skill | Use it to |
|---|---|
| `competitor-pr-finder` | Cross-reference competitor wins with where competitors are getting press |
| `gh-issue-to-demand-signal` | Map feature gap losses to open competitor GitHub issues |
| `pricing-finder` | Validate pricing-related loss drivers against actual competitor pricing |
| `map-your-market` | Refine ICP after seeing which segment profiles appear in recurring losses |
| `outreach-sequence-builder` | Re-engage lost deals with sequences that address the actual loss driver |
