# Layout Library

13 named slide layout patterns. For each: HTML structure, CSS approach, density limits, and when to use.

---

## 1. title-hero

**Use for:** Opening slide. The first thing the audience sees.
**Do not use for:** Any slide other than the first (or first slide of a major section).

**Content limits:**
- Headline: 6 words max
- Subtitle: 1 sentence
- Optional: pill badge (4 words max), background image or CSS gradient

**HTML structure:**
```html
<section class="slide slide--title-hero">
  <div class="slide-content">
    <span class="badge">OPTIONAL BADGE TEXT</span>
    <h1>Headline Here</h1>
    <p class="subtitle">One sentence subtitle that expands on the headline.</p>
  </div>
</section>
```

**CSS approach:**
- Flexbox column: `align-items: flex-start; justify-content: center` (left-aligned, vertically centered)
- Lower-third variant: `justify-content: flex-end; padding-bottom: clamp(3rem, 6vw, 6rem)`
- Background: full-bleed CSS gradient or `background-image: url(data:...)` with `background-size: cover`
- Badge pill: `border-radius: 100px; padding: 0.3em 1em; font-size: clamp(0.65rem, 1vw, 0.875rem); letter-spacing: 0.14em; text-transform: uppercase`
- Headline: `font-size: clamp(2.5rem, 8vw, 6rem); letter-spacing: -0.04em; line-height: 1`
- Subtitle: `font-size: clamp(0.875rem, 1.5vw, 1.25rem); max-width: 55%; opacity: 0.8`

**Signature element:** Oversized headline with extremely tight tracking (`-0.04em`). The headline is a poster.

---

## 2. section-divider

**Use for:** Marking the start of a new section or chapter in the deck.
**Do not use for:** Slides that have any body content.

**Content limits:**
- Section label: 2-4 words max
- Optional: section number, sub-label (1 line)

**HTML structure:**
```html
<section class="slide slide--section-divider">
  <div class="slide-content">
    <span class="section-number">01</span>
    <h2>Section Label</h2>
    <p class="sub-label">Optional one-line description</p>
  </div>
</section>
```

**CSS approach:**
- Background: style's accent color, or strongly contrasting bg (dark on light deck, light on dark)
- Flexbox column, centered horizontally
- Section number: `font-size: clamp(4rem, 10vw, 8rem); opacity: 0.1; position: absolute; top: clamp(1rem, 3vw, 3rem); left: clamp(1rem, 3vw, 3rem)`
- Label: `font-size: clamp(2rem, 6vw, 5rem); letter-spacing: -0.03em`
- Decorative element: thin horizontal rule (2px, 40-60px wide, accent color) above the label

**Key rule:** No body copy on this layout. Label + optional section number only.

---

## 3. text-full

**Use for:** Text-heavy content -- explanations, bullet lists, value propositions, team bios.
**Do not use for:** Any slide where a visual would communicate better.

**Content limits:**
- Heading: 5 words max
- Content: 4-6 bullets OR 2 paragraphs (never both)
- 6 bullets → auto-wrap to 2×3 grid

**HTML structure (bullets):**
```html
<section class="slide slide--text-full">
  <div class="slide-content">
    <h2>Slide Heading</h2>
    <ul class="slide-bullets">
      <li>Bullet point one</li>
      <li>Bullet point two</li>
      <li>Bullet point three</li>
    </ul>
  </div>
</section>
```

**CSS approach:**
- `.slide-bullets`: `list-style: none; padding: 0; display: flex; flex-direction: column; gap: clamp(0.5rem, 1.5vw, 1.5rem)`
- Bullets styled via `::before`: dash or geometric accent mark, NOT browser defaults
- 6 bullet variant: `display: grid; grid-template-columns: 1fr 1fr; column-gap: clamp(1.5rem, 3vw, 3rem)`
- Heading: `font-size: clamp(1.75rem, 4vw, 3.5rem); margin-bottom: clamp(1rem, 2.5vw, 2.5rem)`
- Body text: `font-size: clamp(0.875rem, 1.5vw, 1.125rem); line-height: 1.55`

---

## 4. text-left-image-right

**Use for:** Pairing explanatory text with a supporting visual. Solution slides, feature explanations.
**Do not use for:** When the image is the story (use image-full instead).

**Content limits:**
- Heading: 5 words max
- Bullets: 3-4 (not more -- image column needs space)
- Image: `[IMAGE: description]` placeholder or CSS-generated visual

**HTML structure:**
```html
<section class="slide slide--text-left-image-right">
  <div class="slide-content">
    <div class="text-col">
      <h2>Heading</h2>
      <ul class="slide-bullets">
        <li>Point one</li>
        <li>Point two</li>
        <li>Point three</li>
      </ul>
    </div>
    <div class="image-col">
      <img src="..." alt="Description" />
      <!-- or CSS-generated visual placeholder -->
    </div>
  </div>
</section>
```

**CSS approach:**
- `.slide-content`: `display: grid; grid-template-columns: 55fr 45fr; gap: clamp(1.5rem, 3vw, 4rem); align-items: center`
- Image: `max-height: min(50vh, 400px); width: 100%; object-fit: cover; border-radius: 8px` (border-radius varies by style)
- Responsive: `@media (max-width: 600px) { grid-template-columns: 1fr; }` -- image stacks below text
- CSS-generated visual placeholder: styled `<div>` with gradient background, represents the missing image

---

## 5. image-left-text-right

**Use for:** When the image should lead visually -- product-first slides, social proof with screenshot.
**Content limits / CSS:** Same as text-left-image-right, columns reversed: `grid-template-columns: 45fr 55fr`.

---

## 6. two-column-text

**Use for:** Comparisons, pros/cons, before/after, two parallel processes.
**Do not use for:** Content that isn't genuinely parallel.

**Content limits:**
- 2 column headings (3 words max each)
- Max 3 bullets per column (6 total)

**HTML structure:**
```html
<section class="slide slide--two-column-text">
  <div class="slide-content">
    <h2 class="slide-headline">Main Slide Heading</h2>
    <div class="two-col-grid">
      <div class="col">
        <h3>Column A</h3>
        <ul class="slide-bullets"><li>Point</li></ul>
      </div>
      <div class="col">
        <h3>Column B</h3>
        <ul class="slide-bullets"><li>Point</li></ul>
      </div>
    </div>
  </div>
</section>
```

**CSS approach:**
- `.two-col-grid`: `display: grid; grid-template-columns: 1fr 1fr; gap: clamp(1.5rem, 3vw, 4rem)`
- Column heading `h3`: `font-size: clamp(1.1rem, 2vw, 1.75rem); border-bottom: 2px solid [accent]; padding-bottom: 0.5em; margin-bottom: 0.75em`
- Optional: subtle divider line between columns (`border-right: 1px solid rgba(color, 0.2)` on left column)

---

## 7. image-full

**Use for:** Full-bleed product screenshots, impact moments, visual stories.
**Do not use for:** Images that need more than a short caption to make sense.

**Content limits:**
- Image fills the entire slide
- Optional caption: 10 words max, in overlay zone

**HTML structure:**
```html
<section class="slide slide--image-full">
  <img src="..." alt="Description" class="full-bleed-img" />
  <div class="caption-overlay">Optional short caption here</div>
</section>
```

**CSS approach:**
- `.full-bleed-img`: `position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover`
- `.caption-overlay`: `position: absolute; bottom: 0; left: 0; right: 0; padding: clamp(1rem, 2vw, 2rem); background: linear-gradient(transparent, rgba(0,0,0,0.75)); color: #FFFFFF`
- Caption: `font-size: clamp(0.75rem, 1.2vw, 1rem)`, white text, MUST pass 4.5:1 contrast ratio
- `.slide--image-full`: `position: relative; overflow: hidden`

**CSS-generated alternative (no image):** Full-bleed CSS gradient mesh from `animation-patterns.md` + centered text label describing what the image would show.

---

## 8. image-grid

**Use for:** Product gallery, feature showcase, team photos, screenshot collection.
**Do not use for:** More than 6 images (too dense, content bleeds).

**Content limits:**
- 2×2 grid (4 images) or 3×2 grid (6 images)
- Optional caption below each image (6 words max)

**HTML structure:**
```html
<section class="slide slide--image-grid">
  <div class="slide-content">
    <h2>Grid Heading</h2>
    <div class="image-grid-container">
      <figure><img src="..." alt="..." /><figcaption>Caption</figcaption></figure>
      <figure><img src="..." alt="..." /><figcaption>Caption</figcaption></figure>
      <!-- repeat -->
    </div>
  </div>
</section>
```

**CSS approach:**
- `.image-grid-container`: `display: grid; grid-template-columns: repeat(auto-fit, minmax(min(200px, 100%), 1fr)); gap: clamp(0.5rem, 1.5vw, 1.5rem)`
- Images: `width: 100%; height: clamp(100px, 20vh, 200px); object-fit: cover; border-radius: 6px`
- `figcaption`: `font-size: clamp(0.65rem, 1vw, 0.8rem); text-align: center; margin-top: 0.4em; opacity: 0.7`

---

## 9. stat-highlight

**Use for:** The unmissable slide. Traction, ROI metrics, market size, key results.
**Do not use for:** Any slide where a number isn't the main story.

**Content limits:**
- 2-4 metrics (number + label pairs)
- ZERO body copy competing with the numbers
- ONE context line below all metrics is permitted (max 12 words)

**HTML structure:**
```html
<section class="slide slide--stat-highlight">
  <div class="slide-content">
    <div class="stats-container">
      <div class="stat">
        <span class="stat-number">3×</span>
        <span class="stat-label">Faster Close</span>
      </div>
      <div class="stat">
        <span class="stat-number">140%</span>
        <span class="stat-label">YoY Growth</span>
      </div>
      <div class="stat">
        <span class="stat-number">$2M</span>
        <span class="stat-label">ARR</span>
      </div>
    </div>
    <p class="stat-context">As of Q4 2025 — DataPulse customer average</p>
  </div>
</section>
```

**CSS approach:**
- `.stats-container`: `display: flex; justify-content: center; gap: clamp(2rem, 5vw, 6rem); align-items: center`
- `.stat`: `display: flex; flex-direction: column; align-items: center; text-align: center`
- `.stat-number`: `font-size: clamp(3.5rem, 12vw, 9rem); font-weight: 700 or 900; line-height: 1; color: accent`
- `.stat-label`: `font-size: clamp(0.7rem, 1.2vw, 1rem); letter-spacing: 0.12em; text-transform: uppercase; margin-top: 0.4em; opacity: 0.7`
- `.stat-context`: `font-size: clamp(0.65rem, 1vw, 0.875rem); opacity: 0.5; margin-top: clamp(1.5rem, 3vw, 3rem); text-align: center`
- For 2 metrics: larger gap, even bigger numbers
- For 4 metrics: tighter gap, slightly reduced number size: `clamp(2.5rem, 8vw, 6rem)`

**This is the unmissable slide for most decks.** Numbers fill a significant portion of the slide. Everything else is quiet in comparison.

---

## 10. quote-callout

**Use for:** Customer quotes, compelling statistics stated as prose, key principles.
**Do not use for:** Quotes that need more than 30 words to land.

**Content limits:**
- Quote: 30 words max
- Attribution: name + title (both required)

**HTML structure:**
```html
<section class="slide slide--quote-callout">
  <div class="slide-content">
    <div class="quote-mark" aria-hidden="true">"</div>
    <blockquote>
      <p class="quote-text">The quote goes here. It should be punchy and short.</p>
      <footer class="quote-attribution">
        <span class="attribution-name">Jane Smith</span>
        <span class="attribution-title">VP Sales, Acme Corp</span>
      </footer>
    </blockquote>
  </div>
</section>
```

**CSS approach:**
- `.quote-mark`: `font-size: clamp(4rem, 10vw, 8rem); opacity: 0.15; position: absolute; top: clamp(1rem, 3vw, 3rem); left: clamp(1rem, 3vw, 3rem); line-height: 1; font-family: [display-font]; color: currentColor`
- `.quote-text`: `font-size: clamp(1.25rem, 3vw, 2.25rem); font-style: italic; font-family: [display-font]; line-height: 1.35; max-width: 70%`
- `.attribution-name`: `font-size: clamp(0.75rem, 1.2vw, 1rem); font-weight: 600; display: block; margin-top: 1.5em`
- `.attribution-title`: `font-size: clamp(0.65rem, 1vw, 0.875rem); opacity: 0.6; display: block`
- `.slide-content`: `position: relative; display: flex; flex-direction: column; justify-content: center`

**No competing elements.** No bullet points, no secondary content, no badges. The quote + attribution is the entire slide.

---

## 11. comparison-table

**Use for:** Side-by-side feature comparison, competitive positioning, option evaluation.
**Do not use for:** More than 3 options or more than 6 comparison points.

**Content limits:**
- Max 3 columns (yours + 2 alternatives, or 3 options)
- Max 6 rows
- Cell content: 1-3 words, or Unicode checkmarks `✓` `✗`

**HTML structure:**
```html
<section class="slide slide--comparison-table">
  <div class="slide-content">
    <h2>How We Compare</h2>
    <table class="comparison">
      <thead>
        <tr>
          <th>Feature</th>
          <th class="highlight-col">Our Product</th>
          <th>Alternative A</th>
          <th>Alternative B</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Real-time sync</td>
          <td class="highlight-col">✓</td>
          <td>✗</td>
          <td>✓</td>
        </tr>
        <!-- more rows -->
      </tbody>
    </table>
  </div>
</section>
```

**CSS approach:**
- `table.comparison`: `width: 100%; border-collapse: collapse`
- `th, td`: `padding: clamp(0.5rem, 1vw, 1rem) clamp(0.75rem, 1.5vw, 1.5rem); text-align: center; border-bottom: 1px solid rgba(color, 0.15)`
- `th`: `font-size: clamp(0.75rem, 1.2vw, 1rem); font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase`
- `td`: `font-size: clamp(0.8rem, 1.3vw, 1rem)`
- `.highlight-col` (your product column): `background: rgba(accent-color, 0.08); color: accent-color; font-weight: 600`
- First and last cells in highlight column: `border-radius: 8px 8px 0 0` and `0 0 8px 8px`
- Row alternation: `tr:nth-child(even) td { background: rgba(color, 0.03) }`
- First column (row labels): `text-align: left; font-weight: 500`

---

## 12. timeline

**Use for:** Product roadmaps, company milestones, process steps, historical progression.
**Do not use for:** More than 6 milestones (too dense to read on a slide).

**Content limits:**
- 3-6 milestones
- Each: label (date or phase) + short description (1 line, 8 words max)
- Horizontal layout for ≤4 milestones; vertical layout for 5-6

**HTML structure (horizontal):**
```html
<section class="slide slide--timeline">
  <div class="slide-content">
    <h2>Roadmap</h2>
    <div class="timeline-container timeline--horizontal">
      <div class="timeline-track"></div>
      <div class="milestone">
        <div class="milestone-dot"></div>
        <span class="milestone-label">Q1 2025</span>
        <p class="milestone-desc">Launched v1.0</p>
      </div>
      <!-- more milestones -->
    </div>
  </div>
</section>
```

**CSS approach (horizontal):**
- `.timeline-container`: `position: relative; display: flex; justify-content: space-between; align-items: flex-start; padding-top: 2rem`
- `.timeline-track`: `position: absolute; top: 0.75rem; left: 0; right: 0; height: 2px; background: rgba(accent, 0.3)`
- `.milestone`: `display: flex; flex-direction: column; align-items: center; text-align: center; flex: 1; position: relative`
- `.milestone-dot`: `width: clamp(10px, 1.5vw, 16px); height: clamp(10px, 1.5vw, 16px); border-radius: 50%; background: accent; margin-bottom: 0.75rem`
- `.milestone-label`: `font-size: clamp(0.65rem, 1vw, 0.875rem); font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: accent`
- `.milestone-desc`: `font-size: clamp(0.65rem, 1vw, 0.8rem); opacity: 0.7; margin-top: 0.3em; max-width: 10ch`

**Vertical variant (5-6 milestones):** Left-aligned dot line, milestone text alternates left/right of the track.

---

## 13. closing-cta

**Use for:** The final slide of every deck. No exceptions.
**Do not use for:** Any slide that isn't the last one.

**Content limits:**
- Headline: 5 words max
- CTA action text: 3-5 words (the button or the action)
- Contact: email + URL (both required)
- QR code: `[QR: url]` placeholder -- note in Step 8 checklist to replace

**HTML structure:**
```html
<section class="slide slide--closing-cta">
  <div class="slide-content">
    <h2>Let's Build Together</h2>
    <p class="cta-action">Schedule a 30-minute call</p>
    <div class="contact-info">
      <span>hello@yourcompany.com</span>
      <span>yourcompany.com</span>
    </div>
    <div class="qr-placeholder">[QR: https://cal.com/yourlink]</div>
  </div>
</section>
```

**CSS approach:**
- Background: full accent color OR strongly contrasting bg from style preset -- this slide should stand out
- `.slide-content`: `display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: clamp(1rem, 2.5vw, 2.5rem)`
- Headline: `font-size: clamp(2rem, 5vw, 4.5rem); letter-spacing: -0.03em`
- CTA action: `font-size: clamp(1rem, 2vw, 1.75rem); opacity: 0.8; border-bottom: 2px solid currentColor; padding-bottom: 0.2em`
- Contact info: `display: flex; gap: 2rem; font-size: clamp(0.75rem, 1.2vw, 1rem); opacity: 0.65`
- QR placeholder: styled `<div>` with dashed border, 80-100px square, "QR" label inside -- replace with actual QR image before presenting
- **No bullets, no body copy, no competing elements.** CTA + contact only.
