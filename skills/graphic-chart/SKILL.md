---
name: graphic-chart
description: Generates data visualization charts (bar, line, area, pie, doughnut, scatter, radar, treemap) as PNG using Apache ECharts v6. 1080×1080px default, 5 style presets, highlight annotations. Trigger when user says "create a chart", "visualize data", "make a bar chart", "line graph", "pie chart", "data visualization", "chart this data", "plot", "graph", or "visualize these numbers".
compatibility: [claude-code, gemini-cli, github-copilot]
author: OpenDirectory
version: 2.0.0
---

# graphic-chart

Generates data visualization charts as PNG. Renders HTML with Apache ECharts v6 in headless Chromium via Playwright → screenshots at 2× retina quality.

CDN: `https://cdn.jsdelivr.net/npm/echarts@6.0.0/dist/echarts.min.js`

---

## Critical Rules (read before every generation)

1. **`area` type → `type: 'line'` + `areaStyle: {}`** — ECharts has no `type: 'area'`.
2. **`doughnut` → `type: 'pie'` + `radius: ['40%', '70%']`** — ECharts has no `type: 'doughnut'`.
3. **Readiness signal: register `chart.on('finished', fn)` BEFORE `chart.setOption()`** — ECharts bug #14101/#17500: if listener is registered after setOption, it silently never fires. Always register both `finished` and `rendered` events before setOption.
4. **`xAxis.type: 'category'` must be explicit** — ECharts does not infer it from the data. Forgetting this produces a blank chart.
5. **Category labels go in `xAxis.data`**, not in a `data.labels` array. ECharts structure is flat: `{ xAxis, yAxis, series, grid, title, legend }` — not nested under `data` or `options`.
6. **Data labels are fully built-in** — use `label: { show: true }` on any series. No plugin needed.
7. **Highlight a specific bar/point via per-item `itemStyle`** — put `{ value: N, itemStyle: { color: '#...' } }` directly in the `data` array. Do NOT use Chart.js-style `backgroundColor` arrays.
8. **ECharts init uses a `<div>` container, not `<canvas>`** — `echarts.init(document.getElementById('chart'))`. The container div needs explicit dimensions.
9. **`animation: false` in option** — disables animation for instant render. Still register `finished` + `rendered` events before setOption for the readiness signal.
10. **Never dump HTML in chat.** Save to file, show summary only.
11. **Title states the insight, not the subject.** "Revenue grew 3× in 12 months" not "Monthly Revenue".
12. **Pie/doughnut: use body `padding: 64px 80px` and `.chart-container { max-height: 860px }`** — prevents edge-to-edge fill when no title.

---

## Step 1: Intake

**Required:** `chart_type`, `data`

**Optional parameters and defaults:**

| Parameter | Default | Description |
|---|---|---|
| chart_type | — | bar / line / area / pie / doughnut / scatter / radar / treemap |
| data | — | JSON array or CSV — required |
| title | — | States the insight, ≤10 words |
| subtitle | — | 1-sentence context line |
| style | clean-slate | clean-slate / midnight-editorial / matt-gray / electric-burst / brutalist |
| dimensions | 1080x1080 | WxH pixels (output PNG = 2× via deviceScaleFactor) |
| x_label | — | X-axis label text |
| y_label | — | Y-axis label text |
| source | — | Data source shown in footer |
| highlight | — | Data label to highlight (e.g. "Q4", "Dec", index 3) |

**If `chart_type` or `data` is missing, ask exactly:**

> "To create the chart, I need:
> 1. **Chart type** — bar / line / area / pie / doughnut / scatter / radar / treemap
> 2. **Data** — provide as JSON array or CSV (e.g. `[12, 18, 22, 25, 31]` with labels `['Q1','Q2','Q3','Q4','Q5']`)
>
> Optional: title, style (default: clean-slate), dimensions (default: 1080×1080), highlight a specific data point"

If both present → skip to Step 2.

---

## Step 2: Internal Architecture (never shown to user)

**1. Normalize chart type:**
- `area` → `line` + `areaStyle: {}` on series
- `doughnut` → `pie` + `radius: ['40%', '70%']` on series
- `horizontal bar` → `bar` + swap xAxis/yAxis (category axis on y)
- All others: use as-is

**2. Read `references/chart-library.md`** — load full config spec for this chart type.

**3. Read `references/style-presets.md`** — load CSS tokens + data palette for chosen style.

**4. Commit to design direction:**

| Decision | Derive from |
|---|---|
| Tone | Professional / editorial / bold / technical — match the data's audience |
| Data story | Single insight this chart proves (becomes the title) |
| Highlight strategy | Which data point needs visual emphasis and why? |
| Background | Light (clean-slate, matt-gray) or dark (midnight-editorial, electric-burst, brutalist) |

**5. Parse data:**
- Simple array `[12, 18, 22]` → series.data, labels provided separately
- Object array `[{x: 'Jan', y: 12}]` → xAxis.data from x keys, series.data from y values
- CSV: parse header row as xAxis.data, value row as series.data
- Multi-series: multiple `series` entries each with `type`, `name`, `data`
- Scatter: `series.data: [[x1,y1], [x2,y2], ...]` format

**6. Parse dimensions:** `"1080x1080"` → W=1080, H=1080. Body = WxH. Output PNG = 2W × 2H.

---

## Step 3: HTML Generation

Read ALL before generating:
- `references/chart-library.md` for this chart type's full ECharts config spec
- `references/style-presets.md` for the chosen style's CSS tokens + palette

**Required HTML structure:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
[font CDN link from style preset]
<style>
:root {
  [all CSS tokens from style preset]
}

*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
html, body {
  width: [W]px; height: [H]px;
  overflow: hidden;
  background: var(--bg);
  font-family: var(--font-body);
}
body {
  display: flex;
  flex-direction: column;
  padding: 40px 48px 32px;   /* pie/doughnut: use 64px 80px */
}

/* ECharts container must have explicit size */
.chart-container {
  flex: 1;
  min-height: 0;
  /* pie/doughnut only: max-height: 860px; */
}

.chart-header { margin-bottom: 24px; }
.chart-title {
  font-family: var(--font-display);
  font-size: clamp(1.1rem, 2.5vw, 1.6rem);
  font-weight: 700;
  color: var(--text);
  line-height: 1.2;
}
.chart-subtitle {
  font-family: var(--font-body);
  font-size: clamp(0.75rem, 1.2vw, 0.9rem);
  color: var(--text-muted);
  margin-top: 6px;
  line-height: 1.5;
}
.chart-footer {
  margin-top: 14px;
  font-family: var(--font-body);
  font-size: 10px;
  color: var(--text-muted);
  opacity: 0.65;
}
</style>
</head>
<body>

[if title or subtitle: <div class="chart-header"><div class="chart-title">...</div>...</div>]

<div id="chart" class="chart-container"></div>

[if source: <div class="chart-footer">Source: [source]</div>]

<script src="https://cdn.jsdelivr.net/npm/echarts@6.0.0/dist/echarts.min.js"></script>

<script>
window.__chartReady = false;

document.fonts.ready.then(() => {
  const container = document.getElementById('chart');
  const chart = echarts.init(container, null, { renderer: 'canvas' });

  // CRITICAL: register events BEFORE setOption — ECharts bug #14101/#17500
  // 'finished' may silently not fire if registered after setOption with animation:false
  chart.on('finished', () => {
    window.__chartReady = true;
  });
  // Belt-and-suspenders fallback via 'rendered'
  chart.on('rendered', () => {
    clearTimeout(window.__renderDebounce);
    window.__renderDebounce = setTimeout(() => { window.__chartReady = true; }, 100);
  });

  const palette = [palette from style preset];

  const option = {
    animation: false,                            // instant render for screenshot

    backgroundColor: 'transparent',             // body CSS handles bg color

    textStyle: {
      fontFamily: '[--font-body value]',
      color: '[--text-muted value]',
    },

    [title config if title param provided],
    [legend config per chart type],
    [grid config per chart type],
    [xAxis config per chart type],
    [yAxis config per chart type],

    series: [{
      [full series config from chart-library.md for this type]
      [palette colors applied per chart type]
      [if highlight: per-item itemStyle on the highlighted data point]
    }]
  };

  chart.setOption(option);   // setOption ALWAYS comes after event registration
});
</script>
</body>
</html>
```

**Design quality rules:**
- Title font: `fontWeight: 'bold'`, `fontSize: 20–24` — no thin titles
- Grid lines: low opacity (0.06–0.10) — subordinate to data
- Bars: `barMaxWidth: 60`, rounded via `itemStyle.borderRadius: [4,4,0,0]`
- Lines: `smooth: true` for natural curves, `symbolSize: 8` for points
- Pie/doughnut: `label.formatter: '{b}\n{d}%'` for built-in on-slice labels
- Dark presets: grid `rgba(255,255,255,0.07)`, axis line/tick color `rgba(255,255,255,0.15)`
- Tooltip: `show: false` — static PNG, no hover interaction
- When no title provided: skip `.chart-header`, omit title from ECharts option

---

## Step 4: Self-QA (fix every failure before Step 5)

**Structure:**
- [ ] Container is a `<div>`, not `<canvas>`
- [ ] `window.__chartReady = false` declared before `document.fonts.ready`
- [ ] `chart.on('finished', ...)` registered BEFORE `chart.setOption()`
- [ ] `chart.on('rendered', ...)` debounce fallback registered BEFORE `chart.setOption()`
- [ ] `animation: false` in option object
- [ ] `chart.setOption(option)` is the LAST call in the init block

**Type-specific:**
- [ ] Area: `type: 'line'` + `areaStyle: {}` — no `type: 'area'`
- [ ] Doughnut: `type: 'pie'` + `radius: ['40%', '70%']` — no `type: 'doughnut'`
- [ ] Bar: `xAxis.type: 'category'` explicitly set
- [ ] Category data in `xAxis.data` (not `data.labels`)
- [ ] Pie/doughnut: body `padding: 64px 80px` + `.chart-container { max-height: 860px }`
- [ ] Highlight: per-item `{ value: N, itemStyle: { color } }` in data array

**Design:**
- [ ] All palette colors from `references/style-presets.md`
- [ ] Title states insight (not just subject)
- [ ] `tooltip: { show: false }` or omitted (no hover on static PNG)
- [ ] Dark preset: grid/axis colors use `rgba(255,255,255,...)`
- [ ] Source in footer if `source` param provided
- [ ] Data labels visible (built-in `label: { show: true }` on series)

---

## Step 5: Export

Determine slug from title or chart type + data context (kebab-case, ≤30 chars):
```bash
mkdir -p chart/[slug]
```

Save HTML: `chart/[slug]/chart.html`

Quick browser check:
```bash
open chart/[slug]/chart.html
```

Run export (replace `[skill-root]` with actual path to this skill's directory):
```bash
bash [skill-root]/scripts/export-chart.sh \
  chart/[slug]/chart.html \
  chart/[slug]/chart.png \
  --width [W] \
  --height [H]
```

The script installs Playwright on first run (~200MB Chromium download), then captures the chart at `deviceScaleFactor: 2`.

---

## Step 6: Output Summary

```
## Chart: [title]
Date: [YYYY-MM-DD] | Type: [chart_type] | Style: [style]
Dimensions: [W×H]px → PNG: [2W×2H]px @2× retina

Files
  Source:   chart/[slug]/chart.html
  Output:   chart/[slug]/chart.png
  Size:     [X] KB

Checklist
- [ ] Title states the insight clearly
- [ ] Data labels legible at display size
- [ ] Highlight visible on correct data point
- [ ] Source attribution present in footer
```

---

## Prompt Tips (show when user asks for guidance)

> "Provide structured data — JSON or CSV, not prose descriptions."
>
> "Name the chart type explicitly. 'bar chart comparing Q1–Q4' not 'a chart showing quarters'."
>
> "Specify the data story. 'highlight Q4 which outperformed all others' gives the annotation context."
>
> ✅ Good: "Create a line chart. Title: 'From $12k to $95k ARR in 12 Months'. Data: [12, 18, 22, 25, 31, 38, 44, 52, 61, 68, 78, 95] (Jan–Dec 2024). Highlight December. Source: Internal CRM. Style: electric-burst."
>
> ❌ Bad: "make a chart about our company growth"
