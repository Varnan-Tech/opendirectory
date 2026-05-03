// screenshot-chart.mjs — Capture an ECharts v6 HTML file as a retina-quality PNG
//
// Args: <serve-dir> <html-filename> <output-png> <width> <height>
//
// How it works:
//   1. Starts a local HTTP server to serve the HTML and allow CDN scripts to load
//   2. Launches Chromium at the specified viewport with deviceScaleFactor: 2
//      → output PNG is 2× viewport dimensions (retina quality)
//   3. Waits for window.__chartReady === true
//      → set by chart.on('finished', ...) in the HTML (registered BEFORE setOption)
//      → belt-and-suspenders: also set by chart.on('rendered', ...) + 100ms debounce
//      → ECharts bug #14101/#17500: 'finished' silently skips if registered after setOption
//   4. Takes the screenshot and saves as PNG
//
// CRITICAL: The HTML must register events BEFORE chart.setOption():
//   chart.on('finished', () => { window.__chartReady = true; });
//   chart.on('rendered', () => { clearTimeout(t); t = setTimeout(() => { window.__chartReady = true; }, 100); });
//   chart.setOption(option);   // setOption LAST

import { chromium } from 'playwright';
import { createServer } from 'http';
import { readFileSync, writeFileSync } from 'fs';
import { join, extname } from 'path';

const SERVE_DIR    = process.argv[2];
const HTML_FILE    = process.argv[3];
const OUTPUT_PNG   = process.argv[4];
const VP_WIDTH     = parseInt(process.argv[5]) || 1080;
const VP_HEIGHT    = parseInt(process.argv[6]) || 1080;

// ─── Static file server ───────────────────────────────────
// Required for CDN scripts and Google Fonts to load via HTTP
// (file:// protocol blocks cross-origin requests)

const MIME_TYPES = {
  '.html': 'text/html',
  '.css':  'text/css',
  '.js':   'application/javascript',
  '.json': 'application/json',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.svg':  'image/svg+xml',
  '.woff': 'font/woff',
  '.woff2':'font/woff2',
  '.ttf':  'font/ttf',
};

const server = createServer((req, res) => {
  const decoded = decodeURIComponent(req.url);
  const filePath = join(SERVE_DIR, decoded === '/' ? HTML_FILE : decoded);
  try {
    const content = readFileSync(filePath);
    const ext = extname(filePath).toLowerCase();
    res.writeHead(200, { 'Content-Type': MIME_TYPES[ext] || 'application/octet-stream' });
    res.end(content);
  } catch {
    res.writeHead(404);
    res.end('Not found');
  }
});

const port = await new Promise((resolve) => {
  server.listen(0, () => resolve(server.address().port));
});

console.log(`  Local server on port ${port}`);

// ─── Launch browser at 2× deviceScaleFactor ──────────────
// deviceScaleFactor: 2 → screenshot is 2× VP dimensions (retina)
// --font-render-hinting=none → sharper text on Linux CI

const browser = await chromium.launch({
  args: [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--font-render-hinting=none',
  ]
});

const context = await browser.newContext({
  viewport: { width: VP_WIDTH, height: VP_HEIGHT },
  deviceScaleFactor: 2,
});

const page = await context.newPage();

// Capture browser console errors for diagnostics
const pageErrors = [];
page.on('console', msg => {
  if (msg.type() === 'error') pageErrors.push(msg.text());
});
page.on('pageerror', err => pageErrors.push(err.message));

// ─── Navigate and wait for chart ─────────────────────────
// Use networkidle to ensure CDN scripts (Chart.js, plugins) finish loading
// before we check window.__chartReady

await page.goto(`http://localhost:${port}/`, { waitUntil: 'networkidle' });

// Wait for fonts (CDN Google Fonts need a moment)
await page.evaluate(() => document.fonts.ready);

// Wait for Chart.js to finish rendering
// window.__chartReady is set by animation.onComplete in the HTML
// Timeout: 15s — generous to allow CDN scripts on slow networks
console.log('  Waiting for chart to render...');
try {
  await page.waitForFunction(() => window.__chartReady === true, { timeout: 15000 });
} catch {
  // Provide a helpful error message
  const bodyHTML = await page.evaluate(() => document.body.innerHTML.substring(0, 500));
  console.error('  ERROR: window.__chartReady was never set after 15s.');
  if (pageErrors.length > 0) {
    console.error('  Browser console errors:');
    pageErrors.forEach(e => console.error('   ', e));
  }
  console.error('  Check that your HTML chart config includes:');
  console.error('    animation: { duration: 0, onComplete: () => { window.__chartReady = true; } }');
  console.error('  If using CDN scripts, verify internet access from the headless browser.');
  console.error('  Page body preview:', bodyHTML);
  await browser.close();
  server.close();
  process.exit(1);
}

console.log('  Chart rendered — taking screenshot');

// ─── Screenshot ───────────────────────────────────────────
// animations: 'disabled' stops CSS transitions — does NOT affect Chart.js canvas
// The canvas is already fully drawn at this point (waited for __chartReady)

await page.screenshot({
  path: OUTPUT_PNG,
  animations: 'disabled',
  clip: { x: 0, y: 0, width: VP_WIDTH, height: VP_HEIGHT },
});

await browser.close();
server.close();

const { statSync } = await import('fs');
const sizeKB = Math.round(statSync(OUTPUT_PNG).size / 1024);
console.log(`  ✓ PNG saved: ${OUTPUT_PNG} (${sizeKB}KB, ${VP_WIDTH * 2}×${VP_HEIGHT * 2}px)`);
