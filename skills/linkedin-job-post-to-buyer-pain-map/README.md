# linkedin-job-post-to-buyer-pain-map

<img src="cover.png" width="100%" alt="LinkedIn Job Post to Buyer Pain Map — Signal Decoder for GTM Teams" />

Turn LinkedIn job posts into an actionable buyer pain map with signal strength, urgency, and outreach angles for each account.

## What It Does

- Parses 1–15 pasted job descriptions and groups them by company
- Extracts team, seniority, responsibility emphasis, requirement language, and tool/stack hints from each post
- Infers primary and secondary operational pains with cited evidence from the job text
- Scores each account on 3 dimensions: signal strength (1–10), urgency (1–10), ICP fit (1–10)
- Computes an overall priority score (10–100) using a transparent weighted formula
- Determines buy-vs-build posture and company stage from hiring language
- Generates 1–3 actionable outreach angles per account with talk-track bullets
- Produces a structured handoff object ready for `outreach-sequence-builder` consumption

## Requirements

| Requirement | Purpose | How to Set Up |
|------------|---------|--------------|
| Gemini API key | Signal analysis, scoring, and pain inference | aistudio.google.com → Get API key |

## Setup

```bash
cp .env.example .env
```

Fill in `GEMINI_API_KEY` (required).

No other dependencies. The skill runs entirely through agent instructions and Gemini API calls.

## How to Use

Analyze a single job post:

```
"Analyze this job post for buyer pain. My product is [X]. ICP: [Y]. Here's the post: [paste job description]"
```

Batch analysis of multiple posts:

```
"Build a pain map from these 5 job posts. Product: [X]. ICP: [Y]. Posts: [paste all posts]"
```

Focus on positioning angles:

```
"Decode these hiring descriptions for positioning angles. Focus on positioning. Product: [X]. ICP: [Y]. Posts: [paste posts]"
```

Handoff to outreach:

```
"Analyze these job posts and give me a handoff I can pass to outreach-sequence-builder"
```

## Input Format

Each job post should include at minimum:
- **Company name** and **job title** (required)
- **Job description text** — the full pasted content (required)
- Location, seniority, team/function, URL (optional — inferred if missing)

Posts can be pasted as plain text, numbered lists, or structured JSON objects.

## Output

For each company analyzed, the skill produces:

1. **Summary** — headline, overall score, score breakdown with explanations, stage guess, buy-vs-build posture
2. **Buyer Pain Map** — primary and secondary pains, each with label, description, and cited evidence
3. **Outreach Angles** — 1–3 angles with narrative and talk-track bullets
4. **Handoff** — structured block for outreach-sequence-builder (account summary, key pain, personas, tone)

Reports are saved to `docs/pain-maps/` as dated markdown files.

## Scoring Model

| Dimension | Weight | Measures |
|-----------|--------|----------|
| Signal Strength | 40% | Density and specificity of relevant hiring signals |
| Urgency | 30% | Time-sensitivity indicators in the job text |
| ICP Fit | 30% | Company profile match to user's ICP description |

**Overall Score** = `round((0.4 × signal + 0.3 × urgency + 0.3 × icp_fit) × 10)` → 10–100 scale.

See `references/scoring-rubric.md` for full scoring rules and modifiers.

## Plays Well With

| Skill | How |
|-------|-----|
| `outreach-sequence-builder` | Feed the handoff block as input context to generate a multi-channel outreach sequence |
| `noise-to-linkedin-carousel` | Use primary pains and evidence quotes as content source material |
| `reddit-icp-monitor` | Cross-reference pain themes from job posts with Reddit discussions |

## When NOT to Use

- Need to **find** companies hiring → use `linkedin-hiring-intent-scanner` or `yc-intent-radar-skill`
- Need to **write** outreach messages → use `outreach-sequence-builder`
- Need to **monitor** platforms for signals → use `reddit-icp-monitor` or `twitter-GTM-find-skill`
- Need contact data or email enrichment → this skill does not provide that

## Project Structure

```
linkedin-job-post-to-buyer-pain-map/
├── SKILL.md
├── README.md
├── .env.example
├── cover.png
├── evals/
│   └── evals.json
└── references/
    ├── scoring-rubric.md
    └── examples.md
```

## License

MIT

## Installation in Claude Desktop App

### Video Tutorial
Watch this quick video to see how it's done:

https://github.com/user-attachments/assets/ee98a1b5-ebc4-452f-bbfb-c434f2935067

### Step 1: Download the skill from GitHub
1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

### Step 2: Install the Skill in Claude
1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** (plus) icon button to create a new skill.
4. Choose the option to **Upload a skill**, and drag and drop the `.zip` file (or you can extract it and drop the folder, both work).

> **Note:** Always make sure you are uploading the specific folder that contains the `SKILL.md` file!
