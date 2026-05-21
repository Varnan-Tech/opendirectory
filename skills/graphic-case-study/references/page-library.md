# Page Library — graphic-case-study

7 page section types for A4 portrait case studies. Each section is a content block placed within a `<section class="slide">`. Multiple sections can stack vertically within a single page.

All dimensions assume: viewport 1200px wide × 1697px tall (A4 portrait).

---

## 1. cover

**Purpose:** Opening page -- customer name, headline result, logos
**Density:** Very open
**Content limits:** Headline 12 words max (leads with number), customer name, optional category label, logo placeholders

**HTML structure:**
```html
<section class="slide page--cover">
  <div class="page-inner">
    <div class="cover-top">
      <span class="cover-label reveal">Customer Success Story</span>
    </div>
    <div class="cover-body">
      <h1 class="cover-headline reveal">[Headline result — leads with number]</h1>
      <p class="cover-company reveal">[Customer name]</p>
    </div>
    <div class="cover-bottom">
      <div class="logo-group reveal">
        <div class="logo-box logo-customer">[CSS initials or img]</div>
        <span class="logo-sep">×</span>
        <div class="logo-box logo-vendor">[CSS initials or img]</div>
      </div>
    </div>
  </div>
</section>
```

**CSS approach:**
- `.page-inner`: `display: flex; flex-direction: column; justify-content: space-between; height: 100%; padding: var(--page-padding);`
- `.cover-headline`: `font-family: var(--font-display); font-size: clamp(2rem, 5vw, 3.5rem); letter-spacing: -0.03em; line-height: 1.1; max-width: 20ch;`
- `.cover-label`: uppercase, caption size, accent color or muted
- `.logo-box`: `width: clamp(48px, 6vw, 80px); height: clamp(48px, 6vw, 80px); display: flex; align-items: center; justify-content: center;` -- use CSS-generated initials when no logo URL provided

**Background:** Style preset's primary (often the most distinctive background of the preset -- dark, full-color, or richly styled). This is the first impression.

**Do NOT:** Put challenge/solution text here. Cover = one idea only.

---

## 2. overview

**Purpose:** At-a-glance customer profile
**Density:** Moderate
**Content limits:** 4 fact cells max (label + value each). No paragraph text.

**HTML structure:**
```html
<div class="section--overview reveal">
  <h2 class="section-label">At a Glance</h2>
  <div class="overview-grid">
    <div class="fact-cell">
      <span class="fact-label">Industry</span>
      <span class="fact-value">B2B SaaS</span>
    </div>
    <div class="fact-cell">
      <span class="fact-label">Company size</span>
      <span class="fact-value">200-500 employees</span>
    </div>
    <div class="fact-cell">
      <span class="fact-label">Location</span>
      <span class="fact-value">San Francisco, CA</span>
    </div>
    <div class="fact-cell">
      <span class="fact-label">Use case</span>
      <span class="fact-value">Revenue operations</span>
    </div>
  </div>
</div>
```

**CSS approach:**
- `.overview-grid`: `display: grid; grid-template-columns: repeat(2, 1fr); gap: clamp(0.75rem, 2%, 1.5rem);`
- `.fact-cell`: preset card background + border, `border-radius: var(--card-radius); padding: clamp(0.75rem, 1.5%, 1.25rem);`
- `.fact-label`: caption size, muted color, uppercase, 0.1em tracking
- `.fact-value`: body size, primary text color, font-weight: 600

---

## 3. challenge

**Purpose:** The customer's problem before your product
**Density:** Moderate
**Content limits:** Context paragraph (2-3 sentences) + 3 pain points (1 sentence each)

**HTML structure:**
```html
<div class="section--challenge">
  <h2 class="section-heading reveal">The Challenge</h2>
  <div class="challenge-body">
    <p class="challenge-context reveal">[Context paragraph]</p>
    <ul class="pain-list">
      <li class="pain-item reveal">[Pain point 1]</li>
      <li class="pain-item reveal">[Pain point 2]</li>
      <li class="pain-item reveal">[Pain point 3]</li>
    </ul>
  </div>
</div>
```

**CSS approach:**
- Two-column layout at full page: `display: grid; grid-template-columns: 1fr 1fr; gap: clamp(1.5rem, 4%, 3rem);` OR single-column if stacking with other sections
- `.pain-list`: no browser bullets -- use `list-style: none; display: flex; flex-direction: column; gap: clamp(0.5rem, 1%, 1rem);`
- `.pain-item::before`: `content: "—"; color: var(--accent); margin-right: 0.75em;`
- `.section-heading`: `clamp(1.25rem, 2.5vw, 2rem)` weight 700

**Signature element for warm-earth style:** Drop cap on opening paragraph:
```css
.challenge-context::first-letter {
  font-family: var(--font-display);
  font-size: clamp(3rem, 7vw, 5rem);
  float: left;
  margin: 0.05em 0.12em 0 0;
  color: var(--accent);
  line-height: 0.8;
}
```

---

## 4. solution

**Purpose:** How your product addressed the challenge
**Density:** Moderate
**Content limits:** 2-3 feature callouts (name 3 words max + 1-sentence description each)

**HTML structure:**
```html
<div class="section--solution">
  <h2 class="section-heading reveal">The Solution</h2>
  <div class="feature-grid">
    <div class="feature-card reveal">
      <div class="feature-icon">[CSS shape]</div>
      <div class="feature-name">Feature Name</div>
      <p class="feature-desc">One sentence describing the outcome this feature delivers.</p>
    </div>
    <!-- repeat for 2-3 features -->
  </div>
</div>
```

**CSS approach:**
- `.feature-grid`: `display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: clamp(0.75rem, 2%, 1.5rem);`
- `.feature-card`: preset card background + border + border-radius, `padding: clamp(1rem, 2%, 1.75rem);`
- `.feature-icon`: CSS-generated shape (circle, square, hexagon outline) using `::before` or inline shape elements, 32–48px, accent color or accent-light fill
- `.feature-name`: `font-size: clamp(0.875rem, 1.25vw, 1rem); font-weight: 700; margin-bottom: 0.5em;`
- `.feature-desc`: body size, secondary color

**CSS icon patterns (no images needed):**
```css
/* Circle icon */
.feature-icon {
  width: clamp(32px, 3vw, 48px);
  height: clamp(32px, 3vw, 48px);
  border-radius: 50%;
  background: rgba(var(--accent-rgb), 0.12);
  border: 2px solid var(--accent);
  margin-bottom: 1rem;
}
/* Or: filled square with rounded corner */
.feature-icon {
  width: clamp(32px, 3vw, 48px);
  height: clamp(32px, 3vw, 48px);
  background: var(--accent);
  border-radius: 6px;
  margin-bottom: 1rem;
}
```

---

## 5. results

**Purpose:** Measurable impact -- the most important section
**Density:** Open (numbers need space)
**Content limits:** 3 metrics (number + label + 1-line context each). Optional 2-sentence narrative.

**HTML structure:**
```html
<div class="section--results">
  <h2 class="section-heading reveal">The Results</h2>
  <div class="stat-row">
    <div class="stat-item stat-item--hero reveal" style="--i:0">
      <div class="stat-number" data-count="80" data-suffix="%">0%</div>
      <div class="stat-label">Time saved on reporting</div>
      <div class="stat-context">Down from 20 hours per week</div>
    </div>
    <div class="stat-item reveal" style="--i:1">
      <div class="stat-number" data-count="95" data-suffix="%">0%</div>
      <div class="stat-label">Reduction in errors</div>
      <div class="stat-context">Across all report types</div>
    </div>
    <div class="stat-item reveal" style="--i:2">
      <div class="stat-number" data-prefix="$" data-count="200" data-suffix="K">$0K</div>
      <div class="stat-label">Annual cost savings</div>
      <div class="stat-context">Labor and tooling combined</div>
    </div>
  </div>
  <!-- optional -->
  <p class="results-narrative reveal">[2-sentence narrative]</p>
</div>
```

**CSS approach:**
- `.stat-row`: `display: flex; gap: clamp(1.5rem, 4%, 3rem); align-items: flex-start;` (horizontal, 3 stats)
- `.stat-item`: `flex: 1; display: flex; flex-direction: column; gap: 0.5rem;`
- `.stat-number`: `font-family: var(--font-display); font-size: clamp(2.5rem, 7vw, 5rem); font-weight: 400; letter-spacing: -0.04em; line-height: 0.9; color: var(--text-secondary);`
- `.stat-item--hero .stat-number`: same but `color: var(--accent);` and `font-size: clamp(3rem, 8vw, 5.5rem);`
- `.stat-label`: `font-size: clamp(0.7rem, 1vw, 0.875rem); font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-secondary);`
- `.stat-context`: `font-size: clamp(0.65rem, 0.9vw, 0.8rem); color: var(--text-muted);`

**Stagger animation:**
```css
.stat-item {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
  transition-delay: calc(var(--i) * 0.15s);
}
.slide.visible .stat-item { opacity: 1; transform: none; }
```

**ZERO body copy competing with the numbers.** The optional narrative goes BELOW the stat row in smaller body text, clearly subordinate.

---

## 6. testimonial

**Purpose:** Customer voice -- builds trust
**Density:** Very open
**Content limits:** Quote 40 words max + name + title + company

**HTML structure:**
```html
<div class="section--testimonial">
  <blockquote class="testimonial-quote reveal">
    <div class="quote-mark">"</div>
    <p class="quote-text">[Customer quote, 40 words max]</p>
    <footer class="quote-attribution">
      <span class="attribution-name">[Name]</span>
      <span class="attribution-role">[Title], [Company]</span>
    </footer>
  </blockquote>
</div>
```

**CSS approach:**
- `.section--testimonial`: `display: flex; align-items: center; justify-content: center; padding: clamp(2rem, 5%, 4rem);`
- `.quote-mark`: `position: absolute; font-family: var(--font-display); font-size: clamp(4rem, 12vw, 8rem); opacity: 0.08; top: -0.2em; left: -0.1em; color: var(--accent); line-height: 1; pointer-events: none; user-select: none;`
- `.quote-text`: `font-family: var(--font-display); font-style: italic; font-size: clamp(1.1rem, 2vw, 1.5rem); line-height: 1.5; color: var(--text-primary);`
- `.attribution-name`: `font-weight: 700; font-size: var(--label-size);`
- `.attribution-role`: `color: var(--text-muted); font-size: var(--label-size);`
- Testimonial section background: subtle accent tint (accent at 4-6% opacity) or preset's alt section bg

**Do NOT:** Add bullet points, headings, or any other content inside a testimonial section.

---

## 7. closing-cta

**Purpose:** Clear next step -- drives action
**Density:** Open
**Content limits:** Headline 5 words max + CTA action text 3 words + email + URL (both required)

**HTML structure:**
```html
<div class="section--cta">
  <div class="cta-inner reveal">
    <div class="cta-logo">[Vendor logo or CSS initials]</div>
    <h2 class="cta-headline">[Headline -- 5 words max]</h2>
    <p class="cta-sub">[Optional 1-sentence context]</p>
    <div class="cta-contacts">
      <a href="mailto:[email]" class="cta-email">[email]</a>
      <a href="[url]" class="cta-url">[url]</a>
    </div>
  </div>
</div>
```

**CSS approach:**
- `.section--cta`: preset's darkest or most distinctive background -- this is the closing statement
- `.cta-headline`: `font-family: var(--font-display); font-size: clamp(1.5rem, 4vw, 3rem); font-weight: var(--display-weight); color: var(--cta-text); letter-spacing: -0.02em;`
- `.cta-email`: `font-size: clamp(0.9rem, 1.5vw, 1.25rem); font-weight: 600;`
- `.cta-url`: `font-size: clamp(0.8rem, 1.2vw, 1rem); opacity: 0.7;`
- No bullet lists, no feature lists, no repetition of stats.

**One action only.** Email + URL -- both mandatory (fails QA if either missing).

---

## Standard Page Assemblies

### 1-pager (1 page)
```
<section class="slide page--cover-compact">
  [cover section -- condensed version]
  [challenge-inline -- 2 bullet lines max]
  [solution-inline -- 1 sentence + 3 micro stats]
  [results-inline -- 3 stats in smaller size]
  [cta-inline -- email + url at bottom]
</section>
```
1-pager is a summary card. Every section is abbreviated. Nothing is full-depth.

### 2-pager (2 pages)
```
Page 1: <section class="slide">
  [cover]
  [challenge-solution stacked]
</section>

Page 2: <section class="slide">
  [results]
  [testimonial -- if available]
  [closing-cta]
</section>
```

### 4-pager (4 pages)
```
Page 1: <section class="slide">[cover]</section>
Page 2: <section class="slide">[overview] + [challenge]</section>
Page 3: <section class="slide">[solution] + [results]</section>
Page 4: <section class="slide">[testimonial] + [closing-cta]</section>
```
