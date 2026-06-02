# graphic-ebook

Create professionally designed B2B SaaS e-books (3–10 pages) using HTML + CSS. Supports 9 visual styles and 11 page layout types. Outputs a browser-ready HTML file + print-ready PDF.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install graphic-ebook --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fgraphic-ebook&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What it does

- Asks 4 required questions to establish topic, audience, CTA, and content source
- Asks 9 optional intake questions to determine style, page count, and brand
- Plans the chapter structure and page sequence (with user confirmation)
- Drafts or uses provided content — per-page copy with word count discipline
- Generates a single self-contained HTML file — opens in any browser, no build tools
- Splits into per-page HTML files for individual sharing or editing
- Exports a print-ready PDF via Playwright (A4 portrait, 1200×1697px)
- Enforces visual rhythm — no 2+ consecutive text pages back-to-back

## Example

> "Create a 6-page ebook titled 'The B2B SaaS Guide to Reducing Churn'. Audience: Customer Success Managers at 50–500 person SaaS companies. CTA: book a demo. Style: clean-slate. Brand: DataPulse."

Output: cover + TOC + chapter opener + body page + stat page + closing CTA, exported as PDF.

---

## Supported Styles

| Style | Best for |
|---|---|
| clean-slate | Enterprise B2B, sales teams, any audience that expects professionalism |
| midnight-editorial | Tech/AI companies, premium B2B, thought leadership |
| matt-gray | Board materials, internal reviews, professional mixed audiences |
| product-minimal | Product companies, design-forward B2B, design-savvy buyers |
| mint-pixel-corporate | SaaS sales, tech startups, growth-stage B2B |
| warm-earth | Agencies, consultancies, service businesses, health/education tech |
| brutalist | Standout materials, design-forward agencies, bold brands |
| magazine-red | Marketing agencies, brand-forward companies, research reports |
| soft-cloud | Onboarding materials, customer education, approachable SaaS |

---

## Supported Page Layouts

| Layout | Purpose |
|---|---|
| cover | Opening page — title, subtitle, brand name, visual |
| toc | Table of contents — numbered chapter list |
| chapter-intro | Section opener — large chapter number, title, teaser |
| text-column | Reading body copy — 1-column or 2-column |
| text-sidebar | Body copy + typed callout sidebar (tip/warning/stat/quote/checklist) |
| quote-callout | Full-page pull quote with attribution |
| stat-grid | 3–6 key metrics with visual emphasis |
| key-takeaways | Summary list — what the reader retains |
| full-image | Full-page CSS-generated visual or abstract composition |
| closing-cta | Final page — CTA action + email + URL |

---

## Output

| File | What it is |
|---|---|
| `ebook/[slug]/index.html` | Full ebook, browser-ready |
| `ebook/[slug]/page-01.html` … | Per-page HTML files for individual sharing |
| `ebook/[slug].pdf` | Print-ready PDF (A4 portrait) |

Standard dimensions: 1200×1697px (A4 portrait).

---

## Parameters

| Param | Required | Notes |
|---|---|---|
| topic | Yes | The ebook subject (specific: "5 ways to reduce CAC") |
| audience | Yes | Target reader persona (role, company size, pain point) |
| desired_action | Yes | What reader should do after reading |
| content | Yes | Existing content to use, or "draft from scratch" |
| page_count | No | 3–10 (default: 6) |
| key_takeaways | No | 3–5 things the reader should learn |
| brand_name | No | Company/product name for cover and footer |
| brand_logo | No | Logo URL (CSS initials generated if omitted) |
| style | No | One of 9 named presets or "show me options" (default: clean-slate) |
| chapter_count | No | Number of main sections (derived from page_count if omitted) |
| cta_details | No | Primary CTA (default: "book a demo") |
| contact_info | No | Email + URL for closing page |
| slug | No | Filename slug (derived from topic if omitted) |

---

## Dependencies

**Node.js** — required for PDF export. Auto-detected; install from [nodejs.org](https://nodejs.org) if missing.

Everything else is bundled inside this skill:
- `assets/viewport-base.css` — responsive page foundation (included verbatim in generated HTML)
- `scripts/export-pdf.sh` — PDF export via Playwright (auto-installs Playwright + Chromium on first run)

No external skill dependencies. No API keys required.
