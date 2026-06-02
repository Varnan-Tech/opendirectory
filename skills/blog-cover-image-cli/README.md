# Blog Cover Image CLI

A modern, AI-powered CLI tool designed to automatically generate high-converting, minimalist blog cover images and thumbnails using **Gemini 3.1 Flash Image Preview**. 


<img width="1280" height="640" alt="blog-cover-image-cli-cover" src="https://github.com/user-attachments/assets/20336e16-a838-4281-9c48-af023fc84b4c" />


It handles everything from fetching company logos to pixel-perfect typography integration, all from your terminal or directly via an AI Agent using the included OpenCode Skill.

![Banner](https://img.shields.io/badge/AI-Gemini%203.1-blue)
![Format](https://img.shields.io/badge/Format-16:9-success)
![Platform](https://img.shields.io/badge/Platform-Node.js-green)

---

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install blog-cover-image-cli --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fblog-cover-image-cli&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## Features
- **Full AI Generation**: Uses `gemini-3.1-flash-image-preview` to generate the entire image.
- **Smart Logo Fetching**: Pass a domain (like `vercel.com`) and the CLI automatically fetches the logo using `Brandfetch`, normalizes it to PNG via `sharp`, and injects it into the AI context.
- **Aesthetic Control**: Bundled with `examples/` that automatically guide the model to produce clean, white-background, heavy-typography styles.
- **Google Search Grounding**: The image generation is hooked into Google Search to pull real-time data if your title involves current events.
- **Agent Ready**: Includes an OpenCode `SKILL.md` so your favorite AI agents can use this CLI autonomously.
- **Self-Healing AI Generator**: Automatically validates generated images using Gemini Pro Vision to detect typos or layout issues, retrying up to 3 times with corrective feedback.

---

## Setup

You can install this globally via npm:

```bash
npm install -g blog-cover-image-cli
```

*(Note: Ensure you are using Node.js v18+)*

---

## Configuration

The CLI securely stores your API key on your local machine using the `conf` package so you don't have to export it every time.

```bash
# 1. Set your Gemini API Key (Required for image generation)
blog-cover-cli config set-key <YOUR_GEMINI_API_KEY>

# 2. Set your Brandfetch Client ID (Required to fetch high-res logos)
blog-cover-cli config set-brandfetch-id <YOUR_BRANDFETCH_CLIENT_ID>

# Check your keys (masked)
blog-cover-cli config get-key
blog-cover-cli config get-brandfetch-id
```

*If you run the generate command without a key, a secure, interactive prompt will ask you for it.*

---

## Usage

Generate a 16:9 cover image by providing a title and a domain name for the logo.

```bash
# Example 1: Cursor
blog-cover-cli generate -t "Why Cursor is the Ultimate AI Code Editor" -l "cursor.com"

# Example 2: Lovable
blog-cover-cli generate -t "Building Apps in Minutes with Lovable" -l "lovable.dev"

# Example 3: X (Twitter)
blog-cover-cli generate -t "The Future of Real-time Information" -l "x.com"
```

### Options

| Flag | Full Name | Description | Required | Default |
|---|---|---|---|---|
| `-t` | `--title` | The exact text to render on the cover | **Yes** | |
| `-l` | `--logo` | The domain to fetch the logo from (e.g. `google.com`) | No | |
| `-o` | `--output` | The output path for the PNG file | No | `./output/<auto-name>.png` |

If you omit the `--output` flag, the CLI automatically creates an `output/` directory in your current path and names the file intelligently based on the logo domain or title (e.g., `output/cursor-cover.png`).

---

## For AI Agents (OpenCode Skill)

This skill folder includes a structured `SKILL.md` for AI agents. The skill automatically calls the published `blog-cover-image-cli` npm package to generate cover images for users autonomously. 

**Workflow for Agents:**
1. Execute `npx -p blog-cover-image-cli blog-cover-cli config set-key $KEY`
2. Execute `npx -p blog-cover-image-cli blog-cover-cli generate -t "Title" -l "domain.com"`
3. Return the generated image to the user.

---

## Self-Healing AI Generator

The CLI features a built-in Automated QA (Critic) loop to ensure high-quality results. 

1. **Generation**: The tool generates an image based on your title and logo.
2. **Validation**: It uses `gemini-3.1-pro-preview` to OCR the generated image and check for typos, layout issues, or missing elements.
3. **Self-Correction**: If the validation fails, the CLI automatically retries (up to 3 times), passing the specific "critical feedback" back to the generator to fix the errors.

This ensures that common AI image generation issues, like misspelled words in typography, are caught and corrected before you even see the file.


---

## How it works under the hood
1. **Logo Fetcher**: Hits `Brandfetch`, parses WebP/SVGs/AVIFs, and converts to strict PNGs.
2. **Context Assembly**: Loads aesthetic examples from the `./examples` folder to ground the style.
3. **Multimodal Prompting**: Assembles the exact text instructions, the visual examples, and the fetched logo into a single unified payload.
4. **Google GenAI SDK**: Sends the payload with `tools: [{ googleSearch: {} }]` to the Gemini 3.1 Flash Image model.
