#!/usr/bin/env python3
"""Search Openverse for free, commercially usable audio (music + SFX).

Uses the anonymous Openverse API - no API key. Anonymous use is limited to
~200 searches/day, so search for each kind of sound ONCE and pick from the
shortlist instead of re-searching with tweaked queries.

Only returns results with license in (cc0, by, pdm) and source in
(freesound, jamendo), matching the skill's license policy.

Usage:
  python3 sfx_search.py --query "whoosh" [--max-results 8] [--min-ms 0] [--max-ms 30000]
"""
import argparse, json, sys, urllib.error, urllib.parse, urllib.request

API = "https://api.openverse.org/v1/audio/"
LICENSES = "cc0,by,pdm"
SOURCES = "freesound,jamendo"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--query", required=True, help="one kind of sound, e.g. 'whoosh', 'ui pop', 'upbeat loop'")
    p.add_argument("--max-results", type=int, default=8)
    p.add_argument("--min-ms", type=int, default=0, help="min duration in ms (music: use e.g. 15000)")
    p.add_argument("--max-ms", type=int, default=0, help="max duration in ms (sfx: use e.g. 8000)")
    args = p.parse_args()

    qs = {
        "q": args.query,
        "license": LICENSES,
        "source": SOURCES,
        "page_size": str(min(args.max_results * 3, 20)),  # overfetch, duration filter is client-side
    }
    url = API + "?" + urllib.parse.urlencode(qs)
    req = urllib.request.Request(url, headers={"User-Agent": "openverse-sfx-skill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        sys.exit(f"search failed: {e}")

    out = []
    for res in data.get("results", []):
        dur = res.get("duration") or 0
        if args.min_ms and dur < args.min_ms:
            continue
        if args.max_ms and dur > args.max_ms:
            continue
        out.append({
            "id": res.get("id"),
            "title": res.get("title"),
            "creator": res.get("creator"),
            "license": res.get("license"),
            "license_url": res.get("license_url"),
            "source": res.get("source"),
            "duration_s": round(dur / 1000.0, 2),
            "audio_url": res.get("url"),                 # direct file for sfx_fetch.py
            "landing_url": res.get("foreign_landing_url"),
            "attribution": res.get("attribution"),       # copy into credits.txt AS IS
        })
        if len(out) >= args.max_results:
            break

    print(json.dumps({"query": args.query, "license_filter": LICENSES,
                      "source_filter": SOURCES, "results": out}, indent=2))
    if not out:
        print("NOTE: no results after duration filtering. Broaden the duration range "
              "before rephrasing the query - every call counts toward the daily cap.",
              file=sys.stderr)

if __name__ == "__main__":
    main()
