"""
match_funds.py -- standalone scoring script for vc-finder curated pre-match.
Scores data/vc_funds.json against a product context and outputs ranked matches.

Usage:
  python3 scripts/match_funds.py \
      --tags "DevTools,B2B SaaS" \
      --stage Seed \
      --geo US \
      --output /tmp/vc-curated-matches.json

Available tags:
  DevTools, Infrastructure, Open Source, B2B SaaS, AI, Data, FinTech, HealthTech,
  Enterprise, Consumer, Marketplaces, E-commerce, Crypto, DeepTech, Cybersecurity, Generalist
"""

import argparse
import json
import os
import sys

STAGE_ORDER = {"Pre-seed": 0, "Seed": 1, "Series A": 2, "Growth": 3}


def score_fund(fund, context):
    score = 0
    fund_tags = fund.get("industry_tags", [])
    extracted_tags = context.get("extracted_tags", ["Generalist"])

    tag_points = 0
    matched_tags = []
    for tag in extracted_tags:
        if tag in fund_tags:
            tag_points += 5 if tag == "Generalist" else 20
            matched_tags.append(tag)
    tag_points = min(tag_points, 60)
    score += tag_points

    stage_hint = context.get("stage_hint")
    fund_stages = fund.get("stage_focus", [])
    if not stage_hint:
        score += 10
    elif fund_stages:
        if stage_hint in fund_stages:
            score += 20
        elif stage_hint in STAGE_ORDER:
            hint_idx = STAGE_ORDER[stage_hint]
            if any(f in STAGE_ORDER and abs(STAGE_ORDER[f] - hint_idx) == 1 for f in fund_stages):
                score += 10

    geo_hint = context.get("geography_hint")
    fund_geo = fund.get("geography_focus", ["Global"])
    if not geo_hint or geo_hint == "Global":
        score += 10
    elif fund_geo == ["India"] and geo_hint == "US":
        pass
    elif geo_hint in fund_geo:
        score += 20
    elif "Global" in fund_geo:
        score += 15

    if geo_hint == "US" and "India" in fund_geo and "US" not in fund_geo and "Global" not in fund_geo:
        score = max(0, score - 30)
    if fund_tags and extracted_tags and fund_tags[0] not in extracted_tags and tag_points <= 20:
        score = max(0, score - 15)

    return score, matched_tags


def get_confidence_tier(score):
    if score >= 70:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tags", required=True, help="Comma-separated industry tags")
    parser.add_argument("--stage", default="", help="Pre-seed / Seed / Series A / Growth")
    parser.add_argument("--geo", default="", help="US / Europe / India / Global")
    parser.add_argument("--funds", default="data/vc_funds.json")
    parser.add_argument("--output", default="/tmp/vc-curated-matches.json")
    args = parser.parse_args()

    context = {
        "extracted_tags": [t.strip() for t in args.tags.split(",") if t.strip()],
        "stage_hint": args.stage or None,
        "geography_hint": args.geo or None,
    }

    funds_path = args.funds
    if not os.path.exists(funds_path):
        print(f"ERROR: {funds_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(funds_path) as f:
        funds = json.load(f)

    scored = []
    for fund in funds:
        score, matched_tags = score_fund(fund, context)
        tier = get_confidence_tier(score)
        scored.append({
            "fund_name": fund["fund_name"],
            "thesis": fund["thesis"],
            "check_size": fund["check_size"],
            "stage_focus": fund["stage_focus"],
            "industry_tags": fund["industry_tags"],
            "geography_focus": fund["geography_focus"],
            "notable_portfolio": fund["notable_portfolio"],
            "website": fund["website"],
            "source": "verified (fund website)",
            "score": score,
            "confidence": tier,
            "matched_tags": matched_tags,
        })

    scored.sort(key=lambda x: (-x["score"], x["fund_name"]))
    relevant = [m for m in scored if m["confidence"] in ("High", "Medium")]

    curated_comparables = []
    for m in relevant:
        for company in m.get("notable_portfolio", []):
            if company not in curated_comparables:
                curated_comparables.append(company)

    output = {
        "high_medium_matches": relevant,
        "curated_comparables": curated_comparables[:6],
    }

    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Curated matches: {len(relevant)} High/Medium confidence funds")
    for m in relevant[:8]:
        print(f"  {m['confidence']:6} ({m['score']:3}) {m['fund_name']} | {m['matched_tags']}")
    print(f"Portfolio seed comparables: {curated_comparables[:6]}")


if __name__ == "__main__":
    main()
