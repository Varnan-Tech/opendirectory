<div align="center">
  <img src="docs/assets/opendirectory_banner.webp" width="100%" alt="OpenDirectory Banner" />
</div>

<br />

<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&duration=3000&pause=800&color=58A6FF&center=true&vCenter=true&width=620&height=50&lines=55+Agent+Skills;Works+with+Claude%2C+Codex%2C+Gemini+CLI;Agent+Skills+for+Founders+Who+Hate+Marketing;Install+in+seconds.+No+setup+required." alt="Typing SVG" />
</div>

<br />

<div align="center">

[![npm version](https://img.shields.io/npm/v/@opendirectory.dev/skills.svg?style=flat-square)](https://www.npmjs.com/package/@opendirectory.dev/skills)
[![Skills](https://img.shields.io/badge/skills-56-blue.svg?style=flat-square)](skills/)
[![Stars](https://img.shields.io/github/stars/Varnan-Tech/opendirectory?style=flat-square&color=yellow)](https://github.com/Varnan-Tech/opendirectory/stargazers)
[![Contributors](https://img.shields.io/github/contributors/Varnan-Tech/opendirectory?style=flat-square&color=orange)](https://github.com/Varnan-Tech/opendirectory/graphs/contributors)
[![Agents](https://img.shields.io/badge/agents-7-blueviolet.svg?style=flat-square)](#quick-start)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

</div>

---

## What is OpenDirectory?

OpenDirectory is a library of agent skills for founders who hate marketing. Each skill is a pre-built set of instructions and context you install directly into your AI agent. Install a skill and your agent gains expert-level domain knowledge for complex GTM, marketing, and growth tasks.

<br>

### 1. Browse (Interactive)
```bash
npx "@opendirectory.dev/skills"
```
*Interactive TUI browser - browse by category, search, and install in one session*

Or list all skills:
```bash
npx "@opendirectory.dev/skills" list
```
*56 specialized skills across GTM, growth, and developer tooling*

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
      Find X/Twitter GTM hiring signals with Apify, plus optional TweetClaw discovery for OpenClaw.
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

**1. Browse interactively (recommended):**
```bash
npx "@opendirectory.dev/skills"
```
*Opens a full-screen TUI browser with categories, search, and install flow*

Or list all skills:
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

56 skills across GTM, growth automation, technical marketing, and developer tooling.

<!-- SKILLS_LIST_START -->

| Skill Name | Description | Version |
|---|---|---|
| [`app-store-review-arbitrage`](skills/app-store-review-arbitrage) | No description provided. | `1.0.0` |
| [`blog-cover-image-cli`](skills/blog-cover-image-cli) | Use when the user asks to generate a blog cover image, thumbnail, or article header. | `1.0.17` |
| [`claude-md-generator`](skills/claude-md-generator) | Read the codebase. Write a CLAUDE.md that tells Claude exactly what it needs: no more, no less. | `1.0.0` |
| [`cold-email-verifier`](skills/cold-email-verifier) | Use when the user wants to verify cold emails, enrich a lead list, or autonomously guess email addresses from a CSV using ValidEmail. | `0.0.1` |
| [`cook-the-blog`](skills/cook-the-blog) | Generate high-converting, deep-dive growth case studies in MDX format. | `1.0.0` |
| [`dependency-update-bot`](skills/dependency-update-bot) | Scans your project for outdated npm, pip, Cargo, Go, or Ruby packages. | `1.0.0` |
| [`docs-from-code`](skills/docs-from-code) | Generates and updates README. | `1.0.0` |
| [`explain-this-pr`](skills/explain-this-pr) | Takes a GitHub PR URL or the current branch and writes a plain-English explanation of what it does and why, then posts it as a PR comment. | `1.0.0` |
| [`google-trends-api-skills`](skills/google-trends-api-skills) | SEO keyword research workflow for blog generation using Google Trends data. | `2.0` |
| [`hackernews-intel`](skills/hackernews-intel) | Monitors Hacker News for user-configured keywords, deduplicates against a local SQLite cache, and sends Slack alerts for new matching posts. | `1.0.0` |
| [`human-tone`](skills/human-tone) | Rewrites AI-generated marketing copy to sound naturally human. | `1.0.0` |
| [`kill-the-standup`](skills/kill-the-standup) | Reads yesterday's Linear issues and GitHub commits for the authenticated user, formats a standup update (done / doing / blockers), and posts it to... | `1.0.0` |
| [`linkedin-post-generator`](skills/linkedin-post-generator) | Converts any content, blog post URL, pasted article, GitHub PR description, or a description of something built, into a formatted LinkedIn post wit... | `1.0.0` |
| [`llms-txt-generator`](skills/llms-txt-generator) | Generates and maintains a standards-compliant llms. | `1.0.0` |
| [`meeting-brief-generator`](skills/meeting-brief-generator) | Takes a company name and optional contact, runs targeted research via Tavily, synthesizes a 1-page pre-call brief with Gemini, and optionally saves... | `1.0.0` |
| [`meta-ads-skill`](skills/meta-ads-skill) | Use when interacting with the Meta Ads MCP server to manage accounts, campaigns, ads, insights, and targeting, or to troubleshoot OAuth token authe... | `0.0.1` |
| [`newsletter-digest`](skills/newsletter-digest) | Aggregates RSS feeds from the past week, synthesizes the top stories using Gemini, and publishes a newsletter digest to Ghost CMS. | `1.0.0` |
| [`noise2blog`](skills/noise2blog) | Turns rough notes, bullet points, voice transcripts, or tweet dumps into a polished, publication-ready blog post. | `1.0.0` |
| [`outreach-sequence-builder`](skills/outreach-sequence-builder) | Takes a buying signal and generates a personalized multi-channel outreach sequence across email, LinkedIn, and phone. | `1.0.0` |
| [`position-me`](skills/position-me) | Elite Website Reviewer Agent for AEO, GEO, SEO, UI/UX Psychology, and Copywriting. | `0.0.1` |
| [`pr-description-writer`](skills/pr-description-writer) | Read the current branch diff and write a complete GitHub pull request description. Create or update the PR with one command. | `1.0.0` |
| [`producthunt-launch-kit`](skills/producthunt-launch-kit) | Generate every asset you need for a Product Hunt launch: listing copy, maker comment, and day-one social posts. | `1.0.0` |
| [`reddit-icp-monitor`](skills/reddit-icp-monitor) | Watches subreddits for people describing the exact problem you solve, scores their relevance to your ICP, and drafts a helpful non-spammy reply for... | `1.0.0` |
| [`reddit-post-engine`](skills/reddit-post-engine) | Writes and optionally posts a Reddit post for any subreddit, following that subreddit's specific culture and rules. | `1.0.0` |
| [`schema-markup-generator`](skills/schema-markup-generator) | You are an SEO engineer specialising in structured data. | `1.0.0` |
| [`show-hn-writer`](skills/show-hn-writer) | Draft a Show HN post backed by real HN performance data. Uses observed patterns from 250 top HN posts to maximise score. | `2.0.0` |
| [`tweet-thread-from-blog`](skills/tweet-thread-from-blog) | Converts a blog post URL or article into a Twitter/X thread with a strong hook, one insight per tweet, and a CTA. | `1.0.0` |
| [`twitter-GTM-find-skill`](skills/twitter-GTM-find-skill) | End-to-end pipeline for scraping Twitter for GTM/DevRel tech startup jobs using Apify, and validating them against an Ideal Customer Profile (ICP)... | `0.0.1` |
| [`yc-intent-radar-skill`](skills/yc-intent-radar-skill) | Scrape daily job listings from YCombinator's Workatastartup platform without duplicates. | `0.0.1` |

<!-- SKILLS_LIST_END -->

---

## How to Contribute

We welcome skills across GTM, growth automation, and developer tooling.

> **Top contributors receive OpenDirectory swag.** Limited-edition merchandise shipped to you.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the required format, the security validation process, and please ensure your skill's README includes installation steps, npx install instructions, prerequisites, and usage examples. We provide a helper script at `scripts/update_skill_readmes.py` to auto-generate the standard install section.

---

## Top Contributors

<a href="https://github.com/Varnan-Tech/opendirectory/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Varnan-Tech/opendirectory" />
</a>

Thank you to every contributor. See [CONTRIBUTING.md](CONTRIBUTING.md) to get involved.

---

## License

This project is licensed under the MIT License.
