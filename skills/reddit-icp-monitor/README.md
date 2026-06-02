# reddit-icp-monitor

<img width="1280" height="640" alt="reddit-icp-monitor" src="https://github.com/user-attachments/assets/8182b73f-1f8d-4812-9061-165fd8aeb0e8" />


Watch subreddits for people describing the exact problem you solve. Score each post for ICP relevance. Draft a helpful, non-spammy reply for every high-signal match.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install reddit-icp-monitor --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Freddit-icp-monitor&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Does

- Reads your ICP definition from docs/icp.md (or asks 3 questions to build it)
- Searches specified subreddits for posts matching your pain point phrases
- Scores each candidate post 1-5 using Gemini (how clearly does this person have the problem you solve?)
- Drafts a helpful reply for every post scoring 4 or 5, in the correct mode (vent, how-do-you, or tool recommendation)
- Enforces a hard rule: replies never name your product unless the post explicitly asks for tool recommendations
- Saves the full report to docs/reddit-intel/YYYY-MM-DD.md

## Requirements

| Requirement | Purpose | How to Set Up |
|------------|---------|--------------|
| Gemini API key | Relevance scoring and reply drafting | aistudio.google.com, Get API key |
| Reddit credentials (optional) | Higher rate limit (60 RPM vs 10 RPM) | reddit.com/prefs/apps, create a script app |

Reddit credentials are optional. The skill uses Reddit's public JSON endpoints by default, which require no setup and support 10 RPM. That is enough for most monitoring sessions.

## Setup

```bash
cp .env.example .env
```

Fill in:
- `GEMINI_API_KEY` (required)
- Reddit credentials (optional, see OAuth Upgrade below)

## How to Use

First run (no docs/icp.md yet):
```
"Monitor Reddit for my ICP signals"
"Scan subreddits for people who need my product"
```

The skill asks 3 questions to build your ICP definition and saves it to docs/icp.md.

Subsequent runs (docs/icp.md exists):
```
"Check Reddit for buying signals"
"Run the Reddit ICP monitor for this week"
"Find ICP posts from the last month"
```

Specify a time window:
```
"Monitor Reddit for ICP signals from the last 24 hours"
"Check Reddit for this month's pain point posts"
```

## Output

Each run produces a report with:
- All subreddits monitored and time window
- Each high-signal post: title, URL, upvotes, signal quote, matched keyword, post type
- A drafted reply for each match (2-5 sentences, mode-appropriate)
- A list of subreddits that returned 0 results (for tuning)

Reports are saved to `docs/reddit-intel/YYYY-MM-DD.md`.

## Reply Modes

The skill classifies each post and drafts in the appropriate mode:

| Mode | Post Type | Can Name Product? |
|------|-----------|------------------|
| Mode 1 | Venting / frustration | Never |
| Mode 2 | "How do you handle X?" | Never |
| Mode 3 | "What tool does X?" | Yes, with one alternative |

## Choosing Good Subreddits

**Where to monitor (people describing problems):**
- r/devops, r/ExperiencedDevs, r/sysadmin: engineers asking operational questions
- r/startups, r/SaaS, r/EntrepreneurRideAlong: founders and operators venting about scaling
- r/sales, r/marketing: GTM practitioners asking how others handle things

**Where not to monitor:**
- Topic subreddits (r/programming, r/MachineLearning): discussions, not pain points
- Your product's own subreddit: not monitoring your own community
- Broad consumer subreddits: not your B2B ICP

## OAuth Upgrade

If you need more than 10 RPM (large subreddits or frequent runs):

1. Go to reddit.com/prefs/apps and create a "script" app
2. Note: app approval may take several days as of late 2025
3. Fill in REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD in .env

With OAuth, the skill fetches a Bearer token at session start and uses the `oauth.reddit.com` endpoint for 60 RPM.

## Project Structure

```
reddit-icp-monitor/
├── SKILL.md
├── README.md
├── .env.example
├── evals/
│   └── evals.json
└── references/
    ├── icp-format.md
    └── reply-rules.md
```

## License

MIT
