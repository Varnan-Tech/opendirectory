# Animation Guide

Decision rules for when and where to apply animations. For CSS/JS implementation snippets, read `/Users/ksd/Desktop/Varnan_skills/frontend-slides/animation-patterns.md` directly. This guide tells you WHICH snippets to use -- that file tells you HOW.

---

## The One Dramatic Moment Rule

Every deck has exactly ONE slide with maximum animation intensity. All other slides use the same minimal entrance animation.

This is not a suggestion. A deck where every slide has elaborate animation trains the audience to ignore animation as filler. The one dramatic slide lands because every other slide was quiet.

**What counts as maximum intensity:**
- Counter animation on stat numbers (counting up to the final value)
- Staggered multi-element entrance (each stat/bullet appears with a slight delay)
- Background effect (gradient mesh, grid pattern, particle-like CSS animation)
- Combined: dramatic entrance + background effect on the same slide

**What counts as minimal (the default for all other slides):**
- Single fade + slide-up on the slide content block (the `.reveal` class)
- 200-400ms duration, `ease-out` or `ease-out-expo` easing
- No staggering on regular slides

---

## Animation Budget by Deck Type

### Investor pitch
- **Default entrance:** Fade + slide-up on `.slide-content` (300ms ease-out)
- **Unmissable slide (stat-highlight):** Counter animation on each stat number + staggered entrance (each stat appears 150ms after the previous)
- **Avoid:** Particle systems, glitch effects, 3D tilt on hover, parallax scrolling

### Sales deck
- **Default entrance:** Scale-in on `.slide-content` (`transform: scale(0.97)` → `scale(1)`, 300ms)
- **Unmissable slide (stat-highlight):** Counter animation on the ROI number + brief background flash
- **Avoid:** Bouncy easing (`cubic-bezier` with values > 1), script/handwritten fonts on animated text, anything > 500ms

### Conference talk
- **Default entrance:** Blur-in (blur from 8px to 0, 400ms ease-out) on main content block
- **Unmissable slide:** Staggered text reveals + ONE background effect (gradient mesh or grid pattern CSS animation)
- **Background effect:** Subtle animated gradient or grid on section-divider slides only -- not on content slides
- **Avoid:** Corporate navy as the dominant color (defeats the conference aesthetic), same entrance on every single element

### Internal presentation
- **Default entrance:** Simple fade (opacity 0 → 1, 150ms ease)
- **Unmissable slide:** Same fade -- no dramatic animation for internal decks
- **Avoid:** Any animation that could be perceived as distracting in a board meeting

---

## Which Snippets to Use from animation-patterns.md

Reference these specific sections from `/Users/ksd/Desktop/Varnan_skills/frontend-slides/animation-patterns.md`:

**For investor/sales decks → Core Entrance Animations section:**
- "Fade + Slide Up" -- most versatile, use for default slide entrance
- "Scale In" -- good for sales decks, slightly warmer feeling

**For conference talks → Core Entrance Animations + Background Effects:**
- "Blur In" -- for headline entrances
- "Gradient Mesh" -- for section-divider backgrounds
- "Grid Pattern" -- for technical/developer conference decks

**For the one dramatic slide → Interactive Effects:**
- Counter animation for stat numbers -- in the Optional Enhancements section of html-template.md

**For ALL decks → Intersection Observer setup:**
The `.reveal` class + Intersection Observer pattern from html-template.md. This is the backbone of all entrance animations. Every slide's content block gets `class="reveal"` and becomes visible when scrolled into view.

---

## Animation Reference Table

| Deck type | Default slide | Unmissable slide | Background effects | Avoid |
|---|---|---|---|---|
| Investor pitch | Fade + slide-up (300ms) | Counter + staggered stats | None | Particles, glitch, 3D tilt |
| Sales deck | Scale-in (300ms) | Counter on ROI number | None | Bouncy easing, > 500ms |
| Conference talk | Blur-in (400ms) | Staggered + gradient mesh | Section dividers only | Corporate uniformity |
| Internal | Fade (150ms) | Fade only | None | Any elaborate animation |
| Onboarding (soft-cloud) | Fade + slide-up (250ms) | Staggered steps | Light gradients OK | Heavy or aggressive motion |

---

## Technical Notes

**Stagger implementation:** Apply `animation-delay: calc(var(--i) * 0.15s)` to each stat or bullet element, where `--i` is set via inline style (`style="--i: 0"`, `style="--i: 1"`, etc.).

**Counter animation:** Target `.stat-number` elements. Read the full JS implementation from `html-template.md`'s Optional Enhancements section. Briefly: count from 0 to final value over ~1.2 seconds using `requestAnimationFrame`, applying `easeOutExpo` curve.

**`prefers-reduced-motion` is mandatory:** Every animation must have a corresponding reduced-motion override. The pattern from `viewport-base.css`:
```css
@media (prefers-reduced-motion: reduce) {
  .reveal { opacity: 1; transform: none; transition: none; }
  /* Disable all transforms and transitions */
}
```

**Do not animate layout properties:** Never animate `height`, `width`, `padding`, `margin`. Only animate `opacity`, `transform`, `filter`. Layout animations trigger expensive reflows.

**Performance check:** If a background effect uses CSS animation (like an animated gradient), add `will-change: transform` or `will-change: opacity` to the animated element -- but only for that one element, not globally.
