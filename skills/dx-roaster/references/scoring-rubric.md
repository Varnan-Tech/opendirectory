# DX Scoring Rubric

Each dimension scored 0–10. Total: 100. Convert to letter grade: A (90+), B (75–89), C (60–74), D (40–59), F (<40).

---

## 1. Time-to-first-success (0–10)

Measures how fast a new user goes from finding the repo to seeing it work.

| Score | Signal |
|---|---|
| 10 | One command, runs in <30s, no auth/keys/config |
| 7 | One command, <2 min, optional minor config |
| 5 | 2–3 steps, dependencies clearly listed |
| 3 | 4+ steps OR unclear dep versions OR external service required |
| 0 | No install instructions, or instructions don't work |

Probe: extract install block(s) from README. Count distinct commands. Flag any "see docs" detours.

---

## 2. What-is-this clarity (0–10)

Can a stranger understand the project in 5 seconds?

| Score | Signal |
|---|---|
| 10 | Tagline within first 3 lines, gif/screenshot within first 10 lines |
| 7 | Clear one-paragraph description in first 20 lines |
| 5 | Description present but buried after badges/TOC |
| 3 | Vague description ("a tool for X things") |
| 0 | No description, or only badges + install |

Probe: read first 30 lines of README. Find tagline. Check if a tester would understand the value prop without scrolling.

---

## 3. Visual proof (0–10)

| Score | Signal |
|---|---|
| 10 | Hero video (mp4/gif) within first 50 lines AND additional screenshots in body |
| 7 | Hero gif/screenshot within first 50 lines |
| 4 | Some screenshot present but below the fold |
| 0 | No images at all |

Probe: count `![]()` and `<img>` and `<video>` tags in README. Note positions.

---

## 4. Install simplicity (0–10)

| Score | Signal |
|---|---|
| 10 | Single command, copy-pasteable: `npx X` / `pip install X` / `cargo install X` / `brew install X` |
| 7 | 2 commands max (e.g., clone + install) |
| 4 | Multi-platform install matrix (Mac/Linux/Windows separated) |
| 0 | Build from source required without binaries |

Probe: extract install code blocks. Count lines. Detect platform forks.

---

## 5. Runnable quick-start (0–10)

| Score | Signal |
|---|---|
| 10 | Working code example below install, copy-paste produces visible output |
| 7 | Code example present but requires minor tweaks (e.g., your API key) |
| 4 | Pseudo-code or partial snippet |
| 0 | No quick-start example |

Probe: scan README for first code block after install. Test mental copy-paste — would this run on a clean machine?

---

## 6. Documentation depth (0–10)

| Score | Signal |
|---|---|
| 10 | Linked external docs site + `docs/` folder + API reference |
| 7 | Either external docs site OR rich `docs/` folder |
| 5 | README is comprehensive (>500 lines, multiple sections) |
| 3 | Light README (<200 lines), no docs/ |
| 0 | No documentation beyond install |

Probe: check for `docs/` folder, look for "docs" / "documentation" link in README, measure README depth.

---

## 7. Examples (0–10)

| Score | Signal |
|---|---|
| 10 | `examples/` folder with 3+ working examples |
| 7 | `examples/` folder with 1–2 working examples |
| 4 | Inline examples only |
| 0 | No examples |

Probe: check for `examples/`, `samples/`, `cookbook/`. List contents.

---

## 8. Community signals (0–10)

| Score | Signal |
|---|---|
| 10 | CONTRIBUTING.md + CODE_OF_CONDUCT.md + issue/PR templates + Discord/Slack link |
| 7 | CONTRIBUTING.md + at least one community channel |
| 4 | One community file present |
| 0 | No community files |

Probe: check for files at root and in `.github/`. Look for Discord/Slack/community in README.

---

## 9. Trust signals (0–10)

| Score | Signal |
|---|---|
| 10 | LICENSE + active CI badges (passing) + recent commits (<14 days) + multiple contributors |
| 7 | License + recent activity + some badges |
| 4 | License only, dormant repo |
| 0 | No license, dead repo (>180 days) |

Probe: file system for LICENSE, `gh` for commit recency + contributors + CI status.

---

## 10. Marketing signals (0–10)

| Score | Signal |
|---|---|
| 10 | One-line tagline + homepage URL + Twitter/X + Discord + npm/pypi badges + star count visible |
| 7 | Tagline + homepage + at least one social link |
| 4 | Either homepage OR social link |
| 0 | None |

Probe: check `package.json` / `pyproject.toml` for `homepage`, scan README for social links, check badges.

---

## Grade conversion

| Total | Grade | Verdict |
|---|---|---|
| 90–100 | A | Reference-quality DX. Other repos study this. |
| 75–89 | B | Good DX. Minor friction points. |
| 60–74 | C | Average. Multiple friction points slowing adoption. |
| 40–59 | D | Poor. Most users bounce before activation. |
| <40 | F | Hostile to new users. Dies on launch day. |
