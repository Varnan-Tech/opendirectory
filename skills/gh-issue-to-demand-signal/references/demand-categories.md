# Demand Categories Reference

Used by SKILL.md Step 5 to guide AI classification of GitHub issues into one of 6 demand categories.

---

## The 6 Categories

### feature_gap

**What it captures:** Functionality the product does not have yet. User is describing something they want to do that is currently impossible.

**Signal phrases:**
- "add support for..."
- "it would be great if..."
- "please add..."
- "feature request:"
- "allow users to..."
- "I wish I could..."
- "would love to see..."

**Examples:**
- "Add support for keyboard shortcuts in the editor"
- "Allow exporting to PDF format"
- "Feature request: dark mode"
- "Support for multiple workspaces per account"

**Scoring note:** feature_gap issues with 20+ reactions represent product roadmap signals. These are the gaps your product can claim as intentional design choices.

---

### bug_pattern

**What it captures:** Recurring broken behavior that erodes user trust. Distinct from a one-off error -- the word "pattern" matters. Multiple issues with similar titles indicate a systemic problem.

**Signal phrases:**
- "broken when..."
- "not working..."
- "fails to..."
- "error when..."
- "crashes if..."
- "regression in..."
- "breaks after..."

**Examples:**
- "Login fails when using SSO with Google"
- "File upload crashes on files over 10MB"
- "Pagination breaks on mobile"
- "Notifications not sending after the latest update"

**Scoring note:** Bug patterns with high reactions signal trust erosion. If a competitor has 5+ high-reaction bug issues in the same functional area, that area is a liability in their product positioning.

---

### ux_complaint

**What it captures:** Friction, confusion, or workflow problems. The feature exists but it is hard to use, hard to find, or does not match how users actually work.

**Signal phrases:**
- "confusing..."
- "hard to..."
- "unclear how to..."
- "should be easier to..."
- "the UI for X is..."
- "annoying that..."
- "clunky..."
- "why does X require..."

**Examples:**
- "Confusing navigation between projects"
- "Hard to find the settings for notifications"
- "Should be easier to bulk-edit items"
- "The import flow has too many steps"

**Scoring note:** UX complaints are positioning gold. "Confusing to use" is a contrast you can own directly. If their users are calling something confusing, your messaging can address that exact friction without naming the competitor.

---

### performance

**What it captures:** Slowness, timeouts, resource usage, or reliability problems that degrade the experience even when the feature works correctly.

**Signal phrases:**
- "slow..."
- "timeout..."
- "takes too long..."
- "high memory usage..."
- "performance regression..."
- "loading forever..."
- "lags when..."
- "CPU usage..."

**Examples:**
- "Search is slow on repos with 1000+ files"
- "Dashboard takes 10+ seconds to load"
- "Memory usage spikes when processing large files"
- "Build times increased 3x after v2.0"

**Scoring note:** Performance issues cluster by data size or scale. If the complaints mention large repos, large teams, or high-volume usage, the competitor has a scale ceiling. That ceiling is your advantage if you have solved it.

---

### integration_missing

**What it captures:** Requests to connect with other tools, APIs, or platforms. Users want the product to work alongside something else in their stack.

**Signal phrases:**
- "integrate with..."
- "support for [tool name]..."
- "webhook..."
- "API for..."
- "connect to..."
- "import from..."
- "sync with..."
- "plugin for..."

**Examples:**
- "Integrate with Slack for notifications"
- "Support GitHub Actions webhook triggers"
- "Add Zapier integration"
- "Import from Notion"
- "VS Code extension"

**Scoring note:** Integration requests cluster around the tools their users already use. A high-reaction integration request tells you where their users spend the rest of their day. If you already have that integration, it is a direct switch argument.

---

### docs_missing

**What it captures:** Confusion caused by absent, incomplete, or incorrect documentation. The product may work correctly, but users cannot figure out how to use it.

**Signal phrases:**
- "no documentation for..."
- "docs are missing..."
- "unclear how to..."
- "example for..."
- "how do I..."
- "docs don't explain..."
- "add docs for..."
- "tutorial for..."

**Examples:**
- "No documentation for the webhook authentication flow"
- "Missing example for advanced configuration"
- "How do I set up custom domains? Docs don't cover this."
- "Add a tutorial for migrating from v1 to v2"

**Scoring note:** docs_missing issues often indicate a product that has grown faster than its documentation. High-reaction docs issues in a specific area indicate that the area is both important to users and opaque in practice.

---

## Classification Rules

### One category per issue
Every issue gets exactly one category. Use the primary pain, not all possible interpretations.

- "The export feature is broken and also slow" -- classify as `bug_pattern` (primary pain: it does not work)
- "Export to PDF is slow" -- classify as `performance` (it works, it is just slow)
- "Add export to PDF" -- classify as `feature_gap` (it does not exist)

### When to use ux_complaint vs docs_missing
- If the user says "I can't figure out how to X" and the docs don't cover it: `docs_missing`
- If the user says "X is confusing" or "X is hard to use" and the feature exists: `ux_complaint`
- If both apply: `ux_complaint` (the UI is the product, the docs are secondary)

### When to use bug_pattern vs performance
- If it does not work at all: `bug_pattern`
- If it works but is slow or resource-heavy: `performance`

---

## Category Demand Signal Interpretation

| Category | What high demand here tells you |
|---|---|
| feature_gap | Their roadmap is behind their users. Name what you have built. |
| bug_pattern | Trust erosion in a specific area. Position your reliability there. |
| ux_complaint | Their users are struggling. Position your simplicity there. |
| performance | They hit a scale ceiling. Position your throughput or response time. |
| integration_missing | Their users live in a different stack. Show your integration depth. |
| docs_missing | They ship but do not explain. Position your onboarding and support. |
