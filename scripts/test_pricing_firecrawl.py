"""Offline regression tests for Firecrawl research requests and examples."""

import importlib.util
import io
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "pricing_research", ROOT / "skills/pricing-finder/scripts/research.py"
)
research = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(research)
research.quiet = True


def response(markdown):
    return io.BytesIO(
        json.dumps({"success": True, "data": {"markdown": markdown}}).encode()
    )


class FirecrawlTests(unittest.TestCase):
    def test_v2_request_fetches_fresh_markdown(self):
        markdown = "# Pricing\nPro: $20/month\n" * 30
        with patch.object(
            research.urllib.request, "urlopen", return_value=response(markdown)
        ) as urlopen:
            result = research.fetch_firecrawl(
                "https://example.com/pricing", "test-key", timeout=12
            )

        self.assertEqual(result, (markdown, "ok"))
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "https://api.firecrawl.dev/v2/scrape")
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.get_header("Authorization"), "Bearer test-key")
        self.assertEqual(request.get_header("Content-type"), "application/json")
        self.assertEqual(
            json.loads(request.data),
            {
                "url": "https://example.com/pricing",
                "formats": ["markdown"],
                "onlyMainContent": True,
                "maxAge": 0,
            },
        )
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 12)

    def test_markdown_remains_limited_to_8000_characters(self):
        markdown = "€19/month\n" * 1000
        with patch.object(
            research.urllib.request, "urlopen", return_value=response(markdown)
        ):
            self.assertEqual(
                research.fetch_firecrawl("https://example.com", "test-key"),
                (markdown[:8000], "ok"),
            )

    def test_legacy_markdown_response_remains_supported(self):
        markdown = "# Pricing\nPro: $20/month\n"
        with patch.object(
            research.urllib.request,
            "urlopen",
            return_value=io.BytesIO(json.dumps({"markdown": markdown}).encode()),
        ):
            self.assertEqual(
                research.fetch_firecrawl("https://example.com", "test-key"),
                (markdown, "ok"),
            )

    def test_transport_errors_return_failure_without_retrying(self):
        for error in (
            HTTPError(
                "https://api.firecrawl.dev/v2/scrape", 401, "Unauthorized", {}, None
            ),
            HTTPError(
                "https://api.firecrawl.dev/v2/scrape", 429, "Rate limited", {}, None
            ),
            TimeoutError("request timed out"),
        ):
            with self.subTest(error=str(error)):
                with patch.object(
                    research.urllib.request, "urlopen", side_effect=error
                ) as urlopen:
                    content, status = research.fetch_firecrawl(
                        "https://example.com", "test-key"
                    )
                self.assertEqual(content, "")
                self.assertNotEqual(status, "ok")
                urlopen.assert_called_once()

    def test_invalid_json_returns_failure(self):
        with patch.object(
            research.urllib.request, "urlopen", return_value=io.BytesIO(b"not json")
        ):
            content, status = research.fetch_firecrawl("https://example.com", "test-key")
        self.assertEqual(content, "")
        self.assertNotEqual(status, "ok")

    def test_pricing_uses_v2_markdown_before_free_fallback(self):
        markdown = "# Pricing\nPro: $20/month\n" * 30
        with patch.object(
            research.urllib.request, "urlopen", return_value=response(markdown)
        ), patch.object(research, "fetch_url_bs4") as free_fetch:
            result = research.fetch_pricing_page(
                {"name": "Example", "pricing_url": "https://example.com/pricing"},
                firecrawl_key="test-key",
            )
        self.assertEqual(result["content"], markdown)
        self.assertEqual(result["source"], "firecrawl")
        self.assertEqual(result["data_quality"], "high")
        free_fetch.assert_not_called()

    def test_unusable_responses_keep_free_fallback_working(self):
        for body in (
            {"success": False, "error": "Scrape failed"},
            {"success": True, "data": {"markdown": ""}},
            {"success": True, "data": {"markdown": "short"}},
            {"success": True, "data": None},
        ):
            with self.subTest(body=body):
                with patch.object(
                    research.urllib.request,
                    "urlopen",
                    return_value=io.BytesIO(json.dumps(body).encode()),
                ), patch.object(
                    research, "fetch_url_bs4", return_value=("pricing " * 100, "ok")
                ) as free_fetch:
                    result = research.fetch_pricing_page(
                        {"pricing_url": "https://example.com/pricing"},
                        firecrawl_key="test-key",
                    )
                self.assertEqual(result["source"], "requests")
                free_fetch.assert_called_once_with("https://example.com/pricing")

    def test_no_key_skips_firecrawl(self):
        with patch.object(research.urllib.request, "urlopen") as urlopen, patch.object(
            research, "fetch_url_bs4", return_value=("pricing " * 100, "ok")
        ):
            result = research.fetch_pricing_page(
                {"pricing_url": "https://example.com/pricing"}
            )
        self.assertEqual(result["source"], "requests")
        urlopen.assert_not_called()


class FirecrawlExampleTests(unittest.TestCase):
    def test_skill_examples_request_fresh_v2_markdown(self):
        markdown = "# Example product\nPlans start at $20/month.\n"
        for skill in ("pricing-finder", "vc-finder", "competitor-pr-finder"):
            with self.subTest(skill=skill), tempfile.TemporaryDirectory() as tmp:
                directory = Path(tmp)
                document = (ROOT / "skills" / skill / "SKILL.md").read_text()
                block = next(
                    block
                    for block in re.findall(r"```bash\n(.*?)```", document, re.S)
                    if "api.firecrawl.dev" in block
                )
                # Run the published shell pipeline with a local curl substitute.
                curl = directory / "curl"
                curl.write_text(
                    "#!/usr/bin/env python3\n"
                    "import json, sys\n"
                    "from pathlib import Path\n"
                    "Path('request.json').write_text(json.dumps(sys.argv[1:]))\n"
                    f"print({json.dumps({'success': True, 'data': {'markdown': markdown}})!r})\n"
                )
                curl.chmod(0o755)
                output_match = re.search(r"open\('(/tmp/[^']+)'", block)
                self.assertIsNotNone(output_match)
                output = directory / "product.md"
                block = block.replace(output_match.group(1), str(output))
                env = {
                    **os.environ,
                    "PATH": f"{directory}{os.pathsep}{os.environ['PATH']}",
                }
                env["FIRECRAWL_API_KEY"] = "test-key"
                result = subprocess.run(
                    ["bash", "-o", "pipefail", "-c", block],
                    cwd=directory,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(output.read_text(), markdown)
                args = json.loads((directory / "request.json").read_text())
                self.assertIn("https://api.firecrawl.dev/v2/scrape", args)
                self.assertEqual(args[args.index("-X") + 1], "POST")
                self.assertIn("Authorization: Bearer test-key", args)
                self.assertIn("Content-Type: application/json", args)
                payload = json.loads(args[args.index("-d") + 1])
                self.assertEqual(payload["formats"], ["markdown"])
                self.assertTrue(payload["onlyMainContent"])
                self.assertEqual(payload["maxAge"], 0)


if __name__ == "__main__":
    unittest.main()
