"""
research.py -- two-phase data collector for pricing-finder.

Phase 1 (discover): finds competitor candidates via DuckDuckGo search.
Phase 2 (fetch-pricing): fetches each competitor's pricing page with 3-tier fallback.

Uses only free dependencies -- no API keys required.
Optional: --tavily-key (better search), --firecrawl-key (better JS rendering).

Usage:
  # Phase 1
  python3 scripts/research.py \
      --phase discover \
      --product-analysis /tmp/pf-product-analysis.json \
      --output /tmp/pf-competitors-raw.json

  # Phase 2
  python3 scripts/research.py \
      --phase fetch-pricing \
      --competitors /tmp/pf-competitors-confirmed.json \
      --output /tmp/pf-pricing-raw.json
"""

import argparse
import json
import os
import random
import ssl
import sys
import time
import urllib.request
from datetime import date
from urllib.parse import urlparse

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None

try:
    import requests
    import html2text
    from bs4 import BeautifulSoup
except ImportError:
    requests = None
    html2text = None
    BeautifulSoup = None

_ssl_ctx = ssl._create_unverified_context()
quiet = False

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
]


def log(msg):
    if not quiet:
        print(msg, file=sys.stderr)


def random_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }


# ---------------------------------------------------------------------------
# Search: DuckDuckGo (free) or Tavily (optional upgrade)
# ---------------------------------------------------------------------------

def ddg_search(query, max_results=8):
    """DuckDuckGo search. Returns list of {title, url, snippet}."""
    if DDGS is None:
        log("  ERROR: duckduckgo_search not installed. Run: pip install duckduckgo-search")
        return []
    log(f"  DDG search: {query[:80]}")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return [
            {
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", "")[:300],
            }
            for r in results
        ]
    except Exception as e:
        log(f"  DDG error: {e}")
        return []


def tavily_search(query, key, max_results=8):
    """Tavily search (optional upgrade). Returns same format as ddg_search."""
    log(f"  Tavily search: {query[:80]}")
    try:
        payload = json.dumps({
            "api_key": key,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
        }).encode()
        req = urllib.request.Request(
            "https://api.tavily.com/search",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=25, context=_ssl_ctx) as resp:
            data = json.loads(resp.read())
        return [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("content", "")[:300],
            }
            for r in data.get("results", [])
        ]
    except Exception as e:
        log(f"  Tavily error: {e}")
        return []


def search(query, tavily_key=None, max_results=8):
    """Use Tavily if key provided, otherwise DuckDuckGo."""
    if tavily_key:
        results = tavily_search(query, tavily_key, max_results)
        if results:
            return results
    return ddg_search(query, max_results)


# ---------------------------------------------------------------------------
# Fetch: requests+BS4 (free) or Firecrawl (optional upgrade)
# ---------------------------------------------------------------------------

def fetch_url_bs4(url, timeout=20):
    """Fetch URL with requests + html2text. Returns (markdown, status)."""
    if requests is None or html2text is None:
        return "", "requests/html2text not installed"
    try:
        resp = requests.get(
            url,
            headers=random_headers(),
            timeout=timeout,
            allow_redirects=True,
        )
        if resp.status_code != 200:
            return "", f"HTTP {resp.status_code}"
        converter = html2text.HTML2Text()
        converter.ignore_links = False
        converter.ignore_images = True
        converter.body_width = 0
        md = converter.handle(resp.text)
        return md[:8000], "ok"
    except Exception as e:
        return "", str(e)


_GOOGLE_INTERSTITIAL_SIGNALS = [
    "if you are not redirected",
    "please click here",
    "accounts.google.com/ServiceLogin",
]


def fetch_google_cache(url, timeout=20):
    """Try Google cache as fallback for blocked pages."""
    cache_url = f"https://webcache.googleusercontent.com/search?q=cache:{url}&hl=en"
    content, status = fetch_url_bs4(cache_url, timeout)
    if content and any(sig in content for sig in _GOOGLE_INTERSTITIAL_SIGNALS):
        return "", "google_cache_interstitial"
    return content, status


def fetch_firecrawl(url, key, timeout=30):
    """Firecrawl fetch (optional upgrade)."""
    try:
        payload = json.dumps({
            "url": url,
            "formats": ["markdown"],
            "onlyMainContent": True,
        }).encode()
        req = urllib.request.Request(
            "https://api.firecrawl.dev/v1/scrape",
            data=payload,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout, context=_ssl_ctx) as resp:
            data = json.loads(resp.read())
        content = data.get("data", {}).get("markdown", "") or data.get("markdown", "")
        return content[:8000], "ok"
    except Exception as e:
        return "", str(e)


def infer_pricing_urls(base_url):
    """Return a list of candidate pricing page URLs from the base URL."""
    try:
        parsed = urlparse(base_url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        return [
            f"{base}/pricing",
            f"{base}/plans",
            f"{base}/price",
            f"{base}/pricing/",
        ]
    except Exception:
        return []


def build_result(name, pricing_url, content, source, quality, note=None):
    result = {
        "name": name,
        "pricing_url": pricing_url,
        "content": content,
        "content_length": len(content),
        "source": source,
        "data_quality": quality,
    }
    if note:
        result["data_quality_note"] = note
    return result


# ---------------------------------------------------------------------------
# Phase 1: competitor discovery
# ---------------------------------------------------------------------------

def run_discover(product_analysis, tavily_key=None):
    name = product_analysis.get("product_name", "")
    l2 = product_analysis.get("industry_taxonomy", {}).get("l2", "")
    l3 = product_analysis.get("industry_taxonomy", {}).get("l3", "")

    log(f"\nPhase 1: competitor discovery for '{name}'")
    log(f"  taxonomy: {l2} > {l3}")

    q1 = f"{name} competitors alternatives {l3}"
    q2 = f"{l2} {l3} software tool pricing plans"

    r1 = search(q1, tavily_key, max_results=8)
    r2 = search(q2, tavily_key, max_results=8)

    log(f"  Q1 results: {len(r1)}")
    log(f"  Q2 results: {len(r2)}")
    log("Phase 1 complete.")

    return {
        "date": str(date.today()),
        "product_name": name,
        "competitor_searches": [
            {"query": q1, "results": r1},
            {"query": q2, "results": r2},
        ],
    }


# ---------------------------------------------------------------------------
# Phase 2: fetch pricing pages
# ---------------------------------------------------------------------------

def fetch_pricing_page(competitor, firecrawl_key=None, tavily_key=None):
    name = competitor.get("name", "")
    pricing_url = competitor.get("pricing_url", "")
    base_url = competitor.get("url", "")

    log(f"\n  Fetching pricing: {name}")

    # Build URL candidates: explicit pricing URL first, then inferred
    url_candidates = []
    if pricing_url:
        url_candidates.append(pricing_url)
    url_candidates.extend(infer_pricing_urls(base_url))
    # Deduplicate while preserving order
    seen = set()
    url_candidates = [u for u in url_candidates if u and not (u in seen or seen.add(u))]

    for url in url_candidates:
        # Try 1: Firecrawl (if key provided)
        if firecrawl_key:
            content, status = fetch_firecrawl(url, firecrawl_key)
            if len(content) > 500:
                log(f"    firecrawl OK: {len(content)} chars from {url}")
                return build_result(name, url, content, "firecrawl", "high")
            log(f"    firecrawl: {status} ({len(content)} chars)")

        # Try 2: requests + BS4 (free)
        content, status = fetch_url_bs4(url)
        if len(content) > 500:
            log(f"    requests OK: {len(content)} chars from {url}")
            return build_result(name, url, content, "requests", "high")
        log(f"    requests: {status} ({len(content)} chars)")

        # Try 3: Google cache
        content, status = fetch_google_cache(url)
        if len(content) > 500:
            log(f"    google_cache OK: {len(content)} chars from {url}")
            return build_result(name, url, content, "google_cache", "medium")
        log(f"    google_cache: {status} ({len(content)} chars)")

        time.sleep(1)

    # Final fallback: DuckDuckGo / Tavily search snippet
    log(f"    All fetch attempts failed. Using search snippet fallback.")
    fallback_query = f'"{name}" pricing plans cost per month tiers'
    results = search(fallback_query, tavily_key, max_results=5)
    snippet = " ".join(r.get("snippet", "") for r in results)[:3000]
    return build_result(
        name, pricing_url, snippet, "search_snippet", "low",
        note="Pricing page fetch failed. Data from search snippets only -- prices may be incomplete."
    )


def run_fetch_pricing(confirmed_competitors, firecrawl_key=None, tavily_key=None):
    log(f"\nPhase 2: fetching pricing pages for {len(confirmed_competitors)} competitors")

    results = []
    for comp in confirmed_competitors:
        result = fetch_pricing_page(comp, firecrawl_key, tavily_key)
        results.append(result)
        time.sleep(1.5)  # polite crawl delay

    log("\nPhase 2 complete.")
    return {
        "date": str(date.today()),
        "competitors_fetched": len(confirmed_competitors),
        "results": results,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    global quiet

    parser = argparse.ArgumentParser(description="pricing-finder research script")
    parser.add_argument(
        "--phase",
        required=True,
        choices=["discover", "fetch-pricing"],
        help="Which phase to run",
    )
    parser.add_argument(
        "--product-analysis",
        required=True,
        help="Path to pf-product-analysis.json",
    )
    parser.add_argument(
        "--competitors",
        default="",
        help="Path to pf-competitors-confirmed.json (Phase 2 only)",
    )
    parser.add_argument(
        "--tavily-key",
        default=os.environ.get("TAVILY_API_KEY", ""),
        help="Tavily API key for upgraded search (optional)",
    )
    parser.add_argument(
        "--firecrawl-key",
        default=os.environ.get("FIRECRAWL_API_KEY", ""),
        help="Firecrawl API key for upgraded JS rendering (optional)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to write JSON output",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output to stderr",
    )
    args = parser.parse_args()
    quiet = args.quiet

    # Dependency check
    if DDGS is None and not args.tavily_key:
        print(
            "ERROR: duckduckgo_search not installed and no Tavily key provided.\n"
            "Run: pip install duckduckgo-search requests beautifulsoup4 html2text",
            file=sys.stderr,
        )
        sys.exit(1)

    if not os.path.exists(args.product_analysis):
        print(f"ERROR: {args.product_analysis} not found", file=sys.stderr)
        sys.exit(1)

    with open(args.product_analysis) as f:
        product_analysis = json.load(f)

    if args.phase == "discover":
        output = run_discover(product_analysis, args.tavily_key or None)

    elif args.phase == "fetch-pricing":
        if not args.competitors:
            print("ERROR: --competitors required for fetch-pricing phase", file=sys.stderr)
            sys.exit(1)
        if not os.path.exists(args.competitors):
            print(f"ERROR: {args.competitors} not found", file=sys.stderr)
            sys.exit(1)
        with open(args.competitors) as f:
            competitors_data = json.load(f)
        confirmed = competitors_data.get("confirmed_competitors", [])
        if not confirmed:
            print("ERROR: no confirmed_competitors in input file", file=sys.stderr)
            sys.exit(1)
        output = run_fetch_pricing(
            confirmed,
            firecrawl_key=args.firecrawl_key or None,
            tavily_key=args.tavily_key or None,
        )

    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)
    log(f"\nOutput written to {args.output}")

    # Print summary to stdout for SKILL.md to display
    if args.phase == "discover":
        total = sum(len(s["results"]) for s in output["competitor_searches"])
        print(f"Discover complete: {len(output['competitor_searches'])} queries, {total} total results")
    else:
        print(f"Fetch complete: {output['competitors_fetched']} competitors")
        for r in output.get("results", []):
            quality_label = {"high": "GOOD", "medium": "OK", "low": "SNIPPET ONLY"}.get(
                r["data_quality"], r["data_quality"]
            )
            print(f"  {r['name']:22} {r['source']:15} {r['content_length']:5} chars  [{quality_label}]")


if __name__ == "__main__":
    main()
