---
name: vid-product-launch
description: Generates a cinematic product launch video (MP4) from a product description and launch context. 5-section narrative arc — Tease, Build, Reveal, Proof, CTA — rendered as HTML/CSS in headless Chromium via Playwright, assembled with FFmpeg. 4 tone presets. 30/60/90 second durations. Trigger when user says "product launch video", "launch video", "product reveal video", "cinematic product video", "product announcement video", or "launch day video".
compatibility: [claude-code, gemini-cli, github-copilot]
author: OpenDirectory
version: 1.2.0
---

# vid-product-launch

Generates a narrative MP4 product launch video from a product description and launch context.
Pipeline: HTML/CSS animations → headless Chromium (Playwright, frame-by-frame) → FFmpeg (H.264 MP4).
No React. No AI video APIs. No Python. Zero runtime cost beyond Playwright + FFmpeg.

---

## Critical Rules (read before every generation)

1. **The tagline is not optional. Do not skip it.** It is the product's entire promise in 4–6 words. If the user did not provide it, derive one from the description — a sharp, active-voice distillation. Never write "[tagline here]" or leave it blank.

2. **The reveal moment must feel earned.** The tease and build sections exist to create tension. If the product name appears in the first 20% of the video, the narrative collapses. Never reveal the product name before the Reveal section.

3. **product_name font size: minimum 120px for 16:9, minimum 80px for 9:16.** The name must be the largest element at the reveal moment. If it isn't dominant, the reveal fails.

4. **One proof stat. Not a list.** If the user provides multiple stats, pick the strongest one. A list of 5 numbers destroys the punch. One oversized number creates it.

5. **Use `window.renderFrame(t)` — no CSS `@keyframes` for scene transitions.** CSS `currentTime` seeking is silently ignored for backward seeks in Chromium. The renderFrame function computes element styles directly from milliseconds. Playwright calls it once per frame.

6. **No `animation-delay` on ANY element.** Not needed with renderFrame. If you write `animation-delay`, stop — you are using the wrong architecture.

7. **`window.__videoReady = true` only inside `document.fonts.ready.then(...)`.** Never set synchronously.

8. **Expose `window.__stopPreview()`.** The rAF preview loop races with Playwright's evaluate/screenshot calls. The capture script calls `__stopPreview()` before the frame loop.

9. **Use `t < startMs` (not `t <= startMs`) in scene boundary checks.** `t <= 0` at frame 0 makes scene 1 black.

10. **Body = exact pixel dimensions.** Width and height are integers. No `%`, `vw/vh`, `rem`.

11. **Read `references/scene-library.md` AND `references/style-presets.md` before generating ANY HTML.**

12. **Never dump HTML in chat.** Save to file. Show summary only.

13. **Film grain canvas MUST be 240×135, not W×H.** Set `width="240" height="135"` on the canvas element, then stretch with `style="width:[W]px;height:[H]px"`. Full-resolution grain at 1920×1080 is 64× slower — 8MB of ImageData per frame — and will make 1800-frame exports take hours.

14. **The tease section MUST be dark (#000 or near-black), regardless of tone.** White backgrounds in the tease section read as demo slides, not product launch videos. The dark-to-light narrative arc (dark tease → dark build → product reveal) is how launch videos create drama. Even the `minimal` and `energetic` presets should use `background: #000` for tease-problem and tension-build scenes.

15. **Each tease word must be its own beat at 200px+ font size.** Word-by-word on a single line is not punchy enough. Each problem word (e.g. "Research." / "Write." / "Outreach." / "Repeat.") gets 1500–1800ms of screen time at `font-size: 200px; font-weight: 900` centered, one at a time. See scene-library.md `tease-words` pattern.

16. **Build section must show content that narrates the problem — not just particles.** Use the `terminal-card` pattern: 3 cards appear sequentially with a typewriter animation showing the manual work being done. Cards have `border: 1px solid rgba(255,255,255,0.07)`, blue dot accent, monospace text. Particles alone for 20 seconds is empty screen time.

17. **Dot-grid CSS background on dark scenes.** Add `background-image: radial-gradient(circle, rgba(255,255,255,0.035) 1px, transparent 1px); background-size: 60px 60px;` to build, reveal, proof, and CTA scenes. It costs zero compute and adds depth.

---

## Step 1: Intake

**Required:**
- `product_name` — the name of the product or feature being launched
- `product_description` — 2–3 sentences: what it does, who it's for, key benefit

**Optional parameters and defaults:**

| Parameter | Default | Description |
|---|---|---|
| tagline | auto | 4–6 words — the product's core promise |
| problem_statement | auto-inferred | 1 sentence for tease section (the pain the product solves) |
| proof_stat | auto-inferred | Single metric (e.g. "500+ teams", "10× faster", "$2M saved") |
| cta | auto | URL or action phrase (e.g. "opendirectory.dev", "Join the waitlist") |
| launch_date | — | ISO date string (enables countdown-card scene) |
| tone | cinematic | cinematic / energetic / minimal / emotional |
| duration | 60 | 30 / 60 / 90 (seconds) |
| aspect_ratio | 16:9 | 16:9 (1920×1080) / 9:16 (1080×1920) |
| letterbox | false | Cinematic 2.35:1 black bars — 16:9 only |
| music | — | Path to audio file (mp3/m4a/wav) |
| fps | 30 | Frames per second (24, 30, or 60) |

**If `product_name` or `product_description` is missing, ask exactly:**

> "To create the launch video, I need two things:
>
> 1. **Product name** — what is the product called?
> 2. **Product description** — 2–3 sentences: what does it do, who is it for, what is the key benefit?
>
> Optional: tagline (4–6 words), proof stat (one number), CTA (URL or action phrase), tone (cinematic / energetic / minimal / emotional), duration (30 / 60 / 90s)."

If both are present → proceed to Step 2 immediately.

---

## Step 2: Internal Architecture (never shown to user)

**1. Derive missing params:**
- **tagline** (if not provided): Write one from product_description. 4–6 words. Active voice. No filler ("The future of…", "Introducing…"). Derive the sharpest possible promise.
- **problem_statement** (if not provided): Infer from product_description. 1 sentence stating the pain. Never mentions the product name. Written to make the audience nod in recognition.
- **proof_stat** (if not provided): Infer from product_description. If no stat is available, use a credible scale indicator ("Trusted by 500+ teams", "From days to minutes").
- **cta** (if not provided): Use product domain if inferable from product_name, or "Learn more" as action phrase.

**2. Calculate section timing from `duration`:**

| Section | 30s | 60s | 90s | Start formula |
|---|---|---|---|---|
| Tease | 0–5s | 0–10s | 0–15s | 0ms |
| Build | 5–12s | 10–30s | 15–40s | Tease end |
| Reveal | 12–20s | 30–45s | 40–60s | Build end |
| Proof | 20–25s | 45–55s | 60–75s | Reveal end |
| CTA | 25–30s | 55–60s | 75–90s | Proof end |

Convert every boundary to milliseconds. Assign to constants:
```
TEASE_START_MS, TEASE_END_MS
BUILD_START_MS, BUILD_END_MS
REVEAL_START_MS, REVEAL_END_MS
PROOF_START_MS, PROOF_END_MS
CTA_START_MS, CTA_END_MS
```

**3. Select scenes per section:**

- **Tease:** Always starts with `blackout-opener` (1500ms). Then `tease-words` (each problem keyword as its own 1600–1800ms beat at 200px+). If `launch_date` provided, optionally add `countdown-card` at end of tease.
- **Build:** `terminal-card` sequence (3 cards showing manual tasks being typed in) + optional closing accent line. Duration ≥ 30s gets all 3 cards. Duration = 30s uses 2 cards. Never use bare particles-only for more than 5s — the screen must show content that narrates the problem.
- **Reveal:** `reveal-hero` — always first in this section. Optionally followed by `tagline-card` if duration ≥ 60s.
- **Proof:** `proof-stat` if a numeric stat is available. Otherwise `feature-bullet`.
- **CTA:** `cta-card` — always, always last.

Typical scene counts: 30s = 4 scenes, 60s = 6–7 scenes, 90s = 7–8 scenes.

**4. Calculate per-scene timing:**
Within each section, divide time equally across scenes in that section.
Exception: `blackout-opener` always gets exactly the first 1500ms of Tease.

**5. Determine pixel dimensions:**
- `16:9` → W=1920, H=1080
- `9:16` → W=1080, H=1920

**6. Letterbox calculation (if enabled, 16:9 only):**
- 2.35:1 content height = W / 2.35 = 1920 / 2.35 ≈ 817px
- Bar height = (H - 817) / 2 = (1080 - 817) / 2 ≈ 132px
- Top bar: `top: 0; height: 132px`
- Bottom bar: `bottom: 0; height: 132px`

**7. Cinematic effects flags (by preset):**
- `cinematic`: film-grain=ON (canvas 240×135, opacity 0.025), vignette=ON, light-leak=ON (warm gold), dot-grid=ON on dark scenes
- `energetic`: film-grain=OFF, vignette=OFF, dot-grid=ON, white flash at reveal
- `minimal`: film-grain=ON (canvas 240×135, opacity 0.022), vignette=ON (subtle, 0.5 radial), dot-grid=ON, no light-leak — accent color = #4B9FFF (electric blue)
- `emotional`: film-grain=ON (canvas 240×135, opacity 0.018, warm tint blend), vignette=ON (soft), light-leak=ON (copper warm), dot-grid=OFF

**All presets: tease and build scenes ALWAYS use dark background (#000 or near-black), regardless of preset.**

**8. Embed `window.__sfxTimeline` in the HTML (always — even when no music is provided):**

The export script reads this array, synthesizes each SFX type natively with FFmpeg `aevalsrc`/`anoisesrc`, and places events at exact millisecond offsets using `adelay`. No external audio files required.

SFX type reference:

| Type | Sound | Duration | Notes |
|---|---|---|---|
| `word-hit` | Sub punch (50Hz) + transient click (2.2kHz) + noise burst | 180ms | One per tease word — 3 layers via amix |
| `type-sequence` | Mechanical keyboard clicks at 15Hz (sin^30 pulse envelope) | 1.9s | One per card — runs for full TYPE_DUR |
| `whoosh` | Two-band noise sweep (1.1kHz body + 4–8kHz air) | 700ms | At `BUILD_CLOSE` transition |
| `tension-riser` | Low rumble (250Hz) + sub tone growing with t/2.8 ramp | 2.9s | Start at `BUILD_CLOSE + 700ms` — peaks at `REVEAL_START` |
| `reveal-boom` | Sub (45Hz) + body (90Hz) + shimmer (4.5–11kHz) + 85ms echo | 900ms | Exactly at `REVEAL_START` — THE hit |
| `counter-tick` | Harmonic click (880Hz + 440Hz + 1760Hz + 2640Hz) | 80ms | 3 beats — decrescendo 0.32 → 0.26 → 0.20 |
| `cta-chime` | A major chord (440 + 554 + 659 + 880Hz) + aecho bell shimmer | 1.2s | Exactly at `CTA_START` |

SFX timing map — compute `ms` values from section constants, never hardcode:

```js
window.__sfxTimeline = [
  // ── TEASE: one word-hit per word beat, last louder ───────────────────────
  { ms: WORD_BEATS[0].start,   sfx: 'word-hit',      vol: 0.55 },
  { ms: WORD_BEATS[1].start,   sfx: 'word-hit',      vol: 0.55 },
  { ms: WORD_BEATS[2].start,   sfx: 'word-hit',      vol: 0.55 },
  { ms: WORD_BEATS[N].start,   sfx: 'word-hit',      vol: 0.65 },  // last word louder

  // ── BUILD: type-sequence per card (1.9s, matches TYPE_DUR 1800ms) ────────
  { ms: CARDS[0].start + 180,  sfx: 'type-sequence', vol: 0.28 },
  { ms: CARDS[1].start + 180,  sfx: 'type-sequence', vol: 0.28 },
  { ms: CARDS[2].start + 180,  sfx: 'type-sequence', vol: 0.28 },

  // ── TRANSITION: whoosh then 2.9s riser peaking at REVEAL_START ───────────
  { ms: BUILD_CLOSE,           sfx: 'whoosh',        vol: 0.50 },
  { ms: BUILD_CLOSE + 700,     sfx: 'tension-riser', vol: 0.35 },

  // ── REVEAL: the cinematic hit ─────────────────────────────────────────────
  { ms: REVEAL_START,          sfx: 'reveal-boom',   vol: 0.88 },

  // ── PROOF: harmonic ticks, decrescendo ───────────────────────────────────
  { ms: PROOF_START,           sfx: 'counter-tick',  vol: 0.32 },
  { ms: PROOF_START + 2200,    sfx: 'counter-tick',  vol: 0.26 },
  { ms: PROOF_START + 4400,    sfx: 'counter-tick',  vol: 0.20 },

  // ── CTA: A major chord landing ────────────────────────────────────────────
  { ms: CTA_START,             sfx: 'cta-chime',     vol: 0.62 },
];
```

Place this block immediately before the preview loop, after `window.renderFrame`.

---

## Step 3: HTML Generation

Read `references/scene-library.md` AND `references/style-presets.md` before writing any code.
Use the exact CSS class names, HTML structure, and renderFrame patterns from those files.

**Required HTML skeleton:**

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
  max-width: 1200px;
}

[paste CSS from each scene type in scene-library.md]
</style>
</head>
<body>

<!-- Cinematic overlay elements — rendered on top of all scenes -->
[if film-grain: ON]
<canvas id="grain-overlay"
  width="[W]" height="[H]"
  style="position:fixed;inset:0;pointer-events:none;opacity:0.025;mix-blend-mode:overlay;z-index:50"></canvas>
[end if]

[if vignette: ON]
<div id="vignette-overlay"
  style="position:fixed;inset:0;background:radial-gradient(ellipse at center,transparent 35%,rgba(0,0,0,0.65) 100%);pointer-events:none;z-index:51"></div>
[end if]

[if light-leak: ON]
<div id="light-leak"
  style="position:fixed;inset:0;background:linear-gradient(135deg,rgba(255,220,140,0.5) 0%,rgba(255,255,255,0.3) 45%,transparent 70%);opacity:0;pointer-events:none;z-index:52"></div>
[end if]

[if letterbox: ON]
<div id="lbox-top" style="position:fixed;top:0;left:0;width:[W]px;height:132px;background:#000;z-index:100"></div>
<div id="lbox-bot" style="position:fixed;bottom:0;left:0;width:[W]px;height:132px;background:#000;z-index:100"></div>
[end if]

<!-- Scenes -->
[scene HTML from scene-library.md templates, one per selected scene]

<script>
window.__videoReady = false;
window.TOTAL_DURATION_MS = [duration * 1000];

// ── Section timing constants ──────────────────────────────────────────────────
const TEASE_START_MS  = [N];
const TEASE_END_MS    = [N];
const BUILD_START_MS  = [N];
const BUILD_END_MS    = [N];
const REVEAL_START_MS = [N];
const REVEAL_END_MS   = [N];
const PROOF_START_MS  = [N];
const PROOF_END_MS    = [N];
const CTA_START_MS    = [N];
const CTA_END_MS      = [N];

// ── Animation helpers ─────────────────────────────────────────────────────────
function lerp(a, b, p) { return a + (b - a) * p; }
function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
function easeOutCubic(t) { return 1 - Math.pow(1 - clamp(t, 0, 1), 3); }
function easeInOutCubic(t) { return t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t+2,3)/2; }

function sceneState(t, startMs, endMs) {
  // Standard scene envelope: fade-in, hold, fade-out
  if (t < startMs || t >= endMs) return { opacity: 0, ty: 0 };
  const prog = (t - startMs) / (endMs - startMs);
  if (prog < 0.10) {
    const p = easeOutCubic(prog / 0.10);
    return { opacity: p, ty: lerp(20, 0, p) };
  }
  if (prog < 0.88) return { opacity: 1, ty: 0 };
  // CTA scene: no exit fade (holds until end)
  if (startMs === CTA_START_MS) return { opacity: 1, ty: 0 };
  const p = (prog - 0.88) / 0.12;
  return { opacity: 1 - easeOutCubic(p), ty: lerp(0, -10, p) };
}

function applySceneState(el, state) {
  el.style.opacity = state.opacity.toFixed(3);
  el.style.transform = state.ty !== 0 ? `translateY(${state.ty.toFixed(2)}px)` : '';
}

// ── Film grain (if enabled) ───────────────────────────────────────────────────
[if film-grain: ON]
const grainCanvas = document.getElementById('grain-overlay');
const grainCtx = grainCanvas ? grainCanvas.getContext('2d') : null;
const W_GRAIN = [W], H_GRAIN = [H];
function renderGrain(t) {
  if (!grainCtx) return;
  const d = grainCtx.createImageData(W_GRAIN, H_GRAIN);
  const buf = d.data;
  let seed = (Math.floor(t * 37) ^ 0x5E3779B9) >>> 0;
  for (let i = 0; i < buf.length; i += 4) {
    seed = (seed ^ (seed >>> 13)) >>> 0;
    seed = (seed * 1664525 + 1013904223) >>> 0;
    const n = seed >>> 24;
    buf[i] = buf[i+1] = buf[i+2] = n;
    buf[i+3] = 255;
  }
  grainCtx.putImageData(d, 0, 0);
}
[end if]

// ── Light leak (if enabled) ───────────────────────────────────────────────────
[if light-leak: ON]
const lightLeakEl = document.getElementById('light-leak');
function renderLightLeak(t) {
  if (!lightLeakEl) return;
  const leakStart = REVEAL_START_MS;
  const leakDur = 500; // ms
  const lt = t - leakStart;
  if (lt < 0 || lt > leakDur) { lightLeakEl.style.opacity = 0; return; }
  const p = lt / leakDur;
  const v = p < 0.35 ? p / 0.35 : 1 - (p - 0.35) / 0.65;
  lightLeakEl.style.opacity = (v * 0.55).toFixed(3);
}
[end if]

// ── Main render function ──────────────────────────────────────────────────────
window.renderFrame = function(t) {

  // Cinematic overlays
  [if film-grain: ON] renderGrain(t); [end if]
  [if light-leak: ON] renderLightLeak(t); [end if]

  // ── TEASE SECTION ──
  // blackout-opener
  applySceneState(document.querySelector('.blackout-opener'), sceneState(t, TEASE_START_MS, TEASE_START_MS + 1500));
  // Opener line appears at 40% of its scene
  const openerLine = document.querySelector('.opener-line');
  if (openerLine) {
    const opP = clamp((t - (TEASE_START_MS + 600)) / 500, 0, 1);
    openerLine.style.opacity = easeOutCubic(opP).toFixed(3);
    openerLine.style.transform = `translateY(${lerp(8, 0, easeOutCubic(opP)).toFixed(2)}px)`;
  }

  // tease-problem
  const tpScene = document.querySelector('.tease-problem');
  const tpStart = TEASE_START_MS + 1500;
  const tpEnd = TEASE_END_MS;
  applySceneState(tpScene, sceneState(t, tpStart, tpEnd));
  const words = tpScene ? tpScene.querySelectorAll('.word') : [];
  if (words.length) {
    const stagger = 180, revealStart = tpStart + (tpEnd - tpStart) * 0.15;
    words.forEach((w, i) => {
      const ws = revealStart + i * stagger;
      const wp = clamp((t - ws) / 350, 0, 1);
      w.style.opacity = easeOutCubic(wp).toFixed(3);
      w.style.transform = `translateY(${lerp(20, 0, easeOutCubic(wp)).toFixed(2)}px)`;
    });
    const subLine = tpScene.querySelector('.sub-line');
    if (subLine) {
      const slStart = revealStart + words.length * stagger + 200;
      const slP = clamp((t - slStart) / 400, 0, 1);
      subLine.style.opacity = easeOutCubic(slP).toFixed(3);
    }
  }

  [if countdown-card exists in this video]
  // countdown-card (in tease)
  const cdScene = document.querySelector('.countdown-card');
  if (cdScene) {
    applySceneState(cdScene, sceneState(t, [CD_START_MS], [CD_END_MS]));
    const cdLabel = document.getElementById('cd-label');
    const cdGrid  = document.getElementById('cd-grid');
    const cdDate  = document.getElementById('cd-date');
    if (cdLabel) cdLabel.style.opacity = easeOutCubic(clamp((t - [CD_START_MS]) / 300, 0, 1)).toFixed(3);
    if (cdGrid)  cdGrid.style.opacity  = easeOutCubic(clamp((t - ([CD_START_MS] + 200)) / 400, 0, 1)).toFixed(3);
    if (cdDate)  cdDate.style.opacity  = easeOutCubic(clamp((t - ([CD_START_MS] + 600)) / 400, 0, 1)).toFixed(3);
  }
  [end if]

  // ── BUILD SECTION ──
  // tension-build
  const tbScene = document.querySelector('.tension-build');
  applySceneState(tbScene, sceneState(t, BUILD_START_MS, BUILD_END_MS));
  if (tbScene) {
    // Particle canvas — agent replaces accent hex with literal preset color
    const tbCanvas = document.getElementById('tension-canvas');
    if (tbCanvas && t >= BUILD_START_MS && t < BUILD_END_MS) {
      const tbCtx = tbCanvas.getContext('2d');
      if (!window.__tensionParticles) {
        window.__tensionParticles = Array.from({length: 60}, () => ({
          x: Math.random() * [W], y: Math.random() * [H],
          tx: [W]/2 + (Math.random()-0.5)*60, ty: [H]/2 + (Math.random()-0.5)*60,
          r: Math.random() * 2.5 + 1,
        }));
      }
      const prog = clamp((t - BUILD_START_MS) / (BUILD_END_MS - BUILD_START_MS), 0, 1);
      tbCtx.clearRect(0, 0, [W], [H]);
      window.__tensionParticles.forEach(p => {
        const px = lerp(p.x, p.tx, easeInOutCubic(prog));
        const py = lerp(p.y, p.ty, easeInOutCubic(prog));
        tbCtx.beginPath();
        tbCtx.arc(px, py, p.r, 0, Math.PI * 2);
        tbCtx.fillStyle = '[ACCENT_HEX_FROM_PRESET]'; // replace with literal hex
        tbCtx.globalAlpha = easeOutCubic(prog) * 0.55;
        tbCtx.fill();
        tbCtx.globalAlpha = 1;
      });
    }
    // Build counter (optional label)
    const buildCounter = document.getElementById('build-counter');
    const buildLabel = tbScene.querySelector('.build-label');
    if (buildCounter) {
      const cp = clamp((t - BUILD_START_MS) / ((BUILD_END_MS - BUILD_START_MS) * 0.65), 0, 1);
      buildCounter.style.opacity = easeOutCubic(clamp((t - BUILD_START_MS) / 300, 0, 1)).toFixed(3);
    }
    if (buildLabel) {
      buildLabel.style.opacity = easeOutCubic(clamp((t - (BUILD_START_MS + 600)) / 400, 0, 1)).toFixed(3);
    }
  }

  // ── REVEAL SECTION ──
  // reveal-hero
  const rhScene = document.querySelector('.reveal-hero');
  const rhStart = REVEAL_START_MS;
  const rhEnd   = [REVEAL_END_MS — full section if no tagline-card, else midpoint];
  applySceneState(rhScene, sceneState(t, rhStart, rhEnd));
  if (rhScene) {
    const flash   = document.getElementById('reveal-flash');
    const nameEl  = document.getElementById('product-name-el');
    const tagEl   = document.getElementById('tagline-el');

    // Flash: triangle wave over 350ms at reveal start
    if (flash) {
      const fp = clamp((t - rhStart) / 350, 0, 1);
      const fv = fp < 0.4 ? fp / 0.4 : 1 - (fp - 0.4) / 0.6;
      flash.style.opacity = (fv * 0.65).toFixed(3);
    }
    // Product name: materialise (cinematic/emotional) or slam (energetic) or fade (minimal)
    if (nameEl) {
      const nameStart = rhStart + 220;
      const nameDur = [700 for cinematic/emotional | 120 for energetic | 450 for minimal];
      const np = clamp((t - nameStart) / nameDur, 0, 1);
      nameEl.style.opacity = easeOutCubic(np).toFixed(3);
      // cinematic/emotional: blur
      // [if cinematic or emotional]
      nameEl.style.filter = `blur(${lerp(10, 0, easeOutCubic(np)).toFixed(2)}px)`;
      // [if energetic]
      // nameEl.style.transform = `scale(${lerp(1.12, 1, easeOutCubic(np)).toFixed(4)})`;
    }
    // Tagline: after name
    if (tagEl) {
      const tagStart = rhStart + 220 + [nameDur] + 150;
      const tp = clamp((t - tagStart) / 500, 0, 1);
      tagEl.style.opacity = easeOutCubic(tp).toFixed(3);
    }
  }

  [if tagline-card exists]
  // tagline-card (second beat of Reveal)
  const tcScene = document.querySelector('.tagline-card');
  applySceneState(tcScene, sceneState(t, [TC_START_MS], REVEAL_END_MS));
  if (tcScene) {
    const tcMain = document.getElementById('tagline-main');
    const tcBar  = document.getElementById('tagline-bar');
    if (tcMain) tcMain.style.opacity = easeOutCubic(clamp((t - [TC_START_MS]) / 500, 0, 1)).toFixed(3);
    if (tcBar)  tcBar.style.transform = `scaleX(${easeOutCubic(clamp((t - ([TC_START_MS]+600)) / 200, 0, 1)).toFixed(3)})`;
  }
  [end if]

  // ── PROOF SECTION ──
  [if proof-stat]
  const psScene = document.querySelector('.proof-stat');
  applySceneState(psScene, sceneState(t, PROOF_START_MS, PROOF_END_MS));
  if (psScene) {
    const statEl    = psScene.querySelector('.stat-value');
    const counterEl = document.getElementById('stat-counter');
    const labelEl   = document.getElementById('stat-label');
    const TARGET_NUM = [numeric value — agent fills this in];

    const ap = clamp((t - PROOF_START_MS) / 200, 0, 1);
    if (statEl) statEl.style.opacity = easeOutCubic(ap).toFixed(3);

    const countDur = (PROOF_END_MS - PROOF_START_MS) * 0.60;
    const cp = clamp((t - PROOF_START_MS) / countDur, 0, 1);
    if (counterEl) counterEl.textContent = Math.round(easeOutCubic(cp) * TARGET_NUM).toLocaleString();

    const labelStart = PROOF_START_MS + countDur + 80;
    if (labelEl) labelEl.style.opacity = easeOutCubic(clamp((t - labelStart) / 400, 0, 1)).toFixed(3);
  }
  [end if]

  [if feature-bullet]
  const fbScene = document.querySelector('.feature-bullet');
  applySceneState(fbScene, sceneState(t, PROOF_START_MS, PROOF_END_MS));
  if (fbScene) {
    const iconEl = document.getElementById('bullet-icon');
    const mainEl = document.getElementById('bullet-main');
    const subEl  = document.getElementById('bullet-sub');
    if (iconEl) iconEl.style.transform  = `scaleX(${easeOutCubic(clamp((t - PROOF_START_MS) / 200, 0, 1)).toFixed(3)})`;
    if (mainEl) mainEl.style.opacity    = easeOutCubic(clamp((t - (PROOF_START_MS + 200)) / 500, 0, 1)).toFixed(3);
    if (subEl)  subEl.style.opacity     = easeOutCubic(clamp((t - (PROOF_START_MS + 700)) / 400, 0, 1)).toFixed(3);
  }
  [end if]

  // ── CTA SECTION ──
  const ctaScene = document.querySelector('.cta-card');
  applySceneState(ctaScene, sceneState(t, CTA_START_MS, CTA_END_MS));
  if (ctaScene) {
    const actionEl = document.getElementById('cta-action');
    const urlEl    = document.getElementById('cta-url');
    const accentEl = document.getElementById('cta-accent');
    const subEl    = document.getElementById('cta-sub');
    if (actionEl) actionEl.style.opacity = easeOutCubic(clamp((t - CTA_START_MS) / 350, 0, 1)).toFixed(3);
    if (urlEl) {
      const up = clamp((t - (CTA_START_MS + 250)) / 500, 0, 1);
      urlEl.style.opacity = easeOutCubic(up).toFixed(3);
      // cinematic/emotional: blur reveal
      urlEl.style.filter = `blur(${lerp(6, 0, easeOutCubic(up)).toFixed(2)}px)`;
    }
    if (accentEl) accentEl.style.transform = `scaleX(${easeOutCubic(clamp((t-(CTA_START_MS+800))/200,0,1)).toFixed(3)})`;
    if (subEl) subEl.style.opacity = easeOutCubic(clamp((t-(CTA_START_MS+1050))/400,0,1)).toFixed(3);
  }
};

// ── Preview loop (stopped by Playwright before frame capture) ─────────────────
let __previewActive = false;
let __previewRafId  = null;
window.__stopPreview = function() {
  __previewActive = false;
  if (__previewRafId !== null) { cancelAnimationFrame(__previewRafId); __previewRafId = null; }
};

document.fonts.ready.then(() => {
  window.renderFrame(0);
  window.__videoReady = true;
  __previewActive = true;
  const startTime = performance.now();
  function tick() {
    if (!__previewActive) return;
    const elapsed = performance.now() - startTime;
    if (elapsed < window.TOTAL_DURATION_MS) {
      window.renderFrame(elapsed);
      __previewRafId = requestAnimationFrame(tick);
    } else {
      window.renderFrame(window.TOTAL_DURATION_MS - 1);
      __previewActive = false;
    }
  }
  __previewRafId = requestAnimationFrame(tick);
});
</script>
</body>
</html>
```

**Design quality rules:**
- `product_name` font size: ≥120px for 16:9, ≥80px for 9:16. Non-negotiable.
- Headline letter-spacing: `var(--tracking-tight)` — always.
- One accent color highlight per scene.
- `transform-origin: center center` on every element that uses `transform`.
- Padding inside `.scene`: minimum 80px — text must never touch viewport edges.
- Cinematic preset: all colors from `--` token variables. No free hex except on canvas fillStyle (replace `[ACCENT_HEX_FROM_PRESET]` with literal hex from preset).
- Never write placeholder text ("Your tagline here", "TBD", "[INSERT STAT]").

---

## Step 4: Self-QA (fix every failure before Step 5)

**Narrative structure:**
- [ ] product_name does NOT appear before `REVEAL_START_MS`
- [ ] Tagline is a real 4–6 word phrase — not a placeholder or generic line
- [ ] `reveal-hero` scene falls within `REVEAL_START_MS` to `REVEAL_END_MS`
- [ ] `cta-card` is the final scene, covering `CTA_START_MS` to `CTA_END_MS`
- [ ] CTA contains actual URL or action phrase — not "[your URL here]"

**renderFrame correctness:**
- [ ] `window.renderFrame(t)` is a pure function — no side effects outside style writes
- [ ] Scene boundary uses `t < startMs` (not `t <= startMs`)
- [ ] Zero `animation-delay` or `@keyframes` for scene transitions
- [ ] `window.__stopPreview()` exposed and checks `__previewActive` flag
- [ ] Film grain canvas re-seeds from `t` each frame (different grain per frame)

**Readiness signal:**
- [ ] `window.__videoReady = false` declared before fonts.ready
- [ ] `window.__videoReady = true` set ONLY inside `document.fonts.ready.then(...)`
- [ ] `window.renderFrame(0)` called inside fonts.ready BEFORE setting `__videoReady = true`

**Layout:**
- [ ] `html, body` use exact pixel dimensions (`[W]px`, `[H]px`)
- [ ] No `%`, `vw`, `vh`, `rem` on body width/height
- [ ] `overflow: hidden` on `html, body`
- [ ] All scenes `position: absolute; inset: 0`

**Cinematic effects:**
- [ ] Film grain canvas: `id="grain-overlay"`, `position: fixed`, above all scenes
- [ ] Vignette div: `id="vignette-overlay"`, `position: fixed`, above all scenes
- [ ] Light leak div: `id="light-leak"`, `opacity: 0` initially, fires at `REVEAL_START_MS`
- [ ] Letterbox (if enabled): exact bar heights for 2.35:1 ratio, `z-index: 100`

**Design:**
- [ ] `product_name` font size ≥ 120px (16:9) or ≥ 80px (9:16)
- [ ] All colors from preset token variables
- [ ] All fonts from preset CDN link
- [ ] No placeholder text anywhere

**Sound effects:**
- [ ] `window.__sfxTimeline` present before the preview loop
- [ ] `ms` values derived from actual timing constants — never hardcoded guesses
- [ ] `reveal-boom` fires at exactly `REVEAL_START`
- [ ] `cta-chime` fires at exactly `CTA_START`
- [ ] No SFX event fires before 1000ms (blackout silence must be true silence)
- [ ] Last tease word has `vol: 0.65` (louder than others at `0.55`)

---

## Step 5: Export

Determine slug from `product_name` (kebab-case, ≤30 chars):

```bash
mkdir -p launch/[slug]
```

Save HTML: `launch/[slug]/product-launch.html`

Open for browser preview:
```bash
open launch/[slug]/product-launch.html
```

Run export (replace `[skill-root]` with path to this skill's directory):
```bash
bash [skill-root]/scripts/export-video.sh \
  launch/[slug]/product-launch.html \
  launch/[slug]/product-launch.mp4 \
  --duration [total_duration] \
  --fps [fps] \
  --width [W] \
  --height [H] \
  [--music path/to/audio.mp3]
```

First run installs Playwright (~200MB Chromium, cached after first use) and verifies FFmpeg.

---

## Step 6: Output Summary

```
## Launch Video: [product_name]
Date: [YYYY-MM-DD] | Tone: [tone] | Duration: [N]s | Aspect: [ratio]
Sections: Tease [0–Ns] → Build [N–Ns] → Reveal [N–Ns] → Proof [N–Ns] → CTA [N–Ns]

Narrative
  Tease:  [problem_statement — 1 sentence]
  Reveal: [product_name] — "[tagline]"
  Proof:  [proof_stat]
  CTA:    [cta]

Files
  Source: launch/[slug]/product-launch.html
  Output: launch/[slug]/product-launch.mp4

Checklist
- [ ] Product name does not appear before reveal section
- [ ] Reveal moment feels distinct — flash/materialise visible
- [ ] Tagline is present and legible
- [ ] Proof stat counter animates
- [ ] CTA URL readable at final frame
- [ ] No blank frames
```

---

## Prompt Tips (show when user asks for guidance)

> "Write the tagline yourself. It is the most important 4–6 words in the video — don't AI-generate it lazily."
>
> "The reveal moment is everything. Everything before it builds tension; the reveal must feel earned."
>
> "One benefit in the proof section. Trying to show 5 features kills launch video pacing."
>
> "Match tone to your market: cinematic for B2C premium / Series A+, energetic for dev tools and SaaS, minimal for design-forward products, emotional for consumer / mission-driven."
>
> Good: "Product launch video, 60 seconds. Product: OpenDirectory. Description: A library of pre-built AI agent skills for Claude, Codex, and Gemini. Covers GTM, content, research, and developer tools. Tagline: 'AI skills, ready to install.' Tone: minimal. Proof: '52+ skills, zero setup.' CTA: 'Browse skills at opendirectory.dev.' Aspect: 16:9."
>
> ❌ Bad: "launch video for our new product"
