# outreach-sequence-builder

<img width="1280" height="640" alt="outreach-sequence-builder" src="https://github.com/user-attachments/assets/3d73358a-52ca-48e7-b34e-b1ba33246d6e" />


Turn a buying signal into a ready-to-send multi-channel outreach sequence. Give the skill a signal and it generates 4-6 personalized touchpoints across email, LinkedIn, and phone, with objection pre-emption built in.

## Install

```bash
npx "@opendirectory.dev/skills" install outreach-sequence-builder --target claude
```

## What It Does

- Identifies the signal type from 7 categories: Post-Fundraise, Hiring Signal, Competitor Displacement, Product Launch, Content Engagement, Event Follow-up, Job Change
- Loads your ICP from docs/icp.md or asks 4 questions to define target persona and pain points
- Develops the Insight, Bridge, Opener, and Ask for the specific signal
- Plans a 4-6 touchpoint channel sequence over 10-14 days
- Generates all messages with Gemini, enforcing hard limits (100-word emails, 300-character LinkedIn notes, 20-word phone openers)
- Pre-empts 2-4 objections woven into existing touchpoints
- Runs a 13-point QA pass before presenting the sequence
- Saves the sequence to docs/sequences/ and optionally drafts emails in Gmail via Composio

## Requirements

| Requirement | Purpose | How to Set Up |
|------------|---------|--------------|
| Gemini API key | Sequence generation | aistudio.google.com, Get API key |
| Composio API key (optional) | Gmail draft creation | app.composio.dev, API Keys |

## Setup

```bash
cp .env.example .env
```

Fill in:
- `GEMINI_API_KEY` (required)
- `COMPOSIO_API_KEY` (optional, for Gmail draft creation)

Optional: create `docs/icp.md` with your target personas, company profile, pain points, and differentiators. If the file does not exist, the skill asks 4 questions before generating.

## How to Use

Basic sequence from a signal:

```
"Build an outreach sequence for a prospect who just raised a Series B"
"They're hiring 8 engineers — write me a sequence"
"Create outreach based on this signal: they just launched a new product"
```

With contact context:

```
"Build an outreach sequence for Sarah Chen, VP Sales at Momentum CRM — they just raised $22M Series B"
"They switched from Salesforce and posted a frustrated LinkedIn comment. Write a competitor displacement sequence."
```

With Gmail drafting:

```
"Build a post-fundraise sequence and draft the emails in Gmail"
```

## Signal Types

| Signal | Definition | Window |
|--------|-----------|--------|
| Post-Fundraise | Company raised a round in the last 30 days | 48 hours from announcement |
| Hiring Signal | Company posted 5 or more roles in a function you serve | Within the week posts appear |
| Competitor Displacement | Contact is using a competitor and showing frustration | Within 24 hours |
| Product Launch | Company launched a new product or major feature | 2-4 weeks after launch |
| Content Engagement | Contact liked, commented, or shared your content | Start on LinkedIn first |
| Event Follow-up | You met at a conference or webinar | Within 48 hours of event |
| Job Change | Contact moved to a new company in the last 60 days | Within 2 weeks of announcement |

## Message Rules

- Only `{{first_name}}` is allowed as a variable. All other details must be filled in from context.
- Email bodies: 100 words maximum.
- LinkedIn notes: 300 characters maximum.
- Phone openers: 20 words maximum.
- No placeholders like `[Company Name]` or `[INSERT PAIN POINT]`. If the information is not available, the skill asks before writing.

## Output

The sequence is saved to `docs/sequences/{signal-type}.md`. Each touchpoint includes:

- Channel and day number
- Two subject line variants (email)
- Message body
- Word count (email) or character count (LinkedIn)
- Phone talk track with voicemail script

## Project Structure

```
outreach-sequence-builder/
├── SKILL.md
├── README.md
├── .env.example
├── evals/
│   └── evals.json
└── references/
    ├── signal-playbook.md
    ├── sequence-format.md
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
