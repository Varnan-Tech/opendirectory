#!/usr/bin/env python3
"""Verify an exported video's audio - measurement only, no judgement by feel.

Checks the EXPORTED mp4 (never the pre-export WAV):
  - integrated loudness vs the -16 LUFS target (ffmpeg ebur128)
  - true peak below -4 dBTP (headroom for AAC / phone speakers)
  - one frame before and after every audio cue, grabbed from the mp4
  - a waveform of the exported audio with cue lines drawn on it

Usage:
  python3 verify_mix.py final.mp4 --cue 3.0 --cue 7.0 [--target -16] [--tolerance 1.0] [--outdir verify]
"""
import argparse, json, os, re, subprocess, sys

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("--cue", type=float, action="append", default=[])
    p.add_argument("--target", type=float, default=-16.0)
    p.add_argument("--tolerance", type=float, default=1.0)
    p.add_argument("--outdir", default="verify")
    args = p.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    r = run(["ffmpeg", "-i", args.video, "-af", "ebur128=peak=true", "-f", "null", "-"])
    tail = r.stderr[r.stderr.rfind("Summary:"):]
    def grab(pat):
        m = re.search(pat, tail)
        return float(m.group(1)) if m else None
    integrated = grab(r"Integrated loudness:\s+I:\s+(-?[\d.]+) LUFS")
    true_peak = grab(r"Peak:\s+(-?[\d.]+) dBFS")
    if true_peak is None:  # some builds print "True peak" per-channel block
        vals = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", tail)
        true_peak = max(float(v) for v in vals) if vals else None

    ok_loud = integrated is not None and abs(integrated - args.target) <= args.tolerance
    ok_peak = true_peak is not None and true_peak <= -4.0

    # waveform with cue lines
    wav = os.path.join(args.outdir, "exported_audio.wav")
    if os.path.exists(wav):
        os.remove(wav)
    run(["ffmpeg", "-y", "-i", args.video, "-vn", "-ac", "1", "-ar", "22050", wav])
    if not os.path.isfile(wav) or os.path.getsize(wav) == 0:
        sys.exit(f"could not extract audio stream from {args.video}")
    import numpy as np, wave
    with wave.open(wav) as w:
        sr = w.getframerate()
        y = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768.0
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(16, 4))
    ax.plot(np.arange(len(y)) / sr, y, lw=0.3, color="gray")
    for c in args.cue:
        ax.axvline(c, color="red", lw=0.8)
    ax.set_title("exported audio waveform (red = cues) - each cue should sit on a spike")
    ax.set_xlabel("seconds")
    fig.tight_layout()
    wave_plot = os.path.join(args.outdir, "waveform.png")
    fig.savefig(wave_plot, dpi=110)

    frames = []
    missing_frames = []
    for c in args.cue:
        for label, t in (("before", max(c - 0.1, 0)), ("after", c + 0.1)):
            out = os.path.join(args.outdir, f"cue_{c:.2f}_{label}.png")
            if os.path.exists(out):
                os.remove(out)
            if c < 0:
                missing_frames.append(out)
                continue
            run(["ffmpeg", "-y", "-ss", f"{t:.3f}", "-i", args.video,
                 "-frames:v", "1", "-q:v", "2", out])
            if os.path.isfile(out) and os.path.getsize(out) > 0:
                frames.append(out)
            else:
                missing_frames.append(out)

    ok_frames = len(missing_frames) == 0
    ok = ok_loud and ok_peak and ok_frames

    report = {
        "file": args.video,
        "integrated_lufs": integrated,
        "target_lufs": args.target,
        "loudness_ok": ok_loud,
        "true_peak_dbfs": true_peak,
        "peak_ok": ok_peak,
        "frames_ok": ok_frames,
        "waveform_plot": wave_plot,
        "cue_frames": frames,
        "missing_cue_frames": missing_frames,
    }
    print(json.dumps(report, indent=2))
    print("\nVERDICT:", "PASS" if ok else "NEEDS FIX", file=sys.stderr)
    if not ok_loud:
        print(f"  integrated {integrated} LUFS vs target {args.target} (+-{args.tolerance}) - re-run loudnorm", file=sys.stderr)
    if not ok_peak:
        print(f"  true peak {true_peak} dBFS above -4 - lower gains and re-run loudnorm with true_peak=-4", file=sys.stderr)
    if not ok_frames:
        print(f"  missing cue frames {missing_frames} - cue timestamp may be negative or at/past the end of the video", file=sys.stderr)
    if not ok:
        sys.exit(1)

if __name__ == "__main__":
    main()
