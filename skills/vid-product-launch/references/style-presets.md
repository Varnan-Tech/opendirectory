# Style Presets — vid-product-launch

Four tone-matched presets. Read this file before generating any HTML.
Apply ALL tokens from the chosen preset. No free hex values or font-family strings.

---

## cinematic

**Reference feel:** Apple product reveal. Deliberate, dark, premium.

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
  --accent-soft:    rgba(212,175,55,0.15);
  --divider:        rgba(255,255,255,0.08);
  --font-display:   'Cormorant', 'Cormorant Garamond', Georgia, serif;
  --font-body:      'Cormorant Garamond', Georgia, serif;
  --tracking-tight: -0.02em;
  --tracking-wide:  0.12em;
  --product-size:   160px;   /* product name on 16:9; use 100px for 9:16 */
  --tagline-size:   36px;
  --stat-size:      220px;
  --body-size:      22px;
}
```

**Effects:**
- `film-grain: true` — canvas noise overlay, opacity 0.025
- `vignette: true` — radial gradient dark edges
- `letterbox: user-param` — 2.35:1 black bars if enabled
- `light-leak: true` — warm gold sweep at reveal moment
- Text reveal: slow materialise (`blur 8px→0, opacity 0→1, 700ms`)
- Tease text: word-by-word, 200ms stagger per word, all-caps, letter-spacing 0.12em

**Background treatment:** Pure `#050505`. No gradients on background.

---

## energetic

**Reference feel:** Product Hunt launch day. Fast, bold, electric.

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
  --accent:         #0066FF;
  --accent-soft:    rgba(0,102,255,0.15);
  --divider:        rgba(255,255,255,0.12);
  --font-display:   'DM Sans', system-ui, sans-serif;
  --font-body:      'DM Mono', 'Fira Code', monospace;
  --tracking-tight: -0.03em;
  --tracking-wide:  0.08em;
  --product-size:   180px;
  --tagline-size:   32px;
  --stat-size:      240px;
  --body-size:      20px;
}
```

**Effects:**
- `film-grain: false`
- `vignette: false`
- `letterbox: false`
- `light-leak: false` — instead: white flash (`opacity 0→1→0, 80ms`) at reveal
- Text reveal: slam-in (`scale 1.12→1, opacity 0→1, 120ms`)
- Tease text: full block appears, no stagger

**Background treatment:** Hard black. Optional: 1px accent-color horizontal rule as scene separator element.

---

## minimal

**Reference feel:** Linear / Vercel announcement. Refined, spacious, confident.

**Font CDN:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700;900&display=swap" rel="stylesheet">
```

**CSS tokens:**
```css
:root {
  --bg:             #FFFFFF;
  --bg-secondary:   #FAFAFA;
  --text-primary:   #0A0A0A;
  --text-secondary: #666666;
  --accent:         #0A0A0A;
  --accent-soft:    rgba(10,10,10,0.06);
  --divider:        rgba(0,0,0,0.08);
  --font-display:   'Inter', system-ui, sans-serif;
  --font-body:      'Inter', system-ui, sans-serif;
  --tracking-tight: -0.04em;
  --tracking-wide:  0.06em;
  --product-size:   140px;
  --tagline-size:   30px;
  --stat-size:      200px;
  --body-size:      20px;
}
```

**Effects:**
- `film-grain: false`
- `vignette: false`
- `letterbox: false`
- `light-leak: false`
- Text reveal: typewriter (one character at a time, 40ms per char) OR gentle fade (`opacity 0→1, 400ms`)
- Tease text: gentle fade-up (`translateY 16px→0, opacity 0→1, 500ms`)

**Background treatment:** Pure white. Extremely fine `1px solid var(--divider)` borders on proof elements allowed.

---

## emotional

**Reference feel:** Kickstarter campaign. Warm, human, mission-driven.

**Font CDN:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Playfair+Display+SC:wght@400;700&display=swap" rel="stylesheet">
```

**CSS tokens:**
```css
:root {
  --bg:             #FAF7F2;
  --bg-secondary:   #F3EFE8;
  --text-primary:   #2C1810;
  --text-secondary: #7A6355;
  --accent:         #B87333;
  --accent-soft:    rgba(184,115,51,0.12);
  --divider:        rgba(44,24,16,0.10);
  --font-display:   'Playfair Display', 'Playfair Display SC', Georgia, serif;
  --font-body:      'Playfair Display', Georgia, serif;
  --tracking-tight: -0.01em;
  --tracking-wide:  0.10em;
  --product-size:   120px;
  --tagline-size:   34px;
  --stat-size:      180px;
  --body-size:      22px;
}
```

**Effects:**
- `film-grain: true` — canvas noise overlay, opacity 0.018, warm tint (add rgba(180,120,60,0.03) blend)
- `vignette: true` — soft radial gradient, opacity 0.4
- `letterbox: false`
- `light-leak: true` — warm copper sweep at reveal moment
- Text reveal: word-by-word (`opacity 0→1, translateY 12px→0, 300ms per word, 150ms stagger`)
- Tease text: slow fade per line, 400ms each

**Background treatment:** Warm ivory. Subtle texture suggestion via CSS `background-image: radial-gradient(circle at 20% 80%, rgba(184,115,51,0.04) 0%, transparent 60%)`.
