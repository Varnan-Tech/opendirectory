# graphic-chart

Generate publication-quality data visualization charts as PNG using Chart.js v4. 8 chart types, 5 style presets, annotation highlights.

## Install

```bash
npx "@opendirectory.dev/skills" install graphic-chart --target claude
```

### Manual Install (2 steps)

1. Copy the URL of this skill folder, paste it at [download-directory.github.io](https://download-directory.github.io/), download the zip.
2. Open Claude desktop app → sidebar → **Customize** → **Skills** → **+** → **Upload a skill** → drop the extracted folder.

---

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
