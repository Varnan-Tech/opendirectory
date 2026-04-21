# reddit-post-engine

<img width="1280" height="640" alt="reddit-post-engine" src="https://github.com/user-attachments/assets/2706f326-5fb9-46fc-851a-ec54ccf53f74" />


Write and optionally post Reddit content that fits the target subreddit's culture. Fetches subreddit rules and top posts before drafting. Follows the 90/10 rule. Optionally posts via Composio Reddit MCP.

## Install

```bash
npx "@opendirectory.dev/skills" install reddit-post-engine --target claude
```

## What It Does

- Fetches the target subreddit's rules and top posts from Reddit's public API
- Identifies the subreddit's tone and posting conventions
- Drafts a title and body that match the community's style
- Keeps product links out of the body (puts them in the first comment)
- Optionally posts directly via Composio
- Covers 7 common subreddits with specific playbooks

## Requirements

| Requirement | Purpose | How to Set Up |
|------------|---------|--------------|
| Gemini API key | Post drafting and tone matching | aistudio.google.com, Get API key |
| Composio Reddit MCP (optional) | Direct posting | app.composio.dev |

## Setup

### 1. Configure environment variables

```bash
cp .env.example .env
# Add GEMINI_API_KEY (required)
# Add COMPOSIO_API_KEY if you want direct posting
```

### 2. Connect Reddit via Composio (optional)

Direct posting requires a Composio account connected to Reddit OAuth:

1. Get your Composio API key at app.composio.dev/settings
2. Connect Reddit at app.composio.dev/app/reddit
3. Add the MCP server to Claude Code:

```bash
claude mcp add --transport http reddit-composio \
  "https://mcp.composio.dev/reddit/YOUR_COMPOSIO_API_KEY"
```

4. Verify: `claude mcp list` should show `reddit-composio`

Without Composio, the skill drafts posts for manual copy-paste submission.

## How to Use

Draft a post for a specific subreddit:
```
"Help me post my project on r/SideProject"
"Write a Reddit post for r/devops about my Kubernetes tool"
"Draft something for r/startups: we hit $1k MRR"
```

With direct posting:
```
"Post my project to r/SideProject via Composio"
```

Multi-subreddit drafts:
```
"Draft posts for r/SideProject and r/indiehackers for my launch"
```

## Subreddit Playbook Summary

| Subreddit | Tone | What Works |
|-----------|------|------------|
| r/devops | Technical, direct | Problem + solution + specific numbers |
| r/SideProject | Personal, builder | Build story + honest state + link in comment |
| r/startups | Business-focused | Lessons learned + metrics |
| r/programming | Technical, skeptical | Novel approach + code examples |
| r/ExperiencedDevs | Senior-level | Nuanced tradeoffs, no hand-holding |
| r/indiehackers | Transparent | Revenue numbers, real story |
| r/webdev | Friendly | What you built + how it works |

## The 90/10 Rule

Reddit detects promotional patterns. For your posts to land well, 90% of your Reddit activity should be genuine community contribution: answering questions, discussing topics, sharing interesting links. At most 10% should be posts about your own work.

This skill drafts high-quality posts, but the underlying account reputation matters. New accounts with no history posting self-promotional content often get filtered.

## Project Structure

```
reddit-post-engine/
├── SKILL.md
├── README.md
├── .env.example
├── evals/
│   └── evals.json
└── references/
    └── subreddit-playbook.md
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
