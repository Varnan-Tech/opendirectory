# openverse-sfx

Add a full licensed soundtrack to any video for $0. Searches Openverse's 5.2M free audio files (no API key), beat-matches music to your cuts with librosa, places one sound effect per big move, mixes to -16 LUFS with broadcast-safe peaks, verifies the exported MP4 with FFmpeg, and writes credits.txt automatically.

**Zero API keys required.** Runs entirely on free local tools (`ffmpeg`, `librosa`) and the public Openverse API.

<!-- OPENDIRECTORY_INSTALL_START -->
## Install

### Option A: npx CLI (Recommended)

No global install. Always runs the latest version.

```bash
npx "@opendirectory.dev/skills" install openverse-sfx --target claude
```

### Option B: skills.sh

```bash
npx skills add Varnan-Tech/opendirectory --skill openverse-sfx
```

Requires Node.js. Add `--global` to install to `~/.claude/skills/` instead of the current project.

### Option C: Claude Desktop App

<video src="https://github.com/user-attachments/assets/cea8b565-2002-4a87-8857-d902bfcfdc1c" controls width="100%"></video>

**Step 1: Download the skill from GitHub**

1. Copy the URL of this specific skill folder from your browser's address bar.
2. Go to [download-directory.github.io](https://download-directory.github.io/).
3. Paste the URL and click **Enter** to download.

**Step 2: Install in Claude**

1. Open your **Claude desktop app**.
2. Go to the sidebar on the left side and click on the **Customize** section.
3. Click on the **Skills** tab, then click on the **+** button to create a new skill.
4. Choose **Upload a skill**, then drag and drop the `.zip` file or extracted folder.

> **Note:** For some skills, the `SKILL.md` file might be located inside a subfolder. Always upload the specific folder that contains the `SKILL.md` file.

### Option D: Claude Code Native

Run these commands inside Claude Code:

```bash
/plugin marketplace add Varnan-Tech/opendirectory
/plugin install opendirectory-gtm-skills@opendirectory-marketplace
```

### Option E: Manus AI

<video src="https://github.com/user-attachments/assets/17cbee2a-9e17-4bd4-ac46-68e0e92ffab4" controls width="100%"></video>

[**Install in Manus AI**](https://manus.im/import-skills?githubUrl=https%3A%2F%2Fgithub.com%2FVarnan-Tech%2Fopendirectory%2Ftree%2Fmain%2Fskills%2Fopenverse-sfx&utm_source=opendirectory)

Manus AI users can import a skill directly from its OpenDirectory skill page. This is the easiest path when you want Manus to pull the skill from GitHub for you.

1. Open the skill you want from the [opendirectory homepage](https://opendirectory.dev).
2. In the install panel, select the **Manus AI** tab.
3. Click **Install in Manus AI** - this opens Manus with the skill GitHub URL already attached.
4. Confirm the import inside Manus AI.

> If your Manus workspace prefers file uploads, use the **Download** tab instead and upload the downloaded `.skill.zip` file inside Manus.
<!-- OPENDIRECTORY_INSTALL_END -->


## What It Does

- Searches Openverse's 5.2M audio catalog for commercially usable music and sound effects (`cc0`, `by`, `pdm` from `freesound` and `jamendo` only)
- Downloads selected audio files into `sfx/` and appends verbatim license attributions to `credits.txt`
- Tracks beats with `librosa`, isolates the sub-120 Hz kick-drum band, detects off-beat lock numerically, and plots `beatgrid.png`
- Aligns scene cuts and title reveals to beat timestamps in `beats.json` (or shifts music start timing so existing cuts land on the beat)
- Normalizes every audio layer by measurement: SFX one-shots by true peak (`-3.0 dBTP`) and music beds by integrated loudness (`-20.0 LUFS`)
- Ducks the music bed under voiceover using FFmpeg sidechain compression when speech is present
- Masters the final mix via two-pass EBU R128 `loudnorm` to `-16.0 LUFS` (`-4.5 dBTP` pre-AAC to leave headroom for encoder overshoot)
- Verifies the exported MP4 with `ebur128`, extracts before/after frames at every cue, renders `verify/waveform.png`, and returns 5 timestamps to check with headphones

## Requirements

| Requirement | Purpose | How to Set Up |
|---|---|---|
| FFmpeg | EBU R128 measurement, sidechain ducking, two-pass loudnorm, MP4 muxing | `brew install ffmpeg` / `apt install ffmpeg` / `winget install ffmpeg` |
| Python 3.9+ | Runs the search, download (`urllib.request`), beat-grid, normalization, and verification scripts | python.org |
| Python packages | Beat tracking (`librosa`), Butterworth filtering (`scipy`), waveform plots (`matplotlib`) | `pip install librosa matplotlib numpy scipy` |

No API keys required. The public anonymous Openverse API allows ~200 searches/day, and the skill searches once per sound type.

## Setup

```bash
# Set up FFmpeg (macOS / Linux / Windows)
brew install ffmpeg

# Set up Python audio dependencies
pip install librosa matplotlib numpy scipy
```

## How to Use

```
"Add sound to this video: launch-teaser.mp4"
"Add music and sound effects to my clip at ./demo.mp4"
"Sound design this product reveal video with an upbeat electronic loop and whoosh/pop SFX on every cut"
"Keep the voiceover in demo.mp4, duck a lo-fi music bed underneath, and add UI click sounds at the feature transitions"
"Find free licensed SFX on Openverse for my 15-second ad and mix it to -16 LUFS"
```

## Why Measurement Instead of Guessing

AI agents cannot hear. When an agent mixes audio by guessing volume multipliers or generating sine-wave beeps in code, the result clips, lands off-beat, or drowns out the voiceover.

This skill replaces guesswork with three signal-level safeguards:

- **Off-beat lock correction:** Beat trackers frequently lock onto hi-hat off-beats instead of the kick drum. `beat_grid.py` filters the waveform below 120 Hz, compares energy on the detected grid against a half-beat shift, and shifts the grid automatically when the off-beat alignment scores >5% higher.
- **Peak normalization for short SFX:** FFmpeg's `loudnorm` filter uses a ~3-second rolling window that crushes short one-shots (a 0.5s pop drops by up to 35 dB). `sfx_normalize.py` measures true peak with `ebur128=peak=true`, applies exact linear gain to hit `-3.0 dBTP`, and re-measures to confirm tolerance.
- **AAC encoder headroom:** Mastering a WAV to `-4.0 dBTP` and encoding to 192k AAC adds `0.3-0.6 dB` of true-peak overshoot. Two-pass mastering targets `-4.5 dBTP` on the WAV so the shipped MP4 stays safely below `-4.0 dBTP`.

## Mix Hierarchy

| Layer | Mode | Target | Purpose |
|---|---|---|---|
| Voiceover | Reference layer | Forefront | Triggers 8:1 sidechain compression on the music bed while someone speaks |
| SFX one-shots | True peak (`--mode peak`) | `-3.0 dBTP` | Transients cut through the music bed without clipping |
| Music bed | Integrated (`--mode lufs`) | `-20.0 LUFS` | Sits 4 LU under the final master target so SFX and speech stay clear |
| Pre-mux master WAV | Two-pass `loudnorm` | `-16.0 LUFS` / `-4.5 dBTP` | Broadcast/web loudness standard with 0.5 dB AAC headroom |
| Exported MP4 | Verified (`verify_mix.py`) | `-16.0 LUFS` (±1.0) / `<= -4.0 dBTP` | Clean playback on mono phone speakers and social feeds |

## Output

Each run produces:

1. **`final.mp4`**: Video muxed with a 48 kHz / 192k AAC soundtrack mastered to `-16 LUFS`
2. **`credits.txt`**: Verbatim Openverse attribution lines for every downloaded track (required for `CC BY` audio)
3. **`beats.json` & `beatgrid.png`**: Detected tempo (BPM), beat timestamps in seconds, and kick-band alignment plot
4. **`verify/waveform.png` & cue frames**: Exported audio waveform with red cue markers plus before/after video frames (`cue_<t>_before.png`, `cue_<t>_after.png`) around every SFX cue
5. **5 headphone check timestamps**: Specific moments in the final video for you to spot-check

## Cost Per Run

- Openverse Audio API: free, no auth (~200 searches/day anonymous limit)
- Beat tracking, normalization, and verification (`librosa`, `ffmpeg`): local execution, $0
- Total: free

## Standalone Scripts

Run the individual audio tools directly from the terminal without an agent:

```bash
# 1. Search Openverse for licensed music or SFX (cc0, by, pdm only)
python3 scripts/sfx_search.py --query "upbeat loop" --min-ms 15000
python3 scripts/sfx_search.py --query "whoosh" --max-ms 5000

# 2. Download a track and log its attribution to credits.txt
python3 scripts/sfx_fetch.py \
  --audio-url "https://..." \
  --name whoosh_cut1 \
  --attribution '"Deep Whoosh" by creator (CC0)'

# 3. Extract beat grid and check for off-beat lock
python3 scripts/beat_grid.py sfx/music.mp3 --out beats.json --plot beatgrid.png

# 4. Normalize SFX by true peak (-3 dBTP) or beds by LUFS (-20 LUFS)
python3 scripts/sfx_normalize.py sfx/whoosh_cut1.mp3 whoosh_n.wav
python3 scripts/sfx_normalize.py sfx/music.mp3 bed.wav --mode lufs --target -20

# 5. Verify the exported MP4 loudness, true peak, and cue alignment
python3 scripts/verify_mix.py final.mp4 --cue 0.8 --cue 2.4 --cue 4.1
```

## Project Structure

```
openverse-sfx/
├── SKILL.md
├── README.md
├── package.json
├── scripts/
│   ├── sfx_search.py        Openverse search with license/source/duration filters
│   ├── sfx_fetch.py         Downloader + automatic credits.txt logger
│   ├── beat_grid.py         librosa beat tracker + sub-120 Hz off-beat lock check
│   ├── sfx_normalize.py     ebur128 peak/LUFS normalizer for short SFX and beds
│   └── verify_mix.py        Post-export MP4 loudness, peak, waveform, and frame verifier
└── references/
    └── ffmpeg_recipes.md    Exact FFmpeg commands for ducking, cue placement, and two-pass loudnorm
```

## Plays Well With

| Skill | How to Combine |
|-------|----------------|
| [`vid-motion-graphics`](../vid-motion-graphics) | Generate the multi-scene MP4 first, then run `openverse-sfx` to score the scene cuts and stat reveals with beat-matched music and SFX. |
| [`vid-product-launch`](../vid-product-launch) | Render your 5-act launch video, then pass the exported MP4 and cue timestamps to `openverse-sfx` for licensed audio mastering. |
| [`vid-sizzle-reel`](../vid-sizzle-reel) | Extract `beats.json` with `openverse-sfx` first so your sizzle reel cuts lock to a real licensed track, then master and verify the final export. |
| [`hyperframes-product-launch-video`](../hyperframes-product-launch-video) | Pair Hyperframes visual choreography with `openverse-sfx` for $0 licensed Freesound/Jamendo audio and EBU R128 verification. |

## License

MIT
