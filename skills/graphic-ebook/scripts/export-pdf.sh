#!/usr/bin/env bash
# export-pdf.sh — Export an HTML presentation to PDF
#
# Usage:
#   bash scripts/export-pdf.sh <path-to-html> [output.pdf]
#
# Examples:
#   bash scripts/export-pdf.sh ./my-deck/index.html
#   bash scripts/export-pdf.sh ./presentation.html ./presentation.pdf
#
# What this does:
#   1. Starts a local server to serve the HTML (fonts and assets need HTTP)
#   2. Uses Playwright to screenshot each slide at 1920x1080
#   3. Combines all screenshots into a single PDF
#   4. Cleans up the server and temp files
#
# The PDF preserves colors, fonts, and layout — but not animations.
# Perfect for email attachments, printing, or embedding in documents.
set -euo pipefail

# ─── Colors ────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

info()  { echo -e "${CYAN}ℹ${NC} $*"; }
ok()    { echo -e "${GREEN}✓${NC} $*"; }
warn()  { echo -e "${YELLOW}⚠${NC} $*"; }
err()   { echo -e "${RED}✗${NC} $*" >&2; }

# ─── Parse flags ──────────────────────────────────────────

# Default resolution: 1920x1080 (full HD, ~1-2MB per slide)
# Compact resolution: 1280x720 (HD, ~50-70% smaller files)
# Portrait resolution: 1200x1697 (A4 portrait — for case studies and PDFs)
VIEWPORT_W=1920
VIEWPORT_H=1080
COMPACT=false
PORTRAIT=false

POSITIONAL=()
for arg in "$@"; do
    case $arg in
        --compact)
            COMPACT=true
            VIEWPORT_W=1280
            VIEWPORT_H=720
            ;;
        --portrait)
            PORTRAIT=true
            VIEWPORT_W=1200
            VIEWPORT_H=1697
            ;;
        *)
            POSITIONAL+=("$arg")
            ;;
    esac
done
set -- "${POSITIONAL[@]}"

# ─── Input validation ─────────────────────────────────────

if [[ $# -lt 1 ]]; then
    err "Usage: bash scripts/export-pdf.sh <path-to-html> [output.pdf] [--compact|--portrait]"
    err ""
    err "Examples:"
    err "  bash scripts/export-pdf.sh ./my-deck/index.html"
    err "  bash scripts/export-pdf.sh ./presentation.html ./slides.pdf"
    err "  bash scripts/export-pdf.sh ./presentation.html --compact    # smaller file size (1280×720)"
    err "  bash scripts/export-pdf.sh ./case-study/index.html --portrait  # A4 portrait (1200×1697)"
    exit 1
fi

INPUT_HTML="$1"
if [[ ! -f "$INPUT_HTML" ]]; then
    err "File not found: $INPUT_HTML"
    exit 1
fi

# Resolve to absolute path
INPUT_HTML=$(cd "$(dirname "$INPUT_HTML")" && pwd)/$(basename "$INPUT_HTML")

# Output PDF path: use second argument or derive from input name
if [[ $# -ge 2 ]]; then
    OUTPUT_PDF="$2"
else
    OUTPUT_PDF="$(dirname "$INPUT_HTML")/$(basename "$INPUT_HTML" .html).pdf"
fi

# Resolve output to absolute path
OUTPUT_DIR=$(dirname "$OUTPUT_PDF")
mkdir -p "$OUTPUT_DIR"
OUTPUT_PDF="$OUTPUT_DIR/$(basename "$OUTPUT_PDF")"

echo ""
echo -e "${BOLD}╔══════════════════════════════════════╗${NC}"
echo -e "${BOLD}║       Export Slides to PDF            ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════╝${NC}"
echo ""

# ─── Step 1: Check dependencies ───────────────────────────

info "Checking dependencies..."

if ! command -v npx &>/dev/null; then
    err "Node.js is required but not installed."
    err ""
    err "Install Node.js:"
    err "  macOS:   brew install node"
    err "  or visit https://nodejs.org and download the installer"
    exit 1
fi

ok "Node.js found"

# ─── Step 2: Create the export script ─────────────────────

# We use a temporary Node.js script with Playwright to:
# 1. Start a local server (so fonts load correctly)
# 2. Navigate to each slide
# 3. Screenshot each slide at 1920x1080 (16:9 landscape)
# 4. Combine into a single PDF

TEMP_DIR=$(mktemp -d)
TEMP_SCRIPT="$TEMP_DIR/export-slides.mjs"

# Figure out which directory to serve (the folder containing the HTML)
SERVE_DIR=$(dirname "$INPUT_HTML")
HTML_FILENAME=$(basename "$INPUT_HTML")

cat > "$TEMP_SCRIPT" << 'EXPORT_SCRIPT'
// export-slides.mjs — Vector PDF export via Playwright
//
// Uses page.pdf() directly on the live HTML — produces true vector PDF
// with crisp text, real fonts, and CSS backgrounds. No screenshots.

import { chromium } from 'playwright';
import { createServer } from 'http';
import { readFileSync } from 'fs';
import { join, extname } from 'path';

const SERVE_DIR = process.argv[2];
const HTML_FILE = process.argv[3];
const OUTPUT_PDF = process.argv[4];
const VP_WIDTH  = parseInt(process.argv[5]) || 1920;
const VP_HEIGHT = parseInt(process.argv[6]) || 1080;

// ─── Static file server (needed for Google Fonts + relative assets) ──

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
  '.eot':  'application/vnd.ms-fontobject',
};

const server = createServer((req, res) => {
  const decodedUrl = decodeURIComponent(req.url);
  const filePath = join(SERVE_DIR, decodedUrl === '/' ? HTML_FILE : decodedUrl);
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

// ─── Load page ────────────────────────────────────────────

const browser = await chromium.launch();
const page = await browser.newPage({
  viewport: { width: VP_WIDTH, height: VP_HEIGHT },
});

await page.goto(`http://localhost:${port}/`, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(1000);

// Count slides
const slideCount = await page.evaluate(() =>
  document.querySelectorAll('.slide').length
);

console.log(`  Found ${slideCount} slides`);

if (slideCount === 0) {
  console.error('  ERROR: No .slide elements found.');
  console.error('  Make sure your HTML uses <section class="slide"> or <div class="slide">.');
  await browser.close();
  server.close();
  process.exit(1);
}

// ─── Force all animation states to final visible state ────

await page.evaluate(() => {
  // Trigger intersection observer targets
  document.querySelectorAll('.slide').forEach(s => s.classList.add('visible'));
  // Force reveal + stat-item animations to completed state
  document.querySelectorAll('.reveal, .stat-item').forEach(el => {
    el.style.setProperty('opacity', '1', 'important');
    el.style.setProperty('transform', 'none', 'important');
    el.style.setProperty('transition', 'none', 'important');
  });
});

// ─── Inject print layout CSS ──────────────────────────────
// Each .slide becomes exactly one page in the PDF.
// @page sets the physical page size to match the ebook canvas.
// overflow: visible on html/body lets Playwright see all slides.

await page.addStyleTag({ content: `
  @page {
    size: ${VP_WIDTH}px ${VP_HEIGHT}px;
    margin: 0;
  }
  @media print {
    html, body {
      overflow: visible !important;
      height: auto !important;
      width: ${VP_WIDTH}px !important;
      scroll-snap-type: none !important;
    }
    .slide {
      page-break-after: always !important;
      break-after: page !important;
      width: ${VP_WIDTH}px !important;
      height: ${VP_HEIGHT}px !important;
      min-height: ${VP_HEIGHT}px !important;
      max-height: ${VP_HEIGHT}px !important;
      overflow: hidden !important;
      position: relative !important;
      display: block !important;
      scroll-snap-align: none !important;
    }
    .slide:last-child {
      page-break-after: auto !important;
      break-after: auto !important;
    }
  }
` });

await page.waitForTimeout(200);

// ─── Export as vector PDF ─────────────────────────────────
// page.pdf() renders the live DOM — text stays as vectors,
// fonts stay as fonts, backgrounds render via printBackground.

console.log(`  Generating vector PDF...`);

await page.pdf({
  path: OUTPUT_PDF,
  width:  `${VP_WIDTH}px`,
  height: `${VP_HEIGHT}px`,
  printBackground: true,
  margin: { top: 0, right: 0, bottom: 0, left: 0 },
});

await browser.close();
server.close();

console.log(`  ✓ PDF saved to: ${OUTPUT_PDF}`);
EXPORT_SCRIPT

# ─── Step 3: Install Playwright in temp directory ──────────
# We install Playwright locally in the temp dir so the Node script can import it.
# This avoids polluting global packages and ensures the script is self-contained.

info "Setting up Playwright (headless browser for screenshots)..."
info "This may take a moment on first run..."
echo ""

cd "$TEMP_DIR"

# Create a minimal package.json so npm install works
cat > "$TEMP_DIR/package.json" << 'PKG'
{ "name": "slide-export", "private": true, "type": "module" }
PKG

# Install Playwright into the temp directory
npm install playwright &>/dev/null || {
    err "Failed to install Playwright."
    err "Try running: npm install playwright"
    rm -rf "$TEMP_DIR"
    exit 1
}

# Ensure Chromium browser binary is downloaded
npx playwright install chromium 2>/dev/null || {
    err "Failed to install Chromium browser for Playwright."
    err "Try running manually: npx playwright install chromium"
    rm -rf "$TEMP_DIR"
    exit 1
}
ok "Playwright ready"
echo ""

# ─── Step 4: Run the export ───────────────────────────────

info "Exporting slides to PDF..."
echo ""

if [[ "$COMPACT" == "true" ]]; then
    info "Using compact mode (1280×720) for smaller file size"
fi
if [[ "$PORTRAIT" == "true" ]]; then
    info "Using portrait mode (1200×1697) — A4 portrait format"
fi

node "$TEMP_SCRIPT" "$SERVE_DIR" "$HTML_FILENAME" "$OUTPUT_PDF" "$VIEWPORT_W" "$VIEWPORT_H" || {
    err "PDF export failed."
    rm -rf "$TEMP_DIR"
    exit 1
}

# ─── Step 5: Cleanup and success ──────────────────────────

rm -rf "$TEMP_DIR"

echo ""
echo -e "${BOLD}════════════════════════════════════════${NC}"
ok "PDF exported successfully!"
echo ""
echo -e "  ${BOLD}File:${NC}  $OUTPUT_PDF"
echo ""
FILE_SIZE=$(du -h "$OUTPUT_PDF" | cut -f1 | xargs)
echo "  Size: $FILE_SIZE"
echo ""
echo "  This PDF works everywhere — email, Slack, Notion, print."
echo "  Note: Animations are not preserved (it's a static export)."
echo -e "${BOLD}════════════════════════════════════════${NC}"
echo ""

# Open the PDF automatically
if command -v open &>/dev/null; then
    open "$OUTPUT_PDF"
elif command -v xdg-open &>/dev/null; then
    xdg-open "$OUTPUT_PDF"
fi
