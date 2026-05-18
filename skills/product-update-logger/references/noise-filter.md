# Noise Filter Reference

## Commit Patterns to Skip

These regex patterns match commits that should be excluded from the changelog:

```
^Merge (pull request|branch)\b          -- merge commits
^(bump|update) version\b               -- version bumps
^chore[\s:(]                           -- chore commits (chore: ..., chore(...):)
^ci[\s:(]                              -- CI/CD commits
^build[\s:(]                           -- build system commits
^test[\s:(]                            -- test-only commits
^docs[\s:(]                            -- documentation-only commits
^style[\s:(]                           -- formatting/style commits
^fix typo\b                            -- typo fixes
^\s*typo\b                             -- typo commits
^wip\b                                 -- work in progress
^revert\b                              -- reverts (usually indicate something broken)
^Initial commit$                       -- first commit
^init$                                 -- init commits
single-word subject under 8 chars      -- too vague to be useful
```

## Examples: Skip

```
Merge pull request #45 from user/feature-branch     -> skip (merge commit)
Merge branch 'main' into feature                    -> skip (merge commit)
bump version to 1.3.2                               -> skip (version bump)
Update version: 2.0.1                               -> skip (version bump)
chore: update dependencies                          -> skip (chore)
chore(deps): bump lodash to 4.17.21                 -> skip (chore)
ci: fix GitHub Actions workflow                     -> skip (CI)
build: update webpack config                        -> skip (build)
test: add unit tests for auth module                -> skip (test-only)
docs: update README                                 -> skip (docs-only)
style: fix linting errors                           -> skip (style)
fix typo in error message                           -> skip (typo)
wip: experimenting with new approach                -> skip (WIP)
revert "Add experimental feature"                   -> skip (revert)
Initial commit                                      -> skip
Update                                              -> skip (single word, under 8 chars)
Fix                                                 -> skip (single word, under 8 chars)
```

## Examples: Keep

Even vague commits that don't match noise patterns should be kept and passed to the AI for judgment:

```
Update dashboard layout                             -> keep (AI will decide if useful)
Improve error messages for API validation           -> keep
Add dark mode toggle in Settings                    -> keep
Fix timezone bug in scheduler                       -> keep
Refactor authentication flow                        -> keep (even though technical)
Increase connection pool size                       -> keep (performance-relevant)
Add rate limiting to public API endpoints           -> keep (developer-relevant)
Fix off-by-one error in CSV row iterator            -> keep (specific bug)
```

## PR Labels to Skip

These GitHub PR labels indicate noise:

```
documentation
chore
dependencies
ci
test
tests
```

## What the AI Does With Kept Items

The AI (in Step 4 of the skill) has final discretion over:
- Vague commits like "Update dashboard layout" -- may omit if unclear
- "Under the hood" items -- only includes if developer-relevant
- Categorization -- assigns each item to New, Improved, Fixed, or Under the hood

The noise filter's job is to remove obvious non-user-facing commits before they reach the AI. The AI handles the judgment calls.

## The Rule of Thumb

If removing the commit from the list wouldn't confuse a user reading the changelog -- filter it out. If it might represent a real user-visible change (even if described technically) -- keep it and let the AI decide.
