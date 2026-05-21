// capture-frames.mjs — Capture HTML motion graphic as PNG frame sequence
//
// Args: <serve-dir> <html-filename> <frames-dir> <width> <height> <duration-seconds> <fps>
//
// Architecture: JS-driven renderFrame (NOT CSS @keyframes seeking)
//
//   The HTML exposes window.renderFrame(timeMs) — a pure JS function that computes
//   element styles (opacity, transform) directly from the time value. Playwright calls
//   this once per frame. No CSS animation state, no WAAPI seeking, no timing races.
//
//   Why NOT CSS @keyframes + currentTime:
//     Chromium silently ignores anim.currentTime backward seeks on CSS animations.
//     The animation "sticks" at whatever time it was when we injected pause CSS.
//     For long animations (12s) with networkidle wait (8-12s for Google Fonts CDN),
//     the animation finishes BEFORE we can pause it → all frames capture final state.
//
//   The renderFrame approach:
//     - Works for any duration, any seek direction
//     - Fully deterministic — same input → same output
//     - Browser preview also works (rAF loop in the HTML calls renderFrame)
//     - No race conditions with font loading or network timing

import { chromium } from 'playwright';
import { createServer } from 'http';
import { readFileSync, statSync } from 'fs';
import { mkdir } from 'fs/promises';
import { join, extname } from 'path';

const SERVE_DIR   = process.argv[2];
const HTML_FILE   = process.argv[3];
const FRAMES_DIR  = process.argv[4];
const VP_WIDTH    = parseInt(process.argv[5])   || 1080;
const VP_HEIGHT   = parseInt(process.argv[6])   || 1080;
const DURATION_S  = parseFloat(process.argv[7]) || 9;
const FPS         = parseInt(process.argv[8])   || 30;

const DURATION_MS  = DURATION_S * 1000;
const TOTAL_FRAMES = Math.round(DURATION_S * FPS);

// ─── Static file server ───────────────────────────────────────────────────────

const MIME_TYPES = {
  '.html': 'text/html',
  '.css':  'text/css',
  '.js':   'application/javascript',
  '.json': 'application/json',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.jpeg': 'image/jpeg',
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

// ─── Launch browser ───────────────────────────────────────────────────────────

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

const pageErrors = [];
page.on('console', msg => { if (msg.type() === 'error') pageErrors.push(msg.text()); });
page.on('pageerror', err => pageErrors.push(err.message));

// ─── Navigate and wait for ready ─────────────────────────────────────────────
// networkidle is safe now — no CSS animation timing race.
// renderFrame(t) is pure JS math; it doesn't care how long the page took to load.

await page.goto(`http://localhost:${port}/`, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);

console.log('  Waiting for window.__videoReady...');
try {
  await page.waitForFunction(() => window.__videoReady === true, { timeout: 15000 });
} catch {
  const bodyHTML = await page.evaluate(() => document.body.innerHTML.substring(0, 500));
  console.error('  ERROR: window.__videoReady was never set after 15s.');
  if (pageErrors.length > 0) {
    console.error('  Browser console errors:');
    pageErrors.forEach(e => console.error('   ', e));
  }
  console.error('  Ensure your HTML contains:');
  console.error('    window.__videoReady = false;');
  console.error('    document.fonts.ready.then(() => {');
  console.error('      window.renderFrame(0);');
  console.error('      window.__videoReady = true;');
  console.error('    });');
  console.error('  Page body preview:', bodyHTML);
  await browser.close();
  server.close();
  process.exit(1);
}

// Verify renderFrame exists
const hasRenderFrame = await page.evaluate(() => typeof window.renderFrame === 'function');
if (!hasRenderFrame) {
  console.error('  ERROR: window.renderFrame is not a function.');
  console.error('  The HTML must expose window.renderFrame(timeMs) for frame-accurate capture.');
  console.error('  See SKILL.md Step 3 for the required HTML structure.');
  await browser.close();
  server.close();
  process.exit(1);
}

console.log('  window.renderFrame confirmed — ready to capture');

// Stop browser preview rAF loop — it races with Playwright's evaluate/screenshot:
// between renderFrame(t) and screenshot(), rAF fires renderFrame(elapsed) where
// elapsed >> t, overwriting the correct frame state.
await page.evaluate(() => {
  if (typeof window.__stopPreview === 'function') window.__stopPreview();
});
await page.waitForTimeout(100); // drain any in-flight rAF before capture

// ─── Capture frames ───────────────────────────────────────────────────────────

await mkdir(FRAMES_DIR, { recursive: true });

console.log(`  Capturing ${TOTAL_FRAMES} frames (${DURATION_S}s @ ${FPS}fps)...`);

for (let f = 0; f < TOTAL_FRAMES; f++) {
  const ms = (f / FPS) * 1000;

  // Call renderFrame with the exact timestamp for this frame.
  // The function directly sets element styles — no CSS animation state involved.
  // Force synchronous style recalculation so screenshot captures the updated frame.
  await page.evaluate((t) => {
    window.renderFrame(t);
    void document.body.offsetHeight; // Trigger synchronous reflow
  }, ms);

  // One rAF cycle for GPU compositing
  await page.waitForTimeout(16);

  const padded = String(f + 1).padStart(4, '0');
  await page.screenshot({
    path: join(FRAMES_DIR, `frame_${padded}.png`),
    animations: 'disabled',
    clip: { x: 0, y: 0, width: VP_WIDTH, height: VP_HEIGHT },
  });

  if ((f + 1) % FPS === 0 || f === TOTAL_FRAMES - 1) {
    process.stdout.write(`\r  Captured ${f + 1}/${TOTAL_FRAMES} frames`);
  }
}

console.log('');

await browser.close();
server.close();

const firstFrame = join(FRAMES_DIR, 'frame_0001.png');
const frameSizeKB = Math.round(statSync(firstFrame).size / 1024);
console.log(`  ✓ ${TOTAL_FRAMES} frames saved to ${FRAMES_DIR}`);
console.log(`  Frame size: ${frameSizeKB}KB each (${VP_WIDTH * 2}×${VP_HEIGHT * 2}px retina)`);
