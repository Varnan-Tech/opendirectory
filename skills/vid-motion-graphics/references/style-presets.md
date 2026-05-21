# Style Presets — vid-motion-graphics

5 motion-optimized style presets. Each includes CSS tokens, font stack, Google Fonts CDN link, and animation personality.

Read this file before generating any HTML in Step 3.

---

## 1. kinetic-dark (default)

**Feel:** High-energy. Electric yellow on near-black. Tight grotesque. Fast-in, slow-hold.
**Best for:** Product launches, growth metrics, startup content.

```css
/* Font CDN */
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700;800&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">

:root {
  --bg:           #0A0A0A;
  --text:         #FAFAFA;
  --text-muted:   #888888;
  --accent:       #F5FF00;
  --accent-dim:   rgba(245,255,0,0.15);
  --divider:      rgba(255,255,255,0.10);
  --font-display: 'Space Grotesk', sans-serif;
  --font-body:    'DM Sans', sans-serif;
  --font-mono:    'Space Grotesk', monospace;
}
```

**Data palette:** `['#F5FF00', '#60A5FA', '#4ADE80', '#F87171', '#A78BFA']`

**Animation feel:**
- In: `translateY(24px) → 0, opacity 0 → 1` over first 8% of scene
- Hold: static for 80% of scene
- Out: `translateY(-12px), opacity → 0` over last 12% of scene
- Easing: `cubic-bezier(0.22, 1, 0.36, 1)` for in, `linear` for out

---

## 2. editorial-light

**Feel:** Refined. Ink on paper. Serif display. Long hold, gentle crossfade.
**Best for:** Thought leadership, executive communications, annual reports.

```css
/* Font CDN */
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Source+Serif+4:wght@400;600&display=swap" rel="stylesheet">

:root {
  --bg:           #FAFAF8;
  --text:         #111111;
  --text-muted:   #777777;
  --accent:       #111111;
  --accent-dim:   rgba(17,17,17,0.08);
  --divider:      rgba(0,0,0,0.10);
  --font-display: 'Playfair Display', serif;
  --font-body:    'Source Serif 4', serif;
  --font-mono:    'Source Serif 4', monospace;
}
```

**Data palette:** `['#111111', '#3B82F6', '#16A34A', '#DC2626', '#7C3AED']`

**Animation feel:**
- In: `opacity 0 → 1` only, over first 10% of scene (no transform)
- Hold: static for 85% of scene
- Out: `opacity → 0` over last 5% of scene
- Easing: `ease-in-out` throughout

---

## 3. data-pulse

**Feel:** Terminal/dashboard. Deep navy, electric blue, monospaced. Scan-line entrance.
**Best for:** Technical metrics, engineering announcements, SaaS dashboards.

```css
/* Font CDN */
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500&display=swap" rel="stylesheet">

:root {
  --bg:           #050B1A;
  --text:         #E8F4FF;
  --text-muted:   #4A7FA5;
  --accent:       #00C2FF;
  --accent-dim:   rgba(0,194,255,0.12);
  --divider:      rgba(0,194,255,0.15);
  --font-display: 'IBM Plex Mono', monospace;
  --font-body:    'IBM Plex Sans', sans-serif;
  --font-mono:    'IBM Plex Mono', monospace;
}
```

**Data palette:** `['#00C2FF', '#4ADE80', '#F5FF00', '#F87171', '#A78BFA']`

**Animation feel:**
- In: `translateX(-8px) → 0, opacity 0 → 1` with slight stagger on text lines
- Hold: static with subtle `box-shadow` pulse on accent elements
- Out: `opacity → 0, translateX(8px)` — slide out opposite direction
- Easing: `steps(4)` for entrance (scan-line effect), `linear` for exit

---

## 4. bold-type

**Feel:** Brutalist typographic. White bg, black/red, maximum weight. Slam in.
**Best for:** Announcements, milestones, provocative statements.

```css
/* Font CDN */
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;700&display=swap" rel="stylesheet">

:root {
  --bg:           #FFFFFF;
  --text:         #000000;
  --text-muted:   #555555;
  --accent:       #FF2B00;
  --accent-dim:   rgba(255,43,0,0.10);
  --divider:      #000000;
  --font-display: 'Bebas Neue', sans-serif;
  --font-body:    'Inter', sans-serif;
  --font-mono:    'Inter', monospace;
}
```

**Data palette:** `['#FF2B00', '#000000', '#1D4ED8', '#16A34A', '#9333EA']`

**Animation feel:**
- In: `scale(1.08) → 1, opacity 0 → 1` over first 5% of scene (slam)
- Hold: static for 90% of scene
- Out: `scale(0.96), opacity → 0` over last 5% of scene (snap)
- Easing: `cubic-bezier(0.34, 1.56, 0.64, 1)` for in (overshoot), `linear` for out

---

## 5. minimal-clean

**Feel:** Warm, refined. Off-white, ink-warm neutrals, thin serif display. Gentle rise.
**Best for:** People-focused content, hiring, testimonials, brand storytelling.

```css
/* Font CDN */
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">

:root {
  --bg:           #F5F4F0;
  --text:         #1A1A18;
  --text-muted:   #8A8A82;
  --accent:       #1A1A18;
  --accent-dim:   rgba(26,26,24,0.06);
  --divider:      rgba(26,26,24,0.12);
  --font-display: 'Cormorant Garamond', serif;
  --font-body:    'Jost', sans-serif;
  --font-mono:    'Jost', monospace;
}
```

**Data palette:** `['#1A1A18', '#6366F1', '#16A34A', '#CA8A04', '#DC2626']`

**Animation feel:**
- In: `translateY(32px) → 0, opacity 0 → 1` over first 12% of scene
- Hold: static for 80% of scene
- Out: `opacity → 0` only (no transform) over last 8%
- Easing: `cubic-bezier(0.25, 0.46, 0.45, 0.94)` throughout

---

## renderFrame Timing Quick Reference

All scene timing is computed in `window.renderFrame(t)` (milliseconds). No CSS `@keyframes`.

For a scene at `[startMs, endMs)`:
```javascript
const prog = (t - startMs) / (endMs - startMs); // 0.0 → 1.0
// Enter:  prog 0.00–0.10 → opacity 0→1, translateY 24px→0 (easeOutCubic)
// Hold:   prog 0.10–0.85 → opacity 1, no transform
// Exit:   prog 0.85–1.00 → opacity 1→0, translateY 0→-12px
// Hidden: t < startMs or t >= endMs → opacity 0
```

**Example — 3 scenes, 3s each, 9s total:**
```javascript
// scene 1: 0ms–3000ms  | scene 2: 3000ms–6000ms  | scene 3: 6000ms–9000ms
window.renderFrame = function(t) {
  applySceneState(document.querySelector('.scene-1'), sceneState(t, 0,    3000));
  applySceneState(document.querySelector('.scene-2'), sceneState(t, 3000, 6000));
  applySceneState(document.querySelector('.scene-3'), sceneState(t, 6000, 9000));
};
```

**Animation feel by preset (all implemented in sceneState/easing):**

| Preset | Enter transform | Enter easing | Exit transform |
|---|---|---|---|
| kinetic-dark | translateY(24px)→0 | easeOutCubic | translateY(0→-12px) |
| editorial-light | opacity only | ease-in-out | opacity only |
| data-pulse | translateX(-8px)→0 | easeOutCubic | translateX(0→8px) |
| bold-type | scale(1.08)→1 | easeOutCubic (overshoot) | scale(1→0.96) |
| minimal-clean | translateY(32px)→0 | easeOutCubic | opacity only |

Adapt `sceneState()` or add a style-specific `enterTransform`/`exitTransform` param to match the preset's feel.
