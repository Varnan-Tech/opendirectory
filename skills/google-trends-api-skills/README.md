# Google Trends API Skills

<img width="1280" height="640" alt="google-trends-skills-cover" src="https://github.com/user-attachments/assets/848aa1be-64af-4b4b-bf46-af3d0798b7ee" />

Agent Skills for SEO keyword research using Google Trends data via SerpApi. Built for AI agents that generate tech and developer-focused blog content.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install google-trends-api-skills --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fgoogle-trends-api-skills&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## Skills

### 1. `google-trends-api/`
The API layer — knows how to query Google Trends through SerpApi, handle responses, manage rate limits, and cache results.

### 2. `seo-keyword-research/`
The SEO workflow — uses Google Trends data to find breakout keywords, build content structure, and generate SEO-optimized blog outlines.

## Quick Start

```bash
# 1. Get a free API key (250 searches/month)
# https://serpapi.com/

# 2. Set your key
export SERPAPI_KEY="your_key_here"

# 3. Set up dependency
pip install requests

# 4. Run keyword research for a blog topic
python seo-keyword-research/scripts/blog_seo_research.py "kubernetes deployment"

# 5. Or just discover trending keywords
python google-trends-api/scripts/discover_keywords.py "AI developer tools"
```

## Directory Structure

```
google-trends-api/
├── SKILL.md                        # API skill (endpoints, params, usage)
├── scripts/
│   └── discover_keywords.py        # Keyword discovery script
└── references/
    └── api-responses.md            # Full API response structures

seo-keyword-research/
├── SKILL.md                        # SEO workflow skill (research -> outline)
├── scripts/
│   └── blog_seo_research.py        # Full blog SEO research script
└── references/
    ├── keyword-placement-guide.md  # Detailed keyword placement rules
    └── tech-blog-examples.md       # Real examples for tech/dev blogs
```

## How It Works

```
User: "Write a blog about kubernetes deployment"
  |
  v
[google-trends-api] RELATED_QUERIES -> finds "kubernetes vs docker" (Breakout!)
[google-trends-api] RELATED_TOPICS  -> finds "Helm", "CI/CD", "Container Orchestration"
  |
  v
[seo-keyword-research] Selects primary keyword, builds outline
  |
  v
Output: SEO-optimized blog outline targeting trending keywords
```

## Specification

These skills follow the [Agent Skills specification](https://agentskills.io/specification). Each skill has:
- `SKILL.md` with YAML frontmatter (name, description, compatibility, metadata)
- `scripts/` for executable code
- `references/` for detailed documentation (loaded on demand)

## License

MIT
