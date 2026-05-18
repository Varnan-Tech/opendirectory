---
name: npm-downloads-to-leads
description: Takes a list of npm package names (yours or competitors'), fetches 12 weeks of daily download data from the npm API, computes a breakout velocity score per package to identify hockey-stick growth, fetches maintainer profiles from the npm registry and GitHub API, and outputs a ranked lead brief for each breakout package with who built it, how to reach them, and what to say. Use when asked to find evangelists before they are famous, track competitor package momentum, identify breakout npm packages, map npm maintainers to Twitter or GitHub, or find DevTools leads from package growth signals. Trigger when a user says "find leads from npm packages", "who maintains these breakout packages", "track npm download trends", "find evangelists before they are famous", or "map npm maintainers to Twitter".
compatibility: [claude-code, gemini-cli, github-copilot]
---

# npm Downloads to Leads

Take a list of npm packages. Fetch 12 weeks of download data. Compute breakout velocity. Enrich maintainer profiles. Output a ranked lead brief per breakout package with contact signals and an outreach message.

---

**Critical rule:** Every package download figure in the output must come from the npm API response. Every maintainer GitHub handle or Twitter username must come from the GitHub API response -- not guessed from the npm username. If the GitHub API did not return a twitter_username field, write "not found on GitHub" -- do not invent one.

---

## Common Mistakes

| The agent will want to... | Why that's wrong |
|---|---|
| Fetch GitHub profiles for every package in the list | Rate limit is 60 req/hr without a token. Enriching steady or declining packages wastes the budget before reaching breakout ones. Only fetch profiles for breakout and watching packages. |
| Rank packages by raw weekly downloads | Raw downloads favor React and lodash, which are not leads. A package going from 1K to 8K/week is more actionable than React at 50M/week. Velocity score is the signal. |
| Skip URL-encoding for scoped packages | @org/pkg without encoding causes a 404 from the npm API. Encode @ as %40 and / as %2F for every scoped package name. |
| Stop the skill when the GitHub rate limit is hit | Degrade gracefully. Present the velocity leaderboard from npm data, skip remaining GitHub enrichments, and add a flag to data_quality_flags. Do not abort. |
| Write outreach messages without naming the specific package | Generic "I saw your project" messages go unanswered. Every outreach message must name the package, its growth numbers, and a specific connection to the context the user provided. |
| Include packages below 500 weekly downloads as leads | Below 500/week is noise. The maintainer has no meaningful audience yet. Flag as "too early" but do not present as a lead. |

---

## Step 1: Setup Check

```bash
echo "GITHUB_TOKEN: ${GITHUB_TOKEN:-not set, unauthenticated rate limit applies (60 req/hr -- enough for ~10 packages)}"
```

**If GITHUB_TOKEN is not set:** Continue. Inform the user: "GITHUB_TOKEN is not set. GitHub enrichment is limited to ~10 packages before hitting the rate limit. Add a token at github.com/settings/tokens (no scopes needed)."

No required keys. The npm API and npm registry are fully public with no authentication.

---

## Step 2: Gather Input

Collect from the conversation:
- One or more npm package names (unscoped like `esbuild`, or scoped like `@hono/hono`)
- Optional: a short product context string (used to personalize outreach messages)

If the user gives an npmjs.com URL, extract just the package name. Preserve the full scoped name including `@` and org prefix -- encoding is handled in Step 3.

**If no packages are provided:** Ask: "Which npm packages would you like to analyze? Provide your own, competitors, or a mix. Example: esbuild, @hono/hono, zod, valibot"

```bash
python3 << 'PYEOF'
import json, sys

packages_raw = "PACKAGES_HERE"  # comma or newline separated
product_context = "CONTEXT_HERE"  # optional, can be empty string

packages = [p.strip() for p in packages_raw.replace("\n", ",").split(",") if p.strip()]
if not packages:
    print("ERROR: No packages provided.")
    sys.exit(1)

print(f"Packages to analyze: {len(packages)}")
for p in packages:
    print(f"  {p}")

with open("/tmp/npl-input.json", "w") as f:
    json.dump({"packages": packages, "product_context": product_context}, f)
PYEOF
```

---

## Step 3: Fetch 12-Week Download Data

**Use the standalone script if available -- it handles Steps 3, 4, and 5 in one call so you do not need to run the inline code blocks below.**

```bash
# Check if the script exists
ls scripts/fetch.py 2>/dev/null && echo "script available" || echo "script not found"
```

**If the script is available**, run it directly and skip to Step 6:

```bash
python3 scripts/fetch.py PACKAGES_HERE --context "CONTEXT_HERE" --output /tmp/npl-script-out.json
```

Then load the output into the enriched format Step 6 expects:

```bash
python3 << 'PYEOF'
import json

out = json.load(open("/tmp/npl-script-out.json"))
# Script output has results array -- split into scored and enriched for Steps 6-8
enriched = [r for r in out["results"] if "profile" in r]
scored = out["results"]
json.dump(scored, open("/tmp/npl-scored.json", "w"), indent=2)
json.dump(enriched, open("/tmp/npl-enriched.json", "w"), indent=2)
json.dump({"packages": [r["package"] for r in scored], "product_context": out.get("product_context", "")},
          open("/tmp/npl-input.json", "w"), indent=2)
print(f"Loaded {len(scored)} packages | {out['breakout_count']} breakout | {out['watching_count']} watching")
PYEOF
```

**If the script is not available**, run the inline code below.

Fetch daily download data for each package from the npm Downloads API. Aggregate to weekly buckets.

```bash
python3 << 'PYEOF'
import json, urllib.request, sys, time
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import urllib.parse

data = json.load(open("/tmp/npl-input.json"))
packages = data["packages"]

end_date = datetime.now(tz=timezone.utc)
start_date = end_date - timedelta(weeks=13)  # extra week buffer for partial weeks
start_str = start_date.strftime("%Y-%m-%d")
end_str = end_date.strftime("%Y-%m-%d")

results = []
failed = []

for pkg in packages:
    # URL-encode scoped packages: @ -> %40, / -> %2F
    encoded = pkg.replace("@", "%40").replace("/", "%2F")
    url = f"https://api.npmjs.org/downloads/range/{start_str}:{end_str}/{encoded}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "npm-downloads-to-leads/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = json.loads(resp.read())

        # Aggregate daily to weekly by ISO week
        weekly = defaultdict(int)
        for entry in raw.get("downloads", []):
            day = datetime.strptime(entry["day"], "%Y-%m-%d")
            week_key = day.isocalendar()[:2]  # (year, week_num)
            weekly[week_key] += entry["downloads"]

        weeks = [v for k, v in sorted(weekly.items())]
        # Take last 12 complete weekly buckets
        weeks = weeks[-12:]

        results.append({
            "package": pkg,
            "weeks": weeks,
            "total_weeks": len(weeks),
            "current_weekly": weeks[-1] if weeks else 0,
            "status": "ok"
        })
        print(f"  {pkg}: {len(weeks)} weeks, latest week {weeks[-1]:,} downloads")

    except urllib.error.HTTPError as e:
        if e.code == 404:
            failed.append(pkg)
            results.append({"package": pkg, "weeks": [], "total_weeks": 0, "current_weekly": 0, "status": "not_found"})
            print(f"  {pkg}: NOT FOUND (404) -- will be skipped")
        else:
            failed.append(pkg)
            results.append({"package": pkg, "weeks": [], "total_weeks": 0, "current_weekly": 0, "status": f"error_{e.code}"})
            print(f"  {pkg}: HTTP {e.code} error")
    except Exception as e:
        failed.append(pkg)
        results.append({"package": pkg, "weeks": [], "total_weeks": 0, "current_weekly": 0, "status": f"error"})
        print(f"  {pkg}: fetch failed ({e})")

    time.sleep(0.2)  # gentle rate limiting

json.dump(results, open("/tmp/npl-download-data.json", "w"), indent=2)
print(f"\nFetch complete. OK: {len(results) - len(failed)} | Failed/Not found: {len(failed)}")
if failed:
    print(f"Skipped: {', '.join(failed)}")
PYEOF
```

**If all packages return 404 or errors:** Stop. Tell the user: "No download data could be fetched. Check that the package names are correct and exist on npmjs.com. Scoped packages must include the full name: @org/package."

---

## Step 4: Compute Velocity Scores

No API call. Pure Python. Compute velocity score, growth ratio, and classify each package.

```bash
python3 << 'PYEOF'
import json

raw_results = json.load(open("/tmp/npl-download-data.json"))
scored = []

for item in raw_results:
    pkg = item["package"]
    weeks = item["weeks"]
    status = item["status"]

    if status != "ok" or len(weeks) < 4:
        scored.append({**item, "velocity_score": 0, "growth_pct": 0, "tier": "insufficient_data",
                       "recent_4_avg": 0, "prior_4_avg": 0})
        continue

    recent_4 = sum(weeks[-4:]) / 4
    prior_4 = sum(weeks[-8:-4]) / max(len(weeks) - 4, 1) if len(weeks) >= 8 else sum(weeks[:4]) / max(len(weeks[:4]), 1)
    recent_2 = sum(weeks[-2:]) / 2
    mid_2 = sum(weeks[-4:-2]) / 2 if len(weeks) >= 4 else recent_2

    growth_ratio = recent_4 / max(prior_4, 1)
    acceleration = recent_2 / max(mid_2, 1)
    growth_pct = round((growth_ratio - 1) * 100, 1)

    # Sweet spot multiplier: 500-500K weekly downloads
    if recent_4 < 500:
        noise_factor = max(recent_4 / 500, 0.1)
    elif recent_4 > 500_000:
        noise_factor = max(500_000 / recent_4, 0.1)
    else:
        noise_factor = 1.0

    velocity_score = round(growth_ratio * acceleration * noise_factor * 100, 1)

    # Classify
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

    scored.append({
        **item,
        "velocity_score": velocity_score,
        "growth_pct": growth_pct,
        "recent_4_avg": round(recent_4),
        "prior_4_avg": round(prior_4),
        "tier": tier
    })

# Sort by velocity_score descending
scored.sort(key=lambda x: x["velocity_score"], reverse=True)

json.dump(scored, open("/tmp/npl-scored.json", "w"), indent=2)

breakout = [p for p in scored if p["tier"] == "breakout"]
watching = [p for p in scored if p["tier"] == "watching"]
too_early = [p for p in scored if p["tier"] == "too_early"]

print(f"Velocity scoring complete:")
print(f"  BREAKOUT: {len(breakout)}")
print(f"  WATCHING: {len(watching)}")
print(f"  STEADY/ESTABLISHED: {len([p for p in scored if p['tier'] in ('steady','established')])}")
print(f"  TOO EARLY (<500/week): {len(too_early)}")
print()
for p in scored[:10]:
    print(f"  {p['tier'].upper():12} {p['package']:30} score={p['velocity_score']:6.1f}  "
          f"{p['recent_4_avg']:>8,}/wk  growth={p['growth_pct']:+.0f}%")

# Stop if nothing worth analyzing
if not breakout and not watching:
    all_too_early = all(p["tier"] in ("too_early", "insufficient_data") for p in scored)
    if all_too_early:
        print("\nERROR: All packages are below the 500 weekly downloads threshold for reliable velocity analysis.")
        print("Try packages with more community adoption.")
        import sys; sys.exit(1)
PYEOF
```

**If all packages are below 500/week:** Stop with the message above.

---

## Step 5: Fetch Maintainer Profiles

Only for breakout and watching packages. Fetch npm registry metadata, then GitHub user profiles.

```bash
python3 << 'PYEOF'
import json, urllib.request, re, os, time

scored = json.load(open("/tmp/npl-scored.json"))
token = os.environ.get("GITHUB_TOKEN", "")

gh_headers = {"Accept": "application/vnd.github+json", "User-Agent": "npm-downloads-to-leads/1.0"}
if token:
    gh_headers["Authorization"] = f"Bearer {token}"

target_packages = [p for p in scored if p["tier"] in ("breakout", "watching")]
print(f"Fetching profiles for {len(target_packages)} packages (breakout + watching)...")

gh_rate_remaining = 999
enriched = []

for item in target_packages:
    pkg = item["package"]
    profile = {"package": pkg, "npm_maintainers": [], "description": "", "keywords": [],
               "github_owner": None, "github_repo": None, "github_users": [], "npm_homepage": ""}

    # --- npm registry ---
    encoded = pkg.replace("@", "%40").replace("/", "%2F")
    reg_url = f"https://registry.npmjs.org/{encoded}"
    try:
        req = urllib.request.Request(reg_url, headers={"User-Agent": "npm-downloads-to-leads/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            reg = json.loads(resp.read())

        profile["description"] = reg.get("description", "")
        profile["keywords"] = (reg.get("keywords") or [])[:6]
        profile["npm_homepage"] = reg.get("homepage", "")
        profile["npm_maintainers"] = [m.get("name", "") for m in reg.get("maintainers", []) if m.get("name")]

        # Extract GitHub owner from repository URL
        repo_field = reg.get("repository") or {}
        if isinstance(repo_field, dict):
            repo_url = repo_field.get("url", "")
        else:
            repo_url = str(repo_field)
        gh_match = re.search(r"github\.com[/:]([^/]+)/([^/.]+)", repo_url)
        if gh_match:
            profile["github_owner"] = gh_match.group(1)
            profile["github_repo"] = gh_match.group(2).rstrip(".git")

        print(f"  {pkg}: registry OK | maintainers={profile['npm_maintainers'][:3]} | "
              f"github_owner={profile['github_owner']}")
    except Exception as e:
        print(f"  {pkg}: registry fetch failed ({e})")

    time.sleep(0.1)

    # --- GitHub user profiles ---
    candidates = []
    if profile["github_owner"]:
        candidates.append(profile["github_owner"])
    # Also try npm maintainer usernames (often match GitHub)
    for m in profile["npm_maintainers"][:2]:
        if m and m not in candidates:
            candidates.append(m)

    for username in candidates[:3]:
        if gh_rate_remaining <= 5:
            print(f"  GitHub rate limit low ({gh_rate_remaining} remaining) -- skipping {username}")
            break

        gh_url = f"https://api.github.com/users/{username}"
        req = urllib.request.Request(gh_url, headers=gh_headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                gh_rate_remaining = int(resp.headers.get("X-RateLimit-Remaining", 999))
                gh_data = json.loads(resp.read())

            profile["github_users"].append({
                "username": username,
                "name": gh_data.get("name") or username,
                "twitter_username": gh_data.get("twitter_username") or "not found on GitHub",
                "bio": gh_data.get("bio") or "",
                "blog": gh_data.get("blog") or "",
                "company": gh_data.get("company") or "",
                "followers": gh_data.get("followers", 0),
                "public_repos": gh_data.get("public_repos", 0),
                "github_url": gh_data.get("html_url", f"https://github.com/{username}")
            })
            print(f"    GitHub @{username}: {gh_data.get('followers', 0)} followers | "
                  f"twitter={gh_data.get('twitter_username') or 'none'} | rate_remaining={gh_rate_remaining}")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"    GitHub @{username}: not found")
            else:
                print(f"    GitHub @{username}: HTTP {e.code}")
        except Exception as e:
            print(f"    GitHub @{username}: failed ({e})")

        time.sleep(0.2)

    enriched.append({**item, "profile": profile})

json.dump(enriched, open("/tmp/npl-enriched.json", "w"), indent=2)
json.dump(scored, open("/tmp/npl-scored.json", "w"), indent=2)
print(f"\nEnrichment complete. Profiles fetched: {len(enriched)}")
print(f"GitHub rate limit remaining: {gh_rate_remaining}")
PYEOF
```

---

## Step 6: Generate Lead Briefs

Print enriched breakout and watching packages, then generate lead briefs and outreach messages.

```bash
python3 << 'PYEOF'
import json

enriched = json.load(open("/tmp/npl-enriched.json"))
input_data = json.load(open("/tmp/npl-input.json"))
product_context = input_data.get("product_context", "")

breakout = [p for p in enriched if p["tier"] == "breakout"]
watching = [p for p in enriched if p["tier"] == "watching"]

print("=== DATA FOR LEAD BRIEF GENERATION ===")
print(f"Product context: {product_context or '(none provided)'}")
print()

for item in breakout + watching:
    pkg = item["package"]
    prof = item.get("profile", {})
    gh_users = prof.get("github_users", [])
    primary_gh = gh_users[0] if gh_users else {}

    print(f"PACKAGE: {pkg} ({item['tier'].upper()})")
    print(f"  Velocity score: {item['velocity_score']} | Growth: {item['growth_pct']:+.0f}%")
    print(f"  Recent 4-week avg: {item['recent_4_avg']:,}/week | Prior 4-week avg: {item['prior_4_avg']:,}/week")
    print(f"  Weekly trend (last 8): {item['weeks'][-8:]}")
    print(f"  Description: {prof.get('description', 'none')}")
    print(f"  Keywords: {', '.join(prof.get('keywords', []))}")
    print(f"  npm maintainers: {', '.join(prof.get('npm_maintainers', []))}")
    if primary_gh:
        print(f"  GitHub: @{primary_gh.get('username')} | {primary_gh.get('followers')} followers | "
              f"{primary_gh.get('public_repos')} repos")
        print(f"  Twitter: {primary_gh.get('twitter_username')}")
        print(f"  Bio: {primary_gh.get('bio')}")
        print(f"  Company: {primary_gh.get('company')}")
    else:
        print(f"  GitHub: no profile found")
    print()
PYEOF
```

Using the package data printed above, generate a lead brief for each BREAKOUT and WATCHING package.

Rules:
- Every growth number in the brief must come from the printed data -- do not round or modify
- Every GitHub handle and Twitter username must come from the printed data -- write "not found on GitHub" if the field says that
- "Why reach out now" must reference the specific growth inflection (weeks, numbers) from the data
- "Suggested first message" must name the package and its growth, and if product_context was provided, connect it specifically to that context
- No em dashes. No forbidden words: powerful, robust, seamless, innovative, game-changing, streamline, leverage, transform

Write your lead briefs to `/tmp/npl-briefs.json` with this exact structure:

```json
{
  "lead_briefs": [
    {
      "package": "pkg-name",
      "tier": "breakout",
      "growth_summary": "1-sentence summary of the growth numbers",
      "maintainer_handle": "@github_handle or npm username if no GitHub found",
      "twitter": "@handle or not found on GitHub",
      "github_followers": 0,
      "why_now": "2-3 sentences specific to this package's inflection point",
      "suggested_message": "2-4 sentences. Names the package, the growth, and connects to product_context if provided."
    }
  ]
}
```

After writing the file, confirm with:

```bash
python3 -c "
import json
d = json.load(open('/tmp/npl-briefs.json'))
print(f'Lead briefs generated: {len(d.get(\"lead_briefs\", []))}')
for b in d['lead_briefs']:
    print(f'  {b[\"package\"]} ({b[\"tier\"]}): maintainer={b[\"maintainer_handle\"]}')
"
```

---

## Step 7: Self-QA

```bash
python3 << 'PYEOF'
import json

scored = json.load(open("/tmp/npl-scored.json"))
enriched = json.load(open("/tmp/npl-enriched.json"))
briefs = json.load(open("/tmp/npl-briefs.json"))

failures = []

# Verify: every brief has a real package name from the scored list
real_packages = {p["package"] for p in scored}
for brief in briefs.get("lead_briefs", []):
    if brief.get("package") not in real_packages:
        failures.append(f"Brief for unknown package '{brief.get('package')}' -- removed")

briefs["lead_briefs"] = [b for b in briefs.get("lead_briefs", []) if b.get("package") in real_packages]

# Verify: velocity leaderboard is sorted correctly (checked on scored, not briefs)
sorted_scores = sorted([(p["package"], p["velocity_score"]) for p in scored], key=lambda x: -x[1])
if scored[0]["velocity_score"] < scored[-1]["velocity_score"]:
    failures.append("Scored list not sorted by velocity_score -- re-sorted")
    scored.sort(key=lambda x: x["velocity_score"], reverse=True)

# Verify: no GitHub/Twitter handles in briefs that weren't in GitHub API responses
enriched_gh = {}
for item in enriched:
    for gh_user in item.get("profile", {}).get("github_users", []):
        enriched_gh[gh_user["username"]] = gh_user.get("twitter_username", "not found on GitHub")

for brief in briefs.get("lead_briefs", []):
    twitter = brief.get("twitter", "")
    if twitter and twitter not in ("not found on GitHub", "") and not twitter.startswith("not found"):
        # Verify it came from the API
        found = any(twitter.lstrip("@") == v.lstrip("@") for v in enriched_gh.values() if v != "not found on GitHub")
        if not found:
            failures.append(f"Warning: Twitter handle '{twitter}' for {brief['package']} not verified in GitHub API data")

# Check required fields
for brief in briefs.get("lead_briefs", []):
    for field in ["package", "tier", "growth_summary", "maintainer_handle", "twitter", "why_now", "suggested_message"]:
        if not brief.get(field):
            failures.append(f"Missing field '{field}' in brief for {brief.get('package', '?')}")

# Check for em dashes
briefs_str = json.dumps(briefs)
if "\u2014" in briefs_str:
    briefs_str = briefs_str.replace("\u2014", " - ")
    briefs = json.loads(briefs_str)
    failures.append("Fixed: em dash characters removed from briefs")

# Check for forbidden words
forbidden = ["powerful", "robust", "seamless", "innovative", "game-changing", "streamline", "leverage", "transform"]
full_text = json.dumps(briefs).lower()
for word in forbidden:
    if word in full_text:
        failures.append(f"Warning: forbidden word '{word}' found in briefs -- review before presenting")

output = {
    "scored": scored,
    "enriched": enriched,
    "briefs": briefs,
    "data_quality_flags": failures
}

json.dump(output, open("/tmp/npl-output.json", "w"), indent=2)
print(f"QA complete. Issues: {len(failures)}")
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
import json, os
from datetime import datetime, timezone

output = json.load(open("/tmp/npl-output.json"))
scored = output["scored"]
enriched_map = {e["package"]: e for e in output["enriched"]}
briefs_map = {b["package"]: b for b in output["briefs"].get("lead_briefs", [])}
flags = output["data_quality_flags"]
date_str = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

breakout = [p for p in scored if p["tier"] == "breakout"]
watching = [p for p in scored if p["tier"] == "watching"]
too_early = [p for p in scored if p["tier"] == "too_early"]
established = [p for p in scored if p["tier"] == "established"]

lines = [
    f"## npm Breakout Report",
    f"Packages analyzed: {len(scored)} | Breakout: {len(breakout)} | Watching: {len(watching)} | Date: {date_str}",
    "",
    "---",
    "",
    "### Velocity Leaderboard",
    "",
    "| Rank | Package | Weekly Downloads | 8-Week Growth | Velocity Score | Status |",
    "|---|---|---|---|---|---|",
]

for i, pkg in enumerate(scored[:15], 1):
    status_label = {"breakout": "BREAKOUT", "watching": "WATCHING", "steady": "steady",
                    "established": "established", "too_early": "too early", "insufficient_data": "no data"}.get(pkg["tier"], pkg["tier"])
    growth_str = f"{pkg['growth_pct']:+.0f}%" if pkg.get("growth_pct") else "n/a"
    lines.append(
        f"| {i} | {pkg['package']} | {pkg['recent_4_avg']:,} | {growth_str} | "
        f"{pkg['velocity_score']} | {status_label} |"
    )

lines += ["", "---", ""]

if breakout or watching:
    lines += ["### Lead Briefs", ""]

    for item in breakout + watching:
        pkg = item["package"]
        brief = briefs_map.get(pkg, {})
        profile = enriched_map.get(pkg, {}).get("profile", {})
        gh_users = profile.get("github_users", [])
        primary_gh = gh_users[0] if gh_users else {}

        lines.append(f"#### {pkg} ({item['tier'].upper()})")
        lines.append(f"Weekly downloads: {item['recent_4_avg']:,}/week (was {item['prior_4_avg']:,} -- {item['growth_pct']:+.0f}% growth over 8 weeks)")
        if profile.get("description"):
            lines.append(f"What it does: {profile['description']}")
        if profile.get("keywords"):
            lines.append(f"Keywords: {', '.join(profile['keywords'])}")
        lines.append("")

        if primary_gh:
            lines.append(f"**Maintainer: @{primary_gh.get('username')}**")
            lines.append(f"- GitHub: {primary_gh.get('followers', 0):,} followers | {primary_gh.get('public_repos', 0)} public repos")
            lines.append(f"- Twitter: {primary_gh.get('twitter_username', 'not found on GitHub')}")
            if primary_gh.get("bio"):
                lines.append(f"- Bio: \"{primary_gh['bio']}\"")
            if primary_gh.get("company"):
                lines.append(f"- Company: {primary_gh['company']}")
            if primary_gh.get("blog"):
                lines.append(f"- Website: {primary_gh['blog']}")
        elif profile.get("npm_maintainers"):
            lines.append(f"**Maintainer (npm only):** {', '.join(profile['npm_maintainers'][:3])}")
            lines.append("- GitHub profile: not found")

        lines.append("")
        if brief.get("why_now"):
            lines.append(f"**Why reach out now:** {brief['why_now']}")
        if brief.get("suggested_message"):
            lines.append(f"\n**Suggested first message:**")
            lines.append(f"> {brief['suggested_message']}")
        lines.append("")
        lines.append("---")
        lines.append("")

if too_early:
    lines += [f"### Too Early ({len(too_early)} packages below 500 weekly downloads)", ""]
    for p in too_early:
        lines.append(f"- {p['package']}: ~{p['recent_4_avg']:,}/week -- revisit when above 500/week")
    lines.append("")

if established:
    lines += [f"### Established Packages (above 500K/week, velocity less meaningful)", ""]
    for p in established:
        lines.append(f"- {p['package']}: ~{p['recent_4_avg']:,}/week")
    lines.append("")

lines += ["---", ""]
lines.append(f"Data quality notes: {'; '.join(flags) if flags else 'None'}")

output_path = f"docs/npm-leads/{date_str}.md"
os.makedirs("docs/npm-leads", exist_ok=True)
open(output_path, "w").write("\n".join(lines))

print("\n".join(lines))
print(f"\nSaved to: {output_path}")
PYEOF
```

Clean up temp files:

```bash
rm -f /tmp/npl-input.json /tmp/npl-download-data.json /tmp/npl-scored.json \
      /tmp/npl-enriched.json /tmp/npl-briefs.json /tmp/npl-output.json
```
