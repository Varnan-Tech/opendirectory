<div align="center">
  <img src="docs/assets/opendirectory_banner.webp" width="100%" alt="OpenDirectory Banner" />
</div>

<br />

<div align="center">
  <strong>A curated registry and CLI for AI Agent Skills, meticulously designed for Go-To-Market (GTM), Technical Marketing, and growth automation.</strong>
</div>

<div align="center">

[![npm version](https://img.shields.io/npm/v/@opendirectory.dev/skills.svg?style=flat-square)](https://www.npmjs.com/package/@opendirectory.dev/skills)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

</div>

---

## What is OpenDirectory?

OpenDirectory is a central library that allows you to add new capabilities, or superpowers, to your AI agents. Instead of teaching your AI how to perform complex marketing or growth tasks from scratch, you can simply download a pre-built skill from our catalog and install it directly into your project.

## Available Skills

<!-- SKILLS_LIST_START -->

| Skill Name | Description | Version |
|---|---|---|
| [`blog-cover-image-cli`](skills/blog-cover-image-cli) | Use when the user asks to generate a blog cover image, thumbnail, or article header. | `1.0.17` |
| [`brand-alchemy`](skills/brand-alchemy) | World-class brand strategist and naming expert. | `0.0.1` |
| [`claude-md-generator`](skills/claude-md-generator) | Read the codebase. Write a CLAUDE.md that tells Claude exactly what it needs: no more, no less. | `1.0.0` |
| [`cold-email-verifier`](skills/cold-email-verifier) | Use when the user wants to verify cold emails, enrich a lead list, or autonomously guess email addresses from a CSV using ValidEmail. | `0.0.1` |
| [`cook-the-blog`](skills/cook-the-blog) | Generate high-converting, deep-dive growth case studies in MDX format. | `1.0.0` |
| [`dependency-update-bot`](skills/dependency-update-bot) | Scans your project for outdated npm, pip, Cargo, Go, or Ruby packages. | `1.0.0` |
| [`docs-from-code`](skills/docs-from-code) | Generates and updates README. | `1.0.0` |
| [`explain-this-pr`](skills/explain-this-pr) | Takes a GitHub PR URL or the current branch and writes a plain-English explanation of what it does and why, then posts it as a PR comment. | `1.0.0` |
| [`gh-issue-to-demand-signal`](skills/gh-issue-to-demand-signal) | Takes a competitor's public GitHub repo URL, fetches their open issues via the GitHub REST API, filters noise locally, clusters issues into 6 deman... | `0.0.1` |
| [`google-trends-api-skills`](skills/google-trends-api-skills) | SEO keyword research workflow for blog generation using Google Trends data. | `2.0` |
| [`hackernews-intel`](skills/hackernews-intel) | Monitors Hacker News for user-configured keywords, deduplicates against a local SQLite cache, and sends Slack alerts for new matching posts. | `1.0.0` |
| [`human-tone`](skills/human-tone) | Rewrites AI-generated marketing copy to sound naturally human. | `1.0.0` |
| [`kill-the-standup`](skills/kill-the-standup) | Reads yesterday's Linear issues and GitHub commits for the authenticated user, formats a standup update (done / doing / blockers), and posts it to... | `1.0.0` |
| [`linkedin-post-generator`](skills/linkedin-post-generator) | Converts any content, blog post URL, pasted article, GitHub PR description, or a description of something built, into a formatted LinkedIn post wit... | `1.0.0` |
| [`llms-txt-generator`](skills/llms-txt-generator) | Generates and maintains a standards-compliant llms. | `1.0.0` |
| [`map-your-market`](skills/map-your-market) | Given a product description, category keywords, or competitor names (any combination), searches Reddit, Hacker News, GitHub Issues, G2, and Google... | `0.0.1` |
| [`meeting-brief-generator`](skills/meeting-brief-generator) | Takes a company name and optional contact, runs targeted research via Tavily, synthesizes a 1-page pre-call brief with Gemini, and optionally saves... | `1.0.0` |
| [`meta-ads-skill`](skills/meta-ads-skill) | Use when interacting with the Meta Ads MCP server to manage accounts, campaigns, ads, insights, and targeting, or to troubleshoot OAuth token authe... | `0.0.1` |
| [`newsletter-digest`](skills/newsletter-digest) | Aggregates RSS feeds from the past week, synthesizes the top stories using Gemini, and publishes a newsletter digest to Ghost CMS. | `1.0.0` |
| [`noise2blog`](skills/noise2blog) | Turns rough notes, bullet points, voice transcripts, or tweet dumps into a polished, publication-ready blog post. | `1.0.0` |
| [`npm-downloads-to-leads`](skills/npm-downloads-to-leads) | Takes a list of npm package names (yours or competitors'), fetches 12 weeks of daily download data from the npm API, computes a breakout velocity s... | `0.0.1` |
| [`outreach-sequence-builder`](skills/outreach-sequence-builder) | Takes a buying signal and generates a personalized multi-channel outreach sequence across email, LinkedIn, and phone. | `1.0.0` |
| [`position-me`](skills/position-me) | Elite Website Reviewer Agent for AEO, GEO, SEO, UI/UX Psychology, and Copywriting. | `0.0.1` |
| [`pr-description-writer`](skills/pr-description-writer) | Read the current branch diff and write a complete GitHub pull request description. Create or update the PR with one command. | `1.0.0` |
| [`pricing-page-psychology-audit`](skills/pricing-page-psychology-audit) | Audits any SaaS pricing page URL against 12 pricing psychology principles and outputs a ranked improvement report with specific rewrite suggestions... | `1.0.0` |
| [`producthunt-launch-kit`](skills/producthunt-launch-kit) | Generate every asset you need for a Product Hunt launch: listing copy, maker comment, and day-one social posts. | `1.0.0` |
| [`reddit-icp-monitor`](skills/reddit-icp-monitor) | Watches subreddits for people describing the exact problem you solve, scores their relevance to your ICP, and drafts a helpful non-spammy reply for... | `1.0.0` |
| [`reddit-post-engine`](skills/reddit-post-engine) | Writes and optionally posts a Reddit post for any subreddit, following that subreddit's specific culture and rules. | `1.0.0` |
| [`schema-markup-generator`](skills/schema-markup-generator) | You are an SEO engineer specialising in structured data. | `1.0.0` |
| [`sdk-adoption-tracker`](skills/sdk-adoption-tracker) | Given your SDK or library name, searches GitHub code search for public repos that import or require it, classifies each repo as company org, affili... | `0.0.1` |
| [`show-hn-writer`](skills/show-hn-writer) | Draft a Show HN post backed by real HN performance data. Uses observed patterns from 250 top HN posts to maximise score. | `2.0.0` |
| [`tweet-thread-from-blog`](skills/tweet-thread-from-blog) | Converts a blog post URL or article into a Twitter/X thread with a strong hook, one insight per tweet, and a CTA. | `1.0.0` |
| [`twitter-GTM-find-skill`](skills/twitter-GTM-find-skill) | End-to-end pipeline for scraping Twitter for GTM/DevRel tech startup jobs using Apify, and validating them against an Ideal Customer Profile (ICP)... | `0.0.1` |
| [`vc-finder`](skills/vc-finder) | Takes a startup product URL or description, detects the industry and funding stage, identifies 5 comparable funded companies, searches who invested... | `0.0.1` |
| [`where-your-customer-lives`](skills/where-your-customer-lives) | Given a product utility and ICP, researches the internet to find the specific channels. | `0.0.1` |
| [`yc-intent-radar-skill`](skills/yc-intent-radar-skill) | Scrape daily job listings from YCombinator's Workatastartup platform without duplicates. | `0.0.1` |

<!-- SKILLS_LIST_END -->

## Prerequisites

Before you begin, you must have Node.js installed on your computer. Node.js provides the necessary tools to download and run these skills.

1. Visit [nodejs.org](https://nodejs.org/).
2. Download and install the version labeled Recommended For Most Users.
3. Once installed, you will have access to a tool called terminal or command prompt on your computer, which you will use for the following steps.

## Installation (Zero-Install Required)

Because we use `npx`, there is no need to install the OpenDirectory tool itself. `npx` is a magic command that comes with Node.js. When you type `npx "@opendirectory.dev/skills"`, your computer automatically downloads the registry in the background and runs it instantly.

## Native Installation (Claude Code Only)

Users who exclusively use Anthropic's Claude Code can add OpenDirectory as a native community marketplace directly inside their Claude interface. This allows you to install skills using Claude's built-in plugin system.

Run the following commands inside your Claude Code terminal:

```bash
# Add the OpenDirectory marketplace
/plugin marketplace add Varnan-Tech/opendirectory

# Install a skill directly
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

## Installation in Claude Desktop App

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

> **Note:** For some skills (like `position-me`), the `SKILL.md` file might be located inside a subfolder. Always make sure you are uploading the specific folder that contains the `SKILL.md` file!

## Step 1: View Available Skills

To see the full list of available skills, open your terminal and run the following command:

```bash
npx "@opendirectory.dev/skills" list
```

This command will display a list of all skills currently available in the OpenDirectory registry.

## Step 2: Choose Your Agent

OpenDirectory supports several different AI agents. When you install a skill, you need to tell the system which agent you are using by using the `--target` flag.

Supported agents include:

*   **Claude Code**: Use `--target claude`
*   **OpenCode**: Use `--target opencode`
*   **Codex**: Use `--target codex`
*   **Gemini CLI**: Use `--target gemini`
*   **Anti-Gravity**: Use `--target anti-gravity`
*   **OpenClaw**: Use `--target openclaw`
*   **Hermes**: Use `--target hermes`

## Step 3: Install a Skill

Once you have found a skill you want to use, run the following command in your terminal, replacing `<skill-name>` with the name of the skill and `<your-agent>` with the agent you chose in Step 2:

```bash
npx "@opendirectory.dev/skills" install <skill-name> --target <your-agent>
```

This command installs the skill into your agent's global configuration directory, making it available across all your projects.

## How to Use the Skills

After the installation is complete, your AI agent is ready to use the new skill. Simply open your AI agent (such as Claude Code) within your project folder and give it a command related to the skill.

For example, if you installed a skill for SEO analysis, you might say:
"Use the SEO analysis skill to check the homepage of my website."

## Why NPX?

We use a tool called `npx` to manage these skills. This ensures that every time you run a command, you are automatically using the most recent version of the skill and the latest security updates. You never have to worry about manually updating your software.

## How to Contribute

We welcome contributions from the community. If you have built an innovative GTM, Technical Marketing, or growth automation skill, we encourage you to share it with the ecosystem.

Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on the strict format required for new skills and our security validation process.

## Top Contributors

<a href="https://github.com/Varnan-Tech/opendirectory/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Varnan-Tech/opendirectory" />
</a>

A massive thank you to everyone who has helped build the OpenDirectory ecosystem! Join us by checking out the [CONTRIBUTING.md](CONTRIBUTING.md) guide.

## License

This project is licensed under the MIT License.
