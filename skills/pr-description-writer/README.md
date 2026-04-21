# pr-description-writer

<img width="1280" height="640" alt="pr-description-writer" src="https://github.com/user-attachments/assets/485f5846-b621-40ac-8a99-2b50243fb454" />


Read your current git branch diff and generate a complete GitHub pull request description: summary, specific change bullets, and testing steps. Create or update the PR in one step.

## Install

```bash
npx "@opendirectory.dev/skills" install pr-description-writer --target claude
```

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
