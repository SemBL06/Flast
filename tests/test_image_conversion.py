import json
from pathlib import Path
import shutil
import tempfile
import unittest

from PIL import Image

from python.generator.images import convert_to_webp, rewrite_converted_image_sources
from python.generator.main import main as generate_site


class ImageConversionTests(unittest.TestCase):
    def test_jpeg_conversion_creates_webp(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "photo.jpg"
            destination = root / "photo.webp"
            Image.new("RGB", (2, 2), (10, 20, 30)).save(source, "JPEG")

            convert_to_webp(source, destination)

            with Image.open(destination) as image:
                self.assertEqual("RGB", image.mode)

    def test_png_conversion_preserves_transparency(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "transparent.png"
            destination = root / "transparent.webp"
            Image.new("RGBA", (2, 2), (10, 20, 30, 128)).save(source)

            convert_to_webp(source, destination)

            with Image.open(destination) as image:
                self.assertEqual("RGBA", image.mode)

    def test_rewrites_only_local_converted_image_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_page = root / "content" / "guides" / "page.md"
            output_page = root / "public" / "guides" / "page.html"
            source_image = root / "content" / "assets" / "photo.png"
            converted_image = root / "public" / "assets" / "photo.webp"
            source_page.parent.mkdir(parents=True)
            source_image.parent.mkdir(parents=True)
            source_page.write_text("Page", encoding="utf-8")
            source_image.write_bytes(b"image")

            html = (
                '<img src="../assets/photo.png?width=200#preview">'
                '<img src="https://example.com/photo.png">'
                '<img src="icon.svg">'
            )
            rewritten = rewrite_converted_image_sources(
                html,
                source_page,
                output_page,
                {source_image.resolve(): converted_image},
            )

            self.assertIn('src="../assets/photo.webp?width=200#preview"', rewritten)
            self.assertIn('src="https://example.com/photo.png"', rewritten)
            self.assertIn('src="icon.svg"', rewritten)

    def test_generator_emits_webp_and_updates_rendered_page(self):
        source_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(source_root / "layouts", root / "layouts")
            (root / "content" / "guides").mkdir(parents=True)
            (root / "python" / "configuration").mkdir(parents=True)
            image_path = root / "content" / "guides" / "photo.png"
            gif_path = root / "content" / "guides" / "animated.gif"
            svg_path = root / "content" / "guides" / "icon.svg"
            Image.new("RGB", (2, 2), (255, 0, 0)).save(image_path)
            Image.new("RGB", (2, 2), (0, 255, 0)).save(gif_path, "GIF")
            svg_path.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>', encoding="utf-8")
            (root / "content" / "guides" / "page.md").write_text(
                "---\ntitle: Image Guide\n---\n![Photo](photo.png)\n![GIF](animated.gif)\n![Vector](icon.svg)\n![Remote](https://example.com/photo.png)",
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

            self.assertTrue((root / "public" / "guides" / "photo.webp").exists())
            self.assertFalse((root / "public" / "guides" / "photo.png").exists())
            self.assertTrue((root / "public" / "guides" / "animated.gif").exists())
            self.assertTrue((root / "public" / "guides" / "icon.svg").exists())
            html = (root / "public" / "guides" / "page.html").read_text(encoding="utf-8")
            self.assertIn('src="photo.webp"', html)
            self.assertIn('src="animated.gif"', html)
            self.assertIn('src="icon.svg"', html)
            self.assertIn('src="https://example.com/photo.png"', html)

    def test_invalid_image_reports_source_path(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "invalid.png"
            source.write_text("not an image", encoding="utf-8")

            with self.assertRaisesRegex(RuntimeError, "invalid.png"):
                convert_to_webp(source, source.with_suffix(".webp"))


if __name__ == "__main__":
    unittest.main()
