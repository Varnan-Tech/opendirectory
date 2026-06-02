# meeting-brief-generator

<img width="1280" height="640" alt="meeting-brief-generator" src="https://github.com/user-attachments/assets/30026bc4-657a-4ce9-8c0e-4dd2654783f8" />


Walk into every sales or business development call prepared. Give the skill a company name and it runs targeted research, synthesizes a 1-page brief, and optionally saves it to Notion.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install meeting-brief-generator --target claude
```

### Option B: Claude Desktop App

<video src="https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c" controls width="100%"></video>

**Step 1: Download the skill from GitHub**

1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

**Step 2: Install in Claude**

1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** button to create a new skill.
4. Choose **Upload a skill**, then drag and drop the `.zip` file or extracted folder.

> **Note:** For some skills, the `SKILL.md` file might be located inside a subfolder. Always upload the specific folder that contains the `SKILL.md` file.

### Option C: Claude Code Native

Run these commands inside Claude Code:

```bash
/plugin marketplace add Varnan-Tech/opendirectory
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

### Option D: Manus AI

<video src="https://www.opendirectory.dev/ManusAI-one-click-installation-demo.webm" controls width="100%"></video>

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fmeeting-brief-generator&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


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
