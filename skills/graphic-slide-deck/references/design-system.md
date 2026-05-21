# Slide Deck Design System

Premium slide design. Every deck should look considered and editorial -- not template output.

---

## Design Philosophy

Slides are seen at 1920×1080 on a projector or 1080×1080 on a phone screen. The design must work at both extremes. Everything scales via `clamp()` -- no fixed sizes that break at non-standard viewports.

One rule above all others: **one loud slide per deck.** Every other slide is composed and quiet. The unmissable slide breaks that rhythm -- that contrast is what makes it work.

---

## Typography Tokens

All values use `clamp()`. Never fixed px/rem on any element that scales.

```
Display (title-hero headline):   clamp(2.5rem, 8vw, 6rem)    | letter-spacing: -0.04em
Section heading (h2):            clamp(1.75rem, 4vw, 3.5rem) | letter-spacing: -0.02em
Body text:                       clamp(0.875rem, 1.5vw, 1.125rem)
Stat number (stat-highlight):    clamp(3.5rem, 12vw, 9rem)   | font-weight: 700 or 900
Stat label (below number):       clamp(0.7rem, 1.2vw, 1rem)  | letter-spacing: 0.12em | uppercase
Quote text (quote-callout):      clamp(1.25rem, 3vw, 2.25rem) | italic | display font
Caption / badge text:            clamp(0.65rem, 1vw, 0.875rem) | letter-spacing: 0.12em | uppercase
Timeline label:                  clamp(0.75rem, 1.2vw, 1rem)
```

**Weight contrast rule:**
Display font at 700-900 + body at 400 = correct pairing.
Body font on dark bg: use `#CCCCCC` or `#AAAAAA` -- never `#888888` (too low contrast on dark).

**Letter-spacing rules:**
- Very large display (6rem+): `-0.04em` (tighter = more authoritative)
- Section headings (3-3.5rem): `-0.02em`
- Stats and labels (uppercase small): `0.12em` minimum
- Body: `0` -- never add tracking to body text

---

## Spacing Rhythm

**Valid spacing values (slide scale):** 8 / 16 / 24 / 32 / 48 / 64 / 80 / 96px

Never use arbitrary values like 18px, 30px, 45px. They break visual rhythm.

Implemented via `clamp()`:
```
Slide padding:   clamp(2rem, 5vw, 5rem)      -- outer slide padding
Content gap:     clamp(1rem, 2.5vw, 2.5rem)  -- between major content blocks
Element gap:     clamp(0.5rem, 1.5vw, 1.5rem) -- between list items, small elements
Column gap:      clamp(1.5rem, 3vw, 4rem)    -- between grid columns
```

---

## The One Loud Slide Rule

Every deck must have exactly ONE slide with maximum visual intensity:
- Largest typography on that slide
- The style preset's signature element at full intensity
- The strongest animation (counter effect, staggered reveal, etc.)
- Maximum contrast with the surrounding slides

All other slides must be compositionally quieter -- structured, composed, predictable. The contrast is what makes the loud slide work. A deck where every slide is loud has no loud slides.

**What qualifies as the unmissable slide:**
- stat-highlight with metrics that fill the slide (numbers at `clamp(3.5rem, 12vw, 9rem)`)
- quote-callout with a devastating one-liner in Instrument Serif italic
- title-hero if the headline IS the entire story in 5 words

**What doesn't qualify:** A text-full slide with an extra bold heading.

---

## Background as Atmosphere

Slide decks can use CSS-generated backgrounds. Email cannot -- slides can. These are first-class design choices:

- **Gradient mesh:** layered `radial-gradient()` blobs, different colors, overlapping
- **Grid pattern:** `linear-gradient()` + `background-size` creating grid lines (common in brutalist, product-minimal styles)
- **Noise texture:** inline SVG `<feTurbulence>` filter applied to a pseudo-element
- **Geometric accent:** large CSS shapes (circles, rectangles) at low opacity as background elements

Reference `frontend-slides/animation-patterns.md` for exact CSS snippets for each effect.

Reserve atmospheric backgrounds for section-divider slides and the unmissable slide. Body content slides should have clean backgrounds to maintain readability.

---

## Density Contrast as Craft Signal

Rhythm: Open → Dense → Open → Dense → Open (CTA)

- title-hero: maximum open space (large padding, few elements, generous line-height)
- section-divider: maximum open space (single bold label, no body)
- text-full / comparison-table: dense (tight content, purpose is information delivery)
- stat-highlight: maximum open space (numbers need breathing room to read large)
- closing-cta: maximum open space (one action, nothing competing)

Open slides feel intentional. Dense slides feel earned because they're surrounded by open space.

---

## Layout Alternation for Visual Rhythm

Avoid repeating the same layout back-to-back unless content demands it:
- text-full → text-full: acceptable if different visual treatment (bullets vs. paragraphs, different bg)
- stat-highlight → stat-highlight: avoid -- collapses the "loud" moment
- two text-left-image-right in a row: break with a section-divider between them

---

## Slide Slop Patterns to Avoid

These produce generic AI-looking output:

| Pattern | What it signals | Fix |
|---|---|---|
| Every slide: headline + 5 bullets, centered | No layout thinking, template dump | Vary layout types per content need |
| All slides same background color | No visual rhythm | Use section-dividers, alternate bg per style |
| Stat numbers at body text size | Doesn't understand visual hierarchy | Stats must be 3× minimum body size |
| Animation on every element, every slide | Desperate filler | Reserve animation for the ONE unmissable slide |
| Image placeholder boxes visible in final output | Unfinished | Replace with CSS-generated visuals or remove |
| Closing slide: just "Thank You" | Missed the point of a closing slide | CTA + email + URL minimum |
| Inter as display font | Zero typographic character | Use the preset's display font |
| Purple gradient on white bg | Generic AI aesthetic | If soft-cloud/product-minimal needed: use preset tokens, not defaults |

---

## CSS Technical Rules

These rules come from `frontend-slides/viewport-base.css` -- they are non-negotiable:

```css
/* Every slide */
.slide {
  height: 100vh;
  height: 100dvh;
  overflow: hidden;
}

/* All font sizes and spacing must use clamp() */
font-size: clamp(min, preferred, max);
padding: clamp(min, preferred, max);
gap: clamp(min, preferred, max);

/* Images */
img {
  max-height: min(50vh, 400px);
  object-fit: cover;
}

/* NEVER use negated clamp/min/max directly */
/* Wrong:  margin-top: -clamp(1rem, 2vw, 2rem); */
/* Right:  margin-top: calc(-1 * clamp(1rem, 2vw, 2rem)); */
```

**What NOT to use in slide CSS:**
- `display:flex` / `display:grid` -- OK in slide content (not in outer shell)
- `position:fixed` -- no fixed elements inside slides
- `min-height` / `max-height` on `.slide` -- height:100vh is the constraint; these fight it
- CSS custom properties (`--var`) for font-size values inside `clamp()` -- some browsers handle poorly
- `vh` units inside `calc()` mixed with `rem` without explicit conversion
