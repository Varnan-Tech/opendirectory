# Email Design System

Premium dark-first email design. Every output should look considered and editorial -- not a template dump.

---

## Design Philosophy

Dark emails signal quality. SaaS founders, VPs, and operators live in dark IDEs, dark Notion, dark Slack. A dark newsletter matches their environment and stands out in an inbox of white-bg blasts. The goal is visual character: strong typographic hierarchy, editorial spacing, a single accent color that does real work.

Default: dark. Override: `tone=light` for consumer brands, formal industries, or user preference.

---

## Visual Anchor Rule

Every email must have ONE element with significantly higher visual weight than everything else. This is the thing that makes the email memorable.

**What qualifies as a visual anchor:**
- CTA callout card (`#D8F90A` full-width rounded card) -- strongest option, highest contrast on dark
- Stat callout with a striking number in 24px Instrument Serif italic
- Hero headline in 52px+ Instrument Serif (when the headline IS the story)
- Step cards section (when the numbered content is the primary value)

**What doesn't qualify:** A regular paragraph, a hero with a small button, generic unformatted text.

**Rule:** If you cannot identify the anchor before generating HTML, the structure is wrong. Add or promote the CTA callout card. An email without a visual anchor is a wall of text with branding.

---

## Color Tokens

### Dark (default)

```
Outer bg:         #050505
Container bg:     #111111
Header bg:        #0A0A0A
Alt section bg:   #161616   (subtle alternation for visual rhythm)
Elevated card bg: #1A1A1A   (stat callout, footer)
Footer bg:        #080808

Text primary:     #F2F2F2
Text body:        #CCCCCC
Text muted:       #888888
Text meta:        #555555

CTA primary bg:   #D8F90A   (yellow-green — REQUIRES #0A0A0A dark text)
CTA secondary bg: #FFFFFF   (white — #0A0A0A text)
CTA dark bg:      #111111   (inside yellow callout card — #F2F2F2 text)

Step badge bg:    #D8F90A   (numbered card badge)
Step badge text:  #0A0A0A

Divider:          #2A2A2A
Card border:      #222222
Brand strip:      [BRAND_COLOR] (2px line between header and hero)
```

### Light (fallback when tone=light)

```
Outer bg:         #F0F0EE
Container bg:     #FFFFFF
Header bg:        #1A1A1A   (always dark — anchors the email)
Alt section bg:   #F8F8F6
Footer bg:        #F8F8F6

Text primary:     #111111
Text body:        #444444
Text muted:       #888888

CTA primary bg:   #111111   (dark button on white)
Callout card bg:  #111111   (dark card on white email — reversal effect)

Divider:          #EEEEEE
```

---

## Brand Color Rules

When `brand_color` is provided:
- Use it for: brand strip (2px line), stat callout left border, category label text, step badge bg (if dark and readable), light-mode CTA button
- Do NOT use it for: body text, large bg sections (unless very dark and intentional)

**Luminance check for CTA button text:**
- Light brand color (luminance > 0.5 — yellows, greens, oranges, light purples): use `#0A0A0A` text
- Dark brand color (luminance < 0.4 -- navy, forest, dark purple): use `#FFFFFF` text

**Brand color on dark email:**
- If brand color is `#D8F90A` or similar bright/neon: perfect, use directly for CTA + badge
- If brand color is dark (e.g. `#1A3A5C`): do NOT use for CTA button -- use `#FFFFFF` CTA instead, use brand_color only for the 2px strip and stat border
- If brand color is `#856FE6` (purple): works on dark bg, use for strip + stat border + step badges; CTA stays `#D8F90A` for contrast

**Substitution in template:**
Replace every instance of `#D8F90A` in the dark template with brand_color IF brand_color is light enough (luminance > 0.4). Otherwise keep `#D8F90A` as CTA color and use brand_color only for accent elements.

---

## Typography

### Display (H1, H2)

**Font:** Instrument Serif, Georgia fallback

```css
font-family: 'Instrument Serif', Georgia, 'Times New Roman', serif;
font-weight: 400;   /* Instrument Serif is a display weight at 400 */
letter-spacing: -0.02em;
```

**Why Instrument Serif:** Elegant editorial serif. Renders beautifully at 40-60px. Georgia fallback is close enough in character -- editorial, serif, strong. The pairing with Inter body creates the same tension as print magazine design.

**Loading:**
```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

Gmail strips this `<link>` tag. Georgia renders instead. Both look good. Apple Mail, Yahoo, Outlook 365 keep the Google Font.

**H1 (hero headline):**
```
font-size: 60px  (4-5 words — push to poster scale)
font-size: 56px  (6-7 words — editorial authority)
font-size: 48px  (8 words)
font-size: 32px  (mobile fallback via @media)
line-height: 1.02
letter-spacing: -0.04em at 60px, -0.03em at 56px, -0.02em at 48px
```

Never size a headline down for safety. A bigger headline with tight tracking reads authoritative; a smaller headline reads like a template.

**H2 (section headline):**
```
font-size: 40px  (normal)
font-size: 52px  (CTA callout card -- bigger impact)
line-height: 1.05
```

### Body

**Font:** Inter, Arial fallback

```css
font-family: Inter, Arial, Helvetica, sans-serif;
```

**Body text (dark):**
```
font-size: 16-17px
line-height: 1.65-1.7
color: #CCCCCC
```

**Bold callouts:**
```html
<strong style="color:#F2F2F2;font-weight:600;">Key phrase</strong>
```
Use for the opening 3-4 words of each key idea.

**Meta / label text:**
```
font-size: 11px
font-weight: 600
letter-spacing: 0.14-0.22em
text-transform: uppercase
color: [BRAND_COLOR] or #555555
```

### Typography Nuances

**Italic variant for editorial emphasis:**
Instrument Serif has an italic variant (included in the Google Fonts URL). Use `font-style:italic` for:
- Stat callout quote text -- adds literary weight to a striking number or phrase
- Hero headline when tone is warm/founder
- Never on body copy -- italic at 16px is hard to read on dark backgrounds

```html
<p style="font-family:'Instrument Serif',Georgia,'Times New Roman',serif;font-style:italic;font-size:24px;font-weight:400;line-height:1.3;color:#F2F2F2;">"[STAT OR QUOTE]"</p>
```

**Letter-spacing rules:**
- Very large display (52px+): `-0.03em` (tighter = more editorial authority)
- Section headlines (38-40px): `-0.02em`
- Category label (11px uppercase): `0.22em` minimum, up to `0.30em` for wider/premium feel
- Body Inter: `0` -- never add tracking to body text

**Weight contrast rule:**
`'Instrument Serif' 400` + `Inter 700` (bold callouts) = correct pairing.
Never use Instrument Serif bold -- it's a display font; 400 is its designed weight.
Body Inter on dark: color `#CCCCCC` (not `#888888` -- that's muted/meta only).

---

## Spacing Rhythm

| Location | Padding |
|---|---|
| Section (standard) | 40px top/bottom, 40px left/right |
| Hero section | 64px top, 56px bottom, 40px sides |
| CTA callout card | 52px top/bottom, 40px sides |
| Footer | 44px top, 52px bottom, 40px sides |
| Between body paragraphs | 20px margin-bottom |
| After H2 before content | 24-32px padding |
| Step card gap | 20px margin-bottom per card |
| Container max-width | 600px |

Mobile (max-width 600px): reduce side padding to 24px via @media.

**Valid spacing values (rhythm scale):** 8 / 16 / 20 / 24 / 32 / 40 / 52 / 64px.
Never use arbitrary values like 18px, 22px, 30px, 45px. They break visual rhythm and signal template output.

---

## Section Patterns

### Header
Dark `#0A0A0A` bg always. Brand name in Instrument Serif left. Issue + date in small Inter uppercase right. Followed immediately by a 2px brand color strip.

```html
<tr>
  <td bgcolor="#0A0A0A" style="background-color:#0A0A0A;padding:20px 40px;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
      <tr>
        <td style="font-family:'Instrument Serif',Georgia,serif;font-size:20px;font-weight:400;color:#F2F2F2;letter-spacing:-0.01em;">[BRAND NAME]</td>
        <td align="right" style="font-family:Inter,Arial,sans-serif;font-size:11px;font-weight:500;color:#555555;letter-spacing:0.14em;text-transform:uppercase;white-space:nowrap;">Issue #[N] &nbsp;|&nbsp; [DATE]</td>
      </tr>
    </table>
  </td>
</tr>
<tr>
  <td bgcolor="#D8F90A" style="background-color:#D8F90A;height:2px;font-size:1px;line-height:1px;">&nbsp;</td>
</tr>
```

### Hero
52px Instrument Serif headline. Category label above in brand color uppercase. Inter hook paragraph below. Pill CTA button (border-radius:100px).

H1 word count → font size:
- 5 words or fewer: 56px
- 6-7 words: 52px
- 8 words: 44px

CTA pill button shape (border-radius:100px) is the hero CTA. Rectangular button (border-radius:8px) is used in secondary CTA sections.

### Divider
Centered 96px rule. `#2A2A2A` on dark, `#EEEEEE` on light. Adds visual rhythm between sections.

```html
<tr>
  <td bgcolor="#111111" style="background-color:#111111;padding:40px 40px 0;">
    <table width="96" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
      <tr>
        <td bgcolor="#2A2A2A" style="background-color:#2A2A2A;height:1px;font-size:1px;line-height:1px;">&nbsp;</td>
      </tr>
    </table>
  </td>
</tr>
```

### Stat Callout
`#1A1A1A` elevated card bg. 3px brand color left border. Instrument Serif quote at 24px. Attribution in small Inter.

The callout sits on `#111111` outer padding -- the slight elevation (#1A1A1A vs #111111) creates depth without needing a visible border.

### Numbered Step Cards
Badge: 28x28 `#D8F90A` square, `border-radius:6px`. Number in 11px Inter bold `#0A0A0A`. Text cell: 16px Inter `#E8E8E8`. Each step is its own `<table>` with `margin-bottom:20px`.

This pattern replaces bullet lists. It looks significantly better and draws the eye through sequential content.

### CTA Callout Card
The visual anchor. `#D8F90A` background, `border-radius:14px`, generous padding (52px). H2 in Instrument Serif at 40-52px, `color:#1A1A1A`. Dark `#111111` button inside.

The yellow card inverts the dark email's color relationship -- it's the one bright element, which makes it unmissable as the primary action.

### Footer
`#080808` bg (slightly different from container `#111111` -- creates visual separation). Brand name in Instrument Serif. Company info in small Inter. 96px divider rule. Unsubscribe links.

---

## Tone Variants

### dark (default)
- Container: `#111111`
- Hero bg: `#111111`
- Text: `#F2F2F2` / `#CCCCCC`
- CTA: `#D8F90A` pill button (dark text)
- Use for: SaaS, tech, founders, operators, B2B

### light (fallback)
- Container: `#FFFFFF`
- Header: stays dark `#1A1A1A` (anchors the email)
- Text: `#111111` / `#444444`
- CTA: `#111111` rectangular button (white text)
- Callout card: dark `#111111` card (inverted)
- Use for: consumer brands, formal B2B, healthcare, finance

Trigger light mode: user sets `tone=light` or `tone=formal` or specifies "white background".

---

## Email Client Behavior

| Client | Instrument Serif | Dark bg renders | `@media` |
|---|---|---|---|
| Gmail (web) | No -- falls back to Georgia | Yes | Yes |
| Gmail app (iOS/Android) | No | Yes | Partial |
| Apple Mail | Yes | Yes | Yes |
| Outlook 2019+ | Yes (via Google Fonts CDN) | Yes | No |
| Outlook 2016 | No | May invert colors | No |
| Yahoo Mail | Yes | Yes | Yes |

**Outlook 2016 dark inversion:** Outlook 2016 may invert dark backgrounds to white. Add `<!--[if mso]>` conditional to force dark bg for Outlook if needed. For modern SaaS audiences, Outlook 2016 represents < 5% of opens -- acceptable tradeoff.

---

## Email Slop Patterns to Avoid

These produce generic AI-looking output. Check the self-QA checklist against these before saving.

| Pattern | What it signals | Fix |
|---|---|---|
| White background + colored button | Safe, corporate, forgettable | Use dark template (default) |
| Centered hero text on gradient | Stock newsletter look | Left-aligned hero on `#111111` |
| All-Inter / all-Arial, no display font | No typographic character | Instrument Serif on H1 is non-negotiable |
| No visual anchor -- every section same weight | Wall of text with branding | Identify and elevate the anchor (CTA card, stat callout, or oversized hero) |
| Brand color on 4+ elements | Garish / over-branded | Max 3 accent uses: strip, stat border, category label |
| Bullet lists everywhere | Undesigned content dump | Step cards replace bullets; bold callouts open paragraphs |
| Generic CTA copy ("Click here", "Learn more") | AI filler | 3-5 word action + benefit ("Save My Seat", "Read the Full Breakdown") |
| Footer larger than 3 lines | Compliance dump, reader ignores | Brand name + company line + rule + unsubscribe link. That's it. |

---

## Custom Generation Guide

When template doesn't fit Step 2 answers, generate from scratch using these tokens.

### Background tokens

```
User says "dark":       outer #050505, container #111111, header #0A0A0A, footer #080808
User says "light":      outer #F0F0EE, container #FFFFFF, header #1A1A1A, footer #F8F8F6
User provides hex:      use provided hex for container, darken ~10% for header, lighten ~5% for alt sections
                        If hex is dark (<30% luminance): light text #F2F2F2
                        If hex is light (>70% luminance): dark text #111111
                        If hex is mid: test contrast ratio, pick text accordingly
```

### Font tokens

```
User says "editorial serif":  'Instrument Serif',Georgia,'Times New Roman',serif (display)
                               Inter,Arial,Helvetica,sans-serif (body)
User says "modern sans":       'DM Sans',Arial,Helvetica,sans-serif (display, load from Google Fonts)
                               Inter,Arial,Helvetica,sans-serif (body)
User says "system fonts":      -apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif (both)
```

### Button style tokens

```
User says "pill":            border-radius:100px
User says "softly rounded":  border-radius:10px
User says "sharp":           border-radius:0 (or 2px for sub-pixel rendering)
```

### Accent color tokens

```
User provides accent:     use for brand strip, CTA button, step badges, stat border
                          text on accent: #0A0A0A if luminance >0.4, #FFFFFF if luminance <0.4
User says "keep default": #D8F90A with #0A0A0A text
User says "minimal/none": #FFFFFF CTA on dark, #111111 CTA on light
```

---

## What NOT to Use

In inline styles, never:
- `display:flex` / `display:grid`
- `position:absolute/relative`
- `float:`
- CSS custom properties (`--var`)
- `min-height:` / `max-height:`
- `background-image:` (Outlook strips it)
- `border-radius` on `<table>` elements (use on `<td>` only)
- `rgba()` colors (use solid hex equivalents)
- `linear-gradient` (Outlook renders as solid block)
