"""
Normalizes issues, clusters them, and renders a structured Markdown FAQ.
"""

import re
import copy
from collections import defaultdict
from typing import List, Dict, Any

from thefuzz import fuzz

# Pre-defined guidance providing cautious but useful hypotheses
CATEGORY_GUIDANCE = {
    "Rate Limiting": {
        "cause": "This is often caused by exceeding the allowable burst or sustained request volume for the targeted API key or IP address.",
        "workaround": "Likely resolved by implementing exponential backoff, reducing active concurrency, or checking workspace usage limits."
    },
    "Authentication": {
        "cause": "This issue commonly occurs due to missing, expired, or improperly formatted API keys.",
        "workaround": "Check that the API token is passed correctly in headers and ensure it hasn't been revoked."
    },
    "Validation": {
        "cause": "This typically indicates missing required fields, improper data types, or an invalid JSON payload schema.",
        "workaround": "Review the request payload carefully and ensure all required parameters securely match the official documentation."
    },
    "Timeout": {
        "cause": "Often results from heavy backend processing, localized network latency, or slow queries on the provider's side.",
        "workaround": "Consider increasing client request timeouts, sending smaller batches, or checking the platform's system status pages."
    },
    "Not Found": {
        "cause": "Commonly occurs if the endpoint URL is misspelled, a resource ID does not exist, or the wrong environment/version path is targeted.",
        "workaround": "Verify the endpoint path, ensure any requested resource IDs are valid within your scopes, and confirm the correct base URL."
    }
}

def extract_code_blocks(text: str) -> List[str]:
    """Extract code chunks from both fenced blocks and inline backticks."""
    blocks = re.findall(r"```[a-zA-Z]*\n(.*?)```", text, re.DOTALL)
    inlines = re.findall(r"`([^`\n]+)`", text)
    return blocks + inlines

def escape_markdown_text(text: str) -> str:
    replacements = {
        "\\": "\\\\",
        "`": "\\`",
        "*": "\\*",
        "_": "\\_",
        "[": "\\[",
        "]": "\\]",
        "(": "\\(",
        ")": "\\)",
        "#": "\\#",
        "!": "\\!"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def get_text_basis(issue: Dict[str, Any]) -> str:
    """Concatenates title, body, and comments for signal extraction."""
    parts = [issue.get("title", ""), issue.get("body", "")]
    parts.extend(issue.get("comments", []))
    return " ".join(part for part in parts if part).lower()

def normalize_issue(issue: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts error signals without mutating the original issue.
    Returns: Enriched issue dict with 'signals' key.
    """
    enriched = copy.deepcopy(issue)
    text = get_text_basis(issue)
    
    # Also extract raw code separately so we can keep original casing
    raw_text = [issue.get("title", ""), issue.get("body", "")] + issue.get("comments", [])
    raw_joined = " ".join(part for part in raw_text if part)
    code_snippets = extract_code_blocks(raw_joined)
    
    signals = {
        "status_codes": [],
        "endpoints": [],
        "errors": [],
        "categories": []
    }
    
    status_pattern = r"\b(400|401|403|404|409|422|429|500|502|503|504)\b"
    status_matches = re.findall(status_pattern, text)
    signals["status_codes"] = list(dict.fromkeys(status_matches))
    
    # Endpoint extraction with cleanup
    endpoint_matches = re.findall(r"(/(?:v\d+|api)/[\w/\-{}]+)", text)
    cleaned_endpoints = [e.rstrip('.,;:"\'()?!') for e in endpoint_matches]
    signals["endpoints"] = list(dict.fromkeys(cleaned_endpoints))
    
    # Error extraction from code snippets
    error_keywords = ["error", "exception", "failed", "invalid", "not found", "unauthorized", "timeout", "bad request"]
    for snippet in code_snippets:
        snippet_lower = snippet.lower().strip()
        # Ensure snippet is short enough to be an error message and contains keywords
        if len(snippet) < 150 and any(k in snippet_lower for k in error_keywords):
            signals["errors"].append(snippet.strip()[:100])
            
    # Categories
    if any(k in text for k in ["rate limit", "too many requests", "429"]):
        signals["categories"].append("Rate Limiting")
    if any(k in text for k in ["unauthorized", "api key", "api token", "auth token", "forbidden", "auth "]):
        signals["categories"].append("Authentication")
    if any(k in text for k in ["validation", "invalid param", "bad request"]):
        signals["categories"].append("Validation")
    if any(k in text for k in ["timeout", "timed out", "socket closed", "hang"]):
        signals["categories"].append("Timeout")
    if any(k in text for k in ["not found", "404", "no route", "endpoint not found"]):
        signals["categories"].append("Not Found")
        
    enriched["signals"] = signals
    return enriched


def generate_cluster_title(signals: Dict[str, Any]) -> str:
    """Generates a clean, user-friendly FAQ question based on signals."""
    eps = signals.get("endpoints")
    codes = signals.get("status_codes")
    cats = signals.get("categories")
    
    if eps and codes:
        return f"Why am I getting {codes[0]} errors on `{eps[0]}`?"
    if eps and cats:
        return f"Why do requests to `{eps[0]}` fail with {cats[0].lower()} issues?"
    if codes:
        return f"Why do requests frequently fail with a {codes[0]} status code?"
    if cats:
        return f"How can I resolve recurring {cats[0].lower()} errors?"
    if signals.get("errors"):
        return f"Why am I seeing the error: `{signals['errors'][0]}`?"
        
    return "Why are requests failing with unclear API errors?"


def get_cluster_key(signals: Dict[str, Any]) -> str:
    """Determines the primary deterministic key for clustering."""
    if signals.get("endpoints") and signals.get("status_codes"):
        return f"endpoint:{signals['endpoints'][0]}|status:{signals['status_codes'][0]}"
    if signals.get("endpoints") and signals.get("categories"):
        return f"endpoint:{signals['endpoints'][0]}|category:{signals['categories'][0]}"
    if signals.get("endpoints"):
        return f"endpoint:{signals['endpoints'][0]}"
    if signals.get("errors"):
        return f"error:{signals['errors'][0]}"
    if signals.get("categories"):
        return f"category:{signals['categories'][0]}"
    return ""


def cluster_issues(issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Groups issues contextually and calculates confidence scores."""
    clusters_dict = defaultdict(list)
    unassigned = []
    
    for issue in issues:
        key = get_cluster_key(issue.get("signals", {}))
        if key:
            clusters_dict[key].append(issue)
        else:
            unassigned.append(issue)
            
    # Advanced fuzzing against representative titles and top issue titles
    for issue in unassigned:
        best_match_key = None
        highest_score = 0
        issue_title = issue.get("title", "")
        
        for key, cluster_issues_list in clusters_dict.items():
            rep_title = generate_cluster_title(cluster_issues_list[0].get("signals", {}))
            base_score = fuzz.token_set_ratio(issue_title, rep_title)
            
            # Check against existing issues in cluster to broaden fuzzy scope
            for c_issue in cluster_issues_list[:3]:
                score = fuzz.token_set_ratio(issue_title, c_issue.get("title", ""))
                base_score = max(base_score, score)
                
            if base_score >= 80 and base_score > highest_score:
                highest_score = base_score
                best_match_key = key
                
        if best_match_key:
            clusters_dict[best_match_key].append(issue)
        else:
            clusters_dict[f"fuzzy:{issue.get('number')}"] = [issue]
            
    final_clusters = []
    for key, cl_issues in clusters_dict.items():
        if len(cl_issues) < 2:
            continue  # maintain singleton exclusion
            
        base_signals = cl_issues[0].get("signals", {})
        title = generate_cluster_title(base_signals)
        
        # Calculate cluster confidence score
        size_score = min(0.5, len(cl_issues) * 0.1) # Max 0.5 for size 5+
        signal_score = 0.5 if ("endpoint" in key and "status" in key) else (0.3 if "endpoint" in key else 0.1)
        confidence = round(min(size_score + signal_score, 1.0), 2)
        
        final_clusters.append({
            "key": key,
            "title": title,
            "issues": cl_issues,
            "issue_count": len(cl_issues),
            "signals": base_signals,
            "confidence": confidence
        })
        
    final_clusters.sort(key=lambda x: (x["issue_count"], x["confidence"]), reverse=True)
    return final_clusters


def generate_faq_markdown(repo_full_name: str, clusters: List[Dict[str, Any]], total_scanned: int) -> str:
    """Renders high-confidence clusters into a standard Markdown FAQ."""
    lines = []
    lines.append(f"# Troubleshooting FAQ: `{repo_full_name}`")
    lines.append(f"> Auto-generated from {total_scanned} open issues.\n")
    
    if not clusters:
        lines.append("No recurring API errors or meaningful groupings were found.")
        return "\n".join(lines)
        
    for cluster in clusters:
        lines.append(f"## {cluster['title']}\n")
        
        categories = cluster["signals"].get("categories", [])
        cat = categories[0] if categories else None
        # Resolve sensible contextual guidance
        guidance = CATEGORY_GUIDANCE.get(cat, {
            "cause": "Multiple users reported this behavior. It is frequently caused by invalid parameters or temporary disruptions.",
            "workaround": "Check the related issues below for confirmed maintainer guidance."
        })
        
        lines.append("**Common symptoms**")
        lines.append(f"- Consistent errors matching cluster signature: `{cluster['key']}`")
        if cluster["signals"].get("status_codes"):
            lines.append(f"- API typically responds with HTTP `{cluster['signals']['status_codes'][0]}`")
        lines.append("")
        
        lines.append("**Likely cause**")
        lines.append(f"- {guidance['cause']}\n")
        
        lines.append("**Suggested workaround**")
        lines.append(f"- {guidance['workaround']}\n")
        
        lines.append(f"**Cluster Confidence Score:** {cluster['confidence']}/1.0")
        lines.append(f"\n**Related issues ({cluster['issue_count']})**")
        for issue in cluster['issues']:
            title = escape_markdown_text(issue['title'])
            lines.append(f"- [#{issue['number']}]({issue['url']}) - {title}")
        lines.append("\n---\n")
        
    return "\n".join(lines)
