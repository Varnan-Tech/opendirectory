# noise2blog

<img width="1280" height="640" alt="noise2blog" src="https://github.com/user-attachments/assets/2359cff9-dfd4-4276-bb3e-4b6091ad6983" />


Paste your rough notes, bullet points, voice transcript, or tweet dump and get a publication-ready blog post.

## Install

```bash
npx "@opendirectory.dev/skills" install noise2blog --target claude
```

## What It Does

- Accepts any rough input: bullet points, rough notes, voice transcripts, tweet dumps, short drafts, or a URL
- Detects the right blog post style automatically (Technical Tutorial, Case Study, Thought Leadership, Explainer)
- Enriches claims with Tavily research when you set an API key (supporting data, verification)
- Generates a Markdown post with no AI slop, no em dashes, no banned words
- Formats frontmatter for Ghost, dev.to, Substack, or Hashnode on request

## Requirements

| Requirement | Purpose | How to Set Up |
|------------|---------|--------------|
| Google Gemini API key | Generates the blog post | aistudio.google.com, Get API key |
| Tavily API key (optional) | Enriches claims with research | app.tavily.com, API Keys |

No LLM backend to run. The agent calls the Gemini API directly.

## Setup

```bash
cp .env.example .env
```

Edit `.env` and fill in:
- `GEMINI_API_KEY` (required)
- `TAVILY_API_KEY` (optional, enables research enrichment)

## Blog Post Styles

| Style | Use When | Signals in Your Input |
|-------|----------|----------------------|
| Technical Tutorial | Step-by-step guide, code walkthrough | Numbered steps, commands, "how to" |
| Case Study | Build log, before/after story, lessons learned | Specific results, journey narrative |
| Thought Leadership | Opinion piece, counterintuitive argument | Strong claim, debate framing |
| Explainer | Explaining a concept or tool to newcomers | Definition-first, comparisons |

The agent detects the style automatically. Override it with: "Use Thought Leadership style" or "Make this a tutorial".

## How to Use

From pasted notes:

```
"Write a blog post from these notes: [paste your content]"
"Turn these bullet points into a blog post"
"Expand this into an article"
```

From a voice transcript:

```
"Turn this transcript into a blog post: [paste transcript]"
"Clean up this voice note and make it publishable"
```

From a tweet thread:

```
"Turn this tweet thread into a blog: [paste tweets]"
"Expand this thread into a full article"
```

With style override:

```
"Write a thought leadership post from these notes"
"Make this a technical tutorial"
```

With platform formatting:

```
"Write the post and format it for dev.to"
"Give me Ghost frontmatter too"
```

## Output

- Full blog post in Markdown (800-1,800 words)
- Meta description (1-2 sentences)
- Alternative title option
- Platform-specific frontmatter on request

## Project Structure

```
noise2blog/
├── SKILL.md
├── README.md
├── .env.example
├── evals/
│   └── evals.json
└── references/
    ├── blog-format.md
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
