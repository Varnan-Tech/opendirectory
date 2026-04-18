---
name: show-hn-writer
description: 'Draft a Show HN post backed by real HN performance data. Uses observed patterns from 250 top HN posts to maximise score.'
compatibility: [claude-code, gemini-cli, github-copilot]
author: Varnan / Paras Madan
version: 2.0.0
data-source: 250 top HN posts scraped April 18 2026
---

# Show HN Writer — Data-Backed Edition

This skill drafts HN posts using patterns extracted from 250 real top-ranking posts.
Every rule below comes from observed data, not convention.

---

## What the data says (internalize this before writing anything)

These are the findings from 250 top HN posts scraped April 18 2026. They override
any received wisdom about HN writing.

**Title length is the single strongest predictor of score.**
- Under 40 chars: avg 248 pts (n=82)
- 40–59 chars:    avg 192 pts (n=68)
- 60–79 chars:    avg 150 pts (n=91)
- 80+ chars:      avg 131 pts (n=9)
Default target: under 40 characters. Hard ceiling: 60.

**Body text does not affect score.**
90% of posts had no body. With-body avg: 189. Without-body avg: 193. Statistically
identical. A body is only worth writing if you have genuinely interesting technical
detail that won't fit in a title. Never write a body to pad credibility.

**Show HN prefix suppresses score.**
Show HN posts averaged 94 pts vs 186+ for plain statements. The label signals
"I want feedback on my thing" which triggers a more skeptical read. Only use "Show HN:"
when the project is genuinely novel. Always offer a plain-title alternative.

**First-person titles outperform anonymous statements.**
First-person ("I…", "My…", "We…"): avg 291 pts (n=9).
Plain statement: avg 186 pts (n=126).
If the builder's perspective is part of the story, lead with it.

**Questions generate comments more than upvotes.**
Question titles avg ratio of comments-to-score above 1.0×. Best for discussions,
not for raw score. Ask the user which they're optimising for before writing.

**Themes that consistently outperform:**
- Security / backdoor / breach stories: avg 308 pts
- Privacy / surveillance / data stories: avg 282 pts
- AI / LLM releases: avg 266 pts (42 posts — largest category)
- Open source releases: avg 485 pts (small n, but strong signal)

**The highest-scoring titles share one trait: they are stories, not topics.**
"Someone bought 30 WordPress plugins and planted a backdoor in all of them" — 1192 pts.
"Google broke its promise to me – now ICE has my data" — 1688 pts.
A topic is "WordPress plugin security". A story has an actor, an action, and stakes.

---

## Step 1: Ask the user one question before anything else

Before drafting, ask:

"Two quick questions:
1. Are you optimising for **score** (reach) or **comments** (discussion)?
2. What does the project do — one sentence, technical, no adjectives?"

Do not proceed until you have both answers.

---

## Step 2: Determine the right post type

Based on the project and goal, decide which format to use:

**Plain title (recommended default)**
No prefix. Just what it is or what happened. Highest avg score.
Use when: sharing a release, article, tool, or event.

**Show HN: prefix (use sparingly)**
Use only when: the project is a working demo, the builder is present to answer
questions, and the technical implementation is the interesting part.
Avg score is low (94), but it signals authenticity when the project is genuinely novel.
Always also draft a plain-title alternative for comparison.

**Ask HN: prefix**
Use when: the goal is discussion, not promotion. Avg engagement ratio > 1.0×.
Best for "who is using X?" or "should I do Y?" posts.

**Tell HN: prefix**
Whistleblowing, accountability, or disclosure. One data point at 819 pts.
Only use if the post is factual, verifiable, and the builder is named.

---

## Step 3: Draft the title

**The title is the entire post.** Treat the body as optional.

Rules derived from data:
- Target under 40 characters. Every 20 chars over that costs roughly 30 avg points.
- Write a story, not a category. Actor + action + stakes beats noun phrases.
- First person ("I…") adds ~100 pts avg vs plain statement when builder perspective matters.
- No marketing adjectives. Not "fast", "simple", "powerful", "lightweight" unless
  it is a literal spec (e.g. "35B-A3B" is a spec, "powerful" is not).
- Specificity beats generality. "30 WordPress plugins" beats "popular CMS plugins".
- Year in brackets signals classic worth reading: (2008), (1956). Use when linking
  older content that has aged well.
- En dash (–) for subtitle format: "Product Name – what it does". Not a hyphen (-).

Draft three variants:
1. Shortest possible (aim for under 35 chars) — strip everything non-essential
2. Story angle — actor + action + stakes
3. Technical angle — lead with the interesting engineering decision

Then apply the length test: count chars on each. Flag any over 60.

---

## Step 4: Decide whether to write a body

Ask yourself: does the technical implementation have a detail that cannot fit in
the title and that HN engineers would find genuinely interesting?

If yes: write a body (see Step 5).
If no: stop at the title. No body is better than a padded body.

The data shows bodies do not increase score. The only reason to write one is if
the implementation is interesting enough that engineers will ask "how does this work?"
and you want to pre-answer that.

---

## Step 5: Write the body (only if Step 4 said yes)

Structure — keep it tight:

**Line 1:** One sentence. What you built and why. First person.
Not "Introducing X." Not "X is a tool that." Just: "I built X because Y."

**Lines 2–4:** The real reason. Honest. Specific. Was it a problem you hit yourself?
Something frustrating at work? A curiosity? "I was annoyed that..." is better than
"Developers often struggle with...". The builder's voice is the point.

**Lines 5–8:** How it actually works. This is what HN reads for.
Name the specific technology choices. State the tradeoffs you made and why.
One interesting engineering decision is worth more than a feature list.

**Line 9:** Current state in one sentence. Open source? Free? Alpha? Solo?
How long you've been working on it.

**Line 10:** One closing sentence inviting feedback or questions.
"Happy to answer questions about the implementation." / "Criticism welcome."
Never ask for upvotes, shares, or sign-ups.

Hard rules:
- 150–300 words. Under 200 is usually better.
- First person throughout.
- No bullet points. No headers. No bold.
- No links in body. URL goes in the submission field.
- No marketing words: game-changing, revolutionary, powerful, robust, seamless,
  innovative, best-in-class, streamline, leverage, transform, cutting-edge.

---

## Step 6: Self-check before presenting

Run through this list. Fix anything that fails before outputting.

Title:
- [ ] Under 60 characters (count them)
- [ ] No marketing adjectives
- [ ] Is it a story or a topic? (story = better)
- [ ] First person if the builder's perspective adds something
- [ ] No exclamation marks

Body (if written):
- [ ] Opens with "I built…" or "For the past N months…"
- [ ] Contains at least one specific technology name or architecture decision
- [ ] Under 300 words
- [ ] No links
- [ ] Closes with feedback invitation, not call to action
- [ ] Zero marketing words (check the list in Step 5)

Post type:
- [ ] If using Show HN prefix: is a plain-title alternative also drafted?
- [ ] If goal is comments: is it a question or divisive framing?
- [ ] If goal is score: is it a statement, not a question?

---

## Step 7: Present output

Format exactly as follows. No commentary before or after.

```
## HN Post

### Recommended title
[title — the shortest, strongest variant]

### Alternative titles
1. [variant 2]
2. [variant 3]

---

### Body
[body text, or "Not recommended — title is sufficient." if Step 4 said no body]

---

### Notes
- Goal: [score / comments] — based on user's answer in Step 1
- Post type used: [plain / Show HN / Ask HN / Tell HN]
- Title length: [N chars]
- Best time to post: Tuesday–Thursday, 8–10 AM US Eastern
- After posting: respond to every comment in the first two hours
- Do not share the link elsewhere for 24 hours — HN penalises vote rings
```

---

## Step 8: Optional — scrape current top HN posts for context

If the user wants to check whether similar posts have been submitted recently,
or wants to see what is performing in their category right now, run the scraper:

```python
import requests
from concurrent.futures import ThreadPoolExecutor

HN_API = "https://hacker-news.firebaseio.com/v0"

def fetch_item(id_):
    try:
        r = requests.get(f"{HN_API}/item/{id_}.json", timeout=10)
        return r.json() if r.ok else None
    except Exception:
        return None

ids = requests.get(f"{HN_API}/topstories.json").json()[:250]
with ThreadPoolExecutor(max_workers=20) as ex:
    items = [i for i in ex.map(fetch_item, ids) if i]

# Filter by keyword relevant to the user's project
keyword = "YOUR_KEYWORD_HERE"
matches = [i for i in items if keyword.lower() in i.get("title","").lower()]

for i, item in enumerate(matches, 1):
    score = item.get("score", 0)
    title = item.get("title", "")
    by = item.get("by", "")
    print(f"{i:>2}. [{score:>4}pts] {title} — {by}")

print(f"\nTotal matching: {len(matches)}")
```

Use the results to:
- Check if a near-identical post was submitted in the last 48 hours (avoid duplication)
- See which title patterns are landing in this category right now
- Identify the score floor for this topic area

Results are also appended to hn_log.csv automatically if the full scraper is used.

---

## Reference: observed top performers from dataset

These are real posts from the top 250. Study the title patterns.

Score | Title
------|-------
1941  | Claude Opus 4.7
1688  | Google broke its promise to me – now ICE has my data
1244  | Qwen3.6-35B-A3B: Agentic coding power, now open to all
1192  | Someone bought 30 WordPress plugins and planted a backdoor in all of them
1141  | DaVinci Resolve – Photo
990   | Codex for almost everything
982   | Stop Flock
909   | A new spam policy for "back button hijacking"
893   | GitHub Stacked PRs
819   | Tell HN: Fiverr left customer files public and searchable
668   | I wrote to Flock's privacy contact to opt out of their domestic spying program
619   | Measuring Claude 4.7's tokenizer costs
561   | God sleeps in the minerals
503   | Want to write a compiler? Just read these two papers (2008)

Best Show HN titles (by score):
341  | Show HN: Smol machines – subsecond coldstart, portable virtual machines
199  | Show HN: PanicLock – Close your MacBook lid disable TouchID → password unlock
187  | Show HN: Every CEO and CFO change at US public companies, live from SEC
177  | Show HN: I made a calculator that works over disjoint sets of intervals
152  | Show HN: MacMind – A transformer neural network in HyperCard on a 1989 Macintosh

Highest comment-to-score ratios (for discussion-optimised posts):
1.91× | Why is IPv6 so complicated?
1.43× | Ask HN: Building a solo business is impossible?
1.20× | Ohio prison inmates built computers and hid them in ceiling
1.13× | Ask HN: Who is using OpenClaw?
1.05× | The future of everything is lies, I guess: Where do we go from here?
