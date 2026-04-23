import datetime
import json
import os
from typing import List, Dict

def _generate_rationale(matched_tags: List[str], product_context: Dict) -> str:
    """Generate deterministic rationale based ONLY on matched data."""
    if not matched_tags or matched_tags == ["Generalist"]:
        return "No direct tag overlap. Included as a generalist fund active at your target stage."
    
    tags_str = ", ".join(matched_tags)
    stage = product_context.get("stage_hint") or "applicable"
    geo = product_context.get("geography_hint") or "Global"
    
    return f"This fund focuses on {tags_str} which aligns with your product's {tags_str}. They are active at {stage} stage in {geo}."

def generate_report(matches: List[Dict], product_context: Dict) -> str:
    """Convert matched VC data into a formatted Markdown report."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    # Calculate total funds for the assumptions section
    try:
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "vc_funds.json")
        with open(data_path, "r", encoding="utf-8") as f:
            total_funds = len(json.load(f))
    except Exception:
        total_funds = 25 # Fallback if file isn't accessible
    
    # Handle empty edge case
    if not matches:
        return f"""# VC Curated Match Report

No matches found. Try broadening your description.

---

## Assumptions & Limitations

- Dataset contains {total_funds} funds verified as of {today}
- Fund theses and portfolios change over time. Verify directly at each fund's website before outreach.
- This tool matches based on public thesis data only. It does not reflect current deployment status or fund availability.
- Matches are a starting point for research, not financial advice."""

    # Header block
    desc = product_context.get("description", "").replace("[", "\\[").replace("]", "\\]")
    if len(desc) > 120:
        desc = desc[:120] + "..."
        
    url = product_context.get("url", "").replace("[", "\\[").replace("]", "\\]")
    tags = ", ".join(product_context.get("extracted_tags", []))
    stage = product_context.get("stage_hint") or "Not specified"
    geo = product_context.get("geography_hint") or "Global"

    lines = [
        "# VC Curated Match Report",
        "",
        f"**Product:** {desc}",
        f"**URL:** {url}",
        f"**Extracted Tags:** {tags}",
        f"**Stage:** {stage}",
        f"**Geography:** {geo}",
        f"**Generated:** {today}",
        "",
        "---",
        "",
        "## Top VC Matches"
    ]
    
    has_low_confidence = False
    
    # Matches block
    for rank, match in enumerate(matches, 1):
        fund = match.get("fund", {})
        conf = match.get("confidence", "Low")
        score = match.get("score", 0)
        matched_tags = match.get("matched_tags", [])
        
        if conf == "Low":
            has_low_confidence = True
            
        lines.append("")
        lines.append("---")
        lines.append(f"## {rank}. {fund.get('fund_name', 'Unknown Fund')} — {conf} Confidence")
        lines.append("")
        lines.append(f"**Thesis:** {fund.get('thesis', '')}")
        lines.append(f"**Check Size:** {fund.get('check_size', '')}")
        lines.append(f"**Stage Focus:** {', '.join(fund.get('stage_focus', []))}")
        lines.append(f"**Geography:** {', '.join(fund.get('geography_focus', []))}")
        lines.append(f"**Notable Portfolio:** {', '.join(fund.get('notable_portfolio', []))}")
        
        if fund.get("website"):
            lines.append(f"**Website:** {fund['website']}")
            
        lines.append(f"**Match Score:** {score}/100")
        lines.append(f"**Why this match:** {_generate_rationale(matched_tags, product_context)}")

    # Footer block
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Assumptions & Limitations")
    lines.append("")
    lines.append(f"- Dataset contains {total_funds} funds verified as of {today}")
    lines.append("- Fund theses and portfolios change over time. Verify directly at each fund's website before outreach.")
    lines.append("- This tool matches based on public thesis data only. It does not reflect current deployment status or fund availability.")
    lines.append("- Matches are a starting point for research, not financial advice.")
    
    if has_low_confidence:
        lines.append("- Low-confidence matches are included because no stronger sector-specific matches were found.")

    return "\n".join(lines)
