# Heat Score Methodology

The Company Radar heat score is a 0-100 composite score computed from four equally-weighted dimensions. It measures competitive intensity and momentum -- the higher the score, the more competitive activity the company is generating.

---

## Dimension Breakdown

### 1. Authority (0-25)
Baseline credibility and community validation.

| Signal | Max Points | Formula | Data Source |
|---|---|---|---|
| GitHub Stars | 15 | `min(15, (stars / 1000) * 3)` | GitHub search / API |
| GitHub Forks | 5 | `min(5, (forks / 200) * 2)` | GitHub search / API |
| Product Hunt Votes | 5 | `min(5, (votes / 100) * 5)` | PH search / API |

**Interpretation:**
- 5,000+ stars (15 pts): Established community-validated product
- 1,500-5,000 stars (5-14 pts): Growing traction
- <1,500 stars (<5 pts): Early stage or low community traction

### 2. Shipping (0-25)
Product velocity and development activity.

| Signal | Max Points | Formula | Data Source |
|---|---|---|---|
| Commits This Week | 10 | `min(10, commits * 2)` | GitHub search |
| Releases This Month | 5 | `5 if releases > 0 else 0` | GitHub releases |
| Actively Shipping | 5 | `5 if actively_shipping else 0` | Push recency + commit consistency |
| Days Since Last Activity | 5 | `5 if <7d, 3 if <30d, 0 otherwise` | Last push date |

**Interpretation:**
- 20+ pts: Shipping multiple times per week, very active
- 10-19 pts: Regular shipping cadence
- <10 pts: Infrequent or stalled development

### 3. Social (0-25)
Visibility, mindshare, and community buzz.

| Signal | Max Points | Formula | Data Source |
|---|---|---|---|
| Tweet Count (24h) | 5 | `min(5, tweets * 1)` | Twitter search / skill |
| Mention Count | 5 | `min(5, mentions * 2)` | Twitter search |
| Reddit Posts | 3 | `min(3, posts * 1.5)` | Reddit search / skill |
| Reddit Score | 2 | `min(2, (score / 100) * 2)` | Reddit search |
| HN Stories | 4 | `min(4, stories * 2)` | HN search / skill |
| HN Points | 3 | `min(3, (points / 200) * 3)` | HN search |
| YouTube / Video | 3 | `min(3, videos * 1)` | Web search |

**Interpretation:**
- 20+ pts: Significant social presence, possibly viral
- 10-19 pts: Consistent community engagement
- <10 pts: Low social footprint

### 4. Growth (0-25)
Expansion indicators -- hiring, sentiment, traction.

| Signal | Max Points | Formula | Data Source |
|---|---|---|---|
| Open Job Count | 10 | `min(10, jobs * 3)` | YC Jobs / careers page |
| Hiring Department Diversity | 5 | `min(5, dept_count * 2)` | YC Jobs / job listings |
| Community Sentiment (AI) | 5 | `min(5, (sentiment / 100) * 5)` | AI analysis of Reddit/HN/Twitter |
| Product Traction (AI) | 5 | `min(5, (traction / 100) * 5)` | AI analysis of signals |

**Interpretation:**
- 20+ pts: Rapidly scaling team, high market demand
- 10-19 pts: Measured growth, building team
- <10 pts: Early stage or steady state

---

## Activity Level Thresholds

| Heat Score | Activity Level | Color | Meaning |
|---|---|---|---|
| 60-100 | **High** | Red | Company is very active across multiple signals -- competitive threat |
| 30-59 | **Medium** | Yellow | Moderate activity, some channels active -- worth watching |
| 1-29 | **Low** | Blue | Minimal detectable activity -- low immediate threat |
| 0 | **Dormant** | Gray | No signals detected -- inactive or not found |

---

## Computation Rules

1. **Score each dimension independently**, then sum for final heat score (0-100)
2. Each dimension caps at **25 points** -- cannot overscore on one dimension
3. If a signal value is **unknown** (not found), score it as **0**
4. If ALL data for a dimension is missing, the dimension scores 0
5. **Never estimate or round up** -- use exact formulas with available data
6. A company with 0 on all dimensions is "Dormant" -- but still include in report

### Edge Cases

| Situation | Handling |
|---|---|
| No GitHub org found | Authority and Shipping score 0 for GH signals |
| Company is private (no GH) | Partial score from PH, Social, Growth dimensions only |
| No social handles found | Social dimension scores 0 |
| Not hiring / no job listings | Growth dimension scores 0 (no hiring is a signal too) |
| Only 1-2 channels have data | Score what you have, note data gaps in report |
| Multiple founders active on Twitter | Count all founder tweets combined, cap at Social max |

---

## Worked Example

**Company: Vercel**

| Dimension | Raw Data | Computed Score |
|---|---|---|
| Authority | 60k GH stars, 5k forks, 2k PH votes | 15 + 5 + 5 = **25/25** |
| Shipping | 45 commits/week, 8 releases/month, active daily | 10 + 5 + 5 + 5 = **25/25** |
| Social | 12 tweets/day, 30 mentions, 5 HN stories, 3 Reddit posts | 5 + 5 + 4 + 3 = **17/25** |
| Growth | 15 open jobs, 4 depts hiring, positive sentiment | 10 + 5 + 4 + 3 = **22/25** |
| **Total** | | **89/100 -- High** |
