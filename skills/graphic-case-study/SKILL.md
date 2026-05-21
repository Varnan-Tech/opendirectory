---
name: graphic-case-study
description: Generates a professionally designed case study PDF for B2B SaaS sales and marketing. Supports 7 page layouts, 9 style presets, 1-4 page output. Trigger when user says "create a case study", "write a customer story", "make a case study PDF", "design a success story", "turn this customer win into a PDF".
compatibility: [claude-code, gemini-cli, github-copilot]
author: OpenDirectory
version: 1.0.0
---

# Graphic Case Study

Generate a professionally designed B2B case study PDF from customer story details. Output is a single self-contained HTML file (opens in any browser) plus a print-ready PDF. Supports 7 page section layouts and 9 style presets.

---

**Critical rules -- non-negotiable:**

1. Every page MUST fit within the A4 canvas (1200×1697px). No content overflow.
2. ALL scalable font sizes use `clamp()`. Fixed px only for structural borders/lines.
3. Single self-contained HTML: all CSS inline. Zero external dependencies except font CDN link.
4. Never dump HTML in chat. Save to file, show summary only.
5. Results stat numbers MUST be visually dominant -- at least 3× body text size.
6. No generic AI slop: no Inter as display font, no purple gradient on white, no "Thank You" closing.

---

## Step 1: Brief Intake

Need four things to start. If all four present in the message: skip to Step 2.

If any missing, ask exactly:

> "To create your case study, I need four things:
> 1. **Customer name** -- company name (or a descriptor to anonymize: "Fortune 500 Retailer")
> 2. **Challenge** -- what problem did they have before using your product? (2-5 sentences)
> 3. **Solution** -- what did your product do to solve it? (features, approach)
> 4. **Results** -- measurable outcomes: ideally 3 stats (%, time saved, revenue impact, etc.)"

Wait for all four before continuing.

---

## Step 2: Complete Intake

Ask all questions in one message, grouped by category. User can skip any -- defaults apply.

> "A few questions before I start:
>
> **Content**
> 1. **Customer context** -- industry, company size, location? (optional, used for overview page)
> 2. **Testimonial** -- customer quote (40 words max) + speaker name + title? (or "I'll add later")
> 3. **Page count** -- 1-pager (summary card) / 2-pager (standard, default) / 4-pager (detailed)
> 4. **Customer logo** -- URL or "none"
>
> **Design**
> 5. **Your company name** -- vendor name for the CTA page (+ logo URL if available)
> 6. **Style** -- clean-slate / midnight-editorial / matt-gray / product-minimal / mint-pixel-corporate / warm-earth / brutalist / magazine-red / "show me options"
> 7. **Orientation** -- A4 portrait (default, 1200×1697) / landscape 4:3 (1200×900)
>
> **Output**
> 8. **Anonymize?** -- Keep company name / replace with industry descriptor
> 9. **Slug** -- filename slug (e.g. "acme-corp-2025"); I'll derive from customer name if skipped"

**Defaults if skipped:**

| Question | Default |
|---|---|
| Customer context | none |
| Testimonial | none |
| Page count | 2 |
| Customer logo | none |
| Your company name | derived from context |
| Style | clean-slate |
| Orientation | A4 portrait |
| Anonymize | keep name |
| Slug | kebab-case of customer name |

**If style = "show me options":**
Generate 3 single-page HTML previews (cover page only). Save to `.claude-design/previews/style-a.html`, `style-b.html`, `style-c.html`. Open each: `open .claude-design/previews/style-a.html` etc. Choose 3 style presets that match the case study context. Ask user to pick before Step 3.

---

## Step 2.5: Internal Page Architecture (not shown to user)

Derive internally before Step 3. Never ask the user.

**Hero metric identification:**
Scan results for the single most impressive number (largest %, biggest $, greatest multiplier). This metric gets accent-color treatment and maximum visual weight on the results page.

**Page count -> structure template:**

| Count | Page sequence |
|---|---|
| 1-pager | 1 page: [cover-compact] -- all content condensed into one page |
| 2-pager | Page 1: [cover] + [challenge-solution] stacked · Page 2: [results] + [testimonial-cta] stacked |
| 4-pager | Page 1: [cover] · Page 2: [overview] + [challenge] · Page 3: [solution] + [results] · Page 4: [testimonial] + [closing-cta] |

**Visual character** derived from style choice:
- clean-slate → professional authority, generous whitespace, enterprise-safe
- midnight-editorial → premium dark, editorial weight, tech/AI companies
- matt-gray → trusted neutral, operational, board-safe
- warm-earth → approachable warmth, consulting/agency/services
- brutalist → bold standout, design-forward, attention-commanding
- If not specified: default to clean-slate for B2B SaaS, midnight-editorial for technical companies.

---

## Step 3: Page Structure

Read `references/page-library.md` before planning.

Plan the full page sequence. Assign section types from the 7 in `references/page-library.md` to each page section. Multiple sections can stack within one page.

Output as numbered list with `[section-type]` labels per page. Example for 2-pager:

```
Proposed structure (2 pages, clean-slate style):

Page 1:
  [cover] -- Acme Corp cut reporting time by 80%
  [challenge-solution] -- manual process / DataPulse automation

Page 2:
  [results] -- 80% time saved, 95% error reduction, $200K saved
  [closing-cta] -- Get in touch: hello@datapulse.io

Does this structure work, or should I adjust anything?
```

Wait for confirmation before Step 4.

---

## Step 4: Content Draft

Write per-page-section copy. Plain text only -- no HTML yet.

**Copy rules per section:**

- `cover`: company name + headline result (12 words max, MUST lead with the number: "Acme cut reporting time by 80%") + optional category label ("Customer Success Story")
- `overview`: 4 facts only -- Industry / Company size / Location / Use case -- each value 4 words max
- `challenge`: context paragraph (2-3 sentences) + 3 pain points (1 sentence each, no bullet filler)
- `solution`: 2-3 feature callouts -- feature name (3 words max) + 1-sentence outcome description each
- `results`: 3 metrics (number + short label + 1-line context). Optional: 2-sentence narrative. ZERO body copy at same weight as the numbers.
- `testimonial`: exact quote (40 words max) + speaker name + title + company
- `closing-cta`: headline (5 words max) + CTA action text (3 words) + email + URL (both required)

**Forbidden words** (no exceptions): "powerful", "seamless", "game-changing", "leverage", "innovative", "revolutionary", "transform", "cutting-edge", "robust", "unlock", "scalable" (as filler adjective).

**Copy philosophy:** Numbers beat adjectives. Lead every section with the outcome, not the feature. Fragments are fine.

---

## Step 5: HTML Generation

Read ALL before generating any HTML:

**This skill's references:**
- `references/design-system.md`
- `references/page-library.md`
- `references/style-presets.md`

**frontend-slides cross-references (read this exact file):**
- `/Users/ksd/Desktop/Varnan_skills/frontend-slides/viewport-base.css` -- include FULL contents verbatim inside `<style>` block

**Generation rules:**

1. Single self-contained HTML. All CSS inline. Font CDN `<link>` is the only external reference.
2. Include the FULL verbatim contents of `viewport-base.css` inside the `<style>` block -- do not paraphrase or shorten it.
3. After pasting viewport-base.css, add portrait A4 overrides:
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
   ```
4. Every page section = `<section class="slide">` -- required for export-pdf.sh detection.
5. Comment each page: `/* === PAGE N: SECTION-TYPES === */`
6. Results stat numbers: `clamp(2.5rem, 7vw, 5rem)` minimum. Hero metric in accent color. Other metrics in secondary text color.
7. No images provided -> CSS-generated visuals (geometric shapes, gradient backgrounds, icon-like CSS constructs). Never output visible placeholder boxes.
8. No SlidePresentation JS. Include only a minimal IntersectionObserver for `.reveal` entrance animations (viewer experience; PDF export renders to final state automatically).
9. For landscape 4:3 (if requested): use `clamp()` values from graphic-slide-deck proportions -- landscape 1200×900 means 1vw=12px, similar to portrait.

**Typography discipline (all clamp-based, tuned for 1200px A4 portrait):**
- Cover headline: `clamp(2rem, 5vw, 3.5rem)`
- Section heading: `clamp(1.25rem, 2.5vw, 2rem)`
- Body: `clamp(0.875rem, 1.25vw, 1.1rem)`
- Stat number (hero): `clamp(3rem, 8vw, 5.5rem)` in accent color
- Stat number (secondary): `clamp(2.5rem, 7vw, 5rem)` in secondary color
- Quote: `clamp(1.1rem, 2vw, 1.5rem)` italic
- Label/caption: `clamp(0.65rem, 0.9vw, 0.8rem)` uppercase

---

## Step 6: Self-QA

Check every item. Fix every failure -- do not skip.

**Layout and rendering:**
- [ ] Every `.slide` has `height:100vh; height:100dvh; overflow:hidden`
- [ ] ALL scalable font sizes use `clamp()`
- [ ] No content overflows at 1200×1697 viewport -- check each page's density against `references/page-library.md` limits
- [ ] CSS-generated visuals present for all image placeholder spots
- [ ] No `-clamp()`, `-min()`, `-max()` in CSS -- wrap negatives in `calc(-1 * ...)`

**Structure:**
- [ ] Page count matches Step 3 plan
- [ ] Every page uses `class="slide"`
- [ ] All content sections from Step 3 are present
- [ ] `class="slide"` only on `<section>` elements, not inner divs

**Design quality:**
- [ ] Hero metric visually dominant on results section -- accent color, largest size, no competing elements at equal weight
- [ ] Style preset tokens applied consistently (colors, fonts from `references/style-presets.md`)
- [ ] No slop patterns (check DO NOT USE list in `references/style-presets.md`)
- [ ] Typography hierarchy clear: cover headline >> section heading >> body (at least 2:1 ratio)

**Content:**
- [ ] No forbidden words in any copy
- [ ] Cover headline leads with a number or measurable result
- [ ] Testimonial quote is 40 words or fewer
- [ ] Closing CTA has headline + action + email + URL (all four)
- [ ] All stats in results section have labels (no naked numbers)

---

## Step 7: Output

**Save the main HTML:**

```bash
mkdir -p case-study/[slug]
```

Write to: `case-study/[slug]/index.html`

Open it: `open case-study/[slug]/index.html`

**Per-page HTML files (always generate these):**

Extract each `<section class="slide">` from the main HTML. For each one, create a standalone file with:
- The full `<style>` block from the main HTML (copied verbatim)
- The individual `<section class="slide">` wrapped in a minimal HTML shell
- No JS (static per-page viewing)

Write to: `case-study/[slug]/page-01.html`, `page-02.html`, etc.

**PDF export (always do this for A4 portrait):**

```bash
bash /Users/ksd/Desktop/Varnan_skills/frontend-slides/scripts/export-pdf.sh \
  case-study/[slug]/index.html \
  case-study/[slug].pdf --portrait
```

If landscape 4:3 was requested, omit `--portrait` and use `--compact` instead (1280×720).

Note: first run installs Playwright automatically (~30-60 seconds). Inform the user.

**Cleanup:** Delete `.claude-design/previews/` if style preview files were generated in Step 2.

---

## Step 8: Summary (no HTML in chat)

Present in chat:

```
## Case Study: [customer name]
Date: [today] | Style: [style] | Pages: [N] | Format: A4 portrait
Vendor: [your company] | Customer: [customer name]

---

### Files
Main:      case-study/[slug]/index.html
Per-page:  case-study/[slug]/page-01.html -> page-0N.html
PDF:       case-study/[slug].pdf

---

### Case Study Checklist
- [ ] Replace [IMAGE: logo] placeholder with real logo file
- [ ] Verify all stats are accurate (page [results page number])
- [ ] Confirm customer has approved quote usage
- [ ] Proof company name spelling, speaker title accuracy
- [ ] Test PDF page count = [N] and no content clips
- [ ] Share PDF at case-study/[slug].pdf
```

Do not print HTML in chat.

---

## Section Reference

| Section | Purpose |
|---|---|
| cover | Opening page -- customer name, headline result, logos |
| overview | At-a-glance profile -- industry, size, use case |
| challenge | The problem -- context + pain points |
| solution | How your product solved it -- feature callouts |
| results | Key metrics + supporting narrative |
| testimonial | Full-width pull quote from customer |
| closing-cta | Vendor logo + contact info + next step |
