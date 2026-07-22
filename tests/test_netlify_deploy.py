from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from python.deployment.netlify import NetlifyProvider, main as deploy_to_netlify


class NetlifyDeployTests(unittest.TestCase):
    def test_missing_public_directory_does_not_run_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("python.deployment.netlify.shutil.which") as find_cli:
                self.assertFalse(deploy_to_netlify(Path(directory)))

            find_cli.assert_not_called()

    def test_missing_cli_does_not_run_subprocess(self):
        with tempfile.TemporaryDirectory() as directory:
            root_dir = Path(directory)
            (root_dir / "public").mkdir()

            with (
                patch("python.deployment.netlify.shutil.which", return_value=None),
                patch("python.deployment.netlify.subprocess.run") as run,
            ):
                self.assertFalse(deploy_to_netlify(root_dir))

            run.assert_not_called()

    def test_deploys_directory_and_reads_stable_site_url(self):
        with tempfile.TemporaryDirectory() as directory:
            root_dir = Path(directory)
            public_dir = root_dir / "public"
            public_dir.mkdir()

            with (
                patch("python.deployment.netlify.shutil.which", return_value="netlify"),
                patch(
                    "python.deployment.netlify.subprocess.run",
                    return_value=subprocess.CompletedProcess(
                        [], 0, stdout='{"url": "https://example.netlify.app"}', stderr=""
                    ),
                ) as run,
            ):
                result = NetlifyProvider().deploy_directory(root_dir, public_dir)

            self.assertEqual("https://example.netlify.app", result.canonical_url)
            run.assert_called_once_with(
                [
                    "netlify",
                    "deploy",
                    "--dir",
                    str(public_dir.resolve()),
                    "--prod",
                    "--no-build",
                    "--json",
                ],
                cwd=root_dir.resolve(),
                check=False,
                capture_output=True,
                text=True,
            )

    def test_invalid_json_is_a_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root_dir = Path(directory)
            public_dir = root_dir / "public"
            public_dir.mkdir()
            with (
                patch("python.deployment.netlify.shutil.which", return_value="netlify"),
                patch(
                    "python.deployment.netlify.subprocess.run",
                    return_value=subprocess.CompletedProcess([], 0, stdout="not json", stderr=""),
                ),
            ):
                self.assertIsNone(NetlifyProvider().deploy_directory(root_dir, public_dir))
