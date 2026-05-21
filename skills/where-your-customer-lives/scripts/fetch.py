#!/usr/bin/env python3
"""
where-your-customer-lives fetch script
Discovers channels where your ICP gathers via signal-trace + competitor layer.
No required API keys. GITHUB_TOKEN optional (improves competitor layer rate limits).

Usage:
    python3 scripts/fetch.py "startup gtm" --icp-role "technical co-founders" --icp-pain "customer acquisition"
    python3 scripts/fetch.py "devops tools" --competitors "Datadog,Grafana" --output /tmp/wcl-raw.json
    GITHUB_TOKEN=your_token python3 scripts/fetch.py "B2B sales" --competitors "Clay,Apollo" --stdout
"""

import argparse
import json
import math
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

_ssl_ctx = ssl._create_unverified_context()

TODAY = datetime.now(timezone.utc)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
quiet = False


# ---------------------------------------------------------------------------
# HTTP helpers (verbatim from map-your-market)
# ---------------------------------------------------------------------------

def fetch_json(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers=headers or {})
    req.add_header("User-Agent", "where-your-customer-lives/1.0")
    try:
        with urllib.request.urlopen(req, context=_ssl_ctx, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if not quiet:
            print(f"  HTTP {e.code}: {url[:80]}", file=sys.stderr)
        return None
    except Exception as e:
        if not quiet:
            print(f"  Error: {e} -- {url[:80]}", file=sys.stderr)
        return None


def fetch_html(url, timeout=20):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (compatible; where-your-customer-lives/1.0)")
    req.add_header("Accept", "text/html,application/xhtml+xml")
    try:
        with urllib.request.urlopen(req, context=_ssl_ctx, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        if not quiet:
            print(f"  HTML fetch error: {e} -- {url[:80]}", file=sys.stderr)
        return ""


def gh_get(path):
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return fetch_json(f"https://api.github.com{path}", headers=headers)


# ---------------------------------------------------------------------------
# Subreddit detection (verbatim from map-your-market)
# ---------------------------------------------------------------------------

SUBREDDIT_MAP = {
    "devops": ["devops", "sysadmin", "aws", "kubernetes", "docker"],
    "observability": ["devops", "sysadmin", "dataengineering", "CloudArchitects"],
    "monitoring": ["devops", "sysadmin", "networking", "aws"],
    "analytics": ["analytics", "dataengineering", "datascience", "BusinessIntelligence"],
    "b2b": ["startups", "entrepreneur", "SaaS", "smallbusiness"],
    "saas": ["SaaS", "startups", "entrepreneur", "microsaas"],
    "developer": ["programming", "webdev", "ExperiencedDevs", "devops"],
    "developer tools": ["programming", "webdev", "devops", "ExperiencedDevs"],
    "api": ["webdev", "programming", "devops", "node"],
    "security": ["netsec", "cybersecurity", "devops", "sysadmin"],
    "data": ["dataengineering", "datascience", "analytics", "BusinessIntelligence"],
    "database": ["dataengineering", "Database", "PostgreSQL", "learnprogramming"],
    "auth": ["webdev", "programming", "netsec", "node"],
    "payments": ["webdev", "programming", "entrepreneur", "ecommerce"],
    "ecommerce": ["ecommerce", "entrepreneur", "shopify", "startups"],
    "marketing": ["marketing", "digital_marketing", "entrepreneur", "startups"],
    "gtm": ["startups", "entrepreneur", "sales", "marketing"],
    "go-to-market": ["startups", "entrepreneur", "sales", "marketing"],
    "crm": ["sales", "salesforce", "entrepreneur", "smallbusiness"],
    "sales": ["sales", "entrepreneur", "startups", "smallbusiness"],
    "hr": ["humanresources", "remotework", "startups", "smallbusiness"],
    "finance": ["personalfinance", "accounting", "startups", "smallbusiness"],
    "healthcare": ["healthIT", "medicine", "startups", "technology"],
    "startup": ["startups", "entrepreneur", "SaaS", "smallbusiness"],
    "ai": ["MachineLearning", "artificial", "ChatGPT", "learnmachinelearning"],
    "ml": ["MachineLearning", "learnmachinelearning", "datascience", "artificial"],
    "llm": ["MachineLearning", "artificial", "ChatGPT", "LocalLLaMA"],
    "product": ["ProductManagement", "startups", "entrepreneur", "SaaS"],
    "growth": ["startups", "entrepreneur", "marketing", "digital_marketing"],
    "consumer": ["technology", "apps", "selfhosted", "productivity"],
}

FALLBACK_SUBREDDITS = ["startups", "entrepreneur", "technology", "programming", "webdev"]


def detect_subreddits(category: str, competitors: list) -> list:
    subs = set()
    cat_lower = category.lower()

    for keyword, subreddit_list in SUBREDDIT_MAP.items():
        if keyword in cat_lower:
            subs.update(subreddit_list)

    for comp in competitors:
        comp_lower = comp.lower()
        if any(w in comp_lower for w in ["data", "log", "metric", "monitor", "trace"]):
            subs.update(SUBREDDIT_MAP.get("observability", []))
        if any(w in comp_lower for w in ["pay", "stripe", "billing"]):
            subs.update(SUBREDDIT_MAP.get("payments", []))
        if any(w in comp_lower for w in ["crm", "sales", "hubspot", "salesforce"]):
            subs.update(SUBREDDIT_MAP.get("crm", []))

    if not subs:
        subs.update(FALLBACK_SUBREDDITS)

    subs.add("startups")
    return list(subs)[:8]


# ---------------------------------------------------------------------------
# Pain scoring (verbatim from map-your-market)
# ---------------------------------------------------------------------------

def compute_pain_score(source: str, score_val: int, comments: int, created_at: str) -> float:
    try:
        if created_at:
            dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            days_old = (TODAY - dt).days
        else:
            days_old = 180
    except Exception:
        days_old = 180

    if days_old < 30:
        recency = 1.0
    elif days_old < 90:
        recency = 0.85
    elif days_old < 180:
        recency = 0.7
    else:
        recency = 0.5

    if source == "github_issue":
        base = score_val * 3
    elif source == "reddit":
        base = min(score_val, 500) + comments * 0.3
    else:
        base = score_val + comments * 0.3

    return round(base * recency, 1)


# ---------------------------------------------------------------------------
# Reddit search (verbatim from map-your-market, queries adapted for ICP)
# ---------------------------------------------------------------------------

def build_icp_queries(category: str, icp_role: str, icp_pain: str, competitors: list) -> list:
    queries = []
    if icp_role:
        queries.append(icp_role)
    if icp_pain:
        queries.append(icp_pain)
    queries.append(category)
    for comp in competitors[:2]:
        queries.append(comp)
    if icp_pain:
        words = icp_pain.split()[:3]
        queries.append(" ".join(words) + " alternative")
    elif category:
        cat_words = category.split()[:2]
        queries.append(" ".join(cat_words) + " alternative")
    return list(dict.fromkeys(queries))[:6]


def search_reddit(queries: list, subreddits: list, time_filter: str = "year") -> list:
    results = []
    seen_ids = set()

    def parse_posts(data):
        posts = []
        if not data or "data" not in data:
            return posts
        for child in data["data"].get("children", []):
            p = child.get("data", {})
            post_id = p.get("id", "")
            if not post_id or post_id in seen_ids:
                continue
            seen_ids.add(post_id)
            score_val = p.get("score", 0)
            num_comments = p.get("num_comments", 0)
            created = datetime.fromtimestamp(p.get("created_utc", 0), tz=timezone.utc).isoformat()
            body = (p.get("selftext", "") or "")[:500]
            posts.append({
                "id": post_id,
                "source": "reddit",
                "title": p.get("title", ""),
                "body_excerpt": body,
                "pain_score": compute_pain_score("reddit", score_val, num_comments, created),
                "url": f"https://www.reddit.com{p.get('permalink', '')}",
                "subreddit": p.get("subreddit", ""),
                "score": score_val,
                "comments": num_comments,
                "created_at": created,
                "matched_query": "",
            })
        return posts

    def is_relevant(post: dict, query: str) -> bool:
        query_words = [w.lower() for w in query.split() if len(w) > 3]
        if not query_words:
            return True
        text = (post.get("title", "") + " " + post.get("body_excerpt", "")).lower()
        return any(w in text for w in query_words)

    for sub in subreddits[:6]:
        for query in queries[:3]:
            encoded = urllib.parse.quote_plus(query)
            url = f"https://www.reddit.com/r/{sub}/search.json?q={encoded}&sort=top&t={time_filter}&restrict_sr=true&limit=25"
            if not quiet:
                print(f"  Reddit r/{sub}: {query!r}", file=sys.stderr)
            data = fetch_json(url, headers={"User-Agent": "where-your-customer-lives/1.0"})
            posts = parse_posts(data)
            for p in posts:
                p["matched_query"] = query
            relevant = [p for p in posts if is_relevant(p, query)]
            results.extend(relevant)
            time.sleep(2)

    results = [r for r in results if r["pain_score"] >= 2.0]
    return results


# ---------------------------------------------------------------------------
# HN search (verbatim from map-your-market)
# ---------------------------------------------------------------------------

def search_hn(queries: list, days_back: int = 365) -> list:
    results = []
    seen_ids = set()
    cutoff_ts = int((TODAY - timedelta(days=days_back)).timestamp())

    for query in queries:
        encoded = urllib.parse.quote_plus(query)
        url = f"https://hn.algolia.com/api/v1/search?query={encoded}&tags=story&numericFilters=created_at_i>{cutoff_ts}&hitsPerPage=50"
        if not quiet:
            print(f"  HN: {query!r}", file=sys.stderr)
        data = fetch_json(url)
        if data:
            for hit in data.get("hits", []):
                obj_id = hit.get("objectID", "")
                if not obj_id or obj_id in seen_ids:
                    continue
                seen_ids.add(obj_id)
                points = hit.get("points") or 0
                num_comments = hit.get("num_comments") or 0
                if points < 3:
                    continue
                created = hit.get("created_at", "")
                results.append({
                    "id": obj_id,
                    "source": "hn",
                    "title": hit.get("title", ""),
                    "body_excerpt": (hit.get("story_text") or "")[:400],
                    "pain_score": compute_pain_score("hn", points, num_comments, created),
                    "url": hit.get("url") or f"https://news.ycombinator.com/item?id={obj_id}",
                    "subreddit": "",
                    "score": points,
                    "comments": num_comments,
                    "created_at": created,
                    "matched_query": query,
                })
        time.sleep(1)

    return results


# ---------------------------------------------------------------------------
# NEW: Reddit subreddit metadata
# ---------------------------------------------------------------------------

def get_subreddit_metadata(subreddit: str) -> dict:
    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    data = fetch_json(url, headers={"User-Agent": "where-your-customer-lives/1.0"})
    if not data or "data" not in data:
        return {"subscribers": 0, "active_user_count": 0, "description": ""}
    d = data["data"]
    desc = (d.get("public_description") or d.get("description") or "")[:200]
    desc = re.sub(r'\s+', ' ', desc).strip()
    return {
        "subscribers": d.get("subscribers", 0) or 0,
        "active_user_count": d.get("active_user_count", 0) or 0,
        "description": desc,
    }


# ---------------------------------------------------------------------------
# NEW: DuckDuckGo channel discovery
# ---------------------------------------------------------------------------

_MEMBER_PATTERNS = [
    r'(\d[\d,]+)\s*[Kk]\+?\s*(?:members|subscribers|followers|users)',
    r'(\d[\d,]+)\+?\s*(?:members|subscribers|followers|users|professionals|engineers|developers|founders)',
    r'(?:join|with|over|reach)\s+(\d[\d,]+)\+?\s*(?:members|subscribers|followers)',
    r'(\d[\d,]+)\s*(?:member|subscriber|follower)\s*(?:community|group|list)',
]


def parse_member_count(text: str) -> int:
    for pattern in _MEMBER_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            num_str = m.group(1).replace(",", "")
            try:
                count = int(num_str)
            except ValueError:
                continue
            if re.search(r'\d\s*[Kk]', m.group(0)):
                count *= 1000
            if 10 <= count <= 50_000_000:
                return count
    return 0


def _decode_ddg_url(raw_url: str) -> str:
    """DDG wraps destinations in //duckduckgo.com/l/?uddg=... -- extract the real URL."""
    m = re.search(r'uddg=([^&]+)', raw_url)
    if m:
        return urllib.parse.unquote(m.group(1))
    if raw_url.startswith("//"):
        return "https:" + raw_url
    return raw_url


def parse_ddg_results(html: str) -> list:
    results = []
    # DDG HTML: href comes after class="result__a" in attribute order
    # Pattern: extract raw href (DDG redirect) and title text
    hrefs = re.findall(r'<a[^>]*class="result__a"[^>]*href="([^"]+)"', html)
    titles_raw = re.findall(r'<a[^>]*class="result__a"[^>]*>(.*?)</a>', html, re.DOTALL)
    snippets_raw = re.findall(
        r'class="result__snippet"[^>]*>(.*?)</(?:a|span|div)>',
        html, re.DOTALL | re.IGNORECASE
    )

    titles = [re.sub(r'<[^>]+>', '', t).strip() for t in titles_raw]
    snippets = [re.sub(r'<[^>]+>', '', s).strip() for s in snippets_raw]

    for i, (raw_href, title) in enumerate(zip(hrefs, titles)):
        if not title or len(title) < 4:
            continue
        real_url = _decode_ddg_url(raw_href)
        snippet = snippets[i] if i < len(snippets) else ""
        results.append({"title": title, "url": real_url, "snippet": snippet})

    return results[:12]


_HTML_ENTITIES = {
    "&#x27;": "'", "&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"',
    "&#39;": "'", "&apos;": "'",
}

def _decode_html(text: str) -> str:
    for entity, char in _HTML_ENTITIES.items():
        text = text.replace(entity, char)
    return text


_LISTICLE_PATTERNS = re.compile(
    r'^(?:\d+\s+(?:best|top|great)|best\s+\d+|top\s+\d+|how\s+to|list\s+of|ultimate\s+list|'
    r'complete\s+list|the\s+\d+|full\s+list)',
    re.IGNORECASE
)


def clean_channel_name(title: str, channel_type: str) -> str:
    """Extract a clean channel name from a DDG result title."""
    title = _decode_html(title)

    # Reject listicle titles (they're articles, not channels)
    if _LISTICLE_PATTERNS.match(title.strip()):
        return ""

    # Strip common suffixes
    name = re.sub(r'\s*[-|:]\s*(?:Home|Official|Website|Sign up|Join|Free|Login|Welcome).*$', '', title, flags=re.IGNORECASE)
    name = name.strip()

    if channel_type == "slack":
        m = re.search(r'([A-Za-z][^|:\n]{3,50}?)\s+(?:Slack|Workspace)\b', title, re.IGNORECASE)
        if m:
            return m.group(0).strip()
        m = re.search(r'([A-Za-z][^|:\n]{3,50}?)\s+Community\b', title, re.IGNORECASE)
        if m:
            return m.group(0).strip()

    elif channel_type == "discord":
        m = re.search(r'([A-Za-z][^|:\n]{3,50}?)\s+(?:Discord|Server)\b', title, re.IGNORECASE)
        if m:
            return m.group(0).strip()

    elif channel_type == "conference":
        m = re.search(r'([A-Za-z][^|:\n]{3,60}?(?:Conf(?:erence)?|Summit|Con\b|Meetup|Camp))', title, re.IGNORECASE)
        if m:
            return m.group(0).strip()

    elif channel_type == "podcast":
        # Strip platform suffixes: "- Apple Podcasts", "- Spotify", "| Spotify", "Episodes |"
        name = re.sub(r'\s*[-|]\s*(?:Apple\s+Podcasts?|Spotify|Google\s+Podcasts?|Stitcher|Podbean|Buzzsprout|Anchor).*$', '', name, flags=re.IGNORECASE)
        name = re.sub(r'^Episodes\s*\|\s*', '', name, flags=re.IGNORECASE)
        name = re.sub(r'#\d+.*$', '', name)  # strip episode number suffixes
        name = name.strip()

    elif channel_type == "linkedin_group":
        name = re.sub(r'\s*\|\s*LinkedIn.*$', '', name, flags=re.IGNORECASE).strip()

    elif channel_type == "youtube":
        name = re.sub(r'\s*-\s*YouTube.*$', '', name, flags=re.IGNORECASE).strip()
        name = re.sub(r'\s*\|\s*YouTube.*$', '', name, flags=re.IGNORECASE).strip()

    return name[:70] if len(name) > 5 else ""


def search_channels_ddg(query: str, channel_type: str) -> list:
    encoded = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded}"
    if not quiet:
        print(f"  DDG [{channel_type}]: {query!r}", file=sys.stderr)
    html = fetch_html(url)
    if not html:
        return []

    ddg_results = parse_ddg_results(html)
    channels = []

    for r in ddg_results:
        combined = _decode_html(f"{r['title']} {r['snippet']}")
        member_count = parse_member_count(combined)
        name = clean_channel_name(r["title"], channel_type)
        if not name or len(name) < 4:
            continue

        # Skip obvious noise (search engine meta-pages, encyclopedias)
        bad_domains = ["google.com", "bing.com", "duckduckgo.com", "wikipedia.org", "wikidata.org"]
        if any(d in r.get("url", "") for d in bad_domains):
            continue

        channels.append({
            "name": name,
            "type": channel_type,
            "url": r["url"],
            "members": member_count,
            "active_users": 0,
            "description": r["snippet"][:200],
            "activity_score": 5,  # default; DDG doesn't expose post frequency
            "icp_signal_count": 0,
            "competitor_mentions": 0,
            "entry_type": "open",
            "discovery_method": "ddg_search",
            "evidence_posts": [],
        })

    return channels


# ---------------------------------------------------------------------------
# NEW: Channel scoring
# ---------------------------------------------------------------------------

def score_channel(channel: dict) -> float:
    icp_signals = channel.get("icp_signal_count", 0)
    members = channel.get("members", 0)
    activity = channel.get("activity_score", 0)
    comp_mentions = channel.get("competitor_mentions", 0)
    entry_type = channel.get("entry_type", "open")

    score = (
        icp_signals * 10
        + min(math.log10(max(members, 1)) * 15, 50)
        + min(activity, 30)
        + comp_mentions * 5
    )

    if entry_type == "paid":
        score -= 20
    elif entry_type == "invite-only":
        score -= 10

    return round(score, 1)


def get_tier(score: float) -> str:
    if score >= 100:
        return "top-priority"
    elif score >= 60:
        return "high"
    elif score >= 30:
        return "medium"
    else:
        return "low"


# ---------------------------------------------------------------------------
# NEW: Deduplicate channels
# ---------------------------------------------------------------------------

def deduplicate_channels(channels: list) -> list:
    seen = {}
    for ch in channels:
        key = ch["name"].lower().strip()
        if key not in seen:
            seen[key] = dict(ch)
        else:
            existing = seen[key]
            existing["icp_signal_count"] = max(
                existing.get("icp_signal_count", 0), ch.get("icp_signal_count", 0)
            )
            existing["competitor_mentions"] = existing.get("competitor_mentions", 0) + ch.get("competitor_mentions", 0)
            if ch.get("members", 0) > existing.get("members", 0):
                existing["members"] = ch["members"]
            existing["evidence_posts"] = existing.get("evidence_posts", []) + ch.get("evidence_posts", [])
            # Prefer signal_trace as discovery method
            if ch.get("discovery_method") == "signal_trace":
                existing["discovery_method"] = "signal_trace"

    return list(seen.values())


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main():
    global quiet

    parser = argparse.ArgumentParser(description="Discover channels where your ICP gathers")
    parser.add_argument("category", help="Market category (e.g. 'startup gtm sales tools')")
    parser.add_argument("--icp-role", default="", help="ICP role description (e.g. 'technical co-founders')")
    parser.add_argument("--icp-pain", default="", help="ICP primary pain (e.g. 'customer acquisition')")
    parser.add_argument("--product", default="", help="Product one-liner")
    parser.add_argument("--competitors", "-c", default="", help="Comma-separated competitor names")
    parser.add_argument("--output", "-o", default=None, help="Output JSON file path")
    parser.add_argument("--stdout", action="store_true", help="Print JSON to stdout")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress output")
    args = parser.parse_args()

    quiet = args.quiet
    competitors = [c.strip() for c in args.competitors.split(",") if c.strip()] if args.competitors else []

    if not args.output and not args.stdout:
        slug = re.sub(r"[^a-z0-9]+", "-", args.category.lower()).strip("-")
        args.output = f"/tmp/wcl-raw-{slug}-{TODAY.strftime('%Y-%m-%d')}.json"

    if not quiet:
        print(f"Finding channels for: {args.category!r}", file=sys.stderr)
        print(f"ICP role: {args.icp_role or 'not specified'}", file=sys.stderr)
        print(f"ICP pain: {args.icp_pain or 'not specified'}", file=sys.stderr)
        print(f"Competitors: {competitors or 'none'}", file=sys.stderr)

    # -----------------------------------------------------------------------
    # Step 1: Detect subreddits + build ICP queries
    # -----------------------------------------------------------------------
    subreddits = detect_subreddits(args.category, competitors)
    queries = build_icp_queries(args.category, args.icp_role, args.icp_pain, competitors)

    if not quiet:
        print(f"\nSubreddits: {subreddits}", file=sys.stderr)
        print(f"Queries: {queries}", file=sys.stderr)

    # -----------------------------------------------------------------------
    # Step 2: Signal-trace via Reddit
    # -----------------------------------------------------------------------
    if not quiet:
        print("\n[1/5] Signal-trace: Reddit...", file=sys.stderr)

    reddit_posts = search_reddit(queries, subreddits)

    if not quiet:
        print(f"  Found {len(reddit_posts)} ICP posts", file=sys.stderr)

    # Aggregate by subreddit
    sub_stats = {}
    for post in reddit_posts:
        sub = post.get("subreddit", "")
        if not sub:
            continue
        if sub not in sub_stats:
            sub_stats[sub] = {
                "icp_signal_count": 0,
                "competitor_mentions": 0,
                "total_score": 0.0,
                "evidence_posts": [],
            }
        sub_stats[sub]["icp_signal_count"] += 1
        sub_stats[sub]["total_score"] += post.get("pain_score", 0)
        post_text = (post.get("title", "") + " " + post.get("body_excerpt", "")).lower()
        for comp in competitors:
            if comp.lower() in post_text:
                sub_stats[sub]["competitor_mentions"] += 1
        if len(sub_stats[sub]["evidence_posts"]) < 3:
            sub_stats[sub]["evidence_posts"].append({
                "title": post.get("title", ""),
                "score": post.get("pain_score", 0),
                "url": post.get("url", ""),
                "pain_match": post.get("matched_query", ""),
            })

    # Fetch metadata + build Reddit channels
    reddit_channels = []
    for sub, stats in sub_stats.items():
        if not quiet:
            print(f"  Metadata: r/{sub}", file=sys.stderr)
        meta = get_subreddit_metadata(sub)
        time.sleep(1)

        channel = {
            "name": f"r/{sub}",
            "type": "reddit",
            "url": f"https://reddit.com/r/{sub}",
            "members": meta.get("subscribers", 0),
            "active_users": meta.get("active_user_count", 0),
            "description": meta.get("description", ""),
            "activity_score": min((meta.get("active_user_count", 0) or 0) // 100, 30),
            "icp_signal_count": stats["icp_signal_count"],
            "competitor_mentions": stats["competitor_mentions"],
            "entry_type": "open",
            "discovery_method": "signal_trace",
            "evidence_posts": stats["evidence_posts"],
        }
        channel["channel_score"] = score_channel(channel)
        channel["tier"] = get_tier(channel["channel_score"])
        reddit_channels.append(channel)

    # -----------------------------------------------------------------------
    # Step 3: HN signal-trace
    # -----------------------------------------------------------------------
    if not quiet:
        print("\n[2/5] HN signal-trace...", file=sys.stderr)

    hn_results = search_hn(queries[:3])

    if not quiet:
        print(f"  Found {len(hn_results)} HN signals", file=sys.stderr)

    hn_channel = None
    if len(hn_results) >= 3:
        hn_comp_mentions = sum(
            1 for r in hn_results
            if any(c.lower() in (r.get("title", "") + r.get("body_excerpt", "")).lower() for c in competitors)
        )
        hn_channel = {
            "name": "Hacker News",
            "type": "forum",
            "url": "https://news.ycombinator.com",
            "members": 0,
            "active_users": 0,
            "description": "Tech and startup community; strong signal for developer and founder ICPs",
            "activity_score": 20,
            "icp_signal_count": len(hn_results),
            "competitor_mentions": hn_comp_mentions,
            "entry_type": "open",
            "discovery_method": "signal_trace",
            "evidence_posts": [
                {
                    "title": r.get("title", ""),
                    "score": r.get("pain_score", 0),
                    "url": r.get("url", ""),
                    "pain_match": r.get("matched_query", ""),
                }
                for r in sorted(hn_results, key=lambda x: x.get("pain_score", 0), reverse=True)[:3]
            ],
        }
        hn_channel["channel_score"] = score_channel(hn_channel)
        hn_channel["tier"] = get_tier(hn_channel["channel_score"])

    # -----------------------------------------------------------------------
    # Step 4: DuckDuckGo channel discovery (non-Reddit types)
    # -----------------------------------------------------------------------
    if not quiet:
        print("\n[3/5] Discovering Slack/Discord/newsletter/podcast/conference channels...", file=sys.stderr)

    icp_label = args.icp_role or args.category
    ddg_channels = []

    channel_searches = [
        (f"{args.category} slack community", "slack"),
        (f"{icp_label} discord server community", "discord"),
        (f"{args.category} newsletter weekly", "newsletter"),
        (f"{icp_label} podcast episodes", "podcast"),
        (f"{args.category} conference summit 2025", "conference"),
        (f"site:linkedin.com/groups {args.category}", "linkedin_group"),
        (f"best {args.category} youtube channel", "youtube"),
    ]

    for query, ch_type in channel_searches:
        found = search_channels_ddg(query, ch_type)
        ddg_channels.extend(found[:3])
        time.sleep(2.5)

    for ch in ddg_channels:
        ch["channel_score"] = score_channel(ch)
        ch["tier"] = get_tier(ch["channel_score"])

    # -----------------------------------------------------------------------
    # Step 5: Competitor layer -- where competitors are discussed
    # -----------------------------------------------------------------------
    if competitors:
        if not quiet:
            print("\n[4/5] Competitor layer...", file=sys.stderr)
        for comp in competitors[:3]:
            comp_channels = search_channels_ddg(
                f"{comp} community users discussion forum",
                "forum"
            )
            for ch in comp_channels[:2]:
                ch["competitor_mentions"] = 3
                ch["channel_score"] = score_channel(ch)
                ch["tier"] = get_tier(ch["channel_score"])
                ddg_channels.append(ch)
            time.sleep(2)
    else:
        if not quiet:
            print("\n[4/5] Competitor layer: skipped (no competitors provided)", file=sys.stderr)

    # -----------------------------------------------------------------------
    # Step 6: Combine, deduplicate, rank
    # -----------------------------------------------------------------------
    if not quiet:
        print("\n[5/5] Ranking channels...", file=sys.stderr)

    all_channels = list(reddit_channels)
    if hn_channel:
        all_channels.append(hn_channel)
    all_channels.extend(ddg_channels)

    all_channels = deduplicate_channels(all_channels)

    # Re-score after deduplication (competitor_mentions may have changed)
    for ch in all_channels:
        ch["channel_score"] = score_channel(ch)
        ch["tier"] = get_tier(ch["channel_score"])

    all_channels.sort(key=lambda x: x.get("channel_score", 0), reverse=True)
    # Filter: keep channels with any positive signal (score > 0) -- DDG channels with no
    # member count score at 5 (activity default) and should still appear in output
    all_channels = [ch for ch in all_channels if ch.get("channel_score", 0) > 0]

    by_type: dict = {}
    for ch in all_channels:
        t = ch["type"]
        by_type[t] = by_type.get(t, 0) + 1

    top_priority = [ch["name"] for ch in all_channels if ch.get("tier") == "top-priority"]
    high_channels = [ch["name"] for ch in all_channels if ch.get("tier") == "high"]

    output_data = {
        "date": TODAY.strftime("%Y-%m-%d"),
        "product": args.product,
        "icp_role": args.icp_role,
        "icp_pain": args.icp_pain,
        "category": args.category,
        "competitors": competitors,
        "subreddits_searched": subreddits,
        "queries_used": queries,
        "reddit_posts_found": len(reddit_posts),
        "hn_signals_found": len(hn_results),
        "channels_discovered": all_channels,
        "summary": {
            "total_channels": len(all_channels),
            "top_priority": top_priority,
            "high": high_channels,
            "by_type": by_type,
            "competitor_layer_ran": bool(competitors),
        },
    }

    if not quiet:
        print(f"\nChannels discovered: {len(all_channels)}", file=sys.stderr)
        print(f"Top priority: {len(top_priority)}", file=sys.stderr)
        print(f"By type: {by_type}", file=sys.stderr)
        for i, ch in enumerate(all_channels[:5], 1):
            print(f"  #{i} {ch['name']} [{ch['type']}] score={ch.get('channel_score', 0)} tier={ch.get('tier', '')}", file=sys.stderr)

    if args.stdout:
        print(json.dumps(output_data, indent=2))
    else:
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
        if not quiet:
            print(f"Output: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
