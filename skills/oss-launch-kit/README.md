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

### Video Tutorial
Watch this quick video to see how it's done:

https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c

### Step 1: Download the skill from GitHub
1. Click the **Code** button on this repo's GitHub page.
2. Select **Download ZIP** to download the repository.
3. Extract the ZIP file on your computer.

### Step 2: Install the Skill in Claude
1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** (plus) icon button to create a new skill.
4. Choose the option to **Upload a skill**, and drag and drop the `.zip` file (or you can extract it and drop the folder, both work).

> **Note:** Make sure you are uploading the folder that contains the `SKILL.md` file!

---

## How It Works

1. Point the agent at a GitHub repo URL.
2. The agent analyzes the repo (README, license, install guide, metadata) and scores launch readiness.
3. You receive a channel recommendation, a timed launch checklist, and skill hand-offs to `show-hn-writer`, `producthunt-launch-kit`, and `reddit-post-engine`.

---

## Usage

```
"Run a launch readiness check on https://github.com/owner/repo and give me a channel strategy."
```

```
"Analyze this repo and create a coordinated launch plan across Product Hunt, HN, and Reddit."
```

---

## Requirements

- Claude desktop app (no other dependencies)

---

## Differentiation

Unlike single-channel generators, `oss-launch-kit` acts as the **Root Strategy Layer**:
1. It tells you **if and where** you should launch.
2. It provides a **timed checklist** for coordination.
3. It hands off to **specialized skills** for channel-specific drafting.
