import json
from pathlib import Path
import shutil
import tempfile
import unittest

from python.generator.main import main as generate_site
from python.generator.socials import links


class SocialLinkTests(unittest.TestCase):
    def test_normalizes_email_platforms_and_generic_links(self):
        result = links(
            {
                "core": {
                    "contact_email": "hello@example.com",
                    "socials": [
                        "https://instagram.com/example/",
                        "https://github.com/example/",
                        "https://mastodon.social/@example",
                        "https://example.org/profile",
                    ],
                }
            }
        )

        self.assertEqual("mailto:hello@example.com", result[0]["href"])
        self.assertEqual("email", result[0]["icon"])
        self.assertFalse(result[0]["external"])
        self.assertEqual(["instagram", "github", "mastodon", "link"], [item["icon"] for item in result[1:]])
        self.assertTrue(all(item["external"] for item in result[1:]))

    def test_invalid_links_and_empty_configuration_are_omitted(self):
        self.assertEqual([], links({"core": {"contact_email": "", "socials": []}}))
        self.assertEqual(
            [],
            links(
                {
                    "core": {
                        "contact_email": "invalid address",
                        "socials": ["javascript:alert(1)", "mailto:hello@example.com", "not-a-url"],
                    }
                }
            ),
        )

    def test_generated_sidebar_renders_only_valid_social_links(self):
        source_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(source_root / "layouts", root / "layouts")
            (root / "content").mkdir()
            (root / "python" / "configuration").mkdir(parents=True)
            (root / "content" / "index.md").write_text("---\ntitle: Home\n---\nWelcome", encoding="utf-8")
            (root / "python" / "configuration" / "configuration.json").write_text(
                json.dumps(
                    {
                        "core": {
                            "site_title": "Example",
                            "urls": {"self": "https://example.com/"},
                            "contact_email": "hello@example.com",
                            "socials": ["https://github.com/example/", "javascript:alert(1)"],
                        },
                        "layout": "default",
                    }
                ),
                encoding="utf-8",
            )

            generate_site(root)

            html = (root / "public" / "index.html").read_text(encoding="utf-8")
            self.assertIn('class="sidebar-socials"', html)
            self.assertIn('href="mailto:hello@example.com"', html)
            self.assertIn('href="https://github.com/example/"', html)
            self.assertIn('target="_blank" rel="noopener noreferrer"', html)
            self.assertNotIn("javascript:alert", html)

            configuration = json.loads((root / "python" / "configuration" / "configuration.json").read_text(encoding="utf-8"))
            configuration["core"]["contact_email"] = ""
            configuration["core"]["socials"] = []
            (root / "python" / "configuration" / "configuration.json").write_text(
                json.dumps(configuration), encoding="utf-8"
            )
            generate_site(root)

            empty_html = (root / "public" / "index.html").read_text(encoding="utf-8")
            self.assertNotIn('class="sidebar-socials"', empty_html)


if __name__ == "__main__":
    unittest.main()
