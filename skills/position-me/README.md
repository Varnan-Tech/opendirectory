# Position-Me

<img width="1376" height="768" alt="generated-image" src="https://github.com/user-attachments/assets/118fcd1f-1efc-4eca-b0b0-366a6f9ff5da" />

The Website Reviewer Agent Skill for AEO, GEO, SEO, UI/UX Psychology, and Direct Response Copywriting.

An open source skill that transforms modern AI Agents into rigorous positioning consultants. It forces the agent to use native vision capabilities to evaluate cognitive load and verify Generative Engine Optimization (GEO) compatibility.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install position-me --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fposition-me&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## Core Capabilities

When invoked, the skill commands the AI agent to conduct an exhaustive teardown of the target website through a rigid protocol:

* Autonomous Navigation: Crawl the homepage, about, pricing, and blog pages.
* Visual Psychology: Take full page screenshots and analyze visual friction, layout flow, and cognitive load using the LIFT model.
* Copywriting Critique: Rewrite generic text using the PAS (Problem, Agitation, Solution) framework.
* Deep Content Audits: Read actual blog posts to identify fluff, grade technical depth, and offer new content strategies.
* Technical Readiness: Verify the presence of llms.txt, sitemap.xml, and semantic JSON-LD Schema (FAQPage, SoftwareApplication, etc) for generative search optimization.

## Requirements

The host AI agent must have access to:
1. A multimodal LLM capable of analyzing screenshots natively.
2. Chrome DevTools MCP Server (https://github.com/ChromeDevTools/chrome-devtools-mcp).
3. Chrome CDP Skill (https://github.com/pasky/chrome-cdp-skill).
4. Terminal access to run fallback Python scripts if browser automation fails.

To set up the required Chrome automation:
* Install and configure the Chrome DevTools MCP server in the agent MCP settings.
* Add the Chrome CDP skill to the agent skills directory.
* Ensure Chrome is running with remote debugging enabled (e.g., `chrome --remote-debugging-port=9222`).

## Setup

### For Developers (Manual Setup)

1. Clone or download the `position-me` repository.
2. Copy the `position-me/` directory into the agent designated skills directory.
3. Alternatively, extract the raw `SKILL.md` and `references/` folder into the agent custom prompt configuration.

### For AI Agents (Automated Setup)

1. Clone or download the `position-me` repository into the active project workspace.
2. Read directly from the `position-me/` source folder.
3. Add the `SKILL.md` file to the active context window or skill registry.
4. Verify access to the `references/EVALUATION_SOP.md` and `references/REPORT_TEMPLATE.md` files.

## Execution Protocol for Agents

Once loaded, the AI agent must strictly follow this execution loop:

1. Data Gathering: Prompt the user for the target URL.
2. Connect to Browser: Use the Chrome DevTools MCP combined with the Chrome CDP skill.
3. Multi-Page Crawl: Navigate to the homepage, pricing page, about page, and at least one blog post.
4. Capture Vision Context: Take screenshots of every visited page and load them into memory.
5. Extract DOM Context: Pull the accessibility tree, search for `llms.txt`, and verify JSON-LD schemas.
6. Analyze: Apply the frameworks specified in `references/EVALUATION_SOP.md`.
7. Report: Generate a scored, highly structured teardown using exactly the format in `references/REPORT_TEMPLATE.md`.

## Project Structure

```text
position-me/
├── README.md                        # Documentation
└── position-me/                     # Raw skill source code
    ├── SKILL.md                     # Master protocol
    ├── scripts/
    │   └── extract_links.py         # Fallback crawler script
    └── references/
        ├── EVALUATION_SOP.md        # Evaluation frameworks
        └── REPORT_TEMPLATE.md       # Teardown report template
```
