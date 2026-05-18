# Tone Presets — vid-sizzle-reel

Four tone-matched presets. Read before generating any HTML.
Apply ALL tokens from the chosen preset. No free hex values or font-family strings outside these tables.

---

## energetic

**Reference feel:** Product Hunt launch day. High-BPM. Bold all-caps. White flash cuts.

**Font CDN:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@700;900&display=swap" rel="stylesheet">
```

**CSS tokens:**
```css
:root {
  --bg:             #000000;
  --bg-secondary:   #0A0A0A;
  --text-primary:   #FFFFFF;
  --text-secondary: #888888;
  --accent:         #00F0FF;
  --accent-2:       #FF2D55;
  --divider:        rgba(255,255,255,0.10);
  --font-display:   'DM Sans', system-ui, sans-serif;
  --font-mono:      'DM Mono', monospace;
  --tracking-tight: -0.03em;
  --tracking-wide:  0.08em;
  --display-size:   180px;
  --headline-size:  80px;
  --label-size:     18px;
  --body-size:      22px;
  --cut-flash-bg:   #FFFFFF;
  --cut-flash-dur:  0.06s;
}
```

**Effects:**
- `film-grain: false`
- `vignette: false`
- `cut-flash: true` — white `#FFFFFF` overlay, 60ms opacity 0→1→0 at every cut point
- `dot-grid: true` — `radial-gradient(circle, rgba(255,255,255,0.04) 1px, transparent 1px); background-size: 48px 48px`
- Text entrance: slam-in (`scale 1.08→1, opacity 0→1, 120ms`)
- Text style: ALL CAPS, letter-spacing 0.08em

**Cut timing:** `fast` — 1.0s to 1.8s per cut

**Background treatment:** Pure `#000000`. Dot-grid on all scenes except cold open (which uses pure black for maximum contrast).

---

## cinematic

**Reference feel:** Apple product reveal video. Deliberate pacing, premium dark palette.

**Font CDN:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600;700&family=Cormorant:wght@700;800&display=swap" rel="stylesheet">
```

**CSS tokens:**
```css
:root {
  --bg:             #050505;
  --bg-secondary:   #0D0D0D;
  --text-primary:   #F5F5F5;
  --text-secondary: #999999;
  --accent:         #D4AF37;
  --accent-2:       rgba(212,175,55,0.25);
  --divider:        rgba(255,255,255,0.07);
  --font-display:   'Cormorant', 'Cormorant Garamond', Georgia, serif;
  --font-body:      'Cormorant Garamond', Georgia, serif;
  --tracking-tight: -0.02em;
  --tracking-wide:  0.12em;
  --display-size:   160px;
  --headline-size:  64px;
  --label-size:     16px;
  --body-size:      22px;
  --cut-flash-bg:   rgba(255,255,255,0.0);
  --cut-flash-dur:  0s;
}
```

**Effects:**
- `film-grain: true` — canvas 240×135, opacity 0.022, seeded PRNG per frame
- `vignette: true` — `radial-gradient(ellipse at center, transparent 35%, rgba(0,0,0,0.65) 100%)`
- `cut-flash: false` — cross-dissolve via `opacity 1→0→1` over 400ms instead
- `dot-grid: false`
- Text entrance: materialise (`filter blur 8px→0px, opacity 0→1, 700ms, easeOutCubic`)
- Text style: mixed case, letter-spacing `--tracking-tight`

**Cut timing:** `cinematic` — 3.0s to 5.0s per scene

**Background treatment:** Pure `#050505`. Film grain + vignette create depth.

---

## emotional

**Reference feel:** Kickstarter campaign video. Warm, personal, intimate.

**Font CDN:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700&family=Lora:wght@400;600&display=swap" rel="stylesheet">
```

**CSS tokens:**
```css
:root {
  --bg:             #FAF7F2;
  --bg-secondary:   #F2EDE4;
  --text-primary:   #2C1810;
  --text-secondary: #6B4C3B;
  --accent:         #B87333;
  --accent-2:       rgba(184,115,51,0.18);
  --divider:        rgba(44,24,16,0.10);
  --font-display:   'Playfair Display', Georgia, serif;
  --font-body:      'Lora', Georgia, serif;
  --tracking-tight: -0.01em;
  --tracking-wide:  0.06em;
  --display-size:   140px;
  --headline-size:  56px;
  --label-size:     15px;
  --body-size:      21px;
  --cut-flash-bg:   rgba(250,247,242,0.0);
  --cut-flash-dur:  0s;
}
```

**Effects:**
- `film-grain: true` — canvas 240×135, opacity 0.018, warm tint (blend: multiply)
- `vignette: true` — softer, `radial-gradient(ellipse at center, transparent 45%, rgba(44,24,16,0.40) 100%)`
- `cut-flash: false` — soft cross-dissolve over 600ms
- `dot-grid: false`
- Text entrance: word-by-word gentle fade (`opacity 0→1, 500ms, easeOut, 120ms stagger`)
- Text style: lowercase or mixed case, italic accent words

**Cut timing:** `mixed` — 2.0s to 4.0s, varying by scene energy

**Background treatment:** `--bg` warm ivory. Vignette + grain create warmth.

---

## professional

**Reference feel:** B2B SaaS conference opener. Clean, structured, trustworthy.

**Font CDN:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet">
```

**CSS tokens:**
```css
:root {
  --bg:             #FFFFFF;
  --bg-secondary:   #F5F7FA;
  --text-primary:   #0A0A0A;
  --text-secondary: #6B7280;
  --accent:         #4B9FFF;
  --accent-2:       rgba(75,159,255,0.12);
  --divider:        rgba(10,10,10,0.08);
  --font-display:   'Inter', system-ui, sans-serif;
  --font-body:      'Inter', system-ui, sans-serif;
  --tracking-tight: -0.02em;
  --tracking-wide:  0.04em;
  --display-size:   150px;
  --headline-size:  60px;
  --label-size:     14px;
  --body-size:      20px;
  --cut-flash-bg:   rgba(255,255,255,0.0);
  --cut-flash-dur:  0s;
}
```

**Effects:**
- `film-grain: false`
- `vignette: false`
- `cut-flash: false` — clean instant cut via `display` switching (handled by HyperFrames `data-start`)
- `dot-grid: false`
- Text entrance: slide up (`y 20→0, opacity 0→1, 350ms, easeOutCubic`)
- Text style: sentence case, clean weight hierarchy (900 display, 600 headline, 400 body)

**Cut timing:** `2s` — 1.8s to 2.4s per scene, consistent rhythm

**Background treatment:** White or `--bg-secondary`. Accent blue for key numbers and CTAs.
