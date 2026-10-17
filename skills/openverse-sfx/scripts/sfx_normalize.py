#!/usr/bin/env python3
"""Normalize one audio file by MEASUREMENT, safe for short SFX files.

Two traps this script exists to avoid:
  - ffmpeg's loudnorm filter destroys short SFX: its dynamic mode buffers
    ~3s, so a 0.5s pop comes out tens of dB down. Never loudnorm a short SFX.
  - LUFS gain-matching is wrong for spiky one-shots: a pop can read
    -22 LUFS integrated while its transient already peaks at -3 dBTP, so
    LUFS-matching it to -13 pushes it into clipping. What makes a one-shot
    audible over the bed is its PEAK, not its integrated loudness.

Modes:
  --mode peak  (default, for SFX one-shots) bring true peak to --target dBTP
  --mode lufs  (for beds / longer layers)     bring integrated to --target LUFS

Usage:
  python3 sfx_normalize.py whoosh.mp3 whoosh_n.wav                  # peak to -3 dBTP
  python3 sfx_normalize.py music.mp3 bed.wav --mode lufs --target -20
"""
import argparse, re, subprocess, sys

def measure(path):
    r = subprocess.run(["ffmpeg", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", tail)
    peaks = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", tail)
    if not i:
        sys.exit(f"could not measure {path}")
    return float(i.group(1)), (max(float(p) for p in peaks) if peaks else None)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("dst")
    p.add_argument("--mode", choices=["peak", "lufs"], default="peak")
    p.add_argument("--target", type=float, default=None,
                   help="dBTP in peak mode (default -3), LUFS in lufs mode (default -13)")
    args = p.parse_args()
    target = args.target if args.target is not None else (-3.0 if args.mode == "peak" else -13.0)

    i0, tp0 = measure(args.src)
    current = tp0 if args.mode == "peak" else i0
    if current is None:
        sys.exit("no peak reading - ffmpeg build lacks true-peak; use --mode lufs")
    gain = target - current
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", args.src,
                    "-af", f"volume={gain:.2f}dB", args.dst], check=True)
    i1, tp1 = measure(args.dst)
    after = tp1 if args.mode == "peak" else i1
    ok = after is not None and abs(after - target) <= 0.6
    unit = "dBTP" if args.mode == "peak" else "LUFS"
    print(f"{args.src}: {args.mode} {current} -> {after} {unit} (target {target}, gain {gain:+.1f} dB) "
          f"| integrated now {i1} LUFS " + ("OK" if ok else "OUT OF TOLERANCE"))
    if not ok:
        sys.exit(1)

if __name__ == "__main__":
    main()
