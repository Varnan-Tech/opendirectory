---
name: graphic-slide-deck
description: Generates a professionally designed HTML slide deck from a brief or content. Outputs a single-file presentation + optional PDF. Supports 13 layout types and 8 style presets. Trigger when user says "create a slide deck", "make a presentation", "build a pitch deck", "make slides", "convert my notes to slides".
compatibility: [claude-code, gemini-cli, github-copilot]
author: OpenDirectory
version: 1.0.0
---

# Graphic Slide Deck

Generate a professionally designed HTML slide deck from a brief, content notes, or an existing file. Output is a single self-contained HTML file -- opens in any browser, no build tools.

---

**Critical rules -- non-negotiable:**

1. Every slide MUST fit within 100vh. No scrolling inside slides. Content overflows → split into two slides.
2. ALL font sizes and spacing MUST use `clamp()`. Never fixed px/rem on anything that scales.
3. Single self-contained HTML: all CSS/JS inline. Zero external dependencies except font CDN link.
4. Never dump HTML in chat. Save to file, show summary only.
5. No generic AI slop aesthetics -- check against the DO NOT USE list in `references/style-presets.md`.

---

## Step 1: Brief Intake

Need three things to start. If all three present in the message: skip to Step 2.

If any missing, ask exactly:

> "To get started, I need three things:
> 1. **Purpose** -- what is this deck for? (investor pitch / sales call / conference talk / internal presentation / onboarding / other)
> 2. **Audience** -- who will see it? (VCs, prospects, your team, executives, conference room, LinkedIn)
> 3. **Topic or content** -- paste notes, a URL, a brief description, or upload a file"

Wait for all three before continuing.

---

## Step 2: Complete Intake

Ask all questions in one message, grouped by category. User can skip any -- defaults apply.

> "A few questions before I start:
>
> **Content**
> 1. **Key message** -- single sentence the audience must remember after leaving
> 2. **Slide count** -- Short (5-10) / Medium (10-20) / Long (20+)?
> 3. **Content source** -- All content ready / Rough notes (I'll structure) / Topic only (I'll draft)?
> 4. **Existing assets** -- Any images, screenshots, or logos to include? (yes + paths / no)
>
> **Design**
> 5. **Style** -- midnight-editorial / matt-gray / clean-slate / brutalist / mint-pixel-corporate / product-minimal / magazine-red / soft-cloud / "show me options"
> 6. **Aspect ratio** -- 16:9 (1920×1080, default) / 1:1 (1080×1080, LinkedIn)
> 7. **Inline editing** -- should text be editable in-browser after export? (Yes / No)
>
> **Output**
> 8. **Output format** -- HTML only / HTML + PDF / HTML + PDF + deploy to URL
> 9. **Deck name** -- slug for file/folder naming (e.g. "q2-investor-pitch"); I'll derive if skipped"

**Defaults if skipped:**

| Question | Default |
|---|---|
| Key message | derived from purpose + topic |
| Slide count | 12 |
| Content source | topic only |
| Existing assets | none |
| Style | clean-slate |
| Aspect ratio | 16:9 |
| Inline editing | No |
| Output format | HTML + PDF |
| Deck name | derived from topic slug |

**If style = "show me options":**
Generate 3 single-slide HTML previews (one for each of 3 different style presets that fit the deck's purpose). Save to `.claude-design/previews/style-a.html`, `style-b.html`, `style-c.html`. Open each: `open .claude-design/previews/style-a.html` etc. Ask user to pick before Step 3.

---

## Step 2.5: Internal Design Direction (not shown to user)

From Step 2 answers, determine before Step 3:

**Visual character** (derived from style, or inferred if not specified):
- midnight-editorial or magazine-red → `dark-editorial`
- clean-slate or product-minimal → `light-minimal`
- matt-gray → `neutral-professional`
- brutalist → `bold-expressive`
- mint-pixel-corporate or soft-cloud → `fresh-corporate`
- Style not specified: investor pitch → midnight-editorial; sales → clean-slate; conference → brutalist or midnight-editorial; internal → matt-gray

**ONE unmissable slide** -- identify before Step 3:
- Investor pitch → stat-highlight (traction/metrics slide)
- Sales deck → stat-highlight (ROI/results slide)
- Conference talk → quote-callout or stat-highlight (key insight)
- Internal presentation → closing-cta (decision/recommendation slide)

**Layout selection bias** -- note the 2-3 most relevant layouts for this deck type to prioritize in Step 3.

Never ask the user for design direction -- derive it entirely from their answers.

---

## Step 3: Structure Design

Read `references/layout-library.md` before planning.

Plan the full slide sequence. Assign a layout type from the 13 in `references/layout-library.md` to each slide.

**Deck type → typical structure:**

**Investor pitch (12 slides):**
1. [title-hero] Company + tagline
2. [section-divider] The Problem
3. [text-full] Problem detail
4. [text-left-image-right] Solution overview
5. [image-full] Product screenshot
6. **[stat-highlight] Traction -- unmissable slide**
7. [comparison-table] vs. competitors
8. [timeline] Roadmap
9. [text-full] Team
10. [stat-highlight] Market size
11. [text-left-image-right] Business model
12. [closing-cta] The ask

**Sales deck (8-10 slides):**
1. [title-hero]
2. [quote-callout] Prospect pain point
3. [text-left-image-right] Solution
4. [image-grid] Product screenshots
5. **[stat-highlight] ROI/results -- unmissable**
6. [comparison-table] vs. alternatives
7. [text-full] Implementation / next steps
8. [closing-cta]

**Conference talk (15-20 slides):**
title-hero → section-dividers → text-full slides → image-full → **stat-highlight or quote-callout (unmissable)** → timeline → closing-cta

**Internal presentation (8-12 slides):**
title-hero → text-full (context) → stat-highlight (current state) → two-column-text (options) → comparison-table → text-full (recommendation) → **closing-cta (the decision -- unmissable)**

Output the proposed structure as a numbered list with `[layout-type]` in brackets. Example:

```
Proposed structure (12 slides, midnight-editorial style):

1. [title-hero] DataPulse -- Revenue decisions in 5 minutes
2. [section-divider] The Problem
...
12. [closing-cta] The ask + team@datapulse.io

Does this structure work, or should I adjust any slides?
```

Wait for confirmation before Step 4.

---

## Step 4: Content Draft

Write per-slide copy in sequence. Plain text only -- no HTML yet.

**Copy rules per layout:**

- `title-hero`: headline (6 words max) + subtitle (1 sentence) + optional pill badge text
- `section-divider`: 2-4 word section label only
- `text-full`: heading (5 words max) + 4-6 bullets OR 2 paragraphs (never both on same slide)
- `text-left-image-right` / `image-left-text-right`: heading + 3-4 bullets + `[IMAGE: description]`
- `two-column-text`: 2 column headings + max 3 bullets each
- `image-full`: `[IMAGE: description]` + optional caption (10 words max)
- `image-grid`: up to 6 `[IMAGE: description]` placeholders with short captions
- `stat-highlight`: 2-4 metrics written as `NUMBER | label` (e.g. `3× | faster close`). ZERO body copy.
- `quote-callout`: quote (30 words max) + attribution (name, title)
- `comparison-table`: column headers (3 max) + 4-6 row labels + cell content (1-3 words each)
- `timeline`: 3-6 milestones (label + date + 1-line description)
- `closing-cta`: headline (5 words max) + CTA action text + contact info (email + URL -- both required)

**Forbidden words** (in all copy, no exceptions):
"powerful", "seamless", "game-changing", "leverage", "innovative", "revolutionary", "transform", "cutting-edge", "robust", "unlock", "scalable" (as filler adjective).

**Copy philosophy:** Fragments are fine. Numbers beat adjectives. Every word earns its place.

---

## Step 5: HTML Generation

Read ALL before generating any HTML:

**This skill's references:**
- `references/design-system.md`
- `references/layout-library.md`
- `references/style-presets.md`
- `references/animation-guide.md`

**frontend-slides cross-references (read these exact files):**
- `/Users/ksd/Desktop/Varnan_skills/frontend-slides/viewport-base.css` -- include FULL contents verbatim inside `<style>` block
- `/Users/ksd/Desktop/Varnan_skills/frontend-slides/html-template.md` -- SlidePresentation class, keyboard nav, inline editing system
- `/Users/ksd/Desktop/Varnan_skills/frontend-slides/animation-patterns.md` -- entrance animations, background effects, interactive effects

**Generation rules:**

1. Single self-contained HTML. All CSS and JS inline. Font CDN `<link>` is the only external reference.
2. Include the FULL verbatim contents of `viewport-base.css` inside the `<style>` block -- do not paraphrase or shorten it.
3. Fonts from Google Fonts or Fontshare only. Font choices come from the chosen preset in `references/style-presets.md`.
4. Use the SlidePresentation class from `html-template.md`. Implement full keyboard navigation (arrows, space, page up/down), touch/swipe, progress bar, and nav dots. `navDotsContainer.innerHTML = ""` before building nav dots -- never skip this.
5. If inline editing opted-in: implement the full inline editing system from `html-template.md` including `exportFile()`. The `exportFile()` function MUST strip `contenteditable`, `body.edit-active`, and `.active`/`.show` classes before capturing `outerHTML`.
6. Aspect ratio:
   - 16:9 (default): slides are `width: 100vw; height: 100vh`
   - 1:1 (LinkedIn): add `--slide-height: min(100vh, 100vw)` CSS custom property and use it on `.slide`
7. Every slide section MUST use `class="slide"` -- required for export-pdf.sh's slide detection.
8. Add a comment before each slide: `/* === SLIDE N: LAYOUT-TYPE === */`
9. Apply the ONE unmissable slide from Step 2.5 with maximum visual weight -- largest typography, most animation, the style preset's signature element at full intensity. All other slides are compositionally quieter.
10. No images provided → use CSS-generated visuals (gradient meshes, geometric shapes, grid patterns from `animation-patterns.md`). This is a first-class path, not a fallback.

**Typography discipline:**
- Stat numbers: `clamp(3.5rem, 12vw, 9rem)` -- a metric that fills a third of the slide reads authoritative
- Hero headline: `clamp(2.5rem, 8vw, 6rem)` at minimum. Never size down for safety.
- Never use fixed px/rem on any element the user will see. Clamp everything.

**CSS gotcha from viewport-base.css:** Never write `-clamp()`, `-min()`, `-max()` directly in CSS. Wrap in `calc(-1 * clamp(...))`.

---

## Step 6: Self-QA

Check every item. Fix every failure -- do not skip.

**Viewport and rendering:**
- [ ] Every `.slide` has `height:100vh; height:100dvh; overflow:hidden`
- [ ] ALL font sizes and spacing use `clamp()` -- no fixed px on scaling elements
- [ ] No slide overflows at 1280×720 viewport (check against density limits from `layout-library.md`)
- [ ] Images use `max-height: min(50vh, 400px)`
- [ ] Breakpoints for 700px, 600px, 500px viewport heights present (from viewport-base.css)
- [ ] `prefers-reduced-motion` media query present
- [ ] No `-clamp()`, `-min()`, `-max()` in CSS -- wrapped in `calc(-1 * ...)` if negative needed

**Structure:**
- [ ] Slide count matches Step 3 plan
- [ ] Every slide uses `class="slide"`
- [ ] Each layout type correctly implemented per `references/layout-library.md`
- [ ] SlidePresentation class present with keyboard nav, touch, progress bar, nav dots
- [ ] `navDotsContainer.innerHTML = ""` before building nav dots
- [ ] If inline editing opted-in: `exportFile()` strips edit-state before capturing `outerHTML`

**Design quality:**
- [ ] ONE unmissable slide visually dominant -- not buried among equal-weight slides
- [ ] Typography hierarchy clear: display >> heading >> body (at least 2:1 size ratio between levels)
- [ ] Style preset tokens applied consistently (colors, fonts from `references/style-presets.md`)
- [ ] No slop patterns (check against DO NOT USE list in `references/style-presets.md`)

**Content:**
- [ ] No forbidden words in any slide copy
- [ ] title-hero headline is 6 words or fewer
- [ ] stat-highlight has ZERO body copy competing with the numbers
- [ ] closing-cta has specific action + contact info (not just "Thank You")

If any check fails: fix inline, then re-run the checklist mentally before proceeding.

---

## Step 7: Output

**Save the main HTML first:**

```bash
mkdir -p deck/[name]-slides
```

Write to: `deck/[name]-slides/index.html`

Open it: `open deck/[name]-slides/index.html`

**Per-slide HTML files (always generate these):**

Extract each `<section class="slide">` from the main HTML. For each one, create a standalone file with:
- The full `<style>` block from the main HTML (copied verbatim)
- The individual `<section class="slide">` wrapped in a minimal HTML shell
- No SlidePresentation JS (static per-slide viewing, no navigation needed)

Write to: `deck/[name]-slides/slide-001.html`, `slide-002.html`, etc. (zero-padded to 3 digits).

**If PDF requested:**

```bash
bash /Users/ksd/Desktop/Varnan_skills/frontend-slides/scripts/export-pdf.sh \
  deck/[name]-slides/index.html \
  deck/[name].pdf
```

Note: first run installs Playwright automatically (~30-60 seconds). Inform the user.

**If deploy requested:**

```bash
bash /Users/ksd/Desktop/Varnan_skills/frontend-slides/scripts/deploy.sh \
  deck/[name]-slides/
```

**Cleanup:** Delete `.claude-design/previews/` if style preview files were generated in Step 2.

---

## Step 8: Summary (no HTML in chat)

Present in chat:

```
## Slide Deck: [deck name]
Date: [today] | Style: [style] | Slides: [N] | Aspect: [16:9 or 1:1]
Purpose: [purpose] | Audience: [audience]

---

### Files
Main:      deck/[name]-slides/index.html
Per-slide: deck/[name]-slides/slide-001.html → slide-0NN.html
PDF:       deck/[name].pdf  [if generated]
Live URL:  [url]  [if deployed]

---

### Navigation
Arrow keys / Space / Page Up/Down -- advance slides
Click nav dots -- jump to any slide
Touch / swipe -- works on mobile

---

### Customize
Edit :root CSS variables at the top of the file to change colors
Swap the @import font URL to change typography
Remove .reveal class from elements to disable entrance animations

---

### Deck Checklist
- [ ] Replace [IMAGE: description] placeholders with real images
- [ ] Verify the metric/quote on slide [N] is accurate (the unmissable slide)
- [ ] Test on your target display size ([1920×1080 or 1080×1080])
- [ ] If presenting live: test keyboard nav in fullscreen mode (F11 / Cmd+Ctrl+F)
- [ ] Replace [QR: url] on closing slide with an actual QR code image
```

Do not print the HTML in the chat.

---

## Section Reference

| Layout | Use case |
|---|---|
| title-hero | Opening slide -- large headline + subtext |
| section-divider | Section break -- bold label, minimal |
| text-full | Headers + bullets or paragraphs |
| text-left-image-right | Side-by-side: text + image |
| image-left-text-right | Side-by-side: image first |
| two-column-text | Comparisons, pros/cons, before/after |
| image-full | Full-bleed image + optional caption |
| image-grid | 2×2 or 3×2 image gallery |
| stat-highlight | 2-4 large KPI metrics |
| quote-callout | Pull quote with attribution |
| comparison-table | Feature/option comparison grid |
| timeline | Horizontal or vertical milestones |
| closing-cta | Final slide -- CTA + contact info |
