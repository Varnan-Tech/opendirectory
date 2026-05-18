#!/usr/bin/env python3
"""
fetch_discussions.py
--------------------
Fetches GitHub Discussions from a public repository via the GitHub GraphQL API
and writes normalized JSON to stdout or a file for the agent to analyze.

Usage:
    python fetch_discussions.py --repo owner/repo [options]

Options:
    --repo          owner/repo or full GitHub URL (required)
    --days-back     How many days of history to inspect (default: 90)
    --min-comments  Minimum comment count to include a discussion (default: 3)
    --max-items     Maximum discussions to fetch (default: 100)
    --category      Filter by discussion category name (optional)
    --mode          Output mode: docs | content | combined (default: combined)
    --output        Output file path (default: discussions_raw.json)

Environment:
    GITHUB_TOKEN    GitHub Personal Access Token with read:discussion scope
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse


GRAPHQL_URL = "https://api.github.com/graphql"

DISCUSSIONS_QUERY = """
query FetchDiscussions($owner: String!, $name: String!, $first: Int!, $after: String) {
  repository(owner: $owner, name: $name) {
    discussions(first: $first, after: $after, orderBy: {field: UPDATED_AT, direction: DESC}) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        number
        title
        body
        url
        createdAt
        updatedAt
        isAnswered
        upvoteCount
        commentsCount: comments {
          totalCount
        }
        reactions {
          totalCount
        }
        category {
          name
        }
        author {
          login
        }
        topComments: comments(first: 5) {
          nodes {
            body
            author {
              login
            }
          }
        }
      }
    }
  }
}
"""


def get_token():
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        print(
            "ERROR: GITHUB_TOKEN environment variable is not set.\n"
            "Set it in your .env file or export it in your shell.\n"
            "Generate a token at: https://github.com/settings/tokens\n"
            "Required scope: read:discussion (public repos only)",
            file=sys.stderr,
        )
        sys.exit(1)
    return token


def parse_repo(repo_arg):
    """Accept owner/repo or full GitHub URL."""
    if repo_arg.startswith("https://"):
        path = urlparse(repo_arg).path.strip("/")
        parts = path.split("/")
        if len(parts) < 2:
            print(f"ERROR: Cannot parse owner/repo from URL: {repo_arg}", file=sys.stderr)
            sys.exit(1)
        return parts[0], parts[1]
    parts = repo_arg.split("/")
    if len(parts) != 2 or not all(parts):
        print(
            f"ERROR: --repo must be in 'owner/repo' format. Got: {repo_arg}",
            file=sys.stderr,
        )
        sys.exit(1)
    return parts[0], parts[1]


def graphql_request(token, query, variables):
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = Request(
        GRAPHQL_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github+json",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
    except HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        if e.code == 401:
            print(
                "ERROR: GitHub API returned 401 Unauthorized.\n"
                "Your GITHUB_TOKEN is invalid or expired.\n"
                f"Details: {error_body}",
                file=sys.stderr,
            )
            sys.exit(1)
        if e.code == 403:
            print(
                "ERROR: GitHub API returned 403 Forbidden.\n"
                "Your token may lack read:discussion scope, or you have hit rate limits.\n"
                f"Details: {error_body}",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"ERROR: GitHub API returned HTTP {e.code}.\nDetails: {error_body}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"ERROR: Network error reaching GitHub API: {e.reason}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(body)
    if "errors" in data:
        messages = "; ".join(err.get("message", str(err)) for err in data["errors"])
        print(f"ERROR: GitHub GraphQL returned errors: {messages}", file=sys.stderr)
        sys.exit(1)
    return data


def fetch_all_discussions(token, owner, name, max_items):
    discussions = []
    after = None
    batch = min(max_items, 100)

    while len(discussions) < max_items:
        variables = {
            "owner": owner,
            "name": name,
            "first": min(batch, max_items - len(discussions)),
            "after": after,
        }
        data = graphql_request(token, DISCUSSIONS_QUERY, variables)
        repo_data = data.get("data", {}).get("repository")
        if repo_data is None:
            print(
                f"ERROR: Repository '{owner}/{name}' not found or is not accessible.\n"
                "Ensure the repo is public and your token has read:discussion scope.",
                file=sys.stderr,
            )
            sys.exit(1)

        page = repo_data["discussions"]
        discussions.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]

    return discussions


def normalize(discussion, cutoff_date, min_comments, category_filter):
    """Apply filters and flatten to a clean dict. Returns None if filtered out."""
    # Date filter
    updated = datetime.fromisoformat(discussion["updatedAt"].replace("Z", "+00:00"))
    if updated < cutoff_date:
        return None

    # Comment count filter
    comment_count = discussion["commentsCount"]["totalCount"]
    if comment_count < min_comments:
        return None

    # Category filter
    category_name = discussion.get("category", {}).get("name", "")
    if category_filter and category_name.lower() != category_filter.lower():
        return None

    # Extract top comment snippets for agent context
    top_comments = [
        {
            "author": c.get("author", {}).get("login", "unknown"),
            "body": c.get("body", "")[:500],  # Truncate to keep payload lean
        }
        for c in discussion.get("topComments", {}).get("nodes", [])
    ]

    return {
        "number": discussion["number"],
        "title": discussion["title"],
        "body": discussion.get("body", "")[:1000],  # Truncate body
        "url": discussion["url"],
        "created_at": discussion["createdAt"],
        "updated_at": discussion["updatedAt"],
        "is_answered": discussion.get("isAnswered", False),
        "comment_count": comment_count,
        "reaction_count": discussion.get("reactions", {}).get("totalCount", 0),
        "upvote_count": discussion.get("upvoteCount", 0),
        "category": category_name,
        "author": discussion.get("author", {}).get("login", "unknown"),
        "top_comments": top_comments,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Fetch GitHub Discussions for DevRel content analysis."
    )
    parser.add_argument("--repo", required=True, help="owner/repo or full GitHub URL")
    parser.add_argument("--days-back", type=int, default=90, help="Days of history (default: 90)")
    parser.add_argument("--min-comments", type=int, default=3, help="Min comments to include (default: 3)")
    parser.add_argument("--max-items", type=int, default=100, help="Max discussions to fetch (default: 100)")
    parser.add_argument("--category", default=None, help="Filter by category name (optional)")
    parser.add_argument("--mode", choices=["docs", "content", "combined"], default="combined")
    parser.add_argument("--output", default="discussions_raw.json", help="Output file path")
    args = parser.parse_args()

    token = get_token()
    owner, name = parse_repo(args.repo)
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=args.days_back)

    print(f"Fetching discussions from {owner}/{name} ...", file=sys.stderr)
    raw = fetch_all_discussions(token, owner, name, args.max_items)
    print(f"  Fetched {len(raw)} discussions total.", file=sys.stderr)

    normalized = []
    for d in raw:
        result = normalize(d, cutoff_date, args.min_comments, args.category)
        if result:
            normalized.append(result)

    print(f"  {len(normalized)} discussions passed filters.", file=sys.stderr)

    output = {
        "meta": {
            "repo": f"{owner}/{name}",
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "days_back": args.days_back,
            "min_comments": args.min_comments,
            "max_items": args.max_items,
            "category_filter": args.category,
            "mode": args.mode,
            "total_fetched": len(raw),
            "total_qualifying": len(normalized),
        },
        "low_signal": len(normalized) < 5,
        "discussions": normalized,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"  Written to {args.output}", file=sys.stderr)

    if output["low_signal"]:
        print(
            f"\nLOW_SIGNAL_WARNING: Only {len(normalized)} discussions passed filters "
            f"(threshold: 5). The agent will note this in its output and will not "
            f"fabricate patterns from insufficient data.",
            file=sys.stderr,
        )

    # Also print summary to stdout for agent pickup
    print(json.dumps({"status": "ok", "meta": output["meta"], "low_signal": output["low_signal"]}))


if __name__ == "__main__":
    # Load .env if present
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, val = line.partition("=")
                    val = val.strip()
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    os.environ.setdefault(key.strip(), val)
    main()
