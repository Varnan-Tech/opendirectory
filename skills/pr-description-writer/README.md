# pr-description-writer

<img width="1280" height="640" alt="pr-description-writer" src="https://github.com/user-attachments/assets/485f5846-b621-40ac-8a99-2b50243fb454" />


Read your current git branch diff and generate a complete GitHub pull request description: summary, specific change bullets, and testing steps. Create or update the PR in one step.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install pr-description-writer --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fpr-description-writer&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Does

- Reads `git diff main...HEAD` to understand what changed
- Reads commit messages for context on why it changed
- Generates a structured PR description following a consistent format
- Creates a new PR with `gh pr create` or updates an existing one with `gh pr edit`

## Requirements

| Requirement | Purpose | How to Set Up |
|------------|---------|--------------|
| `gh` CLI | Creating and updating PRs | https://cli.github.com, then run `gh auth login` |
| Git repo with a branch | Source diff | Run from inside the repo |

No API keys needed. The agent reads the diff directly and writes the description.

## How to Use

Write a description for the current branch:

```
"Write a PR description for my current branch"
"Draft my PR"
"Generate a PR description"
```

Create the PR at the same time:

```
"Create a PR for this branch with a good description"
"Open a PR and write the description"
```

Update an existing PR's description:

```
"Update my PR description"
"Rewrite the PR body based on the latest changes"
```

Output only, no gh commands:

```
"Write a PR description but just give me the text"
"Draft the PR description, I'll paste it myself"
```

## Output Format

Every generated description includes:

| Section | Content |
|---------|---------|
| Summary | 1-2 sentences on what this PR does and why |
| Changes | Specific bullets, one per logical change, starting with a verb |
| Testing | Actionable steps to verify the change works |
| Screenshots | Only for UI changes |
| Linked Issues | Only if the branch fixes a tracked issue |

## Project Structure

```
pr-description-writer/
├── SKILL.md
├── README.md
├── evals/
│   └── evals.json
└── references/
    └── pr-format-guide.md
```

## License

MIT
