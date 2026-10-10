---
name: reddit-icp-monitor
description: Watches subreddits for people describing the exact problem you solve, scores their relevance to your ICP, and drafts a helpful non-spammy reply for each high-signal post. Use when asked to monitor Reddit for ICP signals, find prospects on Reddit, surface pain point posts, draft helpful Reddit replies, or scan subreddits for buying signals. Trigger when a user says "monitor Reddit for my ICP", "find people on Reddit who need my product", "scan subreddits for pain points", "draft Reddit replies for prospects", or "check Reddit for buying signals".
author: OpenDirectory
version: 1.0.0
---

# Reddit ICP Monitor

Watch subreddits for people describing the problem you solve. Score their relevance. Draft a helpful reply for each match.

---

**Critical rule:** Never invent post URLs, titles, or content. Every post in the output must come from a Reddit search result. Mark any section with no results as "No matches found." Never draft a reply to a post that was not returned by the search.

**Anti-spam rule:** Drafted replies must never mention your product or company name unless the post explicitly asks for tool recommendations. Sound like a practitioner, not a marketer.

---

## Step 1: Setup Check

```bash
echo "GEMINI_API_KEY: ${GEMINI_API_KEY:+set}"
echo "REDDIT_CLIENT_ID: ${REDDIT_CLIENT_ID:-not set, using public endpoints (10 RPM)}"
```

**If GEMINI_API_KEY is missing:**
Stop. Tell the user: "GEMINI_API_KEY is required. Get it at aistudio.google.com. Add it to your .env file."

**If Reddit credentials are missing:**
Continue. Use Reddit's public JSON endpoints (no auth required, 10 RPM limit). For most monitoring sessions of 3-6 subreddit searches, this is sufficient.

**If REDDIT_CLIENT_ID is set:**
Use OAuth for 60 RPM. Fetch a token first:
```bash
TOKEN=$(curl -s -X POST \
  -d "grant_type=password&username=$REDDIT_USERNAME&password=$REDDIT_PASSWORD" \
  --user "$REDDIT_CLIENT_ID:$REDDIT_CLIENT_SECRET" \
  -H "User-Agent: varnan-skills/1.0" \
  https://www.reddit.com/api/v1/access_token \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
```
Use `Authorization: Bearer $TOKEN` and `https://oauth.reddit.com` base URL for all subsequent requests.

---

## Step 2: Load ICP

Check for an existing ICP file:
```bash
ls docs/icp.md 2>/dev/null && echo "icp found" || echo "icp missing"
```

**If docs/icp.md exists:** Read it. Extract:
- `product`: one-sentence product description
- `pain_points`: list of pain point phrases (exact buyer language)
- `anti_keywords`: phrases that disqualify a post
- `subreddits`: list of subreddits to search

**If docs/icp.md does not exist:** Ask these 3 questions. Do not proceed until all 3 are answered:
1. What does your product do? (one sentence)
2. What subreddits does your ICP post in? (comma-separated, e.g. devops, startups, SaaS)
3. What pain point phrases should trigger a match? (3-5 phrases in your buyer's own words, e.g. "onboarding takes forever", "can't see why users churn")

After answers are collected, save to docs/icp.md in the canonical format from `references/icp-format.md`. Confirm: "ICP saved to docs/icp.md. It will be used automatically in future runs."

Read `references/icp-format.md` for the canonical format and examples of good vs bad pain point phrases.

---

## Step 3: Search Reddit

For each combination of subreddit and pain point phrase, run one search. Use public endpoints unless OAuth credentials are set.

**Without OAuth (public endpoint):**
```bash
curl -s \
  -H "User-Agent: varnan-skills/1.0" \
  "https://www.reddit.com/r/{SUBREDDIT}/search.json?q={PHRASE}&sort=new&t=week&limit=25&restrict_sr=true" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
posts = d.get('data', {}).get('children', [])
for p in posts:
    data = p['data']
    print(json.dumps({
        'id': data['id'],
        'title': data['title'],
        'body': data.get('selftext', '')[:600],
        'url': 'https://reddit.com' + data['permalink'],
        'score': data['score'],
        'comments': data['num_comments'],
        'subreddit': data['subreddit'],
        'created_utc': data['created_utc']
    }))
"
```

**With OAuth:**
Replace `https://www.reddit.com` with `https://oauth.reddit.com` and add `-H "Authorization: Bearer $TOKEN"`.

**URL-encode the phrase** before inserting into the query string:
```bash
ENCODED=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1]))" "{PHRASE}")
```

**Time window defaults:**
- Default: `t=week` (last 7 days)
- User says "today" or "last 24 hours": `t=day`
- User says "this month": `t=month`

**After all searches:**
- Collect all posts into one list
- Deduplicate by post ID. If the same post matches multiple phrases, keep it once and note all matching phrases.
- If a search returns 0 posts: note it and continue. Do not stop.

State the total candidate count before scoring: "Found X candidate posts across Y subreddits."

---

## Step 4: Score Relevance with Gemini

Write all candidate posts and the ICP context to a temp file, then score:

```bash
cat > /tmp/reddit-score-request.json << 'ENDJSON'
{
  "system_instruction": {
    "parts": [{
      "text": "You are a GTM analyst identifying Reddit posts where someone is experiencing the exact pain point that a specific product solves. For each post provided, output a JSON object with these fields: id (the post id), score (integer 1-5), reason (one sentence explaining the score). Scoring rubric: 5 = person clearly has the problem AND is actively seeking help or venting frustration about it; 4 = strong signal, problem is present but less explicit; 3 = possible match, uncertain; 2 = tangentially related but not the core pain; 1 = unrelated. Output only a JSON array of score objects. No commentary before or after the array."
    }]
  },
  "contents": [{
    "parts": [{
      "text": "POSTS_AND_ICP_CONTEXT_HERE"
    }]
  }],
  "generationConfig": {
    "temperature": 0.2,
    "maxOutputTokens": 2048
  }
}
ENDJSON
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/reddit-score-request.json \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['candidates'][0]['content']['parts'][0]['text'])"
```

Replace `POSTS_AND_ICP_CONTEXT_HERE` with:
- The product description and pain point phrases from Step 2
- Each candidate post: id, title, body snippet
- Anti-keywords from the ICP (Gemini should score these lower)

Keep only posts with score >= 4 for response drafting.

State: "X posts scored 4 or 5. Drafting replies."

If 0 posts score >= 4: output the zero-results message from Step 7 and stop. Do not draft empty replies.

---

## Step 5: Draft Replies with Gemini

Read `references/reply-rules.md` before drafting. Determine the post type for each high-scoring post (Mode 1, 2, or 3) and pass the mode to Gemini.

For each post scoring >= 4, draft a reply (maximum 5 replies per session):

```bash
cat > /tmp/reddit-reply-request.json << 'ENDJSON'
{
  "system_instruction": {
    "parts": [{
      "text": "You are a practitioner who has personally solved the exact problem being described in this Reddit post. Write a helpful reply that: (1) directly addresses what the person asked or is frustrated about, (2) shares a specific, useful insight from real experience, (3) does NOT mention any product, tool, or company by name unless the post explicitly asks for tool recommendations, (4) is 2-5 sentences, written in plain conversational prose with no headers or bullet lists, (5) optionally ends with a low-pressure invitation to continue the conversation. Do not use marketing language. Do not use these words: game-changer, best-in-class, streamline, transform, revolutionize, leverage, seamless, robust, comprehensive, innovative. Sound like a real person."
    }]
  },
  "contents": [{
    "parts": [{
      "text": "POST_CONTENT_AND_MODE_HERE"
    }]
  }],
  "generationConfig": {
    "temperature": 0.7,
    "maxOutputTokens": 512
  }
}
ENDJSON
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/reddit-reply-request.json \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['candidates'][0]['content']['parts'][0]['text'])"
```

Replace `POST_CONTENT_AND_MODE_HERE` with:
- The full post title and body
- The reply mode (Mode 1: venting/frustration, Mode 2: how-do-you-handle-X, Mode 3: tool recommendation)
- The product description (so Gemini knows what to avoid naming in Mode 1/2)
- If Mode 3: Gemini may name the product AND must name one alternative

---

## Step 6: Self-QA

Run every check and fix violations before presenting:

- [ ] No product name in any Mode 1 or Mode 2 reply
- [ ] No banned words in any reply: "game-changer", "best-in-class", "streamline", "transform", "revolutionize", "leverage", "seamless", "robust", "innovative"
- [ ] Every reply is 2-5 sentences (count and state)
- [ ] Each reply directly addresses the specific question or frustration in the post
- [ ] All URLs in the output are real Reddit URLs from the search results (not constructed or guessed)
- [ ] No more than 5 replies drafted in total
- [ ] Mode 3 replies mention at least one alternative (not just the product)
- [ ] If any subreddit returned 0 results across all keyword searches, flag it in the output

Fix any violation before presenting.

---

## Step 7: Output and Save

Present the full report:

```
## Reddit ICP Monitor — [YYYY-MM-DD]

**Subreddits monitored:** r/[subreddit1], r/[subreddit2]
**Time window:** Last 7 days
**Keywords searched:** [phrase1], [phrase2], [phrase3]
**Candidates found:** X posts
**High-signal matches (score 4-5):** Y posts

---

### Match 1 — Score [N]/5
**Post:** [title](url)
**Subreddit:** r/[subreddit] | [N] upvotes | [N] comments
**Signal quote:** "[relevant excerpt from post body]"
**Matched keyword:** [phrase]
**Post type:** Mode [1/2/3]

**Drafted reply:**
[reply text]

**Reply word count:** N words

---

[repeat for each match]

---

**Subreddits with 0 results:** [list any that returned nothing]
```

**If 0 posts scored >= 4:**
"No high-signal matches found in the last 7 days across [subreddits]. Keywords searched: [list]. Try widening the time window (run again and say 'last month') or broadening your pain point phrases in docs/icp.md."

**Save to file:**
```bash
mkdir -p docs/reddit-intel
OUTFILE="docs/reddit-intel/$(date +%Y-%m-%d).md"
cat > "$OUTFILE" << 'EOF'
REPORT_CONTENT_HERE
EOF
echo "Saved to $OUTFILE"
```


