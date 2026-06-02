# dx-roaster

Brutally honest developer-experience audit for a GitHub repo. Scores 10 DX dimensions, writes a roast in your chosen tone, ships a prioritized fix list, and sketches what your README could look like.

Use it before Show HN, Product Hunt, npm publish, or any launch where the first five minutes decide whether visitors stay or bounce.

This is not a security scan or a linter. It judges the same thing a stranger would in 30 seconds: can I understand this, install it, and run it?

---

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install dx-roaster --target claude
```

### Option B: Claude Desktop App

<video src="https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c" controls width="100%"></video>

**Step 1: Download the skill from GitHub**

1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

**Step 2: Install in Claude**

1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** button to create a new skill.
4. Choose **Upload a skill**, then drag and drop the `.zip` file or extracted folder.

> **Note:** For some skills, the `SKILL.md` file might be located inside a subfolder. Always upload the specific folder that contains the `SKILL.md` file.

### Option C: Claude Code Native

Run these commands inside Claude Code:

```bash
/plugin marketplace add Varnan-Tech/opendirectory
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

### Option D: Manus AI

<video src="https://www.opendirectory.dev/ManusAI-one-click-installation-demo.webm" controls width="100%"></video>

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fdx-roaster&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## How It Works

1. You point the skill at a repo (local path or GitHub URL) and pick a tone.
2. The agent scans the README, install steps, code samples, docs, examples, badges, community files, license, and recent activity.
3. It scores 10 DX dimensions on a 0–10 scale.
4. It writes four files: a shareable roast, a prioritized fix list, an ideal-README sketch, and raw scores.

The whole thing runs in under a minute. No external services. Read-only on your repo.

---

## The 10 Dimensions

| Dimension | What it measures |
|---|---|
| Time-to-first-success | How fast a new user goes from landing to a working example |
| What-is-this clarity | Whether a stranger gets the value prop in 5 seconds |
| Visual proof | Gif/screenshot/video presence and position |
| Install simplicity | One-command vs. multi-step matrix |
| Runnable quick-start | Whether the example actually works |
| Documentation depth | README, docs/, external docs site |
| Examples | Number and quality of working examples |
| Community signals | CONTRIBUTING.md, CoC, templates, chat link |
| Trust signals | License, CI, recent commits, contributor count |
| Marketing signals | Tagline, homepage, social links, badges |

Total: 100 points. Grades: A (90+), B (75–89), C (60–74), D (40–59), F (<40).

---

## Input Parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| `repo` | Yes | `.` (current dir) | Local path OR `https://github.com/owner/repo` URL |
| `tone` | | `honest` | `brutal` / `honest` / `kind` |
| `output_dir` | | `dx-roast/` | Where to write the 4 output files |
| `compare_to` | | | Optional second repo URL for benchmark comparison |

---

## Tone Reference

| Tone | Voice | Best for |
|---|---|---|
| `brutal` | Battle-scarred CTO. Cutting, dryly funny. Punches the work, not the person. | Shareable Twitter post. Last-resort wake-up call. |
| `honest` | Senior engineer code review. Direct, kind, specific. (default) | Most cases. Internal sharing with the team. |
| `kind` | Encouraging mentor. Specific issues framed as opportunities. | Solo maintainers. First-time OSS authors. |

---

## Output

```
dx-roast/
├── roast.md           # 3–5 paragraph review in your tone
├── action-plan.md     # 5–10 prioritized fixes
├── ideal-readme.md    # Sketch of what your README could be
└── score.json         # Raw scores per dimension
```

The roast is built to be shareable. Tweet an excerpt. Paste in Slack. Forward to your co-founder.

---

## Prompt Examples

Good:
```
Roast my repo. Tone: brutal.
```

Good:
```
DX audit on https://github.com/myorg/mytool. Compare to https://github.com/vercel/next.js.
```

Good:
```
Run dx-roaster on the current directory with tone=kind. Save outputs to ./pre-launch/.
```

Bad:
```
Tell me if my repo is good.
```

(Too vague. The skill needs at minimum a repo path; everything else has good defaults.)

---

## Prompt Tips

Be brave. The brutal tone is funny, but it cuts deep. If you're not ready to read what's wrong with your repo, use `honest` or `kind`.

Share the output. Roasts are designed to be shareable. A grade-D roast posted with the eventual fix is great open-build content.

Run it before launch, not after. The action plan items are typically 5 minutes to 2 hours. Most are doable the night before Show HN.

Compare to one repo, not five. The benchmark feature works best when you pick a single repo whose DX you envy.

---

## Requirements

- Claude Code, Gemini CLI, or GitHub Copilot
- `gh` CLI (only needed if the input is a GitHub URL; not needed for local paths)
- Read access to the target repo (local file system or public GitHub repo)
