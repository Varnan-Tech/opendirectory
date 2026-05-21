# Style Presets — graphic-chart

5 recommended presets for data visualization charts. Each includes CSS tokens AND a data color palette — both are required.

The CSS tokens control: background, typography, grid lines, axis labels.
The data palette controls: bar/line/point colors and pie segment fills.

Read this file before generating HTML in Step 3. Apply ALL tokens from the chosen preset.

---

## 1. clean-slate

**Character:** Professional. Enterprise-safe. High-trust. Works for any audience.

```css
:root {
  --bg:           #FFFFFF;
  --bg-elevated:  #F8FAFC;
  --text:         #0F172A;
  --text-muted:   #64748B;
  --accent:       #3B82F6;
  --divider:      #E2E8F0;
  --font-display: 'Plus Jakarta Sans', sans-serif;
  --font-body:    'Plus Jakarta Sans', sans-serif;
}
```

Font CDN:
```html
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

Data palette (ordered by visual hierarchy):
```javascript
const palette = ['#3B82F6','#10B981','#F59E0B','#EF4444','#8B5CF6','#EC4899','#06B6D4'];
const paletteAlpha = ['rgba(59,130,246,0.15)','rgba(16,185,129,0.15)','rgba(245,158,11,0.15)','rgba(239,68,68,0.15)','rgba(139,92,246,0.15)','rgba(236,72,153,0.15)','rgba(6,182,212,0.15)'];
```

Grid line color: `rgba(0,0,0,0.07)`
Axis tick color: `#64748B`

**Best for:** B2B reports, LinkedIn posts, investor decks, any content requiring professional restraint.

---

## 2. midnight-editorial

**Character:** Editorial. Premium dark. Authoritative.

```css
:root {
  --bg:           #111111;
  --bg-elevated:  #1A1A1A;
  --text:         #F5F5F5;
  --text-muted:   #9CA3AF;
  --accent:       #D8F90A;
  --divider:      #2D2D2D;
  --font-display: 'Instrument Serif', serif;
  --font-body:    'Inter', sans-serif;
}
```

Font CDN:
```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

Data palette:
```javascript
const palette = ['#D8F90A','#60A5FA','#34D399','#FB923C','#C084FC','#F472B6','#38BDF8'];
const paletteAlpha = ['rgba(216,249,10,0.18)','rgba(96,165,250,0.18)','rgba(52,211,153,0.18)','rgba(251,146,60,0.18)','rgba(192,132,252,0.18)','rgba(244,114,182,0.18)','rgba(56,189,248,0.18)'];
```

Grid line color: `rgba(255,255,255,0.07)`
Axis tick color: `#9CA3AF`

**Best for:** Thought leadership content, editorial publications, agency presentations, premium brand charts.

---

## 3. matt-gray

**Character:** Neutral. Sophisticated. Board-room-safe.

```css
:root {
  --bg:           #F5F5F0;
  --bg-elevated:  #EBEBЕ6;
  --text:         #1C1C1C;
  --text-muted:   #737373;
  --accent:       #1C1C1C;
  --divider:      #D4D4C8;
  --font-display: 'DM Serif Display', serif;
  --font-body:    'DM Sans', sans-serif;
}
```

Font CDN:
```html
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
```

Data palette (rich single-accent approach for this neutral style):
```javascript
const palette = ['#1C1C1C','#525252','#737373','#A3A3A3','#D4D4D4','#404040','#262626'];
// For multi-series, add a single accent color:
// const palette = ['#1C1C1C','#D97706','#525252','#92400E','#A3A3A3','#404040','#262626'];
```

Grid line color: `rgba(0,0,0,0.09)`
Axis tick color: `#737373`

**Best for:** Internal reviews, board materials, consultancy reports, mixed professional audiences.

---

## 4. electric-burst

**Character:** Bold. High-contrast. Energy.

```css
:root {
  --bg:           #09090B;
  --bg-elevated:  #18181B;
  --text:         #FAFAFA;
  --text-muted:   #A1A1AA;
  --accent:       #FACC15;
  --divider:      #27272A;
  --font-display: 'Space Grotesk', sans-serif;
  --font-body:    'DM Sans', sans-serif;
}
```

Font CDN:
```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
```

Data palette:
```javascript
const palette = ['#FACC15','#60A5FA','#4ADE80','#F87171','#A78BFA','#FB923C','#34D399'];
const paletteAlpha = ['rgba(250,204,21,0.18)','rgba(96,165,250,0.18)','rgba(74,222,128,0.18)','rgba(248,113,113,0.18)','rgba(167,139,250,0.18)','rgba(251,146,60,0.18)','rgba(52,211,153,0.18)'];
```

Grid line color: `rgba(255,255,255,0.07)`
Axis tick color: `#A1A1AA`

**Accent usage rule for electric-burst:** Yellow (`#FACC15`) on the primary dataset or highlight annotation only. Use blue/green for secondary series. Yellow everywhere = no yellow.

**Best for:** Growth metrics, social media content, startup metrics, bold data stories for tech audiences.

---

## 5. brutalist

**Character:** Raw. Stark. Confrontational. Zero decoration.

```css
:root {
  --bg:           #FFFFFF;
  --bg-elevated:  #F5F5F5;
  --text:         #000000;
  --text-muted:   #666666;
  --accent:       #FF0000;
  --divider:      #000000;
  --font-display: 'Space Mono', monospace;
  --font-body:    'Space Mono', monospace;
}
```

Font CDN:
```html
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
```

Data palette:
```javascript
const palette = ['#000000','#FF0000','#555555','#888888','#BBBBBB','#333333','#777777'];
const paletteAlpha = ['rgba(0,0,0,0.15)','rgba(255,0,0,0.15)','rgba(85,85,85,0.15)','rgba(136,136,136,0.15)','rgba(187,187,187,0.15)','rgba(51,51,51,0.15)','rgba(119,119,119,0.15)'];
```

Grid line color: `rgba(0,0,0,0.15)`
Axis tick color: `#666666`

**Chart.js defaults override for brutalist:**
```javascript
Chart.defaults.font.family = 'Space Mono, monospace';
Chart.defaults.color = '#666666';
Chart.defaults.borderColor = 'rgba(0,0,0,0.15)';
```

**Best for:** Design-forward agencies, bold comparisons, impact charts where the data itself is the aesthetic.

---

## Chart.js Global Defaults — Set Before Chart Init

Apply immediately after `document.fonts.ready.then(() => {`:
```javascript
Chart.defaults.font.family = getComputedStyle(document.documentElement)
  .getPropertyValue('--font-body').trim() || 'system-ui, sans-serif';
Chart.defaults.color = '#64748B';        // use --text-muted value for each preset
Chart.defaults.borderColor = '#E2E8F0'; // use --divider value for each preset
```

Per-preset `Chart.defaults.color` values:
- clean-slate: `#64748B`
- midnight-editorial: `#9CA3AF`
- matt-gray: `#737373`
- electric-burst: `#A1A1AA`
- brutalist: `#666666`

Per-preset `Chart.defaults.borderColor` values:
- clean-slate: `rgba(226,232,240,1)` → `#E2E8F0`
- midnight-editorial: `rgba(45,45,45,1)` → `#2D2D2D`
- matt-gray: `rgba(212,212,200,1)` → `#D4D4C8`
- electric-burst: `rgba(39,39,42,1)` → `#27272A`
- brutalist: `rgba(0,0,0,0.15)`
