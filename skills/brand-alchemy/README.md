# Brand Alchemy

<img src="https://raw.githubusercontent.com/Varnan-Tech/opendirectory/main/docs/assets/opendirectory_banner.webp" width="100%" alt="Brand Alchemy Cover" />

World-class brand strategist and naming expert. Uses an interrogation-led discovery phase to extract your brand's DNA, then applies scientific naming frameworks (Phonosemantics) and automated multi-TLD domain checking.

## Install

```bash
npx "@opendirectory.dev/skills" install brand-alchemy --target claude
```

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

## Installation in Claude Desktop App

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
