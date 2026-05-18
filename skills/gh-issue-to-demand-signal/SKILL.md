---
name: gh-issue-to-demand-signal
description: Takes a competitor's public GitHub repo URL, fetches their open issues via the GitHub REST API, filters noise locally, clusters issues into 6 demand categories, computes a demand score per issue and per cluster, and outputs a ranked demand gap report with a GTM messaging brief. Use when asked to scan a competitor's GitHub issues, find what their users are begging for, turn GitHub complaints into product positioning, identify competitor feature gaps, or generate messaging from real user demand. Trigger when a user says "scan competitor issues", "what are users asking for on X repo", "find demand gaps in Y", "turn GitHub issues into messaging", or "what should I build based on competitor complaints".
compatibility: [claude-code, gemini-cli, github-copilot]
---

# GitHub Issue Demand Signal

Take a competitor's public GitHub repo. Fetch their open issues. Filter noise locally. Cluster into 6 demand categories. Score by real engagement. Output a ranked demand gap report and GTM messaging brief.

---

**Critical rule:** Every issue title in the output must be verbatim from the GitHub API response. Every cluster theme name must be derived from actual issue titles in that cluster. If fewer than 10 issues remain after noise filtering, stop and tell the user -- the repo is too small for reliable clustering. No invented issue content anywhere.

---

## Common Mistakes

| The agent will want to... | Why that's wrong |
|---|---|
| Send all 200 raw issues to the AI without filtering | Bot issues, PRs, and zero-engagement noise inflate cluster counts and waste context. Filter locally first. |
| Use comment count as the primary demand signal | Comments include maintainer responses, off-topic discussion, and spam. reactions["+1"] is the cleanest buyer signal. |
| Paraphrase issue titles when summarizing clusters | Paraphrasing loses the buyer's exact language, which is the entire point. Use verbatim issue titles. |
| Continue past Step 4 if fewer than 10 issues remain after filtering | Under 10 issues means the repo is too small or the wrong URL was given. Clustering on sparse data produces meaningless categories. |
| Include pull requests in the analysis | The GitHub Issues endpoint returns PRs too. Filter by checking that the pull_request key is absent on the issue object. |
| Mark an issue as ignored demand without checking all 3 criteria | All three must be true: reactions >= 10, age >= 180 days, no planned/in-progress/roadmap label. Missing one criterion disqualifies the issue. |

---

## Step 1: Setup Check

```bash
echo "GITHUB_TOKEN: ${GITHUB_TOKEN:-not set, unauthenticated rate limit applies (60 req/hr)}"
```

**If GITHUB_TOKEN is not set:** Continue. Tell the user: "GITHUB_TOKEN is not set. Unauthenticated rate limit is 60 requests/hour -- enough for 2 fetches before hitting the limit. For repeated use, add a token at github.com/settings/tokens (no scopes needed for public repos)."

---

## Step 2: Gather Input

You need:
- GitHub repo URL (e.g. https://github.com/owner/repo) or owner/repo slug (e.g. facebook/react)

Parse owner and repo from input:

```bash
python3 << 'PYEOF'
import re, sys, os

raw = "REPO_INPUT_HERE"

# Normalize to owner/repo
if raw.startswith("http"):
    m = re.search(r"github\.com/([^/]+)/([^/?\s]+)", raw)
    if not m:
        print("ERROR: Could not parse GitHub URL. Expected format: https://github.com/owner/repo")
        sys.exit(1)
    owner, repo = m.group(1), m.group(2).rstrip("/")
elif "/" in raw:
    parts = raw.strip().split("/")
    owner, repo = parts[0], parts[1]
else:
    print("ERROR: Input must be a GitHub URL or owner/repo slug (e.g. vercel/next.js)")
    sys.exit(1)

print(f"Owner: {owner}")
print(f"Repo: {repo}")

with open("/tmp/ghd-target.txt", "w") as f:
    f.write(f"{owner}/{repo}")
PYEOF
```

**If parsing fails:** Stop. Ask: "Please provide the GitHub repo as a URL (https://github.com/owner/repo) or an owner/repo slug (e.g. vercel/next.js)."

---

## Step 3: Fetch Issues from GitHub REST API

Fetch up to 200 issues (2 pages of 100). Check rate limit after the first fetch.

```bash
python3 << 'PYEOF'
import json, urllib.request, os, sys
from datetime import datetime, timezone

target = open("/tmp/ghd-target.txt").read().strip()
owner_repo = target
token = os.environ.get("GITHUB_TOKEN", "")

headers = {"Accept": "application/vnd.github+json", "User-Agent": "gh-issue-demand-signal/1.0"}
if token:
    headers["Authorization"] = f"Bearer {token}"

all_issues = []
rate_limit_hit = False

for page in [1, 2]:
    url = f"https://api.github.com/repos/{owner_repo}/issues?state=open&per_page=100&page={page}"
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            # Check rate limit after first page
            if page == 1:
                remaining = int(resp.headers.get("X-RateLimit-Remaining", 999))
                reset_ts = resp.headers.get("X-RateLimit-Reset", "")
                if remaining == 0:
                    reset_str = datetime.fromtimestamp(int(reset_ts), tz=timezone.utc).strftime("%H:%M UTC") if reset_ts else "unknown"
                    print(f"ERROR: GitHub rate limit exhausted. Resets at {reset_str}.")
                    print("Add GITHUB_TOKEN to your .env file to get 5000 req/hr. See github.com/settings/tokens (no scopes needed).")
                    sys.exit(1)
                print(f"Rate limit remaining: {remaining}")

                # Check for 404/403
                status = resp.status
                if status == 404:
                    print(f"ERROR: Repo '{owner_repo}' not found. Check the URL or slug.")
                    sys.exit(1)

            page_data = json.loads(resp.read())
            if not page_data:
                print(f"Page {page}: empty, stopping.")
                break
            all_issues.extend(page_data)
            print(f"Page {page}: {len(page_data)} issues fetched")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"ERROR: Repo '{owner_repo}' not found (404). Check the URL or slug.")
        elif e.code == 403:
            print(f"ERROR: Access denied (403). Repo may be private or rate limit hit.")
        else:
            print(f"ERROR: GitHub API returned HTTP {e.code}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to fetch page {page}: {e}")
        sys.exit(1)

print(f"Total raw issues fetched: {len(all_issues)}")
json.dump(all_issues, open("/tmp/ghd-raw-issues.json", "w"), indent=2)
PYEOF
```

**If GitHub returns 404:** Stop. Tell the user: "Repo not found. Check the URL or slug and try again. Private repos are not accessible without authentication and explicit repo scope."

**If GitHub returns 403 with rate limit header:** Stop. Show the reset time and tell the user to add GITHUB_TOKEN.

---

## Step 4: Pre-Process Locally -- Filter, Score, Detect Ignored Demand

No API call. Pure Python. Run before anything goes to the AI.

```bash
python3 << 'PYEOF'
import json, re
from datetime import datetime, timezone

raw = json.load(open("/tmp/ghd-raw-issues.json"))
target = open("/tmp/ghd-target.txt").read().strip()
now = datetime.now(tz=timezone.utc)

noise_patterns = re.compile(
    r"^(chore|deps|bump|renovate|dependabot|release|ci|build|revert)[\s:\[]",
    re.IGNORECASE
)
pr_title_patterns = re.compile(
    r"^(feat|fix|refactor|docs|test|style|perf|chore)(\(.+\))?:",
    re.IGNORECASE
)

filtered = []
noise_count = 0
noise_reasons = {}

for issue in raw:
    # Skip pull requests (GitHub Issues endpoint returns PRs too)
    if "pull_request" in issue:
        noise_count += 1
        noise_reasons["pull_request"] = noise_reasons.get("pull_request", 0) + 1
        continue

    title = issue.get("title", "")
    reactions = issue.get("reactions", {}).get("+1", 0)
    comments = issue.get("comments", 0)
    user_type = (issue.get("user") or {}).get("type", "User")

    # Skip bot-authored issues
    if user_type == "Bot":
        noise_count += 1
        noise_reasons["bot_author"] = noise_reasons.get("bot_author", 0) + 1
        continue

    # Skip bot-pattern titles
    if noise_patterns.match(title):
        noise_count += 1
        noise_reasons["bot_title"] = noise_reasons.get("bot_title", 0) + 1
        continue

    # Skip PR-as-issue titles
    if pr_title_patterns.match(title):
        noise_count += 1
        noise_reasons["pr_as_issue"] = noise_reasons.get("pr_as_issue", 0) + 1
        continue

    # Skip zero-signal issues
    if reactions == 0 and comments == 0:
        noise_count += 1
        noise_reasons["zero_signal"] = noise_reasons.get("zero_signal", 0) + 1
        continue

    # Compute demand score
    demand_score = (reactions * 2) + (comments * 0.5)

    # Detect ignored demand
    created_at = issue.get("created_at", "")
    if created_at:
        created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        age_days = (now - created).days
    else:
        age_days = 0

    labels = [l.get("name", "").lower() for l in issue.get("labels", [])]
    has_planned_label = any(
        kw in label for label in labels
        for kw in ["in-progress", "planned", "roadmap", "wip", "in progress"]
    )

    ignored_demand = (
        reactions >= 10 and
        age_days >= 180 and
        not has_planned_label
    )

    filtered.append({
        "number": issue["number"],
        "title": title,
        "url": issue.get("html_url", f"https://github.com/{target}/issues/{issue['number']}"),
        "reactions_plus1": reactions,
        "comments": comments,
        "demand_score": demand_score,
        "age_days": age_days,
        "labels": labels,
        "ignored_demand": ignored_demand,
        "body_snippet": (issue.get("body") or "")[:300]
    })

# Sort by demand score descending
filtered.sort(key=lambda x: x["demand_score"], reverse=True)

print(f"Raw issues: {len(raw)}")
print(f"Noise filtered: {noise_count} ({', '.join(f'{k}: {v}' for k, v in noise_reasons.items())})")
print(f"Issues for analysis: {len(filtered)}")

if len(filtered) < 10:
    print(f"ERROR: Only {len(filtered)} issues remain after filtering. This repo has too few engaged issues for reliable clustering.")
    print("Try a larger repo or a repo with more community engagement.")
    import sys; sys.exit(1)

# Ignored demand summary
ignored = [i for i in filtered if i["ignored_demand"]]
print(f"Ignored demand issues: {len(ignored)}")

json.dump(filtered, open("/tmp/ghd-filtered-issues.json", "w"), indent=2)
print("Pre-processing complete.")
PYEOF
```

**If fewer than 10 issues remain after filtering:** Stop. Tell the user exactly how many issues were found and filtered, and why the repo is too small for reliable demand clustering.

---

## Step 5: Cluster Issues

Print the filtered issues for analysis:

```bash
python3 << 'PYEOF'
import json
filtered = json.load(open("/tmp/ghd-filtered-issues.json"))
target = open("/tmp/ghd-target.txt").read().strip()

issue_list = filtered[:150]
print(f"Repo: {target}")
print(f"Issues to cluster: {len(issue_list)}")
print()
for i in issue_list:
    labels_str = f" [{', '.join(i['labels'][:3])}]" if i['labels'] else ""
    print(f"#{i['number']} [score:{round(i['demand_score'],1)} reactions:{i['reactions_plus1']}] {i['title']}{labels_str}")
PYEOF
```

Classify each issue printed above into one of these 6 categories:
`feature_gap`, `bug_pattern`, `ux_complaint`, `performance`, `integration_missing`, `docs_missing`

Rules:
- Classify each issue into exactly one category
- Extract a 1-sentence pain statement using the user's exact language from the title -- do not paraphrase
- Identify 5-8 cluster themes: short phrases (3-6 words) capturing dominant complaint patterns across all issues
- No em dashes. No marketing language.

Write your analysis to `/tmp/ghd-clusters.json` with this exact structure:

```json
{
  "classified_issues": [
    {"number": 123, "category": "feature_gap", "pain_statement": "Users need X which does not exist yet"}
  ],
  "cluster_themes": [
    {"theme_name": "Missing export options", "category": "feature_gap", "issue_numbers": [123, 456, 789]}
  ],
  "category_counts": {"feature_gap": 5, "bug_pattern": 3, "ux_complaint": 4, "performance": 2, "integration_missing": 6, "docs_missing": 1}
}
```

After writing the file, confirm with:

```bash
python3 -c "
import json
d = json.load(open('/tmp/ghd-clusters.json'))
print(f'Classified: {len(d[\"classified_issues\"])} issues, {len(d[\"cluster_themes\"])} themes')
print('Categories:', d['category_counts'])
"
```

---

## Step 6: Messaging Brief

Compute total demand score per cluster and print the top 3:

```bash
python3 << 'PYEOF'
import json

filtered = json.load(open("/tmp/ghd-filtered-issues.json"))
clusters = json.load(open("/tmp/ghd-clusters.json"))
target = open("/tmp/ghd-target.txt").read().strip()

demand_by_issue = {i["number"]: i["demand_score"] for i in filtered}
issue_titles = {i["number"]: i["title"] for i in filtered}
issue_reactions = {i["number"]: i["reactions_plus1"] for i in filtered}

enriched_themes = []
for theme in clusters.get("cluster_themes", []):
    issue_nums = theme.get("issue_numbers", [])
    total_demand = sum(demand_by_issue.get(n, 0) for n in issue_nums)
    top_issues = sorted(issue_nums, key=lambda n: demand_by_issue.get(n, 0), reverse=True)[:3]
    enriched_themes.append({
        "theme_name": theme["theme_name"],
        "category": theme["category"],
        "issue_count": len(issue_nums),
        "total_demand_score": round(total_demand, 1),
        "top_issues": [
            {"number": n, "title": issue_titles.get(n, ""), "reactions": issue_reactions.get(n, 0)}
            for n in top_issues
        ]
    })

enriched_themes.sort(key=lambda x: x["total_demand_score"], reverse=True)
json.dump(enriched_themes, open("/tmp/ghd-enriched-themes.json", "w"), indent=2)

print(f"Top 3 clusters for messaging brief (repo: {target}):")
for t in enriched_themes[:3]:
    print(f"\n  {t['theme_name']} ({t['category']}) -- total demand: {t['total_demand_score']}")
    for ti in t["top_issues"]:
        print(f"    #{ti['number']}: \"{ti['title']}\" ({ti['reactions']} reactions)")
PYEOF
```

Generate a GTM messaging brief from the top 3 clusters printed above.

Rules:
- Each positioning angle must cite the specific cluster it comes from
- Each outreach hook must quote a verbatim issue title in quotation marks
- Headlines must include a number or specific named pain -- no generic statements
- No em dashes. No forbidden words: powerful, robust, seamless, innovative, game-changing, streamline, leverage, transform

Write your brief to `/tmp/ghd-brief.json` with this exact structure:

```json
{
  "positioning_angles": [
    {
      "angle_name": "3-5 word label",
      "cluster_source": "theme_name from cluster",
      "positioning_statement": "2-3 sentences on what your product does that this competitor does not",
      "evidence": "verbatim issue title that best illustrates this gap"
    }
  ],
  "outreach_hooks": [
    {
      "hook_type": "pain quote hook",
      "hook_text": "2-3 sentences quoting a verbatim issue title in quotes",
      "best_for": "audience this hook works for"
    }
  ],
  "cluster_headlines": [
    {
      "theme_name": "from the cluster",
      "headline": "specific headline with a number or named pain",
      "sub_copy": "1 sentence expanding the headline"
    }
  ]
}
```

After writing the file, confirm with:

```bash
python3 -c "
import json
d = json.load(open('/tmp/ghd-brief.json'))
print('Positioning angles:', len(d.get('positioning_angles', [])))
print('Outreach hooks:', len(d.get('outreach_hooks', [])))
print('Cluster headlines:', len(d.get('cluster_headlines', [])))
"
```

---

## Step 7: Self-QA

Run before presenting. Verify evidence. Remove violations. Check output integrity.

```bash
python3 << 'PYEOF'
import json

filtered = json.load(open("/tmp/ghd-filtered-issues.json"))
clusters = json.load(open("/tmp/ghd-clusters.json"))
themes = json.load(open("/tmp/ghd-enriched-themes.json"))
brief = json.load(open("/tmp/ghd-brief.json"))
target = open("/tmp/ghd-target.txt").read().strip()

failures = []
real_titles = {i["number"]: i["title"] for i in filtered}

# Verify: classified_issues only reference real issue numbers
real_numbers = set(real_titles.keys())
hallucinated = [
    c["number"] for c in clusters.get("classified_issues", [])
    if c["number"] not in real_numbers
]
if hallucinated:
    failures.append(f"Removed {len(hallucinated)} hallucinated issue numbers from classified_issues: {hallucinated[:5]}")
    clusters["classified_issues"] = [
        c for c in clusters.get("classified_issues", [])
        if c["number"] in real_numbers
    ]

# Verify: top-10 list is sorted by demand_score descending
top10 = filtered[:10]
for i, issue in enumerate(top10):
    if i > 0 and issue["demand_score"] > top10[i-1]["demand_score"]:
        failures.append("Top-10 list was not sorted by demand_score -- re-sorted.")
        filtered.sort(key=lambda x: x["demand_score"], reverse=True)
        top10 = filtered[:10]
        break

# Verify: ignored demand issues meet all 3 criteria
ignored = [i for i in filtered if i["ignored_demand"]]
for issue in ignored:
    if issue["reactions_plus1"] < 10 or issue["age_days"] < 180:
        issue["ignored_demand"] = False
        failures.append(f"Removed issue #{issue['number']} from ignored demand -- did not meet all 3 criteria")

# Check messaging brief counts
if len(brief.get("positioning_angles", [])) != 3:
    failures.append(f"Expected 3 positioning angles, got {len(brief.get('positioning_angles', []))}")
if len(brief.get("outreach_hooks", [])) != 3:
    failures.append(f"Expected 3 outreach hooks, got {len(brief.get('outreach_hooks', []))}")
if len(brief.get("cluster_headlines", [])) != 3:
    failures.append(f"Expected 3 cluster headlines, got {len(brief.get('cluster_headlines', []))}")

# Check for em dashes in brief
brief_str = json.dumps(brief)
if "\u2014" in brief_str:
    brief_str = brief_str.replace("\u2014", " - ")
    brief = json.loads(brief_str)
    failures.append("Fixed: em dash characters removed from messaging brief")

# Check for forbidden words
forbidden = ["powerful", "robust", "seamless", "innovative", "game-changing", "streamline", "leverage", "transform"]
full_text = (json.dumps(clusters) + json.dumps(brief)).lower()
for word in forbidden:
    if word in full_text:
        failures.append(f"Warning: forbidden word '{word}' found in output -- review before presenting")

# Build final output bundle
output = {
    "repo": target,
    "issues_analyzed": len(filtered),
    "clusters": clusters,
    "enriched_themes": themes,
    "filtered_issues": filtered,
    "messaging_brief": brief,
    "data_quality_flags": failures
}

json.dump(output, open("/tmp/ghd-output.json", "w"), indent=2)
print(f"QA complete. Issues addressed: {len(failures)}")
for f in failures:
    print(f"  - {f}")
if not failures:
    print("All QA checks passed.")
PYEOF
```

---

## Step 8: Save and Present Output

```bash
python3 << 'PYEOF'
import json
from datetime import datetime, timezone

output = json.load(open("/tmp/ghd-output.json"))
target = output["repo"]
repo_slug = target.replace("/", "-")
date_str = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

filtered = output["filtered_issues"]
themes = output["enriched_themes"]
clusters = output["clusters"]
brief = output["messaging_brief"]
flags = output["data_quality_flags"]

ignored = [i for i in filtered if i.get("ignored_demand")]
top10 = filtered[:10]

# Build category summary from cluster data
category_counts = clusters.get("category_counts", {})

lines = [
    f"## Demand Gap Report: {target}",
    f"Issues analyzed: {output['issues_analyzed']} | Date: {date_str}",
    "",
    "---",
    "",
    "### Demand Gap Leaderboard",
    "",
    "| Rank | Theme | Category | Issues | Total Demand Score | Top Issue Reactions |",
    "|---|---|---|---|---|---|",
]

for i, theme in enumerate(themes[:8], 1):
    top_reactions = theme["top_issues"][0]["reactions"] if theme["top_issues"] else 0
    lines.append(
        f"| {i} | {theme['theme_name']} | {theme['category']} | "
        f"{theme['issue_count']} | {theme['total_demand_score']} | {top_reactions} |"
    )

lines += ["", "---", ""]

if ignored:
    lines += [
        "### Ignored Demand (High Reactions, No Maintainer Response)",
        "",
        "These issues have 10+ reactions, are 6+ months old, and have no planned/in-progress label.",
        "This is your opportunity window.",
        "",
    ]
    for issue in ignored[:10]:
        lines.append(
            f"- [{issue['title']}]({issue['url']}) -- "
            f"{issue['reactions_plus1']} reactions, {issue['age_days']} days old"
        )
    lines += ["", "---", ""]

lines += [
    "### Top 10 Highest-Demand Issues",
    "",
    "| Rank | Issue | Reactions | Comments | Demand Score | Link |",
    "|---|---|---|---|---|---|",
]
for i, issue in enumerate(top10, 1):
    short_title = issue["title"][:70] + ("..." if len(issue["title"]) > 70 else "")
    lines.append(
        f"| {i} | {short_title} | {issue['reactions_plus1']} | "
        f"{issue['comments']} | {round(issue['demand_score'], 1)} | "
        f"[#{issue['number']}]({issue['url']}) |"
    )

lines += ["", "---", "", "### Cluster Deep Dives", ""]

for theme in themes[:3]:
    lines.append(f"#### {theme['theme_name']}")
    lines.append(f"Category: {theme['category']} | Issues: {theme['issue_count']} | Total demand score: {theme['total_demand_score']}")
    lines.append("")
    lines.append("Top issues in this cluster:")
    for ti in theme["top_issues"]:
        lines.append(f"- \"{ti['title']}\" -- {ti['reactions']} reactions")
    lines.append("")

lines += ["---", "", "### Messaging Brief", ""]

for angle in brief.get("positioning_angles", []):
    lines.append(f"**{angle.get('angle_name', 'Angle')}**")
    lines.append(angle.get("positioning_statement", ""))
    lines.append(f"Evidence: \"{angle.get('evidence', '')}\"")
    lines.append("")

lines += ["---", "", "### GTM Angles", ""]

for hook in brief.get("outreach_hooks", []):
    lines.append(f"**{hook.get('hook_type', 'Hook')}**")
    lines.append(hook.get("hook_text", ""))
    lines.append(f"Best for: {hook.get('best_for', '')}")
    lines.append("")

lines += ["---", ""]
if flags:
    lines.append(f"Data quality notes: {'; '.join(flags)}")
else:
    lines.append("Data quality notes: None")

output_path = f"docs/demand-signals/{repo_slug}-{date_str}.md"
import os
os.makedirs("docs/demand-signals", exist_ok=True)
open(output_path, "w").write("\n".join(lines))
print(f"Saved to: {output_path}")

# Print to console
print("\n" + "\n".join(lines))
PYEOF
```

Clean up temp files:

```bash
rm -f /tmp/ghd-target.txt /tmp/ghd-raw-issues.json /tmp/ghd-filtered-issues.json \
      /tmp/ghd-cluster-request.json /tmp/ghd-clusters.json /tmp/ghd-enriched-themes.json \
      /tmp/ghd-brief-request.json /tmp/ghd-brief.json /tmp/ghd-output.json
```
