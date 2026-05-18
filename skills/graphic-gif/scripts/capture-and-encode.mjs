// capture-and-encode.mjs — Frame-accurate CSS animation capture + GIF assembly
//
// Args: <serve-dir> <html-filename> <output-gif> <duration-ms> <fps> <loop> <width> <height>
//
// How frame seeking works:
//   1. All CSS animations are paused via injected stylesheet
//   2. For each frame timestamp, Web Animations API seeks every animation to that time
//   3. A screenshot is captured after a brief paint-settle wait
//   4. gifenc assembles frames into a GIF with the correct frame delay
//
// Frame count = Math.floor((durationMs / 1000) * fps)
// The final frame at t=durationMs is intentionally EXCLUDED — it would duplicate t=0
// at the loop point, causing a visible stutter.

import { chromium } from 'playwright';
import { createServer } from 'http';
import { readFileSync, writeFileSync } from 'fs';
import { join, extname } from 'path';
import gifencPkg from 'gifenc';
const { GIFEncoder, quantize, applyPalette } = gifencPkg;

const SERVE_DIR    = process.argv[2];
const HTML_FILE    = process.argv[3];
const OUTPUT_GIF   = process.argv[4];
const DURATION_MS  = parseInt(process.argv[5]) || 3000;
const FPS          = parseInt(process.argv[6]) || 12;
const LOOP         = process.argv[7] !== 'false';
const VP_WIDTH     = parseInt(process.argv[8]) || 800;
const VP_HEIGHT    = parseInt(process.argv[9]) || 800;

// ─── Static file server ───────────────────────────────────

const MIME_TYPES = {
  '.html': 'text/html',
  '.css':  'text/css',
  '.js':   'application/javascript',
  '.json': 'application/json',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif':  'image/gif',
  '.svg':  'image/svg+xml',
  '.webp': 'image/webp',
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

// ─── PNG decode helper ────────────────────────────────────
// Try sharp first (fast, C extension), fall back to jimp (pure JS).

async function decodePNG(buffer) {
  try {
    const sharp = (await import('sharp')).default;
    const { data, info } = await sharp(buffer)
      .ensureAlpha()
      .raw()
      .toBuffer({ resolveWithObject: true });
    return { data: new Uint8ClampedArray(data), width: info.width, height: info.height };
  } catch {
    // sharp not available — try jimp
    const Jimp = (await import('jimp')).default;
    const img = await Jimp.read(buffer);
    const { width, height } = img.bitmap;
    // jimp stores RGBA in .bitmap.data
    return { data: new Uint8ClampedArray(img.bitmap.data), width, height };
  }
}

// ─── Launch browser ───────────────────────────────────────

const browser = await chromium.launch();
const page = await browser.newPage({
  viewport: { width: VP_WIDTH, height: VP_HEIGHT },
});

await page.goto(`http://localhost:${port}/`, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(500);

// ─── Pause all animations ─────────────────────────────────
// Critical: must pause before any frames are captured.
// Web Animations API currentTime setting only works reliably when paused.

await page.addStyleTag({ content: `
  *, *::before, *::after {
    animation-play-state: paused !important;
  }
` });

// Allow one repaint cycle after pausing
await page.waitForTimeout(100);

// Check animation count for diagnostics
const animCount = await page.evaluate(() => document.getAnimations().length);
console.log(`  Found ${animCount} CSS animation(s)`);

if (animCount === 0) {
  console.warn('  WARNING: No animations detected. The GIF will be a static image.');
  console.warn('  Check that your HTML has CSS @keyframes animations.');
}

// ─── Calculate frame timing ───────────────────────────────

const frameCount = Math.floor((DURATION_MS / 1000) * FPS);
const frameIntervalMs = DURATION_MS / frameCount;

console.log(`  Capturing ${frameCount} frames (${(frameIntervalMs).toFixed(1)}ms each)`);

// ─── Capture frames ───────────────────────────────────────

const frames = [];

for (let i = 0; i < frameCount; i++) {
  const timeMs = i * frameIntervalMs;

  // Seek all animations to this timestamp
  await page.evaluate((t) => {
    document.getAnimations().forEach(anim => {
      try {
        anim.currentTime = t;
      } catch {
        // Some animations may reject currentTime assignment — ignore
      }
    });
  }, timeMs);

  // Wait for paint to settle (requestAnimationFrame cycle)
  await page.waitForTimeout(40);

  const screenshot = await page.screenshot({
    type: 'png',
    clip: { x: 0, y: 0, width: VP_WIDTH, height: VP_HEIGHT },
  });

  frames.push(screenshot);

  if ((i + 1) % 10 === 0 || i === frameCount - 1) {
    process.stdout.write(`\r  Frame ${i + 1}/${frameCount}`);
  }
}

console.log('');
console.log('  All frames captured');

await browser.close();
server.close();

// ─── Assemble GIF with gifenc ─────────────────────────────

console.log('  Assembling GIF...');

const gif = GIFEncoder();
const frameDelayMs = Math.round(frameIntervalMs);

for (let i = 0; i < frames.length; i++) {
  const { data, width, height } = await decodePNG(frames[i]);

  // Quantize: find optimal palette for this frame
  // 256 colors max for GIF spec; fewer colors = smaller file
  const palette = quantize(data, 256);
  const index = applyPalette(data, palette);

  gif.writeFrame(index, width, height, {
    palette,
    delay: frameDelayMs,    // milliseconds per frame
    repeat: LOOP ? 0 : -1, // 0 = infinite loop, -1 = no loop
  });

  if ((i + 1) % 10 === 0 || i === frames.length - 1) {
    process.stdout.write(`\r  Encoded ${i + 1}/${frames.length} frames`);
  }
}

console.log('');

const output = gif.bytes();
writeFileSync(OUTPUT_GIF, Buffer.from(output));

const sizeKB = Math.round(output.byteLength / 1024);
console.log(`  ✓ GIF saved: ${OUTPUT_GIF} (${sizeKB}KB before optimization)`);
