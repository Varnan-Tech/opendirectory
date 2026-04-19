<div align="center">
  <img src="docs/assets/opendirectory_banner.webp" width="100%" alt="OpenDirectory Banner" />
</div>

<br />

<div align="center">
  <strong>A curated registry and CLI for AI Agent Skills, meticulously designed for Go-To-Market (GTM), Technical Marketing, and growth automation.</strong>
</div>

<div align="center">

[![npm version](https://img.shields.io/npm/v/@opendirectory.dev/skills.svg?style=flat-square)](https://www.npmjs.com/package/@opendirectory.dev/skills)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![TypeScript](https://img.shields.io/badge/TypeScript-blue?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org)

</div>

---

[Overview](#overview) • [Features](#features) • [Installation](#installation) • [Usage](#usage) • [Supported Agents](#supported-agents) • [Available Skills](#available-skills)

OpenDirectory is a central library and CLI tool that allows you to add new capabilities, or "skills", to your AI agents. Instead of teaching your AI how to perform complex marketing or growth tasks from scratch, you can simply download a pre-built skill from our catalog and install it directly into your project.

> [!NOTE]  
> OpenDirectory skills are modular, reusable integrations designed to work across a variety of AI coding assistants and agents.

## Overview

Building agentic workflows can be complex and time-consuming. OpenDirectory simplifies this by providing a registry of discoverable skills—ready-to-use markdown files and scripts that give your agents new abilities like Twitter GTM radar, Hacker News intel, docs extraction, and more. 

The main CLI (`@opendirectory.dev/skills`) installs and manages these skills seamlessly, acting as a package manager for AI agent capabilities.

## Features

- **Extensive Registry**: A wide array of pre-built skills for GTM, technical marketing, and growth.
- **Zero-Install CLI**: Run instantly via `npx` to list and install skills without cluttering your environment.
- **Multi-Agent Support**: Compatible with a variety of agents like Claude Code, OpenCode, Gemini CLI, and more.
- **Native Claude Code Integration**: Can be added as a native community marketplace directly inside Claude Code.
- **Global Installation**: Installs skills into your agent's global configuration directory, making them available across all your projects.

## Installation

Because we use `npx`, there is no need to permanently install the OpenDirectory tool. You can run it instantly from your terminal.

> [!TIP]
> Using `npx` ensures you are automatically using the most recent version of the CLI and the latest skills registry.

### Native Installation (Claude Code)

Users who exclusively use Anthropic's Claude Code can add OpenDirectory as a native community marketplace directly inside their Claude interface:

```bash
# Add the OpenDirectory marketplace
/plugin marketplace add Varnan-Tech/opendirectory

# Install a skill directly
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

## Usage

### 1. View Available Skills

To see the full list of available skills in the registry, open your terminal and run:

```bash
npx "@opendirectory.dev/skills" list
```

This command fetches the latest `registry.json` and displays all available skills along with their descriptions.

### 2. Install a Skill

Once you have found a skill you want to use, install it by specifying the skill name and your target agent:

```bash
npx "@opendirectory.dev/skills" install <skill-name> --target <your-agent>
```

For example, to install the `blog-cover-image-cli` skill for Claude:

```bash
npx "@opendirectory.dev/skills" install blog-cover-image-cli --target claude
```

### 3. Use the Skill

After the installation is complete, your AI agent is ready to use the new skill. Simply open your AI agent within your project folder and give it a command related to the skill.

For example:
_"Use the blog-cover-image-cli skill to generate a thumbnail for my new article."_

## Supported Agents

When installing a skill, you must specify the target agent using the `--target` flag. Supported agents include:

- **Claude Code**: `--target claude`
- **OpenCode**: `--target opencode`
- **Codex**: `--target codex`
- **Gemini CLI**: `--target gemini`
- **Anti-Gravity**: `--target anti-gravity`
- **OpenClaw**: `--target openclaw`
- **Hermes**: `--target hermes`

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
| [`pricing-page-psychology-audit`](skills/pricing-page-psychology-audit) | Audits any SaaS pricing page URL against 12 pricing psychology principles and outputs a ranked improvement report with specific rewrite suggestions... | `1.0.0` |
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

<div align="center">
  <em>Powered by the OpenDirectory community.</em>
</div>
