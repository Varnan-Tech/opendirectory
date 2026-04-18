"""
Fetches open issues from a GitHub repository via the REST API.
Skips Pull Requests. Gracefully handles rate limits and missing repos.
"""

import os
import requests
from typing import List, Dict, Any

def fetch_github_issues(
    repo_full_name: str, 
    labels: str = "bug,question", 
    limit: int = 100, 
    include_comments: bool = False,
    comment_limit_per_issue: int = 30
) -> List[Dict[str, Any]]:
    """
    Fetches open issues up to the specified limit using the GitHub REST API.
    
    Output Schema per issue:
    {
        "number": int,
        "title": str,
        "body": str,
        "labels": List[str],
        "state": str,
        "created_at": str,
        "updated_at": str,
        "url": str,
        "comments": List[str]  # Empty if include_comments is False
    }
    """
    token = os.environ.get("GITHUB_TOKEN")
    
    session = requests.Session()
    session.headers.update({
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "api-error-to-faq-builder/1.0.0"
    })
    
    if token:
        session.headers.update({"Authorization": f"token {token}"})
    
    url = f"https://api.github.com/repos/{repo_full_name}/issues"
    params = {
        "state": "open",
        "per_page": min(limit, 100)
    }
    
    # Parse labels for local OR filtering
    target_labels = [l.strip().lower() for l in labels.split(",") if l.strip()] if labels else []
    # Do NOT pass labels to params, since GitHub uses AND. We want OR logic locally.
    
    issues = []
    pages_fetched = 0
    MAX_PAGES = 10 # Prevent infinite crawling on massive repos if matching issues are rare
    
    while url and len(issues) < limit and pages_fetched < MAX_PAGES:
        pages_fetched += 1
        try:
            response = session.get(url, params=params, timeout=20)
        except requests.RequestException as e:
            raise RuntimeError(f"Network error while fetching issues from '{repo_full_name}': {e}")
            
        if response.status_code == 401:
            raise RuntimeError("HTTP 401: Invalid GITHUB_TOKEN. Please check your .env file.")
        elif response.status_code == 403:
            raise RuntimeError("HTTP 403: Rate limited or access denied. Try setting GITHUB_TOKEN if unauthenticated.")
        elif response.status_code == 404:
            raise RuntimeError(f"HTTP 404: Repository '{repo_full_name}' not found. Ensure it is public and spelled correctly.")
            
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise RuntimeError(f"Unexpected HTTP error fetching issues: {e}")
            
        page_data = response.json()
        if not page_data:
            break
            
        for item in page_data:
            # The GitHub Issues API mixes Pull Requests into the issues array. We must skip them.
            if "pull_request" in item:
                continue
                
            item_labels_raw = [label["name"] for label in item.get("labels", [])]
            item_labels_lower = [l.lower() for l in item_labels_raw]
            
            # Local OR filtering with substring match (e.g. 'bug' matches 'Type: Bug')
            if target_labels:
                match_found = any(
                    any(t_lbl in i_lbl for i_lbl in item_labels_lower)
                    for t_lbl in target_labels
                )
                if not match_found:
                    continue
                    
            issue_data = {
                "number": item["number"],
                "title": item["title"],
                "body": item["body"] or "",
                "labels": item_labels_raw,
                "state": item["state"],
                "created_at": item["created_at"],
                "updated_at": item["updated_at"],
                "url": item["html_url"],
                "comments": []
            }
            
            # Fetch issue comments (only first page, capped by comment_limit_per_issue)
            if include_comments and item["comments"] > 0:
                comments_url = item["comments_url"]
                try:
                    c_params = {"per_page": min(comment_limit_per_issue, 100)}
                    c_resp = session.get(comments_url, params=c_params, timeout=20)
                    if c_resp.status_code == 200:
                        issue_data["comments"] = [
                            c["body"] for c in c_resp.json() if c.get("body")
                        ][:comment_limit_per_issue]
                except requests.RequestException:
                    pass  # Fail gracefully on an individual comment fetch timeout
            
            issues.append(issue_data)
            
            if len(issues) >= limit:
                break
                
        # Handle pagination
        if "next" in response.links:
            url = response.links["next"]["url"]
            # After page 1, the 'next' URL from GitHub links natively includes all query params.
            # We set params=None here to avoid the underlying requests library duplicating them.
            params = None  
        else:
            url = None
            
    return issues
