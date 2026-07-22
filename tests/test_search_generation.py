import json
from pathlib import Path
import shutil
import tempfile
import unittest

from python.generator.main import copy_layout_assets, main as generate_site
from python.generator.search import create_index


class SearchGenerationTests(unittest.TestCase):
    def test_index_contains_nested_page_title_url_and_plain_text(self):
        with tempfile.TemporaryDirectory() as directory:
            public = Path(directory) / "public"
            output_file = public / "guides" / "install.html"
            output_file.parent.mkdir(parents=True)

            create_index(
                [
                    {
                        "title": "Install Guide",
                        "output_file": output_file,
                        "body": "<h1>Install</h1><p>Use the <strong>package manager</strong>.</p>",
                    }
                ],
                public,
            )

            index = json.loads((public / "search-index.json").read_text(encoding="utf-8"))
            self.assertEqual(
                [{
                    "title": "Install Guide",
                    "url": "guides/install.html",
                    "content": "Install Use the package manager .",
                }],
                index,
            )

    def test_layout_assets_copy_css_and_javascript(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            layout = root / "layouts" / "default"
            (layout / "css").mkdir(parents=True)
            (layout / "js").mkdir()
            (layout / "css" / "theme.css").write_text("body {}", encoding="utf-8")
            (layout / "js" / "main.js").write_text("console.log('search');", encoding="utf-8")
            public = root / "public"

            copy_layout_assets(root, "default", public)

            self.assertTrue((public / "css" / "theme.css").exists())
            self.assertTrue((public / "js" / "main.js").exists())

    def test_generator_writes_index_copies_javascript_and_uses_relative_index_path(self):
        source_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(source_root / "layouts", root / "layouts")
            (root / "content" / "guides").mkdir(parents=True)
            (root / "python" / "configuration").mkdir(parents=True)
            (root / "content" / "guides" / "install.md").write_text(
                "---\ntitle: Install Guide\n---\nInstall with the package manager.",
                encoding="utf-8",
            )
            (root / "python" / "configuration" / "configuration.json").write_text(
                json.dumps(
                    {
                        "core": {"site_title": "Example", "urls": {"self": "https://example.com/"}},
                        "layout": "default",
                    }
                ),
                encoding="utf-8",
            )

            generate_site(root)

            self.assertTrue((root / "public" / "js" / "main.js").exists())
            self.assertTrue((root / "public" / "search-index.json").exists())
            html = (root / "public" / "guides" / "install.html").read_text(encoding="utf-8")
            self.assertIn('data-search-index="../search-index.json"', html)
            self.assertIn('class="article-metadata"', html)
            self.assertIn("1 min read", html)

    def test_default_layout_contains_accessible_search_controls(self):
        root = Path(__file__).resolve().parents[1]
        template = (root / "layouts" / "default" / "html" / "doc.html").read_text(encoding="utf-8")
        script = (root / "layouts" / "default" / "js" / "main.js").read_text(encoding="utf-8")
        stylesheet = (root / "layouts" / "default" / "css" / "documentation.css").read_text(encoding="utf-8")

        self.assertEqual(2, template.count("search-trigger"))
        self.assertIn('role="dialog"', template)
        self.assertIn('aria-modal="true"', template)
        self.assertIn("data-search-index", template)
        self.assertIn(".search-overlay[hidden]", stylesheet)
        self.assertIn(".code-copy-button", stylesheet)
        self.assertIn(".article-content .codehilite", stylesheet)
        self.assertNotIn("theme-toggle", template)
        self.assertNotIn("localStorage", script)
        self.assertIn("initializeCodeCopyButtons", script)
        self.assertIn("navigator.clipboard", script)


if __name__ == "__main__":
    unittest.main()
