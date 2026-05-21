# graphic-gif

Generate animated looping GIFs from CSS animations. 800×800px default, 6 animation types, 4 style presets.

## Install

```bash
npx "@opendirectory.dev/skills" install graphic-gif --target claude
```

### Manual Install (2 steps)

1. Copy the URL of this skill folder from your browser, paste it at [download-directory.github.io](https://download-directory.github.io/), download the zip.
2. Open Claude desktop app → sidebar → **Customize** → **Skills** → **+** → **Upload a skill** → drop the extracted folder (the one containing `SKILL.md`).

---

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
