# ledger-tasks-yylo

AI-native Kanban task management for coding agents. Your agent plans, tracks, and closes its own tasks on a durable board - with responses, commit links, dependency graphs, and receipts that survive across sessions.

Founders shipping with Claude, Codex, or Gemini agents lose task state the moment a session ends. This skill gives the agent a persistent board it operates itself through the `yy` CLI: it creates implementation-sized tasks, marks progress with evidence, wires dependencies, checks what is unblocked, and links every done-task to its commit.

Built on [YYLO Ledger](https://github.com/yylo-dev/yylo-ledger), the Git-native Record/task store behind the [YYLO orchestrator](https://github.com/yylo-dev/yylo).

---

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install ledger-tasks-yylo --target claude
```

### Option B: skills.sh

```bash
npx skills add Varnan-Tech/opendirectory --skill ledger-tasks-yylo
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fledger-tasks-yylo&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [opendirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## Requirements

- Node.js 18+
- YYLO CLI: `npm install --global '@yylo/cli@latest'`
- A Git repository (the ledger is file-native and lives in your repo)

## Usage

Once installed, ask your agent things like:

- "Create a task for the OAuth refactor and mark it in progress"
- "What tasks are ready to work on?"
- "Show the dependency order for open tasks"
- "Mark TASK-42 done - implemented and tested"

The agent runs `yy ledger` commands following the contract in `SKILL.md`: create, list, search, get, mark, update, archive, deps, ready, order, and merge - with best practices for task sizing, status flow, dependency markup, and receipt-preserving closes.

## Source

- Skill source: [yylo-dev/yylo-skills](https://github.com/yylo-dev/yylo-skills) (MIT)
- CLI: [yylo-dev/yylo](https://github.com/yylo-dev/yylo) (MIT)
