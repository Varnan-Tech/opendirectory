---
name: pr-description-writer
description: Use when the user asks to write, draft, generate, or update a GitHub pull request description for the current branch. Reads the branch diff and commit messages, writes a structured PR body (summary, changes, testing), and optionally creates or updates the PR via the gh CLI.
compatibility: [claude-code, gemini-cli, github-copilot]
author: OpenDirectory
version: 1.0.0
---

# PR Description Writer

Read the current branch diff and write a complete GitHub pull request description. Create or update the PR with one command.

## Writing Style

Apply to all generated PR descriptions:

- Active voice. "Adds X" not "X has been added."
- Present tense for summary ("Adds caching layer"), past tense for context ("The old approach caused N requests per render")
- Short sentences, one idea per bullet
- No em dashes — use a comma or period instead
- No filler: "this PR", "this commit", "as per the discussion"
- Specifics beat generalities: "reduces p95 latency from 800ms to 90ms" beats "improves performance"

---

## Step 1: Check Setup

Confirm `gh` is authenticated:

```bash
gh auth status
```

If not authenticated: `gh auth login` and follow the prompts.

Confirm the current directory is a git repo with an active branch:

```bash
git branch --show-current
```

If detached HEAD or no branch, stop and ask the user which branch they want to describe.

---

## Step 2: Gather Diff Context

Run all three commands to build context:

**File summary (what changed):**
```bash
git diff main...HEAD --stat
```

**Commit messages (why it changed):**
```bash
git log main...HEAD --oneline
```

**Full diff (how it changed):**

Use `origin/main` first (always up to date), fall back to local `main`, then `master`:
```bash
if git rev-parse origin/main &>/dev/null 2>&1; then
  BASE=origin/main
elif git rev-parse main &>/dev/null 2>&1; then
  BASE=main
else
  BASE=master
fi
git diff $BASE...HEAD
```

If the diff is very large (over 500 lines), read the `--stat` summary and the commit messages only. Also read the first 200 lines of the diff to understand the primary changes without processing the entire output.

Also check for an existing PR and read its current title/body:
```bash
gh pr view --json title,body,baseRefName 2>/dev/null
```

---

## Step 3: Read the Format Guide

Read `references/pr-format-guide.md` in full before writing anything. Internalize:
- Required sections and their order
- How to write each section
- What to include vs omit
- The testing section format

---

## Step 4: Generate the Description

Write the PR description using the format from `references/pr-format-guide.md`.

Rules:
- Every bullet in the Changes section must trace to something in the diff
- Do not invent testing steps that are not implied by the code changes
- If a section has no relevant content, omit it entirely (do not write "N/A" or leave it empty)
- Screenshots section: only include if there are UI changes visible in the diff
- If commit messages explain the "why", use that context in the Summary

**QA checkpoint:** Before presenting, verify:
- [ ] Summary is 1-2 sentences, active voice, no filler
- [ ] Every change bullet is specific and traces to the diff
- [ ] No invented metrics or outcomes
- [ ] Testing steps are actionable (someone could follow them)
- [ ] No em dashes in any line

---

## Step 5: Create or Update the PR

Present the description to the user and ask: "Ready to create the PR, update the existing one, or output only?"

**Create a new PR:**

Pass the body via stdin to handle backticks, quotes, and newlines safely:
```bash
gh pr create --title "TITLE_HERE" --body-file - << 'EOF'
BODY_HERE
EOF
```

Suggest a title based on the commit messages and diff summary. The title should be imperative mood, under 72 characters: "Add Redis caching for user session lookups" not "Added caching".

**Update an existing PR:**
```bash
gh pr edit --body-file - << 'EOF'
BODY_HERE
EOF
```

**Output only:** Present the title and body in a code block for manual copy-paste.

After creating or updating, confirm: "PR description updated. View it at: [URL]"




