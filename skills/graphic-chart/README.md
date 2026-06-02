# graphic-chart

Generate publication-quality data visualization charts as PNG using Chart.js v4. 8 chart types, 5 style presets, annotation highlights.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install graphic-chart --target claude
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

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fgraphic-chart&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [OpenDirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What it does

- Takes chart type + data (JSON or CSV) as input
- Generates a self-contained HTML file with Chart.js v4
- Screenshots via headless Chromium at 2× deviceScaleFactor (retina quality)
- Outputs a crisp PNG ready for decks, reports, social, or email
- Supports annotation highlights on a specific data point
- No Python, no API key, no external service

---

## Example

> "Create a line chart. Title: 'From $12k to $95k ARR in 12 Months'. Data: [12, 18, 22, 25, 31, 38, 44, 52, 61, 68, 78, 95] (Jan–Dec 2024, in thousands). Highlight December in gold. Source: Internal CRM. Style: electric-burst. Dimensions: 1080x1080."

Output: `chart.png` — dark canvas, electric yellow December highlight with callout, growth title.

---

## Supported Chart Types

| Type | Best for |
|---|---|
| bar | Comparing values across categories |
| line | Trends over time |
| area | Cumulative trends, volume over time |
| pie | Part-to-whole relationships |
| doughnut | Part-to-whole with center hole |
| scatter | Correlations between two variables |
| radar | Multi-dimensional comparisons |
| treemap | Hierarchical data, proportional sizes |

---

## Supported Styles

| Style | Best for |
|---|---|
| clean-slate | Enterprise B2B, investor decks, any professional audience |
| midnight-editorial | Editorial, premium brand, thought leadership |
| matt-gray | Board materials, consultancy reports, sophisticated neutral |
| electric-burst | Growth metrics, startup content, bold data stories |
| brutalist | Design-forward, stark comparisons, confrontational data |

---

## Parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| chart_type | Yes | — | bar / line / area / pie / doughnut / scatter / radar / treemap |
| data | Yes | — | JSON array or CSV |
| title | No | — | States the insight (≤10 words) |
| subtitle | No | — | 1-sentence context line |
| style | No | clean-slate | Visual style preset |
| dimensions | No | 1080x1080 | WxH in pixels |
| x_label | No | — | X-axis label |
| y_label | No | — | Y-axis label |
| source | No | — | Data source for footer attribution |
| highlight | No | — | Data label/value to annotate (e.g. "Q4", "Dec") |

---

## Output

| File | What it is |
|---|---|
| `chart/[slug]/chart.html` | Self-contained HTML (open in browser to preview) |
| `chart/[slug]/chart.png` | PNG at 2× retina quality |

Default output: `1080×1080` viewport → `2160×2160` PNG (@2× deviceScaleFactor).

---

## Dependencies

**Node.js** — required. Install from [nodejs.org](https://nodejs.org) or `brew install node`.

Bundled inside this skill:
- `scripts/export-chart.sh` — orchestrator script
- `scripts/screenshot-chart.mjs` — Playwright capture script

Auto-installed on first run via npm:
- `playwright` — headless Chromium for screenshot
- Chromium browser binary (~200MB, downloaded once and cached)

No API keys required.
