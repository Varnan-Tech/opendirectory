# vid-motion-graphics

Generates multi-scene motion graphics as MP4 from a content brief. HTML/CSS animations rendered frame-by-frame in headless Chromium via Playwright, assembled with FFmpeg. No React, no AI APIs, no Python.

<img width="1920" height="1072" alt="vid-motion-graphics-cover-image" src="https://github.com/user-attachments/assets/51d085a4-9216-4da5-948c-82ed7e5e0818" />

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install vid-motion-graphics --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fvid-motion-graphics&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What it does

1. Takes a content brief (what each scene should say) and style params
2. Generates a multi-scene HTML/CSS animation file
3. Captures frames via Playwright + Web Animations API seeking
4. Assembles PNG sequence → H.264 MP4 with FFmpeg
5. Optionally mixes in background audio

## Output

- Format: H.264 MP4, `-pix_fmt yuv420p` (compatible with QuickTime, iOS, Android, Twitter, LinkedIn, Instagram)
- Default: 1080×1080px @2× retina (2160×2160 actual)
- Supports: 1:1, 16:9 (1920×1080), 9:16 (1080×1920)
- FPS: 24, 30, or 60

## Scene types

| Type | Best for |
|---|---|
| `title-card` | Opening hook, brand intro |
| `stat-reveal` | Single oversized metric |
| `bullet-list` | 2–4 supporting points |
| `split-screen` | Before/after, two values |
| `quote-card` | Testimonial, pull quote |
| `cta-card` | Final scene, call to action |

## Style presets

| Preset | Feel |
|---|---|
| `kinetic-dark` | Dark bg, electric yellow, tight grotesque (default) |
| `editorial-light` | White bg, serif display, refined |
| `data-pulse` | Deep navy, mono, terminal/dashboard |
| `bold-type` | White bg, Bebas Neue, red accent, slam-in |
| `minimal-clean` | Off-white, Cormorant, gentle rise |

## Requirements

- Node.js (for Playwright frame capture)
- FFmpeg (for MP4 assembly)
- Internet access for Google Fonts CDN during capture

## Usage

```
Create a 9-second motion graphic. Brief: 'Q4 revenue hit $4.2M — 85% growth.
Three drivers: enterprise deals, churn 1.2%, price increase.
CTA: acme.com/q4'. Style: data-pulse. Aspect: 1:1.
```

## Quick export

```bash
bash scripts/export-video.sh chart/[slug]/video.html --duration 9
```

## Differentiator vs SkillsMP

All top SkillsMP motion-graphic skills require Remotion (React build step) or AI video APIs (Runway, Kling — cost + rate limits). This skill uses the proven HTML/CSS → Playwright → FFmpeg pipeline from the `graphic-gif` family: zero new dependencies, pixel-perfect output, full CSS control.
