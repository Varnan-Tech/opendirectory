---
name: meeting-brief-generator
description: Takes a company name and optional contact, runs targeted research via Tavily, synthesizes a 1-page pre-call brief with Gemini, and optionally saves it to Notion. Use when asked to prepare for a meeting, research a prospect before a call, generate a company brief, create a pre-call summary, or write a meeting prep doc. Trigger when a user says "prepare me for a meeting with", "research this company before my call", "generate a meeting brief for", "I have a call with X tomorrow", or "create a prospect brief for".
author: OpenDirectory
version: 1.0.0
---

# Meeting Brief Generator

Take a company name and optional contact. Research the company via Tavily. Synthesize a 1-page pre-call brief with Gemini. Optionally save to Notion.

---

**Critical rule:** DO NOT INVENT SPECIFICS. Every fact, number, and claim in the brief must come from a Tavily search result. Mark any section with no search data as "Limited public information found." Never fabricate funding amounts, employee counts, or product details.

---

## Step 1: Setup Check

Confirm required env vars:

```bash
echo "TAVILY_API_KEY: ${TAVILY_API_KEY:+set}"
echo "GEMINI_API_KEY: ${GEMINI_API_KEY:+set}"
echo "NOTION_TOKEN: ${NOTION_TOKEN:-not set}"
echo "NOTION_DATABASE_ID: ${NOTION_DATABASE_ID:-not set}"
```

**If TAVILY_API_KEY is missing:**
Stop. Tell the user: "TAVILY_API_KEY is required. Get it at app.tavily.com. Add it to your .env file."

**If GEMINI_API_KEY is missing:**
Stop. Tell the user: "GEMINI_API_KEY is required. Get it at aistudio.google.com. Add it to your .env file."

**If NOTION_TOKEN or NOTION_DATABASE_ID is missing:**
Continue. The brief will be output as text only. Notion saving is skipped.

**Confirm input is present.**
The user must provide at minimum a company name. If not provided, ask: "Which company are you meeting with?"

---

## Step 2: Gather Context

Collect the following. Ask only for what is missing.

Required:
- Company name (or domain/URL if provided)
- Meeting date

Optional (do not block if missing):
- Contact name and title
- Meeting type (discovery, demo, follow-up, QBR)
- Any specific topics or goals the user wants to cover

If the user provides a company URL or domain, use it to make Tavily queries more precise (e.g. `site:example.com` or include the domain in search terms).

---

## Step 3: Research with Tavily

Run these searches in sequence. Each targets one section of the brief. Save the top results from each (title, url, content snippet, score).

Keep results with score >= 0.5. If a search returns 0 qualifying results, mark that section as "Limited public information found."

**Search 1: Company overview**
```bash
curl -s -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'"$TAVILY_API_KEY"'",
    "query": "\"COMPANY\" overview founded employees headquarters",
    "search_depth": "advanced",
    "max_results": 5,
    "include_answer": true
  }'
```

**Search 2: Recent news (last 30 days)**
```bash
curl -s -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'"$TAVILY_API_KEY"'",
    "query": "\"COMPANY\" news announcement",
    "search_depth": "advanced",
    "max_results": 5,
    "include_answer": true,
    "topic": "news",
    "time_range": "month"
  }'
```

**Search 3: Tech stack**
```bash
curl -s -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'"$TAVILY_API_KEY"'",
    "query": "\"COMPANY\" technology stack engineering infrastructure tools",
    "search_depth": "advanced",
    "max_results": 5,
    "include_answer": true
  }'
```

**Search 4: Product and pricing**
```bash
curl -s -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'"$TAVILY_API_KEY"'",
    "query": "\"COMPANY\" product features pricing use case",
    "search_depth": "advanced",
    "max_results": 5,
    "include_answer": true
  }'
```

**Search 5: Competitors**
```bash
curl -s -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'"$TAVILY_API_KEY"'",
    "query": "\"COMPANY\" competitors alternatives vs",
    "search_depth": "advanced",
    "max_results": 5,
    "include_answer": true
  }'
```

**Search 6: Funding and growth**
```bash
curl -s -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'"$TAVILY_API_KEY"'",
    "query": "\"COMPANY\" funding raised valuation growth",
    "search_depth": "advanced",
    "max_results": 5,
    "include_answer": true
  }'
```

**If contact name is provided, run two more searches:**

**Search 7: Contact profile**
```bash
curl -s -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'"$TAVILY_API_KEY"'",
    "query": "\"CONTACT_NAME\" \"COMPANY\" role title",
    "search_depth": "advanced",
    "max_results": 5,
    "include_answer": true
  }'
```

**Search 8: Contact background**
```bash
curl -s -X POST "https://api.tavily.com/search" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'"$TAVILY_API_KEY"'",
    "query": "\"CONTACT_NAME\" background career LinkedIn",
    "search_depth": "advanced",
    "max_results": 5,
    "include_answer": true
  }'
```

---

## Step 4: Synthesize with Gemini

Read `references/brief-format.md` in full. Read `references/output-template.md` and use the template.

Write the Gemini request to a temp file:

```bash
cat > /tmp/meeting-brief-request.json << 'ENDJSON'
{
  "system_instruction": {
    "parts": [{
      "text": "You are a GTM research analyst preparing a 1-page pre-call brief for a sales or business development meeting. Rules: Every claim must cite a source URL from the provided research. Use the format 'Because [finding from research], mention [point] to [goal]' for talking points. No invented data. If a section has no research data, write 'Limited public information found.' No em dashes. No banned words. Under 400 words total. The brief must be scannable in 3 minutes."
    }]
  },
  "contents": [{
    "parts": [{
      "text": "RESEARCH_RESULTS_AND_INSTRUCTIONS_HERE"
    }]
  }],
  "generationConfig": {
    "temperature": 0.3,
    "maxOutputTokens": 2500
  }
}
ENDJSON
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/meeting-brief-request.json \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['candidates'][0]['content']['parts'][0]['text'])"
```

Replace `RESEARCH_RESULTS_AND_INSTRUCTIONS_HERE` with:
- All Tavily search results (title, url, content snippet per result)
- The brief template structure from output-template.md
- The company name, contact name (if provided), meeting date, meeting type (if provided)

---

## Step 5: Self-QA

Check before presenting:

- [ ] No invented data. Every fact has a source URL from Tavily results.
- [ ] Talking points use "Because [finding], mention [point] to [goal]" format
- [ ] No em dashes in any line
- [ ] No banned words
- [ ] Brief is under 400 words
- [ ] Decision Maker section says "Not specified" if no contact was provided
- [ ] Sections with no data say "Limited public information found" rather than guessing
- [ ] Open questions are specific to this company, not generic

Fix any violation before presenting.

---

## Step 6: Output or Save to Notion

Present the full brief in a code block.

If NOTION_TOKEN and NOTION_DATABASE_ID are both set, ask: "Save this brief to Notion?"

On confirmation:

```bash
cat > /tmp/notion-brief-payload.json << 'ENDJSON'
{
  "parent": { "database_id": "NOTION_DATABASE_ID_HERE" },
  "properties": {
    "Name": {
      "title": [{ "text": { "content": "Meeting Brief: COMPANY, DATE" } }]
    },
    "Date": {
      "date": { "start": "YYYY-MM-DD" }
    }
  },
  "children": [
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [{ "type": "text", "text": { "content": "BRIEF_CONTENT_HERE" } }]
      }
    }
  ]
}
ENDJSON
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d @/tmp/notion-brief-payload.json
```

After posting: "Brief saved to Notion. Check your database."

If Notion is not configured: present the brief only. Do not mention Notion.


