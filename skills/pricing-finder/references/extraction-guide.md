# Pricing Page Extraction Guide

## What You're Extracting

From every pricing page, extract the following fields. All values must come verbatim from the fetched content -- do not fill from AI training knowledge.

---

## Identifying Tiers

**Signals that indicate a tier boundary:**
- Repeated heading structure: `## Starter`, `## Pro`, `## Business`
- Card-like sections with a name, a price, and a list of features
- A comparison table with tier names as column headers
- Repeated price+CTA pairs: `$29/mo [Get started]`, `$79/mo [Get started]`

**Tier name extraction:**
- Use the exact name shown on the page. Do not rename or paraphrase.
- Common names: Free, Starter, Basic, Plus, Pro, Business, Team, Growth, Scale, Enterprise
- If no tier name is visible: use "Plan 1", "Plan 2", etc.

**If there is only one paid plan:** record it as a single tier. Do not invent additional tiers.

---

## Extracting Prices

**Monthly price signals:**
- "$29/month", "$29/mo", "$29 per month", "$29 monthly"
- "$29" with "/month" nearby

**Annual price signals:**
- "$290/year", "$24.17/month billed annually", "Save 20% with annual"
- Always record the per-month equivalent: $290/year = $24.17/month
- "Billed annually" or "Save X%" indicates annual billing

**Free tier price:** Record as `0` (integer), not `null` or `"Free"`.

**Contact Sales / Custom pricing:**
- Record `enterprise_pricing` as `"Contact Sales"` exactly
- Set `price_monthly: null` for these tiers
- Never estimate or replace with a number

**"Starting at" pricing:** Record the starting price. Note "starting at" in `price_note`.

**If no price is visible on the page:** This is common for JS-rendered pages. Record `price_monthly: null` and `price_note: "not found in page data"`.

---

## Extracting Limits

Look for numbers associated with units. Common limit types:

| Limit type | Example signals |
|---|---|
| Users / seats | "up to 5 users", "per seat", "unlimited members" |
| Storage | "5 GB storage", "100 GB included" |
| API calls | "1,000 API calls/month", "10k requests" |
| Projects / workspaces | "up to 3 projects", "unlimited workspaces" |
| Records / rows | "up to 10,000 records", "unlimited rows" |
| Messages / emails | "5,000 emails/month" |
| Integrations | "up to 3 integrations", "unlimited integrations" |
| History | "7 day history", "unlimited version history" |

Record limits as plain strings: `"up to 5 users"`, `"1,000 API calls/month"`. Do not convert or normalize.

---

## Extracting Features

**Key features per tier:** The 3-5 most prominent features listed for that tier. Extract from:
- Bullet lists under each tier card
- Checkmarks in a comparison table
- "Includes everything in [lower tier], plus:" language

**Feature gate identification:**
- A feature is "always free" if it appears in the free/starter tier across all competitors
- A feature is "always paid" if it appears only in paid tiers across all competitors
- Features shown with a lock icon, strikethrough, or grayed-out are gated behind higher tiers

---

## Identifying the Pricing Model

Use the signals from `references/pricing-models.md`. Key rules:

1. If the price varies with user count: **per-seat**
2. If price is fixed regardless of users: **flat-rate** or **tiered-flat**
3. If price varies with consumption (API calls, messages, etc.): **usage-based**
4. If there is a free tier with feature gating: **freemium** (may also be per-seat or tiered-flat)
5. If multiple scaling dimensions exist: **hybrid**

When unsure between flat-rate and tiered-flat: tiered-flat has 3+ named tiers; flat-rate typically has 1-2.

---

## Billing Cadence

- **Monthly:** "billed monthly", "pay monthly", no mention of annual
- **Annual:** "billed annually", "per year", annual-only pricing shown
- **Both:** monthly and annual prices both shown (common -- record both)

**Annual discount:**
- Calculate from: `(monthly_price - annual_monthly_equivalent) / monthly_price * 100`
- Or read directly from: "Save 20%", "20% off annual"
- Round to nearest integer

---

## Free Tier vs Free Trial

This distinction is critical:

| Signal | Means |
|---|---|
| "Free forever", "Always free", "Free plan" | **Free tier** -- permanent, no credit card |
| "14-day free trial", "Try free for 30 days", "No credit card required" | **Free trial** -- time-limited |
| "Free trial" with no "free plan" | Trial only, no permanent free tier |
| Both | Some products offer both -- record both as `true` |

---

## CTAs (Call to Action) as Tier Signals

| CTA text | What it means |
|---|---|
| "Get started free", "Sign up free" | Free tier or free trial entry point |
| "Start free trial", "Try for free" | Free trial (time-limited) |
| "Get started", "Subscribe now" | Paid tier, direct signup |
| "Contact Sales", "Talk to Sales", "Request a demo" | Enterprise tier |
| "Upgrade", "Unlock" | Upgrade prompt from free tier |

---

## Regional Pricing

Flag if you see:
- Non-USD currency symbols: ₹ (India), € (Europe), £ (UK), R$ (Brazil)
- "Local pricing" or "India pricing" or "Pricing for [region]"
- Different prices shown based on detected country

Record regional pricing as a string: `"India: ₹999/mo"`, `"Europe: €25/mo"`.

---

## Data Quality Assessment

Assign `data_quality` based on what was fetched:

| Score | Condition |
|---|---|
| `high` | Full pricing page fetched (content > 2000 chars), prices clearly extracted |
| `medium` | Page fetched but content incomplete (500-2000 chars), or Google cache used |
| `low` | Page not fetched, using search snippet only (< 500 chars) |

When `data_quality: low`, note it in the output: prices may be outdated or incomplete.
