# Brand Alchemy

<img width="1920" height="1072" alt="brand-alchemy-skill-cover-image" src="https://github.com/user-attachments/assets/15d90c97-9eef-4eed-abb3-7ce58438adf0" />

World-class brand strategist and naming expert. Uses an interrogation-led discovery phase to extract your brand's DNA, then applies scientific naming frameworks (Phonosemantics) and automated multi-TLD domain checking.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install brand-alchemy --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fbrand-alchemy&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## Core Capabilities

When invoked, the skill commands the AI agent to act as an elite branding consultant through a rigorous protocol:

* **The Interrogation**: Forces the AI to stop and ask critical discovery questions (Core, Audience, Alternative, Vibe) to extract your brand's true DNA before generating names.
* **Strategic Positioning**: Applies frameworks from April Dunford ("Obviously Awesome") and Category Design ("Play Bigger") to position your startup against the status quo.
* **Phonosemantics & Lexicon Science**: Uses sound symbolism (Plosives, Fricatives, Vowel Size) to engineer names that subconsciously communicate speed, power, or luxury.
* **Universal Domain Verification**: Automatically runs a robust Python script to check DNS and RDAP availability for any TLD (`.com`, `.io`, `.ai`, `.tech`, etc.), ensuring you don't fall in love with a taken name.

## Project Structure

```text
brand-alchemy/
├── README.md                           # Documentation
├── SKILL.md                            # Master protocol for the AI
├── scripts/
│   └── domain_checker.py               # Universal domain verification script (Python)
└── references/
    ├── core-brand-strategy.md          # Elite positioning & category design playbook
    └── lexicon-naming-science.md       # Phonosemantics & naming linguistics guide
```

## How to Prompt the AI

Once the skill is installed, simply ask the AI to help you name your startup or build a brand strategy.

> "Help me name my AI distribution startup. We help technical founders get users."

The AI will automatically pause and initiate **Step 1: The Interrogation**, asking you specific questions about your core offering, audience, alternatives, and desired brand vibe.
