---
name: oss-launch-kit
description: Higher-level OSS launch orchestrator that analyzes repos, selects channels, and coordinates launch plans.
compatibility: [claude-code, gemini-cli, github-copilot]
author: OpenDirectory
version: 0.2.0
---

# OSS Launch Kit (Orchestrator)

The `oss-launch-kit` is the **root orchestration layer** for open-source launches in OpenDirectory. It turns a GitHub repository URL into a grounded, coordinated launch strategy. 

Rather than just writing generic copy, this skill serves as the **Strategic Entry Point**: it evaluates readiness, determines channel fitness (Show HN vs. Product Hunt vs. Reddit), and provides the coordination logic needed to use specialized skills effectively.

## How it works

- **Project Analysis**: Differentiates between CLI tools, libraries, apps, and templates.
- **Launch Readiness**: Stronger checks for installation guides, examples, and licenses.
- **Skill Orchestration**: Provides hooks and explicit handoffs to `show-hn-writer`, `producthunt-launch-kit`, and `reddit-post-engine`.
- **Coordinated Strategy**: A timed checklist for multi-channel launches.
- **Honest Feedback**: Proactively flags sparse READMEs and recommends documentation sprints.

## When to use

- **Primary Entry Point**: Use this first to map out your launch strategy.
- **Readiness Assessment**: Determine if your repo is actually ready for high-friction channels.
- **Skill Orchestration**: Get hooks and handoffs to specialized skills:
  - `show-hn-writer` (for technical deep-dives)
  - `producthunt-launch-kit` (for PH assets and badges)
  - `reddit-post-engine` (for community-specific variants)
  - `tweet-thread-from-blog` (for Twitter/X threads)
  - `linkedin-post-generator` (for LinkedIn posts)
- **Coordinated Strategy**: Get a realistic, timed checklist for multiple platforms.
