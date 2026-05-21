#!/usr/bin/env bash
# export-gif.sh — Capture CSS animation frames and assemble as a looping GIF
#
# Usage:
#   bash scripts/export-gif.sh <path-to-html> [output.gif] [options]
#
# Options:
#   --duration N      Animation duration in seconds (default: 3.0)
#   --fps N           Frames per second (default: 12)
#   --no-loop         Disable GIF looping (default: loops forever)
#   --optimization    quality | balanced | filesize (default: balanced)
#   --width N         Canvas width in pixels (default: 800)
#   --height N        Canvas height in pixels (default: 800)
#
# Examples:
#   bash scripts/export-gif.sh ./my-anim/animation.html
#   bash scripts/export-gif.sh ./my-anim/animation.html ./output.gif --duration 2 --fps 15
#   bash scripts/export-gif.sh ./my-anim/animation.html --optimization filesize
#
# What this does:
#   1. Launches headless Chromium via Playwright at the specified canvas size
#   2. Injects CSS to pause all animations
#   3. Uses the Web Animations API to seek to each frame timestamp
#   4. Screenshots each frame as PNG
#   5. Assembles frames into a GIF using gifenc
#   6. Runs gifsicle for palette optimization and size reduction
#
# The resulting GIF has crisp, accurate CSS animation — no timing drift.
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
DURATION=3.0
FPS=12
LOOP=true
OPTIMIZATION=balanced
WIDTH=800
HEIGHT=800

POSITIONAL=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --duration)
            DURATION="$2"
            shift 2
            ;;
        --fps)
            FPS="$2"
            shift 2
            ;;
        --no-loop)
            LOOP=false
            shift
            ;;
        --optimization)
            OPTIMIZATION="$2"
            shift 2
            ;;
        --width)
            WIDTH="$2"
            shift 2
            ;;
        --height)
            HEIGHT="$2"
            shift 2
            ;;
        *)
            POSITIONAL+=("$1")
            shift
            ;;
    esac
done
set -- "${POSITIONAL[@]}"

# ─── Input validation ─────────────────────────────────────

if [[ $# -lt 1 ]]; then
    err "Usage: bash scripts/export-gif.sh <path-to-html> [output.gif] [--duration N] [--fps N] [--no-loop] [--optimization quality|balanced|filesize]"
    err ""
    err "Examples:"
    err "  bash scripts/export-gif.sh ./my-anim/animation.html"
    err "  bash scripts/export-gif.sh ./my-anim/animation.html ./output.gif --duration 2 --fps 15"
    err "  bash scripts/export-gif.sh ./my-anim/animation.html --optimization filesize"
    exit 1
fi

INPUT_HTML="$1"
if [[ ! -f "$INPUT_HTML" ]]; then
    err "File not found: $INPUT_HTML"
    exit 1
fi

INPUT_HTML=$(cd "$(dirname "$INPUT_HTML")" && pwd)/$(basename "$INPUT_HTML")

if [[ $# -ge 2 ]]; then
    OUTPUT_GIF="$2"
else
    OUTPUT_GIF="$(dirname "$INPUT_HTML")/$(basename "$INPUT_HTML" .html).gif"
fi

OUTPUT_DIR=$(dirname "$OUTPUT_GIF")
mkdir -p "$OUTPUT_DIR"
OUTPUT_GIF="$OUTPUT_DIR/$(basename "$OUTPUT_GIF")"

# Duration in milliseconds for Node.js script
DURATION_MS=$(echo "$DURATION * 1000" | bc | cut -d. -f1)

echo ""
echo -e "${BOLD}╔══════════════════════════════════════╗${NC}"
echo -e "${BOLD}║       Export Animation to GIF         ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════╝${NC}"
echo ""
info "Animation: ${DURATION}s @ ${FPS}fps → $(echo "$DURATION * $FPS" | bc | cut -d. -f1) frames"
info "Canvas: ${WIDTH}×${HEIGHT}px | Loop: $LOOP | Optimization: $OPTIMIZATION"
echo ""

# ─── Step 1: Check dependencies ───────────────────────────

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

# Check/install gifsicle for optimization
GIFSICLE_AVAILABLE=false
if command -v gifsicle &>/dev/null; then
    GIFSICLE_AVAILABLE=true
    ok "gifsicle found"
else
    warn "gifsicle not found — skipping optimization pass"
    warn "Install for smaller GIFs: brew install gifsicle"
fi

# ─── Step 2: Create the capture+encode script ─────────────

TEMP_DIR=$(mktemp -d)
TEMP_SCRIPT="$TEMP_DIR/capture-and-encode.mjs"

# Get the directory of THIS script so we can find the bundled mjs
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy the bundled capture-and-encode.mjs into the temp dir
cp "$SCRIPT_DIR/capture-and-encode.mjs" "$TEMP_SCRIPT"

SERVE_DIR=$(dirname "$INPUT_HTML")
HTML_FILENAME=$(basename "$INPUT_HTML")

# ─── Step 3: Install dependencies in temp directory ───────

info "Setting up dependencies (gifenc + Playwright)..."
info "This may take a moment on first run..."
echo ""

cd "$TEMP_DIR"

cat > "$TEMP_DIR/package.json" << 'PKG'
{ "name": "gif-export", "private": true, "type": "module" }
PKG

npm install gifenc sharp playwright 2>/dev/null || {
    # sharp is optional (faster PNG decode) — retry without it
    warn "sharp failed to install, falling back to jimp..."
    npm install gifenc jimp playwright 2>/dev/null || {
        err "Failed to install dependencies."
        err "Try running: npm install gifenc playwright"
        rm -rf "$TEMP_DIR"
        exit 1
    }
}

npx playwright install chromium 2>/dev/null || {
    err "Failed to install Chromium browser for Playwright."
    err "Try running manually: npx playwright install chromium"
    rm -rf "$TEMP_DIR"
    exit 1
}
ok "Dependencies ready"
echo ""

# ─── Step 4: Capture frames + assemble GIF ────────────────

info "Capturing ${DURATION}s of animation at ${FPS}fps..."
echo ""

UNOPTIMIZED_GIF="$TEMP_DIR/unoptimized.gif"

node "$TEMP_SCRIPT" \
    "$SERVE_DIR" \
    "$HTML_FILENAME" \
    "$UNOPTIMIZED_GIF" \
    "$DURATION_MS" \
    "$FPS" \
    "$LOOP" \
    "$WIDTH" \
    "$HEIGHT" || {
    err "GIF capture failed."
    rm -rf "$TEMP_DIR"
    exit 1
}

ok "Frames captured and assembled"
echo ""

# ─── Step 5: Optimize with gifsicle ──────────────────────

if [[ "$GIFSICLE_AVAILABLE" == "true" ]]; then
    info "Optimizing GIF (gifsicle $OPTIMIZATION)..."

    case $OPTIMIZATION in
        quality)   GIFSICLE_ARGS="-O2 --colors 256" ;;
        balanced)  GIFSICLE_ARGS="-O3 --lossy=80 --colors 128" ;;
        filesize)  GIFSICLE_ARGS="-O3 --lossy=120 --colors 64" ;;
        *)         GIFSICLE_ARGS="-O3 --lossy=80 --colors 128" ;;
    esac

    # shellcheck disable=SC2086
    gifsicle $GIFSICLE_ARGS "$UNOPTIMIZED_GIF" -o "$OUTPUT_GIF" || {
        warn "gifsicle optimization failed — using unoptimized GIF"
        cp "$UNOPTIMIZED_GIF" "$OUTPUT_GIF"
    }

    BEFORE=$(du -k "$UNOPTIMIZED_GIF" | cut -f1)
    AFTER=$(du -k "$OUTPUT_GIF" | cut -f1)
    if [[ $BEFORE -gt 0 ]]; then
        SAVINGS=$(echo "scale=0; (($BEFORE - $AFTER) * 100) / $BEFORE" | bc)
        ok "Optimized: ${BEFORE}KB → ${AFTER}KB (${SAVINGS}% smaller)"
    fi
else
    cp "$UNOPTIMIZED_GIF" "$OUTPUT_GIF"
fi

# ─── Step 6: Cleanup and success ──────────────────────────

rm -rf "$TEMP_DIR"

echo ""
echo -e "${BOLD}════════════════════════════════════════${NC}"
ok "GIF exported successfully!"
echo ""
echo -e "  ${BOLD}File:${NC}  $OUTPUT_GIF"
echo ""
FILE_SIZE=$(du -h "$OUTPUT_GIF" | cut -f1 | xargs)
echo "  Size: $FILE_SIZE"
echo ""
echo "  This GIF works everywhere — email, Slack, Notion, social."
echo -e "${BOLD}════════════════════════════════════════${NC}"
echo ""

# Open the GIF automatically
if command -v open &>/dev/null; then
    open "$OUTPUT_GIF"
elif command -v xdg-open &>/dev/null; then
    xdg-open "$OUTPUT_GIF"
fi
