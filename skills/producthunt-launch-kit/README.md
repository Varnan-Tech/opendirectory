# producthunt-launch-kit

<img width="1280" height="640" alt="producthunt-launch-kit" src="https://github.com/user-attachments/assets/dc16bde9-9bc4-4022-94a8-a4db024cbd95" />


Generates a complete Product Hunt launch kit from your product description: tagline variants (60 chars max), listing description, maker comment, launch day tweet thread, LinkedIn post, and a 4-email sequence.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install producthunt-launch-kit --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fproducthunt-launch-kit&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Does

- Generates 5 tagline variants with character counts (all under 60 chars)
- Writes a listing description under 500 characters
- Drafts a maker comment (300-400 words) that opens with the builder story, not "Hi PH!"
- Creates a launch day tweet thread (5-7 tweets, no hashtags)
- Writes a LinkedIn post for launch day
- Generates a 4-email sequence: existing users, newsletter, day-of reminder, follow-up
- Includes a launch checklist with timing and community guidelines

## Requirements

| Requirement | Purpose | How to Set Up |
|------------|---------|--------------|
| Gemini API key | All copy generation | aistudio.google.com, Get API key |

## Setup

```bash
cp .env.example .env
# Add GEMINI_API_KEY
```

## How to Use

Full launch kit:
```
"Generate a Product Hunt launch kit for my product"
"Prepare my PH listing and launch copy"
"Help me launch on Product Hunt"
```

Specific assets:
```
"Write my Product Hunt tagline for [product description]"
"Draft a maker comment for my PH launch"
"Write PH launch tweets"
```

From README:
```
"Generate a Product Hunt kit: my README is in this repo"
```

## Copy Constraints

| Asset | Limit | Notes |
|-------|-------|-------|
| Tagline | 60 chars | Hard limit, enforced by PH form |
| Description | 500 chars | Appears in search and email digests |
| Maker comment | 300-400 words | Post within 60 seconds of launch |
| Tweets | 280 chars each | No hashtags on technical threads |

## Maker Comment Strategy

The maker comment drives more PH success than any other single action. It should:

- Open with the real builder story (not "Hi PH! We're excited to announce...")
- Include at least one technical detail about how it works
- Acknowledge what the product does NOT do
- End with a specific question that invites comments

The comment goes live as your first reply to your own listing, within 60 seconds of the product going live at 12:01 AM PST.

## Launch Timing

Best days: Tuesday, Wednesday, Thursday

Avoid: Friday afternoons, holiday weeks, major tech conference days

The first 4 hours determine front page placement. Notify your audience before midnight PST on launch day so they are ready.

## Project Structure

```
producthunt-launch-kit/
├── SKILL.md
├── README.md
├── .env.example
├── evals/
│   └── evals.json
└── references/
    └── copy-rules.md
```

## License

MIT
