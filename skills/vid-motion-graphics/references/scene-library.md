# Scene Library — vid-motion-graphics

6 scene types with complete HTML/CSS templates. Read this before generating any HTML in Step 3.

Each template shows the HTML structure and required CSS classes. Apply colors and fonts from the chosen style preset (`references/style-presets.md`).

---

## Timing Architecture (read this first)

All scene timing is driven by `window.renderFrame(t)` — a pure JS function called by Playwright once per frame. It computes `opacity`/`transform` directly from the millisecond timestamp. No CSS `@keyframes`, no `animation-delay`, no Web Animations API seeking.

**Why renderFrame instead of CSS animations:**
CSS `@keyframes` `currentTime` seeking is silently ignored for backward seeks in Chromium. A 12s animation finishes during `waitUntil: 'networkidle'` (Google Fonts CDN), so all frames capture the final state. The renderFrame approach is deterministic: same `t` → same output, always.

**Scene CSS base (apply to ALL scenes):**
```css
.scene {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px;
  opacity: 0;          /* start hidden — renderFrame sets opacity per frame */
  will-change: opacity, transform;
}
```

**renderFrame helpers (include verbatim in every HTML):**
```javascript
window.__videoReady = false;
window.TOTAL_DURATION_MS = N * 1000; // total duration in ms

function lerp(a, b, p) { return a + (b - a) * p; }
function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
function easeOutCubic(t) { return 1 - Math.pow(1 - clamp(t, 0, 1), 3); }

// Returns {opacity, ty} for scene window [startMs, endMs)
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

window.renderFrame = function(t) {
  // Scene 1: 0ms → scene1DurMs
  applySceneState(document.querySelector('.scene-1'), sceneState(t, 0, scene1EndMs));
  // Scene 2: scene1EndMs → scene2EndMs
  applySceneState(document.querySelector('.scene-2'), sceneState(t, scene1EndMs, scene2EndMs));
  // ... repeat per scene
};

// Preview rAF loop — stopped by Playwright before frame capture
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
```

**Timing math for N scenes of D seconds each:**
```
scene 1: startMs = 0,             endMs = D*1000
scene 2: startMs = D*1000,        endMs = D*2000
scene N: startMs = (N-1)*D*1000,  endMs = N*D*1000
```

Within each scene's `[startMs, endMs)` window:
- Enter: first 10% → opacity 0→1, translateY 24px→0 (easeOutCubic)
- Hold: 10%–85% → opacity 1, no transform
- Exit: 85%–100% → opacity 1→0, translateY 0→-12px

---

## 1. title-card

Large headline with optional eyebrow label and subtext. Best for scene 1 (hook/intro) or final scene.

**HTML:**
```html
<div class="scene scene-N">
  <div class="scene-inner title-card">
    <div class="eyebrow">Q4 2024</div>
    <h1 class="headline">Revenue Grew 85%</h1>
    <p class="subtext">Fastest quarter in company history</p>
  </div>
</div>
```

**CSS:**
```css
.title-card {
  text-align: center;
  max-width: 900px;
}
.title-card .eyebrow {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 20px;
}
.title-card .headline {
  font-family: var(--font-display);
  font-size: clamp(72px, 10vw, 120px);
  font-weight: 700;
  color: var(--text);
  line-height: 1.0;
  letter-spacing: -0.03em;
}
.title-card .subtext {
  font-family: var(--font-body);
  font-size: 22px;
  color: var(--text-muted);
  margin-top: 24px;
  line-height: 1.5;
}
```

**Omit eyebrow or subtext if not needed** — the headline stands alone fine.

---

## 2. stat-reveal

Oversized number + label. Best for a single metric that needs maximum impact.

**HTML:**
```html
<div class="scene scene-N">
  <div class="scene-inner stat-reveal">
    <div class="stat-number">$4.2M</div>
    <div class="stat-label">New ARR this quarter</div>
    <div class="stat-context">vs $2.3M same period last year</div>
  </div>
</div>
```

**CSS:**
```css
.stat-reveal {
  text-align: center;
}
.stat-reveal .stat-number {
  font-family: var(--font-display);
  font-size: clamp(120px, 18vw, 200px);
  font-weight: 800;
  color: var(--accent);
  line-height: 0.9;
  letter-spacing: -0.04em;
}
.stat-reveal .stat-label {
  font-family: var(--font-body);
  font-size: 28px;
  font-weight: 500;
  color: var(--text);
  margin-top: 20px;
  letter-spacing: -0.01em;
}
.stat-reveal .stat-context {
  font-family: var(--font-body);
  font-size: 18px;
  color: var(--text-muted);
  margin-top: 12px;
}
```

**Omit `.stat-context` if not needed.**

---

## 3. bullet-list

2–4 short bullet points. Best for listing factors, drivers, or steps. Bullets animate in staggered within scene's keyframe window.

**HTML:**
```html
<div class="scene scene-N">
  <div class="scene-inner bullet-list">
    <h2 class="list-title">3 Drivers of Growth</h2>
    <ul class="bullets">
      <li class="bullet bullet-1">
        <span class="bullet-marker">01</span>
        <span class="bullet-text">Enterprise deals +120%</span>
      </li>
      <li class="bullet bullet-2">
        <span class="bullet-marker">02</span>
        <span class="bullet-text">Churn dropped to 1.2%</span>
      </li>
      <li class="bullet bullet-3">
        <span class="bullet-marker">03</span>
        <span class="bullet-text">Price increase fully absorbed</span>
      </li>
    </ul>
  </div>
</div>
```

**CSS:**
```css
.bullet-list {
  max-width: 800px;
  width: 100%;
}
.bullet-list .list-title {
  font-family: var(--font-display);
  font-size: 52px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 40px;
  letter-spacing: -0.02em;
}
.bullet-list .bullets {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.bullet-list .bullet {
  display: flex;
  align-items: baseline;
  gap: 20px;
  opacity: 0; /* renderFrame sets per-bullet opacity */
  will-change: opacity;
}
.bullet-list .bullet-marker {
  font-family: var(--font-mono);
  font-size: 14px;
  color: var(--accent);
  letter-spacing: 0.05em;
  min-width: 28px;
}
.bullet-list .bullet-text {
  font-family: var(--font-body);
  font-size: 32px;
  font-weight: 500;
  color: var(--text);
  line-height: 1.2;
}
```

**Stagger bullets in renderFrame:**
Add a `bulletOpacity()` helper and drive bullets from within `window.renderFrame`:

```javascript
function bulletOpacity(sceneProgress, showAtProg) {
  if (sceneProgress < showAtProg) return 0;
  if (sceneProgress < showAtProg + 0.06) return (sceneProgress - showAtProg) / 0.06;
  if (sceneProgress < 0.85) return 1;
  return clamp(1 - (sceneProgress - 0.85) / 0.15, 0, 1);
}

// Inside window.renderFrame(t), for a bullet-list scene (e.g. 6000ms–9000ms):
const sProgress = clamp((t - startMs) / (endMs - startMs), 0, 1);
const staggerOffsets = [0.10, 0.28, 0.46]; // scene-progress when each bullet appears
['.bullet-1', '.bullet-2', '.bullet-3'].forEach((cls, i) => {
  const el = document.querySelector(cls);
  if (el) el.style.opacity = bulletOpacity(sProgress, staggerOffsets[i]);
});
```

Bullet 1 appears at 10% into scene, bullet 2 at 28%, bullet 3 at 46%. All fade out with the scene exit at 85%.

---

## 4. split-screen

Left column: text/context. Right column: large number or metric. Side-by-side contrast.

**HTML:**
```html
<div class="scene scene-N">
  <div class="scene-inner split-screen">
    <div class="split-left">
      <div class="split-label">Before</div>
      <div class="split-value dim">200 req/s</div>
      <div class="split-desc">Legacy system capacity</div>
    </div>
    <div class="split-divider"></div>
    <div class="split-right">
      <div class="split-label accent">After</div>
      <div class="split-value">2,000 req/s</div>
      <div class="split-desc">Post-migration capacity</div>
    </div>
  </div>
</div>
```

**CSS:**
```css
.split-screen {
  display: flex;
  align-items: center;
  gap: 0;
  width: 100%;
  padding: 80px;
}
.split-left,
.split-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 12px;
}
.split-divider {
  width: 1px;
  height: 200px;
  background: var(--divider);
  margin: 0 40px;
  flex-shrink: 0;
}
.split-label {
  font-family: var(--font-body);
  font-size: 13px;
  letter-spacing: 0.10em;
  text-transform: uppercase;
  color: var(--text-muted);
}
.split-label.accent { color: var(--accent); }
.split-value {
  font-family: var(--font-display);
  font-size: clamp(60px, 9vw, 96px);
  font-weight: 700;
  color: var(--text);
  letter-spacing: -0.03em;
  line-height: 1.0;
}
.split-value.dim { opacity: 0.35; }
.split-desc {
  font-family: var(--font-body);
  font-size: 18px;
  color: var(--text-muted);
}
```

---

## 5. quote-card

Large pull quote with attribution. Best for testimonials, founder quotes, or key insights.

**HTML:**
```html
<div class="scene scene-N">
  <div class="scene-inner quote-card">
    <div class="quote-mark">"</div>
    <blockquote class="quote-text">
      This tool saved us 20 hours a week and paid for itself on day one.
    </blockquote>
    <div class="quote-attribution">
      <span class="quote-name">Sarah Chen</span>
      <span class="quote-role">Head of Engineering, Acme Corp</span>
    </div>
  </div>
</div>
```

**CSS:**
```css
.quote-card {
  max-width: 860px;
  text-align: center;
  position: relative;
}
.quote-card .quote-mark {
  font-family: var(--font-display);
  font-size: 120px;
  line-height: 0.6;
  color: var(--accent);
  margin-bottom: 24px;
  display: block;
}
.quote-card .quote-text {
  font-family: var(--font-display);
  font-size: clamp(32px, 5vw, 52px);
  font-weight: 600;
  color: var(--text);
  line-height: 1.25;
  letter-spacing: -0.02em;
  font-style: normal;
}
.quote-card .quote-attribution {
  margin-top: 36px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.quote-card .quote-name {
  font-family: var(--font-body);
  font-size: 18px;
  font-weight: 600;
  color: var(--text);
}
.quote-card .quote-role {
  font-family: var(--font-body);
  font-size: 15px;
  color: var(--text-muted);
}
```

---

## 6. cta-card

Final scene: brand name + call to action + URL or handle. Always the last scene.

**HTML:**
```html
<div class="scene scene-N">
  <div class="scene-inner cta-card">
    <div class="cta-brand">Acme</div>
    <div class="cta-divider"></div>
    <p class="cta-message">See the full Q4 report</p>
    <div class="cta-url">acme.com/q4-2024</div>
  </div>
</div>
```

**CSS:**
```css
.cta-card {
  text-align: center;
  align-items: center;
  gap: 0;
}
.cta-card .cta-brand {
  font-family: var(--font-display);
  font-size: 72px;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -0.04em;
}
.cta-card .cta-divider {
  width: 48px;
  height: 3px;
  background: var(--accent);
  margin: 28px auto;
}
.cta-card .cta-message {
  font-family: var(--font-body);
  font-size: 26px;
  color: var(--text-muted);
  margin-bottom: 16px;
}
.cta-card .cta-url {
  font-family: var(--font-mono);
  font-size: 28px;
  font-weight: 600;
  color: var(--accent);
  letter-spacing: -0.01em;
}
```

---

## Scene Selection Guide

| Content type | Recommended scene type |
|---|---|
| Hook / opening | title-card |
| Single metric / number | stat-reveal |
| Multiple points / list | bullet-list |
| Before vs after / two values | split-screen |
| Testimonial / quote | quote-card |
| Final / CTA / contact | cta-card |

**Max 6 scenes per video.** Beyond 6, the message fragments. If the brief has more than 6 ideas, consolidate similar points or promote the top 5 with a summary CTA.
