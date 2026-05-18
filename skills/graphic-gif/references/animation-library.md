# Animation Library — graphic-gif

6 animation types for CSS-animated GIFs. All specs for 800×800px canvas (1vw = 8px).

Read this file before generating HTML in Step 3. Pick one animation type per GIF.

---

## 1. fade-in

Content fades in from transparent, with subtle upward drift.

**Best for:** Quotes, announcements, single-stat reveals, brand messages.

**Key technique:** `opacity: 0 → 1` + `translateY(12px → 0)` with smooth ease-out.

```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-item {
  animation: fadeIn 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards;
  opacity: 0; /* start hidden */
}
```

**For staggered multi-element fade:**
Do NOT use `animation-delay`. Instead, structure the animation duration to reveal elements sequentially. Web Animations API will seek through the full timeline — each element needs its own named animation with different start points baked into its `@keyframes` percentages.

Example — 3 elements staggered within a 3s animation:
```css
/* Element 1: reveals at 0–25% (0–750ms) */
@keyframes fadeEl1 {
  0%   { opacity: 0; transform: translateY(12px); }
  25%  { opacity: 1; transform: translateY(0); }
  100% { opacity: 1; transform: translateY(0); }
}
/* Element 2: reveals at 25–50% (750–1500ms) */
@keyframes fadeEl2 {
  0%   { opacity: 0; transform: translateY(12px); }
  25%  { opacity: 0; transform: translateY(12px); }
  50%  { opacity: 1; transform: translateY(0); }
  100% { opacity: 1; transform: translateY(0); }
}
/* Element 3: reveals at 50–75% (1500–2250ms) */
@keyframes fadeEl3 {
  0%   { opacity: 0; transform: translateY(12px); }
  50%  { opacity: 0; transform: translateY(12px); }
  75%  { opacity: 1; transform: translateY(0); }
  100% { opacity: 1; transform: translateY(0); }
}

.el1 { animation: fadeEl1 3s cubic-bezier(0.22, 1, 0.36, 1) forwards; }
.el2 { animation: fadeEl2 3s cubic-bezier(0.22, 1, 0.36, 1) forwards; }
.el3 { animation: fadeEl3 3s cubic-bezier(0.22, 1, 0.36, 1) forwards; }
```

**HTML structure:**
```html
<div class="canvas">
  <div class="content">
    <p class="el1 fade-item">Main message here</p>
    <p class="el2 fade-item">Supporting line here</p>
    <p class="el3 fade-item">Third element here</p>
  </div>
</div>
```

---

## 2. slide-in

Elements slide in from one edge with a spring overshoot effect.

**Best for:** Headlines, key stats, before/after comparisons, list reveals.

**Directions:** left (default), right, top, bottom.

**Key technique:** `translateX/Y` + spring cubic-bezier `(0.34, 1.56, 0.64, 1)` for overshoot.

```css
/* Slide from left */
@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-60px); }
  to   { opacity: 1; transform: translateX(0); }
}

/* Slide from right */
@keyframes slideInRight {
  from { opacity: 0; transform: translateX(60px); }
  to   { opacity: 1; transform: translateX(0); }
}

/* Slide from bottom */
@keyframes slideInUp {
  from { opacity: 0; transform: translateY(40px); }
  to   { opacity: 1; transform: translateY(0); }
}

.slide-item {
  animation: slideInLeft 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
  opacity: 0;
}
```

**For sequential slide-in of multiple elements (bake stagger into keyframes):**
```css
@keyframes slideEl1 {
  0%   { opacity: 0; transform: translateX(-60px); }
  20%  { opacity: 1; transform: translateX(0); }
  100% { opacity: 1; transform: translateX(0); }
}
@keyframes slideEl2 {
  0%   { opacity: 0; transform: translateX(-60px); }
  20%  { opacity: 0; transform: translateX(-60px); }
  40%  { opacity: 1; transform: translateX(0); }
  100% { opacity: 1; transform: translateX(0); }
}
```

---

## 3. typewriter

Text types out character by character. The most effective animation for revealing stats, insights, or hooks.

**Best for:** Single sentences, stat reveals, developer-audience content, hooks with tension.

**Key technique:** `steps(N, end)` with `overflow: hidden` and `width: 0 → 100%`. N = exact character count of the text string.

**Critical:** N MUST equal the exact character count of the text. Wrong N = wrong reveal speed.

```css
.typewriter-text {
  display: inline-block;
  overflow: hidden;
  white-space: nowrap;
  border-right: 2px solid var(--accent);
  animation:
    typing 2.5s steps(N, end) forwards,
    blink 0.75s step-end infinite;
  width: 0;
  max-width: 100%;
}

@keyframes typing {
  from { width: 0; }
  to   { width: 100%; }
}

@keyframes blink {
  from, to { border-color: transparent; }
  50%      { border-color: var(--accent); }
}
```

**Where N = character count:**
- Count spaces, punctuation, and numbers as characters
- "73% of buyers" → N = 14
- "Hello, World!" → N = 13

**For multi-line typewriter (sequential lines):**
Each line needs its own keyframe with percentage-baked timing:
```css
/* Line 1: types from 0% to 40% of total duration */
@keyframes typeLine1 {
  0%   { width: 0; }
  40%  { width: 100%; }
  100% { width: 100%; }
}
/* Line 2: appears at 40%, types from 40% to 80% */
@keyframes typeLine2 {
  0%   { width: 0; opacity: 0; }
  40%  { width: 0; opacity: 0; }
  40.1%{ width: 0; opacity: 1; }
  80%  { width: 100%; opacity: 1; }
  100% { width: 100%; opacity: 1; }
}

.line1 { animation: typeLine1 3s steps(N1, end) forwards; }
.line2 { animation: typeLine2 3s steps(N2, end) forwards; }
```

**HTML structure:**
```html
<div class="canvas">
  <div class="typewriter-wrapper">
    <span class="typewriter-text">Your text here exactly</span>
  </div>
</div>
```

---

## 4. counter

Numbers count up from 0 to a target value. Native CSS, no JavaScript.

**Best for:** Stats, metrics, growth numbers, percentages. High-impact for data-driven content.

**Key technique:** `@property --num` CSS custom property with integer interpolation. `counter-reset: num var(--num)` renders the integer as text via `::after { content: counter(num) }`.

**Critical:** Requires Chromium rendering (Playwright uses Chromium → works for GIF export).

```css
@property --num {
  syntax: '<integer>';
  inherits: false;
  initial-value: 0;
}

.counter {
  animation: countUp var(--duration, 2s) linear forwards;
  counter-reset: num var(--num);
}

.counter::after {
  content: counter(num);
}

@keyframes countUp {
  from { --num: 0; }
  to   { --num: var(--target); }
}
```

**Usage (set target per element):**
```html
<!-- Counts 0 → 73 over 2 seconds -->
<div class="counter" style="--target: 73; --duration: 2s;"></div>

<!-- Counts 0 → 500 over 3 seconds -->
<div class="counter" style="--target: 500; --duration: 3s;"></div>
```

**For counter with suffix (%, K, etc.) — use ::before/::after wrappers:**
```html
<div class="stat-block">
  <span class="counter" style="--target: 73; --duration: 2s;"></span>
  <span class="suffix">%</span>
</div>
```

**For multiple counters with staggered start (bake into keyframes):**
```css
/* Counter 1: counts during 0–60% of animation */
@keyframes count1 {
  0%   { --num: 0; }
  60%  { --num: 73; }
  100% { --num: 73; }
}
/* Counter 2: counts during 40–100% of animation */
@keyframes count2 {
  0%   { --num: 0; }
  40%  { --num: 0; }
  100% { --num: 250; }
}
```

---

## 5. pulse

Pulsing / breathing scale or glow effect. Infinite loop by nature.

**Best for:** CTAs, icons, emphasis elements, "live" indicators, attention draws.

**Key technique:** `scale(1) → scale(1.06) → scale(1)` with `ease-in-out` and `animation-iteration-count: infinite`.

**Note:** Since this animation loops in CSS (`infinite`), the GIF frame capture simply captures `duration * fps` frames — the animation is already looping at the CSS level.

```css
/* Scale pulse */
@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50%       { transform: scale(1.06); opacity: 0.85; }
}

/* Glow pulse (for accent elements on dark backgrounds) */
@keyframes glowPulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(var(--accent-rgb), 0.4);
    transform: scale(1);
  }
  50% {
    box-shadow: 0 0 20px 8px rgba(var(--accent-rgb), 0.15);
    transform: scale(1.04);
  }
}

.pulse-item {
  animation: pulse 1.5s ease-in-out infinite;
}

.cta-button {
  animation: glowPulse 2s ease-in-out infinite;
  /* define --accent-rgb as R,G,B values: e.g. 250,204,21 for #FACC15 */
}
```

**Combining pulse with static content:**
```css
/* Background stays still — only the CTA button pulses */
.static-content { /* no animation */ }
.cta-button { animation: pulse 2s ease-in-out infinite; }
```

**HTML structure:**
```html
<div class="canvas">
  <div class="static-content">
    <h1>Ready to reduce churn?</h1>
    <p>See how DataPulse works</p>
  </div>
  <button class="cta-button pulse-item">Book a demo →</button>
</div>
```

---

## 6. loop-scroll

Infinite scrolling ticker / marquee. Content scrolls continuously in one direction.

**Best for:** Feature lists, social proof, product attributes, news-style tickers, repeated keyword emphasis.

**Key technique:** Content is duplicated (`[items] [items]`). `translateX(0 → -50%)` with `linear` timing and `infinite` iteration — the second copy seamlessly takes over when the first exits.

**Critical:** Content MUST be duplicated exactly once. If 4 items, the HTML contains all 8 items (4 original + 4 copy). The GIF frame count covers one full scroll cycle = smooth loop.

```css
.ticker-container {
  width: 800px;
  overflow: hidden;
  /* Add a fade mask for polished edge effect */
  -webkit-mask-image: linear-gradient(
    to right,
    transparent 0%,
    black 8%,
    black 92%,
    transparent 100%
  );
}

.ticker-track {
  display: flex;
  align-items: center;
  white-space: nowrap;
  /* Duration = number of original items × base speed */
  animation: scrollLeft linear infinite;
  animation-duration: calc(var(--item-count) * 1.5s);
}

@keyframes scrollLeft {
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }
}

.ticker-item {
  padding: 0 clamp(1.5rem, 4vw, 2.5rem);
  font-size: clamp(1rem, 2vw, 1.4rem);
  font-weight: 600;
  flex-shrink: 0;
}

.ticker-sep {
  color: var(--accent);
  padding: 0 0.5rem;
  flex-shrink: 0;
}
```

**HTML structure (items duplicated):**
```html
<div class="canvas">
  <div class="ticker-container">
    <div class="ticker-track" style="--item-count: 4;">
      <!-- Original set -->
      <span class="ticker-item">Reduce Churn</span>
      <span class="ticker-sep">·</span>
      <span class="ticker-item">Increase NRR</span>
      <span class="ticker-sep">·</span>
      <span class="ticker-item">Boost LTV</span>
      <span class="ticker-sep">·</span>
      <span class="ticker-item">Drive Expansion</span>
      <span class="ticker-sep">·</span>
      <!-- Duplicate set (exact copy) -->
      <span class="ticker-item">Reduce Churn</span>
      <span class="ticker-sep">·</span>
      <span class="ticker-item">Increase NRR</span>
      <span class="ticker-sep">·</span>
      <span class="ticker-item">Boost LTV</span>
      <span class="ticker-sep">·</span>
      <span class="ticker-item">Drive Expansion</span>
      <span class="ticker-sep">·</span>
    </div>
  </div>
</div>
```

**For vertical scroll (top to bottom):**
```css
@keyframes scrollUp {
  from { transform: translateY(0); }
  to   { transform: translateY(-50%); }
}
.ticker-track-vertical {
  display: flex;
  flex-direction: column;
  animation: scrollUp linear infinite;
}
```

---

## Choosing the Right Animation

| Use case | Best animation |
|---|---|
| "Show a stat with impact" | counter or fade-in |
| "Reveal a quote or insight" | typewriter or fade-in |
| "Social media hook" | typewriter (terminal style) |
| "CTA / button emphasis" | pulse |
| "List of features/benefits" | loop-scroll |
| "Headline announcement" | slide-in |
| "Multiple stats together" | counter (multiple) |
| "Developer/tech audience" | typewriter (terminal style) |

## File Size Guidance by Animation Type

| Animation | Typical size | Why |
|---|---|---|
| fade-in (1 element) | 100–400KB | Few color changes between frames |
| slide-in | 200–600KB | More color variation as element moves |
| typewriter (terminal) | 150–500KB | Dark bg + monochrome text = few colors |
| counter | 100–350KB | Static background, changing number only |
| pulse | 200–600KB | Repetitive frames compress well |
| loop-scroll | 400KB–1.5MB | Many unique positions = more frames |
