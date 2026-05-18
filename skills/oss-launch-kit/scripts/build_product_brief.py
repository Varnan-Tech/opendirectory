"""Build a grounded product brief from GitHub repo context.

This is a deterministic Stage A transformer: it extracts factual signals from
repo metadata and README text, then assembles a concise launch brief that the
asset generator can safely use.
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


def _first_sentence(text: str) -> str:
    cleaned = _strip_markdown(text)
    if not cleaned:
        return ""
    match = re.search(r"^(.+?[.!?])(\s|$)", cleaned)
    return match.group(1).strip() if match else cleaned


def _readme_paragraphs(readme_text: str) -> list[str]:
    blocks = [block.strip() for block in re.split(r"\n\s*\n", readme_text or "")]
    return [block for block in blocks if block]


def _readme_bullets(readme_text: str) -> list[str]:
    bullets = []
    for line in (readme_text or "").splitlines():
        if re.match(r"^\s*[-*+]\s+", line):
            bullets.append(_strip_markdown(re.sub(r"^\s*[-*+]\s+", "", line)))
    return bullets


def _infer_audience(repo_context: dict[str, Any], readme_text: str) -> tuple[str, str]:
    text = f"{repo_context.get('description') or ''}\n{readme_text}".lower()
    candidates = [
        ("developers", ["developer", "developers", "devs", "engineers", "coding"]),
        ("teams", ["team", "teams", "workspace", "collaboration"]),
        ("authors and maintainers", ["maintainer", "maintainers", "author", "open source"]),
        ("data/infra users", ["api", "cli", "server", "deploy", "infra", "pipeline"]),
        ("end users", ["app", "users", "personal", "workflow"]),
    ]
    for label, keywords in candidates:
        if any(keyword in text for keyword in keywords):
            return label, "medium"
    return "unknown", "low"


def _infer_project_type(repo_context: dict[str, Any], readme_text: str) -> str:
    text = f"{repo_context.get('description') or ''}\n{readme_text}".lower()
    if any(term in text for term in ["framework", "platform"]):
        return "framework"
    if any(term in text for term in ["library", "package", "module", "sdk"]):
        return "library"
    if any(term in text for term in ["cli", "tool", "automation", "workflow"]):
        return "tool"
    if any(term in text for term in ["app", "saas", "dashboard", "interface"]):
        return "app"
    if any(term in text for term in ["template", "boilerplate", "starter"]):
        return "template"
    return "project"


def _evaluate_channel_fitness(project_type: str, readiness: str) -> dict[str, str]:
    """Evaluate fitness for launch channels based on project type and readiness."""
    fitness = {
        "show_hn": "medium",
        "product_hunt": "medium",
        "reddit": "medium",
        "twitter_x": "high",
    }

    # Weak repo / Unready project logic
    if readiness == "low":
        return {
            "show_hn": "low",
            "product_hunt": "low",
            "reddit": "low",
            "twitter_x": "medium"
        }

    # Project type nuances for ready projects
    if project_type in ["library", "tool", "framework"]:
        fitness["product_hunt"] = "low"
        fitness["show_hn"] = "high"
    elif project_type == "app":
        fitness["product_hunt"] = "high"
        fitness["show_hn"] = "medium"
    elif project_type == "template":
        fitness["show_hn"] = "low"
        fitness["product_hunt"] = "low"
        fitness["reddit"] = "high"

    return fitness


def _infer_problem(repo_context: dict[str, Any], readme_text: str) -> tuple[str, str]:
    description = _strip_markdown(repo_context.get("description"))
    if description:
        return description, "medium"

    paras = _readme_paragraphs(readme_text)
    if paras:
        return _first_sentence(paras[0]), "low"

    return "Unknown from available repo metadata.", "low"


def _infer_value_prop(problem: str, key_features: list[str]) -> str:
    if key_features:
        first = key_features[0]
        return f"Solves {problem.lower()} with {first.lower()}."
    return f"Grounds launch copy in the repository's own README and metadata around {problem.lower()}."


def _extract_key_features(readme_text: str, repo_context: dict[str, Any]) -> list[str]:
    bullets = _readme_bullets(readme_text)
    features: list[str] = []
    for bullet in bullets:
        if len(features) >= 5:
            break
        if len(bullet) < 3:
            continue
        features.append(bullet)

    if not features:
        description = _strip_markdown(repo_context.get("description"))
        if description:
            features.append(description)

    return features[:5]


def _build_links(repo_context: dict[str, Any]) -> dict[str, str | None]:
    return {
        "repo": repo_context.get("repo_url"),
        "homepage": repo_context.get("homepage") or None,
        "readme_source": repo_context.get("fetched_from", {}).get("readme_api"),
    }


def _check_readiness_signals(readme_text: str, repo_context: dict[str, Any]) -> dict[str, bool]:
    text = readme_text.lower()
    desc = _clean(repo_context.get("description")).lower()
    return {
        "has_license": bool(repo_context.get("license")),
        "has_install": any(term in text for term in ["# install", "npm install", "pip install", "pip3 install", "go get", "setup", "quickstart"]),
        "has_usage_example": any(term in text for term in ["example", "usage", "how to use", "code snippet"]),
        "has_contributing": any(term in text for term in ["contributing", "pull request", "license path", "issue tracker"]),
        "has_quickstart": any(term in text for term in ["# quickstart", "tl;dr", "getting started", "one-command", "fast start"]),
        "has_clear_positioning": len(desc) > 30 and any(term in desc for term in ["built for", "helps", "allows", "solves", "for devs", "for users"]),
        "has_demo_or_proof": any(term in text for term in ["demo", "screenshot", "gif", "preview", "live link", "http", "view it"]),
        "has_description": len(desc) > 20,
    }


def _generate_fix_plan(signals: dict[str, bool]) -> list[dict[str, Any]]:
    """Generate a prioritized list of fixes for the repository."""
    plan = []
    
    if not signals["has_quickstart"]:
        plan.append({
            "id": "add_quickstart_example",
            "severity": "high",
            "reason": "New users need a copy-paste example to reach 'first success' quickly.",
            "suggested_fix": "Add a 'Quickstart' section at the top of README with a single command or minimal code snippet.",
            "likely_files": ["README.md"]
        })

    if not signals["has_usage_example"]:
        plan.append({
            "id": "add_usage_example",
            "severity": "high",
            "reason": "Without a concrete usage example, users cannot see how to apply the project.",
            "suggested_fix": "Add a minimal 'Usage' section with one realistic example and expected output.",
            "likely_files": ["README.md", "docs/usage.md"]
        })

    if not signals["has_clear_positioning"]:
        plan.append({
            "id": "improve_positioning",
            "severity": "high",
            "reason": "The project description is too short or lacks clear target audience context.",
            "suggested_fix": "Update the repository description to clearly state 'Who it is for' and 'What problem it solves'.",
            "likely_files": ["GitHub Metadata", "README.md"]
        })

    if not signals["has_demo_or_proof"]:
        plan.append({
            "id": "add_demo_or_proof",
            "severity": "medium",
            "reason": "Visual proof or live demos significantly increase conversion and trust.",
            "suggested_fix": "Add a screenshot, GIF, or a link to a live demo/sample output in the README.",
            "likely_files": ["README.md"]
        })

    if not signals["has_license"]:
        plan.append({
            "id": "add_license",
            "severity": "medium",
            "reason": "OSS users need a clear license to feel safe adopting the code.",
            "suggested_fix": "Add an MIT or Apache-2.0 LICENSE file to the repository root.",
            "likely_files": ["LICENSE"]
        })

    if not signals["has_contributing"]:
        plan.append({
            "id": "add_contribution_guide",
            "severity": "low",
            "reason": "Contributors need clear expectations for how to propose changes.",
            "suggested_fix": "Create a CONTRIBUTING.md with basic rules (how to open PRs, coding style, etc.).",
            "likely_files": ["CONTRIBUTING.md"]
        })

    return plan


def build_product_brief(repo_context: dict[str, Any]) -> dict[str, Any]:
    """Convert fetched repo context into a grounded launch brief."""

    readme_text = repo_context.get("readme_text") or ""
    repo_name = repo_context.get("full_name") or repo_context.get("name") or "unknown-repo"

    problem, problem_confidence = _infer_problem(repo_context, readme_text)
    audience, audience_confidence = _infer_audience(repo_context, readme_text)
    key_features = _extract_key_features(readme_text, repo_context)
    value_prop = _infer_value_prop(problem, key_features)

    summary = _clean(repo_context.get("description"))
    if not summary:
        summary = _first_sentence(readme_text) or f"Open-source project in {repo_context.get('language') or 'unknown language'}."

    readiness_signals = _check_readiness_signals(readme_text, repo_context)
    signal_count = sum(1 for v in readiness_signals.values() if v)

    assumptions: list[str] = []
    if repo_context.get("readme_error"):
        assumptions.append(f"README issue: {repo_context['readme_error']}")
    if audience == "unknown":
        assumptions.append("Audience inferred from repo metadata only.")
    if not key_features:
        assumptions.append("No strong feature bullets extracted from README.")
    if not readiness_signals["has_install"]:
        assumptions.append("No clear installation instructions found in README.")

    confidence = "high"
    if repo_context.get("confidence") == "low" or audience_confidence == "low" or problem_confidence == "low":
        confidence = "low"
    elif assumptions:
        confidence = "medium"

    proof_points = []
    if repo_context.get("stars") is not None:
        proof_points.append(f"{repo_context['stars']} GitHub stars")
    if repo_context.get("forks") is not None:
        proof_points.append(f"{repo_context['forks']} forks")
    if repo_context.get("topics"):
        proof_points.append("topics: " + ", ".join(repo_context.get("topics", [])[:5]))
    if repo_context.get("language"):
        proof_points.append(f"primary language: {repo_context['language']}")
    if repo_context.get("license"):
        proof_points.append(f"license: {repo_context['license']}")

    project_type = _infer_project_type(repo_context, readme_text)
    
    # Launch Readiness assessment
    stars = repo_context.get("stars", 0)
    readme_len = len(readme_text)
    
    # Heuristic scoring
    if stars >= 50 and readme_len > 1500 and signal_count >= 5:
        score = "high"
    elif stars < 10 or readme_len < 500 or signal_count <= 2:
        score = "low"
    else:
        score = "medium"

    readiness = {
        "score": score,
        "signals": readiness_signals,
        "fix_plan": _generate_fix_plan(readiness_signals)
    }

    channel_fitness = _evaluate_channel_fitness(project_type, score)

    return {
        "repo_name": repo_name,
        "one_line_summary": summary,
        "project_type": project_type,
        "launch_readiness": readiness,
        "audience": audience,
        "problem_solved": problem,
        "value_proposition": value_prop,
        "key_proof_points": proof_points,
        "key_features": key_features,
        "links": _build_links(repo_context),
        "confidence": confidence,
        "assumptions": assumptions,
        "channel_fitness": channel_fitness,
        "source_confidence": {
            "problem": problem_confidence,
            "audience": audience_confidence,
            "repo_context": repo_context.get("confidence", "low"),
        },
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python build_product_brief.py <repo-context-json>")

    with open(sys.argv[1], "r", encoding="utf-8") as handle:
        repo_context = json.load(handle)

    brief = build_product_brief(repo_context)
    print(json.dumps(brief, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
