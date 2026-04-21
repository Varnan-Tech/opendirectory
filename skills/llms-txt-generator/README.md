# llms-txt-generator

<img width="1376" height="768" alt="llms-txt-generator" src="https://github.com/user-attachments/assets/7f549d0b-4d55-40a8-97c6-59510cc40b54" />

Generate a standards-compliant `llms.txt` file for any website. Makes your site fully readable and citable by AI agents the GEO (Generative Engine Optimization) equivalent of having a great sitemap.

## Install

```bash
npx "@opendirectory.dev/skills" install llms-txt-generator --target claude
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

The skill crawls your website using Chrome DevTools, reads your actual pages, and produces a clean `llms.txt` file in the format specified by [Jeremy Howard's llms.txt standard](https://llmstxt.org). When AI agents (Claude, ChatGPT, Gemini) visit your site, they read `llms.txt` first to understand what you are and where to find authoritative content.

**Without llms.txt:** AI agents guess, hallucinate, or cite competitors instead.  
**With llms.txt:** AI agents cite your product correctly and know exactly where your docs, blog, and key pages live.

## Two Modes

### Codebase Mode (no Chrome needed)
If you're inside a website's repo, the skill reads your source files directly pages, routes, blog posts, frontmatter, site config. It writes `llms.txt` straight to `public/` when you approve. No browser required.

Supported frameworks: **Next.js** (pages + app router), **Astro**, **Nuxt**, **Gatsby**, **SvelteKit**, **Hugo**, **Jekyll**

### Live Site Mode (Chrome or fetch fallback)
If you only have the URL, the skill crawls the live site using Chrome DevTools MCP. Falls back to standard web fetch if Chrome isn't available.

---

## Requirements

**Codebase Mode:** No extra setup. Just be inside the repo directory.

**Live Site Mode:**
- Chrome with remote debugging enabled (or any live URL skill will fall back to web fetch)
- Chrome DevTools MCP server configured in your agent (optional, improves JS-rendered sites)

## Setup

### For Live Site Mode: Start Chrome with Remote Debugging

**Mac:**
```bash
open -a "Google Chrome" --args --remote-debugging-port=9222
```

**Linux:**
```bash
google-chrome --remote-debugging-port=9222
```

**Windows:**
```bash
chrome.exe --remote-debugging-port=9222
```

### 2. Install Chrome DevTools MCP Server

Follow the setup at: https://github.com/ChromeDevTools/chrome-devtools-mcp

Add to your agent's MCP configuration:
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "@chrome-devtools/mcp-server"],
      "env": {
        "CHROME_DEBUGGING_PORT": "9222"
      }
    }
  }
}
```

### 3. Configure Environment (Optional)

Copy `.env.example` to `.env` and fill in:
```bash
cp .env.example .env
```

`GITHUB_TOKEN` and `GITHUB_REPO` are only needed if you want the agent to automatically open a GitHub PR with the generated file.

## How to Use

**Codebase Mode** just be inside your project and ask:
```
"Generate an llms.txt for this site"
"Add llms.txt to this project"
"Make this site readable by AI agents"
```

The agent will detect your framework, read your pages and blog posts from source, generate `llms.txt`, and write it to the right directory (e.g. `public/llms.txt`) after you confirm.

**Live Site Mode** provide a URL:
```
"Generate an llms.txt for https://yoursite.com"
"Does https://yoursite.com have an llms.txt? If not, create one."
```

The agent will:
1. Check if `llms.txt` already exists at the domain
2. Crawl homepage, docs, blog, about, pricing, and API pages
3. Generate `llms.txt` following the official spec
4. Optionally generate `llms-full.txt` with full page content
5. Save the file locally and give you deployment instructions
6. Optionally open a GitHub PR if configured

## Where to Deploy the File

Place `llms.txt` at your web root so it's accessible at `https://yourdomain.com/llms.txt`:

| Platform | File Location |
|----------|--------------|
| Next.js / Vercel | `/public/llms.txt` |
| Astro | `/public/llms.txt` |
| Nuxt | `/public/llms.txt` |
| GitHub Pages | Repository root |
| Hugo | `/static/llms.txt` |
| WordPress | Upload via FTP to web root |

## Output Files

| File | Description |
|------|-------------|
| `llms.txt` | Structured link map. LLMs follow links to find content |
| `llms-full.txt` | Full prose content of key pages. LLMs ingest everything at once |

## Project Structure

```
llms-txt-generator/
├── SKILL.md                          # Agent instructions
├── README.md                         # This file
├── .env.example                      # Environment variables template
├── evals/
│   └── evals.json                    # Test prompts for skill evaluation
└── references/
    ├── llms-txt-spec.md              # The llms.txt format specification
    └── output-template.md            # Exact output template with example
```

## License

MIT
