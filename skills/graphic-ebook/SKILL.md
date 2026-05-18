---
name: graphic-ebook
description: Creates professionally designed B2B SaaS e-books in HTML + CSS, exported as print-ready PDF. 3–10 pages, 9 style presets, 11 page layout types. Trigger when user says "create an ebook", "design a lead magnet", "make a PDF guide", "build a gated content piece", "write a B2B ebook", "design a white paper", "create a nurture asset", or "make a PDF report".
compatibility: [claude-code, gemini-cli, github-copilot]
author: OpenDirectory
version: 1.0.0
---

# graphic-ebook

Creates professionally designed B2B SaaS e-books — lead magnets, gated guides, nurture assets, white papers. HTML + CSS → print-ready PDF. 3–10 pages.

## Critical Rules

Before any step, these rules are absolute:

1. Every page MUST fit within A4 canvas (1200×1697px). No content overflow.
2. All scalable font sizes use `clamp()`. Fixed px only for borders/structural elements.
3. Single self-contained HTML. All CSS inline. Font CDN `<link>` only external dependency.
4. **Never dump HTML in chat.** Save to file, show summary only.
5. Body copy is primary. Line-height ≥ 1.75 on all text-column and text-sidebar pages. Max-width ≤ 65ch for single-column body.
6. No generic AI slop: no Inter as display font, no purple-to-blue gradient on white, no "Thank You" closing.
7. Visual rhythm: never place 2+ text-column pages back-to-back. Break with chapter-intro, quote-callout, or stat-grid.
10. **Before generating HTML, commit to a design direction:** one tone, one signature element, one background system. Generic = failure. Each ebook must be distinctly designed for its audience and subject — not a template.
8. `* { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }` — mandatory global CSS. Chromium strips all background colors in PDF without this.
9. Every page except cover must have a page footer: page number + brand name. Absolute position at bottom of each `.slide`.

---

## Step 1: Brief Intake

Four required fields. If all four are present in the user's prompt: **skip to Step 2.**

If any are missing, ask **exactly**:

> "To create your ebook, I need four things:
> 1. **Topic** — what is the ebook about? (be specific: "5 ways to reduce CAC" not "marketing tips")
> 2. **Audience** — who reads it? (role, company size, pain point: "Customer Success Managers at 50–500 person SaaS companies struggling with churn")
> 3. **Desired action** — what should the reader do after? (book a demo, download a template, share with team)
> 4. **Content** — do you have existing content, or should I draft from the topic?"

Stop and wait. Do not read reference files. Do not generate any HTML or outline.

---

## Step 2: Complete Intake

Ask all 9 questions in one message, grouped. Defaults apply if skipped.

**Content**
1. **Page count** — 3–5 (quick guide / checklist) / 6–8 (standard guide) / 9–10 (deep dive) (default: 6)
2. **Key takeaways** — 3–5 things the reader should know or do after reading (informs chapter structure)
3. **Brand name** — company or product name for cover and footer (or "skip")
4. **Brand logo** — URL or "none"

**Design**
5. **Style** — clean-slate / midnight-editorial / matt-gray / product-minimal / mint-pixel-corporate / warm-earth / brutalist / magazine-red / soft-cloud / "show me options" (default: clean-slate)
6. **Chapter count** — how many main sections? (default: derived from page count)

**Output**
7. **CTA details** — demo booking / newsletter signup / template download / other (default: "book a demo")
8. **Contact info** — email + URL for closing CTA page (or "I'll add later")
9. **Slug** — filename slug (e.g., "reduce-churn-guide-2025"; derived from topic if skipped)

**Defaults:**

| Question | Default |
|---|---|
| Page count | 6 |
| Key takeaways | derive from topic |
| Brand name | none |
| Brand logo | none |
| Style | clean-slate |
| Chapter count | derived from page count |
| CTA details | book a demo |
| Contact info | placeholder (flagged in checklist) |
| Slug | kebab-case of topic |

**If style = "show me options":** Generate 3 single-page HTML previews (cover page only) saved to `.claude-design/previews/style-a.html`, `style-b.html`, `style-c.html`. Open each automatically. Ask user to pick before Step 3.

---

## Step 3: Internal Architecture

Derive internally. Never show this to the user.

**Chapter → page mapping:**

| Pages | Typical structure |
|---|---|
| 3 | cover + [1 content page] + closing-cta |
| 4 | cover + [1 chapter-intro + 1 text-column] + closing-cta |
| 5 | cover + toc + [1 chapter-intro + 1 text-column] + closing-cta |
| 6 | cover + toc + [2 chapter-intros + 1 text-column] + closing-cta |
| 8 | cover + toc + [3 chapter-intros + 2 content pages] + closing-cta |
| 10 | cover + toc + [4 chapter-intros + 3 content pages] + key-takeaways + closing-cta |

**TOC rule:** Include for ebooks ≥ 6 pages. For 3–5 page ebooks, use a "What's inside" bullet list on the cover page or skip entirely.

**Three-point CTA architecture** (for ebooks ≥ 6 pages):
1. **Intro CTA** (after page 2) — subtle 1-line inline mention: "explore our [tool] at [url]"
2. **Mid-ebook CTA** (after a stat-grid or chapter-intro) — small `.callout--stat` or `.callout--tip` box with 1-line CTA
3. **Closing CTA** (final page) — full-page, primary conversion action

**Visual rhythm check:** If 2+ consecutive `text-column` pages appear in the plan → insert `quote-callout` or `stat-grid` between them before proceeding.

**Design direction** (derive from style preset + audience — never shown to user):

| Decision | Derive from |
|---|---|
| **Tone** | What emotional register does this audience expect? (authoritative, editorial, energetic, calm, warm…) |
| **Signature element** | ONE visual device used consistently: oversized decorative numerals, diagonal accent bar, dot-grid overlay, gradient mesh on cover, rule lines, geometric shape bleed. Pick one. Use it. |
| **Background system** | How do backgrounds vary across pages? Cover and chapter-intros = most distinctive. Content pages quieter but NOT all-white. Closing CTA = dark or full-accent inversion. No 3+ consecutive pages with identical background. |
| **Motion style** | What do `.reveal` animations do? Pick one and stay consistent: `translateY(16px) → 0`, `scale(0.97) → 1`, `translateX(-12px) → 0`. Stagger delays 0.1s apart. |
| **Unforgettable detail** | What is the ONE thing a reader will remember about the design? Name it before writing any CSS. |

If no strong direction is derivable from style preset alone, ask yourself: what would a top-tier design agency produce for this specific audience and topic? Then execute that.

**Body copy density limits:**
- text-column 1-col: 180–250 words max per page
- text-column 2-col: 280–380 words max (140–190 per column)
- text-sidebar: 140–180 words main + ≤70 words sidebar
- chapter-intro: 40–60 words (teaser only)
- quote-callout: 30–45 words
- stat-grid: 3–6 metrics, minimal labels

---

## Step 4: Page Structure

Read `references/page-library.md` before planning.

Output a numbered list with `[layout-type]` labels per page. Example for 6-pager:
```
Page 1: [cover] — title, subtitle, brand
Page 2: [toc] — 3 chapter titles + page numbers
Page 3: [chapter-intro] — Chapter 1 opener
Page 4: [text-column] — Chapter 1 body (1-column)
Page 5: [stat-grid] — 4 key metrics
Page 6: [closing-cta] — demo booking CTA + contact
```

**Confirm with user before Step 5.**

---

## Step 5: Content Draft

Write per-page copy in plain text (no HTML). Rules per layout type:

- **cover**: title (≤10 words, leads with value or tension — not a generic label) + subtitle (≤15 words) + optional category label + brand name
- **toc**: chapter titles (≤6 words each) + corresponding section numbers. Clean, numbered list.
- **chapter-intro**: chapter number (decorative) + chapter title (≤8 words) + teaser paragraph (2–3 sentences)
- **text-column (1-col)**: section heading + body paragraphs. Max 250 words. Prose > bullets. Every sentence earns its place.
- **text-column (2-col)**: same rules, 140–190 words per column. Use for comparisons, step pairs, dual perspectives.
- **text-sidebar**: main body (140–180 words) + sidebar callout type (tip / warning / stat / quote / checklist) with max 70 words
- **quote-callout**: pull quote ≤40 words + attribution (name, title, company or source)
- **stat-grid**: 3–6 metrics — number + label + 1-line context. Optional: 1-sentence narrative below.
- **key-takeaways**: 5–8 takeaways, ≤15 words each, imperative where possible
- **closing-cta**: headline ≤5 words (imperative) + 1-sentence body + CTA action + email + URL (both required)

**Forbidden words (no exceptions):** "powerful", "seamless", "game-changing", "leverage", "innovative", "revolutionary", "transform", "cutting-edge", "robust", "unlock", "scalable" (as filler).

---

## Step 6: HTML Generation

Read ALL of these before generating. Do not paraphrase or summarize them — read the actual files.

**This skill's references:**
- `references/design-system.md`
- `references/page-library.md`
- `references/style-presets.md`

**Bundled asset (exact path — include FULL verbatim contents in `<style>` block):**
- `assets/viewport-base.css` — bundled inside this skill's directory

> **Path resolution:** All paths prefixed `assets/` or `scripts/` are relative to the directory containing this SKILL.md file. In Claude Code after install: `~/.claude/skills/graphic-ebook/assets/` and `~/.claude/skills/graphic-ebook/scripts/`. Resolve the actual path from the SKILL.md file location before reading.

### Generation Rules

1. **Single self-contained HTML.** All CSS inline. Font CDN `<link>` only external dependency.

2. **Include FULL verbatim contents** of `viewport-base.css` inside the `<style>` block.

3. **Add A4 portrait overrides AFTER viewport-base.css** (in the same `<style>` block):
```css
/* A4 portrait overrides */
html { scroll-snap-type: none; scroll-behavior: auto; }
.slide {
  width: 100vw;
  height: 100vh;
  height: 100dvh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  position: relative;
  scroll-snap-align: none;
}
/* CRITICAL: prevents Chromium from stripping backgrounds in PDF */
* { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
```

4. **Each page = `<section class="slide">`** — required for export-pdf.sh page detection.

5. **Comment each page:** `/* === PAGE N: LAYOUT-TYPE === */`

6. **Body text:** `clamp(0.875rem, 1.25vw, 1.05rem)`, `line-height: 1.75`, `max-width: min(65ch, 100%)` on all `<p>` in text-column and text-sidebar layouts.

7. **Stat numbers:** hero at `clamp(3rem, 8vw, 5.5rem)` in accent color. Supporting at `clamp(2.5rem, 7vw, 5rem)` in secondary color.

8. **No images available** → CSS-generated visuals only (gradients, geometric shapes, dot patterns, abstract elements). Never show placeholder boxes.

9. **No SlidePresentation JS.** Include only minimal IntersectionObserver for `.reveal` animations.

10. **Chapter number decoration** (on chapter-intro pages):
```css
.chapter-number-deco {
  font-family: var(--font-display);
  font-size: clamp(6rem, 18vw, 14rem);
  font-weight: var(--display-weight);
  opacity: 0.06;
  position: absolute;
  top: -0.1em;
  right: var(--page-padding);
  line-height: 1;
  color: var(--accent);
  pointer-events: none;
  user-select: none;
}
```

11. **Typed callout boxes** (for text-sidebar pages):
```css
.callout { border-left: 3px solid; border-radius: var(--card-radius, 4px); padding: clamp(0.75rem, 1.5%, 1.1rem); }
.callout-label { font-size: clamp(0.58rem, 0.8vw, 0.68rem); font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 0.5em; }
.callout--tip      { background: rgba(22, 163, 74, 0.07);  border-color: #16A34A; }
.callout--tip      .callout-label { color: #16A34A; }
.callout--warning  { background: rgba(217, 119, 6, 0.07);  border-color: #D97706; }
.callout--warning  .callout-label { color: #D97706; }
.callout--stat     { background: rgba(var(--accent-rgb, 100,100,100), 0.07); border-color: var(--accent); }
.callout--stat     .callout-label { color: var(--accent); }
.callout--quote    { background: var(--bg-elevated); border-color: var(--divider); font-style: italic; }
.callout--quote    .callout-label { color: var(--text-muted); }
.callout--checklist { background: rgba(8, 145, 178, 0.07);  border-color: #0891B2; }
.callout--checklist .callout-label { color: #0891B2; }
```

12. **Page footer** (on every page except cover):
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
HTML: `<div class="page-footer"><span>[Brand Name]</span><span>[N]</span></div>`

13. **2-column layout:** `display: grid; grid-template-columns: 1fr 1fr; gap: clamp(2rem, 4%, 3.5rem);` with `border-right: 1px solid var(--divider)` on left column.

14. **Text-sidebar layout:** `display: grid; grid-template-columns: 2fr 1fr; gap: clamp(1.5rem, 3%, 2.5rem);`

### Design Quality Rules (from frontend-design principles)

These govern the aesthetic ambition of every generated ebook. Applied after structural rules, before output.

**Typography:**
- Display font must have character at large sizes. Plus Jakarta Sans 800, Instrument Serif, Syne, Lora, Fraunces — all acceptable. Inter at display weight = immediate slop signal.
- Never use the same font weight for two consecutive hierarchy levels. Cover title (800) → chapter heading (700) → section heading (700, smaller size) → body (400/500).
- Pair a display font with a refined body font when the preset supports it (e.g. Instrument Serif + Inter, Syne + IBM Plex Sans). Single-font stacks must use weight contrast instead.

**Backgrounds and atmosphere:**
- Cover MUST have a significant decorative `::before` or `::after` pseudo-element creating visual depth: ghost letter at `opacity: 0.04–0.06`, geometric shape bleed, radial gradient overlay, or dot/line grid pattern.
- Chapter-intro pages MUST visually contrast with adjacent content pages — use `var(--bg-alt)` or a style-appropriate alt treatment.
- Content pages (text-column, text-sidebar) can be white/neutral, but the stat-grid and quote-callout pages should carry a distinct background (alt section bg, elevated card, or accent inversion).
- Closing CTA: always dark or full-accent inversion — never light. It is the conversion moment.
- CSS texture patterns when appropriate: `radial-gradient(circle, var(--accent) 1px, transparent 1px)` dot grids; `repeating-linear-gradient` rule lines; `::before` with clipped geometric shapes.

**Spatial composition:**
- Generous whitespace on chapter-intro pages — the visual openness signals a chapter break.
- At least one element per ebook should break the standard grid: oversized chapter deco number that bleeds off-screen right, quote mark that overlaps content, stat number that dominates 60%+ of its column.
- Avoid centered layouts unless the preset explicitly calls for it (quote-callout is the only centered-by-default layout).

**Motion:**
- All `.reveal` animations use consistent direction derived from design direction step.
- Stagger delays: 0.05s increments, max 0.5s cumulative. Nothing slower than 0.65s duration.
- Stat items in stat-grid: stagger by index for cascade effect.
- No animation on structural elements (footers, borders, rules). Animation = content appearing, not layout materializing.

**The unforgettable detail rule:**
Before writing the first line of CSS, name the ONE element that makes this ebook unmistakably designed — not just competently assembled. That element gets the most CSS investment. If you cannot name it, you have not thought hard enough about the design.

---

## Step 7: Self-QA

Fix every failure before proceeding to output. Do not skip this step.

**Layout & rendering:**
- [ ] Every `.slide` has `height:100vh; height:100dvh; overflow:hidden`
- [ ] `* { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }` present globally
- [ ] All scalable font sizes use `clamp()`
- [ ] No content overflows at 1200×1697 — review each page's density
- [ ] No placeholder boxes visible
- [ ] No `-clamp()`, `-min()`, `-max()` directly (wrap negatives in `calc(-1 * ...)`)

**Structure:**
- [ ] Page count matches Step 4 plan
- [ ] Every page uses `class="slide"` on `<section>` only
- [ ] All layout types from Step 4 present in correct order
- [ ] TOC included for ebooks ≥ 6 pages

**Reading quality:**
- [ ] Body text `line-height ≥ 1.75` on text-column and text-sidebar pages
- [ ] Single-column body text `max-width ≤ 65ch`
- [ ] No 2+ consecutive text-column pages without visual break
- [ ] TOC has chapter titles + section/page numbers
- [ ] Chapter-intro pages have `.chapter-number-deco` (opacity 0.06–0.08)
- [ ] Every page except cover has `.page-footer` with page number + brand name
- [ ] Sidebar callout boxes use typed CSS class (`.callout--tip/warning/stat/quote/checklist`)

**Design quality:**
- [ ] Style preset tokens applied consistently (from `references/style-presets.md`)
- [ ] No slop patterns (see `references/design-system.md` DO NOT USE list)
- [ ] Typography hierarchy: cover title >> chapter heading >> section heading >> body (2:1 min ratio between levels)
- [ ] Stat numbers visually dominant — no body copy at same visual weight
- [ ] Cover has a significant decorative `::before`/`::after` element — not just text on a flat color
- [ ] Chapter-intro pages visually distinct from content pages (different bg or treatment)
- [ ] Closing CTA uses dark or full-accent inversion background — never light
- [ ] No 3+ consecutive pages with identical background color
- [ ] Signature element from design direction step is present and visible
- [ ] At least one layout element breaks the grid (oversized deco number, bleed shape, dominant stat)
- [ ] Reveal animations consistent direction and stagger — not random per-element

**Content:**
- [ ] No forbidden words anywhere
- [ ] Cover title ≤10 words, leads with value or tension
- [ ] Quote callout ≤40 words
- [ ] Closing CTA: imperative headline + email + URL (both mandatory — QA fails without both)
- [ ] TOC matches actual page structure
- [ ] Three-point CTA present for ebooks ≥ 6 pages

---

## Step 8: Output

```bash
mkdir -p ebook/[slug]
```

**Write main HTML:** `ebook/[slug]/index.html`
**Open:** `open ebook/[slug]/index.html`

**Per-page split (always generate):**
Extract each `<section class="slide">` into standalone HTML files with full `<style>` block, no JS:
`ebook/[slug]/page-01.html`, `page-02.html`, … (zero-padded 2 digits)

**PDF export (always run):**
```bash
bash [skill-root]/scripts/export-pdf.sh \
  ebook/[slug]/index.html \
  ebook/[slug].pdf --portrait
```
`[skill-root]` = the directory containing this SKILL.md. Resolve it before running (e.g. `~/.claude/skills/graphic-ebook` in Claude Code after install).

**Cleanup:** Delete `.claude-design/previews/` if style preview files were generated in Step 2.

**Summary (no HTML in chat):**
```
## Ebook: [title]
Date: [today] | Style: [style] | Pages: [N] | Format: A4 portrait
Brand: [brand name] | Topic: [topic]

Files
  Main:      ebook/[slug]/index.html
  Per-page:  ebook/[slug]/page-01.html → page-0N.html
  PDF:       ebook/[slug].pdf

Checklist
- [ ] Replace contact info placeholders (email + URL on closing page)
- [ ] Replace brand logo initials with real asset
- [ ] Verify TOC section numbers match actual page positions
- [ ] Proof all stat accuracy (page [N])
- [ ] Review body copy — no page should feel overflowed
- [ ] Test PDF opens correctly (page count = [N])
```
