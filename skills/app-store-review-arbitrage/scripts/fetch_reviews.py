#!/usr/bin/env python3
"""
fetch_reviews.py — Standalone review collector for app-store-review-arbitrage.

Usage:
    python3 scripts/fetch_reviews.py URL [options]

Options:
    --output PATH       Write JSON to PATH (default: /tmp/asr-raw.json)
    --stdout            Print JSON to stdout instead of writing a file
    --count N           Maximum reviews to collect (default: 200)
    --metadata-only     Fetch store metadata only; skip review collection
    --country CC        2-letter country code (default: extracted from URL or 'us')

Dependencies (pip install):
    google-play-scraper

App Store path uses stdlib urllib — no third-party package required.
No API keys required. All data sources are free and public.
"""

from __future__ import annotations
import argparse
import json
import re
import sys
import tempfile
from datetime import datetime, date
from pathlib import Path

DEFAULT_OUTPUT = str(Path(tempfile.gettempdir()) / "asr-raw.json")


# ---------------------------------------------------------------------------
# URL parsing
# ---------------------------------------------------------------------------

def parse_url(url: str) -> dict:
    """
    Detect platform and extract identifiers from an App Store or Google Play URL.

    Returns:
        {
            "platform": "app_store" | "google_play",
            "app_url": str,
            "app_id": str,           # numeric string (App Store) or package name (GP)
            "country": str,          # 2-letter code extracted from URL or None
        }

    Raises:
        ValueError: if the URL does not match either known pattern.
    """
    # App Store detection
    if "apps.apple.com" in url:
        # Extract numeric app ID (required)
        id_match = re.search(r"/id(\d+)", url)
        if not id_match:
            raise ValueError(
                f"Could not extract app ID from App Store URL: {url}\n"
                "Expected format: https://apps.apple.com/us/app/app-name/id1234567890"
            )
        app_id = id_match.group(1)

        # Extract country code (optional — e.g., /us/, /gb/, /in/)
        country_match = re.search(r"apps\.apple\.com/([a-z]{2})/", url)
        country = country_match.group(1) if country_match else None

        return {
            "platform": "app_store",
            "app_url": url,
            "app_id": app_id,
            "country": country,
        }

    # Google Play detection
    if "play.google.com" in url:
        pkg_match = re.search(r"[?&]id=([a-zA-Z0-9._]+)", url)
        if not pkg_match:
            raise ValueError(
                f"Could not extract package name from Google Play URL: {url}\n"
                "Expected format: https://play.google.com/store/apps/details?id=com.example.app"
            )
        package_name = pkg_match.group(1).split("&")[0]  # strip trailing params

        return {
            "platform": "google_play",
            "app_url": url,
            "app_id": package_name,
            "country": None,
        }

    raise ValueError(
        f"Unrecognised URL: {url}\n"
        "Provide a direct App Store URL (apps.apple.com) or "
        "Google Play URL (play.google.com/store/apps/details?id=...)."
    )


# ---------------------------------------------------------------------------
# Metadata fetching
# ---------------------------------------------------------------------------

def fetch_metadata_appstore(app_id: str) -> dict:
    """
    Fetch App Store metadata via the iTunes lookup API.
    No authentication required.

    Returns a normalized metadata dict. Sets store_description=None if missing.
    Raises RuntimeError on HTTP failure.
    """
    import urllib.request
    import urllib.error

    url = f"https://itunes.apple.com/lookup?id={app_id}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        raise RuntimeError(f"iTunes lookup failed for app_id={app_id}: {e}")

    if not data.get("results"):
        raise RuntimeError(
            f"iTunes lookup returned no results for app_id={app_id}. "
            "Verify the app ID is correct and the app is available in the US store."
        )

    r = data["results"][0]
    description = r.get("description", "").strip() or None

    return {
        "app_name": r.get("trackName", "Unknown"),
        "developer": r.get("artistName", "Unknown"),
        "platform": "app_store",
        "app_id": app_id,
        "version": r.get("version"),
        "average_rating": r.get("averageUserRating"),
        "total_ratings": r.get("userRatingCount"),
        "store_description": description,
        "fetched_at": date.today().isoformat(),
    }


def fetch_metadata_gplay(package_name: str) -> dict:
    """
    Fetch Google Play metadata via google-play-scraper.
    No authentication required.

    Returns a normalized metadata dict. Sets store_description=None if missing.
    Raises RuntimeError on exception.
    """
    try:
        from google_play_scraper import app as gp_app
    except ImportError:
        raise ImportError(
            "google-play-scraper is not installed.\n"
            "Run: pip install google-play-scraper"
        )

    try:
        r = gp_app(package_name, lang="en", country="us")
    except Exception as e:
        raise RuntimeError(
            f"google-play-scraper failed for package={package_name}: {e}\n"
            "This may be a temporary issue with Google Play's internal API. "
            "Try again in a few minutes, or run: pip install --upgrade google-play-scraper"
        )

    description = (r.get("description") or "").strip() or None

    return {
        "app_name": r.get("title", "Unknown"),
        "developer": r.get("developer", "Unknown"),
        "platform": "google_play",
        "app_id": package_name,
        "version": r.get("version"),
        "average_rating": r.get("score"),
        "total_ratings": r.get("ratings"),
        "store_description": description,
        "fetched_at": date.today().isoformat(),
    }


# ---------------------------------------------------------------------------
# Review collection
# ---------------------------------------------------------------------------

def fetch_reviews_appstore(app_id: str, count: int = 200,
                           country: str = "us") -> list:
    """
    Collect App Store reviews using iTunes RSS JSON API.
    Returns raw review dicts matching the structure expected by normalize_appstore.
    Raises RuntimeError if collection fails.
    """
    import urllib.request
    import urllib.error
    import time

    print(f"  Collecting App Store reviews (country={country}, max={count})...", file=sys.stderr)

    reviews = []
    page = 1

    # iTunes RSS feed returns up to 50 reviews per page, max 10 pages
    while len(reviews) < count and page <= 10:
        url = f"https://itunes.apple.com/{country}/rss/customerreviews/page={page}/id={app_id}/sortBy=mostRecent/json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as e:
            if page == 1:
                raise RuntimeError(f"iTunes RSS fetch failed for app_id={app_id}: {e}")
            break

        entries = data.get("feed", {}).get("entry")
        if not entries:
            break

        if isinstance(entries, list):
            for e in entries:
                if "author" in e and "im:rating" in e:
                    raw_rating = e.get("im:rating", {}).get("label")
                    try:
                        rating = int(raw_rating) if raw_rating is not None else None
                    except (TypeError, ValueError):
                        rating = None
                    reviews.append({
                        "rating": rating,
                        "review": e.get("content", {}).get("label", ""),
                        "title": e.get("title", {}).get("label"),
                        "date": e.get("updated", {}).get("label")
                    })
        elif isinstance(entries, dict):
            e = entries
            if "author" in e and "im:rating" in e:
                raw_rating = e.get("im:rating", {}).get("label")
                try:
                    rating = int(raw_rating) if raw_rating is not None else None
                except (TypeError, ValueError):
                    rating = None
                reviews.append({
                    "rating": rating,
                    "review": e.get("content", {}).get("label", ""),
                    "title": e.get("title", {}).get("label"),
                    "date": e.get("updated", {}).get("label")
                })

        page += 1
        time.sleep(0.5)

    reviews = reviews[:count]

    if not reviews:
        # Retry with 'us' if the original country returned nothing
        if country != "us":
            print("  No reviews returned. Retrying with country='us'...", file=sys.stderr)
            return fetch_reviews_appstore(
                app_id,
                count=count,
                country="us",
            )

        print(
            f"  [WARNING] iTunes RSS API returned 0 reviews for app_id={app_id}. "
            "The app may have no reviews or be region-restricted.", file=sys.stderr
        )
        return []

    print(f"  Collected {len(reviews)} raw reviews from App Store.", file=sys.stderr)
    return reviews


def fetch_reviews_gplay(package_name: str, count: int = 200) -> list:
    """
    Collect Google Play reviews using google-play-scraper.
    Returns raw review dicts from the package.
    Raises ImportError if package missing, RuntimeError if collection fails.
    """
    try:
        from google_play_scraper import reviews as gp_reviews, Sort
    except ImportError:
        raise ImportError(
            "google-play-scraper is not installed.\n"
            "Run: pip install google-play-scraper"
        )

    print(f"  Collecting Google Play reviews (max={count})...", file=sys.stderr)

    try:
        result, _ = gp_reviews(
            package_name,
            lang="en",
            country="us",
            sort=Sort.NEWEST,
            count=count,
        )
    except Exception as e:
        raise RuntimeError(
            f"google-play-scraper failed for package={package_name}: {e}\n"
            "This may be a temporary issue with Google Play's internal API. "
            "Try again in a few minutes, or run: pip install --upgrade google-play-scraper"
        )

    print(f"  Collected {len(result)} raw reviews from Google Play.", file=sys.stderr)
    return result


# ---------------------------------------------------------------------------
# Schema normalization
# ---------------------------------------------------------------------------

def _date_to_str(value) -> str:
    """Convert a datetime, date, or ISO string to YYYY-MM-DD string."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        try:
            return datetime.strptime(value[:10], "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            pass
    return str(value)[:10]  # last resort


def normalize_appstore(raw_reviews: list) -> list:
    """
    Map App Store review dicts to the normalized schema.

    Normalized fields: rating, body, title, date, platform
    """
    normalized = []
    for r in raw_reviews:
        normalized.append({
            "rating": int(r.get("rating") or 0),
            "body": str(r.get("review", "") or ""),
            "title": r.get("title") or None,
            "date": _date_to_str(r.get("date", "")),
            "platform": "app_store",
        })
    return normalized


def normalize_gplay(raw_reviews: list) -> list:
    """
    Map Google Play review dicts to the normalized schema.

    score → rating, content → body, at → date, platform = 'google_play'
    thumbsUpCount is stored separately — not in normalized core fields (v2 use).
    """
    normalized = []
    for r in raw_reviews:
        normalized.append({
            "rating": int(r.get("score", 0)),
            "body": str(r.get("content", "") or ""),
            "title": None,  # Google Play has no review title field
            "date": _date_to_str(r.get("at", "")),
            "platform": "google_play",
            # thumbsUpCount stored for v2 — not used in v1 scoring formula
            "_thumbsUpCount": r.get("thumbsUpCount", 0),
        })
    return normalized


# ---------------------------------------------------------------------------
# Stats and filtering
# ---------------------------------------------------------------------------

def compute_date_range(reviews: list) -> dict:
    """Return oldest and newest date from a list of normalized reviews."""
    if not reviews:
        return {"oldest": None, "newest": None}
    dates = [r["date"] for r in reviews if r.get("date")]
    if not dates:
        return {"oldest": None, "newest": None}
    dates.sort()
    return {"oldest": dates[0], "newest": dates[-1]}


def filter_low_star(reviews: list, max_rating: int = 3) -> list:
    """Return only reviews with rating <= max_rating."""
    return [r for r in reviews if r.get("rating", 5) <= max_rating]


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

def collect(url: str, count: int = 200, country_override: str | None = None,
            metadata_only: bool = False, input_fixture: str | None = None) -> dict:
    """
    Full collection pipeline for one app URL.

    Returns the asr-raw.json payload dict.
    Applies Gate 1 and raises SystemExit with a diagnostic message if triggered.
    """
    if input_fixture:
        print(f"\n[app-store-review-arbitrage] Loading fixture: {input_fixture}", file=sys.stderr)
        with open(input_fixture, "r", encoding="utf-8") as f:
            result = json.load(f)
        
        # Re-evaluate Gate 1
        result.setdefault("collection_stats", {})
        stats = result["collection_stats"]
        if stats.get("low_star_count", 0) < 10:
            msg = (
                f"\n[GATE 1 — LOW SIGNAL] Only {stats.get('low_star_count', 0)} low-star review(s) "
                f"found for this app (minimum required: 10).\n"
                "The app may be too new, too niche, or have unusually strong ratings.\n"
                "Try a more established competitor with more review history.\n"
            )
            result["collection_stats"]["gate_triggered"] = "gate_1_low_signal"
            result["gate_message"] = msg.strip()
        return result

    # Step 1: Parse URL
    parsed = parse_url(url)
    platform = parsed["platform"]
    app_id = parsed["app_id"]
    country = country_override or parsed.get("country") or "us"

    print(f"\n[app-store-review-arbitrage] Starting collection", file=sys.stderr)
    print(f"  Platform : {platform}", file=sys.stderr)
    print(f"  App ID   : {app_id}", file=sys.stderr)

    # Step 2: Fetch metadata
    print("  Fetching store metadata...", file=sys.stderr)
    if platform == "app_store":
        metadata = fetch_metadata_appstore(app_id)
    else:
        metadata = fetch_metadata_gplay(app_id)

    if not metadata.get("store_description"):
        print("  WARNING: Store description is empty or unavailable. "
              "Broken promise detection will produce a degraded note in Section 2.",
              file=sys.stderr)

    if metadata_only:
        return {
            "metadata": metadata,
            "all_reviews": [],
            "low_star_reviews": [],
            "collection_stats": {
                "total_fetched": 0,
                "low_star_count": 0,
                "platform": platform,
                "package": "itunes-rss-api" if platform == "app_store" else "google-play-scraper",
                "metadata_only": True,
                "date_range": {"oldest": None, "newest": None},
            },
        }

    # Step 3: Fetch and normalize reviews
    if platform == "app_store":
        raw = fetch_reviews_appstore(app_id, count=count, country=country)
        all_reviews = normalize_appstore(raw)
        package_name = "itunes-rss-api"
    else:
        raw = fetch_reviews_gplay(app_id, count=count)
        all_reviews = normalize_gplay(raw)
        package_name = "google-play-scraper"

    low_star_reviews = filter_low_star(all_reviews)
    date_range = compute_date_range(all_reviews)

    stats = {
        "total_fetched": len(all_reviews),
        "low_star_count": len(low_star_reviews),
        "platform": platform,
        "package": package_name,
        "date_range": date_range,
    }

    if platform == "app_store" and len(all_reviews) == 0:
        stats["warning"] = "iTunes RSS returned 0 reviews"

    print(f"  Total reviews   : {stats['total_fetched']}", file=sys.stderr)
    print(f"  Low-star (1–3★) : {stats['low_star_count']}", file=sys.stderr)

    # Gate 1: Low-signal stop
    if stats["low_star_count"] < 10:
        msg = (
            f"\n[GATE 1 — LOW SIGNAL] Only {stats['low_star_count']} low-star review(s) "
            f"found for this app (minimum required: 10).\n"
            "The app may be too new, too niche, or have unusually strong ratings.\n"
            "Try a more established competitor with more review history.\n"
        )
        # Write minimal output so the caller knows gate was triggered
        return {
            "metadata": metadata,
            "all_reviews": all_reviews,
            "low_star_reviews": low_star_reviews,
            "collection_stats": {**stats, "gate_triggered": "gate_1_low_signal"},
            "gate_message": msg.strip(),
        }

    return {
        "metadata": metadata,
        "all_reviews": all_reviews,
        "low_star_reviews": low_star_reviews,
        "collection_stats": stats,
    }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Collect App Store or Google Play reviews for app-store-review-arbitrage.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("url", help="App Store or Google Play URL")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                        help=f"Output file path (default: {DEFAULT_OUTPUT})")
    parser.add_argument("--input", default=None,
                        help="Load reviews from a local JSON fixture file (skips fetching)")
    parser.add_argument("--stdout", action="store_true",
                        help="Print JSON to stdout instead of writing a file")
    parser.add_argument("--count", type=int, default=200,
                        help="Maximum reviews to collect (default: 200)")
    parser.add_argument("--metadata-only", action="store_true",
                        help="Fetch metadata only, skip review collection")
    parser.add_argument("--country", default=None,
                        help="2-letter country code override (default: extracted from URL or 'us')")
    args = parser.parse_args()

    try:
        result = collect(
            url=args.url,
            count=args.count,
            country_override=args.country,
            metadata_only=args.metadata_only,
            input_fixture=args.input,
        )
    except FileNotFoundError as e:
        print(f"\n[ERROR] Fixture file not found: {e}", file=sys.stderr)
        sys.exit(1)
    except (ValueError, RuntimeError, ImportError) as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    # Gate 1 triggered — still write output so SKILL.md can read the gate message
    gate_triggered = result.setdefault("collection_stats", {}).get("gate_triggered")

    output_json = json.dumps(result, indent=2, default=str)

    if args.stdout:
        print(output_json)
    else:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_json, encoding="utf-8")
        print(f"\n[app-store-review-arbitrage] Output written to {output_path}", file=sys.stderr)

    if gate_triggered == "gate_1_low_signal":
        print(result.get("gate_message", ""), file=sys.stderr)
        sys.exit(2)  # Exit code 2 = gate triggered (not an error, not success)


if __name__ == "__main__":
    main()
