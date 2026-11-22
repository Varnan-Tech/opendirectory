# AutorunX

Turn your coding agent into a film crew. This skill teaches your agent to use the
[AutorunX](https://autorunx.com) MCP tools: it plans a film, writes the script and storyboard,
makes pictures and music with cloud models and video on your own rented GPU, then edits the
timeline. Everything lands in a Studio Mix project you can open and change on autorunx.com.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install autorunx --target claude
```

### Option B: skills.sh

```bash
npx skills add Varnan-Tech/opendirectory --skill autorunx
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fautorunx&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [opendirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## Prerequisites

- An AutorunX account on a paid plan (https://autorunx.com/pricing).
- An AutorunX API key (profile picture → API keys, starts with `axk_`).
- For video: a rented GPU on AutorunX (Rent GPU). Pictures and music use credits.

## Connect the MCP server

```bash
claude mcp add --transport http autorunx https://autorunx.com/api/mcp \
  --header "Authorization: Bearer axk_your_key"
```

Other agents: add a streamable-HTTP MCP server at `https://autorunx.com/api/mcp` with the
header `Authorization: Bearer axk_your_key`.

## Usage

- "Use autorunx to make a 30-second product teaser for my app."
- "Make a storyboard and three frame pictures for a coffee shop reel."
- "Open my last AutorunX project and add background music to the timeline."

Source plugin: https://github.com/bluehans-agency/Autorunx-plugin
