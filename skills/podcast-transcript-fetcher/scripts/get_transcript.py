#!/usr/bin/env python3
"""
Podcast Transcript Fetcher -- 3-tier CLI for getting podcast transcripts.

Tier 1: Direct free sources (GitHub archives, APIs, website scrapes)
Tier 2: RSS audio download + Whisper transcription (local or Groq cloud)
Tier 3: Taddy API (commercial, requires TADDY_API_KEY)

Usage:
    python get_transcript.py <podcast> [--episode <episode>] [--method <method>]
    python get_transcript.py <podcast> --latest
    python get_transcript.py --list-podcasts
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import shutil
import sys
import tempfile
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

# Auto-load .env from project root or parent directories
try:
    from dotenv import load_dotenv

    _script_dir = Path(__file__).resolve().parent
    _project_root = _script_dir.parent
    load_dotenv(_project_root / ".env")
except ImportError:
    pass

# -- Fix Windows console encoding ------------------------------------
# Prevent UnicodeEncodeError when printing transcripts with non-ASCII
# characters (e.g. Dwarkesh transcripts with accented characters) on
# Windows consoles that default to cp1252.
if sys.platform == "win32" and sys.stdout.encoding and sys.stdout.encoding.lower() in ("cp1252", "ansi"):
    sys.stdout.reconfigure(encoding="utf-8")

# -- Paths ---------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
REGISTRY_PATH = SCRIPT_DIR / "podcasts.json"
CACHE_DIR = SCRIPT_DIR / ".rss_cache"
OUTPUT_DIR = PROJECT_DIR / "output"
CACHE_TTL_SEC = 3600  # 1 hour

# -- Registry --------------------------------------------------------

def load_registry():
    """Load the podcast registry JSON."""
    if not REGISTRY_PATH.exists():
        print(f"[ERROR] Registry not found at {REGISTRY_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def find_podcast(query: str, registry: dict[str, Any]):
    """Fuzzy-match a podcast name/slug against the registry."""
    query = query.strip().lower()
    podcasts = registry.get("podcasts", [])
    
    # Exact match on id, slug, or name
    for p in podcasts:
        if query in [p["id"].lower(), p["slug"].lower(), p["name"].lower()]:
            return p
    
    # Substring match
    for p in podcasts:
        if query in p["name"].lower():
            return p
        if query in p["slug"].lower():
            return p
    
    # Token overlap ("lenny" -> "Lenny's Podcast", "20vc" -> "20 Minutes VC")
    query_tokens = set(re.split(r"[\s'-]+", query))
    scored = []
    for p in podcasts:
        name_tokens = set(re.split(r"[\s'-]+", p["name"].lower()))
        overlap = len(query_tokens & name_tokens)
        if overlap > 0:
            scored.append((overlap, p))
    if scored:
        scored.sort(reverse=True)
        return scored[0][1]
    
    return None


def list_podcasts(registry: dict[str, Any], as_json: bool = False):
    """Print all registered podcasts."""
    if as_json:
        print(json.dumps(registry, indent=2))
        return
    print(f"\n== Registered Podcasts ({len(registry['podcasts'])}):")
    print(f"   {'-' * 60}")
    for p in registry["podcasts"]:
        sources = list(p["transcript_sources"].keys())
        print(f"   {p['name']:30s}  ({', '.join(sources)})")
    print()

# -- RSS Caching Layer ----------------------------------------------

def _cache_path(url: str) -> Path:
    """Return the cache file path for a given RSS URL."""
    safe_name = re.sub(r"[^a-zA-Z0-9]+", "_", url.split("//")[-1])
    safe_name = safe_name.strip("_")[:120]
    return CACHE_DIR / f"{safe_name}.json"


def _load_cached_rss(url: str) -> list[dict[str, Any]] | None:
    """Return cached episodes if cache is still fresh (< TTL)."""
    path = _cache_path(url)
    if not path.exists():
        return None
    age = time.time() - path.stat().st_mtime
    if age > CACHE_TTL_SEC:
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        print(f"   [CACHE] Using cached RSS ({int(age)}s old): {len(data)} episodes")
        return data
    except (json.JSONDecodeError, OSError):
        return None


def _save_cached_rss(url: str, episodes: list[dict[str, Any]]):
    """Save parsed RSS episodes to cache."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = _cache_path(url)
    path.write_text(json.dumps(episodes, indent=2, default=str), encoding="utf-8")


def fetch_rss_cached(url: str) -> list[dict[str, Any]]:
    """Fetch and parse RSS with caching. Returns list of episode dicts."""
    cached = _load_cached_rss(url)
    if cached is not None:
        return cached
    episodes = fetch_rss(url)
    if episodes:
        _save_cached_rss(url, episodes)
    return episodes


# -- Output Helpers -------------------------------------------------

def _slugify(text: str) -> str:
    """Convert text to a safe filesystem slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text[:80].rstrip("-")


def _auto_filename(
    podcast_name: str,
    episode_title: str,
    pub_date: str,
    index: int,
) -> Path:
    """Generate output path: output/{podcast_slug}/PodcastName_Date_Title.md"""
    podcast_slug = _slugify(podcast_name)
    date_part = pub_date[:10] if pub_date else "unknown-date"
    title_slug = _slugify(episode_title)[:60]
    filename = f"{podcast_name}_{date_part}_{title_slug}.md"
    # Collision-safe: if filename is too long, use index-based name
    if len(filename) > 200:
        filename = f"{podcast_name}_{date_part}_{index:03d}.md"
    out_dir = OUTPUT_DIR / podcast_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / filename


def _write_transcript_with_header(
    transcript_text: str,
    podcast_name: str,
    episode_title: str,
    pub_date: str,
    episode_url: str,
    output_path: Path,
):
    """Write a transcript file with YAML frontmatter metadata header."""
    header = (
        "---\n"
        f"podcast: {podcast_name}\n"
        f"episode: {episode_title}\n"
        f"date: {pub_date}\n"
        f"url: {episode_url}\n"
        f"source: whisper\n"
        "---\n\n"
    )
    output_path.write_text(header + transcript_text, encoding="utf-8")
    print(f"   [SAVED] {output_path}")


# -- RSS Parsing -----------------------------------------------------

def fetch_rss(url: str):
    """Fetch and parse an RSS feed. Returns list of episode dicts."""
    print(f"   [RSS] Fetching: {url}")
    raw = None
    
    # Try requests first (handles redirects, better headers)
    try:
        import requests
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/rss+xml, application/xml, text/xml, */*",
        }
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            raw = resp.content
    except ImportError:
        pass  # requests not installed, fall back to urllib
    except Exception as e:
        print(f"   [WARN] requests fetch failed: {e}, trying urllib...")
    
    # Fall back to urllib
    if raw is None:
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            )
            resp = urllib.request.urlopen(req, timeout=30)
            raw = resp.read()
        except Exception as e:
            print(f"   [ERROR] RSS fetch failed: {e}", file=sys.stderr)
            return []
    
    episodes = []
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        print(f"   [ERROR] RSS parse failed: {e}", file=sys.stderr)
        return []
    
    # Handle RSS 2.0 and Atom
    ns = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}
    for item in root.iter("item"):
        ep = {
            "title": item.findtext("title", ""),
            "pub_date": item.findtext("pubDate", ""),
            "link": item.findtext("link", ""),
            "description": item.findtext("description", ""),
            "audio_url": None,
            "guid": item.findtext("guid", ""),
        }
        # Audio enclosure
        enclosure = item.find("enclosure")
        if enclosure is not None:
            ep["audio_url"] = enclosure.get("url")
        episodes.append(ep)
    
    # Try RSS 2.0 with namespaces (Simplecast, Transistor)
    if not episodes:
        for item in root.iter("item"):
            ep = {
                "title": item.findtext("title", ""),
                "pub_date": item.findtext("pubDate", ""),
                "link": item.findtext("link", ""),
                "description": item.findtext("description", ""),
                "audio_url": None,
                "guid": item.findtext("guid", ""),
            }
            enclosure = item.find("enclosure")
            if enclosure is not None:
                ep["audio_url"] = enclosure.get("url")
            episodes.append(ep)
    
    # Try JSON Feed / namespace-based RSS
    if not episodes:
        for item in root.iter("{http://www.w3.org/2005/Atom}entry"):
            ep = {
                "title": item.findtext("{http://www.w3.org/2005/Atom}title", ""),
                "pub_date": item.findtext("{http://www.w3.org/2005/Atom}updated", ""),
                "link": "",
                "description": item.findtext("{http://www.w3.org/2005/Atom}summary", ""),
                "audio_url": None,
                "guid": "",
            }
            for link in item.iter("{http://www.w3.org/2005/Atom}link"):
                rel = link.get("rel", "")
                if rel in ("enclosure", "") and link.get("href"):
                    ep["audio_url"] = link.get("href")
            episodes.append(ep)
    
    return episodes


def find_episode(episodes: list[dict[str, Any]], query: str | None):
    """Find an episode by query: 'latest', number, title substring, or None (-> latest)."""
    if not episodes:
        return None
    
    if not query or query == "latest":
        return episodes[0]  # RSS is reverse-chronological
    
    # Try number match ("15" or "episode 15")
    query_lower = query.lower().strip()
    num_match = re.search(r"(\d+)", query_lower)
    
    if num_match:
        num = num_match.group(1)
        for ep in episodes:
            if f"episode {num}" in ep["title"].lower() or f"#{num}" in ep["title"]:
                return ep
    
    # Substring search in title
    for ep in episodes:
        if query_lower in ep["title"].lower():
            return ep
    
    # GUID search
    for ep in episodes:
        if query_lower in ep["guid"].lower():
            return ep
    
    # No match found
    print(f"   [ERROR] Could not find episode matching '{query}'")
    return None


# -- RSS URL helper -------------------------------------------------

def _get_rss_urls(podcast: dict[str, Any]) -> list[str]:
    """Extract RSS URL(s) from a podcast dict (supports 'rss' string or 'rss_urls' list)."""
    if "rss_urls" in podcast:
        urls = podcast["rss_urls"]
        return urls if isinstance(urls, list) else [urls]
    rss = podcast.get("rss")
    return [rss] if rss else []


# -- Search & Batch Transcription ------------------------------------

def search_episodes(
    episodes: list[dict[str, Any]],
    query: str,
) -> list[dict[str, Any]]:
    """Search episodes by keyword in title and description. Returns scored matches."""
    query_lower = query.lower()
    scored = []
    for ep in episodes:
        title = (ep.get("title") or "").lower()
        desc = (ep.get("description") or "").lower()
        score = 0
        if query_lower in title:
            score += 10
        if query_lower in desc:
            score += 3
        if score > 0:
            scored.append((score, ep))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [ep for _, ep in scored]


def find_by_guest(
    episodes: list[dict[str, Any]],
    guest_name: str,
) -> list[dict[str, Any]]:
    """Search episodes by guest name (looks in title and description)."""
    return search_episodes(episodes, guest_name)


def _print_search_results(
    results: list[tuple[str, list[dict[str, Any]]]],
):
    """Print search results grouped by podcast."""
    total = sum(len(eps) for _, eps in results)
    if total == 0:
        print("   No matching episodes found.")
        return
    print(f"\n== Found {total} matching episode(s):\n")
    for podcast_name, eps in results:
        print(f"   [{podcast_name}] ({len(eps)} matches):")
        for ep in eps[:10]:  # show top 10 per podcast
            title = (ep.get("title") or "Untitled")[:90]
            date = (ep.get("pub_date") or "?")[:10]
            print(f"      {date}  {title}")
        if len(eps) > 10:
            print(f"      ... and {len(eps) - 10} more")
    print()


def _transcribe_job(
    job_type: str,
    podcast_name: str,
    ep: dict[str, Any],
    index: int,
    total: int,
    api_keys: list[str],
) -> bool:
    """Process a single episode end-to-end: download, compress, transcribe, save.
    
    Args:
        job_type: Label for logging (e.g. "Batch" or "Search").
        podcast_name: Display name of the podcast.
        ep: Episode dict with title, pub_date, link, audio_url.
        index: 0-based index for round-robin key selection and filename.
        total: Total count for progress display.
        api_keys: List of GROQ API keys for round-robin.
    
    Returns:
        True if the episode was successfully transcribed and saved, False otherwise.
    """
    ep_title = ep.get("title") or f"Episode {index + 1}"
    pub_date = ep.get("pub_date") or ""
    episode_url = ep.get("link") or ep.get("guid") or ""
    audio_url = ep.get("audio_url") or ""

    if not audio_url:
        print(f"   [{job_type}] [SKIP] {ep_title} - no audio URL")
        return False

    output_path = _auto_filename(podcast_name, ep_title, pub_date, index + 1)
    if output_path.exists():
        print(f"   [{job_type}] [SKIP] Already exists: {output_path.name}")
        return True  # Count as success since it's already done

    tmp_dir = Path(tempfile.mkdtemp(prefix="podcast_"))
    audio_path = tmp_dir / "episode.mp3"
    try:
        if not download_audio(audio_url, audio_path):
            print(f"   [{job_type}] [FAIL] Download failed for {ep_title}")
            return False

        audio_path = _compress_audio(audio_path)

        key = _pick_key(api_keys, index)
        transcript = _transcribe_groq(audio_path, api_key=key)
        if transcript:
            _write_transcript_with_header(
                transcript, podcast_name, ep_title, pub_date, episode_url, output_path
            )
            print(f"   [{job_type}] [OK] Transcribed: {ep_title}")
            return True
        else:
            print(f"   [{job_type}] [FAIL] Transcription returned empty for {ep_title}")
            return False
    except Exception as e:
        print(f"   [{job_type}] [ERROR] {ep_title}: {e}")
        return False
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def batch_transcribe(
    podcast: dict[str, Any],
    count: int,
    episodes: list[dict[str, Any]],
    parallel: int = 1,
):
    """Transcribe the last N episodes of a podcast and save to output/."""
    name = podcast["name"]
    total = min(count, len(episodes))
    if total == 0:
        print(f"   No episodes available for {name}.")
        return

    print(f"\n{'='*60}")
    print(f"   Batch transcribing {total} episodes of {name}")
    if parallel > 1:
        print(f"   Parallel workers: {parallel}")
    print(f"{'='*60}\n")

    api_keys = _get_api_keys()
    if not api_keys:
        print("   [ERROR] No GROQ_API_KEY found. Set GROQ_API_KEY in your environment.")
        print("   Fall back to local Whisper by installing faster-whisper.")
        return

    # Reverse: newest episodes first
    tasks = list(range(total - 1, -1, -1))

    success_count = 0
    future_map: dict[concurrent.futures.Future[bool], int] = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as pool:
        for i in tasks:
            ep = episodes[i]
            audio_url = ep.get("audio_url") or ""
            if not audio_url:
                continue
            future = pool.submit(
                _transcribe_job, "Batch", name, ep, total - i, total, api_keys
            )
            future_map[future] = total - i

        for future in concurrent.futures.as_completed(future_map):
            idx = future_map[future]
            try:
                if future.result():
                    success_count += 1
            except Exception as e:
                print(f"   [Batch] [ERROR] Episode {idx}: {e}")

    print(f"\n{'='*60}")
    print(f"   Done. {success_count}/{total} episodes transcribed successfully.")
    print(f"   Output: {OUTPUT_DIR / _slugify(name)}/")
    print(f"{'='*60}\n")


def _run_search_pipeline(
    registry: dict[str, Any],
    query: str | None,
    guest: str | None,
    podcast_name: str | None,
    auto_transcribe: bool,
    transcribe_count: int,
    parallel: int = 1,
):
    """Search across podcasts, optionally transcribe top results."""
    term = query or guest or ""
    if not term:
        print("   No search term provided.")
        return

    all_results: list[tuple[str, list[dict[str, Any]]]] = []

    for p in registry["podcasts"]:
        name = p["name"]
        if podcast_name and podcast_name.lower() not in name.lower():
            continue
        rss_urls = _get_rss_urls(p)
        if not rss_urls:
            continue

        episodes = fetch_rss_cached(rss_urls[0])
        if not episodes:
            continue

        matches = search_episodes(episodes, term)
        if matches:
            all_results.append((name, matches))
    if not auto_transcribe:
        _print_search_results(all_results)
        return

    # Auto-transcribe: pick top matches across all podcasts (up to transcribe_count)
    # Flatten and rank
    flat = []
    for pname, eps in all_results:
        for ep in eps:
            flat.append((pname, ep))
    # Deduplicate and limit
    seen_guids = set()
    picked = []
    for pname, ep in flat:
        guid = ep.get("guid") or ep.get("link") or ep.get("title", "")
        if guid not in seen_guids:
            seen_guids.add(guid)
            picked.append((pname, ep))
        if len(picked) >= transcribe_count:
            break

    if not picked:
        print("   No episodes found to transcribe.")
        return

    print(f"\n   Pipeline: searching for '{term}' → transcribing top {len(picked)} episode(s)\n")

    api_keys = _get_api_keys()
    if not api_keys:
        print("   [ERROR] No GROQ_API_KEY found. Set GROQ_API_KEY in your environment.")
        print("   Fall back to local Whisper by installing faster-whisper.")
        return

    success_count = 0
    future_map: dict[concurrent.futures.Future[bool], tuple[int, str]] = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as pool:
        for idx, (pname, ep) in enumerate(picked):
            audio_url = ep.get("audio_url") or ""
            if not audio_url:
                continue
            future = pool.submit(
                _transcribe_job, "Pipeline", pname, ep, idx + 1, len(picked), api_keys
            )
            future_map[future] = (idx + 1, pname)

        for future in concurrent.futures.as_completed(future_map):
            seq, pname = future_map[future]
            try:
                if future.result():
                    success_count += 1
            except Exception as e:
                print(f"   [Pipeline] [ERROR] ({seq}) {pname}: {e}")

    print(f"\n   Pipeline done. {success_count}/{len(picked)} transcribed.\n")


# -- Audio Download --------------------------------------------------

def download_audio(url: str, output_path: Path) -> bool:
    """Download an audio file from URL to output_path. Returns success."""
    print(f"   [DL] Downloading audio...")
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (podcast-transcript-skill/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=300) as resp:
            with open(output_path, "wb") as f:
                while chunk := resp.read(8192):
                    f.write(chunk)
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"   [OK] Downloaded ({size_mb:.1f} MB)")
        return True
    except Exception as e:
        print(f"   [ERROR] Download failed: {e}", file=sys.stderr)
        return False


# -- Tier 1: Direct Sources ------------------------------------------

def try_tier1(podcast: dict[str, Any], episode_query: str | None = None) -> str | None:
    """Try free direct sources for the podcast. Returns transcript or None."""
    sources = podcast.get("transcript_sources", {})
    print(f"\n   [Tier 1] Checking free sources for {podcast['name']}...")
    
    # 1a: GitHub archive (Lenny's Podcast)
    for source_key, source in sources.items():
        stype = source.get("type", "")
        
        if stype == "github_archive" and "repo" in source:
            print(f"   -> GitHub archive: {source['repo']} (clone separately for Tier 1)")
            # GitHub archive requires local clone; drop through to try other sources
        
        elif stype == "spokenmd_api":
            api_key = os.environ.get("SPOKENMD_API_KEY", source.get("demo_key", "pt_demo"))
            print(f"   -> Querying Spoken.md API...")
            try:
                req = urllib.request.Request(
                    f"{source['api_endpoint']}/transcripts",
                    headers={"Authorization": f"Bearer {api_key}"},
                )
                resp = urllib.request.urlopen(req, timeout=15)
                data = json.loads(resp.read())
                if data and "transcript" in data:
                    return data["transcript"]
            except Exception as e:
                print(f"   [WARN]  Spoken.md API failed: {e}")
    
    return None


# -- Tier 2: RSS + Whisper -------------------------------------------

def try_tier2(podcast: dict[str, Any], episode_query: str | None = None) -> str | None:
    """Download audio from RSS and transcribe via Whisper/Groq."""
    rss_url = podcast.get("rss")
    if not rss_url:
        print("   [WARN]  No RSS feed configured for this podcast")
        return None
    
    print(f"\n   [Tier 2] RSS -> Audio -> Transcription")
    episodes = fetch_rss(rss_url)
    if not episodes:
        print("   [ERROR] No episodes found in RSS feed")
        return None
    
    ep = find_episode(episodes, episode_query)
    if not ep:
        print("   [ERROR] Could not find matching episode")
        return None
    
    print(f"   Episode: {ep['title']}")
    
    audio_url = ep.get("audio_url")
    if not audio_url:
        print("   [ERROR] No audio URL in episode")
        return None
    
    # Download audio to temp file
    tmp_dir = Path(tempfile.mkdtemp(prefix="podcast_"))
    audio_path = tmp_dir / "episode.mp3"
    
    if not download_audio(audio_url, audio_path):
        return None
    
    try:
        # Check if Groq API key is available
        groq_key = os.environ.get("GROQ_API_KEY")
        if groq_key:
            return _transcribe_groq(audio_path)

        # Check if faster-whisper is available
        try:
            return _transcribe_local(audio_path)
        except ImportError:
            print("   [WARN]  No transcription backend available.")
            print("   Install one:")
            print("      Cloud (recommended): pip install groq && export GROQ_API_KEY=...")
            print("      Local:              pip install faster-whisper")
            print(f"   Audio saved at: {audio_path}")
            print(f"   Audio URL: {audio_url}")
            return None
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _compress_audio(path: Path, max_mb: int = 22) -> Path:
    """Compress audio to stay under Groq's 25 MB limit using ffmpeg."""
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb <= max_mb:
        return path
    
    compressed = path.with_suffix(".mp3").parent / f"{path.stem}_compressed.mp3"
    print(f"   [COMPRESS] {size_mb:.0f} MB -> target <{max_mb} MB")
    
    # Try ffmpeg (best quality)
    try:
        import subprocess
        bitrate = "32k"
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(path), "-ac", "1", "-ar", "16000",
             "-b:a", bitrate, str(compressed)],
            capture_output=True, timeout=120, check=True,
        )
        print(f"   [OK] Compressed ({compressed.stat().st_size / 1024 / 1024:.0f} MB)")
        return compressed
    except Exception:
        pass  # fall through
    
    # Fall back to pydub if available
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(path)
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(compressed, format="mp3", bitrate="32k")
        print(f"   [OK] Compressed via pydub ({compressed.stat().st_size / 1024 / 1024:.0f} MB)")
        return compressed
    except ImportError:
        pass
    
    # No compression tool available
    print(f"   [WARN] No compression tool found (ffmpeg/pydub).")
    print(f"   [WARN] File is {size_mb:.0f} MB; Groq limit is 25 MB.")
    print(f"   [WARN] Install ffmpeg or pydub for auto-compression.")
    return path


def _get_api_keys() -> list[str]:
    """Collect all available GROQ API keys from environment variables.
    
    Reads GROQ_API_KEY (base), GROQ_API_KEY_2, GROQ_API_KEY_3, etc.
    Returns a list of unique non-empty keys. If none found, returns [].
    """
    keys: list[str] = []
    seen: set[str] = set()
    
    # Base key always first
    base = os.environ.get("GROQ_API_KEY", "").strip()
    if base and base not in seen:
        keys.append(base)
        seen.add(base)
    
    # Scan for numbered keys
    idx = 2
    while True:
        val = os.environ.get(f"GROQ_API_KEY_{idx}", "").strip()
        if not val:
            break
        if val not in seen:
            keys.append(val)
            seen.add(val)
        idx += 1
    
    return keys


def _pick_key(api_keys: list[str], index: int) -> str | None:
    """Round-robin pick an API key from the list, or return None if empty."""
    if not api_keys:
        return None
    return api_keys[index % len(api_keys)]


def _transcribe_groq(audio_path: Path, api_key: str | None = None) -> str | None:
    """Transcribe audio using Groq's Whisper API.
    
    Args:
        audio_path: Path to the audio file.
        api_key: Optional explicit API key. If None, reads from GROQ_API_KEY env var.
    """
    groq_key = api_key or os.environ.get("GROQ_API_KEY")
    if not groq_key:
        print("   [ERROR] GROQ_API_KEY is not set. Export GROQ_API_KEY or use local Whisper (pip install faster-whisper).")
        return None
    
    print(f"   [Cloud] Transcribing via Groq Whisper API...")
    
    # Compress if needed (Groq limit: 25 MB)
    audio_path = _compress_audio(audio_path)
    
    try:
        import groq
        client = groq.Groq(api_key=groq_key)
        with open(audio_path, "rb") as f:
            transcription = client.audio.transcriptions.create(
                file=(audio_path.name, f.read()),
                model="whisper-large-v3-turbo",
            )
        print(f"   [OK] Transcription complete")
        return transcription.text
    except Exception as e:
        print(f"   [ERROR] Groq transcription failed: {e}", file=sys.stderr)
        return None


def _transcribe_local(audio_path: Path) -> str | None:
    """Transcribe audio using local faster-whisper."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("   [WARN]  faster-whisper not installed.")
        print("   Install: pip install faster-whisper")
        print("   Or use cloud: set GROQ_API_KEY env var")
        return None
    
    print(f"   [Local] Transcribing via faster-whisper (large-v3)...")
    print(f"   [WAIT] This may take a while on CPU...")
    try:
        model = WhisperModel("large-v3", device="cpu", compute_type="int8")
        segments, info = model.transcribe(str(audio_path))
        text_parts = []
        for seg in segments:
            text_parts.append(f"[{seg.start:.1f}s] {seg.text.strip()}")
        print(f"   [OK] Transcription complete ({len(text_parts)} segments)")
        return "\n".join(text_parts)
    except Exception as e:
        print(f"   [ERROR] Local transcription failed: {e}", file=sys.stderr)
        return None


# -- Tier 3: Taddy API -----------------------------------------------

def try_tier3(podcast: dict[str, Any], episode_query: str | None = None) -> str | None:
    """Try Taddy API for transcript."""
    api_key = os.environ.get("TADDY_API_KEY")
    if not api_key:
        print("\n   [WARN]  Tier 3: TADDY_API_KEY not set. Skipping Taddy API.")
        print("   Get a key at: https://taddy.org")
        return None
    
    print(f"\n   [Tier 3] Querying Taddy API...")
    
    # First search for the podcast UUID if not cached
    podcast_id = podcast.get("id")
    
    query = """
    mutation searchForPodcast($name: String!, $page: Int = 1) {
        searchForPodcast(name: $name, page: $page) {
            searchId
            searchResults {
                uuid
                name
                feedUrl
            }
        }
    }
    """
    
    payload = json.dumps({
        "query": query,
        "variables": {"name": podcast["name"]}
    }).encode()
    
    try:
        req = urllib.request.Request(
            "https://api.taddy.org",
            data=payload,
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json",
            },
        )
        resp = urllib.request.urlopen(req, timeout=30)
        data = json.loads(resp.read())
        
        results = data.get("data", {}).get("searchForPodcast", {}).get("searchResults", [])
        if not results:
            print("   [ERROR] Podcast not found on Taddy")
            return None
        
        podcast_uuid = results[0]["uuid"]
        
        # Now fetch the episode transcript
        ep_query = """
        query getEpisodes($podcastUuid: ID!, $page: Int = 1, $limit: Int = 50) {
            getEpisodes(uuid: $podcastUuid, page: $page, limit: $limit) {
                uuid
                name
                transcript
                audioUrl
            }
        }
        """
        
        ep_payload = json.dumps({
            "query": ep_query,
            "variables": {"podcastUuid": podcast_uuid, "limit": 50}
        }).encode()
        
        req2 = urllib.request.Request(
            "https://api.taddy.org",
            data=ep_payload,
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json",
            },
        )
        resp2 = urllib.request.urlopen(req2, timeout=30)
        ep_data = json.loads(resp2.read())
        
        episodes = ep_data.get("data", {}).get("getEpisodes", [])
        if not episodes:
            print("   [ERROR] No episodes found on Taddy")
            return None
        
        # Match episode
        ep = find_episode(
            [{"title": e.get("name", ""), "guid": e.get("uuid", ""),
              "pub_date": "", "description": "", "link": "", "audio_url": None}
             for e in episodes],
            episode_query
        )
        if ep is None:
            print("   [ERROR] Episode not found on Taddy")
            return None
        
        # Find the matching episode data
        for e in episodes:
            if e.get("uuid") == ep["guid"] or e.get("name") == ep["title"]:
                transcript = e.get("transcript")
                if transcript:
                    print(f"   [OK] Found transcript for: {e['name']}")
                    return transcript
                print("   [WARN]  Episode found but no transcript available on Taddy")
                return None
        
        return None
        
    except Exception as e:
        print(f"   [ERROR] Taddy API failed: {e}", file=sys.stderr)
        return None


# -- Output ----------------------------------------------------------

def output_transcript(text: str, podcast_name: str, episode_title: str | None, output_file: str | None = None):
    """Print or save the transcript."""
    if not text:
        print("\n[ERROR] No transcript found.", file=sys.stderr)
        return False
    
    header = f"== Transcript: {podcast_name}"
    if episode_title:
        header += f" -- {episode_title}"
    header += f"\n{'=' * 60}\n"
    
    content = header + text + "\n"
    
    if output_file:
        path = Path(output_file)
        path.write_text(content, encoding="utf-8")
        print(f"\n[OK] Transcript saved to: {path.resolve()}")
    else:
        print(content)
    
    return True


# -- CLI -------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Fetch transcripts from 5 supported podcasts using 3-tier approach.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Lenny's Podcast" --latest
  %(prog)s 20vc --episode "Marc Andreessen"
  %(prog)s dwarkesh --episode 15
  %(prog)s "cheeky pint" --latest --method whisper
  %(prog)s a16z --latest --output transcript.md
  %(prog)s --list-podcasts
        """,
    )
    parser.add_argument("podcast", nargs="?", help="Podcast name, slug, or partial match")
    parser.add_argument("--episode", "-e", default=None, help="Episode: title, number, or 'latest'")
    parser.add_argument("--latest", "-l", action="store_true", help="Get latest episode")
    parser.add_argument("--last", type=int, default=None, metavar="N",
                        help="Batch-transcribe last N episodes into output/ directory")
    parser.add_argument("--search", "-s", default=None, metavar="QUERY",
                        help="Search episodes by keyword in title/description across all podcasts")
    parser.add_argument("--guest", "-g", default=None, metavar="NAME",
                        help="Search episodes by guest name (alias for --search)")
    parser.add_argument("--transcribe", action="store_true",
                        help="With --search/--guest: auto-transcribe top matching episodes instead of listing")
    parser.add_argument("--transcribe-count", type=int, default=3, metavar="N",
                        help="Max episodes to transcribe in search pipeline (default: 3)")
    parser.add_argument("--method", "-m", choices=["auto", "tier1", "whisper", "taddy"], default="auto",
                        help="Transcription method (default: auto = try all tiers)")
    parser.add_argument("--parallel", type=int, default=1, metavar="N",
                        help="Parallel transcription workers (default: 1). Set >1 with multiple GROQ_API_KEY_N env vars.")
    parser.add_argument("--output", "-o", default=None, help="Save transcript to file")
    parser.add_argument("--list-podcasts", action="store_true", help="List available podcasts")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    registry = load_registry()
    
    # -- Feature: Search/guest across podcasts -----------------------
    if args.search or args.guest:
        podcasts = registry["podcasts"]
        term = args.search or args.guest or ""
        # If podcast name is given, filter to that podcast
        podcast_filter = args.podcast if args.podcast else None
        if podcast_filter:
            found = find_podcast(podcast_filter, registry)
            if found:
                podcast_filter = found["name"]
        
        auto_transcribe = args.transcribe
        _run_search_pipeline(registry, args.search, args.guest,
                             podcast_filter, auto_transcribe, args.transcribe_count,
                             parallel=args.parallel)
        return
    
    # -- Feature: Batch transcribe last N (requires podcast + --last) -
    if args.last is not None:
        if not args.podcast:
            print("[ERROR] --last requires a podcast name.")
            sys.exit(1)
        podcast = find_podcast(args.podcast, registry)
        if not podcast:
            print(f"[ERROR] Podcast '{args.podcast}' not found.")
            list_podcasts(registry)
            sys.exit(1)
        rss_urls = _get_rss_urls(podcast)
        if not rss_urls:
            print(f"[ERROR] No RSS feeds for {podcast['name']}")
            sys.exit(1)
        episodes = fetch_rss_cached(rss_urls[0])
        if not episodes:
            print(f"[ERROR] No episodes found via RSS for {podcast['name']}")
            sys.exit(1)
        batch_transcribe(podcast, args.last, episodes, parallel=args.parallel)
        return
    
    # -- Feature: List podcasts --------------------------------------
    if args.list_podcasts:
        list_podcasts(registry, as_json=args.json)
        return
    
    # -- Core: single-episode transcript -----------------------------
    if not args.podcast:
        parser.print_help()
        return
    
    podcast = find_podcast(args.podcast, registry)
    if not podcast:
        print(f"[ERROR] Podcast '{args.podcast}' not found.")
        print("   Available podcasts:")
        list_podcasts(registry)
        sys.exit(1)
    
    episode_query = args.episode or ("latest" if args.latest else None)
    
    print(f"\nGetting transcript for: {podcast['name']}")
    if episode_query and episode_query != "latest":
        print(f"   Episode query: {episode_query}")
    elif episode_query == "latest":
        print(f"   Episode: latest")
    
    transcript = None
    
    if args.method in ("auto", "tier1"):
        transcript = try_tier1(podcast, episode_query)
    
    if not transcript and args.method in ("auto", "whisper"):
        transcript = try_tier2(podcast, episode_query)
    
    if not transcript and args.method in ("auto", "taddy"):
        transcript = try_tier3(podcast, episode_query)
    
    if transcript:
        output_transcript(transcript, podcast["name"], episode_query, args.output)
    else:
        if args.method == "auto":
            print(f"\n[ERROR] Could not fetch transcript for {podcast['name']}.")
            print("   Tips:")
            print("   - For GitHub archive podcasts (Lenny's): clone the repo manually")
            print("   - Set GROQ_API_KEY for cloud Whisper transcription")
            print("   - Set TADDY_API_KEY for commercial API access")
        sys.exit(1 if not transcript else 0)


if __name__ == "__main__":
    main()
