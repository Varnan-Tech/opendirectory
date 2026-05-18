# Design System — graphic-ebook

A4 portrait reading document typography and spacing. Tuned for 1200px viewport where **1vw = 12px**.

---

## Why Different from graphic-slide-deck

| | graphic-slide-deck | graphic-ebook |
|---|---|---|
| Viewport | 1920×1080px | 1200×1697px |
| Primary medium | Display headlines | Body copy |
| Line-height | 1.2–1.4 | 1.75 |
| Body max-width | Full width OK | ≤65ch enforced |
| Stat numbers | Up to `clamp(3.5rem, 12vw, 9rem)` | `clamp(2.5rem, 7vw, 5rem)` |
| Purpose | Audience reads from distance | Reader reads at arm's length |

---

## Typography Scale

All values use `clamp(min, preferred-vw, max)`. At 1200px viewport, 1vw = 12px.

```
Cover title:            clamp(2rem, 5vw, 3.5rem)        60px at 1200px
Chapter heading (h2):   clamp(1.5rem, 3.5vw, 2.8rem)    42px at 1200px
Section heading (h3):   clamp(1rem, 1.8vw, 1.4rem)       21.6px at 1200px
Body text:              clamp(0.875rem, 1.25vw, 1.05rem)  15px at 1200px
Sidebar body:           clamp(0.8rem, 1.1vw, 0.95rem)     13.2px at 1200px
Stat number (hero):     clamp(3rem, 8vw, 5.5rem)          96px at 1200px
Stat number (support):  clamp(2.5rem, 7vw, 5rem)          84px at 1200px
Pull quote:             clamp(1.2rem, 2.2vw, 1.75rem)     26.4px at 1200px  (italic, display font)
TOC entry:              clamp(0.875rem, 1.4vw, 1.1rem)     16.8px at 1200px
Caption / label:        clamp(0.62rem, 0.9vw, 0.78rem)    10.8px at 1200px
Chapter number (deco):  clamp(6rem, 18vw, 14rem)          decorative, opacity 0.06–0.08
Callout label:          clamp(0.58rem, 0.8vw, 0.68rem)    uppercase, 0.12em tracking
Page footer:            clamp(0.55rem, 0.75vw, 0.65rem)   uppercase, 0.1em tracking
```

---

## Line-Height

| Element | Line-height |
|---|---|
| Body text | 1.75 |
| Sidebar body | 1.65 |
| Chapter headings (h2) | 1.15 |
| Section headings (h3) | 1.2 |
| Pull quote | 1.4 |
| TOC entries | 1.3 |
| Cover title | 1.08 |
| Stat numbers | 0.9 |

---

## Letter-Spacing

| Element | Tracking |
|---|---|
| Cover title / headlines | `-0.03em` |
| Chapter headings | `-0.02em` |
| Body text | `0` |
| Labels / captions | `+0.10em` to `+0.14em` |
| Callout labels | `+0.12em` |
| Page footer | `+0.10em` |
| Stat labels | `+0.12em` |

---

## Body Copy Max-Width

Enforce max-width on all paragraph text — uncontrolled line length is the #1 readability failure in AI-generated ebooks.

| Layout | Max-width |
|---|---|
| text-column 1-col body | `min(65ch, 100%)` |
| text-column 2-col each column | natural (fills 50% minus gap) |
| text-sidebar main | natural (fills ~66% minus gap) |
| text-sidebar callout | natural (fills ~33% minus gap) |
| quote-callout | `max-width: 32ch` on the quote |
| stat-grid narrative | `max-width: 70ch` |
| key-takeaways items | natural |

---

## Spacing Rhythm

Valid spacing values: 8 / 16 / 24 / 32 / 48 / 64 / 96px only.

```
Page padding:       clamp(2.5rem, 6%, 4.5rem)       40–72px
Section gap:        clamp(1.5rem, 3%, 3rem)          24–48px
Content gap:        clamp(0.875rem, 1.5%, 1.75rem)   14–28px
Element gap:        clamp(0.5rem, 1%, 1rem)           8–16px
Paragraph gap:      clamp(0.875rem, 1.5%, 1.4rem)    14–22px
Column gap:         clamp(2rem, 4%, 3.5rem)           32–56px
Callout padding:    clamp(0.75rem, 1.5%, 1.1rem)      12–17px
Footer padding:     clamp(0.5rem, 1%, 0.625rem)       8–10px
```

---

## Page Footer

Every page except cover must have a footer. It is the single most common missing element in mediocre AI ebooks — its presence signals quality.

```css
.page-footer {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  padding: clamp(0.5rem, 1%, 0.625rem) var(--page-padding);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--divider);
  font-family: var(--font-body);
  font-size: clamp(0.55rem, 0.75vw, 0.65rem);
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-muted);
}
```

HTML: `<div class="page-footer"><span>[Brand Name]</span><span>[Page Number]</span></div>`

Footer height is ~2.5–3rem. Account for this in the slide content area: add `padding-bottom: 3rem` to all non-cover `.slide` inner containers.

---

## Typed Callout System

5 callout types, each with a unique color token. Never use a generic "just bold the box" approach — the type distinction is part of the design quality signal.

| Type | CSS class | Border color | Background tint |
|---|---|---|---|
| Pro Tip | `.callout--tip` | `#16A34A` (green) | `rgba(22, 163, 74, 0.07)` |
| Warning | `.callout--warning` | `#D97706` (amber) | `rgba(217, 119, 6, 0.07)` |
| Stat callout | `.callout--stat` | `var(--accent)` | `rgba(var(--accent-rgb), 0.07)` |
| Quote | `.callout--quote` | `var(--divider)` | `var(--bg-elevated)` |
| Checklist | `.callout--checklist` | `#0891B2` (teal) | `rgba(8, 145, 178, 0.07)` |

Base callout CSS:
```css
.callout {
  border-left: 3px solid;
  border-radius: var(--card-radius, 4px);
  padding: clamp(0.75rem, 1.5%, 1.1rem);
}
.callout-label {
  font-size: clamp(0.58rem, 0.8vw, 0.68rem);
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 0.5em;
  display: block;
}
.callout-body {
  font-size: clamp(0.8rem, 1.1vw, 0.95rem);
  line-height: 1.6;
  color: var(--text-secondary);
}
```

---

## Visual Rhythm Rule

**Never place 2+ text-column pages consecutively.**

At minimum, insert one of the following between any two text-column pages:
- `chapter-intro` (signals new section, very open)
- `quote-callout` (full-page visual break)
- `stat-grid` (numbers and space — contrast from body copy)
- `key-takeaways` (structured list, different visual weight)

Flat reading decks with no visual rhythm feel like Google Docs exports. The layout variety IS part of the design. The reader's eye needs contrast across pages to stay engaged.

---

## Body Copy Density Limits

At 1200×1697px with 40–72px page padding and a 3rem footer reserve:

| Layout | Word count | Notes |
|---|---|---|
| text-column 1-col | 180–250 words max | Split into 2 pages if over |
| text-column 2-col | 280–380 words (140–190 per col) | Dense reference content only |
| text-sidebar | 140–180 words main + ≤70 sidebar | Main col = 2/3 width |
| chapter-intro | 40–60 words | Teaser only — nothing else |
| quote-callout | 30–45 words | Quote only — nothing else |
| stat-grid | 3–6 metrics + optional 1-sentence narrative | No paragraphs |
| key-takeaways | 5–8 items × ≤15 words | Imperative phrasing |
| closing-cta | ≤30 words total | Headline + 1 sentence + contact |

---

## Three-Point CTA Architecture

For ebooks ≥ 6 pages, embed three CTA touchpoints — not just the closing page:

**1. Intro CTA (page 2 or 3):**
Subtle inline mention within the first body section or TOC page:
> "All templates referenced in this guide are at [url]"

**2. Mid-ebook CTA (after a stat-grid or chapter-intro):**
Small `.callout--stat` or `.callout--tip` box:
```html
<div class="callout callout--tip">
  <p class="callout-label">Next Step</p>
  <p class="callout-body">See how [Brand] addresses this. 20-min demo at [url]</p>
</div>
```

**3. Closing CTA (final page):**
Full-page `closing-cta` layout with email + URL. The primary conversion page.

---

## DO NOT USE — Slop Checklist

Before outputting any HTML, verify none of these are present:

| Pattern | Why wrong |
|---|---|
| Inter as display font | Zero typographic character — reads as default AI output |
| Body copy filling 100% page width | Unreadable — enforce `max-width: min(65ch, 100%)` |
| Same background on every page | No visual rhythm — reads as one flat wall of text |
| Stat numbers at body text size | Defeats the purpose of the stat-grid layout |
| Bullets for everything | Body paragraphs need real prose, not lists |
| Placeholder boxes for images | Never show `[IMAGE]` boxes — CSS-generated visuals only |
| "Thank You" on closing CTA | No action, no contact info = wasted page |
| Chapter numbers at body size | Must be oversized decorative element (opacity 0.06) |
| Identical column layout on all pages | No typographic thinking — visual rhythm is mandatory |
| Missing page footers | Immediately signals "AI template" — every real ebook has them |
| Generic callout boxes (no type distinction) | All-same-color sidebars = template output |
| Missing `-webkit-print-color-adjust: exact` | All background colors disappear in PDF export |
| Line-height < 1.65 on body text | Cramped — reading documents need room to breathe |
| `accent color on 5+ elements per section` | Kills scarcity — accent means important, not everywhere |
| Helvetica Neue / Arial as display font | Generic — no personality at display size |
