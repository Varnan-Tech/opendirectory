---
name: noise2blog
description: Turns rough notes, bullet points, voice transcripts, or tweet dumps into a polished, publication-ready blog post. Optionally enriches with Tavily research to add supporting data and credibility to claims. Use when asked to write a blog post from notes, turn rough ideas into an article, expand bullet points into a full post, clean up a voice transcript into a blog, or repurpose a tweet thread as an article. Trigger when a user says "write a blog post from this", "turn these notes into a post", "expand this into an article", "make this publishable", "I have rough notes write a blog", or "clean up this transcript".
author: OpenDirectory
version: 1.0.0
---

# Noise to Blog

Take any rough input (bullet points, voice transcripts, tweet dumps, or short drafts) and produce a polished, publication-ready blog post. Every claim traces to the source material or Tavily-verified research.

---

**Critical rule:** DO NOT INVENT SPECIFICS. Every claim, metric, and example in the blog post must come from the raw input or a Tavily search result. Never fabricate data, quotes, or outcomes.

---

## Step 1: Setup Check

Confirm required env vars are set:

```bash
echo "GEMINI_API_KEY: ${GEMINI_API_KEY:+set}"
echo "TAVILY_API_KEY: ${TAVILY_API_KEY:-not set, Tavily enrichment will be skipped}"
```

**If GEMINI_API_KEY is missing:**
Stop. Tell the user: "GEMINI_API_KEY is required. Get it at aistudio.google.com → Get API key. Add it to your .env file."

**If TAVILY_API_KEY is missing:**
Continue. Note that Tavily enrichment will be skipped. The blog post will be based entirely on the provided content. This is fine for personal stories, tutorials from experience, or opinion pieces.

**Confirm input is present.**
The user must provide one of:
- Pasted text (bullet points, rough notes, transcript, tweet dump, short draft)
- A URL to fetch

If no input, ask: "Share your rough notes, bullet points, or transcript. Paste them directly, or give me a URL to fetch the source."

---

## Step 2: Read and Analyze Input

**If input is a URL:**
Fetch the page content using WebFetch. Extract: title, author, publish date, all body text, key statistics, numbered lists, subheadings, quotes.

**If input is pasted text:**
Read it directly. Identify the input type:
- **Bullet points or rough notes**: fragmented ideas, incomplete sentences, stream of consciousness
- **Voice transcript**: conversational, repetitive, filler words (um, uh, like, you know), meandering sentences
- **Tweet thread dump**: short fragments, @mentions, hashtags, "1/8" numbering
- **Short draft**: structured but thin, needs expansion and polish

**QA checkpoint:** State before continuing:
1. Input type detected
2. Core thesis or main argument in one sentence
3. The 3-5 strongest insights, facts, or ideas from the raw content
4. Any claims that need external verification (benchmarks, statistics, product comparisons, research findings)

If you cannot identify a core thesis, ask: "What's the single most important thing you want readers to take away from this?"

---

## Step 3: Choose Blog Post Style

Four styles. Auto-detect from content signals. User override always respected.

| Style | When to use | Signals |
|-------|-------------|---------|
| Technical Tutorial | Step-by-step guide, how-to, code walkthrough | Numbered steps, commands, code snippets, "how to" in content |
| Case Study | Before/after story, build log, lessons learned | Specific results, timelines, first-person journey |
| Thought Leadership | Opinion, argument, counterintuitive claim | "I think", "the problem with X", contrarian position, debate framing |
| Explainer | What is X, why it matters, how it works | Concept-first, comparison-heavy, "most people don't know" |

**Detection logic:**
- Content has numbered steps or commands → Technical Tutorial
- Content has before/after, specific metrics, or narrative arc → Case Study
- Content argues against common wisdom or makes a strong opinion claim → Thought Leadership
- Content explains a concept, tool, or trend for people unfamiliar with it → Explainer

State chosen style and reasoning. If ambiguous, pick one and note the choice.

---

## Step 4: Enrich with Tavily Research

Skip this step silently if TAVILY_API_KEY is not set.

Search for supporting evidence for claims in the raw content that could benefit from verification or data. Good candidates:
- Product benchmarks or performance numbers
- Market statistics or industry trends
- Technical comparisons ("X is faster than Y")
- Any number the user mentioned from memory rather than a cited source

Run one Tavily search per claim that needs verification. Limit to 3 searches maximum to avoid over-sourcing:

```bash
curl -s -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'"$TAVILY_API_KEY"'",
    "query": "SPECIFIC_CLAIM_OR_TOPIC",
    "search_depth": "advanced",
    "max_results": 5,
    "include_answer": true
  }'
```

Keep results with `score >= 0.65`. Extract: title, url, content snippet.

**Rules for using Tavily results:**
- Use them to support or verify claims already present in the raw input. Never introduce entirely new claims from search results.
- Attribute sources naturally in the text: "according to [Source]", "data from [X] shows"
- If no Tavily result confirms a claim, leave the claim unverified rather than substituting an unrelated result

---

## Step 5: Generate the Blog Post

Read `references/blog-format.md` in full. Select the matching template from `references/output-template.md`. Internalize all rules before generating.

Write the Gemini request to a temp file to handle special characters safely:

```bash
cat > /tmp/noise2blog-request.json << 'ENDJSON'
{
  "system_instruction": {
    "parts": [{
      "text": "You are a tech writer who sounds like a real person. Rules: Active voice only. Short paragraphs, 1-3 lines max, then a blank line. Use contractions naturally (don't, won't, it's, can't, you're, they're). No em dashes — use a comma or period instead. No semicolons. Every sentence needs a concrete detail: a number, a tool name, a file name, a command, a result. No filler phrases: no 'In today's rapidly evolving', no 'Let's dive in', no 'It's worth noting', no 'In conclusion', no 'I hope this was helpful'. No banned words: incredible, amazing, leveraging, synergize, game-changing, groundbreaking, revolutionary, paradigm, cutting-edge, seamless, robust, unprecedented, delve, harness, utilize, transformative, disruptive, unlock, comprehensive, actionable, crucial, pivotal. Title must not start with I, My, or We. Open with a hook paragraph that does not announce the topic. Close with something actionable. Do not invent claims, metrics, or outcomes not present in the source material."
    }]
  },
  "contents": [{
    "parts": [{
      "text": "RAW_CONTENT_AND_INSTRUCTIONS_HERE"
    }]
  }],
  "generationConfig": {
    "temperature": 0.7,
    "maxOutputTokens": 4096
  }
}
ENDJSON
```

Replace `RAW_CONTENT_AND_INSTRUCTIONS_HERE` with:
- The raw input content
- The blog post style and structure instructions (from the selected template)
- Any Tavily research results gathered in Step 4
- Word target: 800-1,800 words

Post the request:

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/noise2blog-request.json \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['candidates'][0]['content']['parts'][0]['text'])"
```

Also produce:
- (B) A 1-2 sentence meta description for SEO preview text
- (C) One alternative title using a different hook angle

---

## Step 6: Self-QA

Run every check and fix violations before presenting:

- [ ] Title does not start with "I", "My", or "We"
- [ ] Title is specific and conversational (not "A Comprehensive Guide to X" or "The Ultimate Guide to Y")
- [ ] Opening paragraph hooks without announcing the topic ("In this post I will...")
- [ ] No em dashes in any line
- [ ] No semicolons
- [ ] No paragraph longer than 3 lines before a blank line
- [ ] No banned words: incredible, amazing, leveraging, game-changing, delve, harness, unlock, groundbreaking, cutting-edge, remarkable, paradigm, revolutionize, seamless, robust, utilize, unprecedented, comprehensive, actionable, crucial, pivotal
- [ ] No invented data: every claim traces to the raw input or a Tavily result
- [ ] Post does not end with "In conclusion", "To summarize", or "I hope this helped"
- [ ] 800-1,800 words (state the word count)
- [ ] Logical flow: opening → problem/context → body sections → actionable close

Fix any violation before presenting. State the final word count.

---

## Step 7: Output

Present the full blog post in a code block.

Present the meta description and alternative title below the main post.

Ask: "Ready to copy this to your editor? If you're publishing to a specific platform, let me know and I can format the frontmatter."

**On platform-specific request:**

Ghost:
```yaml
---
title: "POST_TITLE"
date: YYYY-MM-DD
tags: [tag1, tag2]
status: draft
---
```

dev.to:
```yaml
---
title: POST_TITLE
description: META_DESCRIPTION
tags: [tag1, tag2, tag3]
published: false
---
```

Substack: Present as plain Markdown. Substack's editor imports markdown directly.

Hashnode:
```yaml
---
title: POST_TITLE
subtitle: META_DESCRIPTION
tags: [tag1, tag2]
---
```


