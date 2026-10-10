---
name: dependency-update-bot
description: Scans your project for outdated npm, pip, Cargo, Go, or Ruby packages. Runs a CVE security audit. Fetches changelogs, summarizes breaking changes with Gemini, and opens one PR per risk group (patch, minor, major). Includes Diagnosis Mode for install conflicts. Use when asked to update dependencies, check for outdated packages, open dependency PRs, scan for package updates, audit for CVEs, or flag breaking changes in upgrades. Trigger when a user says "check for outdated packages", "update my dependencies", "open PRs for dependency updates", "scan for CVEs", or "which packages need upgrading".
author: OpenDirectory
version: 1.0.0
---

# Dependency Update Bot

Scan for outdated packages. Run a security audit. Fetch changelogs. Summarize breaking changes. Open one PR per risk group.

---

**Critical rule:** Only update packages that the package manager's outdated command actually reports. Never guess or invent version numbers. If a changelog cannot be fetched, note the gap rather than inventing content.

---

## Step 1: Setup Check

```bash
echo "GEMINI_API_KEY: ${GEMINI_API_KEY:+set}"
echo "GITHUB_TOKEN: ${GITHUB_TOKEN:-not set, changelog fetching rate-limited to 60/hour}"
gh auth status 2>/dev/null | head -1 || echo "gh: not authenticated"
```

**If GEMINI_API_KEY is missing:** Stop. Tell the user: "GEMINI_API_KEY is required. Get it at aistudio.google.com. Add it to your .env file."

**If gh is not authenticated:** Stop. Tell the user: "GitHub CLI must be authenticated. Run: gh auth login"

**Detect package manager(s):**

```bash
ls package.json 2>/dev/null && echo "npm"
ls requirements.txt pyproject.toml 2>/dev/null && echo "pip"
ls Cargo.toml 2>/dev/null && echo "cargo"
ls go.mod 2>/dev/null && echo "go"
ls Gemfile 2>/dev/null && echo "ruby"
```

If multiple are found, ask: "Found [list]. Which should I scan? (all / npm / pip / cargo / go / ruby)"

---

## Step 2: Detect Outdated Packages

**npm:**
```bash
npm outdated --json --long 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
for name, info in data.items():
    print(json.dumps({'name': name, 'current': info.get('current','?'), 'latest': info.get('latest','?'), 'dep_type': info.get('type','dependencies')}))
"
```

**pip:**
```bash
pip list --outdated --format=json 2>/dev/null | python3 -c "
import sys, json
for p in json.load(sys.stdin):
    print(json.dumps({'name': p['name'], 'current': p['version'], 'latest': p['latest_version']}))
"
```

**Cargo (Rust):**
```bash
cargo outdated --format json 2>/dev/null || \
  cargo outdated 2>/dev/null | grep -v "^---" | tail -n +3 | head -30
# If cargo-outdated not installed: cargo install cargo-outdated
```

**Go modules:**
```bash
go list -u -m -json all 2>/dev/null | python3 -c "
import sys, json
decoder = json.JSONDecoder()
buf = sys.stdin.read()
pos = 0
while pos < len(buf):
    try:
        obj, idx = decoder.raw_decode(buf, pos)
        if obj.get('Update'):
            print(json.dumps({'name': obj['Path'], 'current': obj['Version'], 'latest': obj['Update']['Version']}))
        pos += idx
    except: break
"
```

**Ruby (Bundler):**
```bash
bundle outdated --parseable 2>/dev/null | python3 -c "
import sys
for line in sys.stdin:
    parts = line.strip().split()
    if len(parts) >= 4:
        print('{\"name\":\"' + parts[0] + '\",\"current\":\"' + parts[3].strip('()') + '\",\"latest\":\"' + parts[1] + '\"}')
"
```

If all return empty: "All packages are up to date." Stop.

State count before proceeding: "Found X outdated packages."

---

## Step 3: Classify by Risk Level

Parse version bump (current → latest):
- MAJOR: first digit changed (1.x.x → 2.x.x)
- MINOR: second digit changed (1.2.x → 1.3.x)
- PATCH: third digit changed (1.2.3 → 1.2.4)

```bash
python3 -c "
def classify(current, latest):
    try:
        c = [int(x) for x in current.lstrip('v').split('.')[:3]]
        l = [int(x) for x in latest.lstrip('v').split('.')[:3]]
        if l[0] > c[0]: return 'major'
        if len(l) > 1 and len(c) > 1 and l[1] > c[1]: return 'minor'
        return 'patch'
    except: return 'unknown'
"
```

State the breakdown: "Patch: X packages. Minor: Y packages. Major: Z packages."

---

## Step 4: Security Audit

Run a CVE scan before creating any PRs. This determines urgency.

**npm:**
```bash
npm audit --json 2>/dev/null | python3 -c "
import sys, json
d = json.load(sys.stdin)
vulns = d.get('vulnerabilities', {})
for pkg, info in vulns.items():
    sev = info.get('severity', 'unknown')
    via = [v.get('title','') for v in info.get('via',[]) if isinstance(v, dict)]
    print(f'  [{sev.upper()}] {pkg}: {via[0] if via else \"see npm audit\"}')
" 2>/dev/null || echo "No vulnerabilities found or npm audit not available"
```

**pip:**
```bash
pip-audit --format=json 2>/dev/null | python3 -c "
import sys, json
for vuln in json.load(sys.stdin):
    print(f'  [{vuln.get(\"aliases\",[\"\"])[0]}] {vuln[\"name\"]} {vuln[\"version\"]}: {vuln[\"description\"][:80]}')
" 2>/dev/null || echo "pip-audit not installed. Run: pip install pip-audit"
```

**Cargo:**
```bash
cargo audit 2>/dev/null | grep -E "^(ID|Package|Severity|URL)" | head -30 \
  || echo "cargo-audit not installed. Run: cargo install cargo-audit"
```

**Escalation rule:** If a PATCH or MINOR update has a Critical or High CVE, promote it to MAJOR priority: it gets its own PR and the CVE details go in the PR body.

Report security findings before proceeding:
```
Security audit: [N] vulnerabilities found
  [CRITICAL] lodash 4.17.19: Prototype Pollution (CVE-2021-23337)
  [HIGH] axios 0.21.1: Server-Side Request Forgery (CVE-2021-3749)
```

If no vulnerabilities: "Security audit: clean."

---

## Step 5: Fetch Changelogs

For each package, try sources in order. Stop at first that returns content.

**Source 1: GitHub Releases API**

Get repo URL from registry:
```bash
# npm
curl -s "https://registry.npmjs.org/{PACKAGE}/latest" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); r=d.get('repository',{}); print(r.get('url','') if isinstance(r,dict) else str(r))"

# pip
curl -s "https://pypi.org/pypi/{PACKAGE}/json" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('info',{}).get('home_page','') or d.get('info',{}).get('project_urls',{}).get('Source',''))"
```

Fetch last 5 releases:
```bash
AUTH_HEADER=""
[ -n "$GITHUB_TOKEN" ] && AUTH_HEADER="-H \"Authorization: Bearer $GITHUB_TOKEN\""
curl -s $AUTH_HEADER \
  "https://api.github.com/repos/{OWNER}/{REPO}/releases?per_page=5" \
  | python3 -c "import sys,json; [print(json.dumps({'tag':r.get('tag_name',''),'body':r.get('body','')[:1500]})) for r in json.load(sys.stdin)]"
```

Keep releases between current and latest version only.

**Source 2: npm registry README (fallback)**
```bash
curl -s "https://registry.npmjs.org/{PACKAGE}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('readme','')[:3000])"
```

**Source 3: PyPI description (last resort for pip)**
```bash
curl -s "https://pypi.org/pypi/{PACKAGE}/json" \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('info',{}).get('description','')[:2000])"
```

If no source returns content: note "No changelog found" and continue.

---

## Step 6: Summarize with Gemini

One request per risk group. Include security findings for any CVE-affected packages:

```bash
cat > /tmp/deps-summary-request.json << 'ENDJSON'
{
  "system_instruction": {
    "parts": [{
      "text": "You are a developer writing a GitHub PR description for a dependency update. Given a list of packages being updated and their raw changelog content, write a concise PR body in Markdown. Rules: For each package, list only what changed between the OLD version and the NEW version. Use bullet points. Flag breaking changes with a BREAKING prefix. Flag CVE fixes with a SECURITY prefix and include the CVE ID. Keep each package section to 3-5 bullets maximum. If no changelog was found for a package, write 'No changelog available.' Do not use em dashes. Do not use these words: seamless, robust, leverage, transform, innovative. Output only the Markdown PR body, no commentary."
    }]
  },
  "contents": [{
    "parts": [{
      "text": "PACKAGES_AND_CHANGELOGS_HERE"
    }]
  }],
  "generationConfig": {
    "temperature": 0.2,
    "maxOutputTokens": 2048
  }
}
ENDJSON

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @/tmp/deps-summary-request.json \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['candidates'][0]['content']['parts'][0]['text'])"
```

---

## Step 7: Create PRs

One PR per non-empty risk group. One PR per package for major updates (individual review required).

**1. Create branch:**
```bash
BRANCH="deps/{RISK}-updates-$(date +%Y%m%d)"
git checkout -b "$BRANCH"
```

**2. Update package file:**

npm:
```bash
npm install {package}@{latest_version} --save-exact
# devDependencies:
npm install {package}@{latest_version} --save-dev --save-exact
```

pip:
```bash
python3 -c "
import re, sys
pkg, version, filename = sys.argv[1], sys.argv[2], sys.argv[3]
with open(filename) as f: content = f.read()
pattern = rf'^{re.escape(pkg)}[>=<!\s].*$'
new_content = re.sub(pattern, f'{pkg}=={version}', content, flags=re.MULTILINE|re.IGNORECASE)
if new_content == content: new_content = content + f'\n{pkg}=={version}'
open(filename, 'w').write(new_content)
" "{PACKAGE}" "{LATEST}" "requirements.txt"
```

Cargo:
```bash
# Edit Cargo.toml version field for the package, then:
cargo update {package}
```

Go:
```bash
go get {module}@{latest_version}
go mod tidy
```

Ruby:
```bash
bundle update {gem_name}
```

**3. Commit:**
```bash
git add -A
git commit -m "chore(deps): update {RISK} dependencies $(date +%Y-%m-%d)"
```

**4. Create PR:**
```bash
cat > /tmp/dep-pr-body-{RISK}.md << 'ENDMD'
PR_BODY_FROM_GEMINI
ENDMD

gh pr create \
  --title "chore(deps): update {RISK} dependencies" \
  --body-file /tmp/dep-pr-body-{RISK}.md \
  --label "dependencies" \
  --base main
```

Major updates get label `dependencies,breaking-change`. CVE-fixing updates get label `dependencies,security`.

After each PR, return to main: `git checkout main`

---

## Step 8: Diagnosis Mode

**Trigger:** If any package install command fails mid-run, enter Diagnosis Mode instead of stopping.

Detect the failure type:

| Error pattern | Likely cause | Suggested fix |
|---------------|-------------|--------------|
| `peer dep conflict` | Peer dependency incompatibility | Show conflicting pair, suggest `--legacy-peer-deps` flag or downgrade |
| `ERESOLVE` | npm resolution conflict | Run `npm install --legacy-peer-deps` for the affected package only |
| `version not found` | Version does not exist in registry | Check registry with `npm view {pkg} versions` |
| `python requires` | Python version incompatibility | Note required Python version, skip package |
| `cargo E0463` | Rust edition incompatibility | Flag for manual review |

Present a diagnosis summary:
```
Install failed for {package}: {error type}
Likely cause: {explanation}
Suggested fix: {specific command or action}
Remaining packages: proceeding with {N} that succeeded.
```

Do not stop the entire run when one package fails. Continue with packages that succeed.

---

## Step 9: Output Summary

```
## Dependency Update Summary: [YYYY-MM-DD]

### Security
[CRITICAL] lodash: CVE-2021-23337 fixed in 4.17.21: PR #42
[HIGH] axios: CVE-2021-3749 fixed in 0.21.4: PR #42

| Risk Level | Packages | PR |
|------------|----------|-----|
| Patch | lodash 4.17.19→4.17.21, axios 0.21.1→0.21.4 | #42 |
| Minor | express 4.17.1→4.18.2 | #43 |
| Major | react 17.0.2→18.2.0 | #44 |

PRs opened: 3

Packages with no changelog: some-obscure-pkg (no GitHub repo in registry)
Install failures: none

Next action: Review major update PRs individually before merging.
```


