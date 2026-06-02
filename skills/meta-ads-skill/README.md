# Meta Ads Agentic Skill

<img width="1376" height="768" alt="meta-ads-skill" src="https://github.com/user-attachments/assets/baf2509b-0ee0-41ca-9555-3ad350a6824c" />

## Overview

The **Meta Ads Skill** is a comprehensive, production-ready  skill designed to give LLMs and AI agents expert-level capabilities to orchestrate the official **Meta Ads Python CLI**.

By using this skill, an agent transforms into an **Expert Media Buyer**. It will know exactly how to explore ad structures, troubleshoot campaign performance (like CPA spikes), discover new audiences, and format massive Meta APIs JSON payloads into beautiful, readable markdown reports.

---

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install meta-ads-skill --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fmeta-ads-skill&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## For Agents: How to Use This Skill Efficiently

This skill is designed using a **Progressive Disclosure (Hub-and-Spoke)** architecture to maximize context window efficiency:

1. **The Hub (`SKILL.md`)**: The primary entry point. It provides strict guardrails, safety protocols, and the authentication troubleshooting workflow.
2. **The Spokes (`references/`)**: 
   - When you need to perform a specific task (e.g., investigating a CPA spike), read `references/workflows.md` for the exact step-by-step orchestration strategy.
   - When presenting data to the user, read `references/report_templates.md` to strictly follow the required Markdown layout.

###  Strict Agent Guardrails
* **Context Protection**: ALWAYS default to `time_range="last_7d"` for insights. ALWAYS use `limit=10` for listing campaigns/adsets initially.
* **Safety First**: NEVER execute state-changing tools (`create_campaign`, `update_campaign`) without explicitly showing the parameters to the user and waiting for their affirmative confirmation.

---

## Setup

To use this skill, you must install the official Meta Ads CLI and configure your credentials.

### 1. Set up the CLI
The skill relies on the `meta-ads` Python package:
```bash
pip install meta-ads
```

### 2. Authentication (System User Token)
The CLI uses a **System User Access Token** for authentication. 
1. Generate a System User Token in your [Meta Business Suite](https://business.facebook.com/settings/system-users).
2. Ensure the token has `ads_management`, `ads_read`, and `read_insights` permissions.
3. Set the following environment variables on your machine:

```bash
export ACCESS_TOKEN="your_system_user_access_token"
export AD_ACCOUNT_ID="act_your_ad_account_id"
```

---

## Skill Repository Structure

When you deploy this skill, the structure will look like this:

```text
meta-ads-skill/
 SKILL.md                          # The core router & guardrails
 references/
    report_templates.md           # Standardized markdown report structures
    workflows.md                  # Orchestration strategies (e.g., CPA troubleshooting)
```

## Supported Commands

This skill orchestrates the `meta-ads` CLI using a noun-verb structure:
* **Campaigns**: `meta ads campaign list`, `meta ads campaign create`
* **Ad Sets**: `meta ads adset list`
* **Ads**: `meta ads ad list`
* **Insights**: `meta ads insights get`
