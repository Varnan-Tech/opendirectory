# Stage Signals Reference

Used by SKILL.md Step 4 to detect funding stage from product page content before any API call.

---

## Signal Detection Table

| Signal Pattern (regex) | Stage Hint | Example Page Text |
|---|---|---|
| `join (the )?waitlist` | pre-seed | "Join the waitlist for early access" |
| `sign up for beta` | pre-seed | "Sign up for our beta program" |
| `early access` | pre-seed | "Request early access" |
| `request (an? )?invite` | pre-seed | "Request an invite" |
| `get notified` | pre-seed | "Get notified when we launch" |
| `start (your )?free trial` | seed | "Start your free 14-day trial" |
| `try (it )?for free` | seed | "Try for free, no credit card required" |
| `request a? demo` | seed | "Request a demo" |
| `book a? demo` | seed | "Book a demo with our team" |
| `schedule a? demo` | seed | "Schedule a 30-minute demo" |
| `contact sales` | series-a | "Contact sales for enterprise pricing" |
| `talk to (our )?sales` | series-a | "Talk to our sales team" |
| `see pricing` / `view pricing` | series-a | "See pricing" |
| `plans and pricing` | series-a | "Plans and Pricing" |
| `case stud(y\|ies)` | series-a | "Read our case studies" |
| `customer stor(y\|ies)` | series-a | "Customer success stories" |
| `trusted by \d+` | series-a | "Trusted by 2,000+ teams" |
| `enterprise (plan\|pricing\|tier)` | series-a-or-b | "Enterprise plan available" |
| `we.?re hiring` | series-a-or-b | "We're hiring -- see open roles" |
| `join our team` | series-a-or-b | "Join our team of 50+" |
| `raised \$[\d,.]+[mk]?` | announced | "We raised $8M in Series A" |
| `series [abc] round` | announced | "Series B round closed" |
| `seed round` | announced | "Seed round led by X" |

---

## Signal Confidence Rules

| Signals Found | Confidence |
|---|---|
| 2 or more matching signals | high |
| Exactly 1 matching signal | medium |
| 0 signals (stage estimated from content alone) | low |
| Funding announcement text found directly | high (overrides other signals) |

---

## Handling Conflicting Signals

Some pages show signals from multiple stages simultaneously (e.g. a pricing page AND a waitlist). Use this resolution order:

1. Funding announcement text wins over all other signals (the stage is known, not inferred)
2. If both "pricing page" (Series A) and "free trial" (seed) signals appear: call it seed-to-series-a transition, output `series-a` with medium confidence
3. If both "waitlist" (pre-seed) and "demo request" (seed) signals appear: output `seed` -- the product is likely further along than the waitlist implies
4. If no signals found at all: output `unknown` with low confidence, pass this to Gemini with a note to infer from product maturity and content

---

## Common Misdetections

**"Request demo" from a mature Series B company:** Some large companies keep demo CTAs even after raising Series B. Override signals if the page also shows: enterprise logo bars, "trusted by Fortune 500", or explicit Series B announcement.

**Open-source projects:** Often show no stage signals (no pricing, no CTA). Output `unknown`. In the Gemini analysis step, note that the product appears open-source and ask Gemini to infer whether there is a commercial entity behind it.

**Startup landing pages with no product live:** A site with only a headline, a value prop paragraph, and an email capture is almost certainly pre-seed. Even without explicit waitlist language, if the page has no product demo and no pricing, output `pre-seed` with medium confidence.

---

## Stage-to-Tavily Query Modifiers

These modifiers are added to Track B search queries based on detected stage:

| Detected Stage | Query Modifier |
|---|---|
| pre-seed | "pre-seed micro VC angel" |
| seed | "seed fund" |
| series-a | "series A lead investor" |
| series-b | "growth stage VC" |
| unknown | "early stage" (default) |

Example Track B query with modifier:
- L3 = "CI/CD automation", stage = seed
- Query: `seed fund "CI/CD automation" investment thesis portfolio companies`

---

## Stage-to-VC-Check-Size Reference

Use this to validate stage fit scores in the synthesis step:

| Stage | Typical Check Size |
|---|---|
| Pre-seed | $25K-$500K |
| Seed | $500K-$3M |
| Series A | $3M-$15M |
| Series B | $15M-$50M |

A VC whose typical check size is $20M-$50M has a stage fit score of 2 or lower for a pre-seed product, regardless of how well their thesis matches.
