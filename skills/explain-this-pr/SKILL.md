---
name: explain-this-pr
description: Takes a GitHub PR URL or the current branch and writes a plain-English explanation of what it does and why, then posts it as a PR comment. Use when asked to explain a PR, summarize a pull request, write a plain-English description of a PR, add a summary comment to a PR, or understand what a PR changes. Trigger when a user says "explain this PR", "summarize this pull request", "what does this PR do", "add a comment explaining the PR", or shares a GitHub PR URL and asks what it does.
author: OpenDirectory
version: 1.0.0
---

# Explain This PR

Read a GitHub pull request, understand what it changes, and write a plain-English explanation. Post it as a PR comment so reviewers have instant context.

---

## Step 1: Check Setup

Confirm `gh` is authenticated:

```bash
gh auth status
```

If not authenticated: `gh auth login` and follow the prompts.

Confirm input. The user must provide one of:
- A GitHub PR URL (e.g. `https://github.com/owner/repo/pull/123`)
- A PR number in the current repo (e.g. `#123`)
- The keyword "current" to use the PR for the current branch

If no input, ask: "Which PR should I explain? Share the URL, PR number, or say 'current' for the active branch."

---

## Step 2: Fetch PR Context

**Get PR metadata:**
```bash
gh pr view PR_URL_OR_NUMBER --json number,url,title,body,author,baseRefName,headRefName,additions,deletions,changedFiles,commits,labels,state,isDraft
```

If `isDraft` is `true`, note this to the user: "This PR is still in draft. The explanation is based on its current state."

**Get the diff:**
```bash
gh pr diff PR_URL_OR_NUMBER
```

If the diff is over 400 lines, read the `--stat` summary and the first 200 lines of the diff:
```bash
gh pr view PR_URL_OR_NUMBER --json files
gh pr diff PR_URL_OR_NUMBER | head -200
```

**Get existing comments (to avoid repeating what is already there):**
```bash
gh pr view PR_URL_OR_NUMBER --json comments --jq '.comments[].body' 2>/dev/null | head -20
```

---

## Step 3: Write the Explanation

Write two paragraphs. Read each rule before writing.

**Paragraph 1: What it does (technical)**

- One sentence per major change
- Name the specific files, functions, or systems that changed
- State the before/after if the diff makes it clear
- Include concrete numbers if present in the diff (lines removed, tables dropped, endpoints added)
- Active voice, present tense

Example:
```
Replaces the in-memory session cache in auth.middleware.ts with a Redis-backed cache (src/cache/redis.ts). Adds get, set, and invalidate methods to the new Redis module and wraps UserService.getById() with a 5-minute TTL. Removes the Map-based cache that was limited to a single process and caused session drift across multiple instances.
```

**Paragraph 2: Why it matters (business/product impact)**

- Who benefits and how
- What problem this solves or what risk it reduces
- If the commit messages contain a "why", use that context
- If there is no clear "why" in the diff or commits, omit this paragraph rather than guessing

Example:
```
Users hitting the /api/me endpoint under load were getting inconsistent session data across server instances, causing intermittent 401 errors. This change makes session state consistent across all instances and reduces database load by eliminating one query per authenticated request.
```

**Rules for both paragraphs:**
- No em dashes — use a comma or period
- No filler: "this PR", "this change", "as you can see"
- No invented outcomes. Only state impacts that are directly visible in the diff or commit messages
- If the PR is a pure refactor with no behavior change, say that explicitly: "Refactors X to Y with no change in observable behavior."
- Under 150 words total

---

## Step 4: Self-QA

Before posting, check:

- [ ] Paragraph 1 names specific files or functions from the diff
- [ ] No invented metrics or outcomes
- [ ] No em dashes
- [ ] No filler phrases
- [ ] Under 150 words total
- [ ] If no clear "why" exists, paragraph 2 is omitted rather than guessing

Fix any violation before posting.

---

## Step 5: Post as PR Comment

Present the explanation to the user. Ask: "Ready to post this as a PR comment, or would you like to edit it first?"

On confirmation, pass the body via stdin to handle backticks, quotes, and newlines safely:

```bash
gh pr comment PR_URL_OR_NUMBER --body-file - << 'EOF'
EXPLANATION_HERE
EOF
```

After posting: "Comment added. View it at: [url from Step 2]"

If the user says "output only", present the explanation in a code block for manual copy-paste without posting.


