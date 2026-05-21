# Design System — graphic-case-study

Typography, spacing, and design rules for A4 portrait case study pages. All tokens tuned for 1200px viewport width (A4 portrait format via Playwright).

---

## Typography Scale

All values use `clamp()`. At 1200px viewport: 1vw = 12px.

```
Cover headline:         clamp(2rem, 5vw, 3.5rem)       -- 60px at 1200px
Section heading (h2):   clamp(1.25rem, 2.5vw, 2rem)    -- 30px at 1200px
Body text:              clamp(0.875rem, 1.25vw, 1.1rem) -- 15px at 1200px
Stat number (hero):     clamp(3rem, 8vw, 5.5rem)        -- 96px at 1200px | accent color
Stat number (support):  clamp(2.5rem, 7vw, 5rem)        -- 84px at 1200px | secondary color
Quote text:             clamp(1.1rem, 2vw, 1.5rem)      -- 24px at 1200px | italic, display font
Stat label:             clamp(0.7rem, 1vw, 0.875rem)    -- 12px | uppercase, 0.1em tracking
Caption / label:        clamp(0.65rem, 0.9vw, 0.8rem)   -- 10.8px | uppercase, 0.12em tracking
```

**Why these differ from graphic-slide-deck:**
- Viewport is 1200px not 1920px -- vw values resolve smaller
- A4 is a reading document, not a projector slide -- body text minimum is higher
- Stat numbers cap at 5.5rem not 9rem -- A4 proportions, not stadium-screen scale
- Generous minimum clamp values ensure readability in print PDF export

**Letter spacing:**
- Cover/display headlines: `-0.03em`
- Section headings: `-0.02em`
- Body: `0` (no letter spacing -- readability first)
- Labels/captions: `+0.1em` to `+0.14em`

---

## Spacing Rhythm

Valid values: 8 / 16 / 24 / 32 / 48 / 64 / 96px. No arbitrary values.

```
Page padding:         clamp(2.5rem, 6%, 4.5rem)        -- 40–72px
Section gap:          clamp(1.5rem, 3%, 3rem)           -- 24–48px
Content gap:          clamp(0.875rem, 1.5%, 1.75rem)    -- 14–28px
Element gap:          clamp(0.5rem, 1%, 1rem)            -- 8–16px
Column gap:           clamp(1.5rem, 4%, 3rem)            -- 24–48px
```

---

## One Hero Metric Rule

Every results section has exactly ONE metric that is visually dominant:
- Hero metric: accent color, `clamp(3rem, 8vw, 5.5rem)`, full opacity
- Supporting metrics: secondary text color, `clamp(2.5rem, 7vw, 5rem)`, full opacity
- Context line below: body color, body size, max 12 words

**This is the single thing the reader remembers.** If two metrics fight for dominance, neither wins.

---

## Page Density Guide

Each page section has a natural density:

| Section | Density | Key rule |
|---|---|---|
| cover | Very open | Headline + company name only. Breathe. |
| overview | Moderate | 4 fact cells in a 2×2 grid. No paragraphs. |
| challenge | Moderate-dense | Context paragraph + 3 pain points. |
| solution | Moderate | 2-3 feature callouts. CSS icon shapes. |
| results | Very open | Numbers need space. Nothing competes. |
| testimonial | Very open | The quote fills the section. Nothing else. |
| closing-cta | Open | One action. Contact info. Done. |

**Stacking rule for 1-pager and 2-pager:** When multiple sections share a page, alternate dense sections with open ones. Never stack two dense sections. Never stack two open sections unless one is tiny (e.g., a 2-line testimonial after a big results block).

---

## Background Depth

Use subtle background variation to create visual rhythm across pages:
- Cover: style preset's primary background (often dark or richly styled)
- Overview / Challenge: slightly lighter/alternate background from preset
- Solution: main slide background
- Results: main slide background (never alter -- numbers need neutral ground)
- Testimonial: accent color at 5-8% opacity OR preset's alternate section bg
- Closing CTA: dark or full-accent background (inversion for finality)

---

## Slop Patterns to Avoid

| Pattern | Why it's wrong |
|---|---|
| Inter as display font | Generic -- no character at heading size |
| Every section same background | No visual rhythm across pages |
| Stat numbers at body text size | Defeats the results section entirely |
| Bullet list format for testimonial | A quote is a quote, not a list |
| "Thank You" as closing-cta headline | Wasted opportunity -- no action, no contact |
| Gradient on every section | Cheap depth signal, fights the editorial feel |
| Unstyled logo placeholder boxes | Looks unfinished -- use CSS initials or shape |
| Purple-to-blue gradient on white | Overused AI aesthetic -- signals no design thinking |
| Body text same color on every section | No hierarchy, no visual rhythm |
| Results stats smaller than section headings | Hierarchy inverted -- misses the point |
