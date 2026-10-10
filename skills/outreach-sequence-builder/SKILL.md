---
name: outreach-sequence-builder
description: Takes a buying signal and generates a personalized multi-channel outreach sequence across email, LinkedIn, and phone. Outputs 4-6 ready-to-send touchpoints over 10-14 days. Optionally drafts email touchpoints via Composio Gmail. Use when asked to write an outreach sequence, build a sales cadence, create a follow-up sequence, personalize outreach for a signal, or generate cold outreach messages. Trigger when a user says "build an outreach sequence for", "write a sales cadence for", "create outreach based on this signal", "they just raised a round write me a sequence", or "generate personalized outreach for".
author: OpenDirectory
version: 1.0.0
---

# Outreach Sequence Builder

Take a buying signal. Generate a personalized multi-channel outreach sequence. Output ready-to-send messages across email, LinkedIn, and phone.

---

**Critical rule:** Every message must be filled in completely from the context you load. Only `{{first_name}}` is allowed as a variable. No `[Company Name]` brackets, no `[INSERT PAIN POINT]` placeholders. If you do not have the information to fill something in, ask before writing. Never send a message with an unfilled placeholder.

---

## Step 1: Setup Check

Confirm required env vars:

```bash
echo "GEMINI_API_KEY: ${GEMINI_API_KEY:+set}"
echo "COMPOSIO_API_KEY: ${COMPOSIO_API_KEY:-not set, Gmail drafting will be skipped}"
```

**If GEMINI_API_KEY is missing:**
Stop. Tell the user: "GEMINI_API_KEY is required. Get it at aistudio.google.com. Add it to your .env file."

**If COMPOSIO_API_KEY is missing:**
Continue. Sequences will be output as formatted text for copy-paste. Gmail draft creation is skipped.

---

## Step 2: Load Context

Check for an existing ICP file and account files:

```bash
ls docs/icp.md 2>/dev/null && echo "icp found" || echo "icp missing"
ls docs/accounts/ 2>/dev/null && echo "accounts found" || echo "accounts missing"
```

**If docs/icp.md exists:** Read it. Extract:
- Target personas (job titles, seniority, department)
- Company profile (size, industry, funding stage)
- Core pain points (use the buyer's exact language)
- Key differentiators (why your product over alternatives)

**If docs/accounts/{company}.md exists:** Read the relevant file. Extract:
- Company name, size, recent context
- Known tech stack or pain points
- Any existing relationship or prior contact

**If neither exists:** Ask the user these 4 questions. Do not proceed until all 4 are answered:
1. What does your product do? (one or two sentences)
2. Who are you targeting? (job title, company size, industry)
3. What is the main problem you solve? (from the buyer's perspective, not yours)
4. What is your key differentiator? (why you over the alternative they use today)

---

## Step 3: Identify the Signal

Determine which of the 7 signal types applies. Read `references/signal-playbook.md` for the full Insight, Bridge, Opener, and Ask for each signal type.

**7 signal types:**

| Signal | Definition |
|--------|-----------|
| Post-Fundraise | Company raised a funding round in the last 30 days |
| Hiring Signal | Company posted 5 or more roles in a function you serve |
| Competitor Displacement | Contact is using a competitor and showing frustration |
| Product Launch | Company launched a new product or major feature |
| Content Engagement | Contact liked, commented, or shared your content |
| Event Follow-up | You met or were in the same session at a conference or webinar |
| Job Change | Contact moved to a new company in the last 60 days |

**If the user provided a signal in their prompt:** Confirm the type and extract the specific details (round size, role titles, product name, event name, etc.).

**If no signal is clear:** Ask: "What triggered this outreach? (e.g. they raised a round, they're hiring engineers, you met at an event)"

State the detected signal type and the specific detail before proceeding.

---

## Step 4: Develop the Angle

Using the signal type and context loaded in Steps 2-3, define the four angle elements. Read `references/signal-playbook.md` for the formula for this signal type.

Write out explicitly before generating any messages:

```
Signal: [specific signal + concrete detail]
Insight: [what this signal reveals about their situation]
Bridge: [how your product connects to what the signal reveals]
Opener: [one sentence referencing the specific signal detail]
Ask: [minimum viable CTA, under 10 words]
```

The opener must name the specific trigger. Vague openers are rejected.

Good: "Congrats on the $18M Series B — scaling the sales team fast usually creates an onboarding gap."
Bad: "I saw your company recently raised funding."

---

## Step 5: Plan the Channel Sequence

Design 4-6 touchpoints across email, LinkedIn, and phone. Rules:

- Total duration: 10-14 days
- Minimum gap: 2 days between any two touches
- Never use the same channel twice in a row
- Each follow-up must add new value (new resource, new angle, new proof point). Never "just following up".
- The final touchpoint is a short breakup message

Default cadence for most signals:

```
Day 1:  Email (first touch, signal-led opener)
Day 3:  LinkedIn (connection note or short DM)
Day 7:  Email (new angle or case study)
Day 9:  Phone (talk track + voicemail script)
Day 12: Email (different framing or objection addressed)
Day 14: Email (short breakup message)
```

Adjust for signal type:
- Post-Fundraise: move faster (Day 1, 2, 4, 7, 10). Act within 48 hours of announcement.
- Event Follow-up: start with LinkedIn, not email (warmer channel first)
- Content Engagement: start with LinkedIn reply or comment before email

State the planned day and channel for each touchpoint before writing messages.

---

## Step 6: Generate the Sequence

Read `references/sequence-format.md` in full. Read `references/output-template.md` and select the template for this signal type.

Write the Gemini request to a temp file:

```bash
cat > /tmp/outreach-sequence-request.json << 'ENDJSON'
{
  "system_instruction": {
    "parts": [{
      "text": "You are a B2B sales copywriter who writes cold outreach that gets replies. Rules: The first sentence of every message is about THEM, not your company. Reference the specific buying signal by name and detail in the opening message. Use contractions naturally. Short sentences. No corporate jargon. No banned words: synergy, leverage, touch base, circle back, ping, loop in, alignment, innovative, cutting-edge, best-in-class, world-class, game-changing, disruptive, bandwidth, deep dive, low-hanging fruit, move the needle. No pleasantries: no 'I hope this email finds you well', no 'Happy Monday', no 'Just wanted to'. Each follow-up adds new value — never 'just following up'. Hard limits: email body under 100 words, LinkedIn note under 300 characters, phone opener under 20 words. Only {{first_name}} is allowed as a variable — fill in all other details from the context provided. The breakup message is short (3-4 sentences), friendly, and leaves the door open."
    }]
  },
  "contents": [{
    "parts": [{
      "text": "CONTEXT_AND_INSTRUCTIONS_HERE"
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
  -d @/tmp/outreach-sequence-request.json \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['candidates'][0]['content']['parts'][0]['text'])"
```

Replace `CONTEXT_AND_INSTRUCTIONS_HERE` with:
- The product description, target persona, pain points, and differentiators from Step 2
- The signal type, specific detail, and the four angle elements from Step 4
- The channel plan from Step 5
- Instructions to write each touchpoint with its subject line (email), character count (LinkedIn), and talk track (phone)

For each email touchpoint, require two subject line variants (A/B test).

---

## Step 7: Map Objections

After generating the sequence, identify the 2-4 most likely objections for this signal type. Pre-empt each one naturally within an existing touchpoint. Do not add separate objection-handling messages. Weave the pre-emption into the sequence.

Read the objection playbook in `references/sequence-format.md`. Map which touchpoint handles each objection.

**4 standard objections to pre-empt:**

| Objection | Pre-emption approach |
|-----------|---------------------|
| "We already have a solution" | Acknowledge their current tool, position yours as complementary or next step |
| "Not the right time" | Tie the signal directly to why now is the right time |
| "Too expensive" | Frame ROI, anchor to a number they care about |
| "Need to involve more people" | Offer a shareable resource (one-pager, recorded walkthrough) |

State which touchpoint handles each objection before presenting the final sequence.

---

## Step 8: Self-QA

Run every check and fix violations before presenting:

- [ ] Every message starts with a sentence about THEM
- [ ] The specific signal detail is named in at least the first touchpoint
- [ ] No unfilled placeholders except `{{first_name}}`
- [ ] Email bodies are under 100 words (count and state the word count for each)
- [ ] LinkedIn notes are under 300 characters (count and state for each)
- [ ] Phone opener is under 20 words
- [ ] No banned words in any message
- [ ] No "just following up" in any follow-up
- [ ] Each follow-up adds a new angle or value
- [ ] No same channel used twice in a row
- [ ] At least 2 objections pre-empted across the sequence
- [ ] Breakup message is 3-4 sentences, friendly, no guilt

Fix any violation before presenting.

---

## Step 9: Output and Save

Present the full sequence in a code block.

**Save to file:**
```bash
mkdir -p docs/sequences
cat > docs/sequences/SIGNAL-TYPE.md << 'EOF'
SEQUENCE_CONTENT_HERE
EOF
echo "Sequence saved to docs/sequences/SIGNAL-TYPE.md"
```

**If COMPOSIO_API_KEY is set:** Ask: "Draft the email touchpoints in Gmail via Composio?"

On confirmation, for each email touchpoint:
```bash
# The agent calls the GMAIL_CREATE_EMAIL_DRAFT Composio action
# with subject = [subject line], body = [email body], recipient = [contact email if known]
```

After drafting: "Email drafts created in Gmail. Check your Drafts folder."

**LinkedIn notes:** Present as separate copy-paste blocks with a clear label per touchpoint. LinkedIn does not support programmatic messaging.

**Phone scripts:** Present as a formatted talk track with bullet points, not a rigid script.


