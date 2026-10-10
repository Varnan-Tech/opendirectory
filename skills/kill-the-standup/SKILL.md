---
name: kill-the-standup
description: Reads yesterday's Linear issues and GitHub commits for the authenticated user, formats a standup update (done / doing / blockers), and posts it to Slack. Use when asked to write a standup, generate a standup update, post to the standup channel, summarize yesterday's work, or automate the daily standup. Trigger when a user says "write my standup", "post standup", "generate standup update", "what did I do yesterday", or "kill the standup".
author: OpenDirectory
version: 1.0.0
---

# Kill the Standup

Read yesterday's Linear issues and GitHub commits. Format a standup update. Post it to Slack.

---

## Step 1: Setup Check

Confirm required env vars are set:

```bash
echo "LINEAR_API_KEY: ${LINEAR_API_KEY:+set}"
echo "SLACK_WEBHOOK_URL: ${SLACK_WEBHOOK_URL:+set}"
echo "GITHUB_REPO: ${GITHUB_REPO:-not set}"
echo "GITHUB_USERNAME: ${GITHUB_USERNAME:-not set}"
```

**If LINEAR_API_KEY is missing:**
Stop. Tell the user: "LINEAR_API_KEY is required. Get it from Linear → Settings → API → Personal API keys. Add it to your .env file."

**If SLACK_WEBHOOK_URL is missing:**
Stop. Tell the user: "SLACK_WEBHOOK_URL is required. Create an Incoming Webhook at api.slack.com/apps → Your App → Incoming Webhooks. Add it to your .env file."

**If GITHUB_REPO is missing:**
Continue. GitHub commits will be skipped. Note this to the user.

---

## Step 2: Fetch Linear Activity

Compute yesterday's date in ISO 8601 format (e.g. `2026-04-09T00:00:00.000Z`).

**Get current user ID:**
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: Bearer $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "query { viewer { id name email } }"}'
```

Extract the `id` field from the response. Store as `LINEAR_USER_ID`.

**Fetch issues assigned to me, updated since yesterday:**
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: Bearer $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query($since: DateTime!, $userId: ID!) { issues(first: 50, filter: { assignee: { id: { eq: $userId } } updatedAt: { gte: $since } }) { edges { node { identifier title state { name } url completedAt updatedAt createdAt } } } }",
    "variables": {"since": "YESTERDAY_ISO", "userId": "LINEAR_USER_ID"}
  }'
```

**Categorize issues:**
- `completedAt` is non-null → **Done**
- `state.name` is "In Progress", "Started", or "In Review" → **Doing**
- `state.name` is "Cancelled" → skip
- `state.name` is "Todo" or "Backlog" → skip (not worked on)

If zero issues: note "No Linear activity found for yesterday."

---

## Step 3: Fetch GitHub Commits

Skip this step silently if GITHUB_REPO is not set.

If GITHUB_REPO is set:

```bash
gh api "repos/$GITHUB_REPO/commits?author=${GITHUB_USERNAME:-$(gh api user --jq .login)}&since=YESTERDAY_ISO&per_page=30" \
  --jq '[.[] | {message: .commit.message, url: .html_url}]'
```

**Process commits:**
- Extract the first line of each commit message (everything before the first newline)
- Skip merge commits: drop any message starting with "Merge"
- Deduplicate by message text

If GITHUB_REPO is set but returns zero commits: note "No commits found yesterday."

---

## Step 4: Format Standup

Read `references/standup-format.md` in full before writing.

Produce the standup in this exact structure:

```
**Done**
- [ENG-123] Title of completed issue
- fix: commit message here

**Doing**
- [ENG-124] Title of in-progress issue

**Blockers**
No blockers.
```

Rules from standup-format.md:
- No first-person pronouns ("I", "we")
- Past tense for Done items, present continuous for Doing items
- Each Linear item uses the `[IDENTIFIER] Title` format
- Each GitHub commit uses the first line of the commit message
- If no Done items: write "Nothing completed." under Done
- If no Doing items: write "Nothing in progress." under Doing
- If no blockers: write "No blockers."
- Under 200 words total

---

## Step 5: Post to Slack or Output

Present the formatted standup to the user.

Ask: "Post this to Slack, or output only?"

**On confirmation to post:**

```bash
curl -s -X POST "$SLACK_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "blocks": [
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Standup — DATE_HERE*\n\n*Done*\nITEMS\n\n*Doing*\nITEMS\n\n*Blockers*\nITEMS"
        }
      }
    ]
  }'
```

Pass the body via a temp file or heredoc to avoid shell quoting issues with special characters in commit messages or issue titles:

```bash
cat > /tmp/standup-payload.json << 'ENDJSON'
{
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "STANDUP_CONTENT_HERE"
      }
    }
  ]
}
ENDJSON
curl -s -X POST "$SLACK_WEBHOOK_URL" -H "Content-Type: application/json" -d @/tmp/standup-payload.json
```

After posting: "Standup posted."

**On "output only":** Print the standup in a code block for copy-paste.


