# newsletter-digest

<img width="1280" height="640" alt="newsletter-digest" src="https://github.com/user-attachments/assets/cb2879ae-eb5c-4727-a1a2-47b4462a699b" />


Aggregate RSS feeds, synthesize the week's top stories with Gemini, and publish a newsletter digest to Ghost CMS. Supports three digest formats and outputs HTML, Markdown, and plain text for any platform.

## Install

```bash
npx "@opendirectory.dev/skills" install newsletter-digest --target claude
```

## What It Does

- Reads your RSS/Atom feed list from `feeds.json`
- Fetches all articles published in the last 7 days (configurable)
- Deduplicates across feeds and sorts by date
- Uses Gemini to synthesize a digest in your chosen format
- Publishes to Ghost as a draft or live post
- Outputs formatted Markdown for Substack, Notion, or any other platform

## Digest Formats

| Format | Use When | Target Length |
|--------|----------|---------------|
| Weekly Roundup | General digest covering top stories across all feeds | 350-500 words |
| Topic Deep Dive | Focused issue on a single topic (AI, security, etc.) | 450-650 words |
| Curated Picks | 5 selected articles with editorial context | 250-350 words |

## Requirements

| Requirement | Purpose | Where to Get It |
|------------|---------|-----------------|
| GEMINI_API_KEY | Digest synthesis | https://ai.google.dev |
| GHOST_URL + GHOST_ADMIN_KEY | Ghost publishing (optional) | Ghost Admin, Settings, Integrations |
| Node.js 20+ | Running scripts | https://nodejs.org |

Tavily is not required. The skill uses article excerpts from RSS feeds directly.

## Setup

### 1. Install dependencies

```bash
cd /path/to/newsletter-digest
npm install
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your keys
```

### 3. Configure your feeds

Edit `feeds.json` with the RSS feeds you want to monitor:

```json
[
  { "url": "https://hnrss.org/frontpage", "name": "Hacker News" },
  { "url": "https://feeds.feedburner.com/TheHackersNews", "name": "The Hacker News" },
  { "url": "https://changelog.com/feed", "name": "Changelog" }
]
```

The file ships with 5 example feeds. Replace them with your own.

### 4. Set up Ghost publishing (optional)

1. Go to Ghost Admin, Settings, Integrations
2. Click "Add custom integration"
3. Name it "newsletter-digest"
4. Copy the Admin API Key (format: `key_id:secret`)
5. Set `GHOST_ADMIN_KEY=key_id:secret` in `.env`
6. Set `GHOST_URL=https://your-ghost-site.com` in `.env`

## How to Use

Generate a weekly digest:

```
"Generate a weekly digest from my RSS feeds"
"Create this week's newsletter"
"Summarize my feeds from the last 7 days"
```

Choose a specific format:

```
"Create a topic deep dive about AI agents from this week's news"
"Generate a curated picks digest for this week"
"Write a weekly roundup newsletter"
```

Extend the date window:

```
"Generate a digest from the last 14 days"
"Not many articles this week, extend the window to 2 weeks"
```

Publish to Ghost:

```
"Generate this week's digest and publish it to Ghost as a draft"
"Create the newsletter and publish it to Ghost"
```

Output for Substack:

```
"Generate a newsletter digest for Substack"
"Create the digest and give me the Markdown version"
```

## Output

| Output | Description |
|--------|-------------|
| HTML | Ready to paste into any CMS |
| Markdown | For Substack, Notion, Hashnode |
| Plain text | For email clients |
| Ghost draft | Published automatically if configured |

## Substack Note

Substack has no public API. The skill outputs a Markdown version of the digest for you to paste directly into the Substack editor.

## Project Structure

```
newsletter-digest/
├── SKILL.md
├── README.md
├── .env.example
├── package.json
├── feeds.json            (your RSS feed list, edit this)
├── evals/
│   └── evals.json
├── references/
│   ├── digest-format.md  (format rules, length targets, attribution)
│   └── output-template.md (HTML templates for all 3 formats)
└── scripts/
    ├── fetch-feeds.js    (RSS fetching, dedup, date filtering)
    └── ghost-publish.js  (Ghost Admin API posting)
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
