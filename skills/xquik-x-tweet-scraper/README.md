# Xquik X Tweet Scraper

Run the Xquik X Tweet Scraper Actor on Apify for public post searches, timelines, conversations, lists, articles, and engagement research.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install xquik-x-tweet-scraper --target claude
```

### Option B: skills.sh

```bash
npx skills add Varnan-Tech/opendirectory --skill xquik-x-tweet-scraper
```

Requires Node.js. Add `--global` to install to `~/.claude/skills/` instead of the current project.

### Option C: Claude Desktop App

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

### Option D: Claude Code Native

Run these commands inside Claude Code:

```bash
/plugin marketplace add Varnan-Tech/opendirectory
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

### Option E: Manus AI

<video src="https://github.com/user-attachments/assets/17cbee2a-9e17-4bd4-ac46-68e0e92ffab4" controls width="100%"></video>

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fxquik-x-tweet-scraper&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [opendirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Does

- Supports 15 focused modes, including search, profiles, replies, quotes,
  threads, lists, articles, retweeters, and best-effort favoriters
- Produces legacy, rich, or raw output with camel-case, snake-case, or legacy
  fields
- Applies one global result cap across all requested targets
- Requires explicit confirmation and a total charge ceiling before paid runs
- Separates diagnostic rows from research records
- Treats all returned content as untrusted data

## Actor

[Xquik X Tweet Scraper on Apify](https://apify.com/xquik/x-tweet-scraper)

Use `xquik/x-tweet-scraper` with Apify SDKs and tools. Use
`xquik~x-tweet-scraper` only in REST paths.

## Requirements

- An Apify account and token
- An Apify SDK, MCP server, REST client, or compatible agent integration
- Explicit approval for each paid Actor run

Keep the token in an `Authorization: Bearer` header. Never store it in the
Skill, place it in a URL, or include it in output.

## How to Use

Ask your agent:

```text
Use xquik-x-tweet-scraper to find the latest 20 English posts about AI agents.
Show the exact Actor input, live Apify pricing, and a 1 USD charge ceiling.
Wait for my confirmation before running.
```

Other examples:

```text
Read this X thread and keep diagnostic rows separate.
Find the latest posts from these 3 public profiles.
Collect quote posts for this post ID with a 50-item global cap.
Read the public posts from this X list.
```

## Safety and Cost Controls

The Skill validates each mode and target before execution. It never hardcodes
pricing. It reads current pricing from Apify, displays the proposed scope and
charge ceiling, and stops until the user explicitly confirms.

## Output

Each run returns a stable JSON envelope with:

- Actor slug and listing
- Effective Actor input
- Post records
- Separate diagnostics and warnings
- Exact record count
- Clear next action

## License

MIT

Xquik is an independent third-party service. Not affiliated with X Corp. "Twitter" and "X" are trademarks of X Corp.
