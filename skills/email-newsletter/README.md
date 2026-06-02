# email-newsletter

Draft and design a complete HTML email newsletter from a topic or content brief. Output is paste-ready for Loops, Mailchimp, Beehiiv, Resend, or any standard email platform.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install email-newsletter --target claude
```

### Option B: Claude Desktop App

<video src="https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c" controls width="100%"></video>

**Step 1: Download the skill from GitHub**

1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

**Step 2: Install in Claude**

1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** button to create a new skill.
4. Choose **Upload a skill**, then drag and drop the `.zip` file or extracted folder.

> **Note:** For some skills, the `SKILL.md` file might be located inside a subfolder. Always upload the specific folder that contains the `SKILL.md` file.

### Option C: Claude Code Native

Run these commands inside Claude Code:

```bash
/plugin marketplace add Varnan-Tech/opendirectory
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

### Option D: Manus AI

<video src="https://www.opendirectory.dev/ManusAI-one-click-installation-demo.webm" controls width="100%"></video>

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Femail-newsletter&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What it does

- Asks the 19 questions that actually determine your newsletter layout
- Writes all sections: hero, intro, main content, stat callout, CTA, footer
- Generates table-based HTML with inline styles -- compatible with every major email client
- Tunes variable syntax per platform (Loops, Mailchimp, Beehiiv, Resend)
- Produces 3 subject line options using proven formulas
- Includes a plain-text fallback for deliverability

## Example

> "Write a newsletter about how AI is changing B2B sales. Audience: VPs of Sales at 100-500 person SaaS companies. CTA: join our upcoming webinar. Tone: direct. Platform: Beehiiv."

Output: full HTML email with hero headline, 3-section body, stat callout, CTA block, and footer -- plus 3 subject line options and a plain-text version, tuned for Beehiiv.

## Supported platforms

| Platform | Notes |
|---|---|
| Loops | `{{unsubscribe_url}}` syntax. Paste into custom HTML editor |
| Mailchimp | `*\|UNSUB\|*` syntax. Use "Code your own" template. Includes `mc:edit` regions |
| Beehiiv | `%%unsubscribe_url%%` syntax. Works with custom HTML block |
| Resend | `{unsubscribeUrl}` syntax. React Email `.tsx` output available on request |
| Generic | `[UNSUBSCRIBE_URL]` placeholder -- replace before sending |

## Output formats

- **Standard HTML** (default): inline-styled, table-based, 600px max-width
- **Plain text**: always included unless you opt out
- **React Email** (on request): `.tsx` component output for Resend / dev teams

## Parameters

| Param | Required | Notes |
|---|---|---|
| topic | Yes | What the newsletter is about |
| audience | Yes | Who is reading |
| cta | Yes | Primary action you want readers to take |
| company_name | No | Brand name for header and footer |
| tagline | No | One-line description for footer |
| city_country | No | Footer location (e.g. "San Francisco, US") |
| cta_url | No | Actual link for CTA button -- placeholder used if omitted |
| brand_color | No | Hex code -- used for strip, stat border, category label |
| background | No | dark / light / custom hex (default: dark) |
| display_font | No | editorial serif / modern sans / system fonts (default: Instrument Serif) |
| button_style | No | pill / softly rounded / sharp (default: pill) |
| visual_style | No | editorial / technical+data / warm+founder / bold+campaign |
| tone | No | educational / conversational / bold+direct / formal / playful |
| platform | No | loops / mailchimp / beehiiv / resend (default: generic) |
| personalization | No | none / first name / first name + company (default: none) |
| length | No | brief (300w) / standard (500-700w) / deep dive (800w+) |
| format | No | editorial article / numbered breakdown / personal story / data report |
| subject_line | No | If omitted, 3 options are suggested |
| secondary_sections | No | sponsor block / product callout / event / quick links |

## No API keys required

Pure AI skill. No external services, no scraping, no dependencies to install.

## Design principles

- Max width 600px (email client standard)
- Inline styles only -- no external CSS, email clients strip it
- Table-based layout for Outlook compatibility
- Georgia serif for hero headlines, Arial/system font for body
- CTA buttons use the table+td VML-compatible structure
- All images include alt text
- Dark mode aware where platform supports it
