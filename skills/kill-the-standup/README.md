# kill-the-standup

<img width="1280" height="640" alt="kill-the-standup" src="https://github.com/user-attachments/assets/4fcf306d-7ef9-455a-b5f1-02532c292f65" />


Write your daily standup in seconds. The skill reads yesterday's Linear issues and GitHub commits, formats a done/doing/blockers update, and posts it to Slack.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install kill-the-standup --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fkill-the-standup&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Does

- Fetches yesterday's Linear issues assigned to you (completed and in-progress)
- Fetches yesterday's GitHub commits from your configured repo
- Formats a three-section standup: Done, Doing, Blockers
- Posts to your Slack channel via Incoming Webhook

## Requirements

| Requirement | Purpose | How to Set Up |
|------------|---------|--------------|
| Linear API key | Fetching your issues | Linear, Settings, API, Personal API keys |
| Slack Incoming Webhook | Posting the standup | api.slack.com/apps, Your App, Incoming Webhooks |
| `gh` CLI (optional) | Fetching GitHub commits | https://cli.github.com, then run `gh auth login` |

No LLM API key needed. The agent reads your activity directly.

## Setup

```bash
cp .env.example .env
```

Edit `.env` and fill in:
- `LINEAR_API_KEY` (required)
- `SLACK_WEBHOOK_URL` (required)
- `GITHUB_REPO` (optional, format: `owner/repo`)
- `GITHUB_USERNAME` (optional, defaults to your gh auth username)

## How to Use

Write and post standup:

```
"Write my standup"
"Post my standup to Slack"
"Generate standup update"
```

Output only, no Slack post:

```
"Write my standup but don't post it"
"What did I do yesterday?"
"Give me my standup text"
```

## Output Format

```
Done
- [ENG-123] Fix session timeout bug
- fix: remove duplicate middleware registration

Doing
- [ENG-124] Migrate auth to OAuth2

Blockers
No blockers.
```

## Project Structure

```
kill-the-standup/
├── SKILL.md
├── README.md
├── .env.example
├── evals/
│   └── evals.json
└── references/
    └── standup-format.md
```

## License

MIT
