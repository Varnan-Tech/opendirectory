"""
CLI entry point for api-error-to-faq-builder.
Orchestrates fetching, normalizing, clustering, and Markdown generation.
"""

import argparse
import sys
import os

from dotenv import load_dotenv

# Ensure environment variables (like GITHUB_TOKEN) are loaded
load_dotenv()

from fetch_issues import fetch_github_issues
from build_faq import normalize_issue, cluster_issues, generate_faq_markdown

def main():
    parser = argparse.ArgumentParser(description="Build a troubleshooting FAQ from GitHub issues.")
    parser.add_argument("repo", help="Target repository as 'owner/repo' or full URL")
    parser.add_argument("--limit", type=int, default=100, help="Maximum number of issues to fetch")
    parser.add_argument("--labels", type=str, default="bug,question", help="Comma-separated labels to filter by (leave empty for all)")
    parser.add_argument("--comments", action="store_true", help="Include issue comments in signal extraction")
    parser.add_argument("--output", type=str, default="FAQ.md", help="Output file path")
    
    args = parser.parse_args()
    
    # Strip URL cleanly if a user pastes a full github.com/owner/repo URL
    repo = args.repo.replace("https://github.com/", "")\
                    .replace("http://github.com/", "")\
                    .replace("github.com/", "")\
                    .strip("/")
                    
    if "/" not in repo or len(repo.split("/")) != 2:
        print("[-] Error: Invalid repository format. Please provide 'owner/repo' or a valid GitHub URL.", file=sys.stderr)
        sys.exit(1)
        
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            print(f"[-] Error: Could not create output directory '{output_dir}': {e}", file=sys.stderr)
            sys.exit(1)
    
    print(f"[*] Fetching up to {args.limit} issues from '{repo}' (labels: '{args.labels}')...", file=sys.stderr)
    try:
        issues = fetch_github_issues(
            repo_full_name=repo,
            labels=args.labels,
            limit=args.limit,
            include_comments=args.comments
        )
    except RuntimeError as e:
        print(f"[-] Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    if not issues:
        print("[-] No open issues found matching the criteria. Exiting.", file=sys.stderr)
        sys.exit(0)
        
    print(f"[*] Fetched {len(issues)} issues. Normalizing text and extracting signals...", file=sys.stderr)
    normalized = []
    for issue in issues:
        normalized.append(normalize_issue(issue))
        
    print("[*] Grouping issues into clusters...", file=sys.stderr)
    clusters = cluster_issues(normalized)
    
    print(f"[*] Found {len(clusters)} valid clusters (singletons dropped). Generating Markdown...", file=sys.stderr)
    markdown_content = generate_faq_markdown(repo, clusters, len(issues))
    
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"[+] Success! FAQ written to {args.output}", file=sys.stderr)
        
        # Output summary stats for the user via stderr so stdout stays clean if piped
        if clusters:
            print(f"\nTop {min(3, len(clusters))} FAQ entries generated:", file=sys.stderr)
            for c in clusters[:3]:
                print(f"  - {c['title']} ({c['issue_count']} issues)", file=sys.stderr)
                
    except IOError as e:
        print(f"[-] Error writing to {args.output}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
