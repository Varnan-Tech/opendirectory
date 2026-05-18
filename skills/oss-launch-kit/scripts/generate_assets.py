"""Generate a coordinated OSS launch strategy and asset bundle.

This module acts as an orchestrator: it determines readiness, evaluates channel
fitness, and provides strategic hooks and handoffs to specialized skills.
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any


def _clean(text: str | None) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def _strip_markdown(text: str | None) -> str:
    cleaned = text or ""
    cleaned = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", cleaned)
    cleaned = re.sub(r"\[([^\]]+)\]\[\]", r"\1", cleaned)
    cleaned = re.sub(r"[`*_>#]", "", cleaned)
    return _clean(cleaned)


def _shorten(text: str, limit: int) -> str:
    text = _clean(text)
    if len(text) <= limit:
        return text
    truncated = text[:limit].rstrip()
    if " " in truncated:
        truncated = truncated[: truncated.rfind(" ")].rstrip()
    return truncated + "..."


def _repo_slug(brief: dict[str, Any]) -> str:
    return _clean(brief.get("repo_name") or "unknown-repo")


def _title_case(text: str) -> str:
    words = text.split()
    return " ".join(word if len(word) <= 3 else word[:1].upper() + word[1:] for word in words)


def _strip_trailing_period(text: str) -> str:
    return text[:-1] if text.endswith(".") else text


def _canonical_summary(brief: dict[str, Any]) -> str:
    summary = _strip_markdown(brief.get("one_line_summary"))
    if summary:
        return _strip_trailing_period(summary)

    problem = _strip_markdown(brief.get("problem_solved"))
    if problem:
        return _strip_trailing_period(problem)

    return "an open-source project"


def _choose_show_hn_title(brief: dict[str, Any]) -> str:
    repo_name = _repo_slug(brief)
    summary = _canonical_summary(brief)
    audience = _strip_markdown(brief.get("audience"))

    candidates = []
    if summary and audience and audience != "unknown":
        candidates.append(f"Show HN: {repo_name} - {summary} for {audience}")
    if summary:
        candidates.append(f"Show HN: {repo_name} - {summary}")
    candidates.append(f"Show HN: {repo_name}")

    for candidate in candidates:
        if len(candidate) <= 72:
            return candidate
    return candidates[-1]


def _intro_line(brief: dict[str, Any]) -> str:
    repo_name = _repo_slug(brief)
    summary = _canonical_summary(brief)
    audience = _strip_markdown(brief.get("audience"))
    if audience and audience != "unknown":
        return _shorten(f"I built {repo_name} because I wanted a clearer way to serve {audience} who need {summary.lower()}.", 220)
    return _shorten(f"I built {repo_name} because I wanted a clearer way to package {summary.lower()} as a launchable OSS project.", 220)


def _low_confidence_note(brief: dict[str, Any]) -> str:
    confidence = _clean(brief.get("confidence"))
    assumptions = brief.get("assumptions") or []
    if confidence == "low" or assumptions:
        notes = [f"Confidence: {confidence or 'unknown'}"]
        if assumptions:
            notes.append("Assumptions: " + "; ".join(assumptions[:3]).rstrip("."))
        return "\n".join(f"- {note}" for note in notes)
    return "- Confidence: high"


def _is_low_confidence(brief: dict[str, Any]) -> bool:
    return _clean(brief.get("confidence")) == "low" or bool(brief.get("assumptions"))


def _low_confidence_edit_note() -> str:
    return "Edit before posting: this repo context is sparse, so tighten the copy after reviewing the README and repo signals."


def _normalize_phrase(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", _clean(text).lower()).strip()


def _phrase_overlap(a: str, b: str) -> bool:
    a_words = {word for word in _normalize_phrase(a).split() if len(word) > 2}
    b_words = {word for word in _normalize_phrase(b).split() if len(word) > 2}
    if not a_words or not b_words:
        return False
    return len(a_words & b_words) >= 3


def _is_marketing_heavy(text: str) -> bool:
    normalized = _normalize_phrase(text)
    signals = [
        "worlds best",
        "ultimate",
        "powerful",
        "all in one",
        "beautiful",
        "magical",
        "supercharge",
        "next generation",
        "revolutionary",
        "seamless",
        "unlock",
        "delight",
        "built for teams",
        "move faster",
    ]
    return any(signal in normalized for signal in signals)


def _ph_repo_category(brief: dict[str, Any]) -> str:
    text = " ".join(
        part
        for part in [
            _strip_markdown(brief.get("problem_solved")),
            _strip_markdown(brief.get("one_line_summary")),
            _strip_markdown(brief.get("value_proposition")),
        ]
        if part
    ).lower()
    if any(term in text for term in ["framework", "sdk"]):
        return "framework"
    if any(term in text for term in ["library", "package", "module"]):
        return "library"
    if any(term in text for term in ["cli", "tool", "automation", "workflow", "build", "deploy"]):
        return "tool"
    if any(term in text for term in ["design", "css", "ui", "frontend"]):
        return "UI toolkit"
    return "open-source project"


def _render_low_confidence_note(brief: dict[str, Any]) -> str:
    note = _low_confidence_note(brief)
    if _is_low_confidence(brief):
        note += "\n" + _low_confidence_edit_note()
    return note

def _tagline_candidates(brief: dict[str, Any]) -> list[str]:
    summary = _canonical_summary(brief)
    audience = _strip_markdown(brief.get("audience"))
    problem = _strip_markdown(brief.get("problem_solved"))
    features = [_strip_markdown(feature) for feature in (brief.get("key_features") or [])[:3]]
    repo_name = _repo_slug(brief)
    value_prop = _strip_markdown(brief.get("value_proposition"))
    focus = features[0] if features else summary

    candidates = []
    if audience and audience != "unknown":
        candidates.append(f"Launch copy for {audience} built from repo facts")
    if problem:
        candidates.append(f"Turns {problem.lower()} into launch-ready copy")
    if value_prop:
        candidates.append(_shorten(value_prop, 60))
    if focus:
        candidates.append(_shorten(f"Built for repos about {focus.lower()}", 60))
    candidates.extend(
        [
            f"Launch assets grounded in README and metadata",
            f"Turns GitHub repos into launch copy",
            f"Helps OSS maintainers write launch-ready posts",
        ]
    )
    if repo_name:
        candidates.append(f"Launch copy for {repo_name}")
    return [candidate for candidate in candidates if candidate]


def _pick_tagline(brief: dict[str, Any]) -> str:
    candidates = []
    for candidate in _tagline_candidates(brief):
        candidate = _strip_markdown(candidate)
        if not candidate:
            continue
        if candidate.lower().startswith(_repo_slug(brief).lower()):
            continue
        if candidate.endswith(".") or candidate.endswith("?"):
            candidate = candidate[:-1]
        if len(candidate) <= 60:
            candidates.append(candidate)
    if candidates:
        return candidates[0]
    fallback = _strip_markdown(brief.get("value_proposition")) or "Launch copy grounded in repo facts"
    return _shorten(fallback, 60)

def _reddit_subreddit_candidates(brief: dict[str, Any]) -> list[tuple[str, str]]:
    audience = _strip_markdown(brief.get("audience")).lower()
    summary = _canonical_summary(brief).lower()
    title = _repo_slug(brief).lower()
    candidates: list[tuple[str, str]] = []
    low_conf = _is_low_confidence(brief)

    def add(subreddit: str, context: str) -> None:
        if subreddit and subreddit.lower() not in {item[0].lower() for item in candidates}:
            candidates.append((subreddit, context))

    if low_conf:
        return [
            ("r/opensource", "open-source launch context"),
            ("r/SideProject", "general maker context"),
            ("r/programming", "developer audience"),
            ("r/devtools", "developer tools audience"),
            ("r/commandline", "command-line users"),
        ]

    if any(term in summary for term in ["cli", "tool", "automation", "build", "deploy", "developer"]):
        add("r/devtools", "developer tools audience")
    if any(term in summary for term in ["open source", "oss", "github", "repo"]):
        add("r/opensource", "open-source launch context")
    if any(term in audience for term in ["developer", "engineer", "team"]):
        add("r/programming", "developer audience")
    if any(term in summary for term in ["side project", "indie", "personal"]):
        add("r/SideProject", "maker / indie launch context")
    if any(term in summary for term in ["python", "go", "rust", "javascript", "typescript"]):
        for topic in ["python", "go", "rust", "javascript", "typescript"]:
            if topic in summary:
                add(f"r/{topic.capitalize()}", f"language-specific community for {topic}")
                break

    if "cli" in title or "terminal" in summary:
        add("r/commandline", "command-line users")
    if any(term in summary for term in ["self-host", "server", "infra", "pipeline", "ci"]):
        add("r/devops", "devops / infrastructure audience")

    fallback_pool = [
        ("r/SideProject", "general maker context"),
        ("r/opensource", "open-source launch context"),
        ("r/programming", "developer audience"),
        ("r/devtools", "developer tools audience"),
        ("r/commandline", "command-line users"),
    ]
    for subreddit, context in fallback_pool:
        add(subreddit, context)

    seen: set[str] = set()
    deduped: list[tuple[str, str]] = []
    for subreddit, context in candidates:
        key = subreddit.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append((subreddit, context))
        if len(deduped) == 5:
            break
    return deduped


def generate_product_hunt(brief: dict[str, Any]) -> dict[str, str]:
    """Generate Product Hunt assets from a grounded brief."""

    repo_name = _repo_slug(brief)
    audience = _strip_markdown(brief.get("audience"))
    summary = _strip_markdown(brief.get("one_line_summary")) or _canonical_summary(brief)
    problem = _strip_markdown(brief.get("problem_solved"))
    value_prop = _strip_markdown(brief.get("value_proposition"))
    low_confidence = _is_low_confidence(brief)
    marketing_heavy = _is_marketing_heavy(summary) or _is_marketing_heavy(problem) or _is_marketing_heavy(value_prop)
    category = _ph_repo_category(brief)

    if low_confidence:
        return {
            "tagline": f"Draft: {repo_name}",
            "description": "Draft only. Not enough repo signal for a polished Product Hunt description. Edit after reviewing the README and metadata.",
            "maker_comment": "Draft only. This needs manual editing before posting.",
        }

    if audience and audience != "unknown":
        audience_phrase = audience
    else:
        audience_phrase = "OSS builders"

    if marketing_heavy:
        audience_phrase = category
        description = _shorten(
            f"Built for {audience_phrase}. This draft keeps the pitch factual and avoids repeating the README’s slogans.",
            220,
        )
    else:
        description_parts = [f"Built for {audience_phrase}."]
        if problem and not _phrase_overlap(problem, summary):
            description_parts.append("Focuses on the repo’s core function instead of reusing README language.")
        elif summary and not _phrase_overlap(summary, problem or summary):
            description_parts.append("Keeps the pitch factual and plain.")
        else:
            description_parts.append("Keeps the pitch grounded in repo facts.")
        description = _shorten(" ".join(description_parts), 220)

    if category.lower() == audience_phrase.lower():
        tagline = f"{repo_name}: {category}"
    else:
        tagline = f"{repo_name}: {category} for {audience_phrase}"

    maker_comment = "Draft only. Edit before posting."
    return {
        "tagline": tagline,
        "description": description,
        "maker_comment": maker_comment,
    }


def render_channel_strategy(brief: dict[str, Any]) -> str:
    """Render concise channel strategy with hooks and handoffs."""
    fitness = brief.get("channel_fitness") or {}
    type_ = brief.get("project_type") or "project"
    repo_name = _repo_slug(brief)
    summary = _canonical_summary(brief)
    
    sections = ["## Channel Strategy & Positioning"]
    
    # Show HN
    if fitness.get("show_hn") != "low":
        title = _choose_show_hn_title(brief)
        hook = _intro_line(brief)
        sections.append(f"### [Show HN] - Fit: {fitness.get('show_hn', '').upper()}")
        sections.append(f"**Positioning**: Focus on technical implementation and 'why I built this'.")
        sections.append(f"**Recommended Title**: `{title}`")
        sections.append(f"**Hook**: {hook}")
        sections.append("> [!TIP]\n> Use `show-hn-writer` for a full submission draft.")
        sections.append("")

    # Product Hunt
    if fitness.get("product_hunt") != "low":
        ph = generate_product_hunt(brief)
        sections.append(f"### [Product Hunt] - Fit: {fitness.get('product_hunt', '').upper()}")
        sections.append(f"**Positioning**: Highlight the {type_}'s utility for the broader maker community.")
        sections.append(f"**Tagline**: {ph['tagline']}")
        sections.append(f"**Brief**: {ph['description']}")
        sections.append("> [!TIP]\n> Use `producthunt-launch-kit` for full asset generation (badges, images).")
        sections.append("")
        
    # Reddit
    if fitness.get("reddit") != "low":
        candidates = _reddit_subreddit_candidates(brief)
        sections.append(f"### [Reddit] - Fit: {fitness.get('reddit', '').upper()}")
        sections.append(f"**Niche Strategy**: Engage {', '.join(c[0] for c in candidates[:3])} with feedback-first posts.")
        sections.append(f"**Key Hook**: {summary}")
        sections.append("> [!TIP]\n> Use `reddit-post-engine` to generate subreddit-specific variants.")
        sections.append("")

    # Twitter/X
    sections.append(f"### [Twitter/X] - Fit: HIGH")
    sections.append(f"**Thread Strategy**: Start with the problem of {brief.get('problem_solved', 'the current niche')}.")
    sections.append(f"**Hook**: I built `{repo_name}` to solve {summary.lower()}.")
    sections.append("> [!TIP]\n> Use `tweet-thread-from-blog` or `linkedin-post-generator` to expand this hook.")
    
    return "\n".join(sections)


def render_readiness_fix_plan(brief: dict[str, Any]) -> str:
    """Render a checklist-style fix plan for unready repositories."""
    readiness_obj = brief.get("launch_readiness") or {}
    if not isinstance(readiness_obj, dict) or not readiness_obj.get("fix_plan"):
        return ""
    
    score = readiness_obj.get("score", "low").upper()
    sections = [
        "## Launch Readiness Fix Plan",
        f"The project is currently at **{score}** readiness. Resolve these issues before an aggressive public launch:",
        ""
    ]
    
    for item in readiness_obj["fix_plan"]:
        severity = f"({item['severity'].capitalize()} impact)"
        sections.append(f"- [ ] {item['suggested_fix']} {severity}")
        sections.append(f"  - **Why**: {item['reason']}")
        sections.append(f"  - **Likely file(s)**: {', '.join(f'`{f}`' for f in item['likely_files'])}")
        sections.append("")
        
    return "\n".join(sections)


def _generate_fitness_explanation(brief: dict[str, Any]) -> str:
    fitness = brief.get("channel_fitness") or {}
    type_ = brief.get("project_type") or "project"
    readiness_obj = brief.get("launch_readiness") or {}
    readiness_score = readiness_obj.get("score", "medium") if isinstance(readiness_obj, dict) else readiness_obj
    
    lines = [f"This is identified as a **{type_}** with **{readiness_score.capitalize()} Launch Readiness**."]
    
    if fitness.get("show_hn") == "high":
        lines.append("- **Show HN**: High fit. Technical communities appreciate technical tools and libraries.")
    elif fitness.get("show_hn") == "low":
        lines.append("- **Show HN**: Not recommended yet. Repository context might be too thin for Hacker News.")
        
    if fitness.get("product_hunt") == "high":
        lines.append("- **Product Hunt**: High fit. Polished apps and frameworks perform well here.")
    elif fitness.get("product_hunt") == "low":
        lines.append("- **Product Hunt**: Not recommended yet. Pure libraries or early-stage tools often struggle on PH without a UI/Demo.")

    if fitness.get("reddit") == "high":
        lines.append("- **Reddit**: High fit. Community-driven feedback is ideal for this project.")
    elif fitness.get("reddit") == "low" and readiness_score == "low":
        lines.append("- **Reddit**: OK for feedback only. Avoid a 'launch' post; ask for specific technical reviews instead.")
        
    return "\n".join(lines)


def generate_launch_strategy(brief: dict[str, Any]) -> dict[str, Any]:
    fitness = brief.get("channel_fitness") or {}
    readiness_obj = brief.get("launch_readiness") or {}
    readiness_score = readiness_obj.get("score", "medium") if isinstance(readiness_obj, dict) else readiness_obj
    
    # Simple recommendation logic
    recommended = [k for k, v in fitness.items() if v == "high"]
    if not recommended:
        recommended = [k for k, v in fitness.items() if v == "medium"]
    
    # Timeline coordination
    if readiness_score == "low":
        sequence = [
            "Phase 0: Readiness Fixes (Complete the checklist below)",
            "Day 1-3: Documentation Sprint (Fix README, add examples)",
            "Day 4+: Re-evaluate for Show HN/PH once fundamentals are robust"
        ]
    elif readiness_score == "medium":
        sequence = [
            "Phase 0: Polish Core Docs (Quickstart & Examples)",
            "Step 1: Soft Launch (Internal beta, small Discord niche, existing users)",
            "Step 2: Collect & Address initial feedback",
            "Step 3: Re-readiness check before Product Hunt"
        ]
    elif fitness.get("show_hn") == "high":
        sequence = ["Day 1: Show HN", "Day 3: Reddit", "Day 5: Product Hunt"]
    else:
        sequence = ["Day 1: Twitter/X Soft Launch", "Day 3: Reddit", "Day 7: Show HN (if feedback is good)"]

    return {
        "explanation": _generate_fitness_explanation(brief),
        "recommended_channels": recommended,
        "timeline": sequence
    }


def render_full_launch_kit_markdown(brief: dict[str, Any]) -> str:
    repo_name = _repo_slug(brief)
    strategy = generate_launch_strategy(brief)
    readiness_obj = brief.get("launch_readiness") or {}
    score = readiness_obj.get("score", "medium") if isinstance(readiness_obj, dict) else readiness_obj
    
    sections = [
        f"# Launch Orchestrator for {repo_name}",
        "",
        "## Executive Summary & Launch Readiness",
        f"**Project Maturity**: {score.upper()}",
    ]
    
    if score == "low":
        sections.append("\n> [!CAUTION]")
        sections.append("> **This project is not launch-ready yet.** Fix the fundamental issues in the readiness plan below before running a public launch.")
        sections.append("")
        sections.append(render_readiness_fix_plan(brief))
    elif score == "medium":
        sections.append("\n## Soft Launch Strategy")
        sections.append("- Start with existing community channels, small newsletter segments, or internal users.")
        sections.append("- Avoid high-friction 'loud' launches until the core documentation gaps below are filled.")
        sections.append("")
        sections.append(render_readiness_fix_plan(brief))
        sections.append("")
        sections.append("## Coordinated Launch Timeline")
        sections.append("\n".join(f"- [ ] {step}" for step in strategy["timeline"]))
        sections.append("")
        sections.append("## Suggested Skills (Post-Fix)")
        sections.append("> [!TIP]\n> Once fixes are complete, use `producthunt-launch-kit` for full asset generation.")
        sections.append("> [!TIP]\n> For a technical deep-dive once documentation is robust, use `show-hn-writer`.")
    else:
        # High readiness
        sections.append("")
        sections.append("## Coordinated Launch Timeline")
        sections.append("\n".join(f"- [ ] {step}" for step in strategy["timeline"]))
        sections.append("")
        sections.append(strategy["explanation"])
        sections.append("")
        sections.append(render_readiness_fix_plan(brief))
        sections.append("")
        sections.append(render_channel_strategy(brief))

    sections.extend([
        "",
        "## Full Confidence Notes & Assumptions",
        _render_low_confidence_note(brief),
    ])
    
    return "\n\n".join(sections).rstrip() + "\n"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python generate_assets.py <product-brief-json>")

    with open(sys.argv[1], "r", encoding="utf-8") as handle:
        brief = json.load(handle)

    print(render_full_launch_kit_markdown(brief))


if __name__ == "__main__":
    main()
