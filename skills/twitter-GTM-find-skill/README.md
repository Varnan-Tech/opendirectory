# Twitter GTM Find Skill

<img width="1280" height="640" alt="Generated_chart__twitter-gtm-find-cover-bw png" src="https://github.com/user-attachments/assets/618b0abe-34fc-4c3e-a345-1a3eaeb3d20b" />

Find developer-first GTM, DevRel, and Growth hiring signals from X/Twitter, then verify funding and product fit.

This pipeline uses Apify as the default discovery path. OpenClaw users can also
use TweetClaw for tweet search, reply search, user lookup, follower export,
monitors, and webhooks before the same ICP validation step.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install twitter-GTM-find-skill --target claude
```

### Option B: Claude Desktop App

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

### Option C: Claude Code Native

Run these commands inside Claude Code:

```bash
/plugin marketplace add Varnan-Tech/opendirectory
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

### Option D: Manus AI

<video src="https://www.opendirectory.dev/ManusAI-one-click-installation-demo.webm" controls width="100%"></video>

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Ftwitter-GTM-find-skill&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## The Skill Directory

All executable code and documentation are packaged cleanly inside the `twitter-GTM-find/` folder. This is designed to be directly imported and read by AI agents (like OpenClaw or Claude) so they understand how to use the tool.

```text
twitter-GTM-find/
├── SKILL.md             <-- The AI entry point and documentation
├── references/          
│   └── icp-checklist.md <-- The strict evaluation criteria (Dev-first + $100K+ funded)
└── scripts/
    ├── run_pipeline.sh  <-- The executable shell script
    └── src/             <-- The TypeScript pipeline source code
```

## Usage

To run the pipeline manually or via an agent:

1. Create a `.env` file at the root of the repository:
   ```env
   APIFY_API_TOKEN=your_apify_token
   GEMINI_API_KEY=your_gemini_api_key
   MAX_POSTS=20
   ```
2. Run the shell script:
   ```bash
   cd twitter-GTM-find/scripts
   bash run_pipeline.sh
   ```

## Optional Native X/Twitter Plugin Paths

The existing Apify pipeline remains the default end-to-end workflow.

For OpenClaw users who already run
[TweetClaw](https://github.com/Xquik-dev/tweetclaw), the skill can also use
TweetClaw as a native OpenClaw plugin for the first discovery pass:

```bash
openclaw plugins install @xquik/tweetclaw
```

After setting `XQUIK_API_KEY`, use `explore` to find the relevant tweet search,
reply search, user lookup, follower export, monitor, and webhook endpoints. Use
`tweetclaw` to scrape tweets, search tweets and replies, look up founders or
company accounts, export followers, and monitor promising leads during this
workflow.

For Hermes users who already run
[Hermes Tweet](https://github.com/Xquik-dev/hermes-tweet), the skill can also
use Hermes Tweet as a native Hermes Agent X/Twitter plugin for the first
discovery pass:

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

After setting `XQUIK_API_KEY`, use `tweet_explore` to scrape/search tweets or
search Twitter/X for GTM, DevRel, growth, and startup hiring signals. Use
`tweet_read` to read tweet replies, look up users, and monitor tweets from
promising founders or company accounts. Use `tweet_action` only for read-side
exports such as export followers during this workflow.

Keep the pipeline's validation step intact: export the Hermes Tweet findings
or TweetClaw findings into the same candidate review shape, then run the ICP
checks before any outreach. Post tweets, post replies, send DMs, and other
automated X actions should stay confirmation-gated and outside unattended
discovery runs.

## Output

The pipeline generates two temporary files at the root of the repository (which are `.gitignore`d to prevent leaking data):
- `radar-jobs.json`: The initial raw batch of scraped tech jobs.
- `openclaw-icp-jobs.json`: The final, strict ICP-validated list of highly funded, developer-first startups hiring right now.
