#!/usr/bin/env python3
"""
npm-downloads-to-leads: fetch.py

Fetches 12 weeks of npm download data, computes velocity scores, and enriches
maintainer profiles via the npm registry and GitHub API.

Usage:
    python3 scripts/fetch.py esbuild zod @hono/hono
    python3 scripts/fetch.py --file packages.txt
    python3 scripts/fetch.py esbuild zod --output results.json
    python3 scripts/fetch.py esbuild zod --context "We build a TypeScript DX platform"

Output: JSON written to --output file (default: npm-leads-YYYY-MM-DD.json)
        or printed to stdout with --stdout

Environment:
    GITHUB_TOKEN   optional -- raises GitHub rate limit from 60/hr to 5000/hr
"""

import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone

# Some environments (e.g. macOS without updated certs) fail SSL verification.
# Fall back to unverified context so the script still runs.
_ssl_ctx = ssl._create_unverified_context()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def encode_package(pkg: str) -> str:
    """URL-encode scoped packages: @org/pkg -> %40org%2Fpkg"""
    return pkg.replace("@", "%40").replace("/", "%2F")


def fetch_json(url: str, headers: dict, timeout: int = 20) -> dict | None:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ssl_ctx) as resp:
            return json.loads(resp.read()), resp.headers
    except urllib.error.HTTPError as e:
        return None, {"status": e.code}
    except Exception as e:
        return None, {"error": str(e)}


def compute_velocity(weeks: list[int]) -> dict:
    if len(weeks) < 4:
        return {"velocity_score": 0, "growth_pct": 0, "recent_4_avg": 0, "prior_4_avg": 0,
                "tier": "insufficient_data"}

    recent_4 = sum(weeks[-4:]) / 4
    prior_4 = sum(weeks[-8:-4]) / 4 if len(weeks) >= 8 else sum(weeks[:max(len(weeks)-4, 1)]) / max(len(weeks)-4, 1)
    recent_2 = sum(weeks[-2:]) / 2
    mid_2 = sum(weeks[-4:-2]) / 2 if len(weeks) >= 4 else recent_2

    growth_ratio = recent_4 / max(prior_4, 1)
    acceleration = recent_2 / max(mid_2, 1)
    growth_pct = round((growth_ratio - 1) * 100, 1)

    if recent_4 < 500:
        noise_factor = max(recent_4 / 500, 0.1)
    elif recent_4 > 500_000:
        noise_factor = max(500_000 / recent_4, 0.1)
    else:
        noise_factor = 1.0

    velocity_score = round(growth_ratio * acceleration * noise_factor * 100, 1)

    if velocity_score > 80 and 500 < recent_4 < 500_000 and growth_ratio >= 1.5:
        tier = "breakout"
    elif velocity_score > 40 and recent_4 >= 500 and growth_ratio >= 1.2:
        tier = "watching"
    elif recent_4 < 500:
        tier = "too_early"
    elif recent_4 >= 500_000:
        tier = "established"
    else:
        tier = "steady"

    return {
        "velocity_score": velocity_score,
        "growth_pct": growth_pct,
        "recent_4_avg": round(recent_4),
        "prior_4_avg": round(prior_4),
        "tier": tier,
    }


# ---------------------------------------------------------------------------
# Step 1: Fetch download data from npm API
# ---------------------------------------------------------------------------

def fetch_downloads(packages: list[str], verbose: bool = True) -> list[dict]:
    end_date = datetime.now(tz=timezone.utc)
    start_date = end_date - timedelta(weeks=13)
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    npm_headers = {"User-Agent": "npm-downloads-to-leads/1.0"}
    results = []

    if verbose:
        print(f"Fetching download data for {len(packages)} packages ({start_str} to {end_str})...")

    for pkg in packages:
        encoded = encode_package(pkg)
        url = f"https://api.npmjs.org/downloads/range/{start_str}:{end_str}/{encoded}"

        data, _ = fetch_json(url, npm_headers)

        if data is None or "downloads" not in data:
            if verbose:
                print(f"  {pkg}: NOT FOUND or error")
            results.append({"package": pkg, "weeks": [], "total_weeks": 0,
                            "current_weekly": 0, "status": "not_found"})
            time.sleep(0.1)
            continue

        weekly = defaultdict(int)
        for entry in data.get("downloads", []):
            day = datetime.strptime(entry["day"], "%Y-%m-%d")
            week_key = day.isocalendar()[:2]
            weekly[week_key] += entry["downloads"]

        weeks = [v for k, v in sorted(weekly.items())][-12:]

        result = {
            "package": pkg,
            "weeks": weeks,
            "total_weeks": len(weeks),
            "current_weekly": weeks[-1] if weeks else 0,
            "status": "ok",
        }
        result.update(compute_velocity(weeks))

        if verbose:
            print(f"  {pkg}: {len(weeks)} weeks | {result['recent_4_avg']:,}/wk avg | "
                  f"growth {result['growth_pct']:+.0f}% | {result['tier'].upper()}")

        results.append(result)
        time.sleep(0.2)

    results.sort(key=lambda x: x.get("velocity_score", 0), reverse=True)
    return results


# ---------------------------------------------------------------------------
# Step 2: Fetch maintainer profiles (npm registry + GitHub)
# ---------------------------------------------------------------------------

def fetch_profiles(packages: list[dict], github_token: str = "", verbose: bool = True) -> list[dict]:
    target = [p for p in packages if p.get("tier") in ("breakout", "watching")]

    if not target:
        return []

    if verbose:
        print(f"\nFetching profiles for {len(target)} packages (breakout + watching)...")

    npm_headers = {"User-Agent": "npm-downloads-to-leads/1.0"}
    gh_headers = {"Accept": "application/vnd.github+json", "User-Agent": "npm-downloads-to-leads/1.0"}
    if github_token:
        gh_headers["Authorization"] = f"Bearer {github_token}"

    gh_rate_remaining = 999
    enriched = []

    for item in target:
        pkg = item["package"]
        profile = {
            "package": pkg,
            "description": "",
            "keywords": [],
            "npm_homepage": "",
            "npm_maintainers": [],
            "github_owner": None,
            "github_repo": None,
            "github_users": [],
        }

        # npm registry
        encoded = encode_package(pkg)
        reg_data, _ = fetch_json(f"https://registry.npmjs.org/{encoded}", npm_headers)

        if reg_data:
            profile["description"] = reg_data.get("description", "")
            profile["keywords"] = (reg_data.get("keywords") or [])[:6]
            profile["npm_homepage"] = reg_data.get("homepage", "")
            profile["npm_maintainers"] = [
                m.get("name", "") for m in reg_data.get("maintainers", []) if m.get("name")
            ]

            repo_field = reg_data.get("repository") or {}
            repo_url = repo_field.get("url", "") if isinstance(repo_field, dict) else str(repo_field)
            gh_match = re.search(r"github\.com[/:]([^/]+)/([^/.]+)", repo_url)
            if gh_match:
                profile["github_owner"] = gh_match.group(1)
                profile["github_repo"] = gh_match.group(2).rstrip(".git")

            if verbose:
                print(f"  {pkg}: registry OK | owner={profile['github_owner']} | "
                      f"maintainers={profile['npm_maintainers'][:2]}")

        time.sleep(0.1)

        # GitHub user profiles
        candidates = []
        if profile["github_owner"]:
            candidates.append(profile["github_owner"])
        for m in profile["npm_maintainers"][:2]:
            if m and m not in candidates:
                candidates.append(m)

        for username in candidates[:3]:
            if gh_rate_remaining <= 5:
                if verbose:
                    print(f"  GitHub rate limit low ({gh_rate_remaining}) -- skipping {username}")
                break

            gh_data, gh_resp_headers = fetch_json(
                f"https://api.github.com/users/{username}", gh_headers
            )

            if isinstance(gh_resp_headers, dict):
                remaining_raw = gh_resp_headers.get("X-RateLimit-Remaining") or gh_resp_headers.get("x-ratelimit-remaining")
            else:
                remaining_raw = gh_resp_headers.get("X-RateLimit-Remaining")

            if remaining_raw:
                gh_rate_remaining = int(remaining_raw)

            if gh_data and gh_data.get("login"):
                profile["github_users"].append({
                    "username": gh_data.get("login", username),
                    "name": gh_data.get("name") or username,
                    "twitter_username": gh_data.get("twitter_username") or "not found on GitHub",
                    "bio": gh_data.get("bio") or "",
                    "blog": gh_data.get("blog") or "",
                    "company": gh_data.get("company") or "",
                    "followers": gh_data.get("followers", 0),
                    "public_repos": gh_data.get("public_repos", 0),
                    "github_url": gh_data.get("html_url", f"https://github.com/{username}"),
                })
                if verbose:
                    twitter = gh_data.get("twitter_username") or "none"
                    print(f"    @{username}: {gh_data.get('followers', 0):,} followers | "
                          f"twitter={twitter} | rate_remaining={gh_rate_remaining}")
            else:
                if verbose:
                    print(f"    @{username}: not found on GitHub")

            time.sleep(0.2)

        enriched.append({**item, "profile": profile})

    return enriched


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Fetch npm download trends and maintainer profiles for a list of packages."
    )
    parser.add_argument("packages", nargs="*", help="npm package names (e.g. esbuild @hono/hono zod)")
    parser.add_argument("--file", "-f", help="text file with one package name per line")
    parser.add_argument("--output", "-o", help="output JSON file path (default: npm-leads-YYYY-MM-DD.json)")
    parser.add_argument("--stdout", action="store_true", help="print JSON to stdout instead of writing a file")
    parser.add_argument("--context", "-c", default="", help="short description of your product (used in lead brief context)")
    parser.add_argument("--quiet", "-q", action="store_true", help="suppress progress output")
    args = parser.parse_args()

    # Collect package names
    packages = list(args.packages)
    if args.file:
        try:
            file_pkgs = [l.strip() for l in open(args.file).readlines() if l.strip() and not l.startswith("#")]
            packages.extend(file_pkgs)
        except FileNotFoundError:
            print(f"Error: file '{args.file}' not found.", file=sys.stderr)
            sys.exit(1)

    packages = list(dict.fromkeys(packages))  # deduplicate, preserve order

    if not packages:
        parser.print_help()
        print("\nError: no packages provided. Pass package names as arguments or use --file.", file=sys.stderr)
        sys.exit(1)

    verbose = not args.quiet
    github_token = os.environ.get("GITHUB_TOKEN", "")

    if verbose and not github_token:
        print("Note: GITHUB_TOKEN not set. GitHub enrichment limited to ~10 packages (60 req/hr).")
        print("      Add token at github.com/settings/tokens (no scopes needed).\n")

    # Run pipeline
    scored = fetch_downloads(packages, verbose=verbose)
    enriched = fetch_profiles(scored, github_token=github_token, verbose=verbose)

    # Build enriched map for scored packages
    enriched_map = {e["package"]: e for e in enriched}
    final = []
    for pkg_data in scored:
        pkg = pkg_data["package"]
        if pkg in enriched_map:
            final.append(enriched_map[pkg])
        else:
            final.append(pkg_data)

    # Summary
    breakout = [p for p in scored if p.get("tier") == "breakout"]
    watching = [p for p in scored if p.get("tier") == "watching"]

    date_str = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

    output_data = {
        "date": date_str,
        "product_context": args.context,
        "packages_analyzed": len(packages),
        "breakout_count": len(breakout),
        "watching_count": len(watching),
        "results": final,
        "summary": {
            "breakout": [{"package": p["package"], "velocity_score": p["velocity_score"],
                          "growth_pct": p["growth_pct"], "recent_4_avg": p["recent_4_avg"]}
                         for p in breakout],
            "watching": [{"package": p["package"], "velocity_score": p["velocity_score"],
                          "growth_pct": p["growth_pct"], "recent_4_avg": p["recent_4_avg"]}
                         for p in watching],
        }
    }

    if args.stdout:
        print(json.dumps(output_data, indent=2))
        return

    output_path = args.output or f"npm-leads-{date_str}.json"
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)

    if verbose:
        print(f"\n{'='*50}")
        print(f"Results: {len(packages)} packages analyzed")
        print(f"  BREAKOUT: {len(breakout)}")
        print(f"  WATCHING: {len(watching)}")
        print(f"\nVelocity Leaderboard:")
        for i, p in enumerate(scored[:10], 1):
            tier_label = p.get("tier", "?").upper()
            print(f"  {i:2}. {p['package']:30} score={p.get('velocity_score', 0):6.1f}  "
                  f"{p.get('recent_4_avg', 0):>8,}/wk  {p.get('growth_pct', 0):+.0f}%  [{tier_label}]")

        print(f"\nSaved to: {output_path}")
        print(f"\nNext step: open {output_path} with Claude and ask it to generate lead briefs.")


if __name__ == "__main__":
    main()
