# explain-this-pr

<img width="1280" height="640" alt="explain-this-pr" src="https://github.com/user-attachments/assets/9e76fc64-f982-4c4c-9b58-4398541aab97" />


Point this skill at any GitHub PR and it writes a plain-English explanation of what changed and why, then posts it as a PR comment.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install explain-this-pr --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fexplain-this-pr&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Does

- Fetches the PR diff and metadata via `gh`
- Writes two paragraphs: what changed (technical) and why it matters (impact)
- Posts the explanation as a PR comment with `gh pr comment`
- Works with any public or private repo you have access to via `gh`

## Requirements

| Requirement | Purpose | How to Set Up |
|------------|---------|--------------|
| `gh` CLI | Fetching PR data and posting comments | https://cli.github.com, then run `gh auth login` |

No API keys needed.

## How to Use

Explain a PR by URL:

```
"Explain this PR: https://github.com/owner/repo/pull/123"
"What does this PR do? https://github.com/owner/repo/pull/456"
"Summarize this pull request: [URL]"
```

Explain by PR number (in the current repo):

```
"Explain PR #42"
"Add a summary comment to PR #99"
```

Explain the current branch PR:

```
"Explain the current branch PR"
"Add a plain-English comment to my PR"
```

Output without posting:

```
"Explain this PR but don't post the comment: [URL]"
"What does this PR change? Just give me the text."
```

## Output Format

Two paragraphs, under 150 words total.

Paragraph 1: What it does (technical). Names the specific files, functions, or systems that changed. States the before/after if visible in the diff.

Paragraph 2: Why it matters (impact). Explains who benefits and what problem is solved. Omitted if there is no clear "why" in the diff or commits. The skill never guesses at impact.

## Project Structure

```
explain-this-pr/
├── SKILL.md
├── README.md
└── evals/
    └── evals.json
```

## License

MIT
