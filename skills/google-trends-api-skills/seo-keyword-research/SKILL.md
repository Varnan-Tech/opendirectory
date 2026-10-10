---
name: seo-keyword-research
description: SEO keyword research workflow for blog generation using Google Trends data. Use when writing blog posts, planning content calendars, or optimizing articles for search engines. Finds breakout keywords, builds content structure, and generates SEO-optimized blog outlines targeting tech and developer audiences.
license: MIT
metadata:
  author: farizanjum
  version: "2.0"
  domain: tech-developer-blogs
allowed-tools: Bash(python:*) Bash(curl:*) Read
---

# SEO Keyword Research Skill

Find trending, high-opportunity keywords BEFORE writing blog content. This skill turns generic blog topics into SEO-optimized content that ranks.

## When to Use

- User asks to write a blog post or article
- User wants keyword research for a topic
- User needs a content calendar or content plan
- User wants to optimize existing content for SEO
- Any blog generation task for a tech/developer-focused audience

## Core Principle

**Always research keywords BEFORE generating blog content.**

```
BAD:  Write blog -> Hope it ranks -> Usually doesn't
GOOD: Research keywords -> Find breakout opportunity -> Write optimized blog -> Ranks well
```

## Keyword Priority System

When analyzing Google Trends RELATED_QUERIES results, prioritize keywords in this order:

### 1. Breakout Keywords — HIGHEST priority
- `formatted_value: "Breakout"` = 5000%+ growth
- Very low competition (trend is new)
- Use as PRIMARY blog keyword
- Create content IMMEDIATELY (first-mover advantage)

### 2. High-Growth Keywords — VERY HIGH priority
- `formatted_value: "+100%"` or higher
- Low to moderate competition
- Use as primary or strong secondary keyword
- Create content within 2-4 weeks

### 3. Moderate-Growth Keywords — HIGH priority
- `formatted_value: "+50%"` to `"+99%"`
- Moderate competition
- Use as secondary keywords in body content

### 4. Long-Tail Keywords — STRATEGIC priority
- Question-based queries (how, what, why, when, where)
- Low competition, high conversion
- Use as H3 headings — target featured snippets and voice search

### 5. Established Keywords — MODERATE priority
- Top queries with stable interest, high competition
- Use in body content, not as primary target

## SEO Research Workflow

### Step 1: Keyword Discovery (1 API call — REQUIRED)

Query `RELATED_QUERIES` with the user's blog topic:

```bash
curl -s "https://serpapi.com/search?engine=google_trends&q=USER_TOPIC&data_type=RELATED_QUERIES&date=today+3-m&api_key=$SERPAPI_KEY"
```

From the response, extract:
- **Breakout keywords** → candidate primary keywords
- **High-growth keywords** (+100%) → secondary candidates
- **Question-based queries** → H3 headings and featured snippet targets

Select the primary keyword:
1. First breakout keyword (if any)
2. Else first high-growth keyword
3. Else top query by score

### Step 2: Content Structure (1 API call — REQUIRED)

Query `RELATED_TOPICS` with the same topic:

```bash
curl -s "https://serpapi.com/search?engine=google_trends&q=USER_TOPIC&data_type=RELATED_TOPICS&date=today+3-m&api_key=$SERPAPI_KEY"
```

Extract topic titles from rising + top results. These become your H2 section headings (pick 3-5).

### Step 3: Trend Validation (1 API call — OPTIONAL)

Only if choosing between multiple candidate keywords or validating viability:

```bash
curl -s "https://serpapi.com/search?engine=google_trends&q=KEYWORD&data_type=TIMESERIES&date=today+12-m&api_key=$SERPAPI_KEY"
```

Compare recent 2-month average vs. earlier 2-month average. If recent > earlier, trend is rising — proceed. If declining, consider a different keyword.

### Step 4: Generate Blog Outline

Build the outline using this structure:

```
Title: [Primary Keyword] — [Benefit/Number] [Year]
  (max 60 characters, must include primary keyword)

Meta Description: (150-160 chars, primary + 1-2 secondary keywords)

# [H1 — same as or variation of title]

## Introduction (150 words)
  - Primary keyword in first 100 words
  - Hook with a problem or question
  - Preview what they'll learn

## [H2: Related Topic 1 from Step 2]
### [H3: Long-tail question from Step 1]
  Content answering the question (150-200 words)
### [H3: Another long-tail question]
  Content (150-200 words)

## [H2: Related Topic 2]
### [H3: Long-tail question]
### [H3: Long-tail question]

## [H2: Related Topic 3]
### [H3: Long-tail question]
### [H3: Long-tail question]

## Conclusion (100 words)
  - Summarize key points
  - Primary keyword mentioned once
  - Call-to-action

Target: 1500-2500 words total
```

## Keyword Placement Rules

| Location | Rule |
|----------|------|
| Title | Include primary keyword, max 60 chars |
| H1 | Same as title or slight variation |
| H2 headings (3-5) | Use related topics, natural language |
| H3 headings (8-12) | Use long-tail keywords, question format |
| First paragraph | Primary keyword in first 100 words |
| Body content | Primary keyword 1-2% density, secondary 0.5-1% |
| Conclusion | Primary keyword once |
| Meta description | Primary + 1-2 secondary, 150-160 chars |

**Never keyword-stuff.** Content must read naturally. Google penalizes unnatural repetition.

## Quality Checklist

Before generating the blog, verify:

- [ ] Found at least 1 breakout or +100% keyword (or justified using established keyword)
- [ ] Have 3-5 H2 topics from RELATED_TOPICS
- [ ] Have long-tail keywords for H3 headings
- [ ] Primary keyword is specific enough to rank for
- [ ] Blog structure follows the outline template above
- [ ] Meta description is written (150-160 chars)
- [ ] Target length is 1500-2500 words

If no breakout or high-growth keywords exist for the topic, inform the user that SEO opportunity is limited and suggest alternative angles or related topics that do have growth.

## Budget Awareness

**Free tier: 250 searches/month**

| Strategy | Calls/Blog | Monthly Capacity |
|----------|-----------|-----------------|
| Minimal (recommended) | 2 | 125 blogs |
| Standard | 3 | 83 blogs |
| Complete | 4 | 62 blogs |

Default to 2 calls (RELATED_QUERIES + RELATED_TOPICS). Only add TIMESERIES or GEO_MAP when specifically needed.

## Common Mistakes to Avoid

1. **Skipping research** — writing without checking trends misses breakout opportunities
2. **Ignoring breakout keywords** — using a generic term when a breakout variant exists
3. **Keyword stuffing** — repeating keywords unnaturally; keep density at 1-2%
4. **No long-tail keywords** — missing featured snippet and voice search opportunities
5. **Generic H2 headings** — always use RELATED_TOPICS data for section structure

## Example Script

For a complete working example, run:

```bash
python scripts/blog_seo_research.py "your blog topic"
```

See [scripts/blog_seo_research.py](scripts/blog_seo_research.py) for the implementation.

## References

- [references/keyword-placement-guide.md](references/keyword-placement-guide.md) — Detailed placement rules and examples
- [references/tech-blog-examples.md](references/tech-blog-examples.md) — Real-world examples for tech/developer blogs
