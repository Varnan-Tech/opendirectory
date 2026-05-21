---
name: graphic-gif
description: Creates animated looping GIFs from CSS animations (default) or AI image-to-video. 800×800px default, 6 animation types, 4 style presets. Trigger when user says "create an animated gif", "make a looping gif", "animated banner", "CSS animation gif", "social media animation", "make this loop", "animated graphic", or "motion graphic".
compatibility: [claude-code, gemini-cli, github-copilot]
author: OpenDirectory
version: 1.0.0
---

# graphic-gif

Generates an animated looping GIF from CSS animations or an AI image-to-video API. Output: `animation.gif`.

Unlike every other `graphic-` skill that outputs a static PNG or PDF, this skill outputs an animated `.gif`. Uses CSS `@keyframes` animations captured frame-by-frame via Playwright and the Web Animations API (Option A, default), or an AI image-to-video pipeline via Kling (Option B).

---

## Critical Rules (read before every generation)

1. **Default is css-animated.** Never use `ai-generated` unless explicitly requested.
2. **Canvas is 800×800px square.** All `clamp()` values computed at 800px (1vw = 8px).
3. **Single self-contained HTML.** All CSS inline in `<style>`. Font CDN `<link>` only external dependency.
4. **Never dump HTML in chat.** Save to file, show summary only.
5. **Frame capture uses Web Animations API seeking.** NOT `setTimeout` loops, NOT `animation-delay` tricks.
6. **Exact frame count:** `Math.floor(duration_seconds * fps)` frames. The frame at `t=duration_ms` MUST NOT be captured — it duplicates `t=0` and causes a visible stutter at the loop point.
7. **No placeholder boxes.** CSS-generated visuals only. No "image goes here" elements.
8. **Simpler palettes = smaller files.** Use: `clean-slate`, `terminal`, `electric-burst`, `brutalist`.
9. **No animation-delay for stagger.** Bake stagger into `@keyframes` percentages — frame seeking handles timing.
10. **Commit to design direction before writing CSS.** Tone, signature element, motion style, unforgettable detail — all decided before first line of code.

---

## Step 1: Intake

**Required:** `prompt` (content description AND motion brief)

**Optional with defaults:**

| Parameter | Default | Options |
|---|---|---|
| animation_type | css-animated | css-animated / ai-generated |
| duration | 3.0 | seconds |
| fps | 12 | frames per second |
| loop | true | true / false |
| style | clean-slate | clean-slate / terminal / electric-burst / brutalist |
| dimensions | 800x800 | WxH in pixels |
| optimization | balanced | quality / balanced / filesize |

**If prompt is missing or lacks motion description, ask exactly:**

> "What should the GIF show? Describe the content AND the motion (e.g., 'Stats count up: 73% of buyers read 3+ pieces of content before purchase. Typewriter effect, one character at a time. Style: terminal. 3 seconds, 12fps.')
>
> Key settings (all optional, defaults shown):
> - animation_type: css-animated (default) or ai-generated
> - duration: 3.0 seconds
> - fps: 12
> - loop: true
> - style: clean-slate (options: clean-slate / terminal / electric-burst / brutalist)
> - dimensions: 800x800
> - optimization: balanced (options: quality / balanced / filesize)"

If all required info is present → skip directly to Step 2.

---

## Step 2: Internal Architecture (never shown to user)

**For css-animated:**

1. Choose animation type from: `fade-in`, `slide-in`, `typewriter`, `counter`, `pulse`, `loop-scroll`
2. Read `references/animation-library.md` — find the chosen type's full HTML/CSS spec
3. Read `references/style-presets.md` — load the chosen style's CSS token block
4. Calculate frame count: `Math.floor(duration_seconds * fps)` — write this number down
5. Commit to design direction:

| Decision | Derive from |
|---|---|
| Tone | Emotional register for audience (mechanical / warm / electric / professional) |
| Signature element | ONE visual device used consistently (cursor blink, ghost number, scan-line overlay, accent border) |
| Motion style | Ease curve philosophy for this type (spring / linear / step / ease-in-out) |
| Unforgettable detail | The ONE thing a viewer will remember about this GIF |

**For ai-generated:**
1. Generate base still frame HTML (poster-style layout for the canvas)
2. Export as PNG using screenshot
3. Call Kling API: `POST https://api.klingai.com/v1/videos/image2video` with `image_url` and `prompt` describing the motion
4. Poll for job completion
5. Download video → convert to GIF with ffmpeg:
   ```bash
   # Two-pass palette for best color quality
   ffmpeg -i input.mp4 -vf "fps=12,scale=800:800:flags=lanczos,palettegen=stats_mode=diff" palette.png
   ffmpeg -i input.mp4 -i palette.png -vf "fps=12,scale=800:800:flags=lanczos,paletteuse=dither=bayer:bayer_scale=5" output.gif
   ```

---

## Step 3: HTML Generation (css-animated path)

Read `references/animation-library.md` and `references/style-presets.md` before generating.

**Canvas base — required on every GIF:**
```css
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

body {
  width: 800px;
  height: 800px;
  overflow: hidden;
  background: var(--bg);
  font-family: var(--font-body);
}

.canvas {
  width: 800px;
  height: 800px;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

**Animation rules:**
- `animation-fill-mode: forwards` (or `both`) on ALL animated elements
- Timing functions per type:
  - `typewriter` → `steps(N, end)` where N = exact character count
  - `counter` → `linear`
  - `fade-in` → `cubic-bezier(0.22, 1, 0.36, 1)` (ease-out)
  - `slide-in` → `cubic-bezier(0.34, 1.56, 0.64, 1)` (spring overshoot)
  - `pulse` → `ease-in-out` with `animation-iteration-count: infinite`
  - `loop-scroll` → `linear` with `animation-iteration-count: infinite`
- For one-shot animations (fade-in, slide-in, typewriter, counter): `animation-iteration-count: 1` — looping happens at GIF level
- **No `animation-delay`** — stagger is baked into `@keyframes` percentages

**Typewriter N calculation:**
Count every character including spaces, punctuation, numbers:
- "73% of buyers" = 14 characters → `steps(14, end)`
- "Hello, World!" = 13 characters → `steps(13, end)`

**Counter CSS `@property` (required for counter type):**
```css
@property --num {
  syntax: '<integer>';
  inherits: false;
  initial-value: 0;
}
.counter {
  animation: countUp var(--duration) linear forwards;
  counter-reset: num var(--num);
}
.counter::after { content: counter(num); }
@keyframes countUp {
  from { --num: 0; }
  to   { --num: var(--target); }
}
```

**Loop-scroll: content MUST be duplicated:**
```html
<!-- 4 original items + 4 duplicate items -->
<div class="ticker-track" style="--item-count: 4;">
  [item1][item2][item3][item4][item1][item2][item3][item4]
</div>
```
`translateX(0 → -50%)` with `linear infinite`.

**Design quality rules (from commit in Step 2):**
- Named signature element MUST be present in CSS/HTML (not just described)
- Typography: weight contrast minimum 2:1 (e.g., 700 vs 400) between display and supporting text
- Background: no pure white `#fff` for dark styles — use the preset's exact `--bg` value
- For terminal style: add scan-line overlay `::after` with `repeating-linear-gradient` at `opacity: 0.03`
- For brutalist: thick border `4px solid #000` or `4px solid var(--accent)` on key element
- Unforgettable detail: if it requires an extra element — add it now

---

## Step 4: Self-QA (fix every failure before Step 5)

**Canvas:**
- [ ] `body` and `.canvas` exactly 800×800px (or specified dimensions)
- [ ] `overflow: hidden` on both `body` and `.canvas`
- [ ] No elements overflowing the canvas boundary

**Animations:**
- [ ] NO `animation-delay` anywhere — stagger is in `@keyframes` percentages
- [ ] All animations start at `t=0` (Web Animations API will seek from there)
- [ ] `animation-fill-mode: forwards` or `both` on all animated elements
- [ ] One-shot animations: `animation-iteration-count: 1`
- [ ] Infinite animations (pulse, loop-scroll): `animation-iteration-count: infinite`

**Type-specific checks:**
- [ ] Typewriter: N in `steps(N, end)` = exact character count of text string
- [ ] Counter: `@property --num` declared with `syntax: '<integer>'` and `initial-value: 0`
- [ ] Counter: `counter-reset: num var(--num)` and `::after { content: counter(num) }`
- [ ] Loop-scroll: content duplicated exactly once in HTML

**Design:**
- [ ] No placeholder boxes
- [ ] Style preset tokens applied from `references/style-presets.md` — no free-floating hex colors
- [ ] Signature element named in Step 2 is actually present in the HTML/CSS
- [ ] Unforgettable detail from Step 2 is actually implemented
- [ ] Font CDN `<link>` present for chosen style's font

---

## Step 5: Export

**Determine slug from prompt** (kebab-case, ≤30 chars). Create output directory:
```bash
mkdir -p [slug]
```

Save HTML:
```
[slug]/animation.html
```

Open in browser for quick visual check:
```bash
open [slug]/animation.html
```

Run export script (replace `[skill-root]` with the actual path to this skill):
```bash
bash [skill-root]/scripts/export-gif.sh \
  [slug]/animation.html \
  [slug]/animation.gif \
  --duration [duration] \
  --fps [fps] \
  [--no-loop if loop=false] \
  --optimization [optimization] \
  --width [W] \
  --height [H]
```

The script:
1. Installs `gifenc`, `sharp` (or `jimp`), and `playwright` in a temp directory
2. Downloads Chromium if not cached
3. Runs `capture-and-encode.mjs` — pauses animations, seeks each frame, screenshots, assembles GIF
4. Runs `gifsicle` optimization pass if available
5. Reports file size and opens result

**If export script not found** at `[skill-root]/scripts/export-gif.sh`, check that the skill was installed with its `scripts/` folder intact.

---

## Step 6: Output Summary

Show after successful export:

```
## GIF: [1-line description]
Date: [YYYY-MM-DD] | Style: [style] | Animation: [type] | [duration]s @ [fps]fps
Dimensions: [WxH] | Frames: [N] | Loop: [true/false]

Files
  Source:   [slug]/animation.html
  Output:   [slug]/animation.gif
  Size:     [X] KB

Checklist
- [ ] Preview loops cleanly at start/end point (no stutter)
- [ ] Text legible at intended display size
- [ ] File size appropriate: email <500KB / social <3MB
```

---

## AI-Generated Path (Option B)

Only use when `animation_type: ai-generated` is explicitly specified.

**Requirements:**
- Kling API key in environment: `KLING_API_KEY` (66 free credits/day, no credit card for free tier)
- `ffmpeg` installed locally for video→GIF conversion

**Workflow:**
1. Generate a base still frame HTML matching the prompt (poster/graphic style at specified dimensions)
2. Export still frame as PNG:
   ```bash
   # Quick screenshot via Playwright
   node -e "
     const { chromium } = require('playwright');
     (async () => {
       const browser = await chromium.launch();
       const page = await browser.newPage({ viewport: { width: W, height: H } });
       await page.goto('file://[slug]/animation.html');
       await page.screenshot({ path: '[slug]/base-frame.png' });
       await browser.close();
     })();
   "
   ```
3. Upload to Kling image-to-video endpoint
4. Convert result to GIF with ffmpeg two-pass palette
5. Apply gifsicle optimization

**When Kling is unavailable:** Fall back to css-animated with a note to the user: "AI generation requires a Kling API key (KLING_API_KEY). Falling back to css-animated. Set the key to enable AI generation."

---

## Prompt Tips (show when user asks for guidance)

> "Describe motion, not just content. 'Stats count up one by one' beats 'show stats'."
>
> "Keep it simple for file size. 1–3 animated elements and a solid background."
>
> "Think in loops. The animation should flow invisibly from end back to start."
>
> "Specify the animation type explicitly. `typewriter` and `counter` are the most effective for social."
>
> ✅ Good: "Create an animated GIF, css-animated, typewriter effect. Text: '73% of B2B buyers read 3+ pieces of content before contacting sales.' Each character types out one at a time. Style: terminal. 3 seconds, 12fps, loop=true."
>
> ❌ Bad: "make an animated gif of marketing tips"
