"""
research.py -- two-phase Tavily data collector for competitor-pr-finder.

Phase 1 (discover): finds competitor candidates from product analysis context.
Phase 2 (pr-research): runs three-track PR search per confirmed competitor.

Usage:
  # Phase 1
  python3 scripts/research.py \
      --phase discover \
      --product-analysis /tmp/cprf-product-analysis.json \
      --tavily-key "$TAVILY_API_KEY" \
      --output /tmp/cprf-competitors-raw.json

  # Phase 2
  python3 scripts/research.py \
      --phase pr-research \
      --competitors /tmp/cprf-competitors-confirmed.json \
      --product-analysis /tmp/cprf-product-analysis.json \
      --tavily-key "$TAVILY_API_KEY" \
      --output /tmp/cprf-pr-raw.json
"""

import argparse
import json
import os
import ssl
import sys
import urllib.request
from datetime import date

_ssl_ctx = ssl._create_unverified_context()

quiet = False


def log(msg):
    if not quiet:
        print(msg, file=sys.stderr)


def fetch_json(url, payload, timeout=25):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "competitor-pr-finder/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout, context=_ssl_ctx) as resp:
        return json.loads(resp.read())


def tavily_search(query, key, depth="advanced", max_results=7):
    log(f"  Tavily [{depth}] {query[:80]}")
    try:
        result = fetch_json(
            "https://api.tavily.com/search",
            {
                "api_key": key,
                "query": query,
                "search_depth": depth,
                "max_results": max_results,
            },
        )
        return {
            "answer": result.get("answer", ""),
            "results": result.get("results", []),
        }
    except Exception as e:
        log(f"  ERROR: {e}")
        return {"answer": "", "results": [], "error": str(e)}


# ---------------------------------------------------------------------------
# Phase 1: competitor discovery
# ---------------------------------------------------------------------------

def run_discover(product_analysis, tavily_key):
    name = product_analysis.get("product_name", "")
    l2 = product_analysis.get("industry_taxonomy", {}).get("l2", "")
    l3 = product_analysis.get("industry_taxonomy", {}).get("l3", "")

    log(f"\nPhase 1: competitor discovery for '{name}'")
    log(f"  taxonomy: {l2} > {l3}")

    queries = [
        f'"{name}" competitors alternatives {l3}',
        f"{l2} {l3} startups companies funded 2022 2023 2024",
    ]

    competitor_searches = []
    for q in queries:
        result = tavily_search(q, tavily_key, depth="advanced", max_results=8)
        competitor_searches.append(
            {
                "query": q,
                "answer": result.get("answer", ""),
                "results": [
                    {
                        "title": r.get("title", ""),
                        "url": r.get("url", ""),
                        "content": r.get("content", "")[:500],
                    }
                    for r in result.get("results", [])
                ],
            }
        )
        log(f"    {len(result.get('results', []))} results")

    log("Phase 1 complete.")
    return {
        "date": str(date.today()),
        "product_name": name,
        "competitor_searches": competitor_searches,
    }


# ---------------------------------------------------------------------------
# Phase 2: three-track PR research
# ---------------------------------------------------------------------------

TRACK_QUERIES = {
    "editorial": '"{competitor}" featured press coverage TechCrunch Forbes Wired article interview',
    "podcast": '"{competitor}" founder CEO podcast interview appeared on episode',
    "community": '"{competitor}" site:reddit.com OR site:news.ycombinator.com OR site:producthunt.com',
}

FALLBACK_QUERY = '"{competitor}" review coverage press news'


def run_pr_research(confirmed_competitors, product_analysis, tavily_key):
    log(f"\nPhase 2: PR research for {len(confirmed_competitors)} competitors")

    results = []
    for comp in confirmed_competitors:
        name = comp.get("name", "")
        url = comp.get("url", "")
        log(f"\n  [{name}]")

        comp_result = {
            "competitor": name,
            "url": url,
            "tracks": {},
        }

        total_results = 0
        for track, query_template in TRACK_QUERIES.items():
            query = query_template.replace("{competitor}", name)
            data = tavily_search(query, tavily_key, depth="advanced", max_results=7)
            track_results = [
                {
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", "")[:500],
                }
                for r in data.get("results", [])
            ]
            comp_result["tracks"][track] = {
                "query": query,
                "answer": data.get("answer", ""),
                "results": track_results,
            }
            count = len(track_results)
            total_results += count
            log(f"    {track}: {count} results")

        # Fallback if all 3 tracks returned nothing
        if total_results == 0:
            log(f"    WARNING: 0 results across all tracks. Running fallback search.")
            fallback_query = FALLBACK_QUERY.replace("{competitor}", name)
            fallback_data = tavily_search(
                fallback_query, tavily_key, depth="advanced", max_results=7
            )
            comp_result["tracks"]["fallback"] = {
                "query": fallback_query,
                "answer": fallback_data.get("answer", ""),
                "results": [
                    {
                        "title": r.get("title", ""),
                        "url": r.get("url", ""),
                        "content": r.get("content", "")[:500],
                    }
                    for r in fallback_data.get("results", [])
                ],
            }
            comp_result["data_quality_flag"] = "All 3 tracks returned 0 results. Fallback search used."
            log(f"    fallback: {len(fallback_data.get('results', []))} results")

        results.append(comp_result)

    log("\nPhase 2 complete.")
    return {
        "date": str(date.today()),
        "competitors_researched": len(confirmed_competitors),
        "results": results,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    global quiet

    parser = argparse.ArgumentParser(description="competitor-pr-finder research script")
    parser.add_argument(
        "--phase",
        required=True,
        choices=["discover", "pr-research"],
        help="Which phase to run",
    )
    parser.add_argument(
        "--product-analysis",
        required=True,
        help="Path to cprf-product-analysis.json",
    )
    parser.add_argument(
        "--competitors",
        default="",
        help="Path to cprf-competitors-confirmed.json (Phase 2 only)",
    )
    parser.add_argument(
        "--tavily-key",
        default=os.environ.get("TAVILY_API_KEY", ""),
        help="Tavily API key (or set TAVILY_API_KEY env var)",
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

    if not args.tavily_key:
        print("ERROR: Tavily API key required. Pass --tavily-key or set TAVILY_API_KEY.", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.product_analysis):
        print(f"ERROR: {args.product_analysis} not found", file=sys.stderr)
        sys.exit(1)

    with open(args.product_analysis) as f:
        product_analysis = json.load(f)

    if args.phase == "discover":
        output = run_discover(product_analysis, args.tavily_key)

    elif args.phase == "pr-research":
        if not args.competitors:
            print("ERROR: --competitors required for pr-research phase", file=sys.stderr)
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
        output = run_pr_research(confirmed, product_analysis, args.tavily_key)

    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)

    log(f"\nOutput written to {args.output}")

    # Print summary for SKILL.md to parse
    if args.phase == "discover":
        total = sum(len(s["results"]) for s in output["competitor_searches"])
        print(f"Discover complete: {len(output['competitor_searches'])} queries, {total} total results")
    else:
        print(f"PR research complete: {output['competitors_researched']} competitors researched")
        for r in output.get("results", []):
            track_counts = {t: len(v["results"]) for t, v in r["tracks"].items()}
            print(f"  {r['competitor']}: {track_counts}")


if __name__ == "__main__":
    main()
