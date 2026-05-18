# Chart Library — graphic-chart (ECharts v6)

8 chart types with full Apache ECharts v6 config specs. Read this before generating HTML in Step 3.

CDN:
```html
<script src="https://cdn.jsdelivr.net/npm/echarts@6.0.0/dist/echarts.min.js"></script>
```

**No plugins needed.** ECharts v6 has built-in data labels, annotations (markPoint/markLine/markArea), and all chart types. No separate CDN scripts.

---

## Universal Init Pattern (apply to ALL chart types)

```javascript
window.__chartReady = false;

document.fonts.ready.then(() => {
  const chart = echarts.init(document.getElementById('chart'), null, { renderer: 'canvas' });

  // CRITICAL: register BEFORE setOption — ECharts bug #14101/#17500
  chart.on('finished', () => { window.__chartReady = true; });
  chart.on('rendered', () => {
    clearTimeout(window.__renderDebounce);
    window.__renderDebounce = setTimeout(() => { window.__chartReady = true; }, 100);
  });

  const option = {
    animation: false,            // instant render for Playwright screenshot
    backgroundColor: 'transparent',
    // ... chart-specific config
  };

  chart.setOption(option);       // ALWAYS last
});
```

---

## ECharts Structure vs Chart.js (LLM trap — read this)

| Concept | Chart.js | ECharts |
|---|---|---|
| Chart structure | `{ type, data: {labels, datasets}, options }` | **Flat:** `{ xAxis, yAxis, series, grid, title, legend }` |
| Category labels | `data.labels: ['Q1','Q2']` | `xAxis: { type: 'category', data: ['Q1','Q2'] }` |
| Series data | `datasets: [{ data: [...] }]` | `series: [{ type: 'bar', data: [...] }]` |
| Highlight bar | `backgroundColor: array` | `data: [{ value: N, itemStyle: { color } }]` per item |
| Doughnut | `type: 'doughnut'` | `type: 'pie'` + `radius: ['40%','70%']` |
| Area | `fill: 'origin'` | `areaStyle: {}` on series |
| Data labels | `chartjs-plugin-datalabels` (external) | `label: { show: true }` built into every series |

---

## 1. bar

```javascript
{
  animation: false,
  backgroundColor: 'transparent',
  grid: {
    left: '8%', right: '8%', top: 80, bottom: 60,
    containLabel: true,
  },
  xAxis: {
    type: 'category',                // REQUIRED — not inferred
    data: ['Q1', 'Q2', 'Q3', 'Q4'],
    axisLine: { lineStyle: { color: 'rgba(255,255,255,0.15)' } },
    axisTick: { show: false },
    axisLabel: {
      color: 'var(--text-muted)',
      fontFamily: 'var(--font-body)',
      fontSize: 14,
    },
  },
  yAxis: {
    type: 'value',
    splitLine: { lineStyle: { color: 'rgba(255,255,255,0.07)' } },
    axisLabel: {
      color: 'var(--text-muted)',
      fontFamily: 'var(--font-body)',
      fontSize: 12,
      formatter: (v) => '$' + v + 'k',   // customize per data
    },
  },
  series: [{
    type: 'bar',
    name: 'Revenue',
    barMaxWidth: 72,
    itemStyle: {
      color: palette[0],
      borderRadius: [4, 4, 0, 0],          // rounded top corners
    },
    // Highlight one bar — per-item override
    data: [
      { value: 420, itemStyle: { color: palette[1], borderRadius: [4,4,0,0] } },
      { value: 510, itemStyle: { color: palette[1], borderRadius: [4,4,0,0] } },
      { value: 480, itemStyle: { color: palette[1], borderRadius: [4,4,0,0] } },
      { value: 780, itemStyle: { color: palette[0], borderRadius: [4,4,0,0] } },  // highlighted
    ],
    // Built-in data label — no plugin
    label: {
      show: false,                          // set true to show value on bar
      position: 'top',
      formatter: '{c}',
      color: 'var(--text)',
      fontFamily: 'var(--font-body)',
      fontSize: 13,
    },
    // Highlight annotation — label above bar with callout
    markPoint: {
      symbol: 'pin',
      symbolSize: 0,                        // hide symbol, show label only
      label: {
        show: true,
        formatter: '$780k',
        backgroundColor: palette[0],
        color: '#000',
        borderRadius: 4,
        padding: [6, 10],
        fontWeight: 'bold',
        fontSize: 13,
      },
      data: [{ coord: ['Q4', 780] }],       // [categoryLabel, value]
    },
  }]
}
```

**Horizontal bar:** Swap axes — put `type: 'category'` on `yAxis`, `type: 'value'` on `xAxis`.

**Multi-series bar:**
```javascript
series: [
  { type: 'bar', name: '2023', data: [...], itemStyle: { color: palette[0], borderRadius: [4,4,0,0] } },
  { type: 'bar', name: '2024', data: [...], itemStyle: { color: palette[1], borderRadius: [4,4,0,0] } },
]
legend: { show: true, bottom: 0, textStyle: { color: 'var(--text)' } }
```

**Stacked bar:** Add `stack: 'total'` on each series.

**Dark vs light grid color:**
- Dark presets: `splitLine: { lineStyle: { color: 'rgba(255,255,255,0.07)' } }`
- Light presets: `splitLine: { lineStyle: { color: 'rgba(0,0,0,0.08)' } }`

---

## 2. line

```javascript
{
  animation: false,
  backgroundColor: 'transparent',
  grid: { left: '8%', right: '8%', top: 80, bottom: 60, containLabel: true },
  xAxis: {
    type: 'category',
    data: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    boundaryGap: false,                   // line starts at first point, not center of band
    axisLine: { lineStyle: { color: 'rgba(255,255,255,0.15)' } },
    axisTick: { show: false },
    axisLabel: { color: 'var(--text-muted)', fontSize: 12 },
  },
  yAxis: {
    type: 'value',
    splitLine: { lineStyle: { color: 'rgba(255,255,255,0.07)' } },
    axisLabel: { color: 'var(--text-muted)', fontSize: 12, formatter: '{value}k' },
  },
  series: [{
    type: 'line',
    name: 'ARR ($k)',
    data: [12, 18, 22, 25, 31, 38, 44, 52, 61, 68, 78, 95],
    smooth: true,                         // natural curve (vs false = straight segments)
    lineStyle: { color: palette[0], width: 2.5 },
    itemStyle: { color: palette[0] },
    symbolSize: 8,
    symbol: 'circle',
    // Highlight specific point (e.g. December)
    markPoint: {
      symbolSize: 0,
      label: {
        show: true,
        formatter: '$95k',
        backgroundColor: palette[0],
        color: '#000',
        borderRadius: 4,
        padding: [6, 10],
        fontWeight: 'bold',
        fontSize: 13,
      },
      data: [{ coord: ['Dec', 95] }],
    },
  }]
}
```

---

## 3. area

**No `type: 'area'` in ECharts — it's `type: 'line'` with `areaStyle`.**

```javascript
series: [{
  type: 'line',                           // NOT 'area'
  smooth: true,
  lineStyle: { color: palette[0], width: 2 },
  itemStyle: { color: palette[0] },
  areaStyle: {                            // THIS is what makes it an area chart
    color: {
      type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
      colorStops: [
        { offset: 0, color: paletteAlpha[0] },    // top: semi-transparent
        { offset: 1, color: 'rgba(0,0,0,0)' },    // bottom: fully transparent
      ]
    }
  },
  data: [5, 8, 12, 10, 15, 22, 28, 25, 32, 38, 45, 52],
  symbolSize: 6,
}]
```

---

## 4. pie

**CRITICAL sizing:** Pie fills 100% of container. Always use body `padding: 64px 80px` and `.chart-container { max-height: 860px }` — see SKILL.md rule #12.

```javascript
{
  animation: false,
  backgroundColor: 'transparent',
  // No xAxis/yAxis for pie
  legend: {
    orient: 'vertical',
    right: '5%',
    top: 'center',
    textStyle: {
      color: 'var(--text)',
      fontFamily: 'var(--font-body)',
      fontSize: 20,                       // 20px = readable at 2× retina output
    },
    itemGap: 20,
    formatter: (name) => {
      // Include % in legend — requires access to data
      return name;                        // customize with data lookup if needed
    },
  },
  series: [{
    type: 'pie',
    radius: '65%',                        // size as % of container
    center: ['42%', '50%'],               // shift left to give legend room
    data: [
      { value: 45, name: 'Product A', itemStyle: { color: palette[0] } },
      { value: 28, name: 'Product B', itemStyle: { color: palette[1] } },
      { value: 17, name: 'Product C', itemStyle: { color: palette[2] } },
      { value: 10, name: 'Other',     itemStyle: { color: palette[3] } },
    ],
    // Built-in labels — no plugin needed
    label: {
      show: true,
      formatter: '{b}\n{d}%',            // name + percentage
      color: '#09090B',                  // dark text on bright palette colors
      fontFamily: 'var(--font-body)',
      fontSize: 18,
      fontWeight: 'bold',
      minMargin: 5,
    },
    labelLine: {
      show: true,
      length: 15,
      length2: 10,
      lineStyle: { color: 'rgba(255,255,255,0.3)' },
    },
    // Hide label on tiny slices (< 12%)
    labelFilter: (params) => params.data.value >= 12,
    itemStyle: { borderColor: 'var(--bg)', borderWidth: 3 },
    emphasis: { scale: true, scaleSize: 6 },
  }]
}
```

**No annotation plugin for pie** — ECharts pie doesn't support markPoint/markLine.

If > 7 segments, consolidate smallest as "Other".

---

## 5. doughnut

Same as pie + `radius: ['40%', '70%']`. No `type: 'doughnut'` in ECharts.

```javascript
series: [{
  type: 'pie',
  radius: ['40%', '68%'],               // [inner, outer] — creates the hole
  center: ['42%', '50%'],
  // All other config same as pie
}]
```

**Optional center label:**
```javascript
// Register as a custom ECharts plugin after chart init:
chart.setOption({
  graphic: [{
    type: 'text',
    left: 'center',
    top: 'center',
    style: {
      text: '73%',
      font: 'bold 32px Inter, sans-serif',
      fill: 'var(--text)',
      textAlign: 'center',
    }
  }]
});
```

---

## 6. scatter

```javascript
{
  animation: false,
  backgroundColor: 'transparent',
  grid: { left: '8%', right: '8%', top: 80, bottom: 60, containLabel: true },
  xAxis: {
    type: 'value',                        // value axis — not category
    splitLine: { lineStyle: { color: 'rgba(255,255,255,0.07)' } },
    axisLabel: { color: 'var(--text-muted)', fontSize: 12 },
  },
  yAxis: {
    type: 'value',
    splitLine: { lineStyle: { color: 'rgba(255,255,255,0.07)' } },
    axisLabel: { color: 'var(--text-muted)', fontSize: 12 },
  },
  series: [{
    type: 'scatter',
    symbolSize: 12,
    itemStyle: { color: palette[0], opacity: 0.85 },
    data: [[1.5, 2.3], [2.0, 3.1], [3.5, 1.8], [4.2, 4.5]],  // [x, y] pairs
    emphasis: { scale: true },
  }]
}
```

Highlight a specific point:
```javascript
data: [
  [1.5, 2.3],
  { value: [4.2, 4.5], itemStyle: { color: palette[0], borderColor: '#fff', borderWidth: 2 } }
]
```

---

## 7. radar

```javascript
{
  animation: false,
  backgroundColor: 'transparent',
  radar: {
    shape: 'circle',                      // or 'polygon'
    indicator: [
      { name: 'Speed',    max: 100 },
      { name: 'Accuracy', max: 100 },
      { name: 'Strength', max: 100 },
      { name: 'Stamina',  max: 100 },
      { name: 'Agility',  max: 100 },
    ],
    radius: '65%',
    center: ['50%', '55%'],
    axisName: { color: 'var(--text)', fontSize: 13 },
    splitLine: { lineStyle: { color: 'rgba(255,255,255,0.12)' } },
    splitArea: { show: false },
    axisLine: { lineStyle: { color: 'rgba(255,255,255,0.15)' } },
  },
  legend: {
    bottom: 0,
    textStyle: { color: 'var(--text)', fontSize: 14 },
  },
  series: [{
    type: 'radar',
    data: [{
      name: 'Team A',
      value: [85, 92, 70, 88, 76],
      lineStyle: { color: palette[0], width: 2 },
      itemStyle: { color: palette[0] },
      areaStyle: { color: paletteAlpha[0] },
    }]
  }]
}
```

---

## 8. treemap

```javascript
{
  animation: false,
  backgroundColor: 'transparent',
  series: [{
    type: 'treemap',
    width: '100%',
    height: '100%',
    roam: false,                          // disable pan/zoom (static PNG)
    nodeClick: false,
    breadcrumb: { show: false },
    label: {
      show: true,
      formatter: '{b}\n{c}',             // name + value
      fontSize: 14,
      fontFamily: 'var(--font-body)',
      color: '#fff',
    },
    itemStyle: {
      borderColor: 'var(--bg)',
      borderWidth: 2,
      gapWidth: 2,
    },
    levels: [{
      itemStyle: { borderWidth: 3, borderColor: 'var(--bg)' },
      upperLabel: { show: false },
    }],
    data: [
      { name: 'Category A', value: 45, itemStyle: { color: palette[0] } },
      { name: 'Category B', value: 28, itemStyle: { color: palette[1] } },
      { name: 'Category C', value: 17, itemStyle: { color: palette[2] } },
      { name: 'Other',       value: 10, itemStyle: { color: palette[3] } },
    ],
  }]
}
```

---

## Highlight Patterns (applies to bar, line, scatter)

**Per-item color highlight (most common):**
```javascript
data: [
  420, 510, 480,
  { value: 780, itemStyle: { color: palette[0], borderRadius: [4,4,0,0] } }  // highlighted
]
```

**MarkPoint callout label above bar:**
```javascript
markPoint: {
  symbolSize: 0,                        // invisible pin, just show the label
  data: [{ coord: ['Q4', 780] }],
  label: {
    show: true,
    formatter: '$780k',
    backgroundColor: palette[0],
    color: '#000',
    fontWeight: 'bold',
    fontSize: 14,
    fontFamily: 'var(--font-body)',
    borderRadius: 4,
    padding: [6, 12],
  },
}
```

**MarkArea background highlight:**
```javascript
markArea: {
  silent: true,
  itemStyle: { color: 'rgba(250,204,21,0.1)', borderColor: 'rgba(250,204,21,0.5)', borderWidth: 1 },
  data: [[{ xAxis: 'Q4' }, { xAxis: 'Q4' }]],
}
```

**MarkLine (average, target, threshold):**
```javascript
markLine: {
  silent: true,
  lineStyle: { type: 'dashed', color: 'rgba(255,255,255,0.4)', width: 1.5 },
  label: { formatter: 'Avg: {c}', color: 'var(--text-muted)' },
  data: [{ type: 'average' }],
}
```
