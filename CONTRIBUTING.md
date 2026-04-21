# Contributing to OpenDirectory

Welcome to the OpenDirectory community! We are building the first universal registry for AI Agent Skills. Whether you are a seasoned growth engineer or making your very first open-source contribution, this guide will walk you through exactly how to build and submit a skill.

**Contributor Rewards:** Top contributors receive exclusive OpenDirectory swag, including limited-edition t-shirts and merchandise. We track contributions closely and reward those who help grow the ecosystem with high-quality GTM and Technical Marketing skills.

---

## What is an AI Agent Skill?

An AI Agent Skill is a package of instructions, context, and scripts that teaches an AI assistant (like Claude Code, OpenCode, or Cursor) how to perform a specific, complex task. 

Instead of typing a massive prompt every time you want the AI to do something, you create a **Skill**. Once installed, you just type `/your-skill-name` and the AI instantly knows exactly what to do, what scripts to run, and what format to output.

---

## How to Build a Skill (Step-by-Step)

### Step 1: Clone the Repository
Get the code onto your local machine by opening your terminal and running:

```bash
git clone https://github.com/Varnan-Tech/opendirectory.git
cd opendirectory
```

### Step 2: Create Your Skill Folder
All skills live inside the `skills/` directory. Create a new folder for your skill using a short, descriptive name (use dashes, no spaces).

```bash
mkdir skills/my-awesome-skill
cd skills/my-awesome-skill
```

### Step 3: Choose Your Architecture

You can build a **Basic Skill** (just instructions) or an **Advanced Skill** (instructions + code execution).

#### Option A: The Basic Skill
A basic skill is perfect for simple prompt-based tasks. It only requires two files in your folder:

```text
skills/my-awesome-skill/
├── README.md
└── SKILL.md
```

#### Option B: The Advanced Skill (Highly Recommended)
Advanced skills are production-grade tools that use external scripts (Python/Node), local databases (SQLite), or complex reference materials. This is what makes OpenDirectory powerful. Look at `skills/position-me` or `skills/stargazer` in this repository for real-world examples.

```text
skills/my-advanced-skill/
├── README.md            (The public documentation and cover image)
├── SKILL.md             (The YAML frontmatter and AI instructions)
├── .env.example         (Template for required API keys)
├── scripts/             (Executable Python/JS scripts for scraping or APIs)
│   └── scraper.py
└── references/          (SOPs, output templates, or complex guidelines)
    └── output_format.md
```

### Step 4: Write Your Files

**1. The `SKILL.md` File**
This is the brain of your skill. It MUST start with YAML frontmatter, followed by the instructions you want to give the AI agent.

```markdown
---
name: my-awesome-skill
description: Scrapes a website and generates a targeted cold email.
author: your-github-username
version: 1.0.0
---

# Cold Email Generator Skill

When the user asks you to generate a cold email:
1. Run the `scripts/scraper.py` file to extract the target's website data.
2. Read the rules in `references/email_guidelines.md`.
3. Output the final email in a markdown code block.
```

**2. The `README.md` File**
This is the public face of your skill. **It MUST have a dark-mode cover image at the very top.** This image will be automatically extracted and displayed on the main OpenDirectory registry page.

*Tip: You can use the `blog-cover-image-cli` skill already in this registry, or use Midjourney/ChatGPT/Flux to generate a 1280x640 dark-themed technical banner.*

```markdown
<img src="https://link-to-your-hosted-image.png" width="100%" alt="cover" />

# My Awesome Skill
This skill helps marketers automate their cold outreach by...

### Prerequisites
- Python 3.10+
- OpenAI API Key

### Usage
Once installed, simply type: "Use my-awesome-skill to email john@example.com"
```

### Step 5: Test Your Skill Locally
Before submitting a Pull Request, verify that your skill compiles and installs correctly using our CLI tool.

Run these commands from the root `opendirectory` folder:

```bash
pnpm install
pnpm build
npx "@opendirectory.dev/skills" install my-awesome-skill --target opencode
```

If successful, check your `~/.config/opencode/skills/my-awesome-skill` folder to ensure all your scripts and files were copied perfectly!

### Step 6: Submit a Pull Request
1. Commit your changes: `git add .` -> `git commit -m "feat: add my-awesome-skill"`
2. Push to your fork and open a Pull Request against the main repository.
3. **Security Scan**: Our automated GitHub Actions will strictly scan your code for formatting and malware.
4. **AI Review**: A Gemini 3.1 Pro AI agent will review your code diff and leave comments.
5. **Merge**: If everything passes, a human maintainer will merge your PR, and your skill will instantly be published to NPM and the Claude Marketplace!

---

## Looking for Inspiration? Build One of These!

If you want to contribute but aren't sure what to build, pick one of these high-demand, advanced Go-To-Market (GTM) ideas. Our automation script tracks these, so once your PR is merged, the box will be checked automatically!

- [x] `gh-issue-to-demand-signal` - Scans the open GitHub issues of a competitor's public repo, clusters them by theme (missing features, bugs, UX complaints), and outputs a ranked "demand gap" report. Tells you exactly what their users are begging for — which is your product's messaging brief.
- [ ] `who-viewed-my-talk` - Given a conference talk URL (YouTube/Luma/Sessionize), scrapes the comments, likes, and attendee list, cross-references speakers from the event's speaker page, and outputs a warm lead list of people who watched your category of content.
- [ ] `linkedin-hiring-intent-scanner` - Searches LinkedIn job posts for roles that signal buying intent — e.g., "Head of Developer Relations", "Growth Engineer", "RevOps Manager" — at companies in a given funding stage or industry, and outputs a prioritized list with context on why each company is interesting right now.
- [ ] `npm-downloads-to-leads` - Takes a list of npm package names (yours or competitors'), pulls weekly download trends via the npm API, identifies packages with breakout velocity, and maps the maintainers to Twitter/GitHub profiles. Useful for finding evangelists before they're famous.
- [ ] `api-error-to-faq-builder` - Pulls open issues from your GitHub repo tagged as "bug" or "question", clusters them by the error message or API endpoint mentioned, and auto-drafts a troubleshooting FAQ in Markdown. The most hated support task, automated.
- [ ] `sdk-adoption-tracker` - Given your SDK name, searches GitHub code search for public repos that import/require it, categorizes them by company/project type, and tracks week-over-week adoption velocity. Real signal of who's building on you — often invisible until you look.
- [ ] `noise-to-linkedin-carousel` - Takes a raw voice note transcript, a rough idea dump, or a messy thread of thoughts, and restructures it into a polished LinkedIn carousel script — slide-by-slide, with a hook slide, 5-7 insight slides, and a CTA slide. Designed for founders who think out loud.
- [ ] `oss-launch-kit` - Given a GitHub repo URL, generates the full launch kit: a Show HN post, a Product Hunt description, 5 Reddit posts tailored to relevant subreddits, a Twitter thread, and a "first week" community engagement plan. Built specifically for open-source product launches.
- [ ] `competitor-churner-finder` - Monitors Twitter and Reddit for posts from people expressing frustration with a specific competitor tool (e.g., "switching away from X", "X is broken again"), extracts their profiles, and drafts a timely, empathetic DM that offers your product as the alternative — without being creepy.
- [ ] `ph-daily-radar` - Hits the Product Hunt API every morning, filters launches by category, extracts the makers' Twitter/LinkedIn, and sends you a digest of who launched in your category today — with a drafted "congrats" outreach for each maker. Relationship building on autopilot.
- [ ] `domain-expired-opportunity-finder` - Monitors daily expired domain lists, filters for domains that still have backlinks pointing to them (via public Ahrefs/Moz data), and flags ones in your niche that you could buy cheaply and redirect — one of the most underrated SEO plays, almost nobody automates the search.
- [x] `pricing-page-psychology-audit` - Takes a SaaS pricing page URL and audits it against 12 known pricing psychology principles (anchoring, decoy effect, loss aversion framing, feature-vs-value naming, etc.). Outputs specific suggestions on how to reframe each tier. Pricing is the highest-leverage GTM lever and almost nobody stress-tests it.
- [ ] `content-repurpose-queue` - Looks at your last 30 pieces of content (tweets, blogs, LinkedIn posts), flags every one that got above-average engagement but was never repurposed, and generates a queue of 5 repurposing formats for each one. Most people create, post once, and forget. This treats content like an asset.
- [ ] `github-discussion-to-devrel-content` - Monitors GitHub Discussions on your own or a competitor's repo, surfaces threads with 10+ replies or unresolved questions, and auto-drafts a short blog post or Twitter thread that answers each one — turning your community's questions into SEO-indexed content.
- [ ] `youtube-tutorial-comment-scraper` - Scrapes comments on popular tutorial videos for competitor products, identifies frustrated users, extracts channel metadata, and finds business emails for outreach.
- [ ] `app-store-review-arbitrage` - Scrapes iOS and Android app store reviews for competitor applications, filters for low-star reviews mentioning specific missing features using Python NLP scripts, and generates targeted ad copy highlighting those exact features in your own product.

This list is continuously updated with new high-demand GTM ideas. If you have a great idea for a skill that you want someone else to build, please open an issue to submit your suggestion. We encourage contributors to share their own ideas and help expand the registry.
