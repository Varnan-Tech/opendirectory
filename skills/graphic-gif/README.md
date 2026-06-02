# graphic-gif

Generate animated looping GIFs from CSS animations. 800×800px default, 6 animation types, 4 style presets.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install graphic-gif --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fgraphic-gif&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What it does

- Asks for a prompt (content + motion description) and optional settings
- Generates a self-contained HTML file with CSS `@keyframes` animations
- Captures frames using Playwright + Web Animations API for frame-accurate seeking
- Assembles frames into a GIF with [gifenc](https://github.com/mattdesl/gifenc)
- Optimizes the GIF with gifsicle for 35–50% size reduction
- Outputs a looping `animation.gif` ready for social, email, or Slack

---

## Example

> "Create an animated GIF, css-animated, typewriter effect. Text: '73% of B2B buyers read 3+ pieces of content before contacting sales.' Each character types out one at a time. Style: terminal. 3 seconds, 12fps, loop=true."

Output: `animation.gif` — dark background, JetBrains Mono font, green cursor, character-by-character reveal.

---

## Supported Animation Types

| Animation | Description | Best Use |
|---|---|---|
| fade-in | Content fades in from transparent with upward drift | Quotes, announcements, brand messages |
| slide-in | Elements slide in from edge with spring overshoot | Headlines, stats, before/after |
| typewriter | Text types out character by character | Insights, hooks, developer content |
| counter | Numbers count up to a target value | Stats, metrics, growth numbers |
| pulse | Pulsing / breathing scale or glow effect | CTAs, icons, live indicators |
| loop-scroll | Infinite scrolling ticker or marquee | Feature lists, social proof, tickers |

---

## Supported Styles

| Style | Best for |
|---|---|
| clean-slate | Professional B2B, LinkedIn, any audience expecting polish |
| terminal | Developer audience, typewriter effects, tech metrics |
| electric-burst | Bold stats, CTAs, high-energy social content |
| brutalist | Loop-scroll tickers, design-forward brands, raw aesthetic |

---

## Parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| prompt | Yes | — | Content description AND motion brief |
| animation_type | No | css-animated | css-animated / ai-generated |
| duration | No | 3.0 | Animation duration in seconds |
| fps | No | 12 | Frames per second (higher = smoother, larger file) |
| loop | No | true | Whether GIF loops continuously |
| style | No | clean-slate | Visual style preset |
| dimensions | No | 800x800 | Output dimensions in pixels |
| optimization | No | balanced | quality / balanced / filesize |

---

## Output

| File | What it is |
|---|---|
| `[slug]/animation.html` | Self-contained animated HTML (preview in browser) |
| `[slug]/animation.gif` | Final looping GIF, ready to use |

Typical file size: 150KB–1.5MB depending on animation type, duration, and optimization.

---

## Dependencies

**Node.js** — required. Install from [nodejs.org](https://nodejs.org) or `brew install node`.

Everything else is bundled inside this skill or installed automatically on first run:
- `scripts/export-gif.sh` — orchestrator script
- `scripts/capture-and-encode.mjs` — Playwright frame capture + gifenc assembly
- `gifenc` + `sharp` (or `jimp`) + `playwright` — auto-installed via npm on first run
- **gifsicle** — optional but recommended for 35–50% smaller files: `brew install gifsicle`

**For AI-generated GIFs (optional):**
- Kling API key in environment: `KLING_API_KEY`
- `ffmpeg` for video→GIF conversion: `brew install ffmpeg`
