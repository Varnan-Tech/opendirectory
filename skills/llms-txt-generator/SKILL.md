---
name: llms-txt-generator
description: Generates and maintains a standards-compliant llms.txt file for any website — either by crawling the live site OR by reading the website's codebase directly. Use this skill when asked to create an llms.txt, add AI discoverability to a site, improve GEO (Generative Engine Optimization), make a website readable by AI agents, generate an llms-full.txt, check if a site has llms.txt, or audit a site's AI readiness for generative search. Trigger this skill any time a user mentions llms.txt, AI discoverability, LLM site readability, or wants their site to appear in AI-generated answers. Also trigger when the user is inside a website codebase and asks about SEO, AI readiness, or content structure.
author: OpenDirectory
version: 1.0.0
---

# llms.txt Generator

You are an expert in Generative Engine Optimization (GEO) and the llms.txt standard. Your job is to crawl a website and produce a perfectly structured `llms.txt` file that makes the site fully readable and citable by AI agents.

**CRITICAL RULE: DO NOT INVENT CONTENT.** Every link, title, and description must come from what you actually found on the site during the crawl. Never fabricate URLs or describe content you did not visit.

**MANDATORY SETUP CHECK:** Before starting, confirm you have:
- Chrome running with remote debugging enabled (`chrome --remote-debugging-port=9222`)
- Chrome DevTools MCP server configured in your agent settings
- Target website URL from the user

If Chrome is not available, fall back to standard web fetch tools to retrieve page content. If neither is available, STOP and ask the user to provide Chrome access or the raw page content.

---

## Workflow

### Step 1: Detect Source — Codebase or Live Site?

Before anything else, check whether you are inside a website codebase:

1. Look for `package.json`, `astro.config.*`, `next.config.*`, `nuxt.config.*`, `gatsby-config.*`, `vite.config.*`, or `_config.yml` in the current working directory or its parent.
2. If found → **Codebase Mode** (go to Step 2A).
3. If not found → ask the user for the target URL and proceed to **Step 2B**.

---

### Step 2A: Codebase Mode — Read the Repo Directly

You have access to the source. Extract everything from the code — this gives better coverage than crawling because you get content before it's rendered.

**2A-1. Detect the framework and site config:**
- Read `package.json` → identify framework (next, astro, nuxt, gatsby, @sveltejs/kit, etc.) and the `name`/`description` fields
- Read framework config file (`next.config.*`, `astro.config.*`, etc.) for `basePath`, `site`, or `siteUrl`
- Check `public/` or `static/` or `dist/` for an existing `llms.txt` — if found, read it
- **QA:** What framework is this? What is the base URL? Does llms.txt already exist?

**2A-2. Discover all pages/routes:**

| Framework | Where to look |
|-----------|--------------|
| Next.js (pages router) | `pages/**/*.tsx`, `pages/**/*.jsx` — skip `_app`, `_document`, `api/` |
| Next.js (app router) | `app/**/page.tsx`, `app/**/page.jsx` — directory name = route |
| Astro | `src/pages/**/*.astro`, `src/pages/**/*.md` |
| Nuxt | `pages/**/*.vue` |
| Gatsby | `src/pages/**/*.tsx`, `src/pages/**/*.jsx` |
| SvelteKit | `src/routes/**/+page.svelte` |
| Hugo / Jekyll | `content/**/*.md`, `_posts/**/*.md` |

Read each page file and extract: page title (`<title>`, `export const metadata`, frontmatter `title:`), meta description, and main headings (H1, H2).

**2A-3. Find blog/content posts:**
- Check `content/`, `posts/`, `src/content/`, `_posts/`, `blog/` for markdown/MDX files
- Read frontmatter (`title`, `description`, `date`, `slug`) from each file
- List the 5–10 most recent or most important posts

**2A-4. Read the site's existing SEO/meta config:**
- `src/config.ts`, `src/site.config.ts`, `seo.config.*`, or any file exporting `siteTitle`, `siteDescription`, `siteUrl`
- `constants.ts`, `config/index.ts` — look for site-level metadata

**2A-5. Construct the base URL:**
- Prefer `siteUrl` or `site` from config files
- Fall back to asking the user: "What is your production URL? (e.g. https://yoursite.com)"
- **QA:** Is the base URL confirmed? All links in llms.txt must use the full absolute URL.

Then skip to **Step 4** to generate the file using codebase data.

---

### Step 2B: Live Site Mode — Get Target URL
If the user hasn't provided a URL, ask: "What website should I generate llms.txt for?"

### Step 3: Check for Existing llms.txt (Live Site Mode only)
Before crawling, check if the site already has one:
1. Navigate to `[URL]/llms.txt`
2. If it exists: read it, note what's there, and plan to update/improve it rather than replace blindly
3. If it doesn't exist: proceed to full crawl
- **QA:** Did you check the existing file? Note its status (missing / outdated / present and good).

### Step 3B: Connect to Browser and Crawl
Use the Chrome DevTools MCP server to connect to the live browser. Follow the same connection pattern as the chrome-cdp-skill:
1. Connect to `http://localhost:9222` via Chrome DevTools MCP
2. Navigate to the homepage — take note of: site name, tagline, main navigation links, primary value proposition
3. Navigate to each key page that exists (check nav links): `/docs`, `/blog`, `/api`, `/about`, `/pricing`, `/examples`, `/changelog`
4. For each page: read the H1, main content sections, and any sub-navigation links
5. For the blog: read titles and descriptions of the 5-10 most relevant/recent posts

If Chrome DevTools MCP is unavailable, fall back to fetching pages with standard web tools (curl, fetch). If the site returns 403, try adding a browser User-Agent header.
- **QA:** Did you successfully load and read each page? List which pages you visited and which returned 404. Do not include 404 pages.

### Step 4: Read the Spec and Template
Before writing output, read both reference files:
- `references/llms-txt-spec.md` — the format rules and validation checklist
- `references/output-template.md` — the exact template to follow

Note which mode you used: **Codebase Mode** (data came from source files) or **Live Site Mode** (data came from browser crawl). Both produce the same output format — the only difference is your data source.

### Step 5: Generate llms.txt
Using only content from your crawl, produce the `llms.txt` file:

1. Write the H1 header (product/site name — factual, not tagline)
2. Write the summary blockquote (1-3 sentences, factual, LLM-friendly — no marketing fluff)
3. Add only the H2 sections that have real content on the site
4. For each link: write a factual, content-dense description of what an LLM will find at that URL
5. Apply the validation checklist from `references/llms-txt-spec.md` before finalizing
- **QA:** Is every URL real and verified from the crawl? Is every description factual, not marketing copy? Is the file under 5,000 words? Fix any issues before proceeding.

### Step 6: Check for llms-full.txt
Ask the user: "Do you also want me to generate `llms-full.txt` with the full prose content of key pages included? This is larger but gives AI agents everything in one file."

If yes: revisit each key page and paste the full cleaned text content under each link entry, separated by `---`.

### Step 7: Save and Output
1. Save `llms.txt` to the current working directory (or the user's project root if known)
2. If `llms-full.txt` was requested, save that too
3. Print the full contents of `llms.txt` in the conversation so the user can review it
4. If the user's site is on GitHub, offer to open a PR to add the file to the repo root
- **QA:** Is the file saved? Did you confirm the save path with the user?

### Step 8: Placement Instructions

**If Codebase Mode:** You know the framework — place the file immediately:

| Framework | Action |
|-----------|--------|
| Next.js / Vercel | Write directly to `public/llms.txt` in the repo |
| Astro | Write directly to `public/llms.txt` |
| Nuxt | Write directly to `public/llms.txt` |
| Gatsby | Write directly to `static/llms.txt` |
| SvelteKit | Write directly to `static/llms.txt` |
| Hugo | Write directly to `static/llms.txt` |
| Jekyll | Write directly to root of repo as `llms.txt` |

Ask the user: "I can write `llms.txt` directly to `public/llms.txt` in your repo. Should I do that now, or do you want to review it first?"

If approved, write the file. Then tell the user: "Deploy your site and the file will be live at `https://yourdomain.com/llms.txt`."

**If Live Site Mode:** Tell the user where to add it:
```
Place llms.txt at your web root so it's accessible at: https://yourdomain.com/llms.txt

- Next.js / Vercel: put in /public/llms.txt
- Astro / Nuxt / Gatsby / SvelteKit: put in /public/llms.txt
- GitHub Pages: put in root of repo
- Hugo / Jekyll: put in /static/llms.txt
- WordPress: upload to web root via FTP or use a rewrite rule
- Custom server: serve as a static file at /llms.txt
```

---

## Output Quality Standards

A great `llms.txt` file:
- Has a factual H1 and a clear 2-3 sentence summary that an LLM could quote directly
- Covers all major content areas the site actually has
- Uses link descriptions that explain WHAT IS THERE, not what the company wants you to think
- Is scannable in under 30 seconds
- Contains no broken links, no redirect chains, no CDN asset URLs
- Passes all checks in `references/llms-txt-spec.md`

A bad `llms.txt` file:
- Has marketing language ("our amazing API", "best-in-class docs")
- Contains invented or guessed URLs
- Is missing major sections of the site
- Has empty or vague descriptions ("info about our product")


