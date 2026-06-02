# schema-markup-generator

![schema-markup-generator](https://github.com/user-attachments/assets/4b5e5bfb-3c33-4a20-afff-59fda19196b4)


Generate valid JSON-LD structured data for any webpage. The agent crawls the page, detects which schema types apply, and outputs a script tag ready to paste into your HTML. Optionally opens a GitHub PR with the markup injected.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install schema-markup-generator --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fschema-markup-generator&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## Schema Types Supported

| Type | Use When |
|------|----------|
| FAQPage | Page has 2 or more visible question/answer pairs |
| Article / BlogPosting | Page is a blog post or editorial article |
| Organization | Page represents a company or institution |
| Product | Page sells or describes a product with pricing |
| WebSite | Homepage schema with optional sitelinks search |
| HowTo | Page is a step-by-step guide with numbered steps |
| BreadcrumbList | Page has visible breadcrumb navigation |
| SoftwareApplication | Page describes a software tool or app |
| LocalBusiness | Page represents a physical business location |

The agent detects the right type automatically. A single page often gets multiple types (a blog post gets Article and BreadcrumbList, a homepage gets WebSite and Organization).

## Requirements

No LLM API key needed. The agent reads the page and generates the markup.

Chrome is needed for JavaScript-rendered pages. For static HTML pages or when you paste HTML directly, Chrome is not required.

A GitHub token is optional. Without it, the agent outputs the markup as text for you to paste manually.

## Setup

### 1. Start Chrome with remote debugging (for live URLs)

```bash
# macOS
open -a "Google Chrome" --args --remote-debugging-port=9222

# Linux
google-chrome --remote-debugging-port=9222
```

### 2. Configure environment variables (optional)

```bash
cp .env.example .env
# Add GITHUB_TOKEN if you want auto-PR support
```

## How to Use

From a live URL:

```
"Generate schema markup for https://example.com/faq"
"Add structured data to https://example.com/blog/my-post"
"What schema markup does this page need? https://example.com/about"
```

From pasted HTML:

```
"Generate schema markup for this page: [paste HTML]"
"Add JSON-LD to this HTML: [paste HTML]"
```

Targeting a specific type:

```
"Generate FAQPage schema for https://example.com/support"
"Add Organization schema to our about page: https://example.com/about"
"Generate Product schema for this page: https://example.com/products/pro"
```

With auto-PR:

```
"Generate schema markup for https://example.com/blog/post and open a GitHub PR"
```

## Output

| Output | Description |
|--------|-------------|
| JSON-LD script block | One `<script type="application/ld+json">` block per schema type |
| Placement instructions | Where to insert the block in your HTML or framework |
| MISSING field list | Required fields not found on the page that you need to fill in |
| GitHub PR | If GITHUB_TOKEN and GITHUB_REPO are configured and you confirm |

## Validate Your Markup

After applying the markup, validate it at:

- Google Rich Results Test: https://search.google.com/test/rich-results
- Schema.org Validator: https://validator.schema.org

## Project Structure

```
schema-markup-generator/
├── SKILL.md
├── README.md
├── .env.example
├── evals/
│   └── evals.json
└── references/
    ├── json-ld-spec.md
    └── output-template.md
```

## License

MIT
