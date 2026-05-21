# Changelog Format Reference

## Entry Structure

```markdown
## Week of April 23, 2026

### New
- **Feature name** -- One sentence describing what users can now do.

### Improved
- **Feature name** -- One sentence describing how the experience changed.

### Fixed
- **Feature name** -- One sentence describing what was broken and now works.

### Under the hood
- **Component** -- One sentence for developer-relevant changes only.

---
```

The `---` separator goes at the bottom of each entry. Entries are prepended, so the most recent is always at the top of the file.

## Category Decision Rules

**New**: Use when the change adds net-new capability a user could not do before.
- New page, new API endpoint, new integration, new toggle, new export format
- If in doubt: can users do something they couldn't do yesterday? -> New

**Improved**: Use when an existing feature is made faster, easier, more reliable, or more capable.
- "Now 40% faster", "Works on mobile", "Added bulk actions to existing list view"
- Performance improvements that users will notice -> Improved
- Security patches the user doesn't see -> Under the hood

**Fixed**: Something was broken and now works. Bug reports, regression fixes, crash fixes.
- Prefer specificity: "Fixed: CSV exports no longer drop the last row"
- If the user never knew it was broken, it can be Improved or omitted

**Under the hood**: Infrastructure, dependency updates, refactoring, build changes.
- Include only if developer-relevant: API changes, breaking changes, new environment requirements
- Omit if the user wouldn't care
- Never pad this section -- empty is fine

## Version Label Rules

**Default (date-based):**
- `Week of [Month Day, Year]` -- e.g., "Week of April 23, 2026"
- Use when no semver is detected in existing changelog and user didn't specify

**Semver (auto-detected):**
- If existing changelog headings match `v1.2.3` or `1.2.3` format -> use semver
- Patch bump (x.x.+1): only if all changes are Fixed
- Minor bump (x.+1.0): if any New feature is included
- Show the bumped version: `v1.4.0`

**Custom override:**
- If user says "call it 'The Speed Update'" or "v2.1.0" -> use exactly that
- Do not auto-format custom labels

## Transformation Examples

| Raw (commit/PR) | User-facing (changelog) |
|---|---|
| `Fix memory leak in worker process` | **Worker stability** -- The app no longer slows down after extended use |
| `Add CSV export to reports page` | **Export reports** -- Download any report as a CSV from the Reports page |
| `Improve query performance with index` | **Faster search** -- Search results now load in under half a second |
| `Add dark mode toggle in Settings` | **Dark mode** -- Toggle it in Settings > Appearance. Works across all views |
| `Fix timezone bug in scheduler` | **Scheduler** -- Events no longer fire an hour early in non-UTC timezones |
| `Update dependencies to latest` | (omit -- not user-relevant) |
| `Refactor auth middleware` | (omit unless breaking change) |
| `Add rate limiting to API` | **API rate limits** -- Documented in the API reference. 1000 req/min per key |
| `Fix login page slow on mobile` | **Mobile login** -- The login page now loads instantly on mobile devices |
| `Migrate to Postgres 16` | **Database upgrade** -- Postgres 16 with improved connection pooling |

## What to Omit

- Test file changes
- CI/CD pipeline changes
- Dependency bumps (unless security-relevant)
- Documentation-only commits
- Version bump commits
- Merge commits
- Commit messages under 8 characters

## Item Format

```
**[Feature name]** -- [one sentence benefit, no jargon]
```

- Feature name: 1-3 words, title case, no verbs ("Dark mode" not "Added dark mode")
- Benefit: past tense ("Added", "Fixed", "Improved")
- No period at end
- No nested bullets
- No links (links belong in the full changelog page, not the entry)
