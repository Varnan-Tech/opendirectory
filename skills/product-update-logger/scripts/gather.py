#!/usr/bin/env python3
"""
product-update-logger gather script
Collects shipped items from git commits, GitHub PRs, and free text.
No required API keys. GITHUB_TOKEN optional (enables GitHub PR fetching).

Usage:
    python3 scripts/gather.py --since 7 --output /tmp/pul-raw.json
    python3 scripts/gather.py --items "Add dark mode|Fix CSV bug" --output /tmp/pul-raw.json
    GITHUB_TOKEN=your_token python3 scripts/gather.py --repo owner/repo --since 14
    python3 scripts/gather.py --stdout | jq '.items'
"""

import argparse
import json
import os
import re
import ssl
import subprocess
import sys
from datetime import datetime, timedelta, timezone

_ssl_ctx = ssl._create_unverified_context()

TODAY = datetime.now(timezone.utc)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

quiet = False


# ---------------------------------------------------------------------------
# HTTP helpers (reused from map-your-market pattern)
# ---------------------------------------------------------------------------

def fetch_json(url, headers=None, timeout=20):
    import urllib.request, urllib.error
    req = urllib.request.Request(url, headers=headers or {})
    req.add_header("User-Agent", "product-update-logger/1.0")
    try:
        with urllib.request.urlopen(req, context=_ssl_ctx, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if not quiet:
            print(f"  HTTP {e.code}: {url[:80]}", file=sys.stderr)
        return None
    except Exception as e:
        if not quiet:
            print(f"  Error: {e} -- {url[:80]}", file=sys.stderr)
        return None


def gh_get(path):
    import urllib.request
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return fetch_json(f"https://api.github.com{path}", headers=headers)


# ---------------------------------------------------------------------------
# Noise filter patterns
# ---------------------------------------------------------------------------

NOISE_PATTERNS = [
    re.compile(r"^Merge (pull request|branch)\b", re.IGNORECASE),
    re.compile(r"^(bump|update) version\b", re.IGNORECASE),
    re.compile(r"^chore[\s:(]", re.IGNORECASE),
    re.compile(r"^ci[\s:(]", re.IGNORECASE),
    re.compile(r"^build[\s:(]", re.IGNORECASE),
    re.compile(r"^fix typo\b", re.IGNORECASE),
    re.compile(r"^\s*typo\b", re.IGNORECASE),
    re.compile(r"^wip\b", re.IGNORECASE),
    re.compile(r"^test[\s:(]", re.IGNORECASE),
    re.compile(r"^docs[\s:(]", re.IGNORECASE),
    re.compile(r"^style[\s:(]", re.IGNORECASE),
    re.compile(r"^revert\b", re.IGNORECASE),
    re.compile(r"^Initial commit$", re.IGNORECASE),
    re.compile(r"^init$", re.IGNORECASE),
]

NOISE_PR_LABELS = {"documentation", "chore", "dependencies", "ci", "test", "tests"}


def filter_noise(commits: list) -> list:
    filtered = []
    for c in commits:
        subject = c.get("subject", "").strip()
        if not subject:
            continue
        # Skip single-word subjects under 8 chars
        if len(subject.split()) == 1 and len(subject) < 8:
            continue
        skip = False
        for pat in NOISE_PATTERNS:
            if pat.match(subject):
                skip = True
                break
        if not skip:
            filtered.append(c)
    return filtered


# ---------------------------------------------------------------------------
# Git commits
# ---------------------------------------------------------------------------

def get_git_commits(since_days: int, repo_path: str = ".") -> list:
    try:
        result = subprocess.run(
            [
                "git", "-C", repo_path, "log",
                f"--since={since_days} days ago",
                "--pretty=format:%H|%s|%b|%ad",
                "--date=short",
            ],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return []
        commits = []
        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            parts = line.split("|", 3)
            commit_hash = parts[0].strip() if len(parts) > 0 else ""
            subject = parts[1].strip() if len(parts) > 1 else ""
            body = parts[2].strip() if len(parts) > 2 else ""
            date = parts[3].strip() if len(parts) > 3 else ""
            if subject:
                commits.append({
                    "subject": subject,
                    "body": body,
                    "source": "git_commit",
                    "hash": commit_hash[:7],
                    "date": date,
                })
        return commits
    except FileNotFoundError:
        if not quiet:
            print("  git not installed -- skipping git commits", file=sys.stderr)
        return []
    except Exception as e:
        if not quiet:
            print(f"  git error: {e}", file=sys.stderr)
        return []


# ---------------------------------------------------------------------------
# GitHub PRs
# ---------------------------------------------------------------------------

def get_github_prs(repo: str, since_date: str) -> list:
    if not GITHUB_TOKEN:
        if not quiet:
            print("  GITHUB_TOKEN not set -- skipping GitHub PRs", file=sys.stderr)
        return []
    if not repo:
        return []

    data = gh_get(f"/repos/{repo}/pulls?state=closed&sort=updated&direction=desc&per_page=50")
    if not data:
        return []

    prs = []
    for pr in data:
        merged_at = pr.get("merged_at")
        if not merged_at:
            continue
        # Filter by since_date
        merged_date = merged_at[:10]
        if merged_date < since_date:
            continue
        labels = [lbl["name"].lower() for lbl in (pr.get("labels") or [])]
        # Skip PRs with noise labels
        if any(lbl in NOISE_PR_LABELS for lbl in labels):
            continue
        prs.append({
            "subject": pr.get("title", "").strip(),
            "body": (pr.get("body") or "").strip()[:500],
            "source": "github_pr",
            "pr_number": pr.get("number"),
            "merged_at": merged_at[:10],
            "labels": labels,
        })
    return prs


# ---------------------------------------------------------------------------
# Free text input
# ---------------------------------------------------------------------------

def parse_free_text(items_str: str) -> list:
    if not items_str or not items_str.strip():
        return []
    items = []
    for item in re.split(r"[|\n]", items_str):
        item = item.strip()
        if item:
            items.append({"subject": item, "source": "free_text"})
    return items


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def deduplicate(commits: list, prs: list) -> list:
    result = list(prs)
    pr_titles = [pr["subject"].lower() for pr in prs]

    for commit in commits:
        subject = commit["subject"].lower()
        is_dup = False
        for pr_title in pr_titles:
            # If commit subject is substring of PR title or vice versa -> same item
            if subject in pr_title or pr_title in subject:
                is_dup = True
                break
        if not is_dup:
            result.append(commit)

    return result


# ---------------------------------------------------------------------------
# Existing changelog detection
# ---------------------------------------------------------------------------

def detect_existing_changelog(path: str = "docs/changelog.md") -> dict:
    if not os.path.exists(path):
        return {"exists": False, "last_label": "", "format": "date-based"}

    try:
        with open(path) as f:
            lines = [f.readline() for _ in range(100)]
        lines = [l.rstrip() for l in lines if l.strip()]
    except Exception:
        return {"exists": True, "last_label": "", "format": "date-based"}

    last_label = ""
    version_format = "date-based"

    for line in lines:
        # Look for ## headings (changelog entry labels)
        m = re.match(r"^## (.+)$", line)
        if m:
            last_label = m.group(1).strip()
            # Detect semver format
            if re.match(r"^v?\d+\.\d+\.\d+", last_label):
                version_format = "semver"
            break

    return {"exists": True, "last_label": last_label, "format": version_format}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    global quiet

    parser = argparse.ArgumentParser(description="Gather shipped items for product-update-logger")
    parser.add_argument("--since", default="7",
                        help="Days back to look, or YYYY-MM-DD date (default: 7)")
    parser.add_argument("--repo", default="",
                        help="GitHub repo as owner/repo for PR fetching")
    parser.add_argument("--items", default="",
                        help="Pipe-separated free text items")
    parser.add_argument("--output", default="/tmp/pul-raw.json",
                        help="Output file path (default: /tmp/pul-raw.json)")
    parser.add_argument("--stdout", action="store_true",
                        help="Print JSON to stdout instead of file")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress progress output")
    args = parser.parse_args()

    quiet = args.quiet
    use_stdout = args.stdout

    def log(msg):
        if not quiet:
            print(msg, file=sys.stderr if use_stdout else sys.stdout)

    # Resolve since_days and since_date
    since_str = args.since.strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}$", since_str):
        since_date = since_str
        delta = TODAY.date() - datetime.strptime(since_str, "%Y-%m-%d").date()
        since_days = max(delta.days, 1)
    else:
        since_days = int(since_str)
        since_date = (TODAY - timedelta(days=since_days)).strftime("%Y-%m-%d")

    today_str = TODAY.strftime("%Y-%m-%d")

    log(f"Gathering items since {since_date} ({since_days} days)...")

    # 1. Free text items
    free_text_items = parse_free_text(args.items)
    if free_text_items:
        log(f"  Free text: {len(free_text_items)} items")

    # 2. Git commits
    git_available = False
    raw_commits = []
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, timeout=5
        )
        git_available = result.returncode == 0
    except Exception:
        git_available = False

    noise_filtered = 0
    if git_available:
        raw_commits = get_git_commits(since_days)
        before = len(raw_commits)
        raw_commits = filter_noise(raw_commits)
        noise_filtered = before - len(raw_commits)
        log(f"  Git: {len(raw_commits)} commits ({noise_filtered} noise filtered)")

    # 3. GitHub PRs
    github_available = bool(GITHUB_TOKEN and args.repo)
    prs = []
    if github_available:
        prs = get_github_prs(args.repo, since_date)
        log(f"  GitHub PRs: {len(prs)} merged PRs")

    # 4. Deduplicate commits + PRs
    combined = deduplicate(raw_commits, prs)

    # 5. Merge with free text (free text first, then git/PR items)
    all_items = free_text_items + combined
    free_text_provided = bool(free_text_items)

    # 6. Detect existing changelog
    existing_changelog = detect_existing_changelog()

    output = {
        "date": today_str,
        "since_date": since_date,
        "since_days": since_days,
        "git_available": git_available,
        "github_available": github_available,
        "free_text_provided": free_text_provided,
        "items": all_items,
        "total_items": len(all_items),
        "noise_filtered": noise_filtered,
        "existing_changelog": existing_changelog,
    }

    if use_stdout:
        print(json.dumps(output, indent=2))
    else:
        with open(args.output, "w") as f:
            json.dump(output, f, indent=2)
        log(f"\nOutput: {args.output}")
        log(f"Total items: {len(all_items)}")


if __name__ == "__main__":
    main()
