<img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1280&h=640&fit=crop&q=80" width="100%" alt="cover" />

# pricing-page-psychology-audit

> Paste any SaaS pricing page URL. Get a full audit against 12 pricing
> psychology principles — with scores, specific rewrites, and your Top 3
> Quick Wins ranked by impact.

[![opendirectory](https://img.shields.io/badge/opendirectory-skill-blue)](https://opendirectory.dev)
[![version](https://img.shields.io/badge/version-1.0.0-green)](https://github.com/Varnan-Tech/opendirectory)
[![license](https://img.shields.io/badge/license-MIT-orange)](https://opensource.org/licenses/MIT)

---

## What It Does

Most SaaS pricing pages leave money on the table — not because of bad pricing,
but because of bad psychology. This skill scrapes any pricing page and audits it
against 12 proven pricing psychology principles used by companies like Notion,
Linear, and Vercel.

**12 Principles Audited:**

| # | Principle | What It Checks |
|---|-----------|----------------|
| 1 | Anchoring | Is the priciest plan shown first to anchor perception? |
| 2 | Decoy Effect | Is there a tier that makes the top plan look like great value? |
| 3 | Loss Aversion Framing | Does copy use "don't lose access" vs purely gain language? |
| 4 | Feature-vs-Value Naming | Do tiers sell outcomes or just list features? |
| 5 | Social Proof Placement | Are testimonials/logos visible near the pricing tiers? |
| 6 | Urgency / Scarcity | Are there "limited time" signals or countdown elements? |
| 7 | Plan Naming Psychology | Are names aspirational (Growth, Scale) vs generic (Pro, Basic)? |
| 8 | CTA Button Copy | Do CTAs say "Start closing more deals" vs "Sign up"? |
| 9 | Free Trial vs Freemium | Is the free offer framed clearly without confusion? |
| 10 | Price Ending Tactics | Do prices end in 9 ($49) or round ($50)? |
| 11 | Visual Hierarchy | Is the recommended tier visually distinct (badge, highlight)? |
| 12 | Guarantee / Trust Signals | Is there a money-back guarantee near the CTA? |

**Output includes:**
- ✅ / ⚠️ / ❌ score per principle
- Specific rewrite suggestions per tier
- **Top 3 Quick Wins** — highest-leverage changes, prioritized by impact vs effort

---

## How It Works

```
User provides URL
      ↓
scripts/scrape_pricing.py fetches and extracts:
  - Plan names & prices
  - CTA button copy
  - Feature list items
  - Full visible text
      ↓
AI evaluates scraped content against 12 psychology principles
      ↓
Structured Markdown audit report output
  + Top 3 Quick Wins
```

---

## Prerequisites

- Python 3.10+
- pip packages:

```bash
pip install requests beautifulsoup4
```

- Works with: **Claude Code · Gemini CLI · Cursor · Antigravity**

---

## Install

```bash
npx @opendirectory.dev/skills install pricing-page-psychology-audit
```

---

## Usage

### Basic audit:
```
"Use pricing-page-psychology-audit to audit https://linear.app/pricing"
```

### More examples:
```
"Audit the pricing page at https://notion.so/pricing"
"Run a psychology audit on https://vercel.com/pricing"
"What's wrong with https://stripe.com/pricing from a psychology perspective?"
```

---

## Example Output

```markdown
# Pricing Page Psychology Audit
**URL:** https://linear.app/pricing
**Audited on:** 2026-04-18
**Overall Score:** 9/12 principles passing

---

## Audit Results

### 1. Anchoring — ✅ Pass
**What we found:** Enterprise plan is listed last but priced highest at
custom pricing, creating an anchor that makes the $16/seat Business plan
feel accessible.
**Suggestion:** Consider moving Enterprise to first position for stronger
anchoring effect.

### 2. Decoy Effect — ⚠️ Needs Work
**What we found:** The Business tier exists between Free and Enterprise
but is not clearly positioned as the "sweet spot."
**Suggestion:** Add a "Most Popular" badge to Business and increase visual
size to activate the decoy effect.

[... 10 more principles ...]

---

## 🏆 Top 3 Quick Wins

**Quick Win #1 — CTA Button Copy**
Current: "Get started"
Rewrite to: "Start shipping faster — free"
Why: Action-outcome CTAs convert 14% higher than generic "Get started" copy.

**Quick Win #2 — Social Proof Placement**
Current: Logos shown on a separate /customers page
Rewrite to: Add 3 customer logos directly below the pricing tiers
Why: Social proof near the decision point reduces purchase anxiety.

**Quick Win #3 — Guarantee / Trust Signal**
Current: No guarantee mentioned on pricing page
Rewrite to: Add "30-day money-back guarantee. No questions asked." below CTAs
Why: Guarantees have been shown to increase conversion by up to 21%.
```

---

## Project Structure

```
pricing-page-psychology-audit/
├── SKILL.md              ← AI instructions (the brain)
├── README.md             ← This file
├── .env.example          ← No API keys required
└── scripts/
    └── scrape_pricing.py ← Python scraper (requests + BeautifulSoup)
```

---

## License

MIT — Built by [@ajaycodesitbetter](https://github.com/ajaycodesitbetter)
