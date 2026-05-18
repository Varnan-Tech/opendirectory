---
name: producthunt-launch-kit
description: Use when the user asks to prepare a Product Hunt launch or generate Product Hunt listing assets. Generates tagline variants under 60 chars, a 500-char description, a maker comment, launch-day tweet thread, LinkedIn post, and a 4-email launch sequence.
compatibility: [claude-code, gemini-cli, github-copilot]
author: OpenDirectory
version: 1.0.0
---

# Product Hunt Launch Kit

Generate every asset you need for a Product Hunt launch: listing copy, maker comment, and day-one social posts.

---

**Critical rule:** Product Hunt taglines are maximum 60 characters. Descriptions are maximum 500 characters. Never make factual claims that cannot be verified. Never mention competitor names. Never say "free" unless the product is permanently free (not just a trial).

---

## Step 1: Gather Product Details

You need:

- Product name
- What it does (technical description, one sentence)
- Primary use case and target user
- Key differentiator from existing tools
- Pricing: free, freemium, paid (starting price)
- Open source: yes/no
- Launch date (for scheduling context)
- Any credentials, launch discount, or promo code to offer
- 2-3 things that make it worth upvoting (honest reasons, not marketing)

If any of these are missing, ask in one message before proceeding.

Also check for project context files:

```bash
ls README.md 2>/dev/null && echo "README found"
ls package.json 2>/dev/null && echo "package.json found"
```

If README.md exists, read the first 80 lines to extract product description and key features before asking questions.

---

## Step 2: Gallery Strategy

Product Hunt requires screenshots. Most listings fail because of weak or missing gallery images. Plan these before writing copy.

**Spec:** 1270×760px, PNG or JPG, max 8 images. The first image is the hero: it appears in feeds and cards.

**Five-position framework:**

| Position | Purpose | What to show |
|----------|---------|-------------|
| 1 (Hero) | First impression in feeds | Product in use, clean UI or terminal output, no text overlays |
| 2 (Feature demo) | Show the core action | The thing that makes the product click: the "aha" moment |
| 3 (Before/After) | Show the problem being solved | Split screen: messy/slow state vs. clean/fast state |
| 4 (Social proof) | Build credibility | A real quote, a stat, or a before/after metric from a real user |
| 5 (Technical differentiator) | Address skeptics | Architecture diagram, benchmark, or the unusual technical decision |

If the product is a CLI tool or library, screenshots of terminal output work well. Annotate with arrows pointing to the important part.

**Video (optional but high-impact):** A 60-90 second demo. Under 2 minutes. No voiceover required: screen capture with captions works.

Tell the user: "Plan [N] gallery images before launch day. The hero image (position 1) is the most important. Here's what to capture for each position: [list above, customized for this product]."

---

## Step 3: Generate Tagline Variants

The tagline appears directly under the product name on Product Hunt. It is the most read copy on your listing.

**Hard limits:**
- Maximum 60 characters (including spaces)
- No period at the end
- No hashtags
- Do not start with the product name
- No superlatives: "best", "fastest", "easiest", "most powerful"
- No questions

**Tagline formula:** `[Action verb] + [what it does] + [key differentiator]`

Generate five tagline variants:

1. **Outcome-first:** What the user achieves ("Ship docs without leaving your codebase")
2. **Problem-first:** Names the pain that is solved ("No more copy-pasting between Figma and code")
3. **Technical-angle:** For developer tools, lead with the tech ("SQLite to shareable web app in one command")
4. **Comparison-free alternative:** Positions without naming competitors ("Git-native code review that works inside VS Code")
5. **Plain-English:** No jargon, widest possible audience ("Turns any RSS feed into a daily email digest")

After generating, count characters for each. Flag any that exceed 60 characters and revise.

---

## Step 4: Write the Listing Description

The description appears below the tagline. Maximum 500 characters. It displays in search results and link previews.

**Structure:**
- Sentence 1: What it does and who it's for (specific)
- Sentence 2: The key feature or technical approach that makes it work
- Sentence 3 (optional): Pricing or availability

**Description rules:**
- 280-500 characters (shorter is fine; longer is truncated in previews)
- Present tense throughout
- No hype adjectives
- No "I": write in third person or imperative ("Turns your...", "Connects to...", not "I built...")
- No links (they do not render)
- If open source, say so: "Open source and self-hostable."

---

## Step 5: Write the Maker Comment

The maker comment is the most important driver of Product Hunt success. It is your first reply to your own post, posted within 60 seconds of launch.

**Hard limits:**
- 300-400 words
- Must be posted within 60 seconds of the product going live
- First-person, conversational
- Tell the origin story
- Acknowledge the obvious alternative and explain why you built this anyway
- End with a specific question to invite comments

**Structure:**

**Opening (2-3 sentences):** Why you built this. The real story: what frustrated you, what gap you noticed, what problem you kept hitting. No "I'm thrilled to announce."

**What it does (3-5 sentences):** Explain the core mechanic. What happens when someone uses it for the first time. Include one specific technical detail that shows you thought hard about the problem.

**Who it's for (2-3 sentences):** Describe the specific person who will get the most value. Not "everyone who needs X": a specific persona: "If you're a solo dev who deploys on Friday afternoons and dreads..." or "If you've ever spent 20 minutes explaining the same PR context to three different reviewers..."

**Honest caveat (1-2 sentences):** What it does NOT do. What is still rough. This builds trust and filters in the right early users.

**Call for feedback (1-2 sentences):** Ask a specific question. "We haven't figured out the right approach for [specific edge case]: would love to know how you've handled it." or "The thing I'm most unsure about is [X]: does that matter to you?"

---

## Step 6: Generate All Assets with Gemini

Write all assets in one Gemini call:

```bash
cat > /tmp/ph-launch-request.json << 'ENDJSON'
{
  "system_instruction": {
    "parts": [{
      "text": "You are writing Product Hunt launch copy. Generate all assets in sequence, clearly labeled. Rules: taglines max 60 chars, description max 500 chars, maker comment 300-400 words first-person. No marketing words: 'revolutionary', 'game-changing', 'powerful', 'robust', 'seamless', 'innovative', 'best-in-class', 'streamline'. No competitor names. No superlatives in taglines. Do not use em dashes. For social posts: tweets max 280 chars, no hashtags in tweet threads (they reduce signal quality on technical posts). LinkedIn post 150-300 words, professional but not stiff. Email sequence: 4 emails, each under 150 words, subject line under 50 chars. Output each asset with a clear header. No commentary between sections."
    }]
  },
  "contents": [{
    "parts": [{
      "text": "PRODUCT_DETAILS_HERE"
    }]
  }],
  "generationConfig": {
    "temperature": 0.7,
    "maxOutputTokens": 4096
  }
}
ENDJSON

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/ph-launch-request.json \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['candidates'][0]['content']['parts'][0]['text'])"
```

Replace `PRODUCT_DETAILS_HERE` with all gathered context: product name, description, use case, differentiator, pricing, and any maker notes from Step 1.

Request these assets in the prompt:
1. Five tagline variants (with character counts)
2. Listing description (with character count)
3. Maker comment (300-400 words)
4. Tweet thread for launch day (5-7 tweets, 280 chars each)
5. LinkedIn post (150-300 words)
6. Email sequence (4 emails: existing users, newsletter, day-of reminder, follow-up)

---

## Step 7: Self-QA

Before presenting:

**Taglines:**
- [ ] All under 60 characters (count each)
- [ ] None start with the product name
- [ ] None contain superlatives
- [ ] None contain marketing words

**Description:**
- [ ] Under 500 characters (count)
- [ ] Third person or imperative voice (no "I")
- [ ] No links

**Maker comment:**
- [ ] 300-400 words (count)
- [ ] Opens with the real origin story (not "I'm excited to...")
- [ ] Includes one honest caveat
- [ ] Ends with a specific question
- [ ] No marketing language
- [ ] No em dashes

**Tweet thread:**
- [ ] Each tweet under 280 characters (count)
- [ ] No hashtags
- [ ] First tweet is the hook: most compelling thing about the product

If any item fails, revise before presenting. Do not present drafts with QA failures.

---

## Step 8: Present the Full Launch Kit

Present in this exact order:

```
## Product Hunt Launch Kit: [Product Name]

---

### Taglines (choose one)
1. [tagline]: [char count]
2. [tagline]: [char count]
3. [tagline]: [char count]
4. [tagline]: [char count]
5. [tagline]: [char count]

**Recommendation:** [one-sentence reason to prefer tagline X]

---

### Listing Description
[description text]
[char count] / 500

---

### Maker Comment (post within 60 seconds of launch)
[maker comment text]

---

### Launch Day Tweets
Tweet 1/6: [text]
Tweet 2/6: [text]
...

---

### LinkedIn Post
[post text]

---

### Email Sequence

**Email 1: Existing Users (send 1 week before)**
Subject: [subject]
[body]

**Email 2: Newsletter / Audience (send day before)**
Subject: [subject]
[body]

**Email 3: Day-of Reminder (send at 12:01 AM PST)**
Subject: [subject]
[body]

**Email 4: Follow-up (send 48 hours after launch)**
Subject: [subject]
[body]

---

### Self-Hunt vs. Top Hunter Decision

Answer these questions to decide:

| Question | Self-Hunt | Get a Hunter |
|----------|-----------|--------------|
| Do you have 500+ Twitter/LinkedIn followers in your target audience? | Yes | No |
| Does your product have an existing user base to rally? | Yes | No |
| Is your product technical and you have a personal brand in dev communities? | Yes | No |
| Is this your first launch with no audience yet? | No | Yes |
| Does a top hunter (500+ followers on PH) already use your product? | No | Yes |

If 3+ answers point to "Get a Hunter": reach out to hunters at least 2 weeks before launch day. Frame the ask as sharing something you built that they would genuinely want to know about: not asking for a favor.

---

### 30-Day Pre-Launch Preparation

**Day 30-21: Teaser Phase**
- [ ] Post a "building in public" update on Twitter/LinkedIn: what problem you are solving and why
- [ ] Identify 3-5 hunters with 500+ PH followers who match your product category
- [ ] Start building a supporter list (everyone who would upvote on launch day): team, users, investors, friends in tech
- [ ] Set up a simple "notify me on launch" page (even a TypeForm or Google Form)

**Day 20-8: Asset Phase**
- [ ] Capture all 5 gallery images at 1270×760px (see gallery strategy above)
- [ ] Record 60-90 second demo video if applicable
- [ ] Draft all copy from this kit: tagline, description, maker comment, social posts, emails
- [ ] Send Email 1 (existing users) at Day 8

**Day 7-2: Final Prep**
- [ ] Send Email 2 (newsletter) at Day 2
- [ ] Message your supporter list directly (Slack, DM, email): not a mass blast, personal messages
- [ ] Schedule tweet thread and LinkedIn post
- [ ] Do a dry run: check PH listing preview, verify all gallery images display correctly
- [ ] Confirm maker comment is under 400 words and saved somewhere you can paste instantly

**Day 1: Launch Day**
- [ ] Post goes live at 12:01 AM PST
- [ ] Send Email 3 (day-of reminder) immediately after going live
- [ ] Maker comment posted within 60 seconds of launch
- [ ] Tweet thread posted in the first 30 minutes
- [ ] LinkedIn post published
- [ ] Reply to every comment within 2 hours: PH algorithm rewards active makers
- [ ] Do not ask for upvotes directly: ask people to "check it out" or "share feedback"
- [ ] DM your supporter list with a direct link: not "go upvote" but "we just launched, would love your thoughts"
- [ ] First comment with any promo code posted within 5 minutes of launch

**Day 2: Follow-Up**
- [ ] Send Email 4 (48-hour follow-up) with results and thank-you
- [ ] Post a results update on Twitter/LinkedIn: upvotes, comments, lessons
- [ ] Reply to any overnight comments you missed

---

### Upvote Benchmarks

| Upvotes | Outcome |
|---------|---------|
| 50-100 | Listed but not front page |
| 200-400 | Competitive front page placement |
| 500-800 | Top 5 of the day |
| 800+ | Product of the Day |
| 1500+ | Product of the Week contender |

First-hour velocity matters more than final count. 100 upvotes in the first hour beats 400 spread over 24 hours.

---

### Hour-by-Hour Launch Day Timeline

| Time (PST) | Action |
|------------|--------|
| 12:01 AM | Post goes live. Do not schedule: be awake and click manually. |
| 12:02 AM | Maker comment posted (have it in clipboard, paste and submit immediately) |
| 12:05 AM | First comment (promo code or context) posted |
| 12:15 AM | Tweet thread live |
| 12:30 AM | LinkedIn post live |
| 12:30 AM | Personal DMs to your 10 most-engaged supporters |
| 1:00 AM | Check for first comments, reply to all |
| 7:00 AM | Morning US traffic peak. Check ranking. Reply to overnight comments. |
| 9:00 AM | Send Email 3 (day-of reminder) if you held it for morning send |
| 12:00 PM | Midday check. Reply to all comments. Post a "midday update" tweet if trending. |
| 5:00 PM | Evening US traffic peak. Final push to supporter list if needed. |
| 11:59 PM | Results final. Screenshot your placement. |

---

### Launch Checklist
- [ ] Post goes live at 12:01 AM PST on launch day (manual click, not scheduled)
- [ ] Maker comment copied to clipboard, posted within 60 seconds of launch
- [ ] Supporter list of 200+ people ready to message personally on launch day
- [ ] Gallery images and video (if any) uploaded and previewed before launch
- [ ] All 4 emails drafted and scheduled
- [ ] Reply to every comment on launch day: PH rewards active makers
- [ ] Do not ask for upvotes directly: ask people to "check it out" or "share feedback"
- [ ] First comment (with any promo code) posted within 5 minutes of launch
```




