<img width="2752" height="1536" alt="human-tone-skill-cover-image" src="https://github.com/user-attachments/assets/aa2c99dc-87a6-490e-a989-21fd6a2bbc9a" />

# Human Tone

AI assistants write terrible marketing copy. They rely on generic filler words, force everything into lists of three, and bury your actual product under layers of hype.

The Human Tone skill teaches your AI how to edit its own work. It provides strict rules for stripping out robotic patterns and rewriting text to sound like a direct conversation from a founder to a customer.


## What It Fixes

* Removes words like "streamline", "empower", and "revolutionize".
* Stops the AI from starting emails with "I hope this finds you well".
* Forces the AI to replace vague claims with specific numbers and outcomes.
* Fixes the rigid sentence structures that make AI text obvious.

## Installation

You can install this skill directly into your AI agent environment using the OpenDirectory command line tool.

### Option 1: Quick Install

Run this command in your terminal to install it directly without downloading the whole directory:

```bash
npx "@opendirectory.dev/skills" install human-tone --target opencode
```

Note: You can change `--target opencode` to `--target claude` or `--target cursor` depending on which AI assistant you use.

### Option 2: Global Install

If you plan to browse and install multiple skills, you can install the tool globally on your computer:

```bash
npm install -g @opendirectory.dev/skills
opendirectory install human-tone --target opencode
```

## How to Use It

Once the skill is installed in your workspace, simply ask your AI to humanize your copy.

**Basic usage:**
> "Take this draft for a cold email and run it through the human-tone skill. Make it short and direct."

**Advanced usage (Matching a specific voice):**
> "Rewrite this landing page copy using the human-tone skill. Match the writing style in this sample: [paste a sample of your writing]."

The AI will rewrite the text, provide a bulleted list of what it changed, and flag any placeholders where you need to insert real numbers or actual customer names.
