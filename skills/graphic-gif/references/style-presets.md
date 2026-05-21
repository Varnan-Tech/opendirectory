# Style Presets — graphic-gif

4 GIF-appropriate style presets. These are a subset of the full 9-preset library — chosen because they use simple, flat palettes that produce smaller GIF files and smoother loops.

**Why only 4?** GIF format is limited to 256 colors per frame. Styles with complex gradients, photographic backgrounds, or multiple gradient stops create color-banding artifacts and larger files. The 4 presets below use solid backgrounds and single accent colors.

**Rule:** Pick the preset that matches the tone and audience. Read all 4 before choosing.

---

## 1. clean-slate

**Character:** Professional. Clean. High-trust. No-noise.

```css
:root {
  /* Colors */
  --bg:           #FFFFFF;
  --bg-elevated:  #F8FAFC;
  --text:         #0F172A;
  --text-muted:   #64748B;
  --accent:       #0F172A;
  --accent-light: #F1F5F9;
  --divider:      #E2E8F0;

  /* Typography */
  --font-display: 'Plus Jakarta Sans', sans-serif;
  --font-body:    'Plus Jakarta Sans', sans-serif;

  /* Font CDN */
  /* <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"> */
}
```

**Design direction:**
- Background: white. Period. No gradients.
- Accent: near-black `#0F172A` — used sparingly (underlines, stats, borders)
- Typography: weight contrast is the design — 800 display vs 400 body
- Signature element: a thin 2px `--accent` underline or left border on key elements

**Use for:** Stat counters, professional quote reveals, LinkedIn-style social content. Any audience that expects polish without flair.

**File size:** Small. White bg + black text = ~16 colors per frame.

---

## 2. terminal

**Character:** Developer. Precise. Monochrome matrix. Mechanical.

```css
:root {
  /* Colors */
  --bg:           #0D1117;
  --bg-elevated:  #161B22;
  --text:         #C9D1D9;
  --text-muted:   #8B949E;
  --accent:       #00FF41;
  --accent-light: #1A2332;
  --divider:      #21262D;

  /* Typography */
  --font-display: 'JetBrains Mono', monospace;
  --font-body:    'JetBrains Mono', monospace;

  /* Font CDN */
  /* <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet"> */
}
```

**Design direction:**
- Background: near-black `#0D1117` — GitHub dark mode reference
- Accent: matrix green `#00FF41` — for cursor, numbers, key terms
- Typography: monospace everywhere — even display headings
- Signature element: blinking cursor `|` using `animation: blink step-end infinite`
- Optional: scan-line overlay (`repeating-linear-gradient` with 1px transparent lines at 2px intervals, opacity 0.03)

**Scan-line recipe:**
```css
.canvas::after {
  content: '';
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    to bottom,
    transparent,
    transparent 1px,
    rgba(0, 0, 0, 0.03) 1px,
    rgba(0, 0, 0, 0.03) 2px
  );
  pointer-events: none;
}
```

**Use for:** Typewriter effects (most effective), code reveals, developer stats, startup/tech metrics, anything aimed at builders.

**File size:** Very small. Dark bg + single-color text = ~8–12 colors per frame.

---

## 3. electric-burst

**Character:** Bold. Kinetic. Electric. High-contrast impact.

```css
:root {
  /* Colors */
  --bg:           #09090B;
  --bg-elevated:  #18181B;
  --text:         #FAFAFA;
  --text-muted:   #A1A1AA;
  --accent:       #FACC15;
  --accent-light: #1C1917;
  --divider:      #27272A;

  /* Typography */
  --font-display: 'Space Grotesk', sans-serif;
  --font-body:    'DM Sans', sans-serif;

  /* Font CDN */
  /* <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet"> */
}
```

**Design direction:**
- Background: near-black `#09090B` — darker than terminal, no green tint
- Accent: electric yellow `#FACC15` — for numbers, key words, CTA text
- Typography: `Space Grotesk` is chunky and geometric at large sizes
- Signature element: large accent-colored number or stat as the hero element, with `--text-muted` label below

**Accent usage rule:** Yellow only on the most important element per canvas (one stat, one CTA word, one key number). Everything else in white `#FAFAFA`. Yellow everywhere = no yellow.

**Use for:** Bold stat reveals, CTA buttons (pulse animation), product metric GIFs, high-energy social content.

**File size:** Small-medium. Dark bg + white text + 1 yellow element = ~20–30 colors per frame.

---

## 4. brutalist

**Character:** Raw. Confrontational. Typographic. Zero decoration.

```css
:root {
  /* Colors */
  --bg:           #FFFFFF;
  --bg-elevated:  #F5F5F5;
  --text:         #000000;
  --text-muted:   #666666;
  --accent:       #FF0000;
  --accent-light: #FFF5F5;
  --divider:      #000000;

  /* Typography */
  --font-display: 'Space Mono', monospace;
  --font-body:    'Space Mono', monospace;

  /* Font CDN */
  /* <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap" rel="stylesheet"> */
}
```

**Design direction:**
- Background: white. Nothing soft.
- Accent: pure red `#FF0000` — used for borders, tickers, 1–2 key words
- Typography: monospace everywhere — no humanist curves, no refinement
- Signature element: a thick `4px solid #000000` border or underline. Or a red separator.
- Layout: asymmetric, left-heavy. Text at extreme sizes. Oversized numbers.

**For loop-scroll tickers:** Red `--accent` separator dots (`·`) between items. Track background `--bg` white. Item font `Space Mono` 700.

**For slide-in:** Slide from left with `translateX(-100vw)` overshoot. Hard cubic-bezier: `cubic-bezier(0.87, 0, 0.13, 1)` (no spring — mechanical snap).

**Use for:** Loop-scroll tickers, bold feature lists, confrontational stat reveals, design-forward agencies, brands that want to stand out.

**File size:** Very small. White + black + occasional red = ~8–16 colors per frame.

---

## Styles to AVOID for GIFs

These styles from the full 9-preset library produce poor GIF output:

| Style | Problem |
|---|---|
| midnight-editorial | Complex gradient overlays = hundreds of colors = banding + large files |
| matt-gray | Multiple grey shades with subtle transitions = poor quantization |
| product-minimal | Gradient accents and backgrounds = too many colors |
| mint-pixel-corporate | Mint gradient + purple tones = complex palette |
| warm-earth | Warm texture/noise patterns = photographic complexity |
| magazine-red | Multiple brand colors + photographic intent = GIF banding |
| soft-cloud | Pastel gradients = smooth color transitions that GIF destroys |

**The rule:** If the style uses any `linear-gradient` as a background (not just borders), avoid it for GIFs. Flat solid colors only.
