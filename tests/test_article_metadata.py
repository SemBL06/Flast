from datetime import datetime
from pathlib import Path
import os
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from python.generator.metadata import last_updated, reading_time


class ArticleMetadataTests(unittest.TestCase):
    def test_last_updated_uses_git_commit_timestamp(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_file = root / "content" / "page.md"
            source_file.parent.mkdir()
            source_file.write_text("Page", encoding="utf-8")

            with patch(
                "python.generator.metadata.subprocess.run",
                return_value=subprocess.CompletedProcess(
                    [], 0, stdout="2025-03-04T12:30:00+00:00\n", stderr=""
                ),
            ):
                label, timestamp = last_updated(source_file, root)

            self.assertEqual("Last updated Mar 4, 2025", label)
            self.assertEqual("2025-03-04T12:30:00+00:00", timestamp)

    def test_last_updated_falls_back_to_source_file_timestamp(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_file = root / "page.md"
            source_file.write_text("Page", encoding="utf-8")
            fallback = datetime(2024, 1, 2, 12, 0).timestamp()
            os.utime(source_file, (fallback, fallback))

            with patch("python.generator.metadata.subprocess.run", side_effect=FileNotFoundError):
                label, timestamp = last_updated(source_file, root)

            self.assertEqual("Last updated Jan 2, 2024", label)
            self.assertTrue(timestamp.startswith("2024-01-02T12:00:00"))

    def test_reading_time_rounds_up_and_excludes_fenced_code(self):
        self.assertEqual("1 min read", reading_time(""))
        self.assertEqual("1 min read", reading_time("word " * 200))
        self.assertEqual("2 min read", reading_time("word " * 201))
        self.assertEqual(
            "1 min read",
            reading_time(("word " * 200) + "\n```python\n" + ("code " * 400) + "\n```"),
        )


if __name__ == "__main__":
    unittest.main()
