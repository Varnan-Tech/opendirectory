"""CLI entrypoint for oss-launch-kit.

This orchestrates GitHub repo fetching, brief building, and full launch-kit generation.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from build_product_brief import build_product_brief
from fetch_repo_context import fetch_repo_context
from generate_assets import render_full_launch_kit_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a coordinated OSS launch strategy and readiness report from a GitHub repo.")
    parser.add_argument("--repo-url", required=True, help="Public GitHub repository URL")
    parser.add_argument("--output", default="launch-kit.md", help="Output Markdown file path")
    return parser


def run(repo_url: str) -> tuple[dict, dict, str]:
    repo_context = fetch_repo_context(repo_url)
    brief = build_product_brief(repo_context)
    markdown = render_full_launch_kit_markdown(brief)
    return repo_context, brief, markdown


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    _, _, markdown = run(args.repo_url)
    output_path = Path(args.output)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
