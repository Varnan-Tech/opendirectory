---
name: sdk-adoption-tracker
description: Given your SDK or library name, searches GitHub code search for public repos that import or require it, classifies each repo as company org, affiliated developer, solo developer, or tutorial noise, scores by adoption signal strength, detects new adopters by date, and outputs a ranked list of who is building on you with outreach context per high-signal company. Use when asked to find who uses your SDK, track SDK adoption, find companies building on your library, identify warm leads from existing SDK users, or see which orgs import your package. Trigger when a user says "who is using my SDK", "find repos that import my library", "track adoption of my package", "which companies are building on my SDK", "find my SDK users on GitHub", or "show me who imports my package".
compatibility: [claude-code, gemini-cli, github-copilot]
---

# SDK Adoption Tracker

Take an SDK name. Search GitHub for public repos that import it. Score each repo by company signal, activity, and noise indicators. Enrich high-signal repos with owner and contributor data. Output a ranked adoption report with outreach context for company adopters.

---

**Critical rule:** Every repo in the output must exist in the GitHub code search API response. Every company name must come from the GitHub user or org API `company` or `name` field. Every contributor handle must come from the GitHub contributors API response. If any field is empty in the API, write "not listed" -- do not infer, guess, or extrapolate.

---

## Common Mistakes

| The agent will want to... | Why that's wrong |
|---|---|
| Run code search without GITHUB_TOKEN | Unauthenticated code search hits a 3 req/min secondary rate limit and fails on any meaningful scan. GITHUB_TOKEN is required. Stop at Step 1 with a clear error if it is missing. |
| Include forks of the SDK itself | Repos that fork the SDK are contributors or mirrors, not adopters. Filter out repos where `fork == true` AND the repo name matches the SDK name. |
| Send all 500 raw search results to the AI | Code search can return up to 500 results, most of which are noise. Filter and score locally first. Send only the top 20 high-signal repos to the AI analysis step. |
| Report tutorial and example repos as adopters | Repos with "example", "tutorial", "demo", "learn", "sample", "playground", "starter" in the name or description are not production users. Mark as tutorial_noise and exclude from lead briefs. |
| Invent company names or contact handles | Every company name must come from the GitHub `company` or org `name` field. Every contributor handle must come from the contributors API response. If a field is empty, write "not listed". |
| Use one import pattern for all ecosystems | `require('sdk')` will not find Python users. Auto-detect ecosystem from the SDK name and build ecosystem-specific patterns. Ask the user if auto-detection is ambiguous. |

---

## Step 1: Setup Check

```bash
if [ -z "$GITHUB_TOKEN" ]; then
  echo "ERROR: GITHUB_TOKEN is required for code search."
  echo "Add a token at github.com/settings/tokens (no scopes needed for public repos)."
  echo "Without it, GitHub code search hits a 3 req/min secondary rate limit and fails."
  exit 1
fi
echo "GITHUB_TOKEN: set"
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github+json" \
     "https://api.github.com/rate_limit" | python3 -c "
import json, sys
d = json.load(sys.stdin)
search = d['resources']['search']
core = d['resources']['core']
print(f'Search rate: {search[\"remaining\"]}/{search[\"limit\"]} remaining')
print(f'Core rate:   {core[\"remaining\"]}/{core[\"limit\"]} remaining')
"
```

If search remaining is 0: stop. Tell the user the reset time from `X-RateLimit-Reset`.

---

## Step 2: Gather Input

Collect from the conversation:
- SDK name (e.g. `@company/my-sdk`, `requests`, `github.com/org/go-sdk`)
- Optional: ecosystem override (`npm`, `python`, `go`, `gem`) -- auto-detected if not provided
- Optional: org/user to exclude from results (the SDK owner's own repos)
- Optional: product context string (used to personalize outreach messages)

**Auto-detect ecosystem:**
- Starts with `@` or contains `-`: npm
- snake_case with no `/` or `-`: python
- Contains `github.com/`: go
- Otherwise: ask the user

**If no SDK name is provided:** Ask: "Which SDK or library would you like to track? Provide the package name as it appears in import statements (e.g. `stripe`, `@clerk/nextjs`, `requests`)."

```bash
python3 << 'PYEOF'
import json, sys, re

sdk_name = "SDK_NAME_HERE"
ecosystem_override = ""  # leave empty for auto-detect
exclude_owner = ""       # optional: owner name to exclude (usually the SDK publisher)
product_context = ""     # optional: what your product does

# Auto-detect ecosystem
if ecosystem_override:
    ecosystem = ecosystem_override
elif sdk_name.startswith("@") or "-" in sdk_name:
    ecosystem = "npm"
elif re.match(r'^[a-z][a-z0-9_]*$', sdk_name):
    ecosystem = "python"
elif "github.com/" in sdk_name:
    ecosystem = "go"
else:
    ecosystem = "generic"

print(f"SDK: {sdk_name}")
print(f"Ecosystem: {ecosystem}")
print(f"Exclude owner: {exclude_owner or '(none)'}")

with open("/tmp/sat-input.json", "w") as f:
    json.dump({
        "sdk_name": sdk_name,
        "ecosystem": ecosystem,
        "exclude_owner": exclude_owner,
        "product_context": product_context
    }, f)
PYEOF
```

---

## Step 3: Search GitHub Code

Check for standalone script first -- it handles Steps 3-5 in one call.

```bash
ls scripts/fetch.py 2>/dev/null && echo "script available" || echo "script not found"
```

**If the script is available**, run it and skip to Step 6:

```bash
python3 scripts/fetch.py "$(python3 -c "import json; d=json.load(open('/tmp/sat-input.json')); print(d['sdk_name'])")" \
  --ecosystem "$(python3 -c "import json; d=json.load(open('/tmp/sat-input.json')); print(d['ecosystem'])")" \
  --exclude "$(python3 -c "import json; d=json.load(open('/tmp/sat-input.json')); print(d.get('exclude_owner',''))")" \
  --output /tmp/sat-script-out.json
```

Then load into the temp file format Steps 6-8 expect:

```bash
python3 << 'PYEOF'
import json

out = json.load(open("/tmp/sat-script-out.json"))
json.dump(out["raw_results"], open("/tmp/sat-raw-results.json", "w"), indent=2)
json.dump(out["scored"], open("/tmp/sat-scored.json", "w"), indent=2)
json.dump(out["enriched"], open("/tmp/sat-enriched.json", "w"), indent=2)
print(f"Loaded: {len(out['raw_results'])} raw | {len(out['scored'])} scored | {len(out['enriched'])} enriched")
PYEOF
```

**If the script is not available**, run the inline code below.

Build import patterns and search GitHub code for each:

```bash
python3 << 'PYEOF'
import json, urllib.request, ssl, time, os
from datetime import datetime, timezone

ctx = ssl._create_unverified_context()
token = os.environ["GITHUB_TOKEN"]
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "User-Agent": "sdk-adoption-tracker/1.0"
}

data = json.load(open("/tmp/sat-input.json"))
sdk_name = data["sdk_name"]
ecosystem = data["ecosystem"]

# Build query patterns per ecosystem
if ecosystem == "npm":
    # Use sdk name without @ prefix for bare searches
    bare = sdk_name.lstrip("@").replace("/", "/")
    queries = [
        f'require("{sdk_name}")',
        f"require('{sdk_name}')",
        f'from "{sdk_name}"',
        f"from '{sdk_name}'",
    ]
elif ecosystem == "python":
    queries = [
        f"import {sdk_name}",
        f"from {sdk_name} import",
        f"from {sdk_name}.",
    ]
elif ecosystem == "go":
    queries = [f'"{sdk_name}"']
else:
    queries = [sdk_name]

print(f"Building queries for {sdk_name} ({ecosystem}):")
for q in queries:
    print(f"  {q}")

seen_repos = {}  # full_name -> first match
search_rate_remaining = 30
flags = []

for i, query in enumerate(queries):
    if search_rate_remaining <= 2:
        flags.append(f"Code search rate limit low ({search_rate_remaining}) -- skipped remaining patterns")
        print(f"  Rate limit low ({search_rate_remaining}), stopping early")
        break

    url = f"https://api.github.com/search/code?q={urllib.parse.quote(query)}&per_page=100"
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
            search_rate_remaining = int(resp.headers.get("X-RateLimit-Remaining", 10))
            raw = json.loads(resp.read())

        items = raw.get("items", [])
        total = raw.get("total_count", 0)
        print(f"  Pattern '{query}': {total} total, {len(items)} fetched | rate_remaining={search_rate_remaining}")

        for item in items:
            repo = item.get("repository", {})
            full_name = repo.get("full_name", "")
            if full_name and full_name not in seen_repos:
                seen_repos[full_name] = {
                    "full_name": full_name,
                    "name": repo.get("name", ""),
                    "owner_login": repo.get("owner", {}).get("login", ""),
                    "owner_type": repo.get("owner", {}).get("type", ""),
                    "file_path": item.get("path", ""),
                    "matched_pattern": query,
                    "html_url": repo.get("html_url", ""),
                    "description": repo.get("description") or "",
                }

    except urllib.error.HTTPError as e:
        if e.code == 403:
            flags.append(f"Code search rate limit hit on pattern '{query}'")
            print(f"  Rate limit hit (403) on '{query}'")
            break
        else:
            print(f"  HTTP {e.code} on '{query}'")
    except Exception as e:
        print(f"  Error on '{query}': {e}")

    # Respect 10 req/min code search limit
    if i < len(queries) - 1:
        time.sleep(6)

results = list(seen_repos.values())
json.dump(results, open("/tmp/sat-raw-results.json", "w"), indent=2)
print(f"\nTotal unique repos found: {len(results)}")
if flags:
    print("Flags:", flags)

import urllib.parse  # ensure imported
PYEOF
```

**If 0 results:** Tell the user: "No repos found importing `{sdk_name}`. GitHub code search indexing takes 1-4 weeks for new packages. If the SDK is established, check the import patterns in `references/import-patterns.md`."

---

## Step 4: Score and Classify Repos

No API call. Pure Python. Filter noise, compute adoption score, classify each repo.

```bash
python3 << 'PYEOF'
import json
from datetime import datetime, timezone

data = json.load(open("/tmp/sat-input.json"))
exclude_owner = data.get("exclude_owner", "").lower()
sdk_name = data["sdk_name"].lower().split("/")[-1].replace("@", "")

results = json.load(open("/tmp/sat-raw-results.json"))

TUTORIAL_WORDS = {"example", "tutorial", "demo", "learn", "sample", "starter",
                  "boilerplate", "template", "playground", "test", "course", "workshop"}

scored = []
now = datetime.now(tz=timezone.utc)

for repo in results:
    full_name = repo["full_name"]
    owner_login = repo.get("owner_login", "").lower()
    repo_name = repo.get("name", "").lower()
    description = (repo.get("description") or "").lower()
    owner_type = repo.get("owner_type", "User")

    # Exclude the SDK owner's own repos
    if exclude_owner and owner_login == exclude_owner.lower():
        continue

    # Detect tutorial noise
    name_words = set(repo_name.replace("-", " ").replace("_", " ").split())
    desc_words = set(description.split())
    is_tutorial = bool((name_words | desc_words) & TUTORIAL_WORDS)
    # Also exclude if repo name IS the SDK name (likely a fork)
    if repo_name == sdk_name or repo_name.startswith(sdk_name + "-"):
        is_tutorial = True  # treat as noise

    # Classification tier
    if is_tutorial:
        tier = "tutorial_noise"
    elif owner_type == "Organization":
        tier = "company_org"
    else:
        tier = "solo_dev"  # will be upgraded to affiliated_dev in Step 5 if company field populated

    # Adoption score (filled with partial data now, enriched in Step 5)
    score = 0
    if owner_type == "Organization": score += 50
    if not is_tutorial:              score += 20
    # stars, days_since_push, is_fork, is_archived added in Step 5

    scored.append({
        **repo,
        "tier": tier,
        "is_tutorial": is_tutorial,
        "adoption_score": score,
        "enriched": False
    })

# Sort: company_org first, then by tier
tier_order = {"company_org": 0, "affiliated_dev": 1, "solo_dev": 2, "tutorial_noise": 3}
scored.sort(key=lambda x: (tier_order.get(x["tier"], 9), -x["adoption_score"]))

json.dump(scored, open("/tmp/sat-scored.json", "w"), indent=2)

tiers = {}
for r in scored:
    tiers[r["tier"]] = tiers.get(r["tier"], 0) + 1

print(f"Classification:")
for tier, count in sorted(tiers.items(), key=lambda x: tier_order.get(x[0], 9)):
    print(f"  {tier}: {count}")
print(f"Total: {len(scored)} repos")

non_noise = [r for r in scored if r["tier"] != "tutorial_noise"]
print(f"\nTop repos for enrichment (non-noise): {len(non_noise)}")
for r in non_noise[:5]:
    print(f"  {r['full_name']} ({r['tier']}) -- {r.get('description','')[:60]}")
PYEOF
```

**If all repos are tutorial_noise:** Stop. Tell the user: "All repos found appear to be tutorials or examples. No production adopters detected in public GitHub. The SDK may be too new, or the package name is generic enough that search results are dominated by examples."

---

## Step 5: Enrich High-Signal Repos

Fetch full repo metadata, owner profile, and top contributors for non-noise repos. Skip tutorial_noise repos entirely.

```bash
python3 << 'PYEOF'
import json, urllib.request, ssl, os, time
from datetime import datetime, timezone

ctx = ssl._create_unverified_context()
token = os.environ["GITHUB_TOKEN"]
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "User-Agent": "sdk-adoption-tracker/1.0"
}

scored = json.load(open("/tmp/sat-scored.json"))
core_remaining = 5000
flags = []

def gh_get(path):
    global core_remaining
    req = urllib.request.Request(f"https://api.github.com{path}", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            remaining = resp.headers.get("X-RateLimit-Remaining")
            if remaining:
                core_remaining = int(remaining)
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    except Exception:
        return None

target = [r for r in scored if r["tier"] != "tutorial_noise"]
print(f"Enriching {len(target)} repos (skipping tutorial_noise)...")

enriched = []

for item in target:
    full_name = item["full_name"]
    owner_login = item["owner_login"]
    owner_type = item["owner_type"]

    if core_remaining <= 10:
        flags.append(f"Core rate limit low ({core_remaining}) -- skipped enrichment for {full_name} and remaining repos")
        enriched.append({**item, "enriched": False})
        continue

    # Fetch full repo metadata
    repo_data = gh_get(f"/repos/{full_name}")
    if not repo_data:
        print(f"  {full_name}: repo not found")
        continue

    stars = repo_data.get("stargazers_count", 0)
    is_fork = repo_data.get("fork", False)
    is_archived = repo_data.get("archived", False)
    language = repo_data.get("language") or ""
    description = repo_data.get("description") or item.get("description", "")
    pushed_at = repo_data.get("pushed_at") or ""
    created_at = repo_data.get("created_at") or ""
    repo_url = repo_data.get("html_url", f"https://github.com/{full_name}")

    # Compute days since last push
    days_since_push = 999
    if pushed_at:
        pushed_dt = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
        days_since_push = (datetime.now(tz=timezone.utc) - pushed_dt).days

    days_since_created = 999
    if created_at:
        created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        days_since_created = (datetime.now(tz=timezone.utc) - created_dt).days

    # Fetch owner profile (user or org)
    owner_profile = {}
    company = ""
    org_website = ""

    if owner_type == "Organization":
        org_data = gh_get(f"/orgs/{owner_login}")
        if org_data:
            company = org_data.get("name") or owner_login
            org_website = org_data.get("blog") or ""
            owner_profile = {
                "type": "org",
                "name": org_data.get("name") or owner_login,
                "description": org_data.get("description") or "",
                "website": org_website,
                "email": org_data.get("email") or "",
                "public_repos": org_data.get("public_repos", 0),
                "followers": org_data.get("followers", 0),
            }
    else:
        user_data = gh_get(f"/users/{owner_login}")
        if user_data:
            company = user_data.get("company") or ""
            owner_profile = {
                "type": "user",
                "name": user_data.get("name") or owner_login,
                "company": company,
                "bio": user_data.get("bio") or "",
                "blog": user_data.get("blog") or "",
                "followers": user_data.get("followers", 0),
                "twitter_username": user_data.get("twitter_username") or "not listed",
            }
            # Upgrade tier if company field is populated
            if company and item["tier"] == "solo_dev":
                item["tier"] = "affiliated_dev"

    # Fetch top contributors (skip if rate limit low)
    top_contributors = []
    if core_remaining > 20:
        contributors = gh_get(f"/repos/{full_name}/contributors?per_page=3")
        if contributors:
            top_contributors = [
                {"login": c.get("login", ""), "contributions": c.get("contributions", 0)}
                for c in contributors[:3]
            ]

    # Compute final adoption score
    score = 0
    if owner_type == "Organization":      score += 50
    if company and company.strip():        score += 20
    score += min(stars, 500) / 10
    if days_since_push < 30:              score += 30
    if days_since_push < 7:               score += 20
    if not is_fork:                       score += 10
    if not is_archived:                   score += 10
    if not item.get("is_tutorial", False): score += 20

    tier = item["tier"]
    if is_archived or is_fork:
        tier = "tutorial_noise" if item.get("is_tutorial") else tier

    enriched_item = {
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
        "repo_url": repo_url,
        "tier": tier,
        "adoption_score": round(score, 1),
        "company": company,
        "org_website": org_website,
        "owner_profile": owner_profile,
        "top_contributors": top_contributors,
        "enriched": True,
    }
    enriched.append(enriched_item)

    print(f"  {full_name} | tier={tier} | score={round(score,1)} | "
          f"stars={stars} | pushed={days_since_push}d ago | "
          f"company={company or 'not listed'} | rate={core_remaining}")
    time.sleep(0.1)

enriched.sort(key=lambda x: -x["adoption_score"])

json.dump(enriched, open("/tmp/sat-enriched.json", "w"), indent=2)
print(f"\nEnrichment complete: {len(enriched)} repos | rate_remaining={core_remaining}")
if flags:
    for f in flags:
        print(f"  FLAG: {f}")
PYEOF
```

---

## Step 6: Generate Adoption Briefs

Print top adopters, then generate outreach briefs for high-signal company repos.

```bash
python3 << 'PYEOF'
import json
from datetime import datetime, timezone

enriched = json.load(open("/tmp/sat-enriched.json"))
data = json.load(open("/tmp/sat-input.json"))
product_context = data.get("product_context", "")
sdk_name = data["sdk_name"]

high_signal = [r for r in enriched if r["adoption_score"] >= 80]
medium = [r for r in enriched if 40 <= r["adoption_score"] < 80]
noise = [r for r in enriched if r["adoption_score"] < 40 or r["tier"] == "tutorial_noise"]

print("=== DATA FOR ADOPTION BRIEF GENERATION ===")
print(f"SDK: {sdk_name}")
print(f"Product context: {product_context or '(none provided)'}")
print()

for item in (high_signal + medium)[:20]:
    prof = item.get("owner_profile", {})
    contribs = item.get("top_contributors", [])
    primary = contribs[0] if contribs else {}

    print(f"REPO: {item['full_name']} (tier={item['tier']}, score={item['adoption_score']})")
    print(f"  Stars: {item.get('stars', 0)} | Language: {item.get('language','?')} | "
          f"Pushed: {item.get('days_since_push', '?')} days ago")
    print(f"  Description: {item.get('description','none')}")
    print(f"  SDK found in: {item.get('file_path','?')}")
    print(f"  Owner type: {item.get('owner_type','?')} | Company: {item.get('company','not listed')}")
    if prof.get("type") == "org":
        print(f"  Org: {prof.get('name')} | Website: {prof.get('website','none')} | "
              f"Repos: {prof.get('public_repos',0)}")
    elif prof.get("type") == "user":
        print(f"  User: {prof.get('name')} | Company: {prof.get('company','not listed')} | "
              f"Twitter: {prof.get('twitter_username','not listed')} | "
              f"Followers: {prof.get('followers',0)}")
    if primary:
        print(f"  Top contributor: @{primary.get('login')} ({primary.get('contributions',0)} commits)")
    print()
PYEOF
```

Using the repo data printed above, generate an adoption brief for each HIGH-SIGNAL repo (score >= 80).

Rules:
- Every repo name, star count, and file path must come from the printed data -- do not modify
- Every contributor handle must come from the printed "Top contributor" line -- if none listed, write "not listed"
- Every company name must come from the printed "Company" or "Org" line -- if "not listed", write "not listed"
- "Why reach out" must reference specific signals from the data (score, stars, days since push, company)
- "Suggested message" must name the repo, the specific file where the SDK was found, and connect to product_context if provided
- No em dashes. No forbidden words: powerful, robust, seamless, innovative, game-changing, streamline, leverage, transform

Write your briefs to `/tmp/sat-briefs.json` with this structure:

```json
{
  "adoption_briefs": [
    {
      "repo": "owner/repo-name",
      "tier": "company_org",
      "adoption_score": 124.0,
      "company": "Company Name or not listed",
      "top_contributor": "@handle or not listed",
      "twitter": "@handle or not listed",
      "stars": 234,
      "language": "TypeScript",
      "sdk_file": "src/api/client.ts",
      "why_reach_out": "2-3 sentences specific to this repo's signals",
      "suggested_message": "2-4 sentences naming the repo, SDK file, and product_context connection"
    }
  ]
}
```

After writing, confirm:

```bash
python3 -c "
import json
d = json.load(open('/tmp/sat-briefs.json'))
print(f'Briefs generated: {len(d.get(\"adoption_briefs\", []))}')
for b in d['adoption_briefs']:
    print(f'  {b[\"repo\"]} ({b[\"tier\"]}): score={b[\"adoption_score\"]} company={b[\"company\"]}')
"
```

---

## Step 7: Self-QA

```bash
python3 << 'PYEOF'
import json

raw = json.load(open("/tmp/sat-raw-results.json"))
enriched = json.load(open("/tmp/sat-enriched.json"))
briefs = json.load(open("/tmp/sat-briefs.json"))

failures = []

# Verify every repo in briefs exists in raw search results
raw_full_names = {r["full_name"] for r in raw}
for brief in briefs.get("adoption_briefs", []):
    if brief.get("repo") not in raw_full_names:
        failures.append(f"Brief for unknown repo '{brief.get('repo')}' not in code search results -- removed")

briefs["adoption_briefs"] = [
    b for b in briefs.get("adoption_briefs", []) if b.get("repo") in raw_full_names
]

# Verify briefs are sorted by adoption_score descending
scores = [b["adoption_score"] for b in briefs.get("adoption_briefs", [])]
if scores != sorted(scores, reverse=True):
    briefs["adoption_briefs"].sort(key=lambda x: -x["adoption_score"])
    failures.append("Re-sorted briefs by adoption_score descending")

# Check for em dashes
briefs_str = json.dumps(briefs)
if "—" in briefs_str:
    briefs_str = briefs_str.replace("—", " - ")
    briefs = json.loads(briefs_str)
    failures.append("Fixed: em dash characters removed from briefs")

# Check for forbidden words
forbidden = ["powerful", "robust", "seamless", "innovative", "game-changing",
             "streamline", "leverage", "transform", "revolutionize"]
full_text = json.dumps(briefs).lower()
for word in forbidden:
    if word in full_text:
        failures.append(f"Warning: forbidden word '{word}' found in briefs -- review before presenting")

# Check required fields
for brief in briefs.get("adoption_briefs", []):
    for field in ["repo", "tier", "adoption_score", "company", "top_contributor",
                  "why_reach_out", "suggested_message"]:
        if brief.get(field) is None:
            failures.append(f"Missing field '{field}' in brief for {brief.get('repo', '?')}")

output = {
    "enriched": enriched,
    "briefs": briefs,
    "data_quality_flags": failures
}
json.dump(output, open("/tmp/sat-output.json", "w"), indent=2)
print(f"QA complete. Issues found: {len(failures)}")
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

output = json.load(open("/tmp/sat-output.json"))
enriched = output["enriched"]
briefs_map = {b["repo"]: b for b in output["briefs"].get("adoption_briefs", [])}
flags = output["data_quality_flags"]
data = json.load(open("/tmp/sat-input.json"))
sdk_name = data["sdk_name"]
date_str = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

high_signal = [r for r in enriched if r["adoption_score"] >= 80]
medium = [r for r in enriched if 40 <= r["adoption_score"] < 80]
noise = [r for r in enriched if r["adoption_score"] < 40 or r["tier"] == "tutorial_noise"]

# Compute velocity buckets
new_7d = sum(1 for r in enriched if r.get("days_since_created", 999) <= 7)
new_30d = sum(1 for r in enriched if r.get("days_since_created", 999) <= 30)

# Load previous snapshot for comparison
slug = sdk_name.replace("@", "").replace("/", "-")
prev_repos = set()
prev_path = f"docs/sdk-adopters/"
if os.path.isdir(prev_path):
    import glob
    prev_files = sorted(glob.glob(f"{prev_path}{slug}-*.json"))
    if prev_files:
        try:
            prev_data = json.load(open(prev_files[-1]))
            prev_repos = {r["full_name"] for r in prev_data.get("enriched", [])}
        except Exception:
            pass

new_since_last = len({r["full_name"] for r in enriched} - prev_repos) if prev_repos else None

tier_counts = {}
for r in enriched:
    tier_counts[r["tier"]] = tier_counts.get(r["tier"], 0) + 1

lines = [
    f"## SDK Adoption Report: {sdk_name}",
    f"Repos found: {len(enriched)} | Company repos: {tier_counts.get('company_org', 0)} | "
    f"Active (30 days): {sum(1 for r in enriched if r.get('days_since_push', 999) <= 30)} | Date: {date_str}",
    "",
    "---",
    "",
    "### Adoption Velocity",
    f"New repos last 7 days: {new_7d}",
    f"New repos last 30 days: {new_30d}",
]
if new_since_last is not None:
    lines.append(f"New since last run: {new_since_last}")
lines += ["", "---", ""]

if high_signal or medium:
    lines += ["### Top Adopters", ""]
    lines += [
        "| Rank | Repo | Stars | Tier | Score | Pushed | Language |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate((high_signal + medium)[:15], 1):
        pushed_label = f"{r.get('days_since_push','?')}d ago"
        lines.append(
            f"| {i} | [{r['full_name']}]({r.get('repo_url', '')}) | "
            f"{r.get('stars',0):,} | {r['tier']} | {r['adoption_score']} | "
            f"{pushed_label} | {r.get('language','?')} |"
        )
    lines += ["", "---", ""]

if high_signal:
    lines += ["### Adoption Briefs (score >= 80)", ""]
    for r in high_signal:
        brief = briefs_map.get(r["full_name"], {})
        prof = r.get("owner_profile", {})
        lines.append(f"#### {r['full_name']}  [score: {r['adoption_score']}]")
        lines.append(f"Owner: {r['owner_login']} ({r['owner_type']})")
        lines.append(f"Stars: {r.get('stars',0):,} | Language: {r.get('language','?')} | "
                     f"Last pushed: {r.get('days_since_push','?')} days ago")
        if r.get("description"):
            lines.append(f"What they're building: {r['description']}")
        lines.append(f"SDK found in: {r.get('file_path','?')}")
        if r.get("company") and r["company"] != "not listed":
            lines.append(f"Company: {r['company']}")
        if r.get("org_website"):
            lines.append(f"Website: {r['org_website']}")
        contribs = r.get("top_contributors", [])
        if contribs:
            lines.append(f"Top contributor: @{contribs[0]['login']} ({contribs[0]['contributions']} commits)")
        lines.append("")
        if brief.get("why_reach_out"):
            lines.append(f"**Why reach out:** {brief['why_reach_out']}")
        if brief.get("suggested_message"):
            lines.append(f"\n**Suggested message:**")
            lines.append(f"> {brief['suggested_message']}")
        lines += ["", "---", ""]

lines += [
    "### Adoption Breakdown",
    "",
    "| Tier | Count |",
    "|---|---|",
]
for tier in ["company_org", "affiliated_dev", "solo_dev", "tutorial_noise"]:
    count = tier_counts.get(tier, 0)
    lines.append(f"| {tier} | {count} |")

lines += ["", "---", ""]
lines.append(f"Data quality notes: {'; '.join(flags) if flags else 'None'}")

output_dir = f"docs/sdk-adopters"
os.makedirs(output_dir, exist_ok=True)
md_path = f"{output_dir}/{slug}-{date_str}.md"
json_path = f"{output_dir}/{slug}-{date_str}.json"

open(md_path, "w").write("\n".join(lines))
json.dump({"enriched": enriched, "briefs": output["briefs"]}, open(json_path, "w"), indent=2)

print("\n".join(lines))
print(f"\nSaved to: {md_path}")
print(f"JSON snapshot: {json_path} (used for velocity tracking on next run)")
PYEOF
```

Clean up temp files:

```bash
rm -f /tmp/sat-input.json /tmp/sat-raw-results.json /tmp/sat-scored.json \
      /tmp/sat-enriched.json /tmp/sat-briefs.json /tmp/sat-output.json
```
