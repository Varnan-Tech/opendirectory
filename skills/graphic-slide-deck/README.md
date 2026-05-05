# graphic-slide-deck

Generate a professionally designed HTML slide deck from a brief, content notes, or an existing PowerPoint. Outputs a browser-ready presentation + optional PDF. Supports 13 named layout types and 8 business style presets.

## Install

```bash
npx "@opendirectory.dev/skills" install graphic-slide-deck --target claude
```

### Video Tutorial
Watch this quick video to see how it's done:

https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c

### Step 1: Download the skill from GitHub
1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

### Step 2: Install the Skill in Claude
1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** (plus) icon button to create a new skill.
4. Choose the option to **Upload a skill**, and drag and drop the `.zip` file (or you can extract it and drop the folder, both work).

> **Note:** Make sure you upload the folder that contains the `SKILL.md` file directly.

---

## What it does

- Asks the questions that determine how a deck should be structured
- Plans the slide sequence with named layout types for each slide
- Generates a single self-contained HTML file -- opens in any browser, no build tools
- Splits into per-slide HTML files for individual sharing or editing
- Exports a PDF via Playwright (renders animations to final state)
- Optionally deploys to a live URL via Vercel for phone/tablet sharing
- Converts existing PowerPoint files to HTML

## Example

> "Create a 12-slide Series A investor deck for DataPulse. Audience: Series A VCs. Style: midnight-editorial."

Output: 12-slide HTML presentation, per-slide HTML files, and a PDF -- covering problem/solution/traction/team/market/ask.

---

## Supported Styles

| Style | Best for |
|---|---|
| midnight-editorial | Investor decks, premium B2B, thought leadership |
| matt-gray | Internal decks, operational reviews, mixed audiences |
| clean-slate | Sales decks, customer-facing, enterprise-safe |
| brutalist | Startup pitches, design-forward, tech conferences |
| mint-pixel-corporate | SaaS sales, product demos, growth-stage pitches |
| product-minimal | Product demos, feature showcases, design audiences |
| magazine-red | Marketing reports, campaign reviews, bold internal |
| soft-cloud | Onboarding, customer education, approachable SaaS |

---

## Supported Layouts

| Layout | Use case |
|---|---|
| title-hero | Opening slide -- large headline + subtext |
| section-divider | Section break -- bold label, minimal design |
| text-full | Headers + bullet points or paragraphs |
| text-left-image-right | Side-by-side: text column + visual |
| image-left-text-right | Side-by-side: image first, text second |
| two-column-text | Comparisons, pros/cons, before/after |
| image-full | Full-bleed image with optional caption overlay |
| image-grid | 2x2 or 3x2 grid of images or screenshots |
| stat-highlight | 2-4 large KPI metrics (the unmissable slide) |
| quote-callout | Pull quote with attribution |
| comparison-table | Feature or option comparison grid |
| timeline | Horizontal or vertical milestones |
| closing-cta | Final slide -- CTA, contact info, next steps |

---

## Output

| File | What it is |
|---|---|
| `deck/[name]-slides/index.html` | Full presentation, browser-ready |
| `deck/[name]-slides/slide-001.html` ... | Per-slide HTML files for individual sharing |
| `deck/[name].pdf` | PDF export (if requested) |
| Live URL | Deployed Vercel URL (if requested) |

Slides are 1920x1080px (16:9) by default. 1:1 (1080x1080) available for LinkedIn.

---

## Parameters

| Param | Required | Notes |
|---|---|---|
| purpose | Yes | investor pitch / sales call / conference talk / internal / onboarding |
| audience | Yes | VCs, prospects, your team, executives, conference room |
| topic_or_content | Yes | Freeform brief, notes, URL, or uploaded file |
| key_message | No | Single sentence the audience must remember |
| slide_count | No | Default: 12 |
| style | No | One of 8 named presets or "show me options" (default: clean-slate) |
| aspect_ratio | No | 16:9 or 1:1 (default: 16:9) |
| inline_editing | No | Yes/No -- editable in-browser (default: No) |
| output_format | No | HTML only / HTML+PDF / HTML+PDF+deploy (default: HTML+PDF) |
| deck_name | No | Slug for file/folder naming (derived from topic if omitted) |

---

## Dependencies

This skill requires the `frontend-slides` skill files at:
`/Users/ksd/Desktop/Varnan_skills/frontend-slides/`

Specifically:
- `viewport-base.css` -- responsive slide foundation (included verbatim in generated HTML)
- `html-template.md` -- SlidePresentation class and inline editing system
- `animation-patterns.md` -- entrance animations and background effects
- `scripts/export-pdf.sh` -- PDF export via Playwright (Node.js required, auto-installs)
- `scripts/deploy.sh` -- Vercel deployment (Node.js required)
- `scripts/extract-pptx.py` -- PowerPoint content extraction (Python + `python-pptx` required)

## No API keys required

Pure AI skill. No external services, no scraping, no dependencies to install beyond the above.
