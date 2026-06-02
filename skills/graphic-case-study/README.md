# graphic-case-study

Generate a professionally designed case study PDF for B2B SaaS sales and marketing. Structured around the challenge → solution → results → testimonial arc. Outputs a browser-ready HTML file + print-ready PDF. Supports 7 page section layouts and 9 business style presets.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install graphic-case-study --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fgraphic-case-study&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What it does

- Asks the questions that determine how the case study should be structured
- Interviews you (or processes your notes) to extract customer story details
- Structures the narrative: customer context → challenge → solution → results → testimonial
- Generates a single self-contained HTML file -- opens in any browser, no build tools
- Splits into per-page HTML files for individual sharing or editing
- Exports a print-ready PDF via Playwright (A4 portrait, 1200×1697px)
- Supports 1-pager summary card, standard 2-pager, and detailed 4-pager formats

## Example

> "Create a 2-page case study for Acme Corp. They were spending 20 hrs/week on manual reporting. We automated it. They saved 80% of that time and reduced errors by 95%. Use midnight-editorial style."

Output: 2-page PDF with cover, challenge/solution spread, results stat page, and closing CTA.

---

## Supported Styles

| Style | Best for |
|---|---|
| clean-slate | Enterprise B2B, sales teams, any audience that expects professionalism |
| midnight-editorial | Tech/AI companies, premium B2B, investor-grade materials |
| matt-gray | Board materials, internal reviews, professional mixed audiences |
| product-minimal | Product companies, design-forward B2B, design-savvy buyers |
| mint-pixel-corporate | SaaS sales, tech startups, growth-stage B2B |
| warm-earth | Agencies, consultancies, service businesses, health/education tech |
| brutalist | Standout sales materials, design-forward agencies, bold brands |
| magazine-red | Marketing agencies, brand-forward companies, editorial-style stories |
| soft-cloud | Onboarding materials, customer education, approachable SaaS |

---

## Supported Page Layouts

| Layout | Purpose |
|---|---|
| cover | Opening page -- customer name, headline result, logos |
| overview | At-a-glance: company profile, industry, use case |
| challenge | The problem -- context paragraph + pain points |
| solution | How your product solved it -- feature callouts |
| results | Key metrics in large stat format + supporting narrative |
| testimonial | Full-width pull quote with attribution |
| closing-cta | Vendor logo + contact info + next step CTA |

---

## Output

| File | What it is |
|---|---|
| `case-study/[slug]/index.html` | Full case study, browser-ready |
| `case-study/[slug]/page-01.html` ... | Per-page HTML files for individual sharing |
| `case-study/[slug].pdf` | Print-ready PDF (A4 portrait) |

Standard dimensions: 1200×1697px (A4 portrait). Landscape 4:3 (1200×900) available on request.

---

## Parameters

| Param | Required | Notes |
|---|---|---|
| customer_name | Yes | Company name (or "Anonymous Fortune 500 Retailer" to anonymize) |
| challenge | Yes | Core problem in 2-5 sentences |
| solution | Yes | What your product did |
| results | Yes | Measurable outcomes -- ideally 3 stats |
| customer_context | No | Industry, size, location (for overview page) |
| testimonial | No | Customer quote + name + title |
| page_count | No | 1 / 2 / 4 (default: 2) |
| customer_logo | No | Logo URL for cover page |
| your_company_name | No | Vendor name + logo URL for CTA page |
| style | No | One of 9 named presets or "show me options" (default: clean-slate) |
| orientation | No | A4 portrait (default) or landscape 4:3 |
| anonymize | No | Keep name or replace with industry descriptor |
| slug | No | Filename slug (derived from customer name if omitted) |

---

## Dependencies

This skill requires the `frontend-slides` skill files at:
`/Users/ksd/Desktop/Varnan_skills/frontend-slides/`

Specifically:
- `viewport-base.css` -- responsive page foundation (included verbatim in generated HTML)
- `scripts/export-pdf.sh` -- PDF export via Playwright (Node.js required, auto-installs; use `--portrait` flag for A4)

## No API keys required

Pure AI skill. No external services, no scraping, no dependencies beyond the above.
