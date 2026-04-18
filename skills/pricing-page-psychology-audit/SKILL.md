---
name: pricing-page-psychology-audit
description: Audits any SaaS pricing page URL against 12 pricing psychology principles and outputs a ranked improvement report with specific rewrite suggestions and quick wins.
author: ajaycodesitbetter
version: 1.0.0
---

# Pricing Page Psychology Audit

Scrape any SaaS pricing page and audit it against 12 proven pricing psychology
principles. Get a scored Markdown report with specific rewrite suggestions per
tier and a "Top 3 Quick Wins" section.

---

## Step 1: Get the Target URL

Ask the user:
"Which SaaS pricing page should I audit? Share the full URL
(e.g. https://linear.app/pricing)"

If no URL is provided, stop and ask. Do not proceed without a valid URL
starting with http:// or https://.

---

## Step 2: Run the Scraper

Run the scraper script with the URL:

```bash
python scripts/scrape_pricing.py "URL_HERE"
```

The script outputs structured text to stdout. Capture the output — it contains:
- Page title
- All visible text content
- Button labels (CTAs)
- Plan names and prices
- Feature list items

If the script fails (timeout, blocked, invalid URL), tell the user:
"The page could not be scraped: [error]. Try a different URL or check
if the site blocks bots."

---

## Step 3: Evaluate Against 12 Psychology Principles

Analyze the scraped content against each principle. For each, assign:
- ✅ Pass — clearly present and well-executed
- ⚠️ Needs Work — present but weak or could be improved
- ❌ Missing — not present at all

### The 12 Principles:

1. **Anchoring** — Is there a high-priced plan shown first or prominently to
   make others feel cheaper?

2. **Decoy Effect** — Is there a middle-tier plan designed to make the top
   tier look like better value?

3. **Loss Aversion Framing** — Does copy use "don't miss out", "limited",
   "you'll lose access" rather than purely gain language?

4. **Feature-vs-Value Naming** — Do plan names/descriptions highlight
   outcomes ("Close more deals") vs just features ("10 seats")?

5. **Social Proof Placement** — Are testimonials, logos, or user counts
   shown near pricing tiers (not just on a separate page)?

6. **Urgency / Scarcity Signals** — Is there a countdown timer, limited
   spots badge, or "offer ends" language?

7. **Plan Naming Psychology** — Are plan names aspirational
   (Starter/Growth/Scale) vs generic (Basic/Pro/Enterprise)?

8. **CTA Button Copy** — Do CTAs say action-outcome ("Start growing free")
   vs generic ("Sign up" or "Get started")?

9. **Free Trial vs Freemium Framing** — Is the free offer framed clearly?
   Does it reduce friction or create confusion?

10. **Price Ending Tactics** — Do prices end in 9 ($49, $99) for perceived
    value, or round numbers ($50, $100) for premium feel?

11. **Visual Hierarchy of Tiers** — Is the recommended/popular plan visually
    highlighted (badge, border, size difference)?

12. **Guarantee / Trust Signal Presence** — Is there a money-back guarantee,
    "no credit card required", or security badge near the CTA?

---

## Step 4: Generate the Audit Report

Output the report in this exact Markdown structure:

```
# Pricing Page Psychology Audit
**URL:** [URL]
**Audited on:** [today's date]
**Overall Score:** X/12 principles passing

---

## Audit Results

### 1. Anchoring — ✅ Pass / ⚠️ Needs Work / ❌ Missing
**What we found:** [1-2 sentences from the page]
**Suggestion:** [Specific rewrite or change to make]

[Repeat for all 12 principles]

---

## 🏆 Top 3 Quick Wins

These are your highest-leverage changes, prioritized by impact vs effort:

**Quick Win #1 — [Principle name]**
Current: "[exact copy from page]"
Rewrite to: "[your improved version]"
Why: [1 sentence on the psychological mechanism]

**Quick Win #2 — [Principle name]**
...

**Quick Win #3 — [Principle name]**
...
```

---

## Step 5: Self-QA Before Output

Check before presenting the report:
- [ ] All 12 principles are scored (none skipped)
- [ ] Each "Suggestion" is specific — no generic advice like "add social proof"
- [ ] Quick Wins cite actual copy from the page (not invented)
- [ ] Scores reflect what is literally present in the scraped content
- [ ] Date is today's actual date

Fix any violation before output.

---

## Step 6: Offer Follow-ups

After presenting the report, offer:
1. "Export this as a PDF-ready Markdown file"
2. "Generate rewrite copy for all CTAs on this page"
3. "Compare against a competitor's pricing page"
4. "Build a prioritized action plan for the dev team"
