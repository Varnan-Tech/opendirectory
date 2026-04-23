import json
import os
from typing import List, Dict, Tuple

def load_funds(data_path: str) -> List[Dict]:
    """Load data/vc_funds.json"""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def score_fund(fund: Dict, product_context: Dict) -> Tuple[int, List[str]]:
    """Score a single fund based on overlap with product context."""
    score = 0
    
    # 1. Tag Overlap (max 60 points)
    fund_tags = fund.get("industry_tags", [])
    extracted_tags = product_context.get("extracted_tags", [])
    if not extracted_tags:
        extracted_tags = ["Generalist"]
        
    tag_points = 0
    matched_tags = []
    
    for tag in extracted_tags:
        if tag in fund_tags:
            if tag == "Generalist":
                tag_points += 5
            else:
                tag_points += 20
            matched_tags.append(tag)
            
    tag_points = min(tag_points, 60)
    score += tag_points
    
    # 2. Stage Match (max 20 points)
    stage_points = 0
    stage_hint = product_context.get("stage_hint")
    fund_stages = fund.get("stage_focus", [])
    
    STAGE_ORDER = {"Pre-seed": 0, "Seed": 1, "Series A": 2, "Growth": 3}
    
    if not stage_hint:
        stage_points = 10
    elif not fund_stages:
        pass # skip stage scoring
    else:
        if stage_hint in fund_stages:
            stage_points = 20
        else:
            is_adjacent = False
            if stage_hint in STAGE_ORDER:
                hint_idx = STAGE_ORDER[stage_hint]
                for f_stage in fund_stages:
                    if f_stage in STAGE_ORDER and abs(STAGE_ORDER[f_stage] - hint_idx) == 1:
                        is_adjacent = True
                        break
            if is_adjacent:
                stage_points = 10

    score += stage_points
    
    # 3. Geography Match (max 20 points)
    geo_points = 0
    geo_hint = product_context.get("geography_hint")
    fund_geo = fund.get("geography_focus", [])
    if not fund_geo:
        fund_geo = ["Global"]
        
    if not geo_hint or geo_hint == "Global":
        geo_points = 10
    elif fund_geo == ["India"] and geo_hint == "US":
        geo_points = 0
    elif geo_hint in fund_geo:
        geo_points = 20
    elif "Global" in fund_geo:
        geo_points = 15
        
    score += geo_points
    
    # 4. Final Penalties
    # Bug 1: India-only funds in US searches penalty
    if geo_hint == "US" and "India" in fund_geo and "US" not in fund_geo and "Global" not in fund_geo:
        score = max(0, score - 30)
        
    # Bug 2: Primary focus mismatch 
    if fund_tags and extracted_tags:
        if fund_tags[0] not in extracted_tags and tag_points <= 20:
            score = max(0, score - 15)
    
    return score, matched_tags

def get_confidence_tier(score: int) -> str:
    """Return High/Medium/Low based on score."""
    if score >= 70:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"

def match_vcs(product_context: Dict, data_path: str = "data/vc_funds.json") -> List[Dict]:
    """Score all funds and return prioritized matches."""
    funds = load_funds(data_path)
    scored_funds = []
    
    for fund in funds:
        score, matched_tags = score_fund(fund, product_context)
        scored_funds.append({
            "fund": fund,
            "score": score,
            "confidence": get_confidence_tier(score),
            "matched_tags": matched_tags
        })
        
    scored_funds.sort(key=lambda x: (-x["score"], x["fund"].get("fund_name", "")))
    
    if all(f["score"] == 0 for f in scored_funds):
        generalists = [f for f in funds if "Generalist" in f.get("industry_tags", [])][:5]
        return [{
            "fund": g,
            "score": 0,
            "confidence": "Low",
            "matched_tags": ["Generalist"],
            "warning": "No strong matches found. Showing generalist funds only."
        } for g in generalists]
        
    return scored_funds[:10]
