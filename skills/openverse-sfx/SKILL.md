---
name: openverse-sfx
description: 'Add a licensed soundtrack to any video for $0 with beat-matched music, Openverse sound effects, -16 LUFS mastering, and FFmpeg verification. Searches 5.2M free CC0/CC-BY/public-domain audio files (no API key), aligns cuts to the kick-drum beat grid with librosa, peak-normalizes SFX one-shots, verifies the exported MP4 with ebur128 and cue frame grabs, and auto-writes credits.txt. Trigger when the user says "add sound to this video", "add music to my video", "add sound effects", "find free SFX", "sound design this clip", "my video needs audio", or "add audio to my ad".'
author: farizanjum
version: 1.0.0
---

# openverse-sfx: Free Licensed Sound Design for Video, Verified by Measurement

You cannot hear. Every decision in this skill is made by measurement (`librosa`, `ffmpeg ebur128`, waveform plots) and verified on the exported file - never by feel, and **never tell the user it sounds good**. Hand them a short list of timestamps to check with headphones instead.

All audio comes from Openverse (`https://api.openverse.org`): 5.2M free audio files, no API key, $0. **Never synthesize music or sound effects in code** - no sine-wave beeps, no noise bursts. Use real licensed recordings only.

---

## Critical Rules

1. **License filter is mandatory.** Only use Openverse results with `license=cc0,by,pdm` and `source=freesound,jamendo`. `scripts/sfx_search.py` enforces this - do not bypass it.
2. **One search per kind of sound.** Anonymous Openverse use is limited to ~200 searches/day. Search once per sound kind (`"whoosh"`, `"ui pop"`, `"upbeat loop"`) and pick from the shortlist. Do not re-search with rephrased queries.
3. **`credits.txt` is not optional.** CC BY audio is only legal to use with credit. Every downloaded file's `attribution` field goes into `credits.txt` verbatim. `scripts/sfx_fetch.py` does this automatically. CC0/PDM need nothing, but log them anyway.
4. **Prerequisites first.** If missing, install before starting: `ffmpeg`, and `pip install librosa matplotlib numpy scipy`.
5. **Measure the exported MP4, never the pre-export WAV.** AAC compression and mono phone playback change the result; only the shipped file counts.

---

## Workflow

### Step 1 - Music
Use a track the user gave you, or search Openverse for one (`python3 scripts/sfx_search.py --query "upbeat loop" --min-ms 15000`). Note the source and license. Download it with `scripts/sfx_fetch.py` into `sfx/` so its attribution lands in `credits.txt`.

### Step 2 - Beat Grid
Run `python3 scripts/beat_grid.py sfx/<music_file>`. It plots the sub-120 Hz waveform (where the kick drum lives) against the detected beat grid, detects off-beat lock numerically, and writes `beats.json`. Open `beatgrid.png`: red lines must sit ON the kick spikes. If they don't, shift the whole grid by half a beat interval (the script checks this numerically and shifts automatically when the half-beat alignment scores >5% higher).

### Step 3 - Put Big Moves on the Beat
Scene cuts, titles appearing, big animations: place them on beats from `beats.json`. If you can change the animation, snap the cut to the nearest beat. If you can't, shift where the music starts so the existing cuts land on beats (`-itsoffset` / `adelay` on the music input).

### Step 4 - One Ready-Made SFX per Cut and Big Move
Use the project's existing sound library first if it has one; ask the user if a needed sound is missing. Otherwise, run one `sfx_search.py` call per kind of sound: whoosh for movement, pop for things appearing, click for clicks, typing sounds for typing. Pick the best fit for each shot's action from the shortlist, and download each pick with `sfx_fetch.py`.

### Step 5 - Mix with the Right Hierarchy
- Voiceover is the loudest layer; music drops while someone talks (sidechain duck or manual volume automation).
- Sound effects sit above the music, and source files arrive at wildly different loudness - normalize every layer by measurement, never fixed volume multipliers:
  - SFX one-shots peak-normalized to **-3 dBTP** with `scripts/sfx_normalize.py` (one-shots cut through by transient, so peak not LUFS; and NEVER run `ffmpeg loudnorm` on a short SFX - its 3-second buffer destroys short files).
  - Music bed normalized to **-20 LUFS**.
  - Exact commands are in `references/ffmpeg_recipes.md`.
- Target **-16 LUFS integrated, true peak below -4 dBFS on the shipped MP4**, so nothing clips after AAC compression or on a phone speaker in mono. Master to `TP=-4.5`: the AAC encode adds ~0.3-0.6 dB of overshoot and a `-4.0` master comes back off the mux failing the gate.
- Read `references/ffmpeg_recipes.md` for the exact `ffmpeg` commands for ducking, SFX placement at beat times, and two-pass `loudnorm`.

### Step 6 - Verify the Export, Then Hand Over Check Points
Run `python3 scripts/verify_mix.py final.mp4 --cue <t1> --cue <t2> ...` with every cue time. It measures the exported MP4 with `ebur128`, grabs one frame before and after every cue from the MP4, and plots the exported waveform with cue lines. Confirm loudness and peak pass, and that each cue sits on a waveform spike and its frames show the cut/title. Then give the user **5 timestamps to check with headphones** and the path to `credits.txt`. Do not claim it sounds good.

---

## Scripts

| Script | Purpose |
|---|---|
| `scripts/sfx_search.py` | Openverse search, license/source filters enforced (`cc0,by,pdm` from `freesound,jamendo`), duration filtering, JSON shortlist with attribution fields |
| `scripts/sfx_fetch.py` | Downloads the chosen file into `sfx/` via Python stdlib (`urllib.request`) and appends its verbatim attribution to `credits.txt` |
| `scripts/sfx_normalize.py` | `ebur128` measure + gain + re-measure; peak mode (`-3 dBTP`) for SFX one-shots, LUFS mode for beds - safe where `loudnorm` destroys short files |
| `scripts/beat_grid.py` | `librosa` beat tracking + numerical off-beat lock check + sub-120 Hz kick-band/grid plot (`beatgrid.png`) + `beats.json` |
| `scripts/verify_mix.py` | `ebur128` loudness + true peak on the exported MP4, before/after cue frame grabs, waveform plot (`verify/waveform.png`), `PASS` / `NEEDS FIX` verdict |

## References

- `references/ffmpeg_recipes.md` - exact `ffmpeg` commands for beat-shifting music, placing SFX at cue times, voiceover sidechain ducking, and two-pass `loudnorm` to `-16 LUFS` / `-4 dBTP`. Read it before writing any `ffmpeg` command.
