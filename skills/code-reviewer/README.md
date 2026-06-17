# code-reviewer

Review a diff or pull request and get back severity-ranked findings, each with a file:line reference, the quoted code, and a concrete fix. Built for signal over volume. It scopes to the code you changed, skips style nitpicks, catches over-engineering, and tells you when a change is clean instead of padding the list.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install code-reviewer --target claude
```

### Option B: skills.sh

```bash
npx skills add Varnan-Tech/opendirectory --skill code-reviewer
```

Requires Node.js. Add `--global` to install to `~/.claude/skills/` instead of the current project.

### Option C: Claude Desktop App

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

### Option D: Claude Code Native

Run these commands inside Claude Code:

```bash
/plugin marketplace add Varnan-Tech/opendirectory
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

### Option E: Manus AI

<video src="https://github.com/user-attachments/assets/17cbee2a-9e17-4bd4-ac46-68e0e92ffab4" controls width="100%"></video>

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fcode-reviewer&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [opendirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What it does

Most review bots flood a PR with cosmetic comments and miss the one bug that breaks production. Only about 31% of bot-flagged issues lead to a real change before merge. This skill flips that ratio.

- Works in two modes. Diff mode reviews a PR, branch, or change and scopes to the touched lines. Codebase mode audits a whole repo, directory, or file by risk and reports what it covered.
- Scopes to the diff in diff mode. It reviews the changed lines and the context needed to judge them. It does not comment on code you did not touch.
- Reads intent. It checks the PR title, ticket, and commits, then judges whether the code does what the change intended.
- Reviews in gating order: correctness, then security, then performance, then simplification.
- Runs two passes. A broad pass captures every candidate. A filter pass drops anything weak, out of scope, or not worth acting on.
- Anchors severity to concrete gates, not feel. Critical, High, Medium, Low map to clear merge actions.
- Catches unnecessary complexity. It flags premature abstractions, dead code, and reinvented stdlib, with guards against over-simplification.

## Output

Each finding follows one shape:

```
### 🔴 [CRITICAL] SQL injection in user lookup
**File:** api/users.py:42
**Issue:** user_id is interpolated into the query, so a crafted value runs arbitrary SQL.
**Evidence:**
    query = f"SELECT * FROM users WHERE id = {user_id}"
**Fix:** use a parameterized query:
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

It ends with a verdict: Ready to Merge, Needs Attention, or Needs Work, plus counts by severity.

## Usage

Diff mode, to review a change:

- "Review this PR before I merge it."
- "Check this diff for security and performance issues."
- "Is this code fine to ship?"

Codebase mode, to audit existing code:

- "Review my codebase."
- "Audit this repo for security issues."
- "Review the routes/ directory."

The skill reads the diff with `git diff`, walks the repo with `git ls-files`, or works on code you paste directly.

## Structure

- `SKILL.md` is the review process and the mode selection.
- `references/` holds the detail, loaded by name: `correctness.md`, `security.md`, `performance.md`, `simplification.md`, `codebase.md`, `output.md`.
- `evals/evals.json` holds test cases with assertions.
