# Competitive Positioning Guide

## The Four Quadrants

Map every competitor onto two axes: **price** (entry tier monthly price) and **feature density** (number of features / complexity of offering).

```
High price
    |
    |  [Simple+Premium]    [Feature-rich+Expensive]
    |  rare, luxury feel   enterprise, complex
    |
    |-------------------------------------> High feature density
    |
    |  [Cheap+Simple]      [Cheap+Complex]
    |  common entry play   rare, usually unsustainable
    |
Low price
```

**Cheap + Simple:** Low entry price, few tiers, limited features. Target: individual users or very small teams. Example: a $9/mo tool with 2 tiers.

**Feature-rich + Expensive:** High price, many tiers, deep feature set. Target: mid-market and enterprise. Example: Salesforce, HubSpot Professional.

**Simple + Premium:** High price, few features, strong brand or niche value. Rare. Example: some design tools, high-end professional services SaaS.

**Cheap + Complex:** Low price but feature-heavy. Often unsustainable (or a market disruptor using VC subsidy). Example: early-stage PLG tools burning cash on free tiers.

---

## Identifying the Underserved Gap

After mapping all 5 competitors, look for empty quadrants or unoccupied price ranges.

**Common gap types:**

**Price gap:** All competitors cluster at $15-$79/mo. No one at $99-$199/mo (mid-market gap) or below $10/mo (micro-SMB gap).

**Model gap:** All competitors use per-seat pricing. No flat-rate option for teams that hate per-user billing.

**Tier gap:** All competitors have 3+ tiers with complex feature gates. No simple 2-tier product (free + one paid).

**Segment gap:** All competitors target enterprises with Contact Sales. No self-serve option for the startup/SMB segment.

**Feature gap:** All competitors include features X and Y but no one prominently leads with feature Z (even if Z is in the product). Z could be the lead differentiator.

---

## Positioning the Recommendation

**Anchor pricing principle:** The highest tier sets the perceived value ceiling for lower tiers. A $499/mo enterprise plan makes $99/mo feel cheap and accessible, even if $99/mo was always the real target.

**Implication for recommendation:** Always design top-down: set a high anchor (enterprise or top tier) first, then position the intended primary tier below it to feel like a deal.

---

## Freemium Decision Framework

Ask: how many of the 5 competitors have a free tier?

| Free tier count | Implication |
|---|---|
| 4-5 out of 5 | Free tier is table stakes in this space. Not having one is a significant disadvantage for self-serve acquisition. Recommend free tier. |
| 2-3 out of 5 | Free tier is common but not universal. Consider it if PLG is part of the go-to-market. Not having one is defensible if sales-led. |
| 0-1 out of 5 | Free tier is not the norm. Not expected by buyers. Skip it unless there's a specific PLG reason. |

**Exception:** If the product's primary differentiator is something that should NOT be given away free (e.g., an AI model that costs money to run per query), recommend against free tier regardless of competitor prevalence.

---

## Annual Discount Framework

**Market norm:** 15-20% discount for annual commitment is standard across most B2B SaaS.

**When to go higher (25-30%):** If competitors all offer 20% and annual commitment is strategically important (reduces churn, improves cash flow).

**When to skip annual discount:** If the product is month-to-month by nature (e.g., seasonal tools, event-based tools) or if the team is too small to benefit from annual cash upfront.

**Annual discount calculation benchmark:**
- 15% annual discount = $1 saved for every $6.67/mo
- 20% annual discount = $1 saved for every $5/mo
- Standard formula: annual_monthly_equivalent = monthly_price * (1 - discount)

---

## Feature Gate Strategy

**What to gate behind paid:**
1. The product's primary differentiator -- the thing users upgrade for
2. Collaboration features (more users, sharing, permissions)
3. Advanced integrations (enterprise SSO, API access, webhooks)
4. Historical data, exports, or reporting
5. Priority support or SLAs

**What to keep free:**
1. Core product functionality that demonstrates value (enough to get hooked)
2. Onboarding flows and templates
3. Basic integrations (1-2 popular tools)
4. Community / public sharing features (if they drive viral growth)

**The golden rule of free tier design:** The free tier should be good enough that users get real value and tell others -- but not so good that they never upgrade.

---

## Race-to-the-Bottom Warning Signs

If the market shows these signals, do NOT recommend competing on price:

- Multiple competitors have recently lowered prices (check for "we've lowered our prices" blog posts in search results)
- The lowest entry tier is below $5/mo
- Freemium tiers are extremely generous (unlimited users on free tier, etc.)
- Several competitors have shut down or pivoted recently

**Instead:** Recommend competing on: a specific underserved segment, a specific workflow that competitors ignore, or a model innovation (e.g., flat-rate in a per-seat market).
