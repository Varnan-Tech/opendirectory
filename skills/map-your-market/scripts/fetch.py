#!/usr/bin/env python3
"""
map-your-market fetch script
Collects pain signals from Reddit, HN, GitHub Issues, G2, and Google Trends.
No required API keys. GITHUB_TOKEN optional (improves rate limits).

Usage:
    python3 scripts/fetch.py "developer observability" --competitors "Datadog,Grafana" --output /tmp/mym-raw.json
    python3 scripts/fetch.py "B2B analytics" --output results.json --stdout
    GITHUB_TOKEN=your_token python3 scripts/fetch.py "devops tooling" --competitors "New Relic,Datadog"
"""

import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser

_ssl_ctx = ssl._create_unverified_context()

TODAY = datetime.now(timezone.utc)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------

def fetch_json(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers=headers or {})
    req.add_header("User-Agent", "map-your-market-skill/1.0")
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
    req.add_header("User-Agent", "Mozilla/5.0 (compatible; map-your-market/1.0)")
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


quiet = False


# ---------------------------------------------------------------------------
# Subreddit detection
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
    "crm": ["sales", "salesforce", "entrepreneur", "smallbusiness"],
    "sales": ["sales", "entrepreneur", "startups", "smallbusiness"],
    "hr": ["humanresources", "remotework", "startups", "smallbusiness"],
    "finance": ["personalfinance", "accounting", "startups", "smallbusiness"],
    "healthcare": ["healthIT", "medicine", "startups", "technology"],
    "ai": ["MachineLearning", "artificial", "ChatGPT", "learnmachinelearning"],
    "ml": ["MachineLearning", "learnmachinelearning", "datascience", "artificial"],
    "llm": ["MachineLearning", "artificial", "ChatGPT", "LocalLLaMA"],
}

FALLBACK_SUBREDDITS = ["programming", "webdev", "technology", "startups", "entrepreneur"]


def detect_subreddits(category: str, competitors: list) -> list:
    subs = set()
    cat_lower = category.lower()

    for keyword, subreddit_list in SUBREDDIT_MAP.items():
        if keyword in cat_lower:
            subs.update(subreddit_list)

    # Also infer from competitor names
    for comp in competitors:
        comp_lower = comp.lower()
        if any(w in comp_lower for w in ["data", "log", "metric", "monitor", "trace"]):
            subs.update(SUBREDDIT_MAP.get("observability", []))
        if any(w in comp_lower for w in ["pay", "stripe", "billing"]):
            subs.update(SUBREDDIT_MAP.get("payments", []))
        if any(w in comp_lower for w in ["db", "sql", "postgres", "mongo"]):
            subs.update(SUBREDDIT_MAP.get("database", []))

    if not subs:
        subs.update(FALLBACK_SUBREDDITS)

    # Always include a broad signal subreddit
    subs.add("technology")
    return list(subs)[:8]


# ---------------------------------------------------------------------------
# Pain scoring
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
        base = score_val * 3  # reactions -- most deliberate signal
    elif source == "reddit":
        # Cap Reddit base at 500 to prevent viral off-topic posts dominating
        base = min(score_val, 500) + comments * 0.3
    else:  # hn
        base = score_val + comments * 0.3

    return round(base * recency, 1)


# ---------------------------------------------------------------------------
# Reddit
# ---------------------------------------------------------------------------

def build_reddit_queries(category: str, competitors: list) -> list:
    queries = [category]
    # Add competitor names as queries to find complaints
    for comp in competitors[:3]:
        queries.append(comp)
    # Add pain-oriented variants
    cat_words = category.split()[:2]
    if cat_words:
        queries.append(" ".join(cat_words) + " alternative")
        queries.append(" ".join(cat_words) + " problem")
    return list(dict.fromkeys(queries))  # deduplicate preserving order


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
        """Require query words to appear in title or body for basic relevance."""
        query_words = [w.lower() for w in query.split() if len(w) > 3]
        if not query_words:
            return True
        text = (post.get("title", "") + " " + post.get("body_excerpt", "")).lower()
        return any(w in text for w in query_words)

    # Subreddit-specific search only (more relevant than global search)
    for sub in subreddits[:6]:
        for query in queries[:3]:  # top 3 queries per subreddit
            encoded = urllib.parse.quote_plus(query)
            url = f"https://www.reddit.com/r/{sub}/search.json?q={encoded}&sort=top&t={time_filter}&restrict_sr=true&limit=25"
            if not quiet:
                print(f"  Reddit r/{sub}: {query!r}", file=sys.stderr)
            data = fetch_json(url, headers={"User-Agent": "map-your-market/1.0"})
            posts = parse_posts(data)
            for p in posts:
                p["matched_query"] = query
            # Relevance filter: skip posts where query words don't appear in title/body
            relevant = [p for p in posts if is_relevant(p, query)]
            results.extend(relevant)
            time.sleep(2)

    # Filter noise: min pain score 2.0
    results = [r for r in results if r["pain_score"] >= 2.0]
    return results


# ---------------------------------------------------------------------------
# Hacker News (Algolia API)
# ---------------------------------------------------------------------------

def search_hn(queries: list, days_back: int = 365) -> list:
    results = []
    seen_ids = set()
    cutoff_ts = int((TODAY - timedelta(days=days_back)).timestamp())

    for query in queries:
        encoded = urllib.parse.quote_plus(query)
        # Search stories
        url = f"https://hn.algolia.com/api/v1/search?query={encoded}&tags=story&numericFilters=created_at_i>{cutoff_ts}&hitsPerPage=50"
        if not quiet:
            print(f"  HN stories: {query!r}", file=sys.stderr)
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
                    continue  # noise floor
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

        # Search Ask HN comments
        url = f"https://hn.algolia.com/api/v1/search?query={encoded}&tags=comment&numericFilters=created_at_i>{cutoff_ts}&hitsPerPage=30"
        data = fetch_json(url)
        if data:
            for hit in data.get("hits", []):
                obj_id = hit.get("objectID", "")
                if not obj_id or obj_id in seen_ids:
                    continue
                seen_ids.add(obj_id)
                text = (hit.get("comment_text") or "")[:400]
                if not text or len(text) < 50:
                    continue
                created = hit.get("created_at", "")
                results.append({
                    "id": obj_id,
                    "source": "hn",
                    "title": f"HN comment: {text[:80]}...",
                    "body_excerpt": text,
                    "pain_score": compute_pain_score("hn", 5, 0, created),  # comments = low score base
                    "url": f"https://news.ycombinator.com/item?id={obj_id}",
                    "subreddit": "",
                    "score": 5,
                    "comments": 0,
                    "created_at": created,
                    "matched_query": query,
                })
        time.sleep(1)

    return results


# ---------------------------------------------------------------------------
# GitHub Issues
# ---------------------------------------------------------------------------

def search_github_issues(competitors: list, category: str) -> list:
    results = []
    seen = set()

    # Search for issues mentioning pain keywords in competitor repos
    pain_terms = ["not working", "problem", "issue", "broken", "pricing", "slow", "alternative", "migrate", "annoying", "hate"]

    for comp in competitors[:4]:
        # Try to find the GitHub repo for this competitor
        encoded = urllib.parse.quote_plus(comp)
        search_url = f"/search/repositories?q={encoded}&sort=stars&per_page=3"
        data = gh_get(search_url)
        time.sleep(0.5)
        if not data or "items" not in data:
            continue
        for repo in data["items"][:2]:
            full_name = repo.get("full_name", "")
            if not full_name:
                continue
            if not quiet:
                print(f"  GitHub issues: {full_name}", file=sys.stderr)
            # Fetch top issues by reactions
            issues_url = f"/repos/{full_name}/issues?state=open&sort=reactions&direction=desc&per_page=50"
            issues = gh_get(issues_url)
            time.sleep(0.5)
            if not issues or not isinstance(issues, list):
                continue
            for issue in issues:
                if "pull_request" in issue:
                    continue  # skip PRs
                reactions = issue.get("reactions", {}).get("+1", 0) or issue.get("reactions", {}).get("total_count", 0) or 0
                if reactions < 2:
                    continue  # noise floor
                issue_id = str(issue.get("id", ""))
                if issue_id in seen:
                    continue
                seen.add(issue_id)
                body = (issue.get("body") or "")[:500]
                created = issue.get("created_at", "")
                results.append({
                    "id": issue_id,
                    "source": "github_issue",
                    "title": issue.get("title", ""),
                    "body_excerpt": body,
                    "pain_score": compute_pain_score("github_issue", reactions, issue.get("comments", 0), created),
                    "url": issue.get("html_url", ""),
                    "subreddit": f"github/{full_name}",
                    "score": reactions,
                    "comments": issue.get("comments", 0),
                    "created_at": created,
                    "matched_query": comp,
                })

    # Also do category-based GitHub issue search
    if category:
        encoded = urllib.parse.quote_plus(f"{category} is:issue is:open")
        search_url = f"/search/issues?q={encoded}&sort=reactions&order=desc&per_page=30"
        data = gh_get(search_url)
        time.sleep(0.5)
        if data and "items" in data:
            for issue in data["items"]:
                issue_id = str(issue.get("id", ""))
                if issue_id in seen:
                    continue
                seen.add(issue_id)
                reactions = issue.get("reactions", {}).get("+1", 0) or 0
                if reactions < 2:
                    continue
                body = (issue.get("body") or "")[:500]
                created = issue.get("created_at", "")
                results.append({
                    "id": issue_id,
                    "source": "github_issue",
                    "title": issue.get("title", ""),
                    "body_excerpt": body,
                    "pain_score": compute_pain_score("github_issue", reactions, issue.get("comments", 0), created),
                    "url": issue.get("html_url", ""),
                    "subreddit": "github/search",
                    "score": reactions,
                    "comments": issue.get("comments", 0),
                    "created_at": created,
                    "matched_query": category,
                })

    return results


# ---------------------------------------------------------------------------
# G2 scraper
# ---------------------------------------------------------------------------

class G2Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.vendors = []
        self._in_product = False
        self._current = {}
        self._capture_name = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        cls = attrs.get("class", "")
        if "product-listing" in cls or "product-card" in cls:
            self._in_product = True
            self._current = {}
        if self._in_product and tag == "a" and "product-listing__product-name" in cls:
            self._capture_name = True

    def handle_endtag(self, tag):
        if tag == "div" and self._in_product and self._current.get("name"):
            self.vendors.append(dict(self._current))
            self._in_product = False
        if self._capture_name:
            self._capture_name = False

    def handle_data(self, data):
        if self._capture_name and data.strip():
            self._current["name"] = data.strip()


def scrape_g2_category(category: str) -> dict:
    slug = re.sub(r"[^a-z0-9]+", "-", category.lower()).strip("-")
    urls_to_try = [
        f"https://www.g2.com/categories/{slug}",
        f"https://www.g2.com/software/{slug}/",
    ]
    html = ""
    used_url = urls_to_try[0]
    for url in urls_to_try:
        if not quiet:
            print(f"  G2: {url}", file=sys.stderr)
        html = fetch_html(url)
        if html:
            used_url = url
            break
        time.sleep(1)

    if not html:
        # Fallback: search DuckDuckGo for G2 category to get vendor names
        if not quiet:
            print(f"  G2 blocked -- trying DuckDuckGo fallback", file=sys.stderr)
        ddg_url = f"https://html.duckduckgo.com/html/?q=site:g2.com+{urllib.parse.quote(category)}+software+reviews"
        html = fetch_html(ddg_url)
        if html:
            # Extract product names from DDG results
            ddg_names = re.findall(r'g2\.com/products/([a-z0-9-]+)/reviews', html)
            vendors = [{"name": n.replace("-", " ").title()} for n in list(dict.fromkeys(ddg_names))[:10]]
            return {"vendor_count_g2": len(vendors), "top_vendors": vendors, "g2_url": f"via DuckDuckGo search"}
        return {"vendor_count_g2": 0, "top_vendors": [], "g2_url": used_url}

    # Extract vendor count
    vendor_count = 0
    count_match = re.search(r"(\d[\d,]+)\s+(?:products|software|tools|solutions)", html, re.IGNORECASE)
    if count_match:
        vendor_count = int(count_match.group(1).replace(",", ""))

    # Extract product names
    name_matches = re.findall(r'data-product-name="([^"]+)"', html)
    if not name_matches:
        name_matches = re.findall(r'class="product-listing__product-name[^"]*">([^<]+)<', html)
    if not name_matches:
        name_matches = re.findall(r'"name"\s*:\s*"([^"]{3,50})"', html)

    rating_matches = re.findall(r'"ratingValue"\s*:\s*"?([\d.]+)"?', html)
    review_matches = re.findall(r'"reviewCount"\s*:\s*"?(\d+)"?', html)

    top_vendors = []
    for i, name in enumerate(name_matches[:10]):
        vendor = {"name": name.strip()}
        if i < len(rating_matches):
            vendor["rating"] = rating_matches[i]
        if i < len(review_matches):
            vendor["review_count"] = int(review_matches[i])
        top_vendors.append(vendor)

    if vendor_count == 0 and top_vendors:
        vendor_count = len(top_vendors)

    return {"vendor_count_g2": vendor_count, "top_vendors": top_vendors, "g2_url": used_url}


# ---------------------------------------------------------------------------
# Google Trends (unofficial endpoint)
# ---------------------------------------------------------------------------

def get_trends_direction(keyword: str) -> dict:
    """Infer trend direction from HN post frequency as a proxy when Google Trends is unavailable."""
    if not quiet:
        print(f"  Trends (via HN frequency): {keyword!r}", file=sys.stderr)
    # Compare HN post counts: older 6 months vs recent 6 months
    try:
        cutoff_old = int((TODAY - timedelta(days=365)).timestamp())
        cutoff_mid = int((TODAY - timedelta(days=180)).timestamp())
        encoded = urllib.parse.quote_plus(keyword)

        url_old = (f"https://hn.algolia.com/api/v1/search?query={encoded}"
                   f"&tags=story&numericFilters=created_at_i>{cutoff_old},created_at_i<{cutoff_mid}&hitsPerPage=1")
        url_new = (f"https://hn.algolia.com/api/v1/search?query={encoded}"
                   f"&tags=story&numericFilters=created_at_i>{cutoff_mid}&hitsPerPage=1")

        data_old = fetch_json(url_old)
        time.sleep(0.5)
        data_new = fetch_json(url_new)

        count_old = data_old.get("nbHits", 0) if data_old else 0
        count_new = data_new.get("nbHits", 0) if data_new else 0

        if count_old == 0 and count_new == 0:
            return {"trends_direction": "unknown", "trends_12mo": [], "trends_note": "insufficient HN data"}

        if count_old == 0:
            direction = "up"
        elif count_new > count_old * 1.2:
            direction = "up"
        elif count_new < count_old * 0.8:
            direction = "down"
        else:
            direction = "flat"

        return {
            "trends_direction": direction,
            "trends_12mo": [],
            "trends_note": f"HN posts: {count_old} (6-12mo ago) vs {count_new} (last 6mo)",
        }
    except Exception:
        return {"trends_direction": "unknown", "trends_12mo": []}


# ---------------------------------------------------------------------------
# ICP signals extractor
# ---------------------------------------------------------------------------

def extract_icp_signals(reddit_results: list) -> list:
    sub_counts = {}
    sub_scores = {}
    for p in reddit_results:
        sub = p.get("subreddit", "")
        if sub:
            sub_counts[sub] = sub_counts.get(sub, 0) + 1
            sub_scores[sub] = sub_scores.get(sub, 0) + p.get("pain_score", 0)

    signals = []
    for sub, count in sorted(sub_counts.items(), key=lambda x: -x[1]):
        avg_score = sub_scores[sub] / count if count > 0 else 0
        signals.append({
            "subreddit": sub,
            "post_count": count,
            "avg_pain_score": round(avg_score, 1),
            "total_pain_score": round(sub_scores[sub], 1),
        })
    return signals


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main():
    global quiet

    parser = argparse.ArgumentParser(description="Fetch market pain signals for map-your-market skill")
    parser.add_argument("category", help="Market category keywords (e.g. 'developer observability')")
    parser.add_argument("--competitors", "-c", default="", help="Comma-separated competitor names")
    parser.add_argument("--context", default="", help="Product context for output")
    parser.add_argument("--output", "-o", default=None, help="Output JSON file path")
    parser.add_argument("--stdout", action="store_true", help="Print JSON to stdout")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress output")
    args = parser.parse_args()

    quiet = args.quiet

    if not args.output and not args.stdout:
        slug = re.sub(r"[^a-z0-9]+", "-", args.category.lower()).strip("-")
        args.output = f"market-map-{slug}-{TODAY.strftime('%Y-%m-%d')}.json"

    competitors = [c.strip() for c in args.competitors.split(",") if c.strip()] if args.competitors else []

    if not quiet:
        print(f"Mapping market: {args.category!r}", file=sys.stderr)
        print(f"Competitors: {competitors or 'none'}", file=sys.stderr)

    # Detect subreddits
    subreddits = detect_subreddits(args.category, competitors)
    if not quiet:
        print(f"Subreddits: {subreddits}", file=sys.stderr)

    # Build search queries
    queries = build_reddit_queries(args.category, competitors)
    if not quiet:
        print(f"Queries: {queries}", file=sys.stderr)

    # --- Reddit ---
    if not quiet:
        print("\n[1/5] Reddit...", file=sys.stderr)
    reddit_results = search_reddit(queries, subreddits)
    if not quiet:
        print(f"  Found {len(reddit_results)} Reddit signals", file=sys.stderr)

    # --- HN ---
    if not quiet:
        print("\n[2/5] Hacker News...", file=sys.stderr)
    hn_queries = [args.category] + competitors[:2]
    hn_results = search_hn(hn_queries)
    if not quiet:
        print(f"  Found {len(hn_results)} HN signals", file=sys.stderr)

    # --- GitHub Issues ---
    if not quiet:
        print("\n[3/5] GitHub Issues...", file=sys.stderr)
    github_results = search_github_issues(competitors, args.category)
    if not quiet:
        print(f"  Found {len(github_results)} GitHub issue signals", file=sys.stderr)

    # --- G2 ---
    if not quiet:
        print("\n[4/5] G2...", file=sys.stderr)
    g2_data = scrape_g2_category(args.category)
    if not quiet:
        print(f"  G2 vendors: {g2_data['vendor_count_g2']}", file=sys.stderr)

    # --- Trends ---
    if not quiet:
        print("\n[5/5] Google Trends...", file=sys.stderr)
    trends = get_trends_direction(args.category)
    if not quiet:
        print(f"  Trends direction: {trends['trends_direction']}", file=sys.stderr)

    # --- Combine and score ---
    all_pains = reddit_results + hn_results + github_results
    all_pains.sort(key=lambda x: x["pain_score"], reverse=True)

    # ICP signals
    icp_signals = extract_icp_signals(reddit_results)

    # Build summary
    top20 = all_pains[:20]
    total = len(all_pains)

    # Competitor mention counts
    competitor_mentioned = {}
    for comp in competitors:
        count = sum(1 for p in all_pains if comp.lower() in (p["title"] + " " + p["body_excerpt"]).lower())
        if count > 0:
            competitor_mentioned[comp] = count

    output_data = {
        "date": TODAY.strftime("%Y-%m-%d"),
        "category": args.category,
        "competitors": competitors,
        "product_context": args.context,
        "subreddits_searched": subreddits,
        "queries_used": queries,
        "market_signals": {
            "vendor_count_g2": g2_data["vendor_count_g2"],
            "top_vendors": g2_data["top_vendors"],
            "g2_url": g2_data["g2_url"],
            "trends_direction": trends["trends_direction"],
            "trends_12mo": trends["trends_12mo"],
            "hn_signals_found": len(hn_results),
            "reddit_signals_found": len(reddit_results),
            "github_issue_signals": len(github_results),
        },
        "raw_pains": all_pains,
        "icp_signals": icp_signals,
        "summary": {
            "total_pain_signals": total,
            "high_signal": top20,
            "competitor_mentioned": competitor_mentioned,
        },
    }

    if not quiet:
        print(f"\nTotal signals: {total}", file=sys.stderr)
        print(f"Top pain_score: {all_pains[0]['pain_score'] if all_pains else 0}", file=sys.stderr)

    if args.stdout:
        print(json.dumps(output_data, indent=2))
    else:
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
        if not quiet:
            print(f"Output: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
