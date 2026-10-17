#!/usr/bin/env python3
"""Download a chosen Openverse audio file into sfx/ and log its attribution.

Copies the result's attribution field into credits.txt AS IS - CC BY tracks
are only legal to use if this credit survives into the shipped video.

Usage:
  python3 sfx_fetch.py --audio-url URL --name whoosh_cut1 \
      --attribution '"Deep Whoosh #1" by Alice (CC0) ...' \
      [--dir sfx] [--credits credits.txt]
"""
import argparse, os, shutil, sys, urllib.error, urllib.request

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--audio-url", required=True, help="the result's audio_url field")
    p.add_argument("--name", required=True, help="file stem, e.g. whoosh_cut1")
    p.add_argument("--attribution", required=True, help="the result's attribution field, verbatim")
    p.add_argument("--dir", default="sfx")
    p.add_argument("--credits", default="credits.txt")
    args = p.parse_args()

    os.makedirs(args.dir, exist_ok=True)
    ext = os.path.splitext(args.audio_url.split("?")[0])[1] or ".mp3"
    dest = os.path.join(args.dir, args.name + ext)
    tmp_dest = dest + ".part"
    try:
        req = urllib.request.Request(args.audio_url, headers={"User-Agent": "openverse-sfx-skill/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp, open(tmp_dest, "wb") as out_f:
            shutil.copyfileobj(resp, out_f)
        if os.path.getsize(tmp_dest) == 0:
            raise OSError("empty response")
        os.replace(tmp_dest, dest)
    except (urllib.error.URLError, TimeoutError, OSError):
        if os.path.exists(tmp_dest):
            os.remove(tmp_dest)
        sys.exit("download failed - re-check the audio_url from sfx_search.py output")

    line = f"{args.name}{ext}: {args.attribution}\n"
    existing = open(args.credits, encoding="utf-8").read() if os.path.isfile(args.credits) else ""
    if line not in existing:
        with open(args.credits, "a", encoding="utf-8") as f:
            f.write(line)
    print(f"saved {dest} ({os.path.getsize(dest)} bytes); attribution appended to {args.credits}")

if __name__ == "__main__":
    main()
