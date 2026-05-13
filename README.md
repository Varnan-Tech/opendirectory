<div align="center">
  <img src="docs/assets/opendirectory_banner.webp" width="100%" alt="OpenDirectory Banner" />
</div>

<br />

<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&duration=3000&pause=800&color=58A6FF&center=true&vCenter=true&width=620&height=50&lines=55+pre-built+AI+Agent+Skills;Works+with+Claude%2C+Codex%2C+Gemini+CLI;GTM+%7C+Marketing+%7C+Growth+Automation;Install+in+seconds.+No+setup+required." alt="Typing SVG" />
</div>

<br />

<div align="center">

[![npm version](https://img.shields.io/npm/v/@opendirectory.dev/skills.svg?style=flat-square)](https://www.npmjs.com/package/@opendirectory.dev/skills)
[![Skills](https://img.shields.io/badge/skills-55-blue.svg?style=flat-square)](skills/)
[![Stars](https://img.shields.io/github/stars/Varnan-Tech/opendirectory?style=flat-square&color=yellow)](https://github.com/Varnan-Tech/opendirectory/stargazers)
[![Contributors](https://img.shields.io/github/contributors/Varnan-Tech/opendirectory?style=flat-square&color=orange)](https://github.com/Varnan-Tech/opendirectory/graphs/contributors)
[![Agents](https://img.shields.io/badge/agents-7-blueviolet.svg?style=flat-square)](#quick-start)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

</div>

---

## What is OpenDirectory?

OpenDirectory is a central library of AI Agent Skills. Each skill is a pre-built set of instructions and context you install directly into your AI agent. Install a skill and your agent gains expert-level domain knowledge for complex GTM, marketing, and growth tasks.

<br>

### 1. Browse
```bash
npx "@opendirectory.dev/skills" list
```
*Explore our growing library of 55 specialized skills*

### 2. Pick your agent
```bash
--target claude
```
*Supports Claude, OpenCode, Codex, Gemini, Anti-Gravity, OpenClaw, Hermes*

### 3. Install
```bash
npx "@opendirectory.dev/skills" install <skill> --target claude
```
*Equips your agent with specialized knowledge, tools, and prompts for the task*

---

## Popular Agent Skills

<div align="center"><sub>Ranked by artifact quality and practical value. Install any skill in under 30 seconds.</sub></div>

<br>

<table>
  <tr>
    <td valign="top" width="50%">
      <a href="skills/blog-cover-image-cli"><b>blog-cover-image-cli</b></a>
      <br>
      1200×630px blog cover with self-healing QA loop, retries up to 3× with vision feedback.
    </td>
    <td valign="top" width="50%">
      <a href="skills/brand-alchemy"><b>brand-alchemy</b></a>
      <br>
      World-class brand strategist and naming expert.
    </td>
  </tr>
  <tr>
    <td valign="top">
      <a href="skills/cold-email-verifier"><b>cold-email-verifier</b></a>
      <br>
      Verify cold emails, enrich lead lists, or autonomously guess email addresses from a CSV.
    </td>
    <td valign="top">
      <a href="skills/cook-the-blog"><b>cook-the-blog</b></a>
      <br>
      Generate high-converting, deep-dive growth case studies in MDX format.
    </td>
  </tr>
  <tr>
    <td valign="top">
      <a href="skills/email-newsletter"><b>email-newsletter</b></a>
      <br>
      Drafts and designs a complete HTML email newsletter from a topic or content brief.
    </td>
    <td valign="top">
      <a href="skills/human-tone"><b>human-tone</b></a>
      <br>
      Rewrites AI marketing copy against 18 GTM slop patterns with before/after audit notes.
    </td>
  </tr>
  <tr>
    <td valign="top">
      <a href="skills/meta-tribeV2-skill"><b>meta-tribeV2-skill</b></a>
      <br>
      Analyzes video hooks and scripts using Meta's TRIBE v2 fMRI model for neuro-marketing breakdown.
    </td>
    <td valign="top">
      <a href="skills/npm-downloads-to-leads"><b>npm-downloads-to-leads</b></a>
      <br>
      Velocity scoring on npm download data surfaces breakout maintainers with personalized outreach briefs.
    </td>
  </tr>
  <tr>
    <td valign="top">
      <a href="skills/position-me"><b>position-me</b></a>
      <br>
      Elite Website Reviewer Agent for AEO, GEO, SEO, UI/UX Psychology, and Copywriting.
    </td>
    <td valign="top">
      <a href="skills/twitter-GTM-find-skill"><b>twitter-GTM-find-skill</b></a>
      <br>
      End-to-end pipeline for scraping Twitter for GTM/DevRel tech startup jobs using Apify.
    </td>
  </tr>
  <tr>
    <td valign="top">
      <a href="skills/yc-intent-radar-skill"><b>yc-intent-radar-skill</b></a>
      <br>
      Scrape daily job listings from YCombinator's Workatastartup platform without duplicates.
    </td>
    <td valign="top">
      <a href="skills/pricing-page-psychology-audit"><b>pricing-page-psychology-audit</b></a>
      <br>
      Audits any SaaS pricing page against 12 pricing psychology principles with ranked improvement reports.
    </td>
  </tr>
</table>

---

## Quick Start

**1. View available skills:**
```bash
npx "@opendirectory.dev/skills" list
```

**2. Pick your agent:**

| Agent | Flag |
|---|---|
| Claude Code | `--target claude` |
| OpenCode | `--target opencode` |
| Codex | `--target codex` |
| Gemini CLI | `--target gemini` |
| Anti-Gravity | `--target anti-gravity` |
| OpenClaw | `--target openclaw` |
| Hermes | `--target hermes` |

**3. Install a skill:**
```bash
npx "@opendirectory.dev/skills" install <skill-name> --target <your-agent>
```

> **Requires Node.js.** Download from [nodejs.org](https://nodejs.org/) if not installed. `npx` fetches and runs the latest version automatically; no global install needed.

<br>


```bash
npx "@opendirectory.dev/skills" install show-hn-writer --target claude
```
<div align="center">

<sub>Replace <code>show-hn-writer</code> with any skill name. Replace <code>claude</code> with your agent.</sub>

</div>

---

## Installation

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install <skill-name> --target claude
```

### Option B: Claude Desktop App

https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c

**Step 1: Download the skill**

1. Copy the skill folder URL from this GitHub repo.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and press **Enter** to download the ZIP.

**Step 2: Install in Claude**

1. Open your **Claude desktop app**.
2. Go to the sidebar and click **Customize**.
3. Click the **Skills** tab, then click the **+** button.
4. Choose **Upload a skill** and drag in the `.zip` file or the extracted folder.

For some skills, the `SKILL.md` file sits inside a subfolder. Always upload the specific folder containing `SKILL.md`.

### Option C: Claude Code Native

Run these commands inside Claude Code:

```bash
# Add the OpenDirectory marketplace
/plugin marketplace add Varnan-Tech/opendirectory

# Install a skill
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

---

## All Skills

55 skills across GTM, growth automation, technical marketing, and developer tooling.

<!-- SKILLS_LIST_START -->

<summary><b>55 skills across 8 categories</b> — click to expand</summary>
<br>

<table>
  <tr><th colspan="3" align="left">Visual &amp; Media</th></tr>
  <tr><th>Skill</th><th>Description</th><th>Version</th></tr>
  <tr>
    <td><a href="skills/blog-cover-image-cli"><code>blog-cover-image-cli</code></a></td>
    <td>A modern, AI-powered CLI tool designed to automatically generate high-converting, minimalist blog cover images and thumbnails using Gemini 3.1 Flash Image Preview.</td>
    <td><code>1.0.17</code></td>
  </tr>
  <tr>
    <td><a href="skills/graphic-case-study"><code>graphic-case-study</code></a></td>
    <td>Generate a professionally designed case study PDF for B2B SaaS sales and marketing. Structured around the challenge → solution → results → testimonial arc. Outputs a browser-ready HTML file + print-ready PDF. Supports 7 page section layouts and 9 business style presets.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/graphic-chart"><code>graphic-chart</code></a></td>
    <td>Generate publication-quality data visualization charts as PNG using Chart.js v4. 8 chart types, 5 style presets, annotation highlights.</td>
    <td><code>2.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/graphic-ebook"><code>graphic-ebook</code></a></td>
    <td>Create professionally designed B2B SaaS e-books (3–10 pages) using HTML + CSS. Supports 9 visual styles and 11 page layout types. Outputs a browser-ready HTML file + print-ready PDF.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/graphic-gif"><code>graphic-gif</code></a></td>
    <td>Generate animated looping GIFs from CSS animations. 800×800px default, 6 animation types, 4 style presets.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/graphic-slide-deck"><code>graphic-slide-deck</code></a></td>
    <td>Generate a professionally designed HTML slide deck from a brief, content notes, or an existing PowerPoint. Outputs a browser-ready presentation + optional PDF. Supports 13 named layout types and 8 business style presets.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/hyperframes-product-launch-video"><code>hyperframes-product-launch-video</code></a></td>
    <td>A specialized AI agent skill designed for creating elite, premium product launch videos using the Hyperframes framework. This skill distills months of motion design expertise, brand DNA extraction, and technical debugging into a structured workflow that guides your AI agent.</td>
    <td><code>0.0.1</code></td>
  </tr>
  <tr>
    <td><a href="skills/vid-motion-graphics"><code>vid-motion-graphics</code></a></td>
    <td>Generates multi-scene motion graphics as MP4 from a content brief. HTML/CSS animations rendered frame-by-frame in headless Chromium via Playwright, assembled with FFmpeg. No React, no AI APIs, no Python.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/vid-product-launch"><code>vid-product-launch</code></a></td>
    <td>Generate a cinematic product launch video from a product description and launch context. The video follows a 5-section narrative arc: build anticipation, reveal the product, prove the value, and close with a CTA.</td>
    <td><code>1.2.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/vid-sizzle-reel"><code>vid-sizzle-reel</code></a></td>
    <td>Generate a high-energy sizzle reel or hype video from brand assets and key messages. Fast-paced montage format with dynamic cuts, bold text overlays, and optional beat-synced music.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr><th colspan="3" align="left">Content</th></tr>
  <tr><th>Skill</th><th>Description</th><th>Version</th></tr>
  <tr>
    <td><a href="skills/cook-the-blog"><code>cook-the-blog</code></a></td>
    <td>This guide explains how to set up, configure, and run the cook-the-blog skill. This AI agent pipeline autonomously researches companies, extracts SEO keywords, generates custom cover images, writes high-converting MDX case studies without AI fluff, uploads assets to cloud storage, and pushes the final code to your designated GitHub repository.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/email-newsletter"><code>email-newsletter</code></a></td>
    <td>Draft and design a complete HTML email newsletter from a topic or content brief. Output is paste-ready for Loops, Mailchimp, Beehiiv, Resend, or any standard email platform.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/human-tone"><code>human-tone</code></a></td>
    <td>AI assistants write terrible marketing copy. They rely on generic filler words, force everything into lists of three, and bury your actual product under layers of hype.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/linkedin-post-generator"><code>linkedin-post-generator</code></a></td>
    <td>Generate LinkedIn posts from any content: blog posts, articles, GitHub PRs, or a description of what you built. The agent reads your source material, applies LinkedIn's content patterns, and produces a post with the right hook, story arc, and formatting.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/newsletter-digest"><code>newsletter-digest</code></a></td>
    <td>Aggregate RSS feeds, synthesize the week's top stories with Gemini, and publish a newsletter digest to Ghost CMS. Supports three digest formats and outputs HTML, Markdown, and plain text for any platform.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/noise-to-linkedin-carousel"><code>noise-to-linkedin-carousel</code></a></td>
    <td>noise-to-linkedin-carousel turns rough notes, transcripts, and idea dumps into a LinkedIn-ready carousel content pack with a strong hook, clear slide-by-slide structure, and a CTA — built for founders, GTM teams, and technical marketers who think faster than they write.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/noise2blog"><code>noise2blog</code></a></td>
    <td>Paste your rough notes, bullet points, voice transcript, or tweet dump and get a publication-ready blog post.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/tweet-thread-from-blog"><code>tweet-thread-from-blog</code></a></td>
    <td>Turn any blog post or article into a Twitter/X thread. The agent reads the content, picks the right thread style, and writes 7-10 tweets with a strong hook, one insight per tweet, and a CTA. Optionally posts the full thread to X via Composio using a reply chain.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr><th colspan="3" align="left">Launch</th></tr>
  <tr><th>Skill</th><th>Description</th><th>Version</th></tr>
  <tr>
    <td><a href="skills/brand-alchemy"><code>brand-alchemy</code></a></td>
    <td>World-class brand strategist and naming expert. Uses an interrogation-led discovery phase to extract your brand's DNA, then applies scientific naming frameworks (Phonosemantics) and automated multi-TLD domain checking.</td>
    <td><code>0.0.1</code></td>
  </tr>
  <tr>
    <td><a href="skills/oss-launch-kit"><code>oss-launch-kit</code></a></td>
    <td>The high-level OSS Launch Orchestrator for GitHub repositories. It serves as the strategic entry point that analyzes your repo and coordinates a multi-channel launch plan.</td>
    <td><code>0.2.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/product-update-logger"><code>product-update-logger</code></a></td>
    <td>Tell the skill what your product shipped. It writes a polished, living docs/changelog.md entry and hands you a ready-to-use content package: tweet thread, LinkedIn post, email snippet, and one-liner.</td>
    <td><code>0.0.1</code></td>
  </tr>
  <tr>
    <td><a href="skills/producthunt-launch-kit"><code>producthunt-launch-kit</code></a></td>
    <td>Generates a complete Product Hunt launch kit from your product description: tagline variants (60 chars max), listing description, maker comment, launch day tweet thread, LinkedIn post, and a 4-email sequence.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/show-hn-writer"><code>show-hn-writer</code></a></td>
    <td>Draft a Show HN post (title + body) that follows Hacker News norms: specific, honest, first-person, no marketing. Generates three title variants and a complete body, then runs a Gemini review to catch HN anti-patterns before you post.</td>
    <td><code>2.0.0</code></td>
  </tr>
  <tr><th colspan="3" align="left">GTM Intelligence</th></tr>
  <tr><th>Skill</th><th>Description</th><th>Version</th></tr>
  <tr>
    <td><a href="skills/competitor-pr-finder"><code>competitor-pr-finder</code></a></td>
    <td>Give it your product URL. It finds your top 5 competitors, researches every press mention, podcast appearance, and community post across all of them, and tells you exactly which channels to pitch -- with the journalist's name, the angle that got your competitors featured, and a ready-to-send cold pitch for your product.</td>
    <td><code>0.0.1</code></td>
  </tr>
  <tr>
    <td><a href="skills/gh-issue-to-demand-signal"><code>gh-issue-to-demand-signal</code></a></td>
    <td>Give the skill a competitor's public GitHub repo URL. It fetches their open issues, filters noise locally, clusters into 6 demand categories using the AI already running the skill, scores by real engagement (reactions), detects ignored demand (high reactions + no response = your opportunity), and outputs a ranked demand gap report with a GTM messaging brief.</td>
    <td><code>0.0.1</code></td>
  </tr>
  <tr>
    <td><a href="skills/google-trends-api-skills"><code>google-trends-api-skills</code></a></td>
    <td>Agent Skills for SEO keyword research using Google Trends data via SerpApi. Built for AI agents that generate tech and developer-focused blog content.</td>
    <td><code>2.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/hackernews-intel"><code>hackernews-intel</code></a></td>
    <td>Monitor Hacker News for keywords. Get a Slack alert every time a new post matches your topics, without duplicates. Run it manually, on a cron schedule, or via GitHub Actions.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/map-your-market"><code>map-your-market</code></a></td>
    <td>Give this skill a product description, category keywords, or competitor names. It searches Reddit, Hacker News, GitHub Issues, G2, and Google Trends for real pain signals from your market -- then builds a complete positioning framework: who your ICP is, what they say out loud, and how to talk to them.</td>
    <td><code>0.0.1</code></td>
  </tr>
  <tr>
    <td><a href="skills/meta-ads-skill"><code>meta-ads-skill</code></a></td>
    <td>npx "@opendirectory.dev/skills" install meta-ads-skill --target claude</td>
    <td><code>0.0.1</code></td>
  </tr>
  <tr>
    <td><a href="skills/meta-tribeV2-skill"><code>meta-tribeV2-skill</code></a></td>
    <td>AI Skill that uses Meta's TRIBE v2 fMRI Model to analyze the neuroscience of video hooks, reels, and scripts.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/npm-downloads-to-leads"><code>npm-downloads-to-leads</code></a></td>
    <td>Give this skill a list of npm packages. It fetches 12 weeks of download data, scores each package by growth velocity, maps maintainers to GitHub and Twitter, and outputs a ranked lead brief per breakout package: who built it, how to reach them, and what to say.</td>
    <td><code>0.0.1</code></td>
  </tr>
  <tr>
    <td><a href="skills/reddit-icp-monitor"><code>reddit-icp-monitor</code></a></td>
    <td>Watch subreddits for people describing the exact problem you solve. Score each post for ICP relevance. Draft a helpful, non-spammy reply for every high-signal match.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/reddit-post-engine"><code>reddit-post-engine</code></a></td>
    <td>Write and optionally post Reddit content that fits the target subreddit's culture. Fetches subreddit rules and top posts before drafting. Follows the 90/10 rule. Optionally posts via Composio Reddit MCP.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/sdk-adoption-tracker"><code>sdk-adoption-tracker</code></a></td>
    <td>Give this skill an SDK or library name. It searches GitHub for public repos that import it, scores each repo by company signal and activity, identifies who is building on you in production, and outputs a ranked adoption report with outreach context for high-signal company repos.</td>
    <td><code>0.0.1</code></td>
  </tr>
  <tr>
    <td><a href="skills/twitter-GTM-find-skill"><code>twitter-GTM-find-skill</code></a></td>
    <td>This repository contains the twitter-GTM-find/ AI Skill.</td>
    <td><code>0.0.1</code></td>
  </tr>
  <tr>
    <td><a href="skills/yc-intent-radar-skill"><code>yc-intent-radar-skill</code></a></td>
    <td>An automated scraper that pulls job listings and company data from YCombinator's Workatastartup platform. It bypasses login bottlenecks by utilizing authenticated sessions and ensures no duplicates are recorded by saving everything directly to a local SQLite database (jobs.db).</td>
    <td><code>0.0.1</code></td>
  </tr>
  <tr><th colspan="3" align="left">Outreach</th></tr>
  <tr><th>Skill</th><th>Description</th><th>Version</th></tr>
  <tr>
    <td><a href="skills/cold-email-verifier"><code>cold-email-verifier</code></a></td>
    <td>Agent Skill that equips your AI agent with the ability to autonomously guess, enrich, and verify cold email addresses directly from a CSV file.</td>
    <td><code>0.0.1</code></td>
  </tr>
  <tr>
    <td><a href="skills/outreach-sequence-builder"><code>outreach-sequence-builder</code></a></td>
    <td>Turn a buying signal into a ready-to-send multi-channel outreach sequence. Give the skill a signal and it generates 4-6 personalized touchpoints across email, LinkedIn, and phone, with objection pre-emption built in.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr><th colspan="3" align="left">Research</th></tr>
  <tr><th>Skill</th><th>Description</th><th>Version</th></tr>
  <tr>
    <td><a href="skills/linkedin-job-post-to-buyer-pain-map"><code>linkedin-job-post-to-buyer-pain-map</code></a></td>
    <td>Turn LinkedIn job posts into an actionable buyer pain map with signal strength, urgency, and outreach angles for each account.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/meeting-brief-generator"><code>meeting-brief-generator</code></a></td>
    <td>Walk into every sales or business development call prepared. Give the skill a company name and it runs targeted research, synthesizes a 1-page brief, and optionally saves it to Notion.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/position-me"><code>position-me</code></a></td>
    <td>The Website Reviewer Agent Skill for AEO, GEO, SEO, UI/UX Psychology, and Direct Response Copywriting.</td>
    <td><code>0.0.1</code></td>
  </tr>
  <tr>
    <td><a href="skills/pricing-finder"><code>pricing-finder</code></a></td>
    <td>Tell it what your product is (URL or description). It finds 5 competitors globally, fetches their actual pricing pages, and returns a complete pricing intelligence report: the dominant pricing model in your space, a benchmark price table, feature gate analysis, a competitive positioning map, and a concrete recommended pricing strategy for your product.</td>
    <td><code>0.0.1</code></td>
  </tr>
  <tr>
    <td><a href="skills/pricing-page-psychology-audit"><code>pricing-page-psychology-audit</code></a></td>
    <td>Paste any SaaS pricing page URL. Get a full audit against 12 pricing</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/vc-curated-match"><code>vc-curated-match</code></a></td>
    <td>Identify targeted VC funds based on a product's description and URL. This skill matches project inputs to a curated dataset of top global venture capital firms based on industry tags, stage, and geography.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/vc-finder"><code>vc-finder</code></a></td>
    <td>Give the skill a product URL or description. It detects the industry and funding stage, identifies 5 comparable funded companies, searches who backed those companies (Track A), finds VCs who publish investment theses about this space (Track B), and returns a ranked sourced investor list with deep-dives and outreach hooks.</td>
    <td><code>0.0.1</code></td>
  </tr>
  <tr>
    <td><a href="skills/where-your-customer-lives"><code>where-your-customer-lives</code></a></td>
    <td>Give this skill a product utility and ICP. It searches Reddit, Hacker News, and DuckDuckGo to find the specific communities where your customer actually gathers -- then builds a per-channel playbook: evidence your ICP is there, one entry tactic, one content angle, and specific anti-patterns.</td>
    <td><code>0.0.1</code></td>
  </tr>
  <tr><th colspan="3" align="left">Developer Tools</th></tr>
  <tr><th>Skill</th><th>Description</th><th>Version</th></tr>
  <tr>
    <td><a href="skills/claude-md-generator"><code>claude-md-generator</code></a></td>
    <td>Reads your codebase and writes a CLAUDE.md that gives Claude Code the context it needs: build commands, code conventions, architecture notes, and gotchas. Stays under 200 lines.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/dependency-update-bot"><code>dependency-update-bot</code></a></td>
    <td>Weekly scan for outdated npm or pip packages. Fetches changelogs for each. Summarizes breaking changes with Gemini. Opens one PR per risk group.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/docs-from-code"><code>docs-from-code</code></a></td>
    <td>Automatically generate and maintain README.md, API reference docs, and an Architecture section by reading your codebase. Uses graphify to build a knowledge graph first, then uses AI to write clean documentation grounded in what actually exists.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/explain-this-pr"><code>explain-this-pr</code></a></td>
    <td>Point this skill at any GitHub PR and it writes a plain-English explanation of what changed and why, then posts it as a PR comment.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/kill-the-standup"><code>kill-the-standup</code></a></td>
    <td>Write your daily standup in seconds. The skill reads yesterday's Linear issues and GitHub commits, formats a done/doing/blockers update, and posts it to Slack.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/llms-txt-generator"><code>llms-txt-generator</code></a></td>
    <td>Generate a standards-compliant llms.txt file for any website. Makes your site fully readable and citable by AI agents the GEO (Generative Engine Optimization) equivalent of having a great sitemap.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/pr-description-writer"><code>pr-description-writer</code></a></td>
    <td>Read your current git branch diff and generate a complete GitHub pull request description: summary, specific change bullets, and testing steps. Create or update the PR in one step.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr>
    <td><a href="skills/schema-markup-generator"><code>schema-markup-generator</code></a></td>
    <td>Generate valid JSON-LD structured data for any webpage. The agent crawls the page, detects which schema types apply, and outputs a script tag ready to paste into your HTML. Optionally opens a GitHub PR with the markup injected.</td>
    <td><code>1.0.0</code></td>
  </tr>
  <tr><th colspan="3" align="left">Other</th></tr>
  <tr><th>Skill</th><th>Description</th><th>Version</th></tr>
  <tr>
    <td><a href="skills/domain-expired-opportunity-finder"><code>domain-expired-opportunity-finder</code></a></td>
    <td>Evaluate expired domain candidates against your niche. Get a conservative,</td>
    <td><code>1.0.0</code></td>
  </tr>
</table>


<!-- SKILLS_LIST_END -->

---

## How to Contribute

We welcome skills across GTM, growth automation, and developer tooling.

> **Top contributors receive OpenDirectory swag.** Limited-edition merchandise shipped to you.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the required format and the security validation process.

---

## Top Contributors

<a href="https://github.com/Varnan-Tech/opendirectory/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Varnan-Tech/opendirectory" />
</a>

Thank you to every contributor. See [CONTRIBUTING.md](CONTRIBUTING.md) to get involved.

---

## License

This project is licensed under the MIT License.
