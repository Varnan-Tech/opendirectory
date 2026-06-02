<img width="1280" height="640" alt="human-tone-skill-cover-image" src="https://github.com/user-attachments/assets/aa2c99dc-87a6-490e-a989-21fd6a2bbc9a" />

# Human Tone

AI assistants write terrible marketing copy. They rely on generic filler words, force everything into lists of three, and bury your actual product under layers of hype.

The Human Tone skill teaches your AI how to edit its own work. It provides strict rules for stripping out robotic patterns and rewriting text to sound like a direct conversation from a founder to a customer.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install human-tone --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fhuman-tone&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Fixes

* Removes words like "streamline", "empower", and "revolutionize".
* Stops the AI from starting emails with "I hope this finds you well".
* Forces the AI to replace vague claims with specific numbers and outcomes.
* Fixes the rigid sentence structures that make AI text obvious.

## How to Use It

Once the skill is installed in your workspace, simply ask your AI to humanize your copy.

**Basic usage:**
> "Take this draft for a cold email and run it through the human-tone skill. Make it short and direct."

**Advanced usage (Matching a specific voice):**
> "Rewrite this landing page copy using the human-tone skill. Match the writing style in this sample: [paste a sample of your writing]."

The AI will rewrite the text, provide a bulleted list of what it changed, and flag any placeholders where you need to insert real numbers or actual customer names.
