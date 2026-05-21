# Style Presets

8 business-oriented style presets. Each is fully self-contained -- complete CSS token set, no "derive from" chains.

Choose based on purpose and audience. When in doubt: clean-slate for sales, midnight-editorial for investor, matt-gray for internal.

---

## 1. midnight-editorial

**Best for:** Investor decks, premium B2B, thought leadership presentations
**Feeling:** Editorial authority, premium, considered

```
Background:       #0A0A0A outer / #111111 slide / #1A1A1A elevated cards / #080808 footer
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

Display weight:   400 (Instrument Serif is a display weight at 400)
Body weight:      400 / 600 (bold callouts)
```

**Signature elements:**
- Thin `<hr>` separators between content blocks (`border: none; border-top: 1px solid #2A2A2A; width: 40px; margin: 0`)
- Oversized section numbers at `opacity: 0.08` as absolute background elements
- Instrument Serif italic on quote-callout slides (adds literary weight)
- stat-highlight numbers in `#D8F90A` accent color
- section-divider bg: `#D8F90A` with `#0A0A0A` text (full inversion)

**Background depth via section alternation:**
- Header / opening slides: `#0A0A0A`
- Main content slides: `#111111`
- Elevated cards (stats, callouts): `#1A1A1A`
- Closing slide: `#D8F90A` full bg with dark text

---

## 2. matt-gray

**Best for:** Internal decks, operational reviews, professional presentations to mixed audiences
**Feeling:** Safe, professional, accessible, clean

```
Background:       #F5F5F5 outer / #FFFFFF slide / #EEEEEE section alt / #F8F8F8 footer
Text primary:     #1A1A1A
Text secondary:   #444444
Text muted:       #888888
Accent:           #2563EB  (blue)
Accent text:      #FFFFFF  (white text on accent)
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
- 4px left border on section-divider and section heading elements (`border-left: 4px solid #2563EB; padding-left: 1rem`)
- Subtle drop shadow on stat-highlight cards
- Stat numbers in accent blue
- section-divider: `#EEEEEE` background (slight contrast from main white), left-border accent treatment
- Clean rectangular buttons if any CTAs (`border-radius: 6px`)

---

## 3. clean-slate

**Best for:** Sales decks, customer-facing presentations, any audience that expects professionalism
**Feeling:** Trustworthy, clear, confident, enterprise-safe

```
Background:       #FFFFFF outer / #FFFFFF slide / #F8F8F8 alt sections / #F4F4F4 footer
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
- Rounded card containers on all callout elements (`border-radius: 16px`)
- Badge pills for category labels and key points (`border-radius: 100px; background: #E0F2FE; color: #0F172A; padding: 0.2em 0.8em`)
- Generous whitespace -- padding toward the maximum of each `clamp()` range
- stat-highlight: dark `#0F172A` numbers on white background (high contrast, no color distraction)
- section-divider: dark `#111111` background (inverts the white deck)
- closing-cta: `#0F172A` full bg with white text

---

## 4. brutalist

**Best for:** Startup pitches, design-forward tech audiences, conference talks with strong POV
**Feeling:** Direct, raw, confident, uncompromising

```
Background:       #FFFFFF outer / #FFFFFF slide
Text primary:     #000000
Text secondary:   #333333
Accent:           #FF3300  (red) or #FFE500 (yellow)
Accent text:      #000000  (both red and yellow are light enough for dark text)
Divider:          #000000  (solid black)
Border:           3px solid #000000  (heavy)
Border-radius:    0 (zero everywhere -- no rounded corners)

Display font:     'Archivo Black', Arial Black, Arial, sans-serif
Body font:        'Space Grotesk', Arial, sans-serif
Google Fonts:     https://fonts.googleapis.com/css2?family=Archivo+Black&family=Space+Grotesk:wght@400;500;700&display=swap

Display weight:   900
Body weight:      400 / 700
```

**Signature elements:**
- Heavy borders everywhere: `border: 3px solid #000000` on cards, tables, section elements
- Zero border-radius on all elements -- absolute rule for this style
- Oversized section numbers in accent color (`font-size: clamp(6rem, 15vw, 12rem); opacity: 1` -- fully visible, not ghosted)
- section-divider: accent color full background (`#FF3300` or `#FFE500`) with black text
- stat-highlight: numbers in accent color, extreme size
- comparison-table: bold black borders, no row alternation -- raw grid

**DO NOT apply rounded corners, gradients, or drop shadows to brutalist decks. The aesthetic requires hard edges.**

---

## 5. mint-pixel-corporate

**Best for:** SaaS sales, product demos, tech company pitches, growth-stage startups
**Feeling:** Fresh, modern, startup-professional

```
Background:       #F0FAF7 outer / #FFFFFF slide / #E8F5F0 alt sections / #F0FAF7 footer
Text primary:     #1A2E2A
Text secondary:   #4A6B62
Text muted:       #7A9B92
Accent:           #00B894  (mint)
Accent text:      #1A2E2A  (dark text on mint)
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
- CSS `radial-gradient` dot pattern on section-divider slides:
  ```css
  background-image: radial-gradient(circle, #00B894 1px, transparent 1px);
  background-size: 24px 24px;
  background-color: #1A2E2A;
  ```
- Mint accent pills for feature highlights (`border-radius: 100px; background: #00B894; color: #1A2E2A; padding: 0.15em 0.75em; font-size: clamp(0.65rem, 1vw, 0.8rem)`)
- Screenshot frames with mint border (`border: 2px solid #00B894; border-radius: 8px`)
- section-divider: dark `#1A2E2A` background with dot pattern + mint text
- stat-highlight: mint numbers on white background

---

## 6. product-minimal

**Best for:** Product demos, feature showcases, design system presentations, design-forward audiences
**Feeling:** Maximum whitespace, purposeful restraint, design system precision

```
Background:       #FAFAFA outer / #FAFAFA slide / #F4F4F4 alt / #F0F0F0 footer
Text primary:     #18181B
Text secondary:   #71717A
Text muted:       #A1A1AA
Accent:           #8B5CF6  (violet)
Accent text:      #FFFFFF  (white on violet)
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
- Single accent element per slide rule: the accent color (`#8B5CF6`) appears in AT MOST ONE place per slide -- this creates intentional scarcity that reads premium
- Subtle CSS drop shadow on cards: `box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08)` -- barely visible, adds depth
- Very generous padding (use maximum clamp values)
- stat-highlight: violet stat numbers with a thin violet top-border on each stat card
- section-divider: `#18181B` full bg with Syne display font + white text
- closing-cta: violet background (`#8B5CF6`) with white text

---

## 7. magazine-red

**Best for:** Marketing campaign reviews, brand presentations, bold internal reporting, conference openers
**Feeling:** Authoritative, editorial, high energy, unmissable

```
Background:       #1A1A1A outer / #111111 slide / #1E1E1E alt / #0D0D0D footer
Text primary:     #FFFFFF
Text secondary:   #CCCCCC
Text muted:       #888888
Accent:           #E63329  (red)
Accent secondary: #FFFFFF
Divider:          #2A2A2A

Display font:     'Fraunces', Georgia, 'Times New Roman', serif
Body font:        'Work Sans', Arial, Helvetica, sans-serif
Google Fonts:     https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,900;1,900&family=Work+Sans:wght@400;500;600&display=swap

Display weight:   900
Body weight:      400 / 500
```

**Signature elements:**
- 8px full-width horizontal red band: `<div style="width:100%; height:8px; background:#E63329; margin: clamp(1rem, 2vw, 2rem) 0">` used as visual separator
- Editorial section numbers in red, visible opacity (`opacity: 0.3` -- not fully ghosted like midnight-editorial)
- quote-callout slides: INVERTED to white background with dark text (the only white slide in the deck)
  ```css
  .slide--quote-callout { background: #FFFFFF; color: #111111; }
  ```
- Fraunces italic for quote text: extreme editorial weight
- stat-highlight: red accent numbers, large
- closing-cta: full red background (`#E63329`) with white text

---

## 8. soft-cloud

**Best for:** Onboarding decks, customer education, approachable SaaS, HR/people presentations
**Feeling:** Friendly, accessible, soft, welcoming -- high trust, low intimidation

```
Background:       #EEF2FF outer / #FFFFFF slide / #F5F3FF alt / #EEF2FF footer
Text primary:     #1E1B4B
Text secondary:   #4C4A7B
Text muted:       #9896C0
Accent:           #6366F1  (indigo)
Accent light:     #E0E7FF  (light indigo for card backgrounds)
Accent text:      #FFFFFF
Divider:          #DDD6FE
Card radius:      24px  (soft, generous)
Card shadow:      0 4px 16px rgba(99, 102, 241, 0.08)

Display font:     'Outfit', Arial, Helvetica, sans-serif
Body font:        'Outfit', Arial, Helvetica, sans-serif
Google Fonts:     https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap

Display weight:   700
Body weight:      400 / 500
```

**Signature elements:**
- Generous border-radius everywhere: `border-radius: 24px` on all cards, callout blocks, stat containers
- Gradient section-dividers:
  ```css
  background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 50%, #DDD6FE 100%);
  ```
- Badge pills on key points: `border-radius: 100px; background: #E0E7FF; color: #6366F1; padding: 0.2em 0.9em`
- stat-highlight: stat numbers in indigo on `#F5F3FF` elevated card background
- All `<hr>` dividers: `border-color: #DDD6FE` (matches the soft palette)
- closing-cta: indigo gradient background
  ```css
  background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
  ```

---

## DO NOT USE -- Style Slop Checklist

Before outputting any HTML, verify none of these are present:

| Pattern | Why it's wrong |
|---|---|
| Inter as display font | Zero typographic character -- reads as default AI output |
| Purple-to-blue gradient on white background | Most overused "modern" AI aesthetic -- immediately signals undesigned |
| Every slide centered with the same layout | No typographic thinking, looks like a PowerPoint default theme |
| Identical slide backgrounds throughout | No visual rhythm -- the deck reads as one long scroll |
| `box-shadow` on everything | Overused "depth" signal that adds no real depth |
| `border-radius: 8px` on everything (even brutalist) | Softening that fights the style's aesthetic intent |
| Accent color on 5+ elements per slide | Over-branded, destroys scarcity = destroys premium feel |
| Helvetica Neue / Arial as display font | Generic -- no personality at display size |
| Stat numbers at body text size | Doesn't understand the stat-highlight layout's purpose |
| "Thank You" as closing slide | Missed the closing-cta layout's entire purpose |
