# Meta Ads Agentic Skill

<img width="1376" height="768" alt="meta-ads-skill" src="https://github.com/user-attachments/assets/baf2509b-0ee0-41ca-9555-3ad350a6824c" />

## Install

```bash
npx "@opendirectory.dev/skills" install meta-ads-skill --target claude
```

### Video Tutorial
Watch this quick video to see how it's done:

https://github.com/user-attachments/assets/ee98a1b5-ebc4-452f-bbfb-c434f2935067

### Step 1: Download the skill from GitHub
1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

### Step 2: Install the Skill in Claude
1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** (plus) icon button to create a new skill.
4. Choose the option to **Upload a skill**, and drag and drop the `.zip` file (or you can extract it and drop the folder, both work).

> **Note:** For some skills (like `position-me`), the `SKILL.md` file might be located inside a subfolder. Always make sure you are uploading the specific folder that contains the `SKILL.md` file!

## Overview

The **Meta Ads Skill** is a comprehensive, production-ready OpenCode skill designed to give LLMs and AI agents expert-level capabilities to orchestrate the [Varnan-Tech Meta Ads MCP Server](https://github.com/Varnan-Tech/Meta-Ads-MCP). 

By using this skill, an agent transforms into an **Expert Media Buyer**. It will know exactly how to safely authenticate, explore ad structures, troubleshoot campaign performance (like CPA spikes), discover new audiences, and format massive Meta APIs JSON payloads into beautiful, readable markdown reports.

---

## For Agents: How to Use This Skill Efficiently

This skill is designed using a **Progressive Disclosure (Hub-and-Spoke)** architecture to maximize context window efficiency:

1. **The Hub (`SKILL.md`)**: The primary entry point. It provides strict guardrails, safety protocols, and the authentication troubleshooting workflow.
2. **The Spokes (`references/` & `scripts/`)**: 
   - When you need to perform a specific task (e.g., investigating a CPA spike), read `references/workflows.md` for the exact step-by-step orchestration strategy.
   - When presenting data to the user, read `references/report_templates.md` to strictly follow the required Markdown layout.
   - **Data Parsing**: Meta Ads JSON responses are massive. *Always* use the provided `scripts/formatters.py` to condense raw JSON from `get_campaigns`, `get_adsets`, or `get_insights` into clean markdown tables before reasoning over them.

###  Strict Agent Guardrails
* **Context Protection**: ALWAYS default to `time_range="last_7d"` for insights. ALWAYS use `limit=10` for listing campaigns/adsets initially.
* **Safety First**: NEVER execute state-changing tools (`create_campaign`, `update_campaign`, `clear_database`, `reset_database`) without explicitly showing the parameters to the user and waiting for their affirmative confirmation.

---

## Installation & Setup of the Meta Ads MCP

To use this skill, the host machine must have the Varnan-Tech Meta Ads MCP Server installed and running. 

### 1. Prerequisites
- **Python 3.10+**
- A **Meta Developer Account** with a configured App.

### 2. Configure the Meta App
1. Go to the [Facebook Developers Portal](https://developers.facebook.com/).
2. Create an App and add the **Marketing API** product.
3. Under the Facebook Login settings, add `http://localhost:8000/auth/facebook/callback` to the **Valid OAuth Redirect URIs**.
4. Retrieve your **App ID** and **App Secret**.

### 3. Server Setup
Clone the MCP repository:
```bash
git clone https://github.com/Varnan-Tech/Meta-Ads-MCP.git
cd Meta-Ads-MCP
pip install -r requirements.txt
```

Create a `.env` file in the root of the MCP server:
```env
FB_APP_ID="your_facebook_app_id"
FB_APP_SECRET="your_facebook_app_secret"
FB_OAUTH_ENABLED="true"
FB_REDIRECT_URI="http://localhost:8000/auth/facebook/callback"
DATABASE_URL="sqlite:///.meta-ads-mcp/oauth.db"
```

---

## Authentication Workflow

The server uses OAuth backed by a local SQLite database to seamlessly pass tokens to the MCP context.

1. **Start the local Auth Server**:
   ```bash
   python src/auth/run_web_server.py
   ```
2. **Authenticate**: Open `http://localhost:8000/auth/facebook` in your web browser.
3. **Grant Permissions**: Click "Connect Facebook" and approve the `ads_management`, `ads_read`, and `read_insights` permissions.
4. **Completion**: The OAuth token is saved securely to the SQLite DB. The agent can now use the MCP tools automatically without needing the token pasted into the prompt.

*If an agent encounters an Auth Error during operation, it is instructed by this skill to guide the user back through this exact login flow.*

---

## Skill Repository Structure

When you deploy this skill, the structure will look like this:

```text
meta-ads-skill/
 SKILL.md                          # The core router & guardrails
 references/
    report_templates.md           # Standardized markdown report structures
    workflows.md                  # Orchestration strategies (e.g., CPA troubleshooting)
 scripts/
     auth_check.py                 # Diagnostic script for token status
     formatters.py                 # JSON -> Markdown table utilities
```

## Supported Tools (via MCP)

Through the underlying MCP, this skill orchestrates:
* **Account Management**: `get_ad_accounts()`, `get_account_info()`
* **Campaigns & Ads**: `get_campaigns()`, `get_adsets()`, `get_ads()`, `create_campaign()`, `update_campaign()`
* **Analytics**: `get_insights()`, `analyze_campaigns()`
* **Targeting**: `search_interests()`, `search_demographics()`, `estimate_audience_size()`
* **Database**: `token_status()`, `clear_database()`, `reset_database()`
