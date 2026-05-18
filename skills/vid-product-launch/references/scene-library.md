# Scene Library — vid-product-launch

11 scene types for the 5-section narrative arc. Read this file before generating HTML.
Each entry includes: purpose, narrative placement, CSS, HTML template, and renderFrame logic.

---

## Scene Placement by Narrative Section

```
TEASE (builds problem / curiosity):
  blackout-opener  — always first (0–1500ms of tease)
  tease-words      ★ PRIMARY — each problem keyword as its own 200px+ beat
  tease-problem    — fallback: all words together (shorter durations only)
  countdown-card   — if launch_date provided (can sit in tease OR cta)

BUILD (tension rising, solution approaching):
  terminal-card    ★ PRIMARY — 3 typed cards showing manual work being done
  tension-build    — supplemental: particles/canvas (max 5s alone, never 20s)

REVEAL (the hero moment):
  reveal-hero      — product name + tagline. The slam / materialise.
  tagline-card     — optional second reveal beat for standalone tagline

PROOF (one result, one truth):
  proof-stat       — oversized single metric with counter animation
  feature-bullet   — single capability with supporting line

CTA (close):
  cta-card         — URL large, action text. Final frame. Always last.
```

★ = preferred. Use these first. Old alternatives still valid for 30s or special cases.

---

## Visual Quality Rules (apply to every scene)

- **Dark tease/build**: `background: #000` or `#080808` always — even in minimal/energetic presets.
- **Dot-grid on dark scenes**: `background-image: radial-gradient(circle, rgba(255,255,255,0.035) 1px, transparent 1px); background-size: 60px 60px;` on build, reveal, proof, cta.
- **Film grain canvas**: `width="240" height="135"` (stretched via CSS to W×H). Never full resolution.
- **Vignette**: `radial-gradient(ellipse at center, transparent 28%, rgba(0,0,0,0.65) 100%)` fixed overlay.
- **Accent glow**: blue/gold lines get `box-shadow: 0 0 18px rgba([accent-rgb],0.45)`.
- **Typography scale**: tease words ≥ 200px. Product name ≥ 220px. Proof stat ≥ 240px. CTA URL ≥ 88px.

---

## SFX Cue Reference

Six synthesized SFX types. The export script generates all from FFmpeg `aevalsrc`/`anoisesrc` — no audio files required. Embed `window.__sfxTimeline` in the HTML before the preview loop.

| Scene | SFX Type | Trigger Moment | Vol | Character |
|---|---|---|---|---|
| `blackout-opener` | _(silence)_ | — | — | True silence — no SFX before 1000ms |
| `tease-words` | `word-hit` | Each `WORD_BEATS[i].start` | 0.55 (last: 0.65) | Sub punch (50Hz) + transient click (2.2kHz) + noise burst — 180ms, 3 layers |
| `terminal-card` | `type-sequence` | `CARDS[i].start + 180` | 0.28 | 15Hz mechanical keyboard clicks for 1.9s — sin^30 pulse × 1200Hz click + 200Hz thud |
| `terminal-card` (fade) | `whoosh` | `BUILD_CLOSE` | 0.50 | Two-band noise sweep — 1.1kHz body + 4–8kHz air, 700ms |
| _(transition)_ | `tension-riser` | `BUILD_CLOSE + 700` | 0.35 | 2.9s ascending low rumble + sub tone ramp — peaks at REVEAL_START |
| `reveal-hero` | `reveal-boom` | `REVEAL_START` (exact) | 0.88 | Sub (45Hz) + body (90Hz) + shimmer (4.5–11kHz) + 85ms echo — 900ms |
| `proof-stat` | `counter-tick` | `PROOF_START`, `+2200`, `+4400` | 0.32 → 0.20 | Harmonic click — 880Hz + 440Hz + 1760Hz + 2640Hz, 80ms. Decrescendo |
| `cta-card` | `cta-chime` | `CTA_START` (exact) | 0.62 | A major chord (440 + 554 + 659 + 880Hz) + aecho bell shimmer — 1.2s |

**Mixing rules:**
- If `--music` flag provided: music plays at 22% volume under SFX
- SFX do not duck background music — they sit on top
- `adelay` places each SFX at the exact millisecond — timing is frame-accurate

---

## 1. blackout-opener

**Purpose:** Silence before the storm. 1–2 seconds of pure darkness, then a single line
emerges from black. Sets cinematic tone immediately.

**CSS:**
```css
.blackout-opener {
  background: #000;  /* override preset bg — always black */
  align-items: center;
  justify-content: center;
}
.blackout-opener .opener-line {
  font-family: var(--font-body);
  font-size: var(--body-size);
  font-weight: 400;
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: var(--text-secondary);
  opacity: 0;
  transform: translateY(8px);
}
```

**HTML template:**
```html
<div class="scene blackout-opener">
  <div class="scene-inner" style="text-align:center">
    <p class="opener-line">[one line — year, or a short evocative phrase, or empty for pure black]</p>
  </div>
</div>
```

**renderFrame notes:**
- Scene fades in (standard sceneState opacity).
- `.opener-line` appears at 40% of scene duration: `opacity 0→1, translateY 8px→0, 600ms`.
- For pure black opener (no text): omit the `<p>` element entirely.

---

## 2. tease-problem

**Purpose:** The problem. Revealed word-by-word in all-caps. Audience recognises themselves.
Never names the product. Ends on the pain, not the solution.

**CSS:**
```css
.tease-problem {
  align-items: center;
  justify-content: center;
}
.tease-problem .problem-text {
  font-family: var(--font-display);
  font-size: 52px;
  font-weight: 700;
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: var(--text-primary);
  text-align: center;
  line-height: 1.1;
  max-width: 800px;
}
.tease-problem .problem-text .word {
  display: inline-block;
  opacity: 0;
  transform: translateY(20px);
  margin-right: 0.2em;
}
.tease-problem .sub-line {
  font-family: var(--font-body);
  font-size: var(--body-size);
  color: var(--text-secondary);
  text-align: center;
  margin-top: 24px;
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  opacity: 0;
}
```

**HTML template:**
```html
<div class="scene tease-problem">
  <div class="scene-inner" style="text-align:center">
    <p class="problem-text">
      <!-- Agent: wrap each word in a span.word -->
      <span class="word">You've</span>
      <span class="word">been</span>
      <span class="word">doing</span>
      <span class="word">this</span>
      <span class="word">the</span>
      <span class="word">hard</span>
      <span class="word">way.</span>
    </p>
    <p class="sub-line">[optional: short clarifying line, 4–6 words max]</p>
  </div>
</div>
```

**renderFrame notes:**
```javascript
// Word-by-word reveal: stagger 180ms per word, starting at 15% of scene duration
function wordReveal(words, t, sceneStart, sceneEnd) {
  const stagger = 180; // ms between words
  const revealStart = sceneStart + (sceneEnd - sceneStart) * 0.15;
  words.forEach((w, i) => {
    const wStart = revealStart + i * stagger;
    const wDur = 350;
    const p = clamp((t - wStart) / wDur, 0, 1);
    w.style.opacity = easeOutCubic(p);
    w.style.transform = `translateY(${lerp(20, 0, easeOutCubic(p)).toFixed(2)}px)`;
  });
}
// Sub-line appears after all words: delay = revealStart + wordCount * stagger + 200ms
```

---

## 3. tension-build

**Purpose:** Rising action before the reveal. No product name. Visual energy converges
toward the center — particles, a filling bar, or a count-up to a tipping point.

**CSS (particles variant — default):**
```css
.tension-build {
  align-items: center;
  justify-content: center;
}
.tension-build canvas.particles {
  position: absolute;
  inset: 0;
  opacity: 0.8;
}
.tension-build .build-label {
  font-family: var(--font-body);
  font-size: var(--body-size);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: var(--text-secondary);
  text-align: center;
  position: relative;
  z-index: 1;
  opacity: 0;
}
.tension-build .build-counter {
  font-family: var(--font-display);
  font-size: 80px;
  font-weight: 700;
  color: var(--text-primary);
  text-align: center;
  position: relative;
  z-index: 1;
  margin-bottom: 16px;
  opacity: 0;
}
```

**HTML template:**
```html
<div class="scene tension-build">
  <canvas class="particles" id="tension-canvas" width="[W]" height="[H]"></canvas>
  <div class="scene-inner" style="text-align:center;pointer-events:none">
    <p class="build-counter" id="build-counter">0</p>
    <p class="build-label">[optional: short context, e.g. "teams wasting hours daily"]</p>
  </div>
</div>
```

**renderFrame notes:**
```javascript
// Particle convergence: N particles start spread, converge to center over scene duration
// Initialise once, then animate position each frame
function renderParticles(ctx, t, sceneStart, sceneEnd, W, H) {
  if (!window.__particles) {
    window.__particles = Array.from({length: 60}, () => ({
      x: Math.random() * W, y: Math.random() * H,
      tx: W/2 + (Math.random()-0.5)*40, ty: H/2 + (Math.random()-0.5)*40,
      r: Math.random() * 2 + 1,
    }));
  }
  const prog = clamp((t - sceneStart) / (sceneEnd - sceneStart), 0, 1);
  const ease = easeOutCubic(prog);
  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = 'var(--accent)'; // resolved at runtime; use literal hex from preset
  window.__particles.forEach(p => {
    const px = lerp(p.x, p.tx, ease);
    const py = lerp(p.y, p.ty, ease);
    ctx.beginPath();
    ctx.arc(px, py, p.r, 0, Math.PI * 2);
    ctx.globalAlpha = ease * 0.6;
    ctx.fill();
  });
}
// Build counter: counts up from 0 to a number the agent specifies
// Appears at 10% of scene, completes at 70%
```

---

## 4. reveal-hero

**Purpose:** THE moment. Product name slams or materialises into view.
Everything before this built toward this frame. Make it feel earned.

**CSS:**
```css
.reveal-hero {
  align-items: center;
  justify-content: center;
}
.reveal-hero .flash-overlay {
  position: absolute;
  inset: 0;
  background: #FFFFFF;  /* cinematic/emotional: warm #FFF8F0; energetic: #FFFFFF; minimal: #FFFFFF */
  opacity: 0;
  pointer-events: none;
  z-index: 2;
}
.reveal-hero .product-name {
  font-family: var(--font-display);
  font-size: var(--product-size);  /* min 120px for 16:9, min 80px for 9:16 */
  font-weight: 900;
  letter-spacing: var(--tracking-tight);
  color: var(--text-primary);
  text-align: center;
  line-height: 0.9;
  position: relative;
  z-index: 3;
  opacity: 0;
  transform-origin: center center;
}
.reveal-hero .tagline {
  font-family: var(--font-body);
  font-size: var(--tagline-size);
  font-weight: 400;
  letter-spacing: var(--tracking-wide);
  color: var(--accent);
  text-align: center;
  margin-top: 28px;
  position: relative;
  z-index: 3;
  opacity: 0;
  text-transform: uppercase;
}
```

**HTML template:**
```html
<div class="scene reveal-hero">
  <div class="flash-overlay" id="reveal-flash"></div>
  <div class="scene-inner" style="text-align:center">
    <h1 class="product-name" id="product-name-el">[PRODUCT NAME]</h1>
    <p class="tagline" id="tagline-el">[tagline — 4–6 words]</p>
  </div>
</div>
```

**renderFrame notes:**
```javascript
// Flash fires at scene start: opacity 0→0.6→0 over 300ms
// Then product name: cinematic=materialise(700ms) | energetic=slam(120ms) | minimal=fade(400ms) | emotional=wordReveal
// Tagline: fades in 400ms after product name completes

function renderRevealHero(t, sceneStart) {
  const flash = document.getElementById('reveal-flash');
  const nameEl = document.getElementById('product-name-el');
  const tagEl = document.getElementById('tagline-el');

  // Flash: 0→peak→0 in 300ms at scene start
  const flashDur = 300;
  const fp = clamp(t - sceneStart, 0, flashDur) / flashDur;
  flash.style.opacity = (fp < 0.4 ? fp / 0.4 : (1 - (fp - 0.4) / 0.6) * 0.6).toFixed(3);

  // Product name reveal (example: materialise for cinematic)
  const nameStart = sceneStart + 200; // 200ms after flash peak
  const nameDur = 700;
  const np = clamp((t - nameStart) / nameDur, 0, 1);
  const blurVal = lerp(10, 0, easeOutCubic(np));
  nameEl.style.opacity = easeOutCubic(np).toFixed(3);
  nameEl.style.filter = `blur(${blurVal.toFixed(2)}px)`;

  // Tagline: after name completes
  const tagStart = nameStart + nameDur + 100;
  const tagDur = 500;
  const tp = clamp((t - tagStart) / tagDur, 0, 1);
  tagEl.style.opacity = easeOutCubic(tp).toFixed(3);
}
```

---

## 5. tagline-card

**Purpose:** The product's promise stated alone. Large type, nothing else. Used when the
tagline is powerful enough to hold a scene solo — or as a second Reveal beat.

**CSS:**
```css
.tagline-card {
  align-items: center;
  justify-content: center;
}
.tagline-card .main-line {
  font-family: var(--font-display);
  font-size: 64px;
  font-weight: 700;
  letter-spacing: var(--tracking-tight);
  color: var(--text-primary);
  text-align: center;
  line-height: 1.15;
  max-width: 860px;
  opacity: 0;
}
.tagline-card .accent-bar {
  width: 48px;
  height: 3px;
  background: var(--accent);
  margin: 32px auto 0;
  transform: scaleX(0);
  transform-origin: left center;
}
```

**HTML template:**
```html
<div class="scene tagline-card">
  <div class="scene-inner" style="text-align:center">
    <p class="main-line" id="tagline-main">[The tagline — 4–6 words, no punctuation at end]</p>
    <div class="accent-bar" id="tagline-bar"></div>
  </div>
</div>
```

**renderFrame notes:**
- Text: materialise or fade-up at 10% of scene.
- Accent bar: `scaleX 0→1` after text completes (200ms, `ease-out`).

---

## 6. proof-stat

**Purpose:** One number. One truth. The counter animation makes it feel earned.
No context list — one stat only. If you have multiple, pick the strongest.

**CSS:**
```css
.proof-stat {
  align-items: center;
  justify-content: center;
}
.proof-stat .stat-value {
  font-family: var(--font-display);
  font-size: var(--stat-size);
  font-weight: 900;
  letter-spacing: var(--tracking-tight);
  color: var(--text-primary);
  text-align: center;
  line-height: 0.85;
  opacity: 0;
  transform-origin: center center;
}
.proof-stat .stat-suffix {
  font-family: var(--font-display);
  font-size: calc(var(--stat-size) * 0.45);
  font-weight: 700;
  color: var(--accent);
  vertical-align: super;
  font-size: 80px;
}
.proof-stat .stat-label {
  font-family: var(--font-body);
  font-size: var(--body-size);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: var(--text-secondary);
  text-align: center;
  margin-top: 20px;
  opacity: 0;
}
```

**HTML template:**
```html
<div class="scene proof-stat">
  <div class="scene-inner" style="text-align:center">
    <p class="stat-value" id="stat-number">
      <span id="stat-counter">0</span><span class="stat-suffix">[+ or % or × — agent chooses]</span>
    </p>
    <p class="stat-label" id="stat-label">[3–6 word context, e.g. "teams ship 10× faster"]</p>
  </div>
</div>
```

**renderFrame notes:**
```javascript
// Stat value: slam-in at scene start (all presets — number always feels energetic)
// Counter: counts from 0 to TARGET over 60% of scene duration
// Label: fades in after counter completes

function renderProofStat(t, sceneStart, sceneEnd, targetNum) {
  const counterEl = document.getElementById('stat-counter');
  const statEl = document.querySelector('.stat-value');
  const labelEl = document.getElementById('stat-label');

  // Appear at scene start
  const appearDur = 180;
  const ap = clamp((t - sceneStart) / appearDur, 0, 1);
  statEl.style.opacity = easeOutCubic(ap).toFixed(3);

  // Counter runs from 0 to targetNum over 60% of scene
  const countDur = (sceneEnd - sceneStart) * 0.60;
  const cp = clamp((t - sceneStart) / countDur, 0, 1);
  counterEl.textContent = Math.round(easeOutCubic(cp) * targetNum).toLocaleString();

  // Label appears when counter completes
  const labelStart = sceneStart + countDur + 100;
  const lp = clamp((t - labelStart) / 400, 0, 1);
  labelEl.style.opacity = easeOutCubic(lp).toFixed(3);
}
```

---

## 7. feature-bullet

**Purpose:** Single product capability with one line of context. Used in Proof section
when the proof is qualitative rather than numerical.

**CSS:**
```css
.feature-bullet {
  align-items: center;
  justify-content: center;
}
.feature-bullet .bullet-icon {
  width: 48px;
  height: 3px;
  background: var(--accent);
  margin: 0 auto 40px;
  transform: scaleX(0);
  transform-origin: left center;
}
.feature-bullet .bullet-main {
  font-family: var(--font-display);
  font-size: 60px;
  font-weight: 700;
  letter-spacing: var(--tracking-tight);
  color: var(--text-primary);
  text-align: center;
  line-height: 1.1;
  max-width: 800px;
  opacity: 0;
}
.feature-bullet .bullet-sub {
  font-family: var(--font-body);
  font-size: var(--body-size);
  color: var(--text-secondary);
  text-align: center;
  margin-top: 20px;
  max-width: 640px;
  line-height: 1.6;
  opacity: 0;
}
```

**HTML template:**
```html
<div class="scene feature-bullet">
  <div class="scene-inner" style="text-align:center">
    <div class="bullet-icon" id="bullet-icon"></div>
    <p class="bullet-main" id="bullet-main">[the capability — 4–8 words]</p>
    <p class="bullet-sub" id="bullet-sub">[supporting context — 1 sentence, 10–15 words]</p>
  </div>
</div>
```

**renderFrame notes:**
- Icon bar: `scaleX 0→1` at scene start over 200ms.
- Main text: materialise/fade at 200ms.
- Sub text: fade after main completes.

---

## 8. countdown-card

**Purpose:** Countdown to launch date. Visual tension device. Can appear in Tease OR as
a scene within CTA. Agent sets values at generation time based on current date vs launch_date.

**CSS:**
```css
.countdown-card {
  align-items: center;
  justify-content: center;
}
.countdown-card .countdown-label {
  font-family: var(--font-body);
  font-size: var(--body-size);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: var(--text-secondary);
  text-align: center;
  margin-bottom: 40px;
  opacity: 0;
}
.countdown-card .countdown-grid {
  display: flex;
  gap: 48px;
  justify-content: center;
  align-items: flex-end;
  opacity: 0;
}
.countdown-card .countdown-unit {
  text-align: center;
}
.countdown-card .countdown-num {
  font-family: var(--font-display);
  font-size: 120px;
  font-weight: 900;
  letter-spacing: var(--tracking-tight);
  color: var(--text-primary);
  line-height: 0.9;
}
.countdown-card .countdown-sub {
  font-family: var(--font-body);
  font-size: 14px;
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: var(--text-secondary);
  margin-top: 12px;
}
.countdown-card .countdown-date {
  font-family: var(--font-body);
  font-size: var(--body-size);
  color: var(--accent);
  text-align: center;
  margin-top: 40px;
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  opacity: 0;
}
```

**HTML template:**
```html
<div class="scene countdown-card">
  <div class="scene-inner" style="text-align:center">
    <p class="countdown-label" id="cd-label">Launching in</p>
    <div class="countdown-grid" id="cd-grid">
      <div class="countdown-unit">
        <p class="countdown-num">[DD]</p>
        <p class="countdown-sub">Days</p>
      </div>
      <div class="countdown-unit">
        <p class="countdown-num">[HH]</p>
        <p class="countdown-sub">Hours</p>
      </div>
      <div class="countdown-unit">
        <p class="countdown-num">[MM]</p>
        <p class="countdown-sub">Minutes</p>
      </div>
    </div>
    <p class="countdown-date" id="cd-date">[formatted launch date, e.g. "June 12, 2025"]</p>
  </div>
</div>
```

**renderFrame notes:**
- Label fades first (0–200ms of scene).
- Grid appears (200–500ms of scene): slam-in or materialise per preset.
- Date fades after grid (500–800ms).
- Values are static — agent calculates `DD`, `HH`, `MM` at generation time from `launch_date`.

---

## 9. cta-card

**Purpose:** The close. URL large. Action text above. Always the final scene.
Nothing else — no feature list, no secondary CTA.

**CSS:**
```css
.cta-card {
  align-items: center;
  justify-content: center;
}
.cta-card .cta-action {
  font-family: var(--font-body);
  font-size: var(--body-size);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: var(--text-secondary);
  text-align: center;
  margin-bottom: 24px;
  opacity: 0;
}
.cta-card .cta-url {
  font-family: var(--font-display);
  font-size: 72px;
  font-weight: 700;
  letter-spacing: var(--tracking-tight);
  color: var(--text-primary);
  text-align: center;
  line-height: 1;
  opacity: 0;
}
.cta-card .cta-accent {
  width: 64px;
  height: 2px;
  background: var(--accent);
  margin: 32px auto 0;
  transform: scaleX(0);
  transform-origin: left center;
}
.cta-card .cta-sub {
  font-family: var(--font-body);
  font-size: 18px;
  color: var(--text-secondary);
  text-align: center;
  margin-top: 24px;
  opacity: 0;
}
```

**HTML template:**
```html
<div class="scene cta-card">
  <div class="scene-inner" style="text-align:center">
    <p class="cta-action" id="cta-action">[action phrase — "Available now" / "Join the waitlist" / "Try it free"]</p>
    <p class="cta-url" id="cta-url">[url — no https:// prefix]</p>
    <div class="cta-accent" id="cta-accent"></div>
    <p class="cta-sub" id="cta-sub">[optional: one supporting line — "Free 14-day trial. No card required."]</p>
  </div>
</div>
```

**renderFrame notes:**
- Action text: fades in at scene start (300ms).
- URL: materialise/slam after action (200ms delay, 500ms duration).
- Accent bar: `scaleX 0→1` after URL (200ms).
- Sub text: fades after accent bar (200ms).
- The URL stays fully visible through end of scene — no exit animation on cta-card (it holds on screen).

---

## 10. tease-words ★ PRIMARY TEASE SCENE

**Purpose:** Each problem keyword owns the entire screen at massive scale. Punchy, rhythmic, unavoidable. Reference: Apple "Shot on iPhone" cadence. Replaces `tease-problem` for 60s and 90s videos.

**Timing:** Each word gets 1600–1800ms. 4 words = ~7200ms. Sub-line fades in at last 1500ms of tease. Reserve first 1500ms for `blackout-opener`.

**CSS:**
```css
.scene-tease { background: #000; }
.hero-word {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-display);
  font-size: 210px; font-weight: 900;
  letter-spacing: -0.05em; line-height: 1;
  color: #fff;
  opacity: 0; will-change: opacity, transform;
}
.tease-sub-line {
  position: absolute; bottom: 140px; left: 0; right: 0; text-align: center;
  font-size: 15px; font-weight: 400;
  letter-spacing: 0.22em; text-transform: uppercase;
  color: rgba(255,255,255,0.20);
  opacity: 0; will-change: opacity;
}
```

**HTML template:**
```html
<div class="scene scene-tease">
  <p id="word-0" class="hero-word">[word 1 — e.g. Research.]</p>
  <p id="word-1" class="hero-word">[word 2 — e.g. Write.]</p>
  <p id="word-2" class="hero-word">[word 3 — e.g. Outreach.]</p>
  <p id="word-3" class="hero-word">[word 4 — e.g. Repeat.]</p>
  <p id="tease-sub" class="tease-sub-line">[pain statement — e.g. "Hours that don't scale"]</p>
</div>
```

**renderFrame notes:**
```javascript
// Word beats — each word is a separate element, one visible at a time
const WORD_BEATS = [
  { id: 'word-0', start: TEASE_START + 1500, end: TEASE_START + 3300 },
  { id: 'word-1', start: TEASE_START + 3300, end: TEASE_START + 5100 },
  { id: 'word-2', start: TEASE_START + 5100, end: TEASE_START + 6900 },
  { id: 'word-3', start: TEASE_START + 6900, end: TEASE_END },
];
const FADE = 170; // ms

WORD_BEATS.forEach(({ id, start, end }, i) => {
  const el = document.getElementById(id);
  if (!el) return;
  if (t < start || t > end + 60) { el.style.opacity = '0'; el.style.transform = ''; return; }
  if (t < start + FADE) {
    const p = easeOutQuint((t - start) / FADE);
    el.style.opacity = p.toFixed(3);
    el.style.transform = `translateY(${lerp(32, 0, p).toFixed(2)}px)`;
  } else if (i < 3 && t > end - FADE) {
    const p = (t - (end - FADE)) / FADE;
    el.style.opacity = (1 - p).toFixed(3);
    el.style.transform = `translateY(${lerp(0, -22, p).toFixed(2)}px)`;
  } else { el.style.opacity = '1'; el.style.transform = ''; }
});

const tsub = document.getElementById('tease-sub');
if (tsub) tsub.style.opacity = easeOutCubic(clamp((t - (TEASE_END - 1600)) / 600, 0, 1)).toFixed(3);
```

**Design rules:**
- Each word is centered, full-screen, no decoration.
- 4 words maximum. If description has more pain points, pick the 4 sharpest.
- Sub-line: 15px, all-caps, very low opacity. It echoes, not competes.
- Background: always `#000` — never white, even in minimal preset.

---

## 11. terminal-card ★ PRIMARY BUILD SCENE

**Purpose:** Shows the audience's current reality — manual work being done, line by line, like a terminal output. 3 cards appear sequentially with a typewriter animation. Creates empathy before the reveal destroys that world. Inspired by Linear's "the old way vs new way" narrative pattern.

**CSS:**
```css
.scene-build {
  background: #080808;
  background-image: radial-gradient(circle, rgba(255,255,255,0.035) 1px, transparent 1px);
  background-size: 60px 60px;
  align-items: flex-start; justify-content: center;
  padding: 0 200px;
}
.build-header {
  font-size: 13px; font-weight: 500;
  letter-spacing: 0.22em; text-transform: uppercase;
  color: rgba(245,245,245,0.35);
  margin-bottom: 48px;
  opacity: 0; will-change: opacity;
}
.term-cards { width: 100%; max-width: 1000px; display: flex; flex-direction: column; gap: 20px; }
.term-card {
  display: flex; align-items: center; gap: 18px;
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 14px; padding: 26px 32px;
  background: rgba(255,255,255,0.018);
  opacity: 0; will-change: opacity, transform;
}
.term-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--accent); flex-shrink: 0; }
.term-text {
  font-size: 22px; font-weight: 400; letter-spacing: -0.01em;
  color: rgba(245,245,245,0.65);
}
.build-close-line {
  position: absolute; bottom: 140px; left: 200px; right: 200px;
  height: 1px; background: var(--accent);
  transform: scaleX(0); transform-origin: left center; will-change: transform;
  box-shadow: 0 0 18px rgba([accent-rgb],0.4);
}
.build-close-label {
  position: absolute; bottom: 96px; left: 0; right: 0; text-align: center;
  font-size: 13px; font-weight: 500; letter-spacing: 0.22em; text-transform: uppercase;
  color: var(--accent); opacity: 0; will-change: opacity;
}
```

**HTML template:**
```html
<div class="scene scene-build">
  <div style="width:100%;max-width:1000px">
    <p id="build-header" class="build-header">Meanwhile, your team is spending hours on</p>
    <div class="term-cards">
      <div id="tc0" class="term-card"><div class="term-dot"></div><span id="tt0" class="term-text"></span></div>
      <div id="tc1" class="term-card"><div class="term-dot"></div><span id="tt1" class="term-text"></span></div>
      <div id="tc2" class="term-card"><div class="term-dot"></div><span id="tt2" class="term-text"></span></div>
    </div>
  </div>
  <div id="close-line" class="build-close-line"></div>
  <p id="close-label" class="build-close-label">Not anymore</p>
</div>
```

**renderFrame notes:**
```javascript
const CARDS = [
  { id: 0, start: BUILD_START_MS + 1500, text: 'Researching [N] competitor strategies...' },
  { id: 1, start: BUILD_START_MS + 5500, text: 'Writing [N] content drafts from briefs...' },
  { id: 2, start: BUILD_START_MS + 9500, text: 'Scheduling [N] personalised outreach emails...' },
];
const TYPE_DUR   = 1800; // ms for full typewriter reveal
const BUILD_CLOSE = BUILD_END_MS - 3500; // fade cards out before build ends
const BUILD_LABEL = BUILD_END_MS - 2200;

CARDS.forEach(({ id, start, text }) => {
  const card = document.getElementById(`tc${id}`);
  const txt  = document.getElementById(`tt${id}`);
  if (!card || !txt) return;

  if (t < start) { card.style.opacity = '0'; card.style.transform = ''; txt.textContent = ''; return; }
  if (t >= BUILD_CLOSE) {
    const fp = clamp((t - BUILD_CLOSE) / 550, 0, 1);
    card.style.opacity   = (1 - easeOutCubic(fp)).toFixed(3);
    card.style.transform = `translateX(${lerp(0, -24, easeOutCubic(fp)).toFixed(2)}px)`;
  } else {
    const fi = clamp((t - start) / 380, 0, 1);
    card.style.opacity   = easeOutCubic(fi).toFixed(3);
    card.style.transform = `translateX(${lerp(-24, 0, easeOutCubic(fi)).toFixed(2)}px)`;
  }
  const tp    = clamp((t - (start + 180)) / TYPE_DUR, 0, 1);
  const chars = Math.floor(tp * text.length);
  const blink = t < (start + 180 + TYPE_DUR) && chars < text.length && Math.sin((t / 380) * Math.PI) > 0;
  txt.textContent = text.slice(0, chars) + (blink ? '▋' : '');
});

const closeLine  = document.getElementById('close-line');
const closeLabel = document.getElementById('close-label');
if (closeLine)  closeLine.style.transform = `scaleX(${easeOutCubic(clamp((t - BUILD_LABEL) / 650, 0, 1)).toFixed(3)})`;
if (closeLabel) closeLabel.style.opacity  = easeOutCubic(clamp((t - (BUILD_LABEL + 500)) / 500, 0, 1)).toFixed(3);
```

**Design rules:**
- Card text must describe the actual manual work the target audience does — not generic placeholders.
- Tailor the numbers in the card text to the specific product's context (make them feel real).
- `build-header` sets the scene: "Meanwhile, your team is spending hours on" — always present.
- Cards fade out 3500ms before build ends, leaving a closing accent line + "Not anymore".
- Background: dark with dot-grid always — never white.
