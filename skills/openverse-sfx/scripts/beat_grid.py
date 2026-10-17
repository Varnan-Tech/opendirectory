#!/usr/bin/env python3
"""Find the beat grid of a music track and CHECK it for off-beat lock.

librosa's beat tracker sometimes locks onto the off-beat. This script plots
the sub-120 Hz waveform (where the kick drum lives) against the beat grid so
the alignment can be verified visually, and it also measures both alignments
numerically: it compares low-band energy on the detected grid against the
half-beat-shifted grid and shifts the grid if the shifted one wins.

Usage:
  python3 beat_grid.py <music_file> [--out beats.json] [--plot beatgrid.png]
"""
import argparse, json, sys
import numpy as np

def lowband_env(y, sr, cutoff=120.0):
    from scipy.signal import butter, sosfiltfilt
    nyq = sr / 2.0
    sos = butter(4, min(cutoff / nyq, 0.99), btype="low", output="sos")
    yl = sosfiltfilt(sos, y)
    return np.abs(yl)

def grid_score(env, sr, times):
    idx = np.clip((times * sr).astype(int), 0, len(env) - 1)
    return float(env[idx].mean())

def main():
    p = argparse.ArgumentParser()
    p.add_argument("music")
    p.add_argument("--out", default="beats.json")
    p.add_argument("--plot", default="beatgrid.png")
    args = p.parse_args()

    import librosa
    y, sr = librosa.load(args.music, sr=22050, mono=True)
    tempo, frames = librosa.beat.beat_track(y=y, sr=sr)
    beats = librosa.frames_to_time(frames, sr=sr)
    tempo = float(np.atleast_1d(tempo)[0])
    if len(y) == 0 or not np.isfinite(tempo) or tempo <= 0 or len(beats) == 0:
        sys.exit("no beats detected (silent or ambient track with 0 BPM) - choose a rhythmic track or specify cue timestamps manually")
    half = (60.0 / tempo) / 2.0

    env = lowband_env(y, sr)
    on = grid_score(env, sr, beats)
    off = grid_score(env, sr, beats + half)
    shifted = off > on * 1.05  # shifted grid must win by 5% to override
    if shifted:
        shifted_beats = beats + half
        valid = shifted_beats[shifted_beats <= len(y) / sr]
        beats = valid if len(valid) > 0 else shifted_beats

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"tempo_bpm": round(tempo, 1),
                   "beat_interval_s": round(60.0 / tempo, 4),
                   "beats_s": [round(float(b), 3) for b in beats],
                   "offbeat_lock_detected": bool(shifted)}, f, indent=2)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    t = np.arange(len(y)) / sr
    lo = env / (env.max() or 1)
    fig, axes = plt.subplots(3, 1, figsize=(16, 9), sharex=False)
    span = len(y) / sr / 3.0
    for i, ax in enumerate(axes):
        s = int(i * span * sr)
        e = min(int((i + 1) * span * sr), len(y)) - 1
        ax.plot(t[s:e], lo[s:e], lw=0.5, color="gray")
        for b in beats:
            if t[s] <= b <= t[e]:
                ax.axvline(b, color="red", lw=0.7, alpha=0.7)
        ax.set_ylabel("sub-120Hz env")
    axes[0].set_title(
        f"beat grid vs kick band ({tempo:.0f} BPM"
        + (", grid shifted by half beat - off-beat lock found" if shifted else "")
        + ") - red lines must sit ON the kick spikes")
    axes[-1].set_xlabel("seconds")
    fig.tight_layout()
    fig.savefig(args.plot, dpi=110)
    print(json.dumps({"tempo_bpm": round(tempo, 1), "n_beats": len(beats),
                      "offbeat_lock_detected": bool(shifted),
                      "beats_file": args.out, "plot": args.plot}))

if __name__ == "__main__":
    main()
