# Page Library — graphic-ebook

11 page layout types for A4 portrait ebooks (1200×1697px). Each layout is a content block inside `<section class="slide">`. Multiple sections can stack within a single page (e.g., chapter-intro + short text-column).

All dimensions assume: viewport 1200px wide × 1697px tall (A4 portrait).

---

## 1. cover

**Purpose:** Opening page — title, subtitle, brand
**Density:** Very open
**Content limits:** Title ≤10 words (leads with value or tension), subtitle ≤15 words, brand name, optional category label

**HTML structure:**
```html
<section class="slide page--cover">
  <div class="cover-inner">
    <div class="cover-top reveal">
      <span class="cover-category-label">Lead Magnet</span>
    </div>
    <div class="cover-body">
      <h1 class="cover-title reveal">[Title — leads with value or tension]</h1>
      <p class="cover-subtitle reveal">[Subtitle — 15 words max]</p>
    </div>
    <div class="cover-bottom reveal">
      <div class="brand-logo">[CSS initials or img]</div>
      <span class="brand-name">[Brand Name]</span>
    </div>
  </div>
  <!-- No footer on cover page -->
</section>
```

**CSS approach:**
- Background: style preset's most distinctive (dark, full-color, or richly styled — this is the first impression)
- Decorative element: ghost letter or abstract geometric in `::before` pseudo-element, `opacity: 0.05`
- `.cover-title`: `font-family: var(--font-display); font-size: clamp(2rem, 5vw, 3.5rem); letter-spacing: -0.03em; line-height: 1.08;`
- `.cover-subtitle`: `font-size: clamp(0.875rem, 1.5vw, 1.2rem); line-height: 1.55; max-width: 36ch;`
- `.cover-inner`: `display: flex; flex-direction: column; justify-content: space-between; height: 100%; padding: var(--page-padding);`

**Do NOT:** Put any body copy, bullets, or chapter content here. Cover = one idea only.

---

## 2. toc

**Purpose:** Table of contents — numbered chapter list
**Density:** Open, scannable
**Content limits:** Max 8 entries. Chapter title ≤6 words. Right-aligned page/section numbers.

**HTML structure:**
```html
<section class="slide page--toc">
  <div class="toc-inner">
    <h2 class="toc-heading reveal">Contents</h2>
    <ol class="toc-list">
      <li class="toc-item reveal">
        <span class="toc-num">01</span>
        <span class="toc-title">[Chapter Title]</span>
        <span class="toc-page">[N]</span>
      </li>
      <!-- repeat for each chapter -->
    </ol>
  </div>
  <div class="page-footer"><span>[Brand]</span><span>2</span></div>
</section>
```

**CSS approach:**
- `.toc-list`: `list-style: none; display: flex; flex-direction: column; gap: clamp(0.5rem, 1.2%, 1rem);`
- `.toc-item`: `display: flex; align-items: baseline; gap: clamp(0.75rem, 1.5%, 1.25rem); padding-bottom: clamp(0.5rem, 1%, 0.875rem); border-bottom: 1px solid var(--divider);`
- `.toc-num`: `font-family: var(--font-display); font-size: clamp(1.1rem, 2vw, 1.6rem); color: var(--accent); min-width: 2.5ch; font-weight: var(--display-weight);`
- `.toc-title`: `font-size: clamp(0.875rem, 1.4vw, 1.1rem); font-weight: 600; flex: 1;`
- `.toc-page`: `font-size: clamp(0.75rem, 1.1vw, 0.875rem); color: var(--text-muted); font-weight: 600;`
- `.toc-heading`: `font-family: var(--font-display); font-size: clamp(1.5rem, 3.5vw, 2.8rem); letter-spacing: -0.02em; margin-bottom: clamp(1.5rem, 3%, 2.5rem);`

---

## 3. chapter-intro

**Purpose:** Section opener — signals the start of a new chapter
**Density:** Very open
**Content limits:** Chapter number (decorative) + chapter title ≤8 words + teaser paragraph 2–3 sentences

**HTML structure:**
```html
<section class="slide page--chapter-intro">
  <div class="chapter-intro-inner">
    <span class="chapter-number-deco" aria-hidden="true">01</span>
    <div class="chapter-intro-content">
      <p class="chapter-label reveal">Chapter One</p>
      <h2 class="chapter-title reveal">[Chapter Title — ≤8 words]</h2>
      <p class="chapter-teaser reveal">[2–3 sentence teaser. Sets expectation for the chapter.]</p>
    </div>
  </div>
  <div class="page-footer"><span>[Brand]</span><span>[N]</span></div>
</section>
```

**CSS approach:**
- `.chapter-number-deco`: `font-family: var(--font-display); font-size: clamp(6rem, 18vw, 14rem); font-weight: var(--display-weight); opacity: 0.06; position: absolute; top: -0.1em; right: var(--page-padding); line-height: 1; color: var(--accent); pointer-events: none; user-select: none;`
- `.chapter-intro-inner`: `position: relative; display: flex; flex-direction: column; justify-content: center; height: 100%; padding: var(--page-padding); padding-bottom: 3rem;` (leave room for footer)
- `.chapter-title`: `font-family: var(--font-display); font-size: clamp(1.5rem, 3.5vw, 2.8rem); letter-spacing: -0.02em; line-height: 1.15; font-weight: var(--display-weight); max-width: 20ch;`
- `.chapter-teaser`: `font-size: clamp(0.875rem, 1.25vw, 1.05rem); color: var(--text-secondary); line-height: 1.65; max-width: 55ch; margin-top: clamp(0.875rem, 1.5%, 1.5rem);`
- `.chapter-label`: `font-size: clamp(0.6rem, 0.85vw, 0.7rem); font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.75rem;`

**Background:** Style preset's alt section background OR full-bleed brand color. This page must be visually distinct from body pages.

---

## 4. text-column

**Purpose:** Primary reading content — body paragraphs
**Density:** Moderate
**Variants:** 1-column (default) / 2-column

### 1-Column:
**Content limits:** Section heading + body paragraphs. Max 250 words per page.

**HTML structure:**
```html
<section class="slide page--text-column">
  <div class="text-col-inner">
    <h3 class="section-heading reveal">[Section Heading]</h3>
    <div class="body-content">
      <p class="body-text reveal">[Body paragraph. Max 250 words total on page.]</p>
      <!-- OR a bullet list: -->
      <ul class="body-list reveal">
        <li class="body-list-item">[List item — max 3 items before text looks like a bullet dump]</li>
      </ul>
    </div>
  </div>
  <div class="page-footer"><span>[Brand]</span><span>[N]</span></div>
</section>
```

**CSS (1-col):**
- `.text-col-inner`: `padding: var(--page-padding); padding-bottom: 3rem; height: 100%; display: flex; flex-direction: column; gap: var(--content-gap); overflow: hidden;`
- `.body-text`: `font-size: clamp(0.875rem, 1.25vw, 1.05rem); line-height: 1.75; color: var(--text-secondary); max-width: min(65ch, 100%);`
- `.section-heading`: `font-family: var(--font-display); font-size: clamp(1rem, 1.8vw, 1.4rem); font-weight: 700; letter-spacing: -0.01em; color: var(--text-primary); line-height: 1.2;`
- `.body-list`: `list-style: none; display: flex; flex-direction: column; gap: clamp(0.5rem, 1%, 0.875rem); max-width: min(65ch, 100%);`
- `.body-list-item`: `display: flex; gap: 0.75em; font-size: clamp(0.875rem, 1.25vw, 1.05rem); line-height: 1.7; color: var(--text-secondary);`
- `.body-list-item::before`: `content: "→"; color: var(--accent); flex-shrink: 0; line-height: 1.7;`

### 2-Column:
**Content limits:** 140–190 words per column. Use for comparisons, step pairs, before/after.

**CSS additions:**
```css
.text-col-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: clamp(2rem, 4%, 3.5rem);
  align-items: start;
}
.text-col-2 .col-left {
  border-right: 1px solid var(--divider);
  padding-right: clamp(1.5rem, 3%, 2.5rem);
}
.col-heading {
  font-size: clamp(0.875rem, 1.3vw, 1.1rem);
  font-weight: 700;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--accent);
  margin-bottom: 0.875rem;
  color: var(--text-primary);
}
```

---

## 5. text-sidebar

**Purpose:** Reading content with a typed callout in the sidebar
**Density:** Moderate
**Layout:** 2/3 main content + 1/3 callout sidebar

**HTML structure:**
```html
<section class="slide page--text-sidebar">
  <div class="text-sidebar-inner">
    <div class="sidebar-main">
      <h3 class="section-heading reveal">[Section Heading]</h3>
      <p class="body-text reveal">[Body — max 180 words]</p>
    </div>
    <aside class="sidebar-callout reveal">
      <div class="callout callout--tip">
        <p class="callout-label">Pro Tip</p>
        <p class="callout-body">[Sidebar content — max 70 words. One of: tip, warning, stat, quote, checklist.]</p>
      </div>
    </aside>
  </div>
  <div class="page-footer"><span>[Brand]</span><span>[N]</span></div>
</section>
```

**CSS approach:**
- `.text-sidebar-inner`: `display: grid; grid-template-columns: 2fr 1fr; gap: clamp(1.5rem, 3%, 2.5rem); padding: var(--page-padding); padding-bottom: 3rem; height: 100%; align-items: start; overflow: hidden;`
- `.sidebar-main .body-text`: same as text-column 1-col
- `.callout`: `border-left: 3px solid; border-radius: var(--card-radius, 4px); padding: clamp(0.75rem, 1.5%, 1.1rem);`
- `.callout-label`: `font-size: clamp(0.58rem, 0.8vw, 0.68rem); font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 0.5em; display: block;`
- `.callout-body`: `font-size: clamp(0.8rem, 1.1vw, 0.95rem); line-height: 1.6; color: var(--text-secondary);`

**Callout type tokens:**
```css
.callout--tip      { background: rgba(22, 163, 74, 0.07);  border-color: #16A34A; }
.callout--tip      .callout-label { color: #16A34A; }
.callout--warning  { background: rgba(217, 119, 6, 0.07);  border-color: #D97706; }
.callout--warning  .callout-label { color: #D97706; }
.callout--stat     { background: rgba(var(--accent-rgb, 100,100,100), 0.07); border-color: var(--accent); }
.callout--stat     .callout-label { color: var(--accent); }
.callout--quote    { background: var(--bg-elevated, #1A1A1A); border-color: var(--divider); }
.callout--quote    .callout-body { font-style: italic; }
.callout--quote    .callout-label { color: var(--text-muted); }
.callout--checklist { background: rgba(8, 145, 178, 0.07); border-color: #0891B2; }
.callout--checklist .callout-label { color: #0891B2; }
```

---

## 6. quote-callout

**Purpose:** Full-page pull quote — builds authority, breaks visual rhythm
**Density:** Very open
**Content limits:** Quote ≤40 words + attribution (name, title, company or source)

**HTML structure:**
```html
<section class="slide page--quote-callout">
  <div class="quote-callout-inner">
    <blockquote class="pull-quote reveal">
      <span class="quote-mark" aria-hidden="true">"</span>
      <p class="quote-text">[Quote — ≤40 words]</p>
      <footer class="quote-attribution">
        <span class="attribution-name">[Name]</span>
        <span class="attribution-role">[Title], [Company]</span>
      </footer>
    </blockquote>
  </div>
  <div class="page-footer"><span>[Brand]</span><span>[N]</span></div>
</section>
```

**CSS approach:**
- `.quote-callout-inner`: `display: flex; align-items: center; justify-content: center; height: 100%; padding: var(--page-padding); padding-bottom: 3rem;`
- `.pull-quote`: `position: relative; max-width: 32ch;`
- `.quote-mark`: `position: absolute; font-family: var(--font-display); font-size: clamp(6rem, 15vw, 10rem); opacity: 0.07; top: -0.35em; left: -0.15em; color: var(--accent); line-height: 1; pointer-events: none; user-select: none;`
- `.quote-text`: `font-family: var(--font-display); font-style: italic; font-size: clamp(1.2rem, 2.2vw, 1.75rem); line-height: 1.4; color: var(--text-primary);`
- `.attribution-name`: `font-weight: 700; font-size: clamp(0.7rem, 1vw, 0.85rem); display: block; margin-top: 1.5rem;`
- `.attribution-role`: `font-size: clamp(0.65rem, 0.9vw, 0.78rem); color: var(--text-muted); display: block;`
- Background: preset's alt section bg OR full accent-color inversion for maximum impact

**Do NOT:** Add bullets, headings, body text, or statistics to this page. The quote is the entire content.

---

## 7. stat-grid

**Purpose:** Key metrics with visual emphasis — the results section
**Density:** Open (numbers need breathing room)
**Content limits:** 3–6 metrics. One hero metric in accent color. Optional 1-sentence narrative below.

**HTML structure:**
```html
<section class="slide page--stat-grid">
  <div class="stat-grid-inner">
    <div class="stat-heading-row">
      <p class="section-label reveal">By the Numbers</p>
      <h2 class="section-heading reveal">[Heading — ≤8 words]</h2>
    </div>
    <div class="stat-row">
      <div class="stat-item stat-item--hero reveal" style="--i:0">
        <div class="stat-rule"></div>
        <div class="stat-number">[80%]</div>
        <div class="stat-label">[Label — uppercase, ≤4 words]</div>
        <div class="stat-context">[Context — ≤12 words]</div>
      </div>
      <div class="stat-item reveal" style="--i:1">
        <div class="stat-rule"></div>
        <div class="stat-number">[N]</div>
        <div class="stat-label">[Label]</div>
        <div class="stat-context">[Context]</div>
      </div>
      <!-- 3rd stat -->
    </div>
    <p class="stat-narrative reveal">[Optional: 1-sentence narrative below the stats]</p>
  </div>
  <div class="page-footer"><span>[Brand]</span><span>[N]</span></div>
</section>
```

**CSS approach:**
- `.stat-row`: `display: flex; gap: clamp(2rem, 5%, 4rem); align-items: flex-start; margin-top: clamp(1.5rem, 3%, 2.5rem);`
- `.stat-item`: `flex: 1; display: flex; flex-direction: column; gap: clamp(0.35rem, 0.7%, 0.6rem); opacity: 0; transform: translateY(20px); transition: opacity 0.7s var(--ease-out-expo, ease), transform 0.7s var(--ease-out-expo, ease);`
- `.slide.visible .stat-item`: `opacity: 1; transform: none;`
- `.slide.visible .stat-item:nth-child(1)`: `transition-delay: 0.05s;`
- `.slide.visible .stat-item:nth-child(2)`: `transition-delay: 0.2s;`
- `.slide.visible .stat-item:nth-child(3)`: `transition-delay: 0.35s;`
- `.stat-rule`: `width: 20px; height: 2px; background: var(--accent); margin-bottom: 0.5rem;`
- `.stat-number`: `font-family: var(--font-display); font-size: clamp(2.5rem, 7vw, 5rem); font-weight: var(--display-weight); letter-spacing: -0.04em; line-height: 0.9; color: var(--text-secondary);`
- `.stat-item--hero .stat-number`: `font-size: clamp(3rem, 8vw, 5.5rem); color: var(--accent);`
- `.stat-label`: `font-size: clamp(0.62rem, 0.9vw, 0.78rem); font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-secondary);`
- `.stat-context`: `font-size: clamp(0.6rem, 0.85vw, 0.72rem); color: var(--text-muted); line-height: 1.4;`
- `.stat-narrative`: `font-size: clamp(0.75rem, 1.05vw, 0.875rem); color: var(--text-muted); border-top: 1px solid var(--divider); padding-top: 0.875rem; margin-top: 0.875rem; max-width: 70ch;`

**ZERO body copy competing with the numbers.** The optional narrative goes BELOW the stat row in smaller body text, clearly subordinate.

---

## 8. key-takeaways

**Purpose:** Summary of learnings — leave-behind/reference
**Density:** Open, scannable
**Content limits:** 5–8 takeaways, ≤15 words each. Imperative where possible.
**Position:** Second-to-last page, before closing-cta.

**HTML structure:**
```html
<section class="slide page--key-takeaways">
  <div class="takeaways-inner">
    <h2 class="section-heading reveal">Key Takeaways</h2>
    <ol class="takeaway-list">
      <li class="takeaway-item reveal">
        <span class="takeaway-num">01</span>
        <span class="takeaway-text">[Takeaway — ≤15 words, imperative]</span>
      </li>
      <!-- repeat for 5–8 items -->
    </ol>
  </div>
  <div class="page-footer"><span>[Brand]</span><span>[N]</span></div>
</section>
```

**CSS approach:**
- `.takeaway-list`: `list-style: none; display: flex; flex-direction: column; gap: clamp(0.75rem, 1.5%, 1.25rem); margin-top: clamp(1.5rem, 3%, 2.5rem);`
- `.takeaway-item`: `display: flex; gap: clamp(1rem, 2%, 1.5rem); align-items: flex-start; padding-bottom: clamp(0.75rem, 1.5%, 1.25rem); border-bottom: 1px solid var(--divider);`
- `.takeaway-num`: `font-family: var(--font-display); font-size: clamp(1.2rem, 2vw, 1.6rem); color: var(--accent); min-width: 2.5ch; font-weight: var(--display-weight); line-height: 1.4; flex-shrink: 0;`
- `.takeaway-text`: `font-size: clamp(0.875rem, 1.3vw, 1.05rem); line-height: 1.6; color: var(--text-secondary); font-weight: 500;`

---

## 9. full-image

**Purpose:** Full-page visual — abstract composition, process diagram, or decorative break
**Density:** Very open
**Use:** Sparingly — maximum 1 per ebook. CSS-generated visuals only.

**HTML structure:**
```html
<section class="slide page--full-image">
  <div class="full-image-canvas">
    <!-- CSS-generated visual: shapes, gradient mesh, abstract pattern -->
    <div class="visual-element" aria-hidden="true"></div>
  </div>
  <div class="full-image-caption reveal">[Optional caption — ≤15 words]</div>
  <div class="page-footer"><span>[Brand]</span><span>[N]</span></div>
</section>
```

**CSS approach:**
- `.full-image-canvas`: `position: absolute; inset: 0; overflow: hidden;` — fill the entire slide
- `.full-image-caption`: `position: absolute; bottom: clamp(2.5rem, 5%, 3rem); left: var(--page-padding); right: var(--page-padding); font-size: clamp(0.65rem, 0.9vw, 0.78rem); color: var(--text-muted); font-style: italic;`
- CSS visual patterns: gradient mesh, radial dot grid, geometric shapes via `::before`/`::after`, abstract layered elements

---

## 10. closing-cta

**Purpose:** Final page — single conversion action
**Density:** Open
**Content limits:** Headline ≤5 words (imperative) + 1 sentence body + email + URL (both required)

**HTML structure:**
```html
<section class="slide page--closing-cta">
  <div class="cta-inner">
    <div class="cta-top">
      <p class="cta-label reveal">Ready to start</p>
      <h2 class="cta-headline reveal">[Headline — ≤5 words, imperative]</h2>
      <p class="cta-body reveal">[1-sentence body — ≤25 words]</p>
    </div>
    <div class="cta-bottom">
      <div class="cta-contacts reveal">
        <a href="mailto:[email]" class="cta-email">[email]</a>
        <a href="[url]" class="cta-url">[url]</a>
      </div>
      <div class="cta-brand-logo reveal">[CSS initials or img]</div>
    </div>
  </div>
  <!-- No footer on closing-cta — it IS the closer -->
</section>
```

**CSS approach:**
- `.page--closing-cta`: Background — style preset's darkest or most distinctive. This is the closing statement.
- `.cta-inner`: `display: flex; flex-direction: column; justify-content: space-between; height: 100%; padding: var(--page-padding);`
- `.cta-headline`: `font-family: var(--font-display); font-size: clamp(1.5rem, 4vw, 3rem); letter-spacing: -0.03em; line-height: 1.05; font-weight: var(--display-weight);`
- `.cta-email`: `font-size: clamp(0.875rem, 1.4vw, 1.2rem); font-weight: 700; display: block;`
- `.cta-url`: `font-size: clamp(0.75rem, 1.1vw, 0.9rem); opacity: 0.55; display: block;`

**ONE action only.** Email + URL — both mandatory. No bullets, no stats, no feature lists. Fails QA if either is missing.

---

## Standard Page Assemblies

### 3-pager (quick guide / lead magnet)
```
Page 1: [cover]
Page 2: [stat-grid] OR [text-column]
Page 3: [closing-cta]
```
No TOC. Cover may include "What's inside" 3-bullet list.

### 5-pager (short guide)
```
Page 1: [cover]
Page 2: [toc]
Page 3: [chapter-intro]
Page 4: [text-column] OR [text-sidebar]
Page 5: [closing-cta]
```

### 6-pager (standard)
```
Page 1: [cover]
Page 2: [toc]
Page 3: [chapter-intro] — Chapter 1
Page 4: [text-column] — Chapter 1 body
Page 5: [stat-grid] OR [quote-callout]
Page 6: [closing-cta]
```

### 8-pager (standard + depth)
```
Page 1: [cover]
Page 2: [toc]
Page 3: [chapter-intro] — Chapter 1
Page 4: [text-sidebar]
Page 5: [chapter-intro] — Chapter 2
Page 6: [text-column]
Page 7: [quote-callout] OR [stat-grid]
Page 8: [closing-cta]
```

### 10-pager (deep dive)
```
Page 1:  [cover]
Page 2:  [toc]
Page 3:  [chapter-intro] — Chapter 1
Page 4:  [text-column]
Page 5:  [chapter-intro] — Chapter 2
Page 6:  [text-sidebar]
Page 7:  [chapter-intro] — Chapter 3
Page 8:  [text-column]
Page 9:  [key-takeaways]
Page 10: [closing-cta]
```

**Visual rhythm enforcement:** In all assemblies, no 2+ consecutive text-column or text-sidebar pages. Always break with chapter-intro, quote-callout, stat-grid, or key-takeaways.
