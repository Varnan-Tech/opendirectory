# show-hn-writer

<img width="1280" height="640" alt="show-hn-writer" src="https://github.com/user-attachments/assets/224030e0-c3e0-499c-98d4-a049d7dddc51" />


Draft a Show HN post (title + body) that follows Hacker News norms: specific, honest, first-person, no marketing. Generates three title variants and a complete body, then runs a Gemini review to catch HN anti-patterns before you post.

## Install

```bash
npx "@opendirectory.dev/skills" install show-hn-writer --target claude
```

## What It Does

- Reads your project context (from README or your answers)
- Drafts three Show HN title variants in different formats
- Writes a 150-350 word body following HN community norms
- Uses Gemini to flag marketing language, vague descriptions, or other HN anti-patterns
- Runs a self-QA checklist before presenting output
- Includes submission notes (timing, first-comment strategy, resubmission rules)

## Requirements

| Requirement | Purpose | How to Set Up |
|------------|---------|--------------|
| Gemini API key (optional) | Automated draft review for HN anti-patterns | aistudio.google.com, Get API key |

The skill works without Gemini: it runs the manual self-QA checklist instead.

## Setup

```bash
cp .env.example .env
# Add GEMINI_API_KEY if you want automated review (optional)
```

## How to Use

From a README:
```
"Write a Show HN post for my project"
"Help me launch on Hacker News"
"Draft a Show HN for the project in this repo"
```

With explicit context:
```
"Write a Show HN post for [project name]: [what it does]. I built it because [reason]."
```

For a specific title format:
```
"Write a Show HN title for my CLI tool that converts JSON to TypeScript interfaces"
```

## Show HN Title Formats

| Format | Example | Best For |
|--------|---------|----------|
| Product-First | `Show HN: Datasette – Instantly publish SQLite databases to the web` | Single-function tools |
| Outcome-Focused | `Show HN: Jitsi – Group video calls without an account` | Tools replacing something painful |
| Technical-Angle | `Show HN: Bun – JavaScript runtime built in Zig` | Dev tools where the implementation matters |
| Experiment | `Show HN: Ink – React for command-line apps` | Projects challenging a convention |

## What Makes a Good Show HN Post

**Title:** 60-80 characters. Starts with "Show HN:". En dash separator. No adjectives.

**Body:** First-person. 150-350 words. At least one technical detail. Honest about limitations. Ends with an invitation for feedback, not a CTA.

**What kills HN posts:**
- Vague titles ("Show HN: I built a thing for developers")
- Marketing adjectives ("fast", "simple", "powerful")
- Asking for upvotes
- Body that reads like a product page

## Project Structure

```
show-hn-writer/
├── SKILL.md
├── README.md
├── .env.example
├── evals/
│   └── evals.json
└── references/
    ├── hn-rules.md
    └── title-formulas.md
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
