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
| `blog-cover-generator` | Use when the user asks to generate a blog cover image, thumbnail, or article header. Automatically uses modern typography, brand logos, and Google Search grounding to create beautiful 16:9 images with Gemini 3.1 Flash Image Preview. | `1.0.17` |
| `claude-md-generator` | Read the codebase. Write a CLAUDE.md that tells Claude exactly what it needs: no more, no less. | `1.0.0` |
| `cook-the-blog` | Generate high-converting, deep-dive growth case studies in MDX format. Use this skill when asked to write a case study or blog post about a company's growth, tech stack, or product-led strategy. It handles the full pipeline (researching the company via Tavily, generating a 16:9 cover image, quality checking the draft, uploading assets to cloud storage, and pushing directly to the target repository). | `1.0.0` |
| `dependency-update-bot` | Scans your project for outdated npm, pip, Cargo, Go, or Ruby packages. Runs a CVE security audit. Fetches changelogs, summarizes breaking changes with Gemini, and opens one PR per risk group (patch, minor, major). Includes Diagnosis Mode for install conflicts. Use when asked to update dependencies, check for outdated packages, open dependency PRs, scan for package updates, audit for CVEs, or flag breaking changes in upgrades. Trigger when a user says "check for outdated packages", "update my dependencies", "open PRs for dependency updates", "scan for CVEs", or "which packages need upgrading". | `1.0.0` |
| `docs-from-code` | Generates and updates README.md and API reference docs by reading your codebase's functions, routes, types, schemas, and architecture. Uses graphify to build a knowledge graph first, then writes accurate docs from it. Use when asked to write docs, generate a README, document an API, update stale docs, create an API reference from code, add an architecture section, or document a project in any language. Trigger when a user says their docs are missing, outdated, or wants to document their codebase without writing it manually. | `1.0.0` |
| `explain-this-pr` | Takes a GitHub PR URL or the current branch and writes a plain-English explanation of what it does and why, then posts it as a PR comment. Use when asked to explain a PR, summarize a pull request, write a plain-English description of a PR, add a summary comment to a PR, or understand what a PR changes. Trigger when a user says "explain this PR", "summarize this pull request", "what does this PR do", "add a comment explaining the PR", or shares a GitHub PR URL and asks what it does. | `1.0.0` |
| `seo-keyword-research` | SEO keyword research workflow for blog generation using Google Trends data. Use when writing blog posts, planning content calendars, or optimizing articles for search engines. Finds breakout keywords, builds content structure, and generates SEO-optimized blog outlines targeting tech and developer audiences. | `2.0` |
| `hackernews-intel` | Monitors Hacker News for user-configured keywords, deduplicates against a local SQLite cache, and sends Slack alerts for new matching posts. Use when asked to monitor Hacker News for mentions, track keywords on HN, get alerts when something is posted about a topic on Hacker News, or set up HN keyword monitoring. Trigger when a user mentions Hacker News alerts, HN monitoring, keyword tracking on HN, or wants to know when a topic appears on Hacker News. | `1.0.0` |
| `kill-the-standup` | Reads yesterday's Linear issues and GitHub commits for the authenticated user, formats a standup update (done / doing / blockers), and posts it to Slack. Use when asked to write a standup, generate a standup update, post to the standup channel, summarize yesterday's work, or automate the daily standup. Trigger when a user says "write my standup", "post standup", "generate standup update", "what did I do yesterday", or "kill the standup". | `1.0.0` |
| `linkedin-post-generator` | Converts any content, blog post URL, pasted article, GitHub PR description, or a description of something built, into a formatted LinkedIn post with proper hook, story arc, and formatting. Optionally posts directly to LinkedIn via Composio. Use when asked to write a LinkedIn post, turn a blog into a LinkedIn update, announce a shipped feature, share a case study on LinkedIn, or post something professionally. Trigger when a user mentions LinkedIn, wants to share content professionally, says "post this to LinkedIn", or asks to repurpose a blog/article/PR for social media. | `1.0.0` |
| `llms-txt-generator` | Generates and maintains a standards-compliant llms.txt file for any website — either by crawling the live site OR by reading the website's codebase directly. Use this skill when asked to create an llms.txt, add AI discoverability to a site, improve GEO (Generative Engine Optimization), make a website readable by AI agents, generate an llms-full.txt, check if a site has llms.txt, or audit a site's AI readiness for generative search. Trigger this skill any time a user mentions llms.txt, AI discoverability, LLM site readability, or wants their site to appear in AI-generated answers. Also trigger when the user is inside a website codebase and asks about SEO, AI readiness, or content structure. | `1.0.0` |
| `luma-attendees-scraper` | Browser-console script to export attendee data from a Luma event into a CSV. Use when users ask to scrape or export attendees from a Luma event. | `1.0.0` |
| `meeting-brief-generator` | Takes a company name and optional contact, runs targeted research via Tavily, synthesizes a 1-page pre-call brief with Gemini, and optionally saves it to Notion. Use when asked to prepare for a meeting, research a prospect before a call, generate a company brief, create a pre-call summary, or write a meeting prep doc. Trigger when a user says "prepare me for a meeting with", "research this company before my call", "generate a meeting brief for", "I have a call with X tomorrow", or "create a prospect brief for". | `1.0.0` |
| `meta-ads-expert` | Use when interacting with the Meta Ads MCP server to manage accounts, campaigns, ads, insights, and targeting, or to troubleshoot OAuth token authentication. Act as an Expert Media Buyer. | `0.0.1` |
| `newsletter-digest` | Aggregates RSS feeds from the past week, synthesizes the top stories using Gemini, and publishes a newsletter digest to Ghost CMS. Optionally outputs formatted Markdown for Substack or any other platform. Use when asked to generate a newsletter, create a weekly digest, summarize RSS feeds, compile top stories for a newsletter, or publish a digest to Ghost. Trigger when a user mentions newsletter digest, weekly roundup, RSS digest, compile top stories, or publish to Ghost. | `1.0.0` |
| `noise2blog` | Turns rough notes, bullet points, voice transcripts, or tweet dumps into a polished, publication-ready blog post. Optionally enriches with Tavily research to add supporting data and credibility to claims. Use when asked to write a blog post from notes, turn rough ideas into an article, expand bullet points into a full post, clean up a voice transcript into a blog, or repurpose a tweet thread as an article. Trigger when a user says "write a blog post from this", "turn these notes into a post", "expand this into an article", "make this publishable", "I have rough notes write a blog", or "clean up this transcript". | `1.0.0` |
| `outreach-sequence-builder` | Takes a buying signal and generates a personalized multi-channel outreach sequence across email, LinkedIn, and phone. Outputs 4-6 ready-to-send touchpoints over 10-14 days. Optionally drafts email touchpoints via Composio Gmail. Use when asked to write an outreach sequence, build a sales cadence, create a follow-up sequence, personalize outreach for a signal, or generate cold outreach messages. Trigger when a user says "build an outreach sequence for", "write a sales cadence for", "create outreach based on this signal", "they just raised a round write me a sequence", or "generate personalized outreach for". | `1.0.0` |
| `position-me` | Elite Website Reviewer Agent for AEO, GEO, SEO, UI/UX Psychology, and Copywriting. Use this skill when asked to review or evaluate a website's positioning. It conducts an EXHAUSTIVE, multi-page, psychologically-driven, and ruthless analysis of the entire website. Produces a massive, comprehensive, scored report with charts and actionable fixes. NO EMOJIS allowed. | `0.0.1` |
| `pr-description-writer` | Read the current branch diff and write a complete GitHub pull request description. Create or update the PR with one command. | `1.0.0` |
| `producthunt-launch-kit` | Generate every asset you need for a Product Hunt launch: listing copy, maker comment, and day-one social posts. | `1.0.0` |
| `reddit-icp-monitor` | Watches subreddits for people describing the exact problem you solve, scores their relevance to your ICP, and drafts a helpful non-spammy reply for each high-signal post. Use when asked to monitor Reddit for ICP signals, find prospects on Reddit, surface pain point posts, draft helpful Reddit replies, or scan subreddits for buying signals. Trigger when a user says "monitor Reddit for my ICP", "find people on Reddit who need my product", "scan subreddits for pain points", "draft Reddit replies for prospects", or "check Reddit for buying signals". | `1.0.0` |
| `reddit-post-engine` | Writes and optionally posts a Reddit post for any subreddit, following that subreddit's specific culture and rules. Drafts a title, body, and first comment using the 90/10 rule. Uses Composio Reddit MCP for optional direct posting. Use when asked to post on Reddit, draft a Reddit post, share a project on Reddit, write a subreddit post, or launch something on Reddit. Trigger when a user says "post this on Reddit", "write a Reddit post for r/...", "help me launch on Reddit", "draft something for Reddit", or "how do I share this on Reddit without getting banned". | `1.0.0` |
| `schema-markup-generator` | You are an SEO engineer specialising in structured data. Your job is to read a webpage and generate valid JSON-LD schema markup that matches what is actually on the page. | `1.0.0` |
| `show-hn-writer` | Draft a Show HN post title and body that follows the unwritten rules of Hacker News: specific, honest, first-person, no marketing. | `1.0.0` |
| `stargazer-deep-extractor` | Advanced 5-tier OSINT scraper for extracting GitHub stargazer emails. Use this skill when a user wants to scrape, extract, or download stargazers from a GitHub repository. | `0.0.1` |
| `tweet-thread-from-blog` | Converts a blog post URL or article into a Twitter/X thread with a strong hook, one insight per tweet, and a CTA. Optionally posts the full thread to X via Composio using a reply chain. Use when asked to turn a blog post into a tweet thread, repurpose an article for Twitter, create a thread from a blog, write a Twitter thread about a topic, or share a blog post as a thread. Trigger when a user mentions Twitter thread, X thread, tweet thread, or wants to repurpose blog content for X/Twitter. | `1.0.0` |
| `twitter-GTM-find-Skill` | End-to-end pipeline for scraping Twitter for GTM/DevRel tech startup jobs using Apify, and validating them against an Ideal Customer Profile (ICP) using Gemini's native Google Search Grounding. Use this skill when OpenClaw needs to find developer-first, funded startups actively hiring for GTM, DevRel, or Growth roles. | `0.0.1` |
| `yc-jobs-scraper` | Scrape daily job listings from YCombinator's Workatastartup platform without duplicates. Use this skill when asked to scrape YC jobs, update the YC companies list, or retrieve the latest startup jobs. It handles authentication, extracts company slugs via Inertia.js JSON payloads, falls back to public YC job pages when necessary, and maintains a local SQLite database to track historical jobs and prevent duplicates. | `0.0.1` |

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
