#!/usr/bin/env python3
"""
build_report.py — Assemble the GEO audit report from analysis data.

Reads data/analysis.json and produces:
  - report/geo_audit_report.md  (human-readable markdown)
  - report/geo_audit_report.json (machine-readable structured data)

The markdown report contains all 5 required sections:
  1. Share-of-Voice Table
  2. Prompt-Level Loss Log
  3. Competitor Language Patterns
  4. Citation Gap List
  5. GEO Action Plan

Usage:
    python scripts/build_report.py
"""

import json
import sys
from pathlib import Path

# Schema version for the JSON report — bump when output shape changes.
SCHEMA_VERSION = "1.0.0"

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
ANALYSIS_PATH = DATA_DIR / "analysis.json"
REPORT_DIR = SKILL_ROOT / "report"
REPORT_MD_PATH = REPORT_DIR / "geo_audit_report.md"
REPORT_JSON_PATH = REPORT_DIR / "geo_audit_report.json"


# ── Report Sections ────────────────────────────────────────────────────────


def build_header(meta: dict) -> str:
    """Build the report header."""
    providers = ", ".join(meta["providers_used"])
    return f"""# GEO Gap Audit Report — {meta['brand']}

> **Generated**: {meta['timestamp']}
> **Category**: {meta['category']}
> **Providers**: {providers}
> **Total responses analyzed**: {meta['total_responses']}

---
"""


def build_share_of_voice(sov: dict, brand: str) -> str:
    """Section 1: Share-of-Voice Table."""
    lines = [
        "## 1. Share-of-Voice Table\n",
        "How often each brand is mentioned and recommended by LLMs.\n",
        "| Brand | Mention Rate | Avg Rank | Win Rate | Mentioned | Wins |",
        "|-------|-------------|----------|----------|-----------|------|",
    ]

    sorted_names = sorted(sov, key=lambda n: -sov[n]["mention_rate"])
    for name in sorted_names:
        d = sov[name]
        mr = f"{d['mention_rate']:.0%}"
        ar = f"{d['avg_rank']:.1f}" if d["avg_rank"] is not None else "—"
        wr = f"{d['win_rate']:.0%}"
        mc = str(d["mention_count"])
        wc = str(d["win_count"])
        marker = " **← YOU**" if name == brand else ""
        lines.append(f"| {name}{marker} | {mr} | {ar} | {wr} | {mc} | {wc} |")

    # Health assessment
    brand_data = sov.get(brand, {})
    mr = brand_data.get("mention_rate", 0)
    wr = brand_data.get("win_rate", 0)

    if mr >= 0.6 and wr >= 0.3:
        health = "🟢 **Healthy** — LLMs consistently recommend you"
    elif mr >= 0.3 and wr >= 0.1:
        health = "🟡 **At Risk** — Visible but not dominant; targeted fixes needed"
    else:
        health = "🔴 **Critical** — LLMs rarely mention you; major GEO overhaul needed"

    lines.append(f"\n**Overall Health**: {health}\n")
    lines.append("---\n")
    return "\n".join(lines)


def build_loss_log(losses: list, brand: str) -> str:
    """Section 2: Prompt-Level Loss Log."""
    lines = [
        "## 2. Prompt-Level Loss Log\n",
        "Prompts where your brand was NOT mentioned first (or not at all).\n",
    ]

    if not losses:
        lines.append("🎉 **No losses detected!** Your brand was mentioned first in every response.\n")
        lines.append("---\n")
        return "\n".join(lines)

    lines.extend([
        "| # | Prompt | Provider | Winner | Your Rank |",
        "|---|--------|----------|--------|-----------|",
    ])

    for i, loss in enumerate(losses[:30], 1):  # Cap at 30 rows
        prompt = loss["prompt"]
        if len(prompt) > 60:
            prompt = prompt[:57] + "..."
        # Escape pipe characters that would break the markdown table
        prompt = prompt.replace("|", "\\|")
        provider = loss["provider"]
        winner = (loss.get("winner") or "—").replace("|", "\\|")
        rank = str(loss.get("brand_rank")) if loss.get("brand_rank") else "Not mentioned"
        lines.append(f"| {i} | {prompt} | {provider} | {winner} | {rank} |")

    if len(losses) > 30:
        lines.append(f"\n*...and {len(losses) - 30} more losses (see JSON report for full list)*\n")

    lines.append(f"\n**Total losses**: {len(losses)} out of all analyzed responses\n")
    lines.append("---\n")
    return "\n".join(lines)


def build_competitor_language(comp_lang: dict, brand: str) -> str:
    """Section 3: Competitor Language Patterns."""
    lines = [
        "## 3. Competitor Language Patterns\n",
        "How LLMs describe your competitors — keywords and framing you may be missing.\n",
    ]

    if not comp_lang:
        lines.append("No competitor language patterns detected.\n")
        lines.append("---\n")
        return "\n".join(lines)

    for comp, phrases in sorted(comp_lang.items()):
        lines.append(f"### {comp}")
        if phrases:
            lines.append(f"**Framing used by LLMs**: {', '.join(f'`{p}`' for p in phrases[:10])}")
        else:
            lines.append("No distinctive framing detected.")
        lines.append("")

    lines.append(
        "**💡 Insight**: If competitors are described with keywords your brand lacks, "
        "consider incorporating similar language into your website copy, "
        "comparison pages, and product descriptions.\n"
    )
    lines.append("---\n")
    return "\n".join(lines)


def build_citation_gaps(gaps: list, meta: dict) -> str:
    """Section 4: Citation Gap List."""
    lines = [
        "## 4. Citation Gap List\n",
        "Domains cited by LLMs in their responses. If your domain isn't here, "
        "LLMs don't consider your site an authoritative source.\n",
    ]

    if not gaps:
        lines.append("No citations detected in LLM responses.\n")
        lines.append("---\n")
        return "\n".join(lines)

    lines.extend([
        "| Domain | Times Cited | Your Domain? |",
        "|--------|-------------|-------------|",
    ])

    for gap in gaps[:20]:
        domain = gap["domain"]
        count = gap["cited_count"]
        is_brand = "✅ Yes" if gap.get("is_brand_domain") else "❌ No"
        lines.append(f"| {domain} | {count} | {is_brand} |")

    brand_cited = any(g.get("is_brand_domain") for g in gaps)
    if not brand_cited and meta.get("website_url"):
        lines.append(
            f"\n⚠️ **Your domain ({meta['website_url']}) was never cited by any LLM.**\n"
        )

    lines.append("---\n")
    return "\n".join(lines)


def build_action_plan(analysis: dict) -> str:
    """Section 5: GEO Action Plan — the core deliverable."""
    sov = analysis["share_of_voice"]
    losses = analysis["losses"]
    gaps = analysis["citation_gaps"]
    comp_lang = analysis["competitor_language"]
    brand = analysis["meta"]["brand"]
    competitors = analysis["meta"]["competitors"]
    category = analysis["meta"]["category"]

    brand_data = sov.get(brand, {})
    mr = brand_data.get("mention_rate", 0)
    wr = brand_data.get("win_rate", 0)

    lines = [
        "## 5. GEO Action Plan\n",
        "Prioritized content and positioning fixes based on the audit findings.\n",
    ]

    # ── Critical Actions ────────────────────────────────────────────
    critical = []

    if mr < 0.3:
        critical.append(
            f'- [ ] **Create FAQ page**: "What is the best {category}?" — '
            f"your brand is mentioned in only {mr:.0%} of responses"
        )

    # Find top competitor
    top_comp = None
    top_comp_wr = 0
    for comp in competitors:
        cwr = sov.get(comp, {}).get("win_rate", 0)
        if cwr > top_comp_wr:
            top_comp = comp
            top_comp_wr = cwr

    if top_comp and top_comp_wr > wr:
        critical.append(
            f'- [ ] **Create comparison page**: "{brand} vs {top_comp}" — '
            f"{top_comp} wins {top_comp_wr:.0%} of prompts vs your {wr:.0%}"
        )

    # Check for losses on direct prompts
    direct_losses = [l for l in losses if "best" in l["prompt"].lower() or "recommend" in l["prompt"].lower()]
    if len(direct_losses) > 3:
        critical.append(
            f"- [ ] **Optimize landing page** for \"{category}\" — "
            f"you lost {len(direct_losses)} direct recommendation prompts"
        )

    if critical:
        lines.append("### 🔴 Critical (Do First)\n")
        lines.extend(critical)
        lines.append("")

    # ── High Priority ───────────────────────────────────────────────
    high = []

    # Alternative pages for each competitor that beats the brand
    for comp in competitors:
        comp_mr = sov.get(comp, {}).get("mention_rate", 0)
        if comp_mr > mr and comp != top_comp:
            high.append(
                f'- [ ] **Create alternatives page**: "Best alternatives to {comp}" — '
                f"{comp} has {comp_mr:.0%} mention rate vs your {mr:.0%}"
            )

    # Schema markup if no citations
    brand_cited = any(g.get("is_brand_domain") for g in gaps)
    if not brand_cited:
        high.append(
            "- [ ] **Add schema markup**: FAQPage, SoftwareApplication, Organization — "
            "your domain is not being cited by any LLM"
        )

    # Content depth if sentiment is neutral/negative
    brand_sent = None
    for pr in analysis.get("prompt_results", []):
        if pr.get("sentiment", {}).get("label") == "negative":
            brand_sent = "negative"
            break
    if brand_sent == "negative":
        high.append(
            "- [ ] **Address negative framing**: Review and update product descriptions "
            "to counter negative keywords found in LLM responses"
        )

    if high:
        lines.append("### 🟡 High Priority\n")
        lines.extend(high)
        lines.append("")

    # ── Growth Plays ────────────────────────────────────────────────
    growth = []

    # Authority domains
    cited_domains = [g["domain"] for g in gaps if not g.get("is_brand_domain") and g["cited_count"] >= 2]
    if cited_domains[:3]:
        domains_str = ", ".join(cited_domains[:3])
        growth.append(
            f"- [ ] **Build authority on cited domains**: Get listed/mentioned on {domains_str} — "
            "these are domains LLMs trust and cite"
        )

    # Competitor language mirroring
    if comp_lang:
        all_comp_phrases = set()
        for phrases in comp_lang.values():
            all_comp_phrases.update(phrases[:5])
        if all_comp_phrases:
            sample = ", ".join(f'"{p}"' for p in list(all_comp_phrases)[:5])
            growth.append(
                f"- [ ] **Mirror competitor framing**: Incorporate language like {sample} "
                "into your product pages and descriptions"
            )

    # Data-backed content
    growth.append(
        '- [ ] **Publish original data/statistics**: Add "according to" citations, '
        "benchmarks, and original research that LLMs can extract and cite"
    )

    # Regular auditing
    growth.append(
        "- [ ] **Schedule monthly re-audits**: Run this skill monthly to track "
        "whether your GEO improvements are working"
    )

    if growth:
        lines.append("### 🟢 Growth Plays\n")
        lines.extend(growth)
        lines.append("")

    # ── Summary ─────────────────────────────────────────────────────
    total_actions = len(critical) + len(high) + len(growth)
    lines.append(f"\n**Total actions**: {total_actions} items in your GEO backlog")
    lines.append(f"**Focus first on**: 🔴 Critical items ({len(critical)} actions)\n")
    lines.append("---\n")
    lines.append(
        "*Report generated by [geo-gap-fixer](https://github.com/Varnan-Tech/opendirectory) "
        "— an OpenDirectory skill for GEO auditing.*\n"
    )

    return "\n".join(lines)


# ── Report Assembly ─────────────────────────────────────────────────────────


def build_full_report(analysis: dict) -> str:
    """Assemble the full markdown report."""
    sections = [
        build_header(analysis["meta"]),
        build_share_of_voice(analysis["share_of_voice"], analysis["meta"]["brand"]),
        build_loss_log(analysis["losses"], analysis["meta"]["brand"]),
        build_competitor_language(analysis["competitor_language"], analysis["meta"]["brand"]),
        build_citation_gaps(analysis["citation_gaps"], analysis["meta"]),
        build_action_plan(analysis),
    ]
    return "\n".join(sections)


def build_json_report(analysis: dict) -> dict:
    """Build the structured JSON report."""
    sov = analysis["share_of_voice"]
    brand = analysis["meta"]["brand"]
    brand_data = sov.get(brand, {})

    return {
        "schema_version": SCHEMA_VERSION,
        "meta": analysis["meta"],
        "summary": {
            "brand_mention_rate": brand_data.get("mention_rate", 0),
            "brand_win_rate": brand_data.get("win_rate", 0),
            "brand_avg_rank": brand_data.get("avg_rank"),
            "total_wins": len(analysis.get("wins", [])),
            "total_losses": len(analysis.get("losses", [])),
            "citation_domains_found": len(analysis.get("citation_gaps", [])),
        },
        "share_of_voice": analysis["share_of_voice"],
        "prompt_results": analysis.get("prompt_results", []),
        "losses": analysis.get("losses", []),
        "citation_gaps": analysis.get("citation_gaps", []),
        "competitor_language": analysis.get("competitor_language", {}),
    }


# ── Entry Point ─────────────────────────────────────────────────────────────


def main():
    print("\n" + "=" * 60)
    print("  GEO Gap Fixer — Report Builder")
    print("=" * 60)

    if not ANALYSIS_PATH.exists():
        print(f"\n[ERROR] Analysis file not found: {ANALYSIS_PATH}")
        print("  Run analyze_results.py first.")
        sys.exit(1)

    try:
        with open(ANALYSIS_PATH, "r", encoding="utf-8") as f:
            analysis = json.load(f)
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] Invalid JSON in {ANALYSIS_PATH}: {e}")
        sys.exit(1)

    # Validate required keys
    required_keys = ["meta", "share_of_voice", "losses"]
    missing = [k for k in required_keys if k not in analysis]
    if missing:
        print(f"\n[ERROR] analysis.json is missing required keys: {', '.join(missing)}")
        print("  Re-run analyze_results.py to regenerate.")
        sys.exit(1)

    brand = analysis["meta"]["brand"]
    print(f"  Building report for: {brand}")
    print("-" * 60)

    # Build reports
    md_report = build_full_report(analysis)
    json_report = build_json_report(analysis)

    # Save
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    with open(REPORT_MD_PATH, "w", encoding="utf-8") as f:
        f.write(md_report)

    with open(REPORT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(json_report, f, indent=2, ensure_ascii=False)

    print(f"\n  ✅ Markdown report: {REPORT_MD_PATH}")
    print(f"  ✅ JSON report:     {REPORT_JSON_PATH}")

    # Quick preview
    sov = analysis["share_of_voice"]
    brand_data = sov.get(brand, {})
    print(f"\n  📊 Brand mention rate: {brand_data.get('mention_rate', 0):.0%}")
    print(f"  📊 Brand win rate:     {brand_data.get('win_rate', 0):.0%}")
    print(f"  📊 Total losses:       {len(analysis['losses'])}")
    print(f"\n  → Open {REPORT_MD_PATH.name} to see your GEO action plan")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
