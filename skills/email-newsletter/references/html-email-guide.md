# HTML Email Guide

Rules for writing HTML that renders correctly in Gmail, Apple Mail, Outlook, Samsung Mail, and Yahoo Mail.

---

## The One Rule

**Inline styles only.** No `<style>` blocks, no `<link>` to external CSS, no CSS classes. Every element that needs styling gets `style=""` directly on the tag. Email clients strip `<style>` blocks (especially Gmail on Android) and ignore class-based rules entirely.

Exception: `@media` queries for mobile responsiveness can go in a `<head>` `<style>` block -- but always include inline fallbacks so the layout works without them.

---

## Layout: Table-Based Only

Use `<table>` for layout. Not `<div>`, not flexbox, not grid. Outlook renders HTML as if it's Microsoft Word, and Word does not understand modern CSS layout.

### Outer wrapper pattern

```html
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F4F4F4;">
  <tr><td align="center" style="padding:24px 16px;">

    <!-- 600px container -->
    <table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#FFFFFF;">
      <!-- sections go here as <tr><td> blocks -->
    </table>

  </td></tr>
</table>
```

Always use both `width="600"` (HTML attribute) and `max-width:600px` (inline style). The attribute handles Outlook; the style handles everything else.

### Required table attributes

Every `<table>` needs all three:
```html
<table cellpadding="0" cellspacing="0" border="0">
```

Missing any of these adds default spacing or borders that break layout.

---

## Typography

**Font stack (always use system fonts with web-safe fallbacks):**

For sans-serif:
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, Helvetica, sans-serif;
```

For serif (headlines only):
```css
font-family: Georgia, 'Times New Roman', Times, serif;
```

**Web fonts (optional, with caveats):**
- Declare in `<head>` `<style>` block using `@import` or `<link>`
- Always include a web-safe fallback -- Gmail strips web font declarations
- Never rely on a web font being rendered -- design so the fallback looks good

**Type scale:**
- H1 (hero): 28-36px, font-weight 700, line-height 1.2
- H2 (section headers): 20-24px, font-weight 600, line-height 1.3
- Body: 15-16px, line-height 1.6-1.7, color #333333 or #444444
- Small/meta: 12-13px, color #888888

**Always set:**
```css
font-size: [px];
line-height: [number];
color: [hex];
font-family: [stack];
```

On every text element. Do not rely on inheritance -- email clients do not inherit styles reliably.

---

## Images

Every image:
```html
<img src="[hosted-url]" alt="[descriptive text]" width="600" border="0" style="display:block;max-width:100%;border:0;">
```

Rules:
- `display:block` removes bottom gap (inline images add ~4px gap below)
- `border="0"` (HTML attribute) + `border:0` (inline style) -- need both for Outlook
- Always hosted URL -- base64 images are often blocked by spam filters
- `max-width:100%` for mobile responsiveness
- Always fill in `alt` -- many clients block images by default, alt text is what readers see first

For full-width hero images:
```html
<img src="[url]" alt="" width="600" border="0" style="display:block;max-width:100%;width:100%;height:auto;border:0;">
```

---

## CTA Buttons

**Never** use a simple `<a>` tag with `display:block` and background color for buttons. Outlook ignores `display:block` on `<a>` tags.

**Always** use the table+td structure:

```html
<table cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td align="center" bgcolor="#1A1A1A" style="background-color:#1A1A1A;border-radius:6px;">
      <a href="[CTA_URL]" target="_blank" style="display:inline-block;padding:14px 32px;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:600;color:#FFFFFF;text-decoration:none;letter-spacing:0.01em;">Button Text Here</a>
    </td>
  </tr>
</table>
```

Notes:
- `bgcolor=` HTML attribute + `background-color:` inline style -- need both for Outlook
- `border-radius` on `<td>` -- Outlook ignores it on `<a>`
- `display:inline-block` on `<a>` is fine (it's not a layout block, just expands the click area)

---

## Colors and Backgrounds

Always use both the HTML attribute and inline style for backgrounds:

```html
<td bgcolor="#FFFFFF" style="background-color:#FFFFFF;">
```

Outlook uses `bgcolor` attribute; other clients use the inline style.

**Dark backgrounds:**
Use `bgcolor="#1A1A1A"` (safe dark) or `bgcolor="#000000"`. Avoid pure black text on very dark backgrounds -- use `#FFFFFF` or `#F0F0F0` for text on dark.

---

## Spacing

Use `padding` on `<td>` elements, not margins. `margin` on table cells behaves unpredictably across clients.

Standard section padding: `padding:40px 32px`
Content padding (narrower): `padding:24px 32px`
Header/footer padding: `padding:20px 32px`

For vertical spacing between elements, use empty `<tr><td style="height:16px;font-size:1px;line-height:1px;">&nbsp;</td></tr>` rows in Outlook-heavy sends. For most modern clients, `padding-bottom` on the previous `<td>` is enough.

---

## Mobile Responsiveness

Minimal media query approach (add to `<head>` style block):

```html
<style>
  @media only screen and (max-width: 600px) {
    .container { width: 100% !important; max-width: 100% !important; }
    .stack { display: block !important; width: 100% !important; }
    .hide-mobile { display: none !important; }
    h1 { font-size: 26px !important; }
    td { padding-left: 20px !important; padding-right: 20px !important; }
  }
</style>
```

Always set inline fallbacks -- treat media queries as an enhancement, not a requirement.

---

## Dark Mode

Some clients (Apple Mail, Gmail Android) support dark mode. Add to `<head>` style block:

```html
<style>
  @media (prefers-color-scheme: dark) {
    .dark-bg { background-color: #1A1A1A !important; }
    .dark-text { color: #F0F0F0 !important; }
  }
</style>
```

Most clients will ignore this. It is a progressive enhancement. Do not rely on it for readability -- ensure the light mode version is always readable.

---

## What to Avoid

Never use in inline styles:
- `display: flex` / `display: grid` -- not supported in Outlook
- `position: absolute/relative/fixed` -- breaks table layout
- `float:` -- unreliable across clients
- CSS custom properties (`--variable`) -- Outlook does not support
- `min-height:` / `max-height:` -- Outlook ignores
- `background-image:` CSS property -- Outlook strips it (use VML instead for complex cases, or avoid background images)
- `border-radius` on `<table>` -- use on `<td>` only

---

## Outlook VML (advanced, optional)

For solid-color background sections in Outlook, the `bgcolor` attribute is enough. For background images in Outlook specifically, use VML conditionals:

```html
<!--[if gte mso 9]>
<v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width:600px;height:200px;">
  <v:fill type="tile" src="[image-url]" color="#1A1A1A"/>
  <v:textbox inset="0,0,0,0">
<![endif]-->
  <!-- content here -->
<!--[if gte mso 9]>
  </v:textbox>
</v:rect>
<![endif]-->
```

Use this only when background images are critical to the design.

---

## Pre-Send QA Checklist

- [ ] All styles inline -- no `<style>` blocks (except optional `<head>` media queries)
- [ ] All `<table>` have `cellpadding="0" cellspacing="0" border="0"`
- [ ] Images have `alt`, `border="0"`, `display:block`
- [ ] CTA button uses table+td with `bgcolor=` attribute
- [ ] Max-width 600px enforced on container
- [ ] Footer has unsubscribe link
- [ ] No `flexbox`, `grid`, `position`, `float`, CSS variables in inline styles
- [ ] Test in: Gmail web, Gmail app (iOS/Android), Apple Mail, Outlook 2016+
