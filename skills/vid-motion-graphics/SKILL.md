---
name: vid-motion-graphics
description: Generates motion graphics videos (MP4) from a content brief. Multi-scene HTML/CSS animations rendered frame-by-frame in headless Chromium via Playwright, assembled with FFmpeg. 1080×1080 default, 16:9 (1920×1080) and 9:16 (1080×1920) supported. 5 style presets. Trigger when user says "create a video", "motion graphic", "animated video", "make a reel", "create an explainer", "animated infographic", or "short video".
compatibility: [claude-code, gemini-cli, github-copilot]
author: OpenDirectory
version: 1.0.0
---

# vid-motion-graphics

Generates multi-scene motion graphics as MP4. Renders HTML/CSS animations in headless Chromium via Playwright (Web Animations API frame-seeking), assembles PNG frames with FFmpeg. No React, no AI APIs, no Python — zero new dependencies beyond the graphic-gif family.

CDN fonts only. No external libraries in HTML.

---

## Critical Rules (read before every generation)

1. **Use `window.renderFrame(t)` — no CSS `@keyframes` for scene transitions.** CSS animation `currentTime` seeking is silently ignored for backward seeks in Chromium. The renderFrame approach: a pure JS function computes `opacity`/`transform` directly from milliseconds. Playwright calls it once per frame. Deterministic, race-free.
2. **No `animation-delay` on ANY element.** Not needed with renderFrame. If you catch yourself writing `animation-delay`, stop — you're using the wrong architecture.
3. **`window.__videoReady = true` only inside `document.fonts.ready.then(...)`.** Never set synchronously — fonts must load before Playwright captures frame 1 or text renders with fallback fonts.
4. **Expose `window.__stopPreview()`.** The browser's rAF preview loop races with Playwright's evaluate/screenshot calls. `capture-frames.mjs` calls `__stopPreview()` before the frame loop. Always include it.
5. **Use `t < startMs` (not `<=`) in scene boundary checks.** `t <= 0` at frame 0 makes scene 1 black. The correct guard is `if (t < startMs || t >= endMs) return hidden`.
6. **Body = exact pixel dimensions.** Width and height are integers (`1080px`, `1920px`). No `%`, `vw/vh`, or responsive units.
7. **No two scenes visible simultaneously** (except 10% enter overlap). All scenes `opacity: 0` outside their renderFrame window.
8. **Transitions use `opacity` only.** No `display` toggle, no `visibility` — GPU-composited opacity is frame-perfect.
9. **Never dump HTML in chat.** Save to file, show summary only.
10. **Title states the message, not the topic.** "3 Reasons Q4 Crushed Targets" not "Q4 2024 Performance Video".
11. **Read `references/scene-library.md` before generating ANY HTML.** Use exact HTML structure and CSS class names from that file.

---

## Step 1: Intake

**Required:** `content_brief`

**Optional parameters and defaults:**

| Parameter | Default | Description |
|---|---|---|
| content_brief | — | Text describing what the video communicates (required) |
| scenes | auto | Number of scenes (1–6). Auto = derived from brief. |
| duration_per_scene | 3s | Duration per scene in seconds (1–8s) |
| style | kinetic-dark | kinetic-dark / editorial-light / data-pulse / bold-type / minimal-clean |
| aspect_ratio | 1:1 | 1:1 (1080×1080) / 16:9 (1920×1080) / 9:16 (1080×1920) |
| fps | 30 | Frames per second (24, 30, or 60) |
| music | none | Path to audio file for background track (mp3/m4a/wav) |
| source | — | Source attribution shown in final frame footer |

**If `content_brief` is missing, ask exactly:**

> "To create the video, I need a content brief — what should the video communicate?
>
> Example: 'Show 3 reasons why Q4 revenue grew 85%: new enterprise deals, reduced churn, price increase. Use bold numbers. Style: data-pulse.'
>
> Optional: style (default: kinetic-dark), aspect ratio (default: 1:1), seconds per scene (default: 3s)"

If `content_brief` is present → proceed to Step 2 immediately.

---

## Step 2: Internal Architecture (never shown to user)

**1. Parse brief into scenes (max 6):**
- Scene 1 = hook or title (always)
- Scenes 2–N-1 = supporting points, metrics, or story beats
- Scene N = CTA or closing summary (always, if more than 1 scene)
- One key idea per scene — if brief has 7+ ideas, consolidate the weakest ones

**2. Read `references/scene-library.md`** — choose scene type for each scene:
- Hook/opening → `title-card`
- Single metric → `stat-reveal`
- List of 2–4 points → `bullet-list`
- Before vs after / two values → `split-screen`
- Testimonial / quote → `quote-card`
- Final / CTA → `cta-card`

**3. Read `references/style-presets.md`** — load CSS tokens + animation personality for chosen style.

**4. Calculate timing:**
```
totalDuration = sceneCount × duration_per_scene  (seconds)
totalFrames   = totalDuration × fps
```
Each scene occupies `(100 / sceneCount)%` of the total `@keyframes` range.

| Scene | Start % | End % |
|---|---|---|
| 1 | 0% | (100/N)% |
| 2 | (100/N)% | (200/N)% |
| … | … | … |
| N | ((N-1)×100/N)% | 100% |

Within each scene's range:
- Enter: first 10% of scene range
- Hold: 10% to 85% of scene range
- Exit: 85% to 100% of scene range

**5. Determine pixel dimensions:**
- `1:1` → W=1080, H=1080
- `16:9` → W=1920, H=1080
- `9:16` → W=1080, H=1920

---

## Step 3: HTML Generation

Read `references/scene-library.md` AND `references/style-presets.md` before writing any code.

**Required HTML structure:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
[font CDN link from style preset]
<style>
:root {
  [all CSS tokens from style preset]
}

*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
html, body {
  width: [W]px; height: [H]px;
  overflow: hidden;
  background: var(--bg);
  font-family: var(--font-body);
  position: relative;
}

.scene {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px;
  opacity: 0;
  will-change: opacity, transform;
}
.scene-inner {
  width: 100%;
  max-width: 960px;
}

/* Scene-type CSS from scene-library.md */
[paste scene-type CSS here]
</style>
</head>
<body>

<div class="scene scene-1">
  <div class="scene-inner">
    [scene 1 HTML from scene-library.md template]
  </div>
</div>

[repeat for each scene]

<script>
window.__videoReady = false;
window.TOTAL_DURATION_MS = [totalDuration * 1000];

// ── Animation helpers ─────────────────────────────────────────────────────────
function lerp(a, b, p) { return a + (b - a) * p; }
function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
function easeOutCubic(t) { return 1 - Math.pow(1 - clamp(t, 0, 1), 3); }

function sceneState(t, startMs, endMs) {
  if (t < startMs || t >= endMs) return { opacity: 0, ty: 0 };
  const prog = (t - startMs) / (endMs - startMs);
  if (prog < 0.10) {
    const p = easeOutCubic(prog / 0.10);
    return { opacity: p, ty: lerp(24, 0, p) };
  }
  if (prog < 0.85) return { opacity: 1, ty: 0 };
  const p = (prog - 0.85) / 0.15;
  return { opacity: 1 - p, ty: lerp(0, -12, p) };
}

function applySceneState(el, state) {
  el.style.opacity = state.opacity;
  el.style.transform = state.ty !== 0 ? `translateY(${state.ty.toFixed(2)}px)` : '';
}

// ── Main render function — called by Playwright once per frame ────────────────
window.renderFrame = function(t) {
  // Scene 1: 0ms – [D]ms
  applySceneState(document.querySelector('.scene-1'), sceneState(t, 0, [D]));
  // Scene 2: [D]ms – [2D]ms
  applySceneState(document.querySelector('.scene-2'), sceneState(t, [D], [2D]));
  // ... repeat per scene ...
};

// ── Preview loop — stopped by Playwright before frame capture ─────────────────
let __previewActive = false;
let __previewRafId = null;
window.__stopPreview = function() {
  __previewActive = false;
  if (__previewRafId !== null) { cancelAnimationFrame(__previewRafId); __previewRafId = null; }
};

document.fonts.ready.then(() => {
  window.renderFrame(0);
  window.__videoReady = true;
  __previewActive = true;
  const startTime = performance.now();
  function previewTick() {
    if (!__previewActive) return;
    const elapsed = performance.now() - startTime;
    if (elapsed < window.TOTAL_DURATION_MS) {
      window.renderFrame(elapsed);
      __previewRafId = requestAnimationFrame(previewTick);
    } else {
      window.renderFrame(window.TOTAL_DURATION_MS - 1);
      __previewActive = false;
    }
  }
  __previewRafId = requestAnimationFrame(previewTick);
});
</script>
</body>
</html>
```

**Design quality rules:**
- Headline font size: never smaller than 60px — text must read at mobile thumbnail size
- Numbers and stats: always the largest element on screen (120–200px)
- Tight letter-spacing on display type: `-0.02em` to `-0.04em`
- One accent color per scene — don't scatter accent across multiple elements
- Dark presets: dividers `rgba(255,255,255,0.10)`, never solid
- Light presets: dividers `rgba(0,0,0,0.10)`, never solid
- `transform-origin: center center` on every element that uses `transform`
- Padding inside `.scene`: minimum 80px — never let text touch viewport edges

---

## Step 4: Self-QA (fix every failure before Step 5)

**renderFrame correctness:**
- [ ] `window.renderFrame(t)` defined — pure function, no side effects outside style writes
- [ ] Scene boundary uses `t < startMs` (not `t <= startMs`) — avoids black frame 0
- [ ] Zero instances of `animation-delay` or `@keyframes` for scene transitions
- [ ] No two scenes have overlapping `opacity: 1` windows (except 10% enter overlap)
- [ ] `window.__stopPreview()` exposed and preview rAF loop checks `__previewActive`

**Readiness signal:**
- [ ] `window.__videoReady = false` declared before `document.fonts.ready`
- [ ] `window.__videoReady = true` set ONLY inside `document.fonts.ready.then(...)`
- [ ] `window.renderFrame(0)` called inside `document.fonts.ready.then(...)` before setting `__videoReady = true`

**Layout:**
- [ ] `html, body` use exact pixel dimensions (`[W]px`, `[H]px`)
- [ ] No `%`, `vw`, `vh`, `rem` units on `body` width/height
- [ ] `overflow: hidden` on `html, body`
- [ ] All scenes `position: absolute; inset: 0`

**Design:**
- [ ] All colors from style preset tokens — no free hex values
- [ ] All fonts from style preset — no free font-family strings
- [ ] Headline font size ≥ 60px
- [ ] Source in final scene if `source` param provided

---

## Step 5: Export

Determine slug from brief content (kebab-case, ≤30 chars):
```bash
mkdir -p chart/[slug]
```

Save HTML: `chart/[slug]/video.html`

Browser preview:
```bash
open chart/[slug]/video.html
```

Run export (replace `[skill-root]` with path to this skill's directory):
```bash
bash [skill-root]/scripts/export-video.sh \
  chart/[slug]/video.html \
  chart/[slug]/video.mp4 \
  --duration [totalDuration] \
  --fps [fps] \
  --width [W] \
  --height [H] \
  [--music path/to/audio.mp3]
```

The script installs Playwright on first run (~200MB Chromium), captures all frames, then assembles MP4 with FFmpeg.

---

## Step 6: Output Summary

```
## Video: [title from brief]
Date: [YYYY-MM-DD] | Scenes: [N] | Style: [style] | Aspect: [ratio]
Duration: [N]s | FPS: [fps] | Frames: [N]

Files
  Source:   chart/[slug]/video.html
  Output:   chart/[slug]/video.mp4
  Size:     [X] MB

Checklist
- [ ] All scenes appear in sequence with no blank frames
- [ ] Text legible at mobile thumbnail size
- [ ] Scene transitions smooth (no jump cuts)
- [ ] Final scene includes CTA or closing message
- [ ] Source attribution present in final frame (if provided)
```

---

## Prompt Tips (show when user asks for guidance)

> "Provide a content brief — bullet points of what each scene should say."
>
> "Name the insight directly. '3 reasons Q4 grew 85%' gives the video a spine."
>
> "Mention the style if you have a preference: kinetic-dark (default), editorial-light, data-pulse, bold-type, minimal-clean."
>
> "Specify aspect ratio for the platform: 1:1 for LinkedIn/Instagram feed, 9:16 for Stories/Reels, 16:9 for YouTube/presentations."
>
> ✅ Good: "Create a 9-second video. Q4 revenue hit $4.2M (85% growth). Drivers: enterprise deals, churn 1.2%, price increase. CTA: acme.com/q4. Style: data-pulse. Aspect: 1:1."
>
> ❌ Bad: "make a video about our company"
