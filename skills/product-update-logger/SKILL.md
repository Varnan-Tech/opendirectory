---
name: product-update-logger
description: Tell the skill what your product shipped. It writes a polished dated entry to a living docs/changelog.md and produces a ready-to-use content package: tweet thread, LinkedIn post, email snippet, and one-liner.
---

# product-update-logger

Tell this skill what your product shipped. It writes a polished changelog entry to `docs/changelog.md` (a living log, newest entry first) and simultaneously produces a content package: tweet thread, LinkedIn post, email snippet, and one-liner.

Input sources: free text from your message, git commits auto-read from the local repo, or GitHub PRs if you provide a repo. Any combination works.

## Reference Files

Read these files before each run:

```bash
cat references/changelog-format.md
cat references/content-rules.md
cat references/noise-filter.md
```

---

## Step 1: Setup Check

```bash
echo "GITHUB_TOKEN: ${GITHUB_TOKEN:-not set -- GitHub PR fetching disabled}"
echo "Git:          $(git rev-parse --is-inside-work-tree 2>/dev/null && echo 'repo detected' || echo 'not a git repo')"
echo "Changelog:    $(ls docs/changelog.md 2>/dev/null && echo 'exists' || echo 'will be created')"
```

Note whether git is available and whether a changelog already exists. This determines the version label format.

---

## Step 2: Parse Input

Collect from the conversation:

- `items` -- free text description of what shipped (pipe-separated if multiple). Optional if git is available.
- `since` -- how many days back to look. Default: 7. User may say "last 2 weeks" (14) or "since last release."
- `repo` -- GitHub "owner/repo" for PR fetching. Optional.
- `version_label` -- custom label like "v2.1.0" or "The Speed Update." Optional; default is date-based.

**If the user said nothing about items AND there is no git repo:** Ask "What did you ship? List the features, fixes, or improvements -- one per line."

**If git is available and user said nothing specific:** Proceed with git auto-read in Step 3. Show the user what was found and confirm before transforming.

Write parsed input:

```bash
python3 << 'PYEOF'
import json, os, re

inp = {
    "items": "",          # FILL: pipe-separated free text, or "" if none
    "since": 7,           # FILL: integer days
    "repo": "",           # FILL: "owner/repo" or ""
    "version_label": ""   # FILL: "" means auto (date-based), or custom string
}

with open("/tmp/pul-input.json", "w") as f:
    json.dump(inp, f, indent=2)
print(f"Since: {inp['since']} days")
print(f"Free text items: {inp['items'] or 'none (will use git/GitHub)'}")
print(f"GitHub repo: {inp['repo'] or 'none'}")
print(f"Version label: {inp['version_label'] or 'auto (date-based)'}")
PYEOF
```

---

## Step 3: Run the Gather Script

```bash
ls scripts/gather.py 2>/dev/null && echo "script found" || echo "ERROR: scripts/gather.py not found"
```

```bash
GITHUB_TOKEN="${GITHUB_TOKEN:-}" python3 scripts/gather.py \
    --since "$(python3 -c "import json; print(json.load(open('/tmp/pul-input.json'))['since'])")" \
    --repo "$(python3 -c "import json; print(json.load(open('/tmp/pul-input.json'))['repo'])")" \
    --items "$(python3 -c "import json; print(json.load(open('/tmp/pul-input.json'))['items'])")" \
    --output /tmp/pul-raw.json
```

Verify output:

```bash
python3 -c "
import json
with open('/tmp/pul-raw.json') as f:
    d = json.load(f)
print(f'Items found:      {d[\"total_items\"]}')
print(f'Noise filtered:   {d[\"noise_filtered\"]}')
print(f'Git available:    {d[\"git_available\"]}')
print(f'GitHub available: {d[\"github_available\"]}')
print(f'Sources: git={sum(1 for i in d[\"items\"] if i[\"source\"]==\"git_commit\")}, '
      f'prs={sum(1 for i in d[\"items\"] if i[\"source\"]==\"github_pr\")}, '
      f'text={sum(1 for i in d[\"items\"] if i[\"source\"]==\"free_text\")}')
print()
print('Items:')
for item in d['items']:
    print(f'  [{item[\"source\"]}] {item[\"subject\"]}')
"
```

**If total_items == 0:** Stop. Tell the user: "No shipped items found. Either describe what you shipped, point me to a git repo with recent commits, or add a GitHub repo with `repo: owner/repo` and a GITHUB_TOKEN."

**Show the item list to the user and ask: "These are the items I found. Anything to add or remove before I write the changelog?"**

Wait for confirmation or edits. If the user says "looks good", "proceed", or makes no changes, continue. If the user adds or removes items, update `/tmp/pul-raw.json` accordingly before Step 4.

---

## Step 4: Generate Changelog Entry

Print items for context:

```bash
python3 -c "
import json
with open('/tmp/pul-raw.json') as f:
    d = json.load(f)
print(json.dumps(d['items'], indent=2))
print()
print(f'Existing changelog format: {d[\"existing_changelog\"][\"format\"]}')
print(f'Last label: {d[\"existing_changelog\"][\"last_label\"]}')
print(f'Today: {d[\"date\"]}')
"
```

**AI instructions:** Transform each raw item from technical language to user-facing benefit language. Follow `references/changelog-format.md` for transformation rules and examples.

Rules:
- **Do NOT invent outcomes or metrics.** "40% faster" must come from the source data. If no number is in the commit or PR, do not add one.
- **Use past tense:** "Added", "Fixed", "Improved" -- not "Adds", "Fixes"
- **Assign exactly one category** to each item: New, Improved, Fixed, or Under the hood
- **Under the hood:** Only include if developer-relevant (API changes, breaking changes). Omit empty sections.
- **Omit** anything that maps to: test changes, CI changes, documentation-only commits

Determine version label:
- If user specified one: use it exactly
- If `existing_changelog.format == "semver"`: increment based on changes (patch for fixes only, minor for any new feature)
- Default: `Week of [Month Day, Year]` using today's date

Write the entry to `/tmp/pul-entry.json`:

```json
{
  "label": "Week of April 23, 2026",
  "date": "2026-04-23",
  "new": [
    {"title": "Dark mode", "description": "Toggle in Settings > Appearance. Works across all views."}
  ],
  "improved": [
    {"title": "API response time", "description": "40% faster on average. Dashboard now loads in under 1 second."}
  ],
  "fixed": [
    {"title": "CSV export", "description": "Exports no longer drop the last row."}
  ],
  "under_the_hood": []
}
```

Verify the entry:

```bash
python3 -c "
import json
with open('/tmp/pul-entry.json') as f:
    e = json.load(f)
print(f'Label: {e[\"label\"]}')
total = 0
for cat in ['new', 'improved', 'fixed', 'under_the_hood']:
    items = e.get(cat, [])
    if items:
        print(f'{cat.replace(\"_\", \" \").title()} ({len(items)}):')
        for item in items:
            print(f'  - {item[\"title\"]}: {item[\"description\"]}')
        total += len(items)
print(f'Total: {total} items')
"
```

---

## Step 5: Generate Content Package

Using the changelog entry from Step 4, generate all four content pieces. Follow `references/content-rules.md` strictly.

**One-liner** (max 20 words): One sentence covering the biggest 1-2 items. Plain language, no jargon.

**Tweet thread** (3-5 tweets):
- Tweet 1: Hook -- "We shipped [N] things this week." or lead with the biggest feature
- Tweets 2-N: One item per tweet, 1-2 sentences max
- Last tweet: "Changelog: [link]" or "More next week." (optional)
- Each tweet strictly under 280 characters
- No hashtags. No em dashes. Active voice.

**LinkedIn post**:
- No markdown (asterisks render as literal on LinkedIn)
- No hashtags
- Founder voice: "We shipped", not "We are excited to announce"
- Short paragraphs (1-2 sentences each), blank lines between them
- Close with a question or observation, not a CTA
- 150-400 words total

**Email snippet**:
- Subject: "What shipped this week: [biggest item] + [1 more]"
- Body: 50-100 words. "Here's what we shipped this week:" then bullets.

Write to `/tmp/pul-content.json`:

```json
{
  "one_liner": "Dark mode, faster API, and a fixed export bug.",
  "tweet_thread": [
    "We shipped 3 things this week.",
    "Dark mode is live. Toggle it in Settings > Appearance. Works everywhere.",
    "API response time is now 40% faster. Dashboard loads in under a second.",
    "Fixed: CSV exports were dropping the last row. That's gone now.",
    "Changelog: [link]"
  ],
  "linkedin_post": "We shipped 3 updates this week.\n\nDark mode is live. Toggle it in Settings under Appearance. It works across every view.\n\nAPI response time is 40% faster on average. The dashboard now loads in under a second for most users.\n\nWe also fixed a bug where CSV exports were silently dropping the last row. If you hit this and stopped exporting, it's worth trying again.\n\nWhat feature have you been waiting for?",
  "email_snippet": {
    "subject": "What shipped this week: dark mode + faster API",
    "body": "Here's what we shipped this week:\n\n- Dark mode: toggle in Settings > Appearance\n- API response time: 40% faster, dashboard loads under 1 second\n- Fixed: CSV exports no longer drop the last row\n\nFull changelog below."
  }
}
```

---

## Step 6: Self-QA

```bash
python3 -c "
import json, re

with open('/tmp/pul-raw.json') as f:
    raw = json.load(f)
with open('/tmp/pul-entry.json') as f:
    entry = json.load(f)
with open('/tmp/pul-content.json') as f:
    content = json.load(f)

full_text = json.dumps(entry) + json.dumps(content)
fails = 0

# Check 1: No em dashes
if chr(8212) in full_text:
    print('FAIL: em dash found -- replace with hyphen')
    fails += 1
else:
    print('PASS: no em dashes')

# Check 2: Banned words
banned = ['powerful', 'robust', 'seamless', 'innovative', 'game-changing',
          'streamline', 'leverage', 'transform', 'revolutionize', 'excited to announce',
          'pleased to announce', 'we are thrilled', 'cutting-edge', 'best-in-class',
          'world-class', 'unlock', 'delightful']
found = [w for w in banned if w.lower() in full_text.lower()]
if found:
    print(f'FAIL: banned words found: {found}')
    fails += 1
else:
    print('PASS: no banned words')

# Check 3: Tweet length
thread = content.get('tweet_thread', [])
long_tweets = [(i+1, len(t)) for i, t in enumerate(thread) if len(t) > 280]
if long_tweets:
    print(f'FAIL: tweets over 280 chars: {long_tweets}')
    fails += 1
else:
    print(f'PASS: all {len(thread)} tweets under 280 chars')

# Check 4: LinkedIn no hashtags
li = content.get('linkedin_post', '')
if re.search(r'#[A-Za-z]', li):
    print('FAIL: hashtags found in LinkedIn post')
    fails += 1
else:
    print('PASS: no hashtags in LinkedIn')

# Check 5: No markdown in LinkedIn
if '**' in li or '__' in li:
    print('FAIL: markdown formatting in LinkedIn (renders as literal asterisks)')
    fails += 1
else:
    print('PASS: no markdown in LinkedIn')

# Check 6: One-liner word count
one_liner = content.get('one_liner', '')
word_count = len(one_liner.split())
if word_count > 20:
    print(f'FAIL: one-liner is {word_count} words (max 20)')
    fails += 1
else:
    print(f'PASS: one-liner is {word_count} words')

# Check 7: Item count
entry_items = (len(entry.get('new', [])) + len(entry.get('improved', [])) +
               len(entry.get('fixed', [])) + len(entry.get('under_the_hood', [])))
raw_total = raw['total_items']
print(f'INFO: {entry_items} changelog items from {raw_total} raw items')

print()
print(f'Result: {\"PASS\" if fails == 0 else f\"FAIL ({fails} issues)\"}')
"
```

**If any check fails:** Fix the issue in the relevant temp file before proceeding to Step 7. Re-run the check after fixing.

---

## Step 7: Append to Changelog + Save Content

```bash
python3 << 'PYEOF'
import json, os, re

with open('/tmp/pul-entry.json') as f:
    entry = json.load(f)
with open('/tmp/pul-content.json') as f:
    content = json.load(f)

# Build the new changelog section
lines = [f"## {entry['label']}", ""]

CAT_HEADERS = {
    "new": "### New",
    "improved": "### Improved",
    "fixed": "### Fixed",
    "under_the_hood": "### Under the hood",
}

for cat, header in CAT_HEADERS.items():
    items = entry.get(cat, [])
    if items:
        lines.append(header)
        for item in items:
            lines.append(f"- **{item['title']}** -- {item['description']}")
        lines.append("")

lines.append("---")
lines.append("")
new_section = "\n".join(lines)

# Prepend to docs/changelog.md
os.makedirs("docs", exist_ok=True)
changelog_path = "docs/changelog.md"

if os.path.exists(changelog_path):
    existing = open(changelog_path).read()
    # Insert after the top-level heading (if any) or at the very top
    if existing.startswith("# "):
        end_of_heading = existing.index("\n") + 1
        updated = existing[:end_of_heading] + "\n" + new_section + existing[end_of_heading:]
    else:
        updated = new_section + existing
else:
    updated = "# Changelog\n\n" + new_section

with open(changelog_path, "w") as f:
    f.write(updated)

print(f"Changelog updated: {changelog_path}")

# Save content package
date = entry['date']
content_dir = "docs/product-updates"
os.makedirs(content_dir, exist_ok=True)
content_path = f"{content_dir}/{date}-content.md"

content_lines = [
    f"# Content Package: {entry['label']}",
    "",
    "## One-liner",
    content.get('one_liner', ''),
    "",
    "## Tweet Thread",
    "",
]
thread = content.get('tweet_thread', [])
for i, tweet in enumerate(thread, 1):
    content_lines.append(f"[{i}/{len(thread)}] {tweet}")
    content_lines.append("")

content_lines += [
    "## LinkedIn Post",
    "",
    content.get('linkedin_post', ''),
    "",
    "## Email Snippet",
    "",
    f"Subject: {content.get('email_snippet', {}).get('subject', '')}",
    "",
    content.get('email_snippet', {}).get('body', ''),
    "",
]

with open(content_path, "w") as f:
    f.write("\n".join(content_lines))

print(f"Content package: {content_path}")
PYEOF
```

---

## Step 8: Clean Up and Present

```bash
rm -f /tmp/pul-input.json /tmp/pul-raw.json /tmp/pul-entry.json /tmp/pul-content.json
echo "Done."
```

Present to the user in this order:

**1. Changelog entry** (formatted markdown, not raw JSON):

```
## Week of April 23, 2026

### New
- **Dark mode** -- Toggle in Settings > Appearance. Works across all views.

### Improved
- **API response time** -- 40% faster on average. Dashboard now loads in under 1 second.

### Fixed
- **CSV export** -- Exports no longer drop the last row.
```

**2. Content package:**

- One-liner: `[text]`
- Tweet thread: numbered list of tweets
- LinkedIn post: full text
- Email snippet: subject line + body

**3. Saved files:**
- `docs/changelog.md` -- updated (new entry prepended)
- `docs/product-updates/[date]-content.md` -- full content package saved

---

## Common Mistakes

| The agent will want to... | Why that's wrong |
|---|---|
| Invent outcomes or metrics | Every claim must come from the raw items. "40% faster" needs to come from the commit message or PR body. If no number is present, don't add one. |
| Write "We are excited to announce" | Banned. Use "We shipped", "[Feature] is now live", or just state the fact. |
| Use markdown bold (**) in LinkedIn | LinkedIn renders ** as literal asterisks. Plain text only. |
| Add hashtags to LinkedIn or tweets | This skill never uses hashtags. |
| Put all items in "New" | Bugs are Fixed, speed improvements are Improved. Miscategorizing weakens the changelog. |
| Skip the confirmation step in Step 3 | Always show the item list and ask the user to confirm before transforming. This prevents wrong-branch commits or stale items. |
| Include empty "Under the hood" section | Omit if empty. Silence is better than noise. |
| Combine multiple items into one tweet | One item per tweet. Specificity > breadth. |
| Pad with filler tweets | If there's one real item, write 2 tweets. Don't pad to 5. |
