# Radar Report Template

One output template for all radar runs. The structure is fixed. Fill in all brackets from collected data. No brackets should appear in the final output.

---

## Report Header

```
# Company Radar Report

**Generated:** [date]
**Companies tracked:** [N]
**Timeframe:** [realtime / last-week / last-month]
**Channels scanned:** GitHub, Twitter/X, Reddit, Hacker News, Product Hunt, YC Jobs, Web, [other]

---

## Executive Summary

[2-3 paragraph synthesis of the competitive landscape. Rank companies by heat score. 
Call out the biggest movers, most interesting signals, and any urgent alerts.]

**Top-line rankings:**
1. [Company A] — [score]/100 — [activity level]
2. [Company B] — [score]/100 — [activity level]
3. [Company C] — [score]/100 — [activity level]

**Key alerts this run:** [N] notable signals detected
```

---

## Heat Score Leaderboard

```
| Rank | Company | Heat Score | Activity | Authority | Shipping | Social | Growth | Hiring? |
|---|---|---|---|---|---|---|---|---|
| 1 | [Name] | [0-100] | [High/Med/Low/Dormant] | [0-25] | [0-25] | [0-25] | [0-25] | [Yes/No] |
| 2 | [Name] | [0-100] | [High/Med/Low/Dormant] | [0-25] | [0-25] | [0-25] | [0-25] | [Yes/No] |
```

---

## Per-Company Deep Dives

Repeat for each company. Order by heat score (highest first).

```
---

## [Company Name]

**Profile:** [description from web research]
**Domain:** [url]
**Twitter:** [@handle or "Not found"]
**GitHub:** [org or "Not found"]
**YC Batch:** [batch or "N/A"]
**Founders:** [names with Twitter handles]

### Heat Score: [score]/100 — [Activity Level]

| Dimension | Score | Key Drivers |
|---|---|---|
| Authority | [0-25] | [key data points] |
| Shipping | [0-25] | [key data points] |
| Social | [0-25] | [key data points] |
| Growth | [0-25] | [key data points] |

### Signal Details

**GitHub:**
- Stars: [N] | Forks: [N] | Commits/Week: [N]
- Releases/Month: [N] | Last push: [date]
- Primary language: [lang]
- [Notes on shipping velocity]

**Twitter/X:**
- Tweets (24h): [N] | Mentions: [N]
- Founder activity: [summary]
- Key topics: [topics]

**Reddit:**
- Mentions: [N] | Total score: [N]
- Sentiment: [positive/negative/mixed]
- Key threads: [top 2-3 thread titles]

**Hacker News:**
- Stories: [N] | Total points: [N]
- Front page stories: [N]
- Key discussions: [top 1-2 story titles]

**Product Hunt:**
- Recent launches: [N]
- Total votes: [N]
- Launch frequency: [High/Medium/Low/None]

**YC Jobs:**
- Open roles: [N]
- Departments hiring: [list]
- Notable roles: [top 2-3 titles]

**Web / Press:**
- Funding: [details or "None detected"]
- Product launches: [details or "None"]
- Key news: [top 1-2 items]

### Executive Briefing

[AI-generated briefing following the format from SKILL.md Step 6]

### Alerts

| Type | Severity | Detail |
|---|---|---|
| [Alert type] | [High/Med/Low] | [Description] |
```

---

## Alerts Summary

```
## Alerts This Run

| Severity | Type | Company | Description |
|---|---|---|---|
| 🔴 High | [Type] | [Company] | [Summary] |
| 🟡 Medium | [Type] | [Company] | [Summary] |
| 🟢 Low | [Type] | [Company] | [Summary] |
```

---

## Data Quality Notes

```
## Data Quality

| Company | GitHub | Twitter | Reddit | HN | PH | YC Jobs | Web |
|---|---|---|---|---|---|---|---|
| [A] | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| [B] | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |

**Notes:**
- [Channel X] had no data for [reason]. Score may be understated.
- [Company Y] missing GitHub because org not found.
- [Channel Z] API key not configured.
```

---

## Worked Example (Truncated)

```
# Company Radar Report

**Generated:** 2026-05-29
**Companies tracked:** 3
**Channels scanned:** GitHub, Twitter/X, Reddit, Hacker News, Product Hunt, YC Jobs, Web

---

## Executive Summary

Vercel leads the pack with a heat score of 89 (High activity), driven by massive GitHub
authority and active shipping. Netlify is close behind at 72, with strong social presence
but slower shipping velocity. Railway is the dark horse at 45, showing medium activity with
interesting hiring signals that suggest a growth phase.

**Top-line rankings:**
1. Vercel — 89/100 — High
2. Netlify — 72/100 — High
3. Railway — 45/100 — Medium

**Key alerts this run:** 2 notable signals (Vercel GH star surge, Railway hiring spike)

---

## Heat Score Leaderboard

| Rank | Company | Heat Score | Activity | Authority | Shipping | Social | Growth | Hiring? |
|---|---|---|---|---|---|---|---|---|
| 1 | Vercel | 89 | High | 25 | 25 | 17 | 22 | Yes |
| 2 | Netlify | 72 | High | 20 | 15 | 22 | 15 | Yes |
| 3 | Railway | 45 | Medium | 8 | 12 | 10 | 15 | Yes |
```
