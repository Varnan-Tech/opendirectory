# Platform Compatibility

Per-platform quirks, variable syntax, and paste instructions.

---

## Loops

**Variable syntax:** Handlebars `{{ }}`

| Placeholder | Loops variable |
|---|---|
| `[UNSUBSCRIBE_URL]` | `{{unsubscribe_url}}` |
| `[FIRST_NAME]` | `{{first_name}}` |
| `[EMAIL]` | `{{email}}` |

**How to use:**
- Open Loops dashboard > New Email > Custom HTML
- Paste the full HTML directly into the custom HTML editor
- Loops supports most standard email HTML including table layouts

**Notes:**
- Loops strips some `<head>` content -- the email still renders correctly
- Test with a preview send before publishing to subscribers

---

## Mailchimp

**Variable syntax:** Merge tags `*| |*`

| Placeholder | Mailchimp merge tag |
|---|---|
| `[UNSUBSCRIBE_URL]` | `*\|UNSUB\|*` |
| `[FIRST_NAME]` | `*\|FNAME\|*` |
| `[EMAIL]` | `*\|EMAIL\|*` |
| `[COMPANY NAME]` | `*\|COMPANY\|*` (if merge field exists) |

**How to use:**
- Create Campaign > Email > Code your own
- Paste HTML into the code editor

**Additional: mc:edit regions**
Mailchimp lets editors modify sections in their visual builder if you add `mc:edit` attributes:

```html
<td mc:edit="main-content" style="padding:24px 32px;">
  <!-- editable content here -->
</td>
```

Add `mc:edit="[section-name]"` to any `<td>` that the Mailchimp team should be able to edit visually. Use descriptive names: `mc:edit="hero"`, `mc:edit="body"`, `mc:edit="footer"`.

**Notes:**
- Inline styles are required -- Mailchimp strips `<style>` blocks in some plans
- Mailchimp has its own image hosting -- you can upload images during setup

---

## Beehiiv

**Variable syntax:** Double percent `%% %%`

| Placeholder | Beehiiv variable |
|---|---|
| `[UNSUBSCRIBE_URL]` | `%%unsubscribe_url%%` |
| `[FIRST_NAME]` | `%%first_name%%` |
| `[EMAIL]` | `%%email%%` |

**How to use:**
- Post > New post > Switch to custom HTML block
- Paste HTML into the HTML block editor
- Table-based layouts are fully supported in Beehiiv

**Notes:**
- Beehiiv wraps your HTML in their outer template -- you do not need to add their header/footer chrome
- Some users paste only the inner content (hero + body + CTA) and let Beehiiv handle the wrapper

---

## Resend

**Variable syntax:** JSX-style curly braces `{ }`

| Placeholder | Resend variable |
|---|---|
| `[UNSUBSCRIBE_URL]` | `{unsubscribeUrl}` |
| `[FIRST_NAME]` | `{firstName}` |

**How to use (Standard HTML):**
- Resend accepts raw HTML via their API: `html: yourHtmlString`
- Or use the Resend dashboard > Broadcasts > Custom HTML

**React Email option:**
Resend supports React Email natively -- if the team is developer-focused, request React Email `.tsx` output instead:
- Each section becomes a React Email component
- Styled with inline styles via the `style=` prop
- Compatible with the `@react-email/components` package

**React Email component structure:**
```tsx
import { Html, Head, Body, Container, Section, Text, Button, Hr } from '@react-email/components';

export default function NewsletterEmail({ firstName = 'there' }: { firstName?: string }) {
  return (
    <Html>
      <Head />
      <Body style={{ backgroundColor: '#F4F4F4', margin: '0', padding: '0' }}>
        <Container style={{ maxWidth: '600px', margin: '0 auto', backgroundColor: '#FFFFFF' }}>
          {/* sections here */}
        </Container>
      </Body>
    </Html>
  );
}
```

Install: `npm install @react-email/components`
Preview: `npx react-email dev`

**Notes:**
- Resend's HTML-to-email rendering is more modern than Outlook -- less table wrestling needed
- Still use inline styles in React Email for maximum compatibility

---

## Generic / Other ESPs

Use these placeholders and instruct the user to replace manually before sending:

| Placeholder | What to replace with |
|---|---|
| `[UNSUBSCRIBE_URL]` | Your ESP's unsubscribe URL or merge tag |
| `[FIRST_NAME]` | Your ESP's first name merge tag |
| `[CTA_URL]` | Actual destination URL |
| `[COMPANY NAME]` | Your company name |
| `[CITY, COUNTRY]` | Your registered address |

Add HTML comment above footer:
```html
<!-- Replace [UNSUBSCRIBE_URL] with your ESP's unsubscribe variable before sending -->
```

---

## Platform Comparison Quick Reference

| Feature | Loops | Mailchimp | Beehiiv | Resend |
|---|---|---|---|---|
| Variable syntax | `{{var}}` | `*\|VAR\|*` | `%%var%%` | `{var}` or JSX |
| Custom HTML | Yes, native | Yes, "Code your own" | Yes, HTML block | Yes, API or dashboard |
| Table layouts | Full support | Full support | Full support | Full support |
| React Email | No | No | No | Yes, native |
| Unsubscribe var | `{{unsubscribe_url}}` | `*\|UNSUB\|*` | `%%unsubscribe_url%%` | `{unsubscribeUrl}` |
