"""Fetch GitHub repo context for oss-launch-kit.

This module resolves a public GitHub repo URL into structured context that
downstream stages can use without re-hitting GitHub.
"""

from __future__ import annotations

import base64
import os
import os
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

try:
    import requests
except ImportError as exc:
    # Use the class name directly since RepoContextError is defined below
    raise ValueError(
        "This skill requires the 'requests' library. Install it with: pip install requests"
    ) from exc

GITHUB_API_BASE = "https://api.github.com"
DEFAULT_TIMEOUT = 30


class RepoContextError(ValueError):
    """Raised when repo context cannot be fetched or validated."""


@dataclass(frozen=True)
class RepoRef:
    owner: str
    name: str


def _parse_repo_url(repo_url: str) -> RepoRef:
    parsed = urlparse(repo_url.strip())
    if parsed.scheme not in {"http", "https"}:
        raise RepoContextError("repo-url must start with http:// or https://")
    if parsed.netloc.lower() != "github.com":
        raise RepoContextError("repo-url must point to github.com")

    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        raise RepoContextError("repo-url must look like https://github.com/owner/repo")

    owner, name = parts[0], parts[1]
    if name.endswith(".git"):
        name = name[:-4]
    if not owner or not name:
        raise RepoContextError("repo-url is missing owner or repository name")

    return RepoRef(owner=owner, name=name)


def _headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "opendirectory-oss-launch-kit",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _request_json(url: str) -> requests.Response:
    return requests.get(url, headers=_headers(), timeout=DEFAULT_TIMEOUT)


def _raise_for_github_error(response: requests.Response, repo_url: str) -> None:
    if response.status_code == 401:
        raise RepoContextError("GitHub authentication failed. Check GITHUB_TOKEN.")
    if response.status_code == 403:
        remaining = response.headers.get("X-RateLimit-Remaining")
        if remaining == "0":
            raise RepoContextError("GitHub API rate limit exceeded. Set GITHUB_TOKEN and retry.")
        raise RepoContextError("GitHub access forbidden. The repo may be private or blocked.")
    if response.status_code == 404:
        raise RepoContextError(f"Repository not found or inaccessible: {repo_url}")
    raise RepoContextError(f"GitHub API error {response.status_code} for {repo_url}")


def _decode_readme(content: str, encoding: str | None) -> str:
    if not content:
        return ""
    if encoding == "base64":
        return base64.b64decode(content).decode("utf-8", errors="replace")
    return content


def _pick_readme_path(repo_ref: RepoRef) -> str | None:
    # GitHub's /readme endpoint already resolves the default README.
    return f"{GITHUB_API_BASE}/repos/{repo_ref.owner}/{repo_ref.name}/readme"


def fetch_repo_context(repo_url: str) -> dict[str, Any]:
    """Fetch structured GitHub repo context for the launch-kit pipeline.

    Returns a dict with repo metadata, README text, and a confidence flag.
    """

    repo_ref = _parse_repo_url(repo_url)
    repo_api_url = f"{GITHUB_API_BASE}/repos/{repo_ref.owner}/{repo_ref.name}"

    repo_response = _request_json(repo_api_url)
    if not repo_response.ok:
        _raise_for_github_error(repo_response, repo_url)
    repo = repo_response.json()

    readme_text = ""
    readme_url = _pick_readme_path(repo_ref)
    readme_error = None
    readme_response = _request_json(readme_url)
    if readme_response.status_code == 200:
        readme_payload = readme_response.json()
        readme_text = _decode_readme(readme_payload.get("content", ""), readme_payload.get("encoding"))
    elif readme_response.status_code == 404:
        readme_error = "README not found"
    else:
        readme_error = f"README fetch failed with status {readme_response.status_code}"
        if readme_response.status_code in {401, 403}:
            _raise_for_github_error(readme_response, repo_url)

    return {
        "repo_url": repo_url,
        "owner": repo.get("owner", {}).get("login"),
        "name": repo.get("name"),
        "full_name": repo.get("full_name"),
        "description": repo.get("description"),
        "homepage": repo.get("homepage"),
        "topics": repo.get("topics", []),
        "language": repo.get("language"),
        "license": (repo.get("license") or {}).get("spdx_id") or (repo.get("license") or {}).get("name"),
        "stars": repo.get("stargazers_count", 0),
        "forks": repo.get("forks_count", 0),
        "open_issues": repo.get("open_issues_count", 0),
        "created_at": repo.get("created_at"),
        "updated_at": repo.get("updated_at"),
        "archived": repo.get("archived", False),
        "fork": repo.get("fork", False),
        "default_branch": repo.get("default_branch"),
        "readme_text": readme_text,
        "readme_found": bool(readme_text),
        "readme_error": readme_error,
        "fetched_from": {
            "repo_api": repo_api_url,
            "readme_api": readme_url,
        },
        "confidence": "low" if not readme_text else "medium",
    }


def main() -> None:
    import json
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("Usage: python fetch_repo_context.py <github-repo-url>")

    context = fetch_repo_context(sys.argv[1])
    print(json.dumps(context, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
