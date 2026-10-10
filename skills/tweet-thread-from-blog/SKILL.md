---
name: tweet-thread-from-blog
description: Converts a blog post URL or article into a Twitter/X thread with a strong hook, one insight per tweet, and a CTA. Optionally posts the full thread to X via Composio using a reply chain. Use when asked to turn a blog post into a tweet thread, repurpose an article for Twitter, create a thread from a blog, write a Twitter thread about a topic, or share a blog post as a thread. Trigger when a user mentions Twitter thread, X thread, tweet thread, or wants to repurpose blog content for X/Twitter.
author: OpenDirectory
version: 1.0.0
---

# Tweet Thread from Blog

Convert a blog post or article into a 7-10 tweet thread. One insight per tweet. Strong hook. CTA in the final tweet. Optionally post the thread directly to X via Composio.

## Writing Style

Apply these rules to every tweet you write:

- Active voice only
- Conversational, like a person typed it on their phone
- Contractions required: don't, it's, won't, can't, I've
- Short sentences, one idea per tweet
- No em dashes — use a period or comma instead
- No semicolons
- No markdown or asterisks
- No hashtags anywhere in the thread

Banned words — do not use any of these:
incredible, amazing, leveraging, synergize, game-changing, game changer, let's dive in, buckle up, it's worth noting, delve, harness, unlock, groundbreaking, cutting-edge, remarkable, paradigm, revolutionize, disruptive, transformative, thrilled, excited to share, powerful, innovative, comprehensive, actionable, crucial, vital, pivotal, elucidate, utilize, can, may, just, that, very, really, literally, actually, certainly, probably, basically, could, maybe

If a draft tweet contains any banned word, rewrite it before presenting.

## CRITICAL RULE

Do not invent specifics. Every claim, stat, and example in the thread must come from the blog post. Never fabricate data, quotes, or outcomes.

---

## Step 1: Check Setup

Confirm input is present. The user must provide one of:
- A blog post URL
- Pasted article text

If no input is present, ask: "What blog post or article should I turn into a thread? Share a URL or paste the content."

COMPOSIO_API_KEY is only needed for direct posting to X. Output-only mode works without it.

---

## Step 2: Fetch and Extract Content

**If input is a URL:**
Use WebFetch or Chrome DevTools MCP to fetch the page. Extract:
- Title
- Author name
- Publish date
- All body text
- Key statistics and data points
- Numbered lists or steps
- Subheadings
- Any quotes

**If input is pasted text:**
Read it directly.

After fetching, identify:
- The single most surprising or counterintuitive insight
- 6-9 supporting insights, data points, or steps
- Any specific numbers, percentages, or concrete results
- The core argument or main takeaway

QA checkpoint: State the core thesis and list the top insights you will use. Confirm every insight comes directly from the source. Do not proceed if you cannot verify a claim.

---

## Step 3: Choose Thread Style

Four styles. Auto-detect from content signals. Respect explicit user override.

| Style | When to Use | Signals |
|-------|-------------|---------|
| Data/Insight | Evidence-based article with stats or research findings | Numbers, percentages, study results, data points |
| How-To | Tutorial, guide, or step-by-step article | Numbered lists, step headers, "how to" in title |
| Story/Journey | Personal experience, build log, lessons learned | First-person narrative, "I learned", "we built" |
| Hot Take | Opinion piece, contrarian argument | "Why X is wrong", "Stop doing X", counterintuitive claim |

Decision logic:
- Article has specific stats or data: Data/Insight
- Article is structured as steps or tips: How-To
- Article is first-person narrative: Story/Journey
- Article argues against a common belief: Hot Take

State the chosen style and reason. If ambiguous, pick one and note it.

---

## Step 4: Read Format Rules

Read `references/thread-format.md` in full before writing any tweet. Internalize:
- Hook tweet rules (tweet 1 must stop the scroll)
- One-insight-per-tweet rule
- Character limit (280 per tweet, count carefully)
- Thread numbering format (1/8, 2/8, etc.)
- CTA tweet rules (final tweet only)
- No hashtags
- No em dashes
- Banned word list

Read `references/output-template.md` and select the template matching the chosen style.

---

## Step 5: Generate the Thread

Produce three things:

**(A) The full thread (7-10 tweets)**

Each tweet:
- Under 280 characters including the tweet number ("1/8 " = 4 characters)
- Contains exactly one insight, step, or idea
- Sounds like a human typed it
- No URLs in tweets 1 through N-1
- No hashtags

**(B) The CTA tweet (final tweet)**
- Summarizes the key takeaway in one sentence
- Ends with one action: "Read the full post in the replies." or "What's your take?" or "Follow for more like this."
- Includes the source URL if one was provided

**(C) One alternative hook tweet**
- Uses a different format from the primary hook
- If primary used a stat, offer a question-based hook
- If primary used a bold claim, offer a before/after hook

---

## Step 6: Self-QA

Run every check before presenting. Fix violations first.

- [ ] Tweet 1 creates a curiosity gap or leads with the most surprising insight
- [ ] Every tweet is under 280 characters (count including tweet number)
- [ ] Each tweet contains exactly one idea
- [ ] No tweet starts with "I" (exception: Story/Journey style)
- [ ] No banned words in any tweet
- [ ] No em dashes in any tweet
- [ ] No hashtags in any tweet
- [ ] No URLs except in the final CTA tweet
- [ ] No invented data. Every stat and example traces to the source.
- [ ] Thread reads naturally in sequence
- [ ] Total tweet count is between 7 and 10

State total tweet count and confirm every tweet is under 280 characters before presenting.

---

## Step 7: Post via Composio or Output

**Check for COMPOSIO_API_KEY.**

If set:
"Thread ready. Confirm to post to X via Composio, or say 'output only' to get the text."

On confirmation:
1. Post tweet 1 using action `TWITTER_CREATION_OF_A_POST` with `text` set to tweet 1 content
2. Capture the returned tweet ID
3. Post tweet 2 with `reply_in_reply_to_tweet_id` = tweet 1 ID, capture its ID
4. Continue for each tweet in sequence, each replying to the previous tweet's ID
5. Wait 1 second between posts to avoid rate limiting
6. After all tweets post: "Thread posted. Tweets 1-N are live."

If not set:
Present each tweet in a numbered list inside a code block. Add:

"To enable direct posting, add COMPOSIO_API_KEY to your .env file. See README.md for Composio setup."


