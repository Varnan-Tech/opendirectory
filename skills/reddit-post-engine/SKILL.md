---
name: reddit-post-engine
description: Writes and optionally posts a Reddit post for any subreddit, following that subreddit's specific culture and rules. Drafts a title, body, and first comment using the 90/10 rule. Uses Composio Reddit MCP for optional direct posting. Use when asked to post on Reddit, draft a Reddit post, share a project on Reddit, write a subreddit post, or launch something on Reddit. Trigger when a user says "post this on Reddit", "write a Reddit post for r/...", "help me launch on Reddit", "draft something for Reddit", or "how do I share this on Reddit without getting banned".
author: OpenDirectory
version: 1.0.0
---

# Reddit Post Engine

Draft a Reddit post that fits the subreddit's culture. Optionally post it via Composio.

---

**Critical rule:** Never post without confirming subreddit rules. Never include product links in the body: put them in the first comment only if appropriate. Follow the 90/10 rule: your post should add value independent of any product mention.

**Anti-spam rule:** Posts that are primarily promotional will be removed and may get the account banned. The goal is to contribute to the community first. Product mentions go in the first comment, and only if the subreddit allows self-promotion.

---

## Step 1: Setup Check

```bash
echo "GEMINI_API_KEY: ${GEMINI_API_KEY:+set}"
# Check if Composio Reddit MCP is connected
claude mcp list 2>/dev/null | grep -i reddit || echo "Composio Reddit MCP: not connected"
```

**If GEMINI_API_KEY is missing:**
Stop. Tell the user: "GEMINI_API_KEY is required. Get it at aistudio.google.com. Add it to your .env file."

**If Composio Reddit MCP is not connected:**
Continue. The skill will draft posts but skip the posting step. Inform the user: "Composio Reddit MCP not connected: I'll draft your post for manual submission. To enable direct posting, see the setup instructions in README.md."

---

## Step 2: Gather Context

You need:
- Target subreddit (e.g., r/devops, r/startups, r/SideProject)
- What you are sharing (project, article, question, discussion, tool)
- One-sentence description of what it does
- Why it's relevant to this specific subreddit's community
- Whether you want a self-post (text) or link post

If any of these are missing, ask in one message:

"To draft your Reddit post, I need:
1. Which subreddit? (e.g., r/devops, r/startups)
2. What are you sharing? (project, article, tool, question)
3. What does it do? (one sentence, technical)
4. Why does this subreddit care about it specifically?"

---

## Step 3: Fetch Subreddit Rules and Culture

**Fetch the subreddit's rules:**
```bash
curl -s \
  -H "User-Agent: varnan-skills/1.0" \
  "https://www.reddit.com/r/{SUBREDDIT}/about/rules.json" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
rules = d.get('rules', [])
for r in rules:
    print(f'Rule: {r.get(\"short_name\", \"\")}')
    print(f'Detail: {r.get(\"description\", \"\")[:200]}')
    print()
"
```

**Fetch recent top posts to understand tone and style:**
```bash
curl -s \
  -H "User-Agent: varnan-skills/1.0" \
  "https://www.reddit.com/r/{SUBREDDIT}/top.json?t=week&limit=10" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
for p in d['data']['children'][:10]:
    pd = p['data']
    print(f'Score: {pd[\"score\"]} | Title: {pd[\"title\"][:100]}')
"
```

Note patterns in the top posts:
- Are titles questions or statements?
- Do they lead with the technology or the outcome?
- Are they personal ("I built...") or impersonal ("Tool for...")?
- What format gets the most engagement in this subreddit?

**Check subreddit sidebar for posting rules:**
```bash
curl -s \
  -H "User-Agent: varnan-skills/1.0" \
  "https://www.reddit.com/r/{SUBREDDIT}/about.json" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
data = d.get('data', {})
print('Public description:', data.get('public_description', '')[:300])
print('Subscribers:', data.get('subscribers', 0))
"
```

**Identify the subreddit type:**

| Type | Examples | Post style |
|------|----------|-----------|
| Technical practitioner | r/devops, r/sysadmin, r/ExperiencedDevs | Technical specifics, no fluff, "I did X and learned Y" |
| Startup/builder | r/startups, r/SideProject, r/indiehackers | Personal story, metrics, lessons learned |
| General tech | r/programming, r/technology | News angle, discussion hook, controversial take |
| Career | r/cscareerquestions, r/ITCareerQuestions | Question format, specific scenario, ask for experience |
| Niche tool | r/vim, r/rust, r/golang | Deep technical content, code examples, benchmarks |

Use the fetched rules and top posts to determine which style applies.

---

## Step 4: Draft the Post with Gemini

Write the post content to a temp file and call Gemini:

```bash
cat > /tmp/reddit-post-request.json << 'ENDJSON'
{
  "system_instruction": {
    "parts": [{
      "text": "You are a developer who is active in the {SUBREDDIT} community. Write a Reddit post that fits this subreddit's culture. Rules: (1) Write in first person if it is a project or experience post. (2) Do NOT include any product links in the body: links go in the first comment only. (3) The post must add genuine value to the community independent of any product being shared. (4) Match the tone of top posts in this subreddit: {SUBREDDIT_TONE_NOTES}. (5) Title max 300 characters. (6) Body 150-400 words for text posts. (7) No marketing language: no 'game-changing', 'powerful', 'robust', 'seamless', 'innovative'. (8) If the post is about a tool the user built, use the 'I made...' or 'I built...' opener: it performs best on Reddit. (9) Output: title on first line, blank line, then body. No labels, no commentary. Do not use em dashes."
    }]
  },
  "contents": [{
    "parts": [{
      "text": "POST_DETAILS_HERE"
    }]
  }],
  "generationConfig": {
    "temperature": 0.7,
    "maxOutputTokens": 1024
  }
}
ENDJSON

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/reddit-post-request.json \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['candidates'][0]['content']['parts'][0]['text'])"
```

Replace `POST_DETAILS_HERE` with:
- Subreddit name and type
- Top post patterns observed
- What is being shared and why it's relevant
- Key technical details
- Builder's honest motivation

---

## Step 5: Draft the First Comment

If the user has a product link or additional context to share, draft a first comment to post immediately after the post goes live.

The first comment serves two purposes:
1. Provide the link (which keeps the body link-free and feels less promotional)
2. Add context that would be too promotional in the post body

**First comment rules:**
- Post this as the first reply to your own post, immediately after it goes live
- Keep it under 100 words
- Example format: "Link for those who want to check it out: [URL]: also happy to answer questions about [specific technical thing mentioned in the post]."
- Only include the first comment if the subreddit allows self-promotion in comments
- If the subreddit has a "No self-promotion" rule, omit the link entirely

---

## Step 6: Self-QA

Check the draft before presenting:

**Structure:**
- [ ] Title does not exceed 300 characters
- [ ] No links appear in the post body
- [ ] Post opens in first person (for project/experience posts)
- [ ] At least one specific technical detail or concrete number included
- [ ] Post matches the tone of top posts observed in this subreddit (noted in Step 3)
- [ ] Subreddit rules from Step 3 are not violated

**Claude-ism detection: scan for these vocabulary categories and remove all instances:**

| Category | Words to remove |
|----------|----------------|
| Filler intensifiers | incredibly, absolutely, certainly, definitely, essentially, fundamentally, literally, particularly, quite, rather, really, significantly, simply, truly, ultimately, very |
| AI hedging | I should note, it's worth noting, it's important to note, as mentioned, as I noted |
| Hype descriptors | game-changing, revolutionary, powerful, robust, seamless, innovative, best-in-class, cutting-edge, groundbreaking, remarkable |
| Throat-clearing | In conclusion, in summary, to summarize, overall, first and foremost, last but not least |
| Unnecessary connectors | Furthermore, moreover, additionally, however (at sentence start), thus, hence, thereby |
| AI tells | This ensures that, This allows for, This helps to, This enables, delve, utilize, leverage, foster |

If any appear: replace with a specific noun, verb, or number. "Very fast" becomes "runs in 12ms". "Powerful tool" becomes what it actually does.

**Instant-delete phrase check: these patterns trigger Reddit spam filters or moderator removal:**

- Any sentence that reads as an advertisement ("Try [Product] today", "Sign up now", "Get started free")
- Phrases that imply you are not the builder ("I came across this great tool", "I found this amazing product")
- First-person possession of users ("our users", "our customers") in subreddits where you have not established community presence
- "I made X and you can use it to..." followed immediately by a link (promotional structure)
- Superlatives without qualification ("the best way to...", "the only tool that...")
- External links in post body (use first comment only)

If any instant-delete phrases appear: revise the sentence entirely, not just swap words.

---

## Step 7: Adversarial Review

Before presenting the final draft, run a 3-persona review. Each persona reads the post and finds ONE specific problem, quoting the exact text that triggers it.

**Persona 1: The Skeptical Practitioner**
This person has been in r/{SUBREDDIT} for years and has seen hundreds of product launches disguised as posts. Their read:
- Does any sentence feel promotional even if not explicitly selling?
- Does the post reveal genuine knowledge of the community's problems, or does it just talk about the product?
- Is there any claim that a practitioner would roll their eyes at?

State the one specific line they would flag and why.

**Persona 2: The Moderator**
This person enforces the rules fetched in Step 3. Their read:
- Does the post technically comply with subreddit rules?
- Is the ratio of self-promotion to community contribution acceptable?
- Would they have seen this exact post structure removed before?

State the one specific rule that is at risk of violation, or confirm it is clean.

**Persona 3: The Target Reader**
This is a non-builder community member who matches the subreddit's demographic. Their read:
- Would they upvote this post even if they never use the product?
- Is there a takeaway they can apply even if they skip the link in the first comment?
- Does the opening sentence make them want to keep reading?

State the one thing they would stop reading at, or confirm the post holds their attention.

After all three personas report: apply any fixes. If no persona found a problem, state "Adversarial review: clean."

---

## Step 8: Post via Composio (Optional)

If Composio Reddit MCP is connected and the user confirms they want to post:

```
Use the reddit-composio MCP tool REDDIT_CREATE_REDDIT_POST with:
- subreddit: {SUBREDDIT_WITHOUT_r/}
- title: {TITLE}
- kind: "self"
- text: {BODY}
```

**Before posting, confirm with the user:**
"Ready to post to r/{SUBREDDIT}. Post title: '{TITLE}'. Shall I go ahead?"

Only proceed after explicit confirmation.

**After posting:**
1. Note the post URL from the response
2. If a first comment was drafted, post it immediately using the same MCP with the returned post ID

**If posting fails (403, 429, or other error):**
Present the draft for manual submission. Tell the user: "Direct posting failed ([error code]). Here is your post for manual submission. Copy-paste the title and body at reddit.com/r/{SUBREDDIT}/submit."

---

## Step 9: Present Output

```
## Reddit Post: r/{SUBREDDIT}

### Title
{title}

### Body
{body}

### First Comment (post immediately after)
{first comment, if applicable}

---

### Submission Notes
- Post type: {self/link}
- Best time to post: {peak hours for this subreddit: weekday mornings US time for most tech subreddits}
- After posting: Reply to every comment in the first hour: early engagement signals quality to the algorithm
- Karma note: {If account is new, note that some subreddits require minimum karma before posting}
```

If the post was already submitted via Composio, replace the output block with:
```
Post submitted: {reddit_post_url}
```


