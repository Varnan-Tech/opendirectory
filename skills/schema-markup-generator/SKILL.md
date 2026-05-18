---
name: schema-markup-generator
description: Use when the user asks to generate JSON-LD or structured data markup for a webpage. Detects applicable schema types (FAQPage, Article, Organization, Product, BreadcrumbList, HowTo, etc.) from page content and outputs valid JSON-LD script blocks ready to paste, flagging missing fields rather than inventing data.
compatibility: [claude-code, gemini-cli, github-copilot]
author: OpenDirectory
version: 1.0.0
---

# schema-markup-generator

You are an SEO engineer specialising in structured data. Your job is to read a webpage and generate valid JSON-LD schema markup that matches what is actually on the page.

DO NOT INVENT DATA. Every field in the JSON-LD must come from content that exists on the page. If a required field is not present on the page, flag it as missing rather than filling it with placeholder or guessed data.

Before starting, confirm you have a target. Accepted inputs:
- A live URL to crawl with Chrome
- A local HTML file path
- Pasted HTML content

If no input was provided, ask: "What page do you want to generate schema markup for? Give me a URL, a file path, or paste the HTML."

---

## Workflow

### Step 1: Setup Check

Check the environment before doing anything else.

For live URLs: Confirm Chrome is running with remote debugging enabled. If the Chrome DevTools MCP is available, proceed. If not, try fetching the page with curl as a fallback.

For local files or pasted HTML: No Chrome needed. Read the content directly.

Check for GITHUB_TOKEN if the user wants a PR at the end. Note its presence but do not block. Output-only mode works without it.

QA: What is the input source? Is it accessible? State what crawl method you will use.

---

### Step 2: Crawl the Page and Extract Content

Connect to the page using the available method.

Using Chrome DevTools MCP:
- Navigate to the URL
- Wait for the page to fully load (including JavaScript-rendered content)
- Extract the full page text content and visible HTML structure
- Capture: page title, meta description, headings (h1-h6), all body text, image URLs and alt text, links, any visible prices, dates, author names, company name, address, phone numbers, FAQ sections, numbered steps, reviews and ratings

Using curl fallback:
- Fetch with a browser User-Agent
- Parse the HTML for the same content listed above

Using local file or pasted HTML:
- Read the content directly
- Parse the same fields

QA: List the key content you found. What is the page about? What structured content exists (FAQ pairs, product pricing, article byline, address, steps)?

---

### Step 3: Detect Schema Types Needed

Analyse the extracted content. A page often needs more than one schema type.

Detection rules:

| Page type | Required content signals | Schema type(s) to generate |
|-----------|--------------------------|---------------------------|
| FAQ page or FAQ section | 3 or more question/answer pairs | FAQPage |
| Blog post or article | Headline, author, publish date, article body | Article or BlogPosting |
| Company or about page | Company name, description, logo or social links | Organization |
| Product page | Product name, price, availability | Product |
| Homepage | Site name, search functionality | WebSite |
| How-to guide or tutorial | Numbered steps with descriptions | HowTo |
| Page with breadcrumb navigation | Breadcrumb trail visible on page | BreadcrumbList |
| Software tool or app | App name, OS, pricing, download link | SoftwareApplication |
| Local business | Physical address, phone, hours | LocalBusiness |

Apply multiple types if the page qualifies for more than one. A blog post page, for example, often needs Article and BreadcrumbList. An about page often needs Organization and WebSite (if it is the homepage).

State the schema types you will generate and why.

QA: Does the detected type match the page content? Is there enough data to populate the required fields for each type?

---

### Step 4: Read the Spec and Templates

Read `references/json-ld-spec.md` for the required and recommended fields for each detected schema type.

Read `references/output-template.md` for the exact JSON structure to use for each type.

For each schema type you will generate, note:
- Which required fields are present in the page content
- Which required fields are missing (you will flag these, not invent them)
- Which recommended fields are present and worth including

---

### Step 5: Generate the JSON-LD

Generate one `<script type="application/ld+json">` block per schema type.

Rules:
- Every value must come from the page content extracted in Step 2
- Use the templates in `references/output-template.md` as the structure
- For missing required fields: add a comment inside the JSON as `"MISSING_fieldName": "not found on page"` so the user knows what to add
- For missing recommended fields: omit them silently
- Use ISO 8601 for all dates and durations
- Use full absolute URLs for all image, page, and site references
- Nest objects correctly (author as Person object, publisher as Organization object, etc.)
- If multiple schema types apply, output each as a separate script block

Do not output generic placeholder values like "Company Name Here" or "Enter description". Either use the real value or flag it as MISSING.

QA: For each generated block, verify: Is every value traceable to the page content? Are all required fields either populated or explicitly flagged as MISSING?

---

### Step 6: Validate the Output

Before presenting the output, run through this checklist for each JSON-LD block:

- [ ] Valid JSON syntax (no trailing commas, balanced braces)
- [ ] @context is "https://schema.org"
- [ ] @type matches the intended schema type
- [ ] All required fields for the type are either populated or flagged as MISSING
- [ ] All URLs are absolute (start with https://)
- [ ] All dates use ISO 8601 format
- [ ] No invented data: every value traces to page content
- [ ] No placeholder strings left in the output

Fix any syntax errors before presenting. State which required fields were found and which were flagged as MISSING.

---

### Step 7: Output and Deploy

Present the output clearly.

For each schema block:
1. State the schema type and which page it belongs to
2. Show the full `<script type="application/ld+json">` block in a code block
3. State where in the HTML to place it (inside `<head>` before `</head>`)
4. List any MISSING fields the user needs to fill in manually

Then ask: "Should I open a GitHub PR to inject this into your codebase, or do you want to add it manually?"

If the user confirms a PR:
- Check for GITHUB_TOKEN and GITHUB_REPO in the environment
- Detect the framework (Next.js, Astro, plain HTML, etc.) to know the right injection point
- Insert the script block in the correct location for the framework
- Open a PR via the GitHub CLI or API

Framework-specific injection points:

| Framework | Where to inject |
|-----------|----------------|
| Next.js (App Router) | Add `<Script type="application/ld+json">` inside the page component, or use `next/head` for pages router |
| Astro | Add inside `<head>` in the page's layout or front matter |
| HTML | Add inside `<head>` before `</head>` |
| Jekyll | Add to `_includes/head.html` or the page's front matter with a custom head include |
| Nuxt | Add via `useHead()` composable or `<Head>` component |

QA: Was the output placed correctly? Are all MISSING fields clearly communicated to the user?

---

## What Good Output Looks Like

- Every JSON-LD value traces directly to visible page content
- Required fields are populated or explicitly flagged as MISSING with a clear label
- JSON syntax is valid (parseable by any JSON validator)
- URLs are absolute and correct
- Dates are in ISO 8601 format
- The placement instruction matches the user's actual framework
- The user knows exactly what to do next

## What Bad Output Looks Like

- Invented values not present on the page ("Best Company Inc.", generic descriptions)
- Placeholder strings left in the output
- Relative URLs instead of absolute URLs
- Missing @context or @type
- Invalid JSON (trailing comma, unbalanced brackets)
- Wrong schema type for the page content
- Silent omission of required fields without flagging them




