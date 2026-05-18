# Hyperframes Product Launch Video Skill

A specialized AI agent skill designed for creating elite, premium product launch videos using the Hyperframes framework. This skill distills months of motion design expertise, brand DNA extraction, and technical debugging into a structured workflow that guides your AI agent.

## Install

```bash
npx "@opendirectory.dev/skills" install hyperframes-product-launch-video --target claude
```

### Video Tutorial
Watch this quick video to see how it's done:

https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c

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

## Purpose

When building complex motion graphics or product launch videos, AI agents need structured guidance to avoid common pitfalls and to hit premium quality benchmarks. This skill provides:

- Step-by-step workflows for brand discovery and storyboarding
- Premium motion design patterns (Apple-style zooms, glassmorphism, typewriter physics)
- Best practices for combining Hyperframes with GSAP
- Perfect sound design (SFX) synchronization rules

## Architecture: Skill vs. Project

It is important to distinguish between the **Skill Folder** and the **Project Folder**:

- **Skill Folder** (`hyperframes-product-launch-video/`): This is the "instruction manual" and template repository. It is **read-only**. It contains the logic, scripts, and references needed to build a video.
- **Project Folder** (e.g., `my-new-video/`): This is where the actual video composition lives. All generated files—including `brand_dna.json`, `ART_DIRECTION.md`, and the final `index.html`—must be saved here, in the user's workspace.

The agent uses the skill to inform its actions but always outputs the results into the user's designated project directory.

## Initialization and Setup

To get started with Hyperframes and this skill in a target project, follow these steps:

1. **Initialize Hyperframes**:
   Run the following command in your project root:
   ```bash
   npx hyperframes init
   ```

2. **Install Dependencies**:
   Ensure all required packages are installed:
   ```bash
   npm install
   ```

3. **Development Mode**:
   Launch the studio editor to preview your composition in real-time:
   ```bash
   npm run dev
   ```

4. **Rendering**:
   Once your composition is ready, render it to an MP4 file:
   ```bash
   npm run render
   ```

## FFmpeg Requirement

FFmpeg is essential for the final video rendering process. Hyperframes uses FFmpeg to stitch screenshots and audio together. It expects the `ffmpeg` binary to be available in your system's `PATH`.

1. **System-wide Installation (Recommended)**:
   - **macOS:** `brew install ffmpeg`
   - **Linux:** `sudo apt install ffmpeg`
   - **Windows:** `choco install ffmpeg`

2. **Local Fallback**:
   If you cannot install FFmpeg globally, you can install the binary locally:
   ```bash
   npm install @ffmpeg-installer/ffmpeg
   ```
   *Note: Ensure your build script is configured to resolve this local path using `require('@ffmpeg-installer/ffmpeg').path`.*

## Leveraging Official Skills

This "Product Launch Video" skill is designed to work in tandem with the official Hyperframes documentation skills. It acts as the **Director and Architect**, providing the high-level strategy and art direction, while the official skills provide the granular implementation details.

**Required Official Skills**:
Run the following command to add the official Hyperframes skill:
```bash
npx skills add heygen-com/hyperframes
```

**How to use them together**:
- Use **this skill** for: Brand DNA extraction, scene-by-scene storyboarding, and premium motion strategy.
- Use the **official /hyperframes skill** for: Core composition rules, data-attribute semantics, and framework constraints.
- Use the **official /gsap skill** for: Detailed timeline references, easing functions, and complex animation patterns.

## What's Inside & Key Features
- **Brand DNA Extraction**: Automatically pulls colors and fonts from your site.
  - *To run manually:* Navigate to the `scripts/` directory, run `npm install` (this installs playwright and automatically downloads the Chromium browser binary), and execute `node extract_site_dna.js https://your-website.com`.
- **Elite Workflow**: From brand DNA extraction to final render.
- **Art Direction Template**: A scene-by-scene planning guide.
- **Perfect SFX Sync**: Generates a sound design shopping list and syncs it to the millisecond.
- **Premium Patterns**: Code snippets for Apple-style zooms, glassmorphism, and more.
- **Technical Gotchas**: Solutions to common Hyperframes and GSAP pitfalls.

---
*Created for the Hyperframes community.*