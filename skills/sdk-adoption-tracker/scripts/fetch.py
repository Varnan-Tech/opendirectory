#!/usr/bin/env python3
"""
sdk-adoption-tracker: fetch.py

Searches GitHub code for public repos that import a given SDK, scores each
repo by adoption signal strength, and enriches high-signal repos with owner
and contributor data.

Usage:
    python3 scripts/fetch.py stripe
    python3 scripts/fetch.py @clerk/nextjs --ecosystem npm
    python3 scripts/fetch.py requests --ecosystem python --output results.json
    python3 scripts/fetch.py stripe --exclude stripe --context "We build billing tooling"

Output: JSON written to --output file (default: sdk-adopters-YYYY-MM-DD.json)
        or printed to stdout with --stdout

Environment:
    GITHUB_TOKEN   required -- code search is rate-limited to 3 req/min without it
"""

import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

_ssl_ctx = ssl._create_unverified_context()

TUTORIAL_WORDS = {
    "example", "tutorial", "demo", "learn", "sample", "starter",
    "boilerplate", "template", "playground", "test", "course", "workshop"
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def gh_get(path: str, headers: dict, timeout: int = 15):
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ssl_ctx) as resp:
            remaining = resp.headers.get("X-RateLimit-Remaining")
            data = json.loads(resp.read())
            return data, int(remaining) if remaining else 999
    except urllib.error.HTTPError as e:
        return None, 999
    except Exception:
        return None, 999


def detect_ecosystem(sdk_name: str) -> str:
    if sdk_name.startswith("@") or "-" in sdk_name:
        return "npm"
    if re.match(r'^[a-z][a-z0-9_]*$', sdk_name):
        return "python"
    if "github.com/" in sdk_name:
        return "go"
    return "generic"


def build_queries(sdk_name: str, ecosystem: str) -> list[str]:
    if ecosystem == "npm":
        return [
            f'require("{sdk_name}")',
            f"require('{sdk_name}')",
            f'from "{sdk_name}"',
            f"from '{sdk_name}'",
        ]
    elif ecosystem == "python":
        return [
            f"import {sdk_name}",
            f"from {sdk_name} import",
        ]
    elif ecosystem == "go":
        return [f'"{sdk_name}"']
    else:
        return [sdk_name]


def is_tutorial(repo_name: str, description: str) -> bool:
    name_words = set(repo_name.lower().replace("-", " ").replace("_", " ").split())
    desc_words = set((description or "").lower().split())
    return bool((name_words | desc_words) & TUTORIAL_WORDS)


def compute_score(owner_type: str, company: str, stars: int, days_since_push: int,
                  is_fork: bool, is_archived: bool, tutorial: bool) -> float:
    score = 0.0
    if owner_type == "Organization":   score += 50
    if company and company.strip():    score += 20
    score += min(stars, 500) / 10
    if days_since_push < 30:           score += 30
    if days_since_push < 7:            score += 20
    if not is_fork:                    score += 10
    if not is_archived:                score += 10
    if not tutorial:                   score += 20
    return round(score, 1)


# ---------------------------------------------------------------------------
# Step 1: Search GitHub code
# ---------------------------------------------------------------------------

def search_code(sdk_name: str, ecosystem: str, exclude_owner: str,
                headers: dict, verbose: bool) -> list[dict]:
    queries = build_queries(sdk_name, ecosystem)
    seen = {}
    sdk_bare = sdk_name.lower().split("/")[-1].replace("@", "")
    search_remaining = 30

    if verbose:
        print(f"Searching GitHub code for {sdk_name} ({ecosystem})...")

    for i, query in enumerate(queries):
        if search_remaining <= 2:
            if verbose:
                print(f"  Search rate limit low ({search_remaining}) -- stopping early")
            break

        encoded = urllib.parse.quote(query)
        url = f"https://api.github.com/search/code?q={encoded}&per_page=100"
        req = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=20, context=_ssl_ctx) as resp:
                remaining = resp.headers.get("X-RateLimit-Remaining")
                if remaining:
                    search_remaining = int(remaining)
                raw = json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 403:
                if verbose:
                    print(f"  Rate limit hit on '{query}'")
                break
            if verbose:
                print(f"  HTTP {e.code} on '{query}'")
            if i < len(queries) - 1:
                time.sleep(6)
            continue
        except Exception as e:
            if verbose:
                print(f"  Error on '{query}': {e}")
            if i < len(queries) - 1:
                time.sleep(6)
            continue

        items = raw.get("items", [])
        total = raw.get("total_count", 0)
        if verbose:
            print(f"  '{query}': {total} total, {len(items)} fetched | rate={search_remaining}")

        for item in items:
            repo = item.get("repository", {})
            full_name = repo.get("full_name", "")
            owner_login = repo.get("owner", {}).get("login", "").lower()

            if not full_name:
                continue
            if full_name in seen:
                continue
            if exclude_owner and owner_login == exclude_owner.lower():
                continue

            seen[full_name] = {
                "full_name": full_name,
                "name": repo.get("name", ""),
                "owner_login": repo.get("owner", {}).get("login", ""),
                "owner_type": repo.get("owner", {}).get("type", "User"),
                "file_path": item.get("path", ""),
                "matched_pattern": query,
                "html_url": repo.get("html_url", ""),
                "description": repo.get("description") or "",
            }

        if i < len(queries) - 1:
            time.sleep(6)  # respect 10 req/min code search limit

    results = list(seen.values())
    if verbose:
        print(f"  Total unique repos: {len(results)}")
    return results


# ---------------------------------------------------------------------------
# Step 2: Score repos (pure Python)
# ---------------------------------------------------------------------------

def score_repos(raw_results: list[dict], sdk_name: str, exclude_owner: str) -> list[dict]:
    sdk_bare = sdk_name.lower().split("/")[-1].replace("@", "")
    scored = []

    for repo in raw_results:
        owner_login = repo.get("owner_login", "").lower()
        repo_name = repo.get("name", "").lower()
        description = repo.get("description") or ""

        if exclude_owner and owner_login == exclude_owner.lower():
            continue

        tutorial = is_tutorial(repo_name, description)
        if repo_name == sdk_bare or repo_name.startswith(sdk_bare + "-"):
            tutorial = True

        owner_type = repo.get("owner_type", "User")
        tier = "tutorial_noise" if tutorial else (
            "company_org" if owner_type == "Organization" else "solo_dev"
        )

        scored.append({
            **repo,
            "tier": tier,
            "is_tutorial": tutorial,
            "adoption_score": 0.0,
            "enriched": False,
        })

    tier_order = {"company_org": 0, "affiliated_dev": 1, "solo_dev": 2, "tutorial_noise": 3}
    scored.sort(key=lambda x: tier_order.get(x["tier"], 9))
    return scored


# ---------------------------------------------------------------------------
# Step 3: Enrich high-signal repos
# ---------------------------------------------------------------------------

def enrich_repos(scored: list[dict], headers: dict, verbose: bool) -> list[dict]:
    target = [r for r in scored if r["tier"] != "tutorial_noise"]
    if verbose:
        print(f"\nEnriching {len(target)} repos (skipping tutorial_noise)...")

    core_remaining = 5000
    enriched = []
    now = datetime.now(tz=timezone.utc)

    for item in target:
        full_name = item["full_name"]
        owner_login = item["owner_login"]
        owner_type = item["owner_type"]

        if core_remaining <= 10:
            enriched.append({**item, "enriched": False})
            continue

        repo_data, core_remaining = gh_get(f"/repos/{full_name}", headers)
        if not repo_data:
            continue

        stars = repo_data.get("stargazers_count", 0)
        is_fork = repo_data.get("fork", False)
        is_archived = repo_data.get("archived", False)
        language = repo_data.get("language") or ""
        description = repo_data.get("description") or item.get("description", "")
        pushed_at = repo_data.get("pushed_at") or ""
        created_at = repo_data.get("created_at") or ""

        days_since_push = 999
        if pushed_at:
            pushed_dt = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
            days_since_push = (now - pushed_dt).days

        days_since_created = 999
        if created_at:
            created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            days_since_created = (now - created_dt).days

        company = ""
        owner_profile = {}
        org_website = ""

        if owner_type == "Organization":
            org_data, core_remaining = gh_get(f"/orgs/{owner_login}", headers)
            if org_data:
                company = org_data.get("name") or owner_login
                org_website = org_data.get("blog") or ""
                owner_profile = {
                    "type": "org", "name": company,
                    "description": org_data.get("description") or "",
                    "website": org_website, "email": org_data.get("email") or "",
                    "public_repos": org_data.get("public_repos", 0),
                    "followers": org_data.get("followers", 0),
                }
        else:
            user_data, core_remaining = gh_get(f"/users/{owner_login}", headers)
            if user_data:
                company = user_data.get("company") or ""
                owner_profile = {
                    "type": "user", "name": user_data.get("name") or owner_login,
                    "company": company, "bio": user_data.get("bio") or "",
                    "blog": user_data.get("blog") or "",
                    "followers": user_data.get("followers", 0),
                    "twitter_username": user_data.get("twitter_username") or "not listed",
                }
                if company and item["tier"] == "solo_dev":
                    item["tier"] = "affiliated_dev"

        top_contributors = []
        if core_remaining > 20:
            contrib_data, core_remaining = gh_get(
                f"/repos/{full_name}/contributors?per_page=3", headers
            )
            if contrib_data:
                top_contributors = [
                    {"login": c.get("login", ""), "contributions": c.get("contributions", 0)}
                    for c in contrib_data[:3]
                ]

        score = compute_score(
            owner_type, company, stars, days_since_push,
            is_fork, is_archived, item.get("is_tutorial", False)
        )

        tier = item["tier"]
        if is_archived:
            tier = "tutorial_noise" if item.get("is_tutorial") else tier

        enriched.append({
            **item,
            "description": description,
            "stars": stars,
            "language": language,
            "is_fork": is_fork,
            "is_archived": is_archived,
            "days_since_push": days_since_push,
            "days_since_created": days_since_created,
            "pushed_at": pushed_at,
            "created_at": created_at,
            "repo_url": repo_data.get("html_url", f"https://github.com/{full_name}"),
            "tier": tier,
            "adoption_score": score,
            "company": company or "not listed",
            "org_website": org_website,
            "owner_profile": owner_profile,
            "top_contributors": top_contributors,
            "enriched": True,
        })

        if verbose:
            print(f"  {full_name} | {tier} | score={score} | stars={stars} | "
                  f"pushed={days_since_push}d | company={company or 'not listed'} | "
                  f"rate={core_remaining}")
        time.sleep(0.1)

    enriched.sort(key=lambda x: -x["adoption_score"])
    return enriched


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Search GitHub for repos that import a given SDK and score adoption."
    )
    parser.add_argument("sdk", help="SDK name (e.g. stripe, @clerk/nextjs, requests)")
    parser.add_argument("--ecosystem", "-e", default="",
                        help="Ecosystem: npm, python, go, generic (auto-detected if omitted)")
    parser.add_argument("--exclude", "-x", default="",
                        help="Owner login to exclude (usually the SDK publisher)")
    parser.add_argument("--context", "-c", default="",
                        help="Short product description for outreach message context")
    parser.add_argument("--output", "-o", default="",
                        help="Output JSON file path (default: sdk-adopters-YYYY-MM-DD.json)")
    parser.add_argument("--stdout", action="store_true", help="Print JSON to stdout")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress output")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("ERROR: GITHUB_TOKEN is required for code search.", file=sys.stderr)
        print("Add a token at github.com/settings/tokens (no scopes needed).", file=sys.stderr)
        sys.exit(1)

    verbose = not args.quiet
    ecosystem = args.ecosystem or detect_ecosystem(args.sdk)

    if verbose:
        print(f"SDK: {args.sdk} | Ecosystem: {ecosystem}")
        if not args.exclude:
            print("Tip: use --exclude <owner> to filter out the SDK publisher's own repos.")

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "sdk-adoption-tracker/1.0",
    }

    raw_results = search_code(args.sdk, ecosystem, args.exclude, headers, verbose)

    if not raw_results:
        print("No repos found. GitHub code search indexing takes 1-4 weeks for new packages.")
        sys.exit(0)

    scored = score_repos(raw_results, args.sdk, args.exclude)
    enriched = enrich_repos(scored, headers, verbose)

    high = [r for r in enriched if r["adoption_score"] >= 80]
    medium = [r for r in enriched if 40 <= r["adoption_score"] < 80]
    tier_counts = {}
    for r in enriched:
        tier_counts[r["tier"]] = tier_counts.get(r["tier"], 0) + 1

    date_str = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

    output_data = {
        "date": date_str,
        "sdk_name": args.sdk,
        "ecosystem": ecosystem,
        "product_context": args.context,
        "repos_found": len(enriched),
        "company_repos": tier_counts.get("company_org", 0),
        "tier_counts": tier_counts,
        "raw_results": raw_results,
        "scored": scored,
        "enriched": enriched,
        "summary": {
            "high_signal": [
                {"repo": r["full_name"], "score": r["adoption_score"],
                 "company": r.get("company", ""), "tier": r["tier"]}
                for r in high
            ],
            "medium_signal": [
                {"repo": r["full_name"], "score": r["adoption_score"], "tier": r["tier"]}
                for r in medium
            ],
        }
    }

    if args.stdout:
        print(json.dumps(output_data, indent=2))
        return

    output_path = args.output or f"sdk-adopters-{date_str}.json"
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)

    if verbose:
        print(f"\n{'='*50}")
        print(f"Results: {len(enriched)} repos analyzed")
        print(f"  Company org repos: {tier_counts.get('company_org', 0)}")
        print(f"  Affiliated devs:   {tier_counts.get('affiliated_dev', 0)}")
        print(f"  Solo devs:         {tier_counts.get('solo_dev', 0)}")
        print(f"  Tutorial noise:    {tier_counts.get('tutorial_noise', 0)}")
        print(f"\nTop Adopters (by score):")
        for i, r in enumerate((high + medium)[:10], 1):
            print(f"  {i:2}. {r['full_name']:40} score={r['adoption_score']:5.1f}  "
                  f"stars={r.get('stars',0):>5}  {r['tier']}")
        print(f"\nSaved to: {output_path}")
        print(f"\nNext step: open {output_path} with Claude and ask it to generate adoption briefs.")


if __name__ == "__main__":
    main()
