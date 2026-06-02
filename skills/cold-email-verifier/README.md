# Cold Email Verifier

Agent Skill that equips your AI agent with the ability to autonomously guess, enrich, and verify cold email addresses directly from a CSV file.

Instead of running Python scripts manually, this skill teaches your AI how to read your lead lists, discover corporate domains via the Clearbit API, generate standard email permutations, and securely verify them.

<img width="2752" height="1536" alt="cold-email-verifier-cover-image" src="https://github.com/user-attachments/assets/f033ec61-d2c1-4cee-a6d5-71e7cf9632a6" />

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install cold-email-verifier --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fcold-email-verifier&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## Verification Engines Supported
The AI is trained to use two different verification backends:
1. **ValidEmail.co API (Highly Recommended)**: The AI will use this SaaS API for enterprise-grade accuracy, bypassing strict catch-all servers. You can get a free tier of verification credits at validemail.co.
2. **Reacher (Self-Hosted)**: The AI can route checks through your own self-hosted Reacher Docker container (e.g., on an AWS EC2 instance with an unblocked Port 25) for 100% free verification.

## Setup

To install this skill into your AI agent's workspace:

1. Clone or download this folder.
2. Copy the entire cold-email-verifier folder into your agent's skills directory (e.g., ~/.agents/skills/ or your project's .agents/skills/ folder).
3. Ensure the dependencies in 
equirements.txt are installed in your environment:
   `ash
   pip install -r requirements.txt
   `
4. Copy the .env.example to .env and add your ValidEmail.co API key:
   `ash
   cp .env.example .env
   `

## How to Prompt the AI

Once the skill is installed, you can simply talk to your AI agent. Here are example prompts:

**Using ValidEmail.co:**
> "Use the cold email verifier skill to process leads.csv. Please use the validemail mode."

**Using a Self-Hosted Reacher Server:**
> "Verify the emails in leads.csv using the cold email verifier. Use reacher-http mode and point it to http://YOUR_SERVER_IP:8080/v0/check_email."

The AI will automatically parse the CSV, handle the domain lookups, generate the permutations, run the verification engine, and output a clean CSV with the valid emails appended.

## CSV Format Requirements
The AI expects the input CSV to contain at least the following headers:
- First Name
- Last Name
- Company Name
- Domain Name
