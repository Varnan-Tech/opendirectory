# Skill Integration Map

How to call each opendirectory skill for radar signal collection. Every channel has either a dedicated skill or a web search fallback.

---

## 1. GitHub Signal

### Primary: `gh-issue-to-demand-signal`
Use this skill when you need deeper demand signal analysis from GitHub Issues.

**Trigger phrase:** "Find demand signals from GitHub issues for [org/repo]"

**What it returns:** Clustered demand categories with scores, GTM messaging briefs, ranked issue list.

**Limitation:** This skill analyzes *issues*, not general repo health. For stars/forks/commits, use the web search fallback below.

### Fallback: Tavily Search
```text
github.com/[org] stars forks commits
```

**What to extract:** Total stars, forks, recent commits, releases, last push date, primary language, open issues.

### Data Points Collected

| Field | Source | Required? |
|---|---|---|
| total_stars | GitHub search / API | Yes |
| total_forks | GitHub search / API | Yes |
| commits_this_week | GitHub search (commits feed) | Yes |
| releases_this_month | GitHub releases tab | Yes |
| last_push_date | GitHub repo page | Yes |
| primary_language | GitHub repo page | Nice-to-have |
| open_issues | GitHub search / API | Nice-to-have |

---

## 2. Twitter/X Signal

### Primary: `twitter-GTM-find-skill`
Use this skill to scrape company and founder Twitter activity.

**Trigger phrase:** "Find GTM talent / activity on Twitter for [company/handle]"

**What it returns:** Tweet data, follower counts, activity patterns.

**Limitation:** This skill is optimized for finding GTM roles, not general social monitoring. For basic tweet counts, use Tavily search.

### Fallback: Tavily Search
```text
site:twitter.com [handle] OR site:x.com [handle]
```

**What to extract:** Recent tweet count, mentions, key topics/hashtags, engagement levels.

### Data Points Collected

| Field | Source | Required? |
|---|---|---|
| tweet_count_24h | Twitter search | Yes |
| mention_count | Twitter search | Nice-to-have |
| founder_tweet_activity | Founder handle search | Yes |
| key_topics | Tweet content analysis | Nice-to-have |

---

## 3. Reddit Signal

### Primary: `reddit-icp-monitor`
Use this skill to monitor Reddit for company mentions and sentiment.

**Trigger phrase:** "Monitor Reddit for [company name] mentions and sentiment"

**What it returns:** Ranked posts with ICP scores, pain point summaries, draft replies.

### Secondary: `reddit-post-engine`
Use when you need to understand subreddit culture around this company's space.

**Trigger phrase:** "Analyze Reddit posts about [company] in [subreddit]"

### Fallback: Tavily Search
```text
site:reddit.com [company name] [category]
```

**What to extract:** Post count, scores (upvotes), sentiment, subreddits, key thread titles.

### Data Points Collected

| Field | Source | Required? |
|---|---|---|
| mention_count | Reddit search | Yes |
| total_score | Sum of post scores | Yes |
| sentiment | Content analysis | Yes |
| top_threads | Reddit search | Nice-to-have |
| relevant_subreddits | Reddit search | Nice-to-have |

---

## 4. Hacker News Signal

### Primary: `hackernews-intel`
Use this skill to monitor HN for company mentions.

**Trigger phrase:** "Monitor Hacker News for [company name]"

**What it returns:** Matching HN posts with points, deduplicated against SQLite cache, Slack alerts.

**Setup required:** `HN_KEYWORDS` and `SLACK_WEBHOOK` environment variables. If not configured, use fallback.

### Fallback: HN Algolia API + Tavily
```text
site:news.ycombinator.com [company name]
```

Or direct Algolia API:
```text
https://hn.algolia.com/api/v1/search?query=[company]&tags=story
```

**What to extract:** Story count, total points, front-page stories, key discussion topics.

### Data Points Collected

| Field | Source | Required? |
|---|---|---|
| story_count | HN search / API | Yes |
| total_points | HN search / API | Yes |
| front_page_stories | HN search / API | Nice-to-have |
| top_stories | HN search | Nice-to-have |

---

## 5. Product Hunt Signal

### Primary: `producthunt-launch-kit`
Use this skill to research Product Hunt presence.

**Trigger phrase:** "Prepare a Product Hunt launch analysis for [company name]"

**What it returns:** Launch assets, taglines, post drafts, launch strategy.

### Fallback: Tavily Search
```text
site:producthunt.com [company name] products
```

**What to extract:** Recent launches, upvotes, comments, launch frequency.

### Data Points Collected

| Field | Source | Required? |
|---|---|---|
| recent_launches | PH search | Yes |
| total_votes | PH search | Yes |
| launch_frequency | PH search | Nice-to-have |
| recent_products | PH search | Nice-to-have |

---

## 6. YC Jobs Signal

### Primary: `yc-intent-radar-skill` / `yc-jobs-scraper`
Use this skill to scrape Y Combinator job listings.

**Trigger phrase:** "Scrape YC jobs for [company name]"

**What it returns:** Company slugs, job listings with IDs, deduplicated SQLite database, JSON export of radar candidates.

**Scripts available:**
```bash
cd scripts
node auth.js          # First-time auth (manual login)
node scraper.js       # Scrape all YC jobs
node export_radar_candidates.js  # Export targeted roles to JSON
```

### Fallback: Tavily Search
```text
site:workatastartup.com [company name] OR site:ycombinator.com/companies [company name]
```

**What to extract:** Open job count, job titles, departments, locations.

### Data Points Collected

| Field | Source | Required? |
|---|---|---|
| job_count | YC jobs search | Yes |
| job_titles | YC jobs search | Yes |
| department_breakdown | Job title analysis | Yes |
| locations | YC jobs search | Nice-to-have |

---

## 7. Web / Press Signal

### Primary: Tavily Search + `competitor-pr-finder`

Use Tavily search directly for press signals:
```text
[company name] funding announcement product launch 2026
```

For PR opportunity analysis, use `competitor-pr-finder`:
**Trigger phrase:** "Find PR opportunities for [company name]"

### Data Points Collected

| Field | Source | Required? |
|---|---|---|
| funding_rounds | Tavily search | Nice-to-have |
| product_launches | Tavily search | Nice-to-have |
| press_mentions | Tavily search | Nice-to-have |
| partnerships | Tavily search | Nice-to-have |

---

## 8. Pricing Signal (Optional)

### Primary: `pricing-finder`
Use this skill for detailed pricing research.

**Trigger phrase:** "Find pricing for [company name] competitors"

**What it returns:** Competitor pricing tiers, feature gate analysis, competitive positioning map, recommended strategy.

### Fallback: Tavily Search
```text
[company name] pricing plans 2026
```

### Data Points Collected

| Field | Source | Required? |
|---|---|---|
| pricing_tiers | Web search | Optional |
| plan_structure | Web search | Optional |
| free_tier_info | Web search | Optional |

---

## 9. Market Positioning (Optional Deep Dive)

### Primary: `map-your-market`
Use this skill for comprehensive market mapping.

**Trigger phrase:** "Map the market for [product category]"

**What it returns:** ICP definition, ranked pain themes with verbatim quotes, market size signals, messaging angles.

**Not a per-company tool -- use this to understand the broader competitive landscape, not an individual company.**

---

## Orchestration Pattern

When calling multiple skills in one radar run, use this parallel execution pattern:

```text
For each company in [company list]:
    PARALLEL:
        - Run GitHub research (web search or gh-issue-to-demand-signal)
        - Run Twitter research (web search or twitter-GTM-find-skill)
        - Run Reddit research (web search or reddit-icp-monitor)
        - Run HN research (web search or hackernews-intel)
        - Run PH research (web search or producthunt-launch-kit)
        - Run YC Jobs research (web search or yc-jobs-scraper)
        - Run Web/Press research (Tavily search)
    
    After ALL parallel tasks complete:
        - Compute heat score
        - Generate AI briefing
        - Add to report

Combine all company reports into single radar document.
```

**Never run channels sequentially.** All 8 channels are independent. Running them in sequence wastes 8x the time.
