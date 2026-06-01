<img src="./hero.png" width="100%" alt="OSS Launch Kit Cover" />

# oss-launch-kit (Orchestrator)

The high-level **OSS Launch Orchestrator** for GitHub repositories. It serves as the strategic entry point that analyzes your repo and coordinates a multi-channel launch plan.

## Features

- **Project Analysis**: Differentiates between CLI tools, libraries, apps, and templates.
- **Enhanced Readiness**: Checks for installation guides, usage examples, license, and metadata.
- **Channel Orchestration**: Recommends the best channels (PH, HN, Reddit, X) based on fitness.
- **Skill Hand-offs**: Provides hooks and pointers to `show-hn-writer`, `producthunt-launch-kit`, and `reddit-post-engine`.
- **Honest Feedback**: Explicitly flags low-readiness repos and recommends documentation sprints.

## Install

```bash
npx "@opendirectory.dev/skills" install oss-launch-kit --target claude
```

### Step 1: Download the skill from GitHub
1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

### Step 2: Install the Skill in Claude

<video src="https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c" controls width="100%"></video>

1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** (plus) icon button to create a new skill.
4. Choose the option to **Upload a skill**, and drag and drop the `.zip` file (or you can extract it and drop the folder, both work).

> **Note:** For some skills (like `position-me`), the `SKILL.md` file might be located inside a subfolder. Always make sure you are uploading the specific folder that contains the `SKILL.md` file!

### Step 3: Install in Manus AI

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.


---

## How It Works

1. Point the agent at a GitHub repo URL.
2. The agent analyzes the repo (README, license, install guide, metadata) and scores launch readiness.
3. You receive a channel recommendation, a timed launch checklist, and skill hand-offs to `show-hn-writer`, `producthunt-launch-kit`, and `reddit-post-engine`.

---

## Usage

```bash
# Generate a launch strategy and checklist for a repo
python scripts/run.py --repo-url https://github.com/owner/repo
```

---

## Differentiation

Unlike single-channel generators, `oss-launch-kit` acts as the **Root Strategy Layer**:
1. It tells you **if and where** you should launch.
2. It provides a **timed checklist** for coordination.
3. It hands off to **specialized skills** for channel-specific drafting.
