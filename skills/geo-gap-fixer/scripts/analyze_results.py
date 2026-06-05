#!/usr/bin/env python3
"""
analyze_results.py — Extract brand mentions, rank, sentiment, citations, and framing.

Reads data/raw_responses.json (output of probe_llms.py) and produces
data/analysis.json with structured metrics for each prompt-provider pair.

Usage:
    python scripts/analyze_results.py
"""

import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Fix Windows console encoding
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

# ── Constants ───────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
DATA_DIR = SKILL_ROOT / "data"
RAW_RESPONSES_PATH = DATA_DIR / "raw_responses.json"
ANALYSIS_PATH = DATA_DIR / "analysis.json"

# Sentiment keyword lists — matched with word boundaries to avoid false positives
# (e.g., "best" inside "asbest" won't match)
POSITIVE_KEYWORDS = [
    "best", "recommend", "excellent", "leading", "top", "popular",
    "powerful", "intuitive", "fast", "modern", "innovative", "reliable",
    "robust", "preferred", "standout", "impressive", "superior",
    "seamless", "elegant", "efficient",
]

NEGATIVE_KEYWORDS = [
    "limited", "lacks", "downside", "expensive", "complex",
    "steep learning curve", "missing", "outdated", "slow", "clunky",
    "basic", "restrictive", "difficult", "confusing", "poor",
    "frustrating", "buggy", "unreliable", "overpriced",
]

# Pre-compile word-boundary patterns for sentiment keywords
_POS_PATTERNS = [re.compile(r'\b' + re.escape(kw) + r'\b') for kw in POSITIVE_KEYWORDS]
_NEG_PATTERNS = [re.compile(r'\b' + re.escape(kw) + r'\b') for kw in NEGATIVE_KEYWORDS]

# URL extraction regex
URL_PATTERN = re.compile(r'https?://(?:[a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=%])+')


# ── Core Analysis Functions ─────────────────────────────────────────────────


def find_mentions(text: str, names: list[str]) -> dict[str, list[int]]:
    """
    Find all mentions of each name in the text.
    Returns {name: [char_positions]} using word-boundary matching.
    """
    mentions = {}
    text_lower = text.lower()
    for name in names:
        pattern = re.compile(r'\b' + re.escape(name.lower()) + r'\b')
        positions = [m.start() for m in pattern.finditer(text_lower)]
        if positions:
            mentions[name] = positions
    return mentions


def compute_rank(mentions: dict[str, list[int]], brand: str) -> int | None:
    """
    Compute mention rank for the brand.
    Rank 1 = brand appears first among all tracked names.
    Returns None if brand not mentioned.
    """
    if brand not in mentions:
        return None

    brand_first = mentions[brand][0]
    rank = 1
    for name, positions in mentions.items():
        if name != brand and positions[0] < brand_first:
            rank += 1
    return rank


def compute_sentiment(text: str, name: str) -> dict:
    """
    Compute sentiment for a specific brand/name within the text.
    Uses keyword proximity scoring: look within ±200 chars of each mention.
    """
    text_lower = text.lower()
    pattern = re.compile(r'\b' + re.escape(name.lower()) + r'\b')
    match_positions = [m.start() for m in pattern.finditer(text_lower)]

    if not match_positions:
        return {"score": 0.0, "label": "not_mentioned", "positive": [], "negative": []}

    # Collect context around all mentions
    context_chars = []
    for pos in match_positions:
        start = max(0, pos - 200)
        end = min(len(text_lower), pos + len(name) + 200)
        context_chars.append(text_lower[start:end])

    context = " ".join(context_chars)

    pos_found = [POSITIVE_KEYWORDS[i] for i, p in enumerate(_POS_PATTERNS) if p.search(context)]
    neg_found = [NEGATIVE_KEYWORDS[i] for i, p in enumerate(_NEG_PATTERNS) if p.search(context)]

    total = len(pos_found) + len(neg_found)
    if total == 0:
        score = 0.0
        label = "neutral"
    else:
        score = round((len(pos_found) - len(neg_found)) / total, 2)
        if score > 0.2:
            label = "positive"
        elif score < -0.2:
            label = "negative"
        else:
            label = "neutral"

    return {
        "score": score,
        "label": label,
        "positive": pos_found,
        "negative": neg_found,
    }


def extract_citations(text: str) -> list[str]:
    """Extract unique cited domains from URLs in the response text."""
    urls = URL_PATTERN.findall(text)
    domains = set()
    for url in urls:
        # Extract domain from URL
        match = re.match(r'https?://([^/\s?#]+)', url)
        if match:
            domain = match.group(1).lower()
            # Remove common prefixes
            domain = re.sub(r'^www\.', '', domain)
            domains.add(domain)
    return sorted(domains)


def extract_framing(text: str, name: str) -> list[str]:
    """
    Extract descriptive phrases used near a brand mention.
    Captures adjectives and short phrases within ±60 chars.
    """
    text_lower = text.lower()
    pattern = re.compile(r'\b' + re.escape(name.lower()) + r'\b')
    phrases = set()

    for match in pattern.finditer(text_lower):
        start = max(0, match.start() - 60)
        end = min(len(text_lower), match.end() + 60)
        context = text_lower[start:end]

        # Extract adjective-like words near the brand
        # Look for common descriptive patterns
        desc_patterns = [
            r'(?:is|are|was)\s+((?:a\s+)?(?:very\s+)?[\w-]+(?:\s+[\w-]+)?)',
            r'([\w-]+(?:\s+[\w-]+)?)\s+(?:tool|platform|solution|app|software)',
            r'(?:known for|best for|great for|ideal for)\s+([\w\s-]+?)(?:\.|,|$)',
        ]
        for dp in desc_patterns:
            for dm in re.finditer(dp, context):
                phrase = dm.group(1).strip()
                if len(phrase) > 2 and phrase != name.lower():
                    phrases.add(phrase)

    return sorted(phrases)[:10]  # Cap at 10 phrases


def determine_winner(mentions: dict[str, list[int]]) -> str | None:
    """Determine which brand/competitor was mentioned first (i.e., the 'winner')."""
    if not mentions:
        return None

    first_positions = {name: positions[0] for name, positions in mentions.items()}
    return min(first_positions, key=first_positions.get)


# ── Main Analysis Pipeline ──────────────────────────────────────────────────


def analyze(raw_data: dict) -> dict:
    """Run the full analysis pipeline on raw response data."""
    meta = raw_data["meta"]
    responses = raw_data["responses"]
    brand = meta["brand_name"]
    competitors = meta["competitors"]
    all_names = [brand] + competitors
    website_url = meta.get("website_url", "")

    if not responses:
        print("  [WARN] No responses to analyze (empty dataset).")

    # Per-prompt results
    prompt_results = []
    # Aggregate trackers
    mention_counts = defaultdict(int)
    rank_sums = defaultdict(float)
    rank_counts = defaultdict(int)
    win_counts = defaultdict(int)
    all_cited_domains = defaultdict(int)
    brand_cited_count = 0
    competitor_language = defaultdict(list)
    total_prompts_per_provider = defaultdict(int)

    for resp in responses:
        text = resp["response"]
        prompt_text = resp["prompt"]
        provider = resp["provider"]

        total_prompts_per_provider[provider] += 1

        # 1. Mention detection
        mentions = find_mentions(text, all_names)

        # 2. Brand rank
        brand_rank = compute_rank(mentions, brand)

        # 3. Track mention counts
        for name in all_names:
            if name in mentions:
                mention_counts[name] += 1

        # 4. Track ranks
        if brand_rank is not None:
            rank_sums[brand] += brand_rank
            rank_counts[brand] += 1

        for comp in competitors:
            comp_rank = compute_rank(mentions, comp)
            if comp_rank is not None:
                rank_sums[comp] += comp_rank
                rank_counts[comp] += 1

        # 5. Winner
        winner = determine_winner(mentions)
        if winner:
            win_counts[winner] += 1

        # 6. Sentiment for brand
        brand_sentiment = compute_sentiment(text, brand)

        # 7. Citations
        cited_domains = extract_citations(text)
        for domain in cited_domains:
            all_cited_domains[domain] += 1

        # Check if brand's domain is cited
        if website_url:
            brand_domain = re.sub(r'^https?://(www\.)?', '', website_url).split('/')[0].lower()
            if brand_domain and any(d == brand_domain or d.endswith("." + brand_domain) for d in cited_domains):
                brand_cited_count += 1

        # 8. Competitor mentions list
        comps_mentioned = [c for c in competitors if c in mentions]

        # 9. Framing for competitors
        for comp in comps_mentioned:
            framing = extract_framing(text, comp)
            if framing:
                competitor_language[comp].extend(framing)

        prompt_results.append({
            "prompt": prompt_text,
            "prompt_category": resp.get("prompt_category", "unknown"),
            "provider": provider,
            "brand_mentioned": brand in mentions,
            "brand_rank": brand_rank,
            "competitors_mentioned": comps_mentioned,
            "winner": winner,
            "sentiment": brand_sentiment,
            "cited_domains": cited_domains,
        })

    # ── Aggregate Metrics ───────────────────────────────────────────────

    total_responses = len(responses)

    # Share of voice
    share_of_voice = {}
    for name in all_names:
        mc = mention_counts.get(name, 0)
        avg_rank = round(rank_sums[name] / rank_counts[name], 2) if rank_counts[name] > 0 else None
        share_of_voice[name] = {
            "mention_count": mc,
            "mention_rate": round(mc / total_responses, 3) if total_responses > 0 else 0,
            "avg_rank": avg_rank,
            "win_count": win_counts.get(name, 0),
            "win_rate": round(win_counts.get(name, 0) / total_responses, 3) if total_responses > 0 else 0,
        }

    # Wins and losses
    wins = [r for r in prompt_results if r["brand_mentioned"] and r["brand_rank"] == 1]
    losses = [r for r in prompt_results if not r["brand_mentioned"] or (r["brand_rank"] and r["brand_rank"] > 1)]

    # Citation gaps
    citation_gaps = []
    for domain, count in sorted(all_cited_domains.items(), key=lambda x: -x[1])[:20]:
        citation_gaps.append({
            "domain": domain,
            "cited_count": count,
            "is_brand_domain": False,  # Updated below
        })

    if website_url:
        brand_domain = re.sub(r'^https?://(www\.)?', '', website_url).split('/')[0].lower()
        brand_gap_found = False
        for gap in citation_gaps:
            if brand_domain and (gap["domain"] == brand_domain or gap["domain"].endswith("." + brand_domain)):
                gap["is_brand_domain"] = True
                brand_gap_found = True
        
        if brand_domain and not brand_gap_found:
            actual_count = 0
            for d, c in all_cited_domains.items():
                if d == brand_domain or d.endswith("." + brand_domain):
                    actual_count += c
            citation_gaps.append({
                "domain": brand_domain,
                "cited_count": actual_count,
                "is_brand_domain": True,
            })

    # Deduplicate competitor language
    for comp in competitor_language:
        unique = list(set(competitor_language[comp]))
        competitor_language[comp] = sorted(unique)[:15]

    return {
        "meta": {
            "brand": brand,
            "competitors": competitors,
            "category": meta["category"],
            "website_url": meta.get("website_url", ""),
            "total_responses": total_responses,
            "providers_used": meta["providers_used"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "brand_domain_cited": brand_cited_count > 0,
            "brand_domain_citation_count": brand_cited_count,
            "responses_per_provider": dict(total_prompts_per_provider),
        },
        "share_of_voice": share_of_voice,
        "prompt_results": prompt_results,
        "wins": [{"prompt": w["prompt"], "provider": w["provider"]} for w in wins],
        "losses": [
            {
                "prompt": l["prompt"],
                "provider": l["provider"],
                "winner": l["winner"],
                "brand_rank": l["brand_rank"],
            }
            for l in losses
        ],
        "citation_gaps": citation_gaps,
        "competitor_language": dict(competitor_language),
    }


# ── Entry Point ─────────────────────────────────────────────────────────────


def main():
    print("\n" + "=" * 60)
    print("  GEO Gap Fixer — Analysis Engine")
    print("=" * 60)

    if not RAW_RESPONSES_PATH.exists():
        print(f"\n[ERROR] Raw responses not found: {RAW_RESPONSES_PATH}")
        print("  Run probe_llms.py first.")
        sys.exit(1)

    try:
        with open(RAW_RESPONSES_PATH, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] Invalid JSON in {RAW_RESPONSES_PATH}: {e}")
        sys.exit(1)

    # Validate structure
    if "responses" not in raw_data or "meta" not in raw_data:
        print("\n[ERROR] raw_responses.json is missing 'responses' or 'meta' key.")
        print("  Re-run probe_llms.py to regenerate.")
        sys.exit(1)

    total = len(raw_data.get("responses", []))
    print(f"  Loaded {total} responses from {RAW_RESPONSES_PATH.name}")
    print("-" * 60)

    # Run analysis
    analysis = analyze(raw_data)

    # Save
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(ANALYSIS_PATH, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    # Print summary
    brand = analysis["meta"]["brand"]
    sov = analysis["share_of_voice"]
    print(f"\n  Share of Voice:")
    print(f"  {'Name':<20} {'Mention Rate':>12} {'Avg Rank':>10} {'Win Rate':>10}")
    print(f"  {'-'*20} {'-'*12} {'-'*10} {'-'*10}")

    for name in sorted(sov, key=lambda n: -sov[n]["mention_rate"]):
        data = sov[name]
        mr = f"{data['mention_rate']:.0%}"
        ar = f"{data['avg_rank']}" if data['avg_rank'] else "—"
        wr = f"{data['win_rate']:.0%}"
        marker = " ← YOU" if name == brand else ""
        print(f"  {name:<20} {mr:>12} {ar:>10} {wr:>10}{marker}")

    print(f"\n  Wins:   {len(analysis['wins'])}")
    print(f"  Losses: {len(analysis['losses'])}")
    print(f"  Citations tracked: {len(analysis['citation_gaps'])} domains")

    print(f"\n  ✅ Saved analysis to {ANALYSIS_PATH}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
