# ffmpeg recipes for openverse-sfx

Assumes: `sfx/music.*` is the music bed, `beats.json` from `beat_grid.py`, SFX files in `sfx/`, and cue times chosen from `beats_s` in beats.json. Work at 48 kHz and keep intermediate WAV files in 32-bit float (`-c:a pcm_f32le`) so overlapping layers in `amix=normalize=0` never clip 16-bit integer rails before Step 4's two-pass `loudnorm`.

## 1. Shift music so existing cuts land on beats
If the video's cuts are at fixed times T_cut, pick a beat B from beats.json near the first cut and delay the music by (T_cut - B) seconds:

```
ffmpeg -i sfx/music.mp3 -af "adelay=<delay_ms>|<delay_ms>" -c:a pcm_f32le music_shifted.wav
```

(delay_ms = (T_cut - B) * 1000; use 0 if negative and instead trim with `-ss`. Loop or trim the music track to the video duration with `-stream_loop -1 -i sfx/music.mp3 ... -t <video_duration_s>` before mixing so it matches whether the source song is shorter or longer than the video.)

## 2. Place one SFX per cue time
Source files arrive at wildly different loudness (a Freesound whoosh can be 15 LU quieter than a music bed), so NEVER trust "SFX at full volume". Normalize every layer by measurement first:

- Each SFX by PEAK to **-3 dBTP**. What makes a one-shot cut through is its transient, not its integrated loudness: a pop can read -22 LUFS while already peaking at -3 dBTP, so LUFS-matching SFX pushes them into clipping. Peak-normalize instead.
- The music bed to **-20 LUFS** (4 LU under target - SFX sit above the music, and the combined mix lands near -16).

WARNING: never run ffmpeg's `loudnorm` filter on a short SFX file. Its dynamic mode buffers ~3 seconds and quietly destroys anything shorter (measured: a 0.5s pop comes out 35 dB down). Use `scripts/sfx_normalize.py` for SFX - it measures with ebur128, applies gain, and re-measures:

```
# normalize each layer once, up front
python3 scripts/sfx_normalize.py sfx/whoosh.mp3 whoosh_n.wav                  # peak -> -3 dBTP
python3 scripts/sfx_normalize.py sfx/pop.mp3    pop_n.wav                     # peak -> -3 dBTP
ffmpeg -y -i music_shifted.wav -af loudnorm=I=-20:TP=-4 -c:a pcm_f32le music_bed.wav   # bed is long - loudnorm is safe here
```

For cues at 3.00s and 7.20s:

```
ffmpeg -i music_bed.wav -i whoosh_n.wav -i pop_n.wav -filter_complex \
"[1:a]adelay=3000|3000[s1]; \
 [2:a]adelay=7200|7200[s2]; \
 [0:a][s1][s2]amix=inputs=3:normalize=0[mix]" \
-map "[mix]" -c:a pcm_f32le mix.wav
```

Sanity-check before the final pass: measure 0.3s at each cue vs 0.8s of bed before it (e.g. with astats or ebur128 on segments). The cue should read clearly louder than the bed. If not, raise that SFX's normalization target, not the whole mix.

## 3. Duck music under voiceover (sidechain)
`sidechaincompress` outputs only the compressed main input (`mix.wav`) and consumes the sidechain (`voiceover.wav`), so split `[1:a]` with `asplit=2[sc][vo]` first and mix `[vo]` back with the ducked bed:

```
ffmpeg -i mix.wav -i voiceover.wav -filter_complex \
"[1:a]asplit=2[sc][vo]; \
 [0:a][sc]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400:makeup=1[bg]; \
 [bg][vo]amix=inputs=2:normalize=0[ducked]" \
-map "[ducked]" -c:a pcm_f32le ducked.wav
```

Voiceover stays loudest; music drops while someone talks.

## 4. Two-pass loudnorm to -16 LUFS, with encoder headroom
Normalize to TP=-4.5, not -4: the AAC encode in step 5 adds ~0.3-0.6 dB of true-peak overshoot, so a -4.0 master comes back off the mux at -3.9 and fails the -4 dBTP gate on the shipped MP4. -4.5 lands at about -4.1 after AAC.
Pass 1 (measure):
```
ffmpeg -i ducked.wav -af loudnorm=I=-16:TP=-4.5:LRA=11:print_format=json -f null -
```
Pass 2 (apply, using the measured_* values from pass 1):
```
ffmpeg -i ducked.wav -af "loudnorm=I=-16:TP=-4.5:LRA=11:measured_I=<v>:measured_TP=<v>:measured_LRA=<v>:measured_thresh=<v>:offset=<v>:linear=true" -c:a pcm_f32le final_audio.wav
```

## 5. Mux onto the video (re-encode audio to AAC, copy video)
Pair `-af apad` on the audio stream with `-shortest` on the output: `apad` extends shorter audio with silence so `-shortest` never truncates video frames, while `-shortest` still caps longer soundtracks at the exact end of `0:v`.

```
ffmpeg -i input.mp4 -i final_audio.wav -map 0:v -c:v copy -map 1:a -af apad -c:a aac -b:a 192k -shortest final.mp4
```

Then verify: `python3 scripts/verify_mix.py final.mp4 --cue 3.0 --cue 7.2`
