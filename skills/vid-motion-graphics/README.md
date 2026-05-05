# vid-motion-graphics

Generates multi-scene motion graphics as MP4 from a content brief. HTML/CSS animations rendered frame-by-frame in headless Chromium via Playwright, assembled with FFmpeg. No React, no AI APIs, no Python.

<img width="1920" height="1072" alt="vid-motion-graphics-cover-image" src="https://github.com/user-attachments/assets/51d085a4-9216-4da5-948c-82ed7e5e0818" />

## Install

```bash
npx "@opendirectory.dev/skills" install vid-motion-graphics --target claude
```

### Video Tutorial
Watch this quick video to see how it's done:

https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c

### Step 1: Download the skill from GitHub
1. Click the **Code** button on this repo's GitHub page.
2. Select **Download ZIP** to download the repository.
3. Extract the ZIP file on your computer.

### Step 2: Install the Skill in Claude
1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** (plus) icon button to create a new skill.
4. Choose the option to **Upload a skill**, and drag and drop the `.zip` file (or you can extract it and drop the folder, both work).

> **Note:** Make sure you are uploading the folder that contains the `SKILL.md` file!

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
