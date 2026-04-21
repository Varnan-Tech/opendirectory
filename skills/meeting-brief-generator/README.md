# meeting-brief-generator

<img width="1280" height="640" alt="meeting-brief-generator" src="https://github.com/user-attachments/assets/30026bc4-657a-4ce9-8c0e-4dd2654783f8" />


Walk into every sales or business development call prepared. Give the skill a company name and it runs targeted research, synthesizes a 1-page brief, and optionally saves it to Notion.

## Install

```bash
npx "@opendirectory.dev/skills" install meeting-brief-generator --target claude
```

## What It Does

- Runs 6-8 targeted Tavily searches covering company overview, recent news, tech stack, product, competitors, funding, and contact background
- Synthesizes results into a structured 1-page brief using Gemini
- Every claim cites a source URL from the research
- Optionally saves the brief to a Notion database
- Handles low-data companies by marking gaps instead of inventing content

## Requirements

| Requirement | Purpose | How to Set Up |
|------------|---------|--------------|
| Tavily API key | Company research | app.tavily.com, API Keys |
| Gemini API key | Brief synthesis | aistudio.google.com, Get API key |
| Notion token (optional) | Saving briefs | notion.so/my-integrations |

## Setup

```bash
cp .env.example .env
```

Fill in:
- `TAVILY_API_KEY` (required)
- `GEMINI_API_KEY` (required)
- `NOTION_TOKEN` and `NOTION_DATABASE_ID` (optional, for saving briefs)

## How to Use

Basic brief with company only:

```
"Prepare me for a meeting with Stripe next Tuesday"
"Generate a meeting brief for Vercel"
"Research Acme Corp before my call tomorrow"
```

With contact and meeting type:

```
"Prepare a discovery call brief for Linear. I'm meeting with the VP Engineering, Jordan Lee."
"Create a pre-call brief for Notion. Demo call on April 20."
```

Save to Notion:

```
"Generate a meeting brief for Figma and save it to Notion"
```

## Brief Sections

| Section | Content |
|---------|---------|
| Company Snapshot | What they do, size, funding stage, HQ |
| Recent News | Last 30 days, source URLs |
| Decision Maker | Name, title, background (if contact provided) |
| Tech Stack Signals | Tools spotted in job posts, blog, GitHub |
| Competitive Context | Who they compete with and how |
| Talking Points | Because/mention/to formula, 3-5 bullets |
| Open Questions | Company-specific discovery questions |

## Output Format

One page, under 400 words. Every claim has a source URL. Talking points follow the format: "Because [finding from research], mention [point] to [goal]."

## Project Structure

```
meeting-brief-generator/
├── SKILL.md
├── README.md
├── .env.example
├── evals/
│   └── evals.json
└── references/
    ├── brief-format.md
    └── output-template.md
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

> **Note:** For some skills (like `position-me`), the `SKILL.md` file might be located inside a subfolder. Always make sure you are uploading the specific folder that contains the `SKILL.md` file!
