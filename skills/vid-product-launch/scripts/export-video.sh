#!/usr/bin/env bash
# export-video.sh — Render product launch HTML to MP4
#
# Usage:
#   bash scripts/export-video.sh <path-to-html> [output.mp4] [options]
#
# Options:
#   --duration N            Total animation duration in seconds (required)
#   --fps N                 Frames per second (default: 30)
#   --width N               Canvas width in pixels (default: 1920)
#   --height N              Canvas height in pixels (default: 1080)
#   --music <file>          Path to audio file to add as background track (mp3/m4a/wav)
#   --letterbox             Pass letterbox flag through to HTML (for cinematic tone)
#   --both-orientations     Generate 16:9 AND 9:16 versions from a single HTML file
#
# Examples:
#   bash scripts/export-video.sh launch/gooseworks-ai/product-launch.html --duration 60
#   bash scripts/export-video.sh launch/gooseworks-ai/product-launch.html --duration 60 --fps 30 --width 1920 --height 1080
#   bash scripts/export-video.sh launch/gooseworks-ai/product-launch.html --duration 60 --music bg.mp3
#   bash scripts/export-video.sh launch/gooseworks-ai/product-launch.html --duration 60 --both-orientations
#
# What this does:
#   1. Checks Node.js and FFmpeg are installed
#   2. Installs Playwright in a temp dir (uses cache after first run)
#   3. Runs capture-frames.mjs — headless Chromium calls renderFrame(t) per frame
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
WIDTH=1920
HEIGHT=1080
MUSIC=""
LETTERBOX=false
BOTH_ORIENTATIONS=false

POSITIONAL=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --duration)           DURATION="$2"; shift 2 ;;
        --fps)                FPS="$2"; shift 2 ;;
        --width)              WIDTH="$2"; shift 2 ;;
        --height)             HEIGHT="$2"; shift 2 ;;
        --music)              MUSIC="$2"; shift 2 ;;
        --letterbox)          LETTERBOX=true; shift ;;
        --both-orientations)  BOTH_ORIENTATIONS=true; shift ;;
        *) POSITIONAL+=("$1"); shift ;;
    esac
done
set -- "${POSITIONAL[@]}"

# ─── Input validation ─────────────────────────────────────────────────────────

if [[ $# -lt 1 ]]; then
    err "Usage: bash scripts/export-video.sh <path-to-html> [output.mp4] [--duration N] [--fps N] [--width N] [--height N] [--music audio.mp3] [--letterbox] [--both-orientations]"
    err ""
    err "Examples:"
    err "  bash scripts/export-video.sh launch/my-product/product-launch.html --duration 60"
    err "  bash scripts/export-video.sh launch/my-product/product-launch.html output.mp4 --duration 60 --fps 30"
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
    err "Example: --duration 60"
    exit 1
fi

if [[ $# -ge 2 ]]; then
    OUTPUT_MP4="$2"
else
    OUTPUT_MP4="$(dirname "$INPUT_HTML")/product-launch.mp4"
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
echo -e "${BOLD}║    Export Product Launch to MP4       ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════╝${NC}"
echo ""
info "Animation: ${DURATION}s @ ${FPS}fps → ${TOTAL_FRAMES} frames"
info "Canvas: ${WIDTH}×${HEIGHT}px (MP4 output: $((WIDTH*2))×$((HEIGHT*2))px @2× retina)"
[[ "$LETTERBOX" == "true" ]] && info "Letterbox: enabled (2.35:1)"
[[ "$BOTH_ORIENTATIONS" == "true" ]] && info "Both orientations: will export 16:9 + 9:16"
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

# ─── SFX Synthesis ───────────────────────────────────────────────────────────
#
# All SFX synthesized natively with FFmpeg aevalsrc/anoisesrc.
# Zero external audio files needed.

synth_sfx_type() {
    local sfx_type="$1"
    local sfx_dir="$2"
    local sfx_path="$sfx_dir/${sfx_type}.wav"
    [[ -f "$sfx_path" ]] && return 0

    case "$sfx_type" in
        word-hit)
            # Cinematic word impact — sub punch (50Hz) + transient click (2.2kHz) + noise burst
            # Three layers mixed: felt body + sharp attack + air
            ffmpeg -y \
                -f lavfi -i "aevalsrc=0.85*sin(2*PI*50*t)*exp(-t/0.045)+0.45*sin(2*PI*120*t)*exp(-t/0.028):s=44100:d=0.18" \
                -f lavfi -i "aevalsrc=0.55*sin(2*PI*2200*t)*exp(-t/0.005)+0.30*sin(2*PI*1100*t)*exp(-t/0.008):s=44100:d=0.02" \
                -f lavfi -i "anoisesrc=s=44100:d=0.015" \
                -filter_complex \
                    "[2:a]highpass=f=3500,lowpass=f=9000,volume=0.45,afade=t=out:st=0.008:d=0.007[burst];
                     [0:a][1:a]amix=inputs=2:normalize=0[body];
                     [body][burst]amix=inputs=2:normalize=0[out]" \
                -map "[out]" -t 0.18 "$sfx_path" 2>/dev/null ;;

        type-sequence)
            # Typewriter loop — 15Hz narrow clicks for 1.9s (matches TYPE_DUR 1800ms)
            # sin(t*PI*15)^30 creates 15Hz pulses each ~9ms wide — no multi-arg functions needed
            # 1200Hz click + 200Hz body thud, bandpass 400–5000Hz for mechanical keyboard character
            ffmpeg -y -f lavfi \
                -i "aevalsrc=sin(t*PI*15)^30*(sin(t*2*PI*1200)*0.30+sin(t*2*PI*200)*0.18)*0.7:s=44100:d=1.9" \
                -af "highpass=f=400,lowpass=f=5000" \
                "$sfx_path" 2>/dev/null ;;

        whoosh)
            # Directional sweep — two-band noise (body + air), 700ms
            ffmpeg -y \
                -f lavfi -i "anoisesrc=s=44100:d=0.7" \
                -f lavfi -i "anoisesrc=s=44100:d=0.7" \
                -filter_complex \
                    "[0:a]bandpass=f=1100:width_type=h:width=900,volume=0.7,afade=t=in:st=0:d=0.06,afade=t=out:st=0.45:d=0.25[lo];
                     [1:a]highpass=f=4000,lowpass=f=8000,volume=0.3,afade=t=in:st=0:d=0.03,afade=t=out:st=0.20:d=0.15[hi];
                     [lo][hi]amix=inputs=2:normalize=0[out]" \
                -map "[out]" -t 0.7 "$sfx_path" 2>/dev/null ;;

        tension-riser)
            # 2.8s ascending tension build — amplitude ramps from silence to peak at reveal-boom
            # Layer 1: bandpass rumble (200Hz) growing louder via volume ramp
            # Layer 2: sub tone (55Hz) with linear amplitude ramp t/2.8 → starts silent, peaks at end
            ffmpeg -y \
                -f lavfi -i "anoisesrc=s=44100:d=2.9" \
                -f lavfi -i "aevalsrc=0.22*sin(2*PI*55*t)*(t/2.8):s=44100:d=2.9" \
                -filter_complex \
                    "[0:a]bandpass=f=250:width_type=h:width=400,afade=t=in:st=0:d=1.8,afade=t=out:st=2.55:d=0.35[rumble];
                     [rumble]volume=0.45[rumble_v];
                     [1:a]afade=t=in:st=0:d=2.4[tone];
                     [rumble_v][tone]amix=inputs=2:normalize=0[out]" \
                -map "[out]" -t 2.9 "$sfx_path" 2>/dev/null ;;

        reveal-boom)
            # Full cinematic impact — sub (45Hz) + body (90Hz) + high shimmer + reverb tail
            # aecho adds 85ms tail at 0.25 decay — makes it feel cinematic not digital
            ffmpeg -y \
                -f lavfi -i "aevalsrc=0.90*sin(2*PI*45*t)*exp(-t/0.12)+0.50*sin(2*PI*90*t)*exp(-t/0.07)+0.25*sin(2*PI*180*t)*exp(-t/0.04):s=44100:d=0.6" \
                -f lavfi -i "anoisesrc=s=44100:d=0.10" \
                -filter_complex \
                    "[1:a]highpass=f=4500,lowpass=f=11000,volume=0.40,afade=t=out:st=0.05:d=0.05[shimmer];
                     [0:a][shimmer]amix=inputs=2:normalize=0[mix];
                     [mix]aecho=0.8:0.4:85:0.25[out]" \
                -map "[out]" -t 0.9 "$sfx_path" 2>/dev/null ;;

        counter-tick)
            # Harmonic data tick — 880Hz + 440Hz + 1760Hz overtones, satisfying click
            ffmpeg -y -f lavfi \
                -i "aevalsrc=0.38*sin(2*PI*880*t)*exp(-t/0.010)+0.22*sin(2*PI*440*t)*exp(-t/0.018)+0.15*sin(2*PI*1760*t)*exp(-t/0.006)+0.08*sin(2*PI*2640*t)*exp(-t/0.004):s=44100:d=0.08" \
                "$sfx_path" 2>/dev/null ;;

        cta-chime)
            # A major chord resolution — 440 + 554 + 659Hz + octave, musical arrival
            # aecho adds 60ms shimmer tail at 0.35 decay — bell-like character, not digital blip
            ffmpeg -y -f lavfi \
                -i "aevalsrc=(0.38*sin(2*PI*440*t)+0.30*sin(2*PI*554*t)+0.25*sin(2*PI*659*t)+0.12*sin(2*PI*880*t))*exp(-t/0.60):s=44100:d=1.2" \
                -af "aecho=0.8:0.88:60:0.35" \
                "$sfx_path" 2>/dev/null ;;

        *)
            warn "Unknown SFX type: ${sfx_type} — skipping"
            return 1 ;;
    esac
}

add_sfx_to_video() {
    local in_mp4="$1"
    local out_mp4="$2"
    local html_file="$3"
    local music_file="${4:-}"
    local sfx_dir="$TEMP_DIR/sfx"

    mkdir -p "$sfx_dir"

    # Write Node.js timeline extractor once
    if [[ ! -f "$TEMP_DIR/extract-sfx.mjs" ]]; then
        cat > "$TEMP_DIR/extract-sfx.mjs" << 'NODEEOF'
import { readFileSync } from 'node:fs';
const html = readFileSync(process.argv[2], 'utf-8');
const m = html.match(/window\.__sfxTimeline\s*=\s*(\[[\s\S]*?\]);/);
if (!m) process.exit(0);
try {
  // Use Function() not JSON.parse — timeline uses JS syntax (single quotes, trailing commas, // comments)
  const arr = new Function('return ' + m[1])();
  arr.forEach(e =>
    process.stdout.write(`${e.ms}|${e.sfx}|${e.vol !== undefined ? e.vol : 1.0}\n`)
  );
} catch (err) {
  process.stderr.write('SFX parse error: ' + err.message + '\n');
  process.exit(0);
}
NODEEOF
    fi

    # Parse SFX timeline from HTML
    local events
    events=$(node "$TEMP_DIR/extract-sfx.mjs" "$html_file" 2>/dev/null) || events=""

    # No SFX timeline found — fall back to music-only or silent copy
    if [[ -z "$events" ]]; then
        warn "No SFX timeline found in HTML (add window.__sfxTimeline to enable SFX)"
        if [[ -n "$music_file" ]]; then
            info "Adding background audio: $music_file"
            ffmpeg -y -i "$in_mp4" -i "$music_file" \
                -c:v copy -c:a aac -b:a 192k -shortest \
                "$out_mp4" 2>/dev/null || { warn "Audio mix failed — saving silent"; cp "$in_mp4" "$out_mp4"; }
            ok "Audio mixed"
        else
            cp "$in_mp4" "$out_mp4"
        fi
        return
    fi

    local event_count
    event_count=$(echo "$events" | grep -c '.' 2>/dev/null) || event_count=0
    info "Synthesizing SFX: ${event_count} events..."

    # Synthesize each unique SFX type
    local synthesized=()
    while IFS='|' read -r ms sfx vol; do
        [[ -z "$sfx" ]] && continue
        if ! printf '%s\n' "${synthesized[@]:-}" | grep -qx "$sfx"; then
            synthesized+=("$sfx")
            synth_sfx_type "$sfx" "$sfx_dir"
        fi
    done <<< "$events"

    # Build FFmpeg inputs + filter_complex
    local ffmpeg_inputs=()
    local filter_parts=()
    local mix_labels=()
    local input_idx=1   # 0 = in_mp4

    if [[ -n "$music_file" ]]; then
        ffmpeg_inputs+=("-i" "$music_file")
        filter_parts+=("[1:a]volume=0.22[bg_music]")
        mix_labels+=("[bg_music]")
        input_idx=2
    fi

    local event_idx=0
    while IFS='|' read -r ms sfx vol; do
        [[ -z "$sfx" ]] && continue
        local sfx_path="$sfx_dir/${sfx}.wav"
        [[ ! -f "$sfx_path" ]] && continue

        ffmpeg_inputs+=("-i" "$sfx_path")
        filter_parts+=("[${input_idx}:a]volume=${vol},adelay=${ms}|${ms}[s${event_idx}]")
        mix_labels+=("[s${event_idx}]")
        input_idx=$((input_idx + 1))
        event_idx=$((event_idx + 1))
    done <<< "$events"

    if [[ $event_idx -eq 0 && ${#mix_labels[@]} -eq 0 ]]; then
        cp "$in_mp4" "$out_mp4"
        return
    fi

    local total_inputs=${#mix_labels[@]}
    local all_labels
    printf -v all_labels '%s' "${mix_labels[@]}"
    filter_parts+=("${all_labels}amix=inputs=${total_inputs}:normalize=0:dropout_transition=0[finalsfx]")

    local filter_complex
    filter_complex=$(IFS=';'; echo "${filter_parts[*]}")

    ffmpeg -y \
        -i "$in_mp4" \
        "${ffmpeg_inputs[@]}" \
        -filter_complex "$filter_complex" \
        -map 0:v \
        -map "[finalsfx]" \
        -c:v copy \
        -c:a aac -b:a 192k \
        "$out_mp4" 2>/dev/null || {
        warn "SFX mixing failed — saving without SFX"
        if [[ -n "$music_file" ]]; then
            ffmpeg -y -i "$in_mp4" -i "$music_file" \
                -c:v copy -c:a aac -b:a 192k -shortest \
                "$out_mp4" 2>/dev/null || cp "$in_mp4" "$out_mp4"
        else
            cp "$in_mp4" "$out_mp4"
        fi
        return
    }

    ok "SFX mixed: ${event_idx} events"
}

# ─── Helper: render one orientation ──────────────────────────────────────────

render_orientation() {
    local w="$1"
    local h="$2"
    local out_mp4="$3"
    local frames_subdir="$TEMP_DIR/frames_${w}x${h}"

    info "Capturing ${TOTAL_FRAMES} frames at ${w}×${h}..."
    echo ""

    node "$TEMP_SCRIPT" \
        "$(dirname "$INPUT_HTML")" \
        "$(basename "$INPUT_HTML")" \
        "$frames_subdir" \
        "$w" \
        "$h" \
        "$DURATION" \
        "$FPS" || {
        err "Frame capture failed (${w}×${h})."
        rm -rf "$TEMP_DIR"
        exit 1
    }

    echo ""
    ok "Frames captured (${w}×${h})"
    echo ""

    local silent_mp4="$TEMP_DIR/silent_${w}x${h}.mp4"

    info "Assembling MP4 (H.264, yuv420p) → ${out_mp4}..."

    ffmpeg -y \
        -framerate "$FPS" \
        -i "$frames_subdir/frame_%04d.png" \
        -c:v libx264 \
        -crf 20 \
        -pix_fmt yuv420p \
        -movflags +faststart \
        "$silent_mp4" 2>/dev/null || {
        err "FFmpeg assembly failed (${w}×${h})."
        rm -rf "$TEMP_DIR"
        exit 1
    }

    ok "Video assembled (silent)"
    echo ""

    add_sfx_to_video "$silent_mp4" "$out_mp4" "$INPUT_HTML" "${MUSIC}"
}

# ─── Step 3 + 4 + 5: Capture + assemble ──────────────────────────────────────

if [[ "$BOTH_ORIENTATIONS" == "true" ]]; then
    # 16:9 landscape
    LANDSCAPE_MP4="${OUTPUT_MP4%.mp4}-16x9.mp4"
    render_orientation 1920 1080 "$LANDSCAPE_MP4"

    # 9:16 portrait
    PORTRAIT_MP4="${OUTPUT_MP4%.mp4}-9x16.mp4"
    render_orientation 1080 1920 "$PORTRAIT_MP4"
else
    render_orientation "$WIDTH" "$HEIGHT" "$OUTPUT_MP4"
fi

# ─── Step 6: Cleanup + report ─────────────────────────────────────────────────

rm -rf "$TEMP_DIR"

echo ""
echo -e "${BOLD}════════════════════════════════════════${NC}"
ok "Product launch video exported!"
echo ""

if [[ "$BOTH_ORIENTATIONS" == "true" ]]; then
    LANDSCAPE_SIZE=$(du -h "$LANDSCAPE_MP4" | cut -f1 | xargs)
    PORTRAIT_SIZE=$(du -h "$PORTRAIT_MP4" | cut -f1 | xargs)
    echo -e "  ${BOLD}16:9 (landscape):${NC} $LANDSCAPE_MP4 (${LANDSCAPE_SIZE})"
    echo -e "  ${BOLD}9:16 (portrait):${NC}  $PORTRAIT_MP4 (${PORTRAIT_SIZE})"
else
    FILE_SIZE=$(du -h "$OUTPUT_MP4" | cut -f1 | xargs)
    echo -e "  ${BOLD}File:${NC}     $OUTPUT_MP4"
    echo -e "  ${BOLD}Size:${NC}     $FILE_SIZE"
fi

echo -e "  ${BOLD}Duration:${NC} ${DURATION}s @ ${FPS}fps"
echo ""
echo "  Compatible with: QuickTime, iOS, Android, Twitter, LinkedIn, Instagram"
echo -e "${BOLD}════════════════════════════════════════${NC}"
echo ""

if command -v open &>/dev/null; then
    if [[ "$BOTH_ORIENTATIONS" == "true" ]]; then
        open "$LANDSCAPE_MP4"
    else
        open "$OUTPUT_MP4"
    fi
elif command -v xdg-open &>/dev/null; then
    if [[ "$BOTH_ORIENTATIONS" == "true" ]]; then
        xdg-open "$LANDSCAPE_MP4"
    else
        xdg-open "$OUTPUT_MP4"
    fi
fi
