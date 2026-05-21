---
name: email-newsletter
description: Drafts and designs a complete HTML email newsletter from a topic or content brief. Outputs paste-ready HTML for Loops, Mailchimp, Beehiiv, Resend, or any standard email platform. Includes subject line options and plain-text fallback. Trigger when a user says "write a newsletter", "draft an email newsletter", "create an HTML email", "design an email for my subscribers", or "write a newsletter about [topic]".
compatibility: [claude-code, gemini-cli, github-copilot]
author: OpenDirectory
version: 1.0.0
---

# Email Newsletter

Draft and design a complete HTML email newsletter from a topic or content brief. Output is paste-ready for Loops, Mailchimp, Beehiiv, Resend, or any standard email platform.

---

**Critical rule:** Table-based HTML with inline styles only. No CSS classes, no flexbox, no grid, no `<style>` blocks. Every element gets `style=""` directly. This is not optional -- email clients strip everything else.

---

## Step 1: Brief Intake

Need three things to start. If all three present in the message: skip to Step 2.

If any missing, ask exactly:

> "To get started, I need three things:
> 1. **Topic** -- what is this newsletter about?
> 2. **Audience** -- who is reading? (role, company size, how they know you)
> 3. **Primary CTA** -- what one action do you want readers to take?"

Wait for all three before continuing.

---

## Step 2: Complete Intake

Ask all questions in one message, grouped by category. User can skip any -- defaults apply.

> "A few questions before I draft -- answer what you know, skip the rest:
>
> **Content**
> 1. **Length** -- brief (300 words, punchy) / standard (500-700) / deep dive (800+ words)?
> 2. **Format** -- editorial article / numbered breakdown / personal story / data report?
> 3. **Issue context** -- one-time send / part of weekly series / monthly digest?
> 4. **CTA URL** -- what's the actual link? (or I'll use a placeholder)
>
> **Brand**
> 5. **Company / brand name** -- for header and footer
> 6. **Tagline** -- one-line description (optional, for footer)
> 7. **City & country** -- for footer (e.g. "San Francisco, US")
> 8. **Primary brand color** -- hex? (e.g. #856FE6)
> 9. **Secondary accent** -- keep default yellow-green (#D8F90A) / use brand color / something else?
>
> **Design**
> 10. **Background** -- dark (editorial/SaaS) / light (clean/corporate) / custom hex?
> 11. **Display font** -- editorial serif (Instrument Serif) / clean modern sans / system fonts only?
> 12. **Button style** -- pill (very rounded) / softly rounded / sharp corners?
> 13. **Visual style** -- editorial / technical+data / warm+founder / bold+campaign?
>
> **Platform & Technical**
> 14. **Platform** -- Loops / Mailchimp / Beehiiv / Resend / other?
> 15. **Tone** -- educational / conversational / bold+direct / formal / playful?
> 16. **Personalization** -- none / first name / first name + company?
> 17. **Subject line** -- have one / want 3 options?
> 18. **Secondary sections** -- sponsor block / product callout / event / quick links / none?
> 19. **Plain-text version** -- yes (recommended) / no?"

**Defaults if skipped:**

| Question | Default |
|---|---|
| Length | standard (500-700 words) |
| Format | editorial article |
| Issue context | one-time send |
| CTA URL | `[CTA_URL]` placeholder |
| Company name | `[YOUR BRAND]` placeholder |
| Tagline | none |
| City & country | `[CITY, COUNTRY]` placeholder |
| Brand color | none (use `#D8F90A` for all accents) |
| Secondary accent | `#D8F90A` (yellow-green default) |
| Background | dark |
| Display font | Instrument Serif (editorial serif) |
| Button style | pill |
| Visual style | editorial |
| Platform | generic |
| Tone | conversational |
| Personalization | none |
| Subject line | generate 3 options |
| Secondary sections | none |
| Plain-text | yes |

---

## Step 2.5: Design Direction (internal -- not shown to user)

From Step 2 answers, determine:
- Visual character (from question 13, or inferred from tone + format if skipped)
- ONE unmissable element -- identify before Step 3
- Template path (see Step 5)

Character defaults if question 13 skipped:
- Educational / formal tone: Editorial
- Metrics-heavy content (stats, benchmarks, reports): Technical/data-forward
- Product launches, events, campaigns: Bold/campaign

Never ask the user for design direction separately -- derive it from their answers.

---

## Step 3: Structure Design

Read `references/html-email-guide.md` for layout rules before choosing sections.

Based on topic + audience + CTA + secondary sections requested, select sections from this library:

| Section | Include when |
|---|---|
| header | Always -- logo placeholder + issue number or date |
| hero | Always -- big headline + 1-2 sentence hook |
| intro | Conversational or educational tone -- short personal note |
| main-content | Primary article or insight (text-heavy) |
| stat-callout | There is a compelling stat, quote, or data point |
| secondary-section | Secondary CTA was requested |
| product-cta | Brand context present and soft product plug fits |
| sponsor-block | Sponsor section was requested |
| quick-links | Curated links section was requested |
| footer | Always -- unsubscribe link + company name |

Output the chosen structure as a numbered list with one-line purpose per section:

```
Proposed structure:
1. Header -- logo + Issue #1 / [date]
2. Hero -- headline + hook paragraph
3. Intro -- short personal framing
4. Main Content -- [topic] breakdown
5. Stat Callout -- key data point from the story
6. CTA -- [cta text]
7. Footer -- unsubscribe + company

Does this structure work, or should I adjust any sections?
```

Wait for confirmation before Step 4.

---

## Step 4: Content Draft

Write copy for each section in sequence. No HTML yet -- clean prose only.

**Rules per section:**
- **Header**: Issue number + date. No copy needed.
- **Hero headline**: 8 words max, outcome-focused, no starting with "I/We/Our"
- **Hero hook**: 1-2 sentences, problem or curiosity gap, pulls reader in
- **Intro**: 2-3 sentences, personal or contextual, not corporate-speak, contractions OK
- **Main content**: 250-400 words, scannable -- use **bold phrases** for key points, short paragraphs (1-3 lines), no walls of text, no bullet overload
- **Stat callout**: One stat or quote, 20 words max, punchy
- **Product CTA**: 2-3 sentences, value-forward, not "Check out our product" -- tell them what changes for them
- **CTA button text**: 3-5 words, action verb + benefit ("Read the full breakdown", "Save my seat", "Get the guide")
- **Footer**: Unsubscribe link placeholder + company name

Read `references/subject-line-formulas.md` then write 3 subject line options (if subject line not provided by user):
- Option A: Curiosity gap formula
- Option B: Direct benefit formula
- Option C: Number/list formula

Do not use em dashes. Do not use: "powerful", "seamless", "game-changing", "leverage", "innovative", "unlock", "transform", "elevate", "cutting-edge", "robust".

---

## Step 5: HTML Generation

Read `references/design-system.md` and `references/html-email-guide.md` before generating HTML.

**Template or custom -- decide based on Step 2 answers:**

**Use `templates/dark-newsletter.html` as base when ALL of:**
- background = dark (or not specified)
- display font = Instrument Serif (or not specified)
- no custom background hex provided

**Use `templates/light-newsletter.html` as base when ALL of:**
- background = light OR tone = formal
- display font = Instrument Serif (or not specified)
- no custom background hex provided

**Generate custom HTML from scratch when ANY of:**
- custom background hex provided (not dark, not white)
- display font = modern sans or system fonts only
- combination of answers produces a design neither template serves

For custom generation: use `references/design-system.md` Custom Generation Guide as the full token spec. Apply user's background/font/button/accent choices throughout.

**Then (for template path):**
1. Select only the sections needed from the template (based on Step 3 structure)
2. Fill in all `[PLACEHOLDER]` values with content from Step 4
3. Apply brand color substitution (see below)
4. Verify all `[UNSUBSCRIBE_URL]` placeholders are still present (platform tuning happens in Step 6)

**Brand color substitution rules:**

If `brand_color` is provided:
- Replace brand strip `bgcolor` (`#D8F90A` in the `height:2px` row) with brand_color
- Replace stat callout left border color with brand_color
- Replace category label color with brand_color
- If brand_color luminance is high (yellows, greens, oranges -- most neons): replace step badge `#D8F90A` with brand_color too
- If brand_color luminance is low (dark navy, forest, charcoal): keep step badges and CTA button as `#D8F90A`, only use brand_color for strip + stat border

If `brand_color` is NOT provided: keep all `#D8F90A` values as-is.

**Content substitution rules (from Step 2 answers):**
- If `company_name` provided: replace all `[YOUR BRAND]` and `[COMPANY NAME]` placeholders
- If `city_country` provided: replace `[CITY, COUNTRY]` placeholder
- If `tagline` provided: add as subtitle line in footer after company name
- If `cta_url` provided: replace all `[CTA_URL]` placeholders with actual URL
- If `personalization = first_name`: add platform-appropriate first name variable to hero greeting -- e.g. `Hey %%first_name%%,` on Beehiiv, `Hey {{first_name}},` on Loops, `Hey *|FNAME|*,` on Mailchimp
- If `personalization = first_name + company`: add both variables where contextually appropriate

**Brand color visual tension check (on dark email):**

Does the brand color visually pop on `#111111`? Test mentally: would it be visible as a 2px strip?
- High-saturation colors (purples, blues, teals, pinks, yellows, oranges, greens): YES -- use for strip + stat border + category label
- Low-saturation / near-neutral (warm greys, beige, off-white): strip only; category label reverts to `#555555`
- Near-black (very dark navy, forest, charcoal below ~`#2A2A2A`): skip brand_color for ALL accent uses, fall back to `#D8F90A` for every element

**Accent discipline rule:** brand_color appears in AT MOST 3 places: brand strip, stat border, category label. Never in body copy, headlines, button backgrounds, or section backgrounds. Over-branding kills the premium feel.

**CTA button text color:**
- On `#D8F90A` button background: always use `#0A0A0A` text (it's a light color)
- On `#111111` button background (inside yellow callout card): always use `#F2F2F2` text
- On brand_color button: use `#0A0A0A` if brand is light, `#FFFFFF` if brand is dark

**Required on every `<td>` with a background color:**
Both the `bgcolor=` HTML attribute AND the inline `background-color:` style. Example:
```html
<td bgcolor="#D8F90A" style="background-color:#D8F90A;">
```
The attribute handles Outlook. The style handles everything else. Never use just one.

**Design excellence (frontend-design principles, email-adapted):**

Email's table constraints don't limit design ambition. Push within them:

- **Typography to its extreme**: 4-5 word headlines = 60px, `-0.04em` tracking. 6-7 word headlines = 56px, `-0.03em`. 8 words = 48px. Never size down for safety -- the headline is a poster, not a label. Instrument Serif italic on stat quotes adds literary weight no other element can match.

- **Density contrast as craft signal**: Hero = maximum open space (64px top). Body paragraphs = tight and dense. CTA callout card = maximum open space again (64px). Open → tight → open is the rhythm that reads as intentional design, not template output.

- **Background depth via section alternation** (all email-safe):
  - Header: `#0A0A0A`
  - Hero: `#111111`
  - Stat callout outer: `#111111`, inner elevated card: `#1A1A1A`
  - Body paragraphs: `#161616` (subtle elevation creates depth without color)
  - Step cards: `#111111` (contrast with body)
  - CTA callout card: `#D8F90A` (the ONLY bright element -- never dilute)
  - Footer: `#080808`

- **Accent scarcity = luxury**: One yellow callout card in a sea of dark reads premium. Yellow appearing in six places reads cheap. The CTA card's power comes entirely from being the single bright element in a dark email.

- **Unforgettable test**: Before saving, state in one sentence what a reader would describe to a colleague 3 hours later. If it's vague ("it was dark and clean") -- the visual anchor isn't strong enough. Make it specific ("the yellow card with the big serif headline").

- **Stat callout as editorial pull quote**: 4px left border (not 3px). 26px italic Instrument Serif on the quote text. 32px inner padding. This is the closest an email gets to a magazine pull quote. Treat it like one.

---

## Step 6: Platform Tuning

Read `references/platform-compat.md` and apply platform-specific adjustments:

| Platform | Action |
|---|---|
| Loops | Replace `[UNSUBSCRIBE_URL]` with `{{unsubscribe_url}}`. Replace `[FIRST_NAME]` refs with `{{first_name}}` |
| Mailchimp | Replace `[UNSUBSCRIBE_URL]` with `*\|UNSUB\|*`. Add `mc:edit="[section-name]"` to editable `<td>` blocks |
| Beehiiv | Replace `[UNSUBSCRIBE_URL]` with `%%unsubscribe_url%%`. Replace `[FIRST_NAME]` with `%%first_name%%` |
| Resend | Replace `[UNSUBSCRIBE_URL]` with `{unsubscribeUrl}`. Note: React Email `.tsx` output available on request |
| Generic/Other | Keep `[UNSUBSCRIBE_URL]` as placeholder with comment: `<!-- Replace with your unsubscribe link -->` |

---

## Step 7: Self-QA

Check the generated HTML before output. Fix every issue found -- do not skip.

**Rendering checks:**
- [ ] All styles inline -- no `<style>` blocks, no `class=` attributes anywhere
- [ ] All `<table>` have `cellpadding="0" cellspacing="0" border="0"`
- [ ] Images (if any) have `alt=""`, `border="0"`, `display:block` in style
- [ ] Max-width 600px enforced on container table
- [ ] CTA button uses `<table>` + `<td>` structure with `bgcolor=` attribute, not just `<a>` with `display:block`
- [ ] No `flexbox`, `grid`, `position:`, `float:`, CSS variables (`--var`), `min-height`, `max-height` in any inline style
- [ ] `border-radius` on `<td>` only -- not on `<table>` or `<a>` (Outlook renders `<td>` radius)
- [ ] Footer has unsubscribe link with platform-correct variable

**Content checks:**
- [ ] Hero headline is 8 words or fewer
- [ ] CTA button text is 3-5 words
- [ ] No em dashes (-- is fine, not --)
- [ ] No banned words: "powerful", "seamless", "game-changing", "leverage", "innovative", "unlock", "transform", "elevate", "cutting-edge", "robust"
- [ ] Plain-text version strips all HTML cleanly (if requested)

**Design quality checks:**
- [ ] ONE unmissable element from Step 2.5 is visually dominant -- not buried between equal-weight sections
- [ ] Typography hierarchy clear: H1 >> H2 >> body -- size contrast at least 2:1 between each level
- [ ] All spacing values from valid rhythm only: 8 / 16 / 20 / 24 / 32 / 40 / 52 / 64px -- no arbitrary values (18px, 22px, 30px, 45px, etc.)
- [ ] Brand color appears in 3 or fewer places -- count instances; if more, remove from lowest-priority element
- [ ] No email slop patterns -- check against the slop list in `references/design-system.md`

If any check fails: fix inline, then re-run the checklist mentally.

---

## Step 8: Subject Line Presentation

If 3 subject line options were generated, present them with a recommendation:

```
**Subject Line Options**

A. [subject] -- [formula used, best for what audience/context]
B. [subject] -- [formula used]
C. [subject] -- [formula used]

Recommendation: [A/B/C] -- [one sentence reason based on audience and tone]
```

If user provided their own subject line, skip this step.

---

## Step 9: Save Files + Present Summary

**Save the HTML to a file first -- do not dump it in the chat.**

```bash
mkdir -p docs/newsletters
```

Write the full HTML to:
`docs/newsletters/[topic-slug]-[YYYY-MM-DD].html`

Where `[topic-slug]` is the topic lowercased with spaces replaced by hyphens (e.g. "AI B2B Sales" → `ai-b2b-sales`).

If a plain-text version was requested, also write it to:
`docs/newsletters/[topic-slug]-[YYYY-MM-DD].txt`

**Then present this summary in the chat (no HTML code fence):**

```
## Newsletter: [topic slug]
Date: [today's date] | Platform: [platform] | Tone: [tone]

Saved to: docs/newsletters/[topic-slug]-[YYYY-MM-DD].html

---

### Subject Lines
A. [subject A] -- [formula]
B. [subject B] -- [formula]
C. [subject C] -- [formula]
Recommended: [letter] -- [one-sentence reason]

---

### Send Checklist
- [ ] Replace [CTA_URL] with your actual link
- [ ] Replace [COMPANY NAME] and [CITY, COUNTRY] in footer
- [ ] Replace [YOUR BRAND] in header with your brand name (or swap in a logo image)
- [ ] Verify unsubscribe variable works in [platform]
- [ ] Send a test email to yourself before launching
```

Do not print the HTML in the chat. The file path tells the user where to find it.

---

## Section Reference

| Section | Purpose |
|---|---|
| header | Logo + issue number or date |
| hero | Big headline + 1-2 sentence hook |
| intro | Short personal note or context |
| main-content | Primary article or insight (text-heavy) |
| image-block | Full-width image + caption |
| stat-callout | Highlighted stat or quote in a box |
| secondary-section | Second story or feature |
| product-cta | Soft product plug or feature highlight |
| sponsor-block | Sponsored content (clearly labeled) |
| quick-links | Curated links section (3-5 items) |
| footer | Unsubscribe link, company info, legal |

## Output Formats (on request)

- **Standard HTML** (default): inline-styled, table-based, works everywhere
- **React Email**: `.tsx` component output -- request explicitly, good for Resend + dev teams
- **Plain text**: stripped fallback always included unless user opts out
