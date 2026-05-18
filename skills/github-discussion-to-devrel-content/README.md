# github-discussion-to-devrel-content

Your users keep asking the same questions in GitHub Discussions. This skill finds those patterns, tells you which docs to fix first, and drafts the actual FAQ entries and content angles — backed by verbatim quotes and direct links to the threads that prove the gap is real.

You get two ranked lists: documentation holes with ready-to-paste fix drafts, and content opportunities with specific angles and outlines. Unanswered community pain gets flagged as urgent.

---

## Installation

```bash
npx "@opendirectory.dev/skills" install --target claude github-discussion-to-devrel-content
```

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

---

## What It Does

- Scans your own repo's Discussions (not competitors' — that's `gh-issue-to-demand-signal`)
- Clusters recurring confusion by underlying concept, not surface keywords
- Ranks each cluster by frequency, engagement, recency, and unanswered rate
- Drafts the actual FAQ / doc fix as a Markdown snippet you can paste into your docs
- Generates a specific content angle and outline for each content opportunity
- Flags unanswered community pain as ⚠️ URGENT so you know what's bleeding
- Refuses to fabricate patterns when data is thin (low-signal guard built in)

## What It Does NOT Do

- Does not mine competitor repos — use `gh-issue-to-demand-signal` for outbound GTM signals
- Does not write full-length blog posts or published docs pages — use `noise2blog` to expand a draft into a finished asset
- Does not post to LinkedIn, Twitter, or any platform
- Does not predict SEO, engagement, or content performance outcomes
- Does not access private repositories

---

## Requirements

| Requirement | Purpose | How to Get |
|---|---|---|
| GitHub Personal Access Token | Fetch discussions via GraphQL API | [github.com/settings/tokens](https://github.com/settings/tokens) — enable `read:discussion` scope |
| Python 3.10+ | Run the fetcher script | No external packages required — stdlib only |

No paid APIs. No third-party SaaS. Free GitHub accounts work.

---

## Setup

```bash
cp .env.example .env
# Edit .env and add your GITHUB_TOKEN
```

---

## How to Use

### Step 1 — Fetch Discussions

```bash
# Basic usage (last 90 days, all categories, min 3 comments)
python scripts/fetch_discussions.py --repo owner/repo

# Filter to Q&A category only
python scripts/fetch_discussions.py --repo owner/repo --category "Q&A"

# Docs gaps only, last 60 days
python scripts/fetch_discussions.py --repo owner/repo --days-back 60 --mode docs

# Content opportunities only
python scripts/fetch_discussions.py --repo owner/repo --mode content

# Full GitHub URL also accepted
python scripts/fetch_discussions.py --repo https://github.com/owner/repo
```

Output: `discussions_raw.json` in the working directory.

### Step 2 — Run the Skill

Once `discussions_raw.json` is present, tell your agent:

```
"Run the github-discussion-to-devrel-content skill and produce the DevRel backlog."
```

Or:

```
"Analyze discussions_raw.json and generate devrel-backlog.md"
```

Output: `devrel-backlog.md` — a ranked Markdown report ready to commit.

---

## CLI Options

| Flag | Default | Description |
|---|---|---|
| `--repo` | required | `owner/repo` or full GitHub URL |
| `--days-back` | 90 | Days of discussion history to inspect |
| `--min-comments` | 3 | Minimum comment count to include a discussion |
| `--max-items` | 100 | Cap on discussions fetched (API cost control) |
| `--category` | all | Filter by discussion category name (e.g., `Q&A`) |
| `--mode` | combined | `docs`, `content`, or `combined` |
| `--output` | `discussions_raw.json` | Output file path |

---

## Output

`devrel-backlog.md` contains:

**Run Summary** — repo, date, discussions analyzed, clusters found, mode.

**Docs / FAQ Gaps** — Up to 7 ranked items. Each includes:
- Priority score (0–100, relative ranking within this run)
- Frequency and engagement metrics
- A verbatim evidence quote from the thread
- A direct link to the source discussion
- A ready-to-paste **Draft FAQ / Doc Update** as a Markdown snippet
- ⚠️ URGENT badge if the community pain is unresolved

**Content Opportunities** — Up to 7 ranked items. Each includes:
- A working content title and type (blog post, tutorial, FAQ entry, Twitter thread, video script)
- Why this matters for the founder
- A verbatim evidence quote and source link
- A **Recommended Angle** and 3–4 point outline tied to the community confusion

> **Note on scores:** Priority scores are relative rankings within this analysis run, not absolute quality measures. A score of 84 ranks higher than a score of 71 in this dataset. Scores are not comparable across different repos or different run configurations.

---

## Project Structure

```
github-discussion-to-devrel-content/
├── SKILL.md
├── README.md
├── .env.example
├── scripts/
│   └── fetch_discussions.py
├── evals/
│   └── evals.json
└── references/
    ├── output-format.md
    └── scoring-guide.md
```

---

## License

MIT


