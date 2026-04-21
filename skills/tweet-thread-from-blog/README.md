# tweet-thread-from-blog

<img width="1280" height="640" alt="tweet-thread-from-blog" src="https://github.com/user-attachments/assets/18b96a6b-9477-444d-b169-ea14a63e9fdf" />


Turn any blog post or article into a Twitter/X thread. The agent reads the content, picks the right thread style, and writes 7-10 tweets with a strong hook, one insight per tweet, and a CTA. Optionally posts the full thread to X via Composio using a reply chain.

## Install

```bash
npx "@opendirectory.dev/skills" install tweet-thread-from-blog --target claude
```

## Thread Styles

| Style | Use When | Example Input |
|-------|----------|---------------|
| Data/Insight | Evidence-based article with stats or research findings | Engineering blog post with benchmark numbers |
| How-To | Tutorial or step-by-step guide | "How to set up X in 10 minutes" post |
| Story/Journey | Personal experience, build log, lessons learned | Indie hacker retrospective |
| Hot Take | Opinion piece, contrarian argument | "Why X is wrong" editorial |

The agent auto-detects the right style. Override it by specifying the style in your prompt.

## Requirements

No LLM API key needed. The agent reads the page and writes the thread.

**Note on X/Twitter posting:** Twitter's API v2 now requires a paid developer account (Basic tier, $100/month minimum). As a result, the Composio Twitter integration returns a 403 error for most users. The skill still generates complete, ready-to-post threads — just copy-paste them manually. Direct posting via Composio is documented below but is only viable if you have a paid Twitter developer account connected.

## Setup

### 1. Configure environment variables (optional)

```bash
cp .env.example .env
# Add COMPOSIO_API_KEY if you want direct posting to X
```

### 2. Connect X/Twitter via Composio (optional, requires paid Twitter developer account)

Twitter's API v2 now requires a paid developer account before Composio can post on your behalf. If you get a 403 error, this is why. Skip this step and use copy-paste output instead.

1. Sign up for Twitter Developer Portal (Basic tier, ~$100/month): https://developer.twitter.com/en/portal/products
2. Get your Composio API key at: https://app.composio.dev/settings
3. Connect your X/Twitter account at: https://app.composio.dev/app/twitter
4. Complete the OAuth flow

## How to Use

From a URL:

```
"Turn this into a tweet thread: https://example.com/blog/post"
"Create a Twitter thread from this article: https://example.com/post"
"Write a tweet thread about this blog post: https://example.com/tutorial"
```

From pasted content:

```
"Make a thread from this: [paste article text]"
"Turn this into a Twitter thread: [paste blog post]"
```

With a style override:

```
"Turn this into a How-To thread: https://example.com/data-article"
"Write a Hot Take thread from this: https://example.com/opinion"
```

With direct posting (requires paid Twitter developer account + Composio setup):

```
"Post this blog post as a Twitter thread: https://example.com/post"
```

## Output

| Output | Description |
|--------|-------------|
| Full thread | 7-10 numbered tweets, each under 280 characters |
| Alternative hook | A second hook tweet in a different format |
| Posted confirmation | If COMPOSIO_API_KEY is set and you confirm, the thread posts as a reply chain on X |

## How Threads Are Formatted

Hook first. Tweet 1 leads with the most surprising insight or a curiosity gap. It never announces the thread.

One idea per tweet. If a tweet can be split, it gets split. Each tweet stands alone.

Numbered throughout. Every tweet starts with its position: "1/8", "2/8", etc.

CTA last. The final tweet is the only one with a URL or call to action.

No hashtags. Hashtags reduce the quality signal of technical threads.

## Project Structure

```
tweet-thread-from-blog/
├── SKILL.md
├── README.md
├── .env.example
├── evals/
│   └── evals.json
└── references/
    ├── thread-format.md
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
