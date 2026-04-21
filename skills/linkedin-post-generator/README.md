# linkedin-post-generator

<img width="1376" height="768" alt="LinkedIn_post_generator" src="https://github.com/user-attachments/assets/dc71e06b-8b3c-486a-adbf-d56a7b22cdc1" />

Generate LinkedIn posts from any content: blog posts, articles, GitHub PRs, or a description of what you built. The agent reads your source material, applies LinkedIn's content patterns, and produces a post with the right hook, story arc, and formatting.

## Install

```bash
npx "@opendirectory.dev/skills" install linkedin-post-generator --target claude
```

## Post Styles

| Style | Use When | Example Input |
|-------|----------|---------------|
| Founder/Ship | Personal story of building or shipping | "We merged our streaming SDK after 3 weeks" |
| Insight | Educational observation or lesson | Blog article, pattern you noticed, lesson learned |
| Product Launch | Announcing a new tool or feature | PR description, launch brief, feature going GA |
| Tutorial Summary | Distilling a long technical post | Tutorial URL, deep-dive article, step-by-step guide |

The agent auto-detects the right style. You override it by asking for a specific one.

## Requirements

No LLM API key needed. The agent writes the post.

Composio is optional. Add it to post directly to LinkedIn.

## Setup

### Composio (Optional)

Without Composio, the agent outputs formatted text for copy-paste. No configuration needed.

To enable direct posting:
1. Get your API key at https://app.composio.dev/settings
2. Connect your LinkedIn account at https://app.composio.dev/app/linkedin
3. Complete the OAuth flow
4. Add the key to your .env file:

```bash
cp .env.example .env
# Edit .env and add your COMPOSIO_API_KEY
```

## How to Use

From a URL:
```
"Turn this into a LinkedIn post: https://yourblog.com/my-post"
"Write a LinkedIn post about this article: [URL]"
```

From pasted text:
```
"Here's a case study, turn it into a LinkedIn post: [paste text]"
"Convert this to a LinkedIn post: [paste article]"
```

From a PR or shipped feature:
```
"Write a LinkedIn post about this PR we merged: [paste PR description]"
"Announce our new feature on LinkedIn: [describe the feature]"
```

With a style override:
```
"Write a LinkedIn post in Tutorial Summary style about: [topic]"
"Use the Product Launch style for this: [description]"
```

With direct posting:
```
"Post this to LinkedIn: [paste content]"
"Generate and post a LinkedIn update about [topic]"
```

## Output

| Output | Description |
|--------|-------------|
| LinkedIn post | Formatted text, 900-1,300 characters, ready to publish |
| First comment | Text with source links. Post this immediately after publishing. |
| Hook alternatives | 2 additional hook lines in different formats |
| Posted confirmation | If Composio is configured and you confirm posting |

## How Posts Are Formatted

Four rules drive every post the agent writes:

- Hook first. The first line is all most people see. It works standalone.
- Short paragraphs. 1-3 lines, then a blank line. LinkedIn is mobile-first.
- Links in the first comment. URLs in the post body reduce LinkedIn's distribution.
- Question or CTA at the end. One or the other, not both.

## Project Structure

```
linkedin-post-generator/
├── SKILL.md
├── README.md
├── .env.example
├── evals/
│   └── evals.json
└── references/
    ├── linkedin-format.md
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
