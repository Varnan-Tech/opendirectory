#!/usr/bin/env python3
"""
scrape_pricing.py — Pricing Page Scraper
Part of: pricing-page-psychology-audit skill
Author: ajaycodesitbetter

Usage:
    python scripts/scrape_pricing.py "https://linear.app/pricing"

Output:
    Structured plain-text to stdout for AI analysis.
    Errors are printed to stderr so stdout stays clean.
"""

import os
import sys
import re
import requests
from bs4 import BeautifulSoup


# ── Constants ────────────────────────────────────────────────────────────────

TIMEOUT_SECONDS = int(os.environ.get("SCRAPE_TIMEOUT", 15))

# Browser-like headers to reduce bot-blocking (no API key needed)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Allow env var override of User-Agent (e.g. for custom scraping setups)
_custom_ua = os.environ.get("SCRAPE_USER_AGENT")
if _custom_ua:
    HEADERS["User-Agent"] = _custom_ua

# HTML tags that carry pricing-relevant content
CONTENT_TAGS = ["h1", "h2", "h3", "h4", "p", "li", "span", "button", "a"]


# ── Helpers ──────────────────────────────────────────────────────────────────

def clean(text: str) -> str:
    """Strip extra whitespace and blank lines from a string."""
    return re.sub(r"\s+", " ", text).strip()


def validate_url(url: str) -> bool:
    """Return True if the URL looks valid (starts with http/https)."""
    return url.startswith("http://") or url.startswith("https://")


def fetch_page(url: str) -> str:
    """
    Fetch the raw HTML of a URL.
    Raises a descriptive RuntimeError on failure.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.text

    except requests.exceptions.MissingSchema:
        raise RuntimeError(f"Invalid URL format: '{url}'. Include http:// or https://")

    except requests.exceptions.ConnectionError:
        raise RuntimeError(f"Could not connect to '{url}'. Check the URL or your internet.")

    except requests.exceptions.Timeout:
        raise RuntimeError(f"Request timed out after {TIMEOUT_SECONDS}s for '{url}'.")

    except requests.exceptions.HTTPError as e:
        code = e.response.status_code
        if code == 403:
            raise RuntimeError(
                f"Access blocked (HTTP 403) — '{url}' may have bot protection. "
                "Try opening it in a browser and using the page source manually."
            )
        raise RuntimeError(f"HTTP error {code} for '{url}': {e}")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Unexpected request error for '{url}': {e}")


# ── Extraction ────────────────────────────────────────────────────────────────

def extract_page_title(soup: BeautifulSoup) -> str:
    """Get the <title> tag text."""
    tag = soup.find("title")
    return clean(tag.get_text()) if tag else "No title found"


def extract_buttons(soup: BeautifulSoup) -> list:
    """
    Extract all button and CTA link text.
    Targets <button> tags and <a> tags with common CTA class names.
    """
    buttons = []

    # All <button> elements
    for btn in soup.find_all("button"):
        text = clean(btn.get_text())
        if text:
            buttons.append(text)

    # <a> tags that look like CTAs (common class keywords)
    cta_keywords = ["btn", "button", "cta", "action", "signup", "start", "trial"]
    for link in soup.find_all("a", href=True):
        classes = " ".join(link.get("class", [])).lower()
        if any(kw in classes for kw in cta_keywords):
            text = clean(link.get_text())
            if text:
                buttons.append(text)

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for b in buttons:
        if b.lower() not in seen:
            seen.add(b.lower())
            unique.append(b)

    return unique


def extract_prices(soup: BeautifulSoup) -> list:
    """
    Extract price strings using regex on page text.
    Catches formats like: $49, $49/mo, $49/month, EUR99, GBP19.99, Free
    """
    text = soup.get_text(" ", strip=True)
    price_pattern = re.compile(
        r"(Free|free|\$[\d,.]+(?:/\w+)?|€[\d,.]+(?:/\w+)?|£[\d,.]+(?:/\w+)?|"
        r"[\d,.]+\s*(?:USD|EUR|GBP)(?:/\w+)?)"
    )
    matches = price_pattern.findall(text)

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for m in matches:
        val = m.strip()
        if val.lower() not in seen:
            seen.add(val.lower())
            unique.append(val)

    return unique


def extract_plan_names(soup: BeautifulSoup) -> list:
    """
    Extract likely plan/tier names from headings and elements
    with pricing-related class names.
    """
    plan_keywords = ["plan", "tier", "pricing", "package"]
    candidates = []

    # Check headings inside pricing-related sections
    for tag in soup.find_all(["h2", "h3", "h4"]):
        parent = tag.find_parent()
        parent_classes = " ".join(parent.get("class", [])).lower() if parent else ""
        if any(kw in parent_classes for kw in plan_keywords):
            text = clean(tag.get_text())
            if text and len(text) < 50:  # plan names are short
                candidates.append(text)

    # Also grab standalone headings that look like tier names
    tier_hints = re.compile(
        r"^(free|starter|basic|pro|growth|scale|business|enterprise|team|"
        r"plus|premium|advanced|essentials|standard)$",
        re.IGNORECASE,
    )
    for tag in soup.find_all(["h2", "h3", "h4", "span", "p"]):
        text = clean(tag.get_text())
        if tier_hints.match(text):
            candidates.append(text)

    # Deduplicate
    seen = set()
    unique = []
    for c in candidates:
        if c.lower() not in seen:
            seen.add(c.lower())
            unique.append(c)

    return unique


def extract_features(soup: BeautifulSoup) -> list:
    """
    Extract feature list items — typically <li> elements inside
    pricing card sections.
    """
    features = []
    for li in soup.find_all("li"):
        text = clean(li.get_text())
        # Feature items are usually one short line
        if text and 3 < len(text) < 120:
            features.append(text)

    # Deduplicate
    seen = set()
    unique = []
    for f in features:
        if f.lower() not in seen:
            seen.add(f.lower())
            unique.append(f)

    return unique[:60]  # Cap at 60 to keep output focused


def extract_all_text(soup: BeautifulSoup) -> str:
    """
    Extract all visible text in document order for full-context analysis.
    Removes <script>, <style>, <nav>, <footer> noise.
    """
    # Remove noisy tags
    for tag in soup(["script", "style", "nav", "footer", "noscript", "meta"]):
        tag.decompose()

    lines = []
    for tag in soup.find_all(CONTENT_TAGS):
        text = clean(tag.get_text())
        if text and len(text) > 2:
            lines.append(text)

    # Deduplicate consecutive duplicates (common in SPAs)
    deduped = []
    prev = None
    for line in lines:
        if line != prev:
            deduped.append(line)
            prev = line

    return "\n".join(deduped)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Validate arguments
    if len(sys.argv) < 2:
        print("ERROR: No URL provided.", file=sys.stderr)
        print("Usage: python scripts/scrape_pricing.py <URL>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1].strip()

    if not validate_url(url):
        print(f"ERROR: Invalid URL '{url}'. Must start with http:// or https://", file=sys.stderr)
        sys.exit(1)

    # Fetch the page
    try:
        html = fetch_page(url)
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse HTML
    soup = BeautifulSoup(html, "html.parser")

    # Extract structured data
    title      = extract_page_title(soup)
    buttons    = extract_buttons(soup)
    prices     = extract_prices(soup)
    plan_names = extract_plan_names(soup)
    features   = extract_features(soup)
    all_text   = extract_all_text(soup)

    # ── Output to stdout (clean structured text for AI) ──────────────────────
    separator = "\u2500" * 60

    print(f"PAGE TITLE: {title}")
    print(f"URL: {url}")
    print(separator)

    print("\n## PLAN NAMES DETECTED")
    if plan_names:
        for name in plan_names:
            print(f"  - {name}")
    else:
        print("  (none detected — check page structure)")

    print("\n## PRICES DETECTED")
    if prices:
        for price in prices:
            print(f"  - {price}")
    else:
        print("  (none detected — page may use dynamic pricing)")

    print("\n## CTA BUTTON TEXT")
    if buttons:
        for btn in buttons:
            print(f"  - {btn}")
    else:
        print("  (none detected)")

    print("\n## FEATURE LIST ITEMS")
    if features:
        for feat in features[:30]:  # Show top 30 for readability
            print(f"  - {feat}")
    else:
        print("  (none detected)")

    print(f"\n{separator}")
    print("## FULL PAGE TEXT (for AI analysis)")
    print(separator)
    print(all_text)


if __name__ == "__main__":
    main()
