from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from python.deployment.cloudflare_pages import CloudflarePagesProvider


class CloudflarePagesProviderTests(unittest.TestCase):
    def test_creates_then_deploys_and_returns_project_url(self):
        with tempfile.TemporaryDirectory() as directory:
            root_dir = Path(directory)
            public_dir = root_dir / "public"
            public_dir.mkdir()

            with (
                patch(
                    "python.deployment.cloudflare_pages.shutil.which",
                    return_value="wrangler",
                ),
                patch(
                    "python.deployment.cloudflare_pages.subprocess.run",
                    return_value=subprocess.CompletedProcess([], 0),
                ) as run,
            ):
                result = CloudflarePagesProvider("flast-docs", create_project=True).deploy_directory(
                    root_dir, public_dir
                )

            self.assertEqual("https://flast-docs.pages.dev/", result.canonical_url)
            self.assertEqual(2, run.call_count)
