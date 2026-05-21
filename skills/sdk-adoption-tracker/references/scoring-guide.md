# Adoption Scoring Guide

Used by SKILL.md Step 4 and scripts/fetch.py to classify repos by adoption signal strength.

---

## The Problem with Raw Search Results

A GitHub code search for `require("stripe")` returns 1,000+ repos. Most are:
- Tutorials: "learn-stripe-payments", "stripe-integration-example"
- Forks: someone forked the official Stripe SDK
- Abandoned side projects: last push was 2021
- Test repos: "stripe-test-app", "payment-playground"

The adoption score filters these out and surfaces the signal that matters: an active company repo using your SDK in production.

---

## Scoring Formula

```python
score = 0

# Company signals (highest weight -- this is what you want to find)
if owner_type == "Organization":          score += 50  # GitHub org = company or team
if company_field and company_field.strip(): score += 20  # user has company listed on GitHub

# Activity signals
score += min(stars, 500) / 10            # up to 50 points; capped at 500 stars
if days_since_push < 30:                 score += 30  # active in last month
if days_since_push < 7:                  score += 20  # active this week (cumulative with above)

# Quality signals
if not is_fork:                          score += 10  # original project, not a fork
if not is_archived:                      score += 10  # not abandoned
if not is_tutorial:                      score += 20  # not a demo or example

# Maximum possible score: 160+
# Typical company_org with recent activity: 110-150
# Typical active solo dev project: 60-90
# Typical stale personal project: 20-40
# Tutorial/noise: 0-20
```

---

## Score Tiers

| Score | Tier | What it means |
|---|---|---|
| >= 80 | High signal | Generate a full adoption brief and outreach message |
| 40-79 | Medium signal | List in report, no full brief |
| < 40 | Noise | Include in breakdown count only |

---

## Company Classification Tiers

| Tier | Criteria | Confidence |
|---|---|---|
| `company_org` | `owner.type == "Organization"` | High -- GitHub org accounts are almost always a company, team, or serious open-source project |
| `affiliated_dev` | `owner.type == "User"` AND `company` field populated on GitHub profile | Medium -- self-reported, but developers with a company listed are usually professionals |
| `solo_dev` | `owner.type == "User"` AND no company field AND stars >= 10 | Low -- could be anyone; stars signal real usage |
| `tutorial_noise` | Name or description matches tutorial keywords, OR repo is a fork, OR repo is archived | Excluded from lead output |

---

## Tutorial Noise Detection

A repo is classified as `tutorial_noise` if its name or description contains any of these words:

```
example, tutorial, demo, learn, sample, starter, boilerplate,
template, playground, test, course, workshop
```

Additional noise signals:
- `fork == true`: the repo is a fork (could be a fork of the SDK itself)
- `archived == true`: the repo is no longer maintained
- Repo name matches the SDK name exactly (e.g. searching for `stripe` and finding a repo called `stripe`)
- Repo name starts with the SDK name followed by a dash (e.g. `stripe-clone`, `stripe-copy`)

---

## Velocity Signals

Velocity is inferred from `created_at` dates, not from direct historical data.

**Primary velocity metric:** Count of repos with `created_at` in the last 7, 14, and 30 days.

```
New repos last 7 days:  3
New repos last 30 days: 11
```

This tells you: 3 new teams started using the SDK in the last week.

**Secondary velocity metric (requires previous snapshot):** When a previous JSON snapshot exists in `docs/sdk-adopters/`, compare the current repo list to the previous one. The difference is the exact set of new adopters since the last run.

```
New since last run (14 days ago): 5
```

**Velocity interpretation:**
- 0 new in 30 days: stagnant adoption, possibly indexed months ago and no new users
- 1-3 new in 7 days: healthy organic growth
- 5+ new in 7 days: breakout adoption, consider proactive outreach

---

## The Top Contributor Signal

For each enriched repo, the script fetches the top 3 contributors by commit count via:
`GET /repos/{owner}/{repo}/contributors?per_page=3`

The person with the most commits is the most likely person to have introduced the SDK to that project. They are the warmest possible outreach target because:
1. They chose the SDK
2. They understand what it does
3. They have the context to evaluate an upgrade, integration, or partnership

If you cannot identify the top contributor (rate limit, private contributors), fall back to the repo owner.

---

## Why Organization Repos Are Worth 50 Points

A `owner.type == "Organization"` repo means:
- A team created a GitHub org to publish this code
- At minimum, multiple people are involved
- The code is likely maintained beyond a single developer's interest
- The org may represent an actual company (check `org.blog` for the website)

Contrast with a user repo: one developer, may be a side project, no team ownership.

The 50-point weight reflects that finding a company using your SDK is 2-3x more valuable for GTM purposes than finding an individual developer.

---

## Common Misclassifications

**Large open-source projects classified as company_org:**
A GitHub org doesn't always mean a company. The Linux Foundation, Apache, CNCF, and similar foundations use orgs. These are valuable signal (indicates enterprise-grade adoption) but the outreach angle differs -- reach out to the project maintainers, not a sales contact.

**Tutorial repos with high stars:**
A well-known tutorial like "stripe-payments-tutorial" may have 500 stars. The adoption score caps the star contribution at 50 points (max 500 stars / 10), but the tutorial detection should have already filtered it. If a high-star tutorial slips through, check `data_quality_flags`.

**New repos with inflated scores:**
A repo created this week by an organization (50 points) with active recent push (50 points) scores 100+ even with 0 stars. This is intentional: a company adopting the SDK this week is a higher-priority outreach target than a solo dev with 50 stars who hasn't pushed in 6 months.
