#!/usr/bin/env bash
# export-video.sh — Render HTML/CSS motion graphic to MP4
#
# Usage:
#   bash scripts/export-video.sh <path-to-html> [output.mp4] [options]
#
# Options:
#   --duration N      Total animation duration in seconds (required)
#   --fps N           Frames per second (default: 30)
#   --width N         Canvas width in pixels (default: 1080)
#   --height N        Canvas height in pixels (default: 1080)
#   --music <file>    Path to audio file to add as background track (mp3/m4a/wav)
#
# Examples:
#   bash scripts/export-video.sh ./q4-growth/video.html --duration 9
#   bash scripts/export-video.sh ./q4-growth/video.html output.mp4 --duration 9 --fps 30
#   bash scripts/export-video.sh ./q4-growth/video.html --duration 12 --width 1080 --height 1920
#   bash scripts/export-video.sh ./q4-growth/video.html --duration 9 --music bg.mp3
#
# What this does:
#   1. Checks Node.js and FFmpeg are installed
#   2. Installs Playwright in a temp dir (uses cache after first run)
#   3. Runs capture-frames.mjs — headless Chromium seeks Web Animations API frame-by-frame
#   4. Runs FFmpeg: PNG sequence → H.264 MP4 (-pix_fmt yuv420p for max compatibility)
#   5. Optional: second FFmpeg pass to mix in background audio
#   6. Cleans up frames, reports output
#
# Output PNG dimensions: 2× input (deviceScaleFactor: 2 retina)
# Output MP4 dimensions: same as PNG (2× specified width/height)
set -euo pipefail

# ─── Colors ──────────────────────────────────────────────────────────────────
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

# ─── Parse flags ─────────────────────────────────────────────────────────────
DURATION=""
FPS=30
WIDTH=1080
HEIGHT=1080
MUSIC=""

POSITIONAL=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --duration) DURATION="$2"; shift 2 ;;
        --fps)      FPS="$2"; shift 2 ;;
        --width)    WIDTH="$2"; shift 2 ;;
        --height)   HEIGHT="$2"; shift 2 ;;
        --music)    MUSIC="$2"; shift 2 ;;
        *) POSITIONAL+=("$1"); shift ;;
    esac
done
set -- "${POSITIONAL[@]}"

# ─── Input validation ─────────────────────────────────────────────────────────

if [[ $# -lt 1 ]]; then
    err "Usage: bash scripts/export-video.sh <path-to-html> [output.mp4] [--duration N] [--fps N] [--width N] [--height N] [--music audio.mp3]"
    err ""
    err "Examples:"
    err "  bash scripts/export-video.sh ./my-video/video.html --duration 9"
    err "  bash scripts/export-video.sh ./my-video/video.html output.mp4 --duration 12 --fps 30"
    exit 1
fi

INPUT_HTML="$1"
if [[ ! -f "$INPUT_HTML" ]]; then
    err "File not found: $INPUT_HTML"
    exit 1
fi
INPUT_HTML=$(cd "$(dirname "$INPUT_HTML")" && pwd)/$(basename "$INPUT_HTML")

if [[ -z "$DURATION" ]]; then
    err "--duration is required (total animation length in seconds)"
    err "Example: --duration 9"
    exit 1
fi

if [[ $# -ge 2 ]]; then
    OUTPUT_MP4="$2"
else
    OUTPUT_MP4="$(dirname "$INPUT_HTML")/$(basename "$INPUT_HTML" .html).mp4"
fi

OUTPUT_DIR=$(cd "$(dirname "$OUTPUT_MP4")" 2>/dev/null && pwd || { mkdir -p "$(dirname "$OUTPUT_MP4")" && cd "$(dirname "$OUTPUT_MP4")" && pwd; })
OUTPUT_MP4="$OUTPUT_DIR/$(basename "$OUTPUT_MP4")"

if [[ -n "$MUSIC" && ! -f "$MUSIC" ]]; then
    err "Music file not found: $MUSIC"
    exit 1
fi

TOTAL_FRAMES=$(echo "$DURATION * $FPS" | bc | cut -d. -f1)

echo ""
echo -e "${BOLD}╔══════════════════════════════════════╗${NC}"
echo -e "${BOLD}║     Export Motion Graphic to MP4      ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════╝${NC}"
echo ""
info "Animation: ${DURATION}s @ ${FPS}fps → ${TOTAL_FRAMES} frames"
info "Canvas: ${WIDTH}×${HEIGHT}px (MP4 output: $((WIDTH*2))×$((HEIGHT*2))px @2× retina)"
[[ -n "$MUSIC" ]] && info "Audio: $MUSIC"
echo ""

# ─── Step 1: Check dependencies ──────────────────────────────────────────────

info "Checking dependencies..."

if ! command -v node &>/dev/null; then
    err "Node.js is required but not installed."
    err ""
    err "Install Node.js:"
    err "  macOS:   brew install node"
    err "  or visit https://nodejs.org"
    exit 1
fi
ok "Node.js found ($(node --version))"

if ! command -v ffmpeg &>/dev/null; then
    err "FFmpeg is required but not installed."
    err ""
    err "Install FFmpeg:"
    err "  macOS:   brew install ffmpeg"
    err "  Ubuntu:  sudo apt install ffmpeg"
    exit 1
fi
ok "FFmpeg found ($(ffmpeg -version 2>&1 | head -1 | cut -d' ' -f3))"

# ─── Step 2: Set up Node dependencies ────────────────────────────────────────

TEMP_DIR=$(mktemp -d)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMES_DIR="$TEMP_DIR/frames"
TEMP_SCRIPT="$TEMP_DIR/capture-frames.mjs"

cp "$SCRIPT_DIR/capture-frames.mjs" "$TEMP_SCRIPT"

info "Setting up Playwright..."
cd "$TEMP_DIR"

cat > "$TEMP_DIR/package.json" << 'PKG'
{ "name": "video-export", "private": true, "type": "module" }
PKG

npm install playwright 2>/dev/null || {
    err "Failed to install Playwright."
    rm -rf "$TEMP_DIR"
    exit 1
}

npx playwright install chromium 2>/dev/null || {
    err "Failed to install Chromium for Playwright."
    rm -rf "$TEMP_DIR"
    exit 1
}
ok "Playwright ready"
echo ""

# ─── Step 3: Capture frames ───────────────────────────────────────────────────

SERVE_DIR=$(dirname "$INPUT_HTML")
HTML_FILENAME=$(basename "$INPUT_HTML")

info "Capturing ${TOTAL_FRAMES} frames from ${HTML_FILENAME}..."
echo ""

node "$TEMP_SCRIPT" \
    "$SERVE_DIR" \
    "$HTML_FILENAME" \
    "$FRAMES_DIR" \
    "$WIDTH" \
    "$HEIGHT" \
    "$DURATION" \
    "$FPS" || {
    err "Frame capture failed."
    rm -rf "$TEMP_DIR"
    exit 1
}

echo ""
ok "Frames captured"
echo ""

# ─── Step 4: Assemble MP4 with FFmpeg ────────────────────────────────────────

SILENT_MP4="$TEMP_DIR/silent.mp4"

info "Assembling MP4 (H.264, yuv420p)..."

# -pix_fmt yuv420p: required for QuickTime / iOS / social platform compatibility
# -crf 20: high quality (18=lossless, 28=lower quality)
# -movflags +faststart: move metadata to file start (enables streaming)
ffmpeg -y \
    -framerate "$FPS" \
    -i "$FRAMES_DIR/frame_%04d.png" \
    -c:v libx264 \
    -crf 20 \
    -pix_fmt yuv420p \
    -movflags +faststart \
    "$SILENT_MP4" 2>/dev/null || {
    err "FFmpeg assembly failed."
    rm -rf "$TEMP_DIR"
    exit 1
}

ok "Video assembled (silent)"
echo ""

# ─── Step 5: Add audio (optional) ────────────────────────────────────────────

if [[ -n "$MUSIC" ]]; then
    info "Adding background audio: $MUSIC"

    # -c:v copy: no re-encode of video stream
    # -c:a aac: encode audio as AAC (universal MP4 support)
    # -shortest: truncate to shortest stream (video or audio)
    ffmpeg -y \
        -i "$SILENT_MP4" \
        -i "$MUSIC" \
        -c:v copy \
        -c:a aac \
        -b:a 192k \
        -shortest \
        "$OUTPUT_MP4" 2>/dev/null || {
        warn "Audio mixing failed — saving silent version"
        cp "$SILENT_MP4" "$OUTPUT_MP4"
    }
    ok "Audio mixed"
else
    cp "$SILENT_MP4" "$OUTPUT_MP4"
fi

# ─── Step 6: Cleanup + report ─────────────────────────────────────────────────

rm -rf "$TEMP_DIR"

FILE_SIZE=$(du -h "$OUTPUT_MP4" | cut -f1 | xargs)

echo ""
echo -e "${BOLD}════════════════════════════════════════${NC}"
ok "MP4 exported successfully!"
echo ""
echo -e "  ${BOLD}File:${NC}     $OUTPUT_MP4"
echo -e "  ${BOLD}Size:${NC}     $FILE_SIZE"
echo -e "  ${BOLD}Duration:${NC} ${DURATION}s @ ${FPS}fps"
echo ""
echo "  Compatible with: QuickTime, iOS, Android, Twitter, LinkedIn, Instagram"
echo -e "${BOLD}════════════════════════════════════════${NC}"
echo ""

if command -v open &>/dev/null; then
    open "$OUTPUT_MP4"
elif command -v xdg-open &>/dev/null; then
    xdg-open "$OUTPUT_MP4"
fi
