#!/usr/bin/env bash
# export-chart.sh — Screenshot a Chart.js HTML file as a high-quality retina PNG
#
# Usage:
#   bash scripts/export-chart.sh <path-to-html> [output.png] [--width N] [--height N]
#
# Examples:
#   bash scripts/export-chart.sh ./my-chart/chart.html
#   bash scripts/export-chart.sh ./my-chart/chart.html ./chart.png --width 1200 --height 628
#
# What this does:
#   1. Starts a local HTTP server so CDN scripts and fonts load correctly
#   2. Launches headless Chromium at the specified viewport with deviceScaleFactor: 2
#   3. Waits for window.__chartReady === true (set by Chart.js animation.onComplete)
#   4. Takes a PNG screenshot — output is 2× the specified dimensions (retina quality)
#   5. Cleans up temp files and opens the result
#
# Output PNG = 2× viewport size (e.g. 1080×1080 viewport → 2160×2160 PNG)
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
WIDTH=1080
HEIGHT=1080

POSITIONAL=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --width)  WIDTH="$2";  shift 2 ;;
        --height) HEIGHT="$2"; shift 2 ;;
        *)        POSITIONAL+=("$1"); shift ;;
    esac
done
set -- "${POSITIONAL[@]}"

# ─── Input validation ─────────────────────────────────────

if [[ $# -lt 1 ]]; then
    err "Usage: bash scripts/export-chart.sh <path-to-html> [output.png] [--width N] [--height N]"
    err ""
    err "Examples:"
    err "  bash scripts/export-chart.sh ./my-chart/chart.html"
    err "  bash scripts/export-chart.sh ./my-chart/chart.html ./chart.png --width 1200 --height 628"
    exit 1
fi

INPUT_HTML="$1"
if [[ ! -f "$INPUT_HTML" ]]; then
    err "File not found: $INPUT_HTML"
    exit 1
fi

INPUT_HTML=$(cd "$(dirname "$INPUT_HTML")" && pwd)/$(basename "$INPUT_HTML")

if [[ $# -ge 2 ]]; then
    OUTPUT_PNG="$2"
else
    OUTPUT_PNG="$(dirname "$INPUT_HTML")/$(basename "$INPUT_HTML" .html).png"
fi

OUTPUT_DIR=$(dirname "$OUTPUT_PNG")
mkdir -p "$OUTPUT_DIR"
OUTPUT_PNG="$OUTPUT_DIR/$(basename "$OUTPUT_PNG")"

echo ""
echo -e "${BOLD}╔══════════════════════════════════════╗${NC}"
echo -e "${BOLD}║       Export Chart to PNG             ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════╝${NC}"
echo ""
info "Viewport: ${WIDTH}×${HEIGHT}px → PNG output: $((WIDTH*2))×$((HEIGHT*2))px @2× retina"
echo ""

# ─── Step 1: Check Node.js ────────────────────────────────

info "Checking dependencies..."

if ! command -v node &>/dev/null; then
    err "Node.js is required but not installed."
    err ""
    err "Install Node.js:"
    err "  macOS:   brew install node"
    err "  or visit https://nodejs.org and download the installer"
    exit 1
fi

ok "Node.js found ($(node --version))"

# ─── Step 2: Create temp dir + copy screenshot script ─────

TEMP_DIR=$(mktemp -d)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMP_SCRIPT="$TEMP_DIR/screenshot-chart.mjs"
cp "$SCRIPT_DIR/screenshot-chart.mjs" "$TEMP_SCRIPT"

SERVE_DIR=$(dirname "$INPUT_HTML")
HTML_FILENAME=$(basename "$INPUT_HTML")

# ─── Step 3: Install Playwright ───────────────────────────

info "Setting up Playwright (headless Chromium)..."
info "This may take a moment on first run..."
echo ""

cd "$TEMP_DIR"

cat > "$TEMP_DIR/package.json" << 'PKG'
{ "name": "chart-export", "private": true, "type": "module" }
PKG

npm install playwright 2>/dev/null || {
    err "Failed to install Playwright."
    err "Try running: npm install playwright"
    rm -rf "$TEMP_DIR"
    exit 1
}

npx playwright install chromium 2>/dev/null || {
    err "Failed to install Chromium browser for Playwright."
    err "Try running manually: npx playwright install chromium"
    rm -rf "$TEMP_DIR"
    exit 1
}

ok "Playwright ready"
echo ""

# ─── Step 4: Screenshot ───────────────────────────────────

info "Launching headless Chromium and capturing chart..."
echo ""

node "$TEMP_SCRIPT" \
    "$SERVE_DIR" \
    "$HTML_FILENAME" \
    "$OUTPUT_PNG" \
    "$WIDTH" \
    "$HEIGHT" || {
    err "Chart screenshot failed."
    err ""
    err "Common causes:"
    err "  - window.__chartReady never set (check animation.onComplete in HTML)"
    err "  - Chart.js CDN script failed to load (check internet connection)"
    err "  - HTML syntax error (open in browser to verify)"
    rm -rf "$TEMP_DIR"
    exit 1
}

# ─── Step 5: Cleanup + success ────────────────────────────

rm -rf "$TEMP_DIR"

echo ""
echo -e "${BOLD}════════════════════════════════════════${NC}"
ok "Chart exported successfully!"
echo ""
echo -e "  ${BOLD}File:${NC}  $OUTPUT_PNG"
echo ""
FILE_SIZE=$(du -h "$OUTPUT_PNG" | cut -f1 | xargs)
echo "  Size: $FILE_SIZE"
echo "  Dimensions: $((WIDTH*2))×$((HEIGHT*2))px (@2× retina)"
echo ""
echo "  Ready for social, decks, reports, or email."
echo -e "${BOLD}════════════════════════════════════════${NC}"
echo ""

if command -v open &>/dev/null; then
    open "$OUTPUT_PNG"
elif command -v xdg-open &>/dev/null; then
    xdg-open "$OUTPUT_PNG"
fi
