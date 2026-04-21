# kill-the-standup

<img width="1280" height="640" alt="kill-the-standup" src="https://github.com/user-attachments/assets/4fcf306d-7ef9-455a-b5f1-02532c292f65" />


Write your daily standup in seconds. The skill reads yesterday's Linear issues and GitHub commits, formats a done/doing/blockers update, and posts it to Slack.

## Install

```bash
npx "@opendirectory.dev/skills" install kill-the-standup --target claude
```

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
