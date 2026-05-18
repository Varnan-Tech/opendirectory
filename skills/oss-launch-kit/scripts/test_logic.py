import unittest
import sys
from pathlib import Path

# Add the scripts directory to sys.path
sys.path.append(str(Path(__file__).parent))

from build_product_brief import build_product_brief
from generate_assets import render_full_launch_kit_markdown

class TestOSSLaunchKitLogic(unittest.TestCase):
    def test_low_readiness_handling(self):
        # Mock repo context for a very weak repo
        low_context = {
            "name": "octocat/Hello-World",
            "description": "My first repository on GitHub!",
            "stars": 2,
            "readme_text": "Hello World!",
            "language": "HTML",
            "license": None,
            "confidence": "low"
        }
        
        brief = build_product_brief(low_context)
        self.assertEqual(brief["launch_readiness"]["score"], "low")
        self.assertTrue(len(brief["launch_readiness"]["fix_plan"]) > 0)
        
        markdown = render_full_launch_kit_markdown(brief)
        
        # Assertions for low readiness output
        self.assertIn("Project Maturity**: LOW", markdown)
        self.assertIn("> [!CAUTION]", markdown)
        self.assertIn("This project is not launch-ready yet", markdown)
        self.assertIn("## Launch Readiness Fix Plan", markdown)
        
        # High friction sections and full checklist should be absent
        self.assertNotIn("### [Show HN]", markdown)
        self.assertNotIn("### [Product Hunt]", markdown)
        self.assertNotIn("## Coordinated Launch Timeline", markdown)
        self.assertNotIn("## Channel Strategy & Positioning", markdown)

    def test_medium_readiness_handling(self):
        # Mock repo context for a medium tool
        medium_context = {
            "full_name": "user/medium-tool",
            "description": "A tool that does something useful",
            "stars": 25,
            "readme_text": "# Medium Tool\n\n## install\nnpm install medium-tool\n\n## usage\nmedium-tool --help\n\n## license\nMIT\n\n" + "Word " * 200, # > 1000 chars
            "language": "JavaScript",
            "license": "MIT",
            "confidence": "medium"
        }
        
        brief = build_product_brief(medium_context)
        self.assertEqual(brief["launch_readiness"]["score"], "medium")
        
        markdown = render_full_launch_kit_markdown(brief)
        
        # Assertions for medium readiness output
        self.assertIn("Project Maturity**: MEDIUM", markdown)
        self.assertIn("## Soft Launch Strategy", markdown)
        self.assertIn("## Launch Readiness Fix Plan", markdown)
        self.assertIn("## Coordinated Launch Timeline", markdown)
        self.assertIn("Step 1: Soft Launch", markdown)
        self.assertIn("## Suggested Skills (Post-Fix)", markdown)
        
        # Should still have handoffs but in the Post-Fix section
        self.assertIn("use `producthunt-launch-kit`", markdown)

    def test_high_readiness_handling(self):
        # Mock repo context for a strong tool
        high_context = {
            "full_name": "cli/cli",
            "description": "GitHub’s official command line tool helps developers solve github workflow issues",
            "stars": 35000,
            "readme_text": "# GitHub CLI\n\n## Quickstart\nbrew install gh\n\n## Usage\ngh issue list\n\n## License\nMIT\n\n## Contributing\nSee CONTRIBUTING.md\n\n## Demo\nVisit https://cli.github.com for a demo.\n\n" + "Long description about why this tool is amazing. " * 50,
            "language": "Go",
            "license": "MIT",
            "confidence": "high"
        }
        
        brief = build_product_brief(high_context)
        self.assertEqual(brief["launch_readiness"]["score"], "high")
        
        markdown = render_full_launch_kit_markdown(brief)
        
        # Assertions for high readiness output
        self.assertIn("Project Maturity**: HIGH", markdown)
        self.assertIn("## Coordinated Launch Timeline", markdown)
        self.assertIn("- [ ] Day 1: Show HN", markdown)
        self.assertIn("## Channel Strategy & Positioning", markdown)
        self.assertIn("### [Show HN] - Fit: HIGH", markdown)
        # cli/cli is a tool so PH is low, which is fine
        self.assertIn("### [Twitter/X]", markdown)
        self.assertNotIn("> [!CAUTION]", markdown)
        self.assertNotIn("## Soft Launch Strategy", markdown)

if __name__ == "__main__":
    unittest.main()
