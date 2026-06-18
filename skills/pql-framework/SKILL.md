---
name: pql-framework
description: Build, calibrate, or audit a Product-Qualified Lead (PQL) scoring and routing system for PLG and developer-first companies. Use this skill whenever someone asks how to identify users ready to buy, which product events signal upgrade intent, how to route high-intent users to sales without a RevOps team, how to score users by product behavior, or any question about product-to-sales handoff, in-product conversion signals, or founder-scale PLG sales motions. Covers the full stack — signal library (behavioral + firmographic), pre-scoring exclusion filters, scoring matrix with decay and disqualifiers, A/B/C tiering, webhook routing to Slack/CRM, and a founder-day-1 path that requires zero data warehouse infrastructure.
compatibility:
  - claude-code
  - gemini-cli
  - github-copilot
author: Varnan
version: 1.0.0
---

# PQL Framework

A Product-Qualified Lead is a user who experienced your product firsthand and showed buying intent through behavior — not someone who downloaded a PDF. Two dimensions are always required: **what they did** (behavioral signals) and **who they are** (firmographic fit). Neither alone is sufficient.

## When to Use

- Launching a PQL motion for the first time (including founder-scale, no RevOps)
- Recalibrating a model generating too much noise or missing real buyers
- Deciding which product events to instrument before you have full telemetry
- Routing high-intent users to sales without a CRM pipeline
- Auditing why PQL→paid conversion is low

---

## Step 0: Pre-Scoring Filters

Run these **before** any scoring. Users that fail a filter are excluded entirely — not deprioritized in score. This prevents model noise from accounts that can never convert.

| Exclude if | Reason |
|---|---|
| Already paid, no upgrade path available | No upsell potential |
| Trial expired >14 days, no re-engagement | Intent has decayed; route to re-engagement nurture instead |
| Active CS escalation or churn-save flag in progress | Sales outreach during a crisis destroys the relationship |
| Confirmed competitor domain | Research accounts, not buyers |
| Bot / spam pattern (no meaningful activity sequence) | Pollutes scoring |

---

## Step 1: Signal Library

### Behavioral Signals (What They Did)

**Activation** — has the user completed your core value loop?
- Created first project / connected first integration / completed onboarding
- Used the defining core feature at least once

**Depth** — are they going deeper, not just exploring?
- Used high-value features (features paid customers use disproportionately)
- Repeated core feature use: 3+ sessions in a rolling 7-day window
- Multi-product or multi-workspace usage

**Expansion** — organizational buying intent (strongest signal class for developer-first PLG)
- Invited a teammate → account now has 2+ users (Vercel's upsell trigger 1)
- Account grew from single-team to multi-team usage (Vercel's upsell trigger 2)
- Created shared workspaces, projects, or permission structures
- Collaboration feature engagement (comments, sharing, role assignments)

Expansion signals represent permanent organizational state changes. They outperform arbitrary usage thresholds because they surface the moment a team — not just an individual — is adopting the product.

**Monetization proximity** — bumping into limits?
- Visited pricing page 2+ times in 14 days
- Clicked an upgrade CTA or viewed a paid feature gate
- Approaching or hit a plan usage/seat/API limit

### Firmographic Signals (Who They Are)

Determine whether behavioral signals are worth acting on. High usage from a bad-fit account is noise.

| Signal | Source options |
|---|---|
| Company size (10–500 employees is PLG sweet spot) | Clearbit, Apollo, LinkedIn |
| Job title / role (decision-maker vs. individual contributor) | Email domain + enrichment |
| Funding stage (funded = budget exists) | Crunchbase, Apollo |
| Tech stack overlap | BuiltWith, GitHub profile analysis |
| ICP vertical match | Email domain + enrichment |

Use the `company-radar` skill for multi-source firmographic enrichment on signup email.

---

## Step 2: Scoring Model

Start with a weighted point system. ML-based scoring only pays off after 100+ observed conversions.

### Sample Scoring Matrix

| Signal | Points | Notes |
|---|---|---|
| Completed activation milestone | +20 | Your defined "aha moment" event |
| Core feature used 3x in 7 days | +15 | Rolling 7-day window |
| Invited a teammate | +20 | Strongest early expansion signal |
| Multi-team account growth | +25 | Organization-level buying intent |
| Pricing page visited 2x in 14 days | +15 | Explicit upgrade consideration |
| Hit plan usage limit | +20 | Forced upgrade consideration |
| ICP firmographic match | +15 | Multiplier on behavioral signals |
| No activation after 7 days of signup | −10 | Weak engagement signal |
| Single session, never returned | −15 | No retention signal |

**Default routing threshold:** score ≥ 60 → route to Tier A or B. Calibrate this after 30 days of conversion data.

### Decay Logic

Signals go stale. Apply time-based decay so old behavior doesn't perpetually inflate scores.

- **7-day decay**: halve the score contribution of any event with no follow-on activity in 7 days
- **14-day reset**: no product activity for 14 days → score drops to 0, account enters re-engagement pool
- **Exception**: expansion signals (teammate invite, multi-team growth) do not decay — they are permanent organizational state changes, not time-bounded behaviors

### Disqualifier Signals (Override High Scores)

These suppress routing even when score is high:

- Trial expiry warning fired + no login in 5 days → likely churning, not buying → re-engagement nurture
- Support ticket marked critical or escalated → wrong moment for sales contact
- Previously marked "not interested" by sales → respect the signal

---

## Step 3: Tiering

| Tier | Score | Meaning | Motion |
|---|---|---|---|
| **A** | 80+ | High intent + ICP match | Personal outreach within 2 hours |
| **B** | 60–79 | Moderate intent or partial ICP fit | Outreach within 24 hours |
| **C** | 40–59 | Early signal, watch | Add to nurture; revisit in 7 days |
| **Disqualified** | Any (triggered a disqualifier) | Excluded | Re-engagement nurture or no action |

---

## Step 4: Routing

### Founder-Scale Path (No RevOps, No CRM Pipeline)

**Day 1 — wire 2-3 signals to Slack:**
1. Pick the 2-3 events most correlated with paid conversion in your product. If unknown, start with: `user_activated` + `teammate_invited` + `pricing_page_viewed_2x`
2. Wire those events to a Slack webhook via your existing analytics tool:
   - PostHog → Webhooks (free, open source)
   - Mixpanel → Zapier → Slack
   - Segment → webhook destination
   - Amplitude → webhook integration
3. When alert fires, founder reviews and sends a personal email within the hour
4. Log outcome in Notion or Airtable: contacted → replied → converted → deal size

**Day 30 — add firmographic filter:**
1. Before the webhook fires, check ICP firmographic match (company size, job title)
2. Use Clearbit Reveal or Apollo enrichment on the signup email domain
3. Only fire the Slack alert when behavioral signal + ICP match are both true
4. This cuts alert volume significantly without missing real buyers

**Day 90 — add tiering:**
1. Implement A/B/C tiers based on 30 days of conversion data
2. Tier A → founder or AE reaches out personally
3. Tier B → automated personalized email sequence (use `outreach-sequence-builder`)
4. Tier C → add to drip nurture

### Routing Channels by Tier

| Tier | Channel | Response SLA | Owner |
|---|---|---|---|
| A | Slack alert + personal email or call | 2 hours | Founder / AE |
| B | Automated personalized email sequence | 24 hours | Email automation |
| C | Nurture drip | 7 days | Marketing |
| Disqualified | Re-engagement nurture or no action | N/A | — |

**Timing matters:** For PLG with fast sales cycles (<14 days), fire the alert while the user is still active in the product. Webhook routing achieves seconds-level latency — use it. For enterprise cycles (6+ months), batch or hourly scoring is sufficient.

---

## Step 5: Measurement Loop

Track these weekly:

| Metric | What it tells you |
|---|---|
| PQL → paid conversion rate | Model precision — are you flagging the right people? |
| Time-to-first-touch after PQL fires | Routing speed — are you acting fast enough? |
| Tier A conversion rate vs. Tier B | Is your tiering calibrated correctly? |
| False positive rate (PQLs that never engage back) | Model noise — tighten ICP filter or raise threshold |
| Disqualification rate | If >40% of scored users get excluded, pre-filters need tuning |

**Compound the model:** After 30 days, identify users who converted to paid but were never flagged as PQLs. What signals did they share? Add those events to the scoring matrix. Repeat monthly.

---

## Tips

- Expansion signals (teammate invite, multi-team growth) are the highest-signal PQL events for developer-first products. Vercel's CRO identified these two milestones as their primary enterprise upsell triggers — weight them heavily
- Exclude ineligible accounts before scoring (pre-filter), not after (deprioritize). Keeping them in the model pollutes weights and wastes review time
- Ship the simplest possible version first: one Slack webhook, two behavioral events, one firmographic filter. You'll learn more from 30 days of real routing than from building a perfect model upfront
- For SDK/API-first products, use `sdk-adoption-tracker` to surface adoption events (new repos importing your SDK, rising download velocity) as behavioral signals in your PQL library
- Re-evaluate scoring weights every 30 days using actual conversion data — the model calibrated at 100 users rarely holds at 10,000

---

## Complementary Opendirectory Skills

| Skill | Use it to |
|---|---|
| `sdk-adoption-tracker` | Surface API/SDK adoption as behavioral signals (dev-first products) |
| `company-radar` | Enrich accounts with firmographic data for the identity dimension |
| `outreach-sequence-builder` | Build Tier A/B follow-up sequences triggered by PQL routing |
| `where-your-customer-lives` | Define your ICP before configuring firmographic filters |
| `map-your-market` | Validate ICP definition using real market signal data |
