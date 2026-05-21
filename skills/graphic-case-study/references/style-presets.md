# Style Presets — graphic-case-study

9 business-oriented style presets. Each is fully self-contained -- complete CSS token set, no "derive from" chains.

Choose based on the vendor's brand and audience. When in doubt: clean-slate for enterprise B2B, midnight-editorial for tech/AI companies, warm-earth for agencies and services.

---

## 1. clean-slate

**Best for:** Enterprise B2B, sales teams, customer-facing materials, any audience that expects professionalism
**Feeling:** Trustworthy, clear, confident, enterprise-safe

```
Background:       #FFFFFF outer / #FFFFFF page / #F8F8F8 alt sections / #F4F4F4 footer
Text primary:     #111111
Text secondary:   #555555
Text muted:       #999999
Accent:           #0F172A  (near-black navy)
Accent light:     #E0F2FE  (light blue for pill/badge backgrounds)
Accent text:      #FFFFFF
Divider:          #E8E8E8
Card border:      #E0E0E0
Card radius:      16px
Card shadow:      0 2px 8px rgba(0, 0, 0, 0.06)

Display font:     'Plus Jakarta Sans', Arial, Helvetica, sans-serif
Body font:        'Plus Jakarta Sans', Arial, Helvetica, sans-serif
Google Fonts:     https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;800&display=swap

Display weight:   800
Body weight:      400 / 500
```

**Signature elements:**
- Rounded card containers (`border-radius: 16px`) on all fact cells, feature cards, stat containers
- Badge pills for category labels (`border-radius: 100px; background: #E0F2FE; color: #0F172A; padding: 0.2em 0.8em`)
- Generous whitespace -- push toward maximum clamp values
- Hero stat in dark `#0F172A` (high contrast, authoritative -- no color distraction)
- Cover background: `#0F172A` full dark (inversion for premium feel)
- Closing CTA: `#0F172A` full bg with white headline and white CTA

---

## 2. midnight-editorial

**Best for:** Tech, AI, developer-focused companies, premium B2B, thought leadership
**Feeling:** Editorial authority, premium, considered

```
Background:       #0A0A0A outer / #111111 page / #1A1A1A elevated cards / #080808 footer
Text primary:     #F2F2F2
Text secondary:   #AAAAAA
Text muted:       #555555
Accent:           #D8F90A  (yellow-green)
Accent text:      #0A0A0A  (dark text on accent)
Divider:          #2A2A2A
Card border:      #222222

Display font:     'Instrument Serif', Georgia, 'Times New Roman', serif
Body font:        Inter, Arial, Helvetica, sans-serif
Google Fonts:     https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&display=swap

Display weight:   400
Body weight:      400 / 600
```

**Signature elements:**
- Thin `<hr>` separators (`border: none; border-top: 1px solid #2A2A2A; width: 40px; margin: 0`)
- Oversized section numbers at `opacity: 0.06` as absolute background elements
- Instrument Serif italic on testimonial quotes (literary weight)
- Hero stat number in `#D8F90A` accent
- Cover: `#D8F90A` full-bg inversion with `#0A0A0A` text (unmissable)
- Closing CTA: `#D8F90A` full bg with `#0A0A0A` text

---

## 3. matt-gray

**Best for:** Internal business reviews, board materials, professional presentations to mixed audiences
**Feeling:** Safe, professional, accessible, clean

```
Background:       #F5F5F5 outer / #FFFFFF page / #EEEEEE section alt / #F8F8F8 footer
Text primary:     #1A1A1A
Text secondary:   #444444
Text muted:       #888888
Accent:           #2563EB  (blue)
Accent text:      #FFFFFF
Divider:          #E5E5E5
Card border:      #DDDDDD
Card shadow:      0 1px 3px rgba(0, 0, 0, 0.08)

Display font:     'DM Sans', Arial, Helvetica, sans-serif
Body font:        'DM Sans', Arial, Helvetica, sans-serif
Google Fonts:     https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;800&display=swap

Display weight:   700
Body weight:      400 / 500
```

**Signature elements:**
- 4px left border on section headings and fact cells (`border-left: 4px solid #2563EB; padding-left: 1rem`)
- Subtle drop shadow on stat containers
- Hero stat in accent blue `#2563EB`
- Section headings use `#EEEEEE` alt background
- Closing CTA: `#1A1A1A` full dark bg with white text and blue button

---

## 4. brutalist

**Best for:** Standout sales materials, design-forward agencies, brands that want to be remembered
**Feeling:** Direct, raw, confident, uncompromising

```
Background:       #FFFFFF outer / #FFFFFF page
Text primary:     #000000
Text secondary:   #333333
Accent:           #FF3300  (red) or #FFE500 (yellow)
Accent text:      #000000
Divider:          #000000  (solid black)
Border:           3px solid #000000  (heavy)
Border-radius:    0  (zero everywhere -- absolute rule)

Display font:     'Archivo Black', Arial Black, Arial, sans-serif
Body font:        'Space Grotesk', Arial, sans-serif
Google Fonts:     https://fonts.googleapis.com/css2?family=Archivo+Black&family=Space+Grotesk:wght@400;500;700&display=swap

Display weight:   900
Body weight:      400 / 700
```

**Signature elements:**
- Heavy borders everywhere: `border: 3px solid #000000` on ALL cards, tables, containers, page sections
- Zero border-radius on every element -- this is a hard rule, never soften
- Oversized section numbers fully visible (`opacity: 1`) in accent color
- Cover: accent color full bg (`#FF3300` or `#FFE500`) with `#000000` text
- Hero stat in accent color, extreme size
- Closing CTA: `#000000` full bg with white text and accent-color button/border

**DO NOT apply rounded corners, gradients, or drop shadows to brutalist case studies.**

---

## 5. mint-pixel-corporate

**Best for:** SaaS sales, product-focused companies, tech startups, growth-stage B2B
**Feeling:** Fresh, modern, startup-professional

```
Background:       #F0FAF7 outer / #FFFFFF page / #E8F5F0 alt sections / #F0FAF7 footer
Text primary:     #1A2E2A
Text secondary:   #4A6B62
Text muted:       #7A9B92
Accent:           #00B894  (mint)
Accent text:      #1A2E2A
Divider:          #D1E8E1
Card border:      #C5DFD7
Card radius:      10px

Display font:     'Manrope', Arial, Helvetica, sans-serif
Body font:        'Manrope', Arial, Helvetica, sans-serif
Google Fonts:     https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;800&display=swap

Display weight:   800
Body weight:      400 / 500
```

**Signature elements:**
- Mint accent pills for feature labels and category tags (`border-radius: 100px; background: #00B894; color: #1A2E2A`)
- CSS `radial-gradient` dot pattern on cover background:
  ```css
  background-image: radial-gradient(circle, #00B894 1px, transparent 1px);
  background-size: 24px 24px;
  background-color: #1A2E2A;
  ```
- Hero stat in mint `#00B894`
- Feature cards with mint border (`border: 2px solid #00B894`)
- Closing CTA: `#1A2E2A` dark bg with dot pattern + mint text and white button

---

## 6. product-minimal

**Best for:** Product companies, design-forward B2B, companies presenting to design-savvy buyers
**Feeling:** Maximum whitespace, purposeful restraint, design system precision

```
Background:       #FAFAFA outer / #FAFAFA page / #F4F4F4 alt / #F0F0F0 footer
Text primary:     #18181B
Text secondary:   #71717A
Text muted:       #A1A1AA
Accent:           #8B5CF6  (violet)
Accent text:      #FFFFFF
Divider:          #E4E4E7
Card shadow:      0 1px 3px rgba(0, 0, 0, 0.08)
Card radius:      12px

Display font:     'Syne', Arial, Helvetica, sans-serif
Body font:        'IBM Plex Sans', Arial, Helvetica, sans-serif
Google Fonts:     https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=IBM+Plex+Sans:wght@400;500;600&display=swap

Display weight:   700-800
Body weight:      400 / 500
```

**Signature elements:**
- Single accent element per section rule: violet appears in AT MOST ONE element per section
- Subtle CSS drop shadow on cards (`box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08)`)
- Very generous padding (use maximum clamp values everywhere)
- Hero stat in violet `#8B5CF6` with thin violet top-border on stat container
- Cover: `#18181B` full dark bg with Syne display font in white
- Closing CTA: violet background (`#8B5CF6`) with white text

---

## 7. magazine-red

**Best for:** Marketing agencies, bold companies, brand-forward case studies, attention-commanding materials
**Feeling:** Authoritative, editorial, high energy

```
Background:       #1A1A1A outer / #111111 page / #1E1E1E alt / #0D0D0D footer
Text primary:     #FFFFFF
Text secondary:   #CCCCCC
Text muted:       #888888
Accent:           #E63329  (red)
Divider:          #2A2A2A

Display font:     'Fraunces', Georgia, 'Times New Roman', serif
Body font:        'Work Sans', Arial, Helvetica, sans-serif
Google Fonts:     https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,900;1,900&family=Work+Sans:wght@400;500;600&display=swap

Display weight:   900
Body weight:      400 / 500
```

**Signature elements:**
- 8px full-width red band separator: `<div style="width:100%; height:8px; background:#E63329; margin: clamp(1rem, 2vw, 2rem) 0">`
- Editorial section numbers at `opacity: 0.25` in red
- Testimonial section inverted to white bg with dark text (only white section in the deck)
- Fraunces italic for quote text (extreme editorial weight)
- Hero stat in red `#E63329`, large
- Closing CTA: full red background (`#E63329`) with white text

---

## 8. soft-cloud

**Best for:** Onboarding materials, customer education, HR/people companies, approachable SaaS
**Feeling:** Friendly, accessible, soft, welcoming

```
Background:       #EEF2FF outer / #FFFFFF page / #F5F3FF alt / #EEF2FF footer
Text primary:     #1E1B4B
Text secondary:   #4C4A7B
Text muted:       #9896C0
Accent:           #6366F1  (indigo)
Accent light:     #E0E7FF  (light indigo for card backgrounds)
Accent text:      #FFFFFF
Divider:          #DDD6FE
Card radius:      24px
Card shadow:      0 4px 16px rgba(99, 102, 241, 0.08)

Display font:     'Outfit', Arial, Helvetica, sans-serif
Body font:        'Outfit', Arial, Helvetica, sans-serif
Google Fonts:     https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap

Display weight:   700
Body weight:      400 / 500
```

**Signature elements:**
- Generous border-radius (`border-radius: 24px`) on all cards, callout blocks, stat containers
- Gradient section backgrounds: `linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 50%, #DDD6FE 100%)`
- Badge pills on key points (`border-radius: 100px; background: #E0E7FF; color: #6366F1`)
- Hero stat in indigo `#6366F1` on `#F5F3FF` elevated card bg
- Closing CTA: indigo gradient (`linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)`) with white text

---

## 9. warm-earth (case-study-exclusive)

**Best for:** Agencies, consultancies, service businesses, health/education tech, companies that sell on trust
**Feeling:** Trusted, grounded, human, warm authority

```
Background:       #FDF6EF outer / #FFFFFF page / #FAF0E4 alt sections / #F5EBD8 footer
Text primary:     #2C1A0E
Text secondary:   #6B4C30
Text muted:       #A08060
Accent:           #D4622A  (burnt orange)
Accent light:     #FDE8D8  (peach -- for pill/badge backgrounds)
Accent text:      #FFFFFF
Divider:          #E8D5BF
Card border:      #E0C9A8
Card radius:      10px
Card shadow:      0 2px 8px rgba(44, 26, 14, 0.06)

Display font:     'Lora', Georgia, 'Times New Roman', serif
Body font:        'Source Sans 3', Arial, Helvetica, sans-serif
Google Fonts:     https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700&family=Source+Sans+3:wght@400;600&display=swap

Display weight:   700
Body weight:      400 / 600
```

**Signature elements:**
- Warm off-white background (`#FDF6EF`) -- not pure white, not gray. The warmth starts with the canvas.
- Accent pills in peach (`background: #FDE8D8; color: #D4622A; border-radius: 100px`) for category labels
- **Drop cap on challenge page opening paragraph:**
  ```css
  .challenge-context::first-letter {
    font-family: 'Lora', Georgia, serif;
    font-size: clamp(3rem, 7vw, 5rem);
    float: left;
    margin: 0.05em 0.12em 0 0;
    color: var(--accent);
    line-height: 0.8;
  }
  ```
- Hero stat in burnt orange `#D4622A`
- Section headings: `border-left: 4px solid #D4622A; padding-left: 1rem` (no full-background inversion -- subtle accent)
- Cover: warm-dark background `#2C1A0E` with off-white text `#F5EBD8` and burnt-orange accent label
- Closing CTA: `#2C1A0E` full dark bg with `#FDE8D8` peach headline, white CTA button with burnt orange border

---

## DO NOT USE -- Style Slop Checklist

Before outputting any HTML, verify none of these are present:

| Pattern | Why it's wrong |
|---|---|
| Inter as display font | Zero typographic character -- reads as default AI output |
| Purple-to-blue gradient on white background | Most overused AI aesthetic -- immediately signals undesigned |
| Every section same background color | No visual rhythm -- the PDF reads as one flat block |
| Identical section layouts throughout | No typographic thinking -- copy-pasted template feel |
| `box-shadow` on everything | Overused "depth" signal with no real depth |
| `border-radius: 8px` on everything (especially brutalist) | Softening that fights the style's aesthetic intent |
| Accent color on 5+ elements per section | Over-branded, destroys scarcity = destroys premium feel |
| Helvetica Neue / Arial as display font | Generic -- no personality at display size |
| Stat numbers at body text size | Breaks the entire purpose of the results section |
| "Thank You" as closing-cta headline | No action, no contact info = completely wasted page |
| Logo placeholder box with no styling | Unfinished -- use CSS initials at minimum |
