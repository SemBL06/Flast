from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import call, patch

from python.deployment.surge import SurgeProvider


class SurgeDeployTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root_dir = Path(self.directory.name)
        self.public_dir = self.root_dir / "public"
        self.public_dir.mkdir()

    def tearDown(self):
        self.directory.cleanup()

    def test_missing_cli_does_not_run_subprocess(self):
        with (
            patch("python.deployment.surge.shutil.which", return_value=None),
            patch("python.deployment.surge.subprocess.run") as run,
        ):
            self.assertIsNone(SurgeProvider().deploy_directory(self.root_dir, self.public_dir))

        run.assert_not_called()

    def test_signed_in_deploy_reads_published_domain(self):
        domain = "fresh-site.surge.sh"
        with (
            patch("python.deployment.surge.shutil.which", return_value="surge"),
            patch(
                "python.deployment.surge.subprocess.run",
                side_effect=[
                    subprocess.CompletedProcess([], 0, stdout="me@example.com - Standard\n", stderr=""),
                    subprocess.CompletedProcess(
                        [], 0, stdout="Success! - Published to fresh-site.surge.sh\n", stderr=""
                    ),
                ],
            ) as run,
        ):
            result = SurgeProvider(domain).deploy_directory(self.root_dir, self.public_dir)

        self.assertEqual("https://fresh-site.surge.sh", result.canonical_url)
        run.assert_has_calls(
            [
                call(
                    ["surge", "whoami"],
                    cwd=self.root_dir.resolve(),
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=15,
                    encoding="utf-8",
                    errors="replace",
                ),
                call(
                    ["surge", str(self.public_dir.resolve()), domain],
                    cwd=self.root_dir.resolve(),
                    check=False,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                ),
            ]
        )

    def test_known_domain_is_used_for_later_deployments(self):
        domain = "https://fresh-site.surge.sh/"
        with (
            patch("python.deployment.surge.shutil.which", return_value="surge"),
            patch(
                "python.deployment.surge.subprocess.run",
                side_effect=[
                    subprocess.CompletedProcess([], 0, stdout="me@example.com\n", stderr=""),
                    subprocess.CompletedProcess(
                        [], 0, stdout="Success! Published fresh-site.surge.sh\n", stderr=""
                    ),
                ],
            ) as run,
        ):
            result = SurgeProvider(domain).deploy_directory(self.root_dir, self.public_dir)

        self.assertEqual("https://fresh-site.surge.sh", result.canonical_url)
        self.assertEqual(
            ["surge", str(self.public_dir.resolve()), domain], run.call_args.args[0]
        )

    def test_styled_success_output_reads_published_domain(self):
        output = "\x1b[32mSuccess!\x1b[0m - \x1b[1mPublished\x1b[0m to site.surge.sh"
        self.assertEqual("https://site.surge.sh", SurgeProvider._published_url(output))

    def test_signed_out_account_stops_before_publish(self):
        with (
            patch("python.deployment.surge.shutil.which", return_value="surge"),
            patch(
                "python.deployment.surge.subprocess.run",
                return_value=subprocess.CompletedProcess([], 1, stdout="", stderr="Not logged in"),
            ) as run,
        ):
            self.assertIsNone(SurgeProvider().deploy_directory(self.root_dir, self.public_dir))

        run.assert_called_once()
        self.assertEqual(["surge", "whoami"], run.call_args.args[0])

    def test_missing_domain_stops_before_publish(self):
        with (
            patch("python.deployment.surge.shutil.which", return_value="surge"),
            patch(
                "python.deployment.surge.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, stdout="me@example.com", stderr=""),
            ) as run,
        ):
            self.assertIsNone(SurgeProvider().deploy_directory(self.root_dir, self.public_dir))

        run.assert_called_once()

    def test_failed_or_unparseable_deploy_returns_none(self):
        signed_in = subprocess.CompletedProcess([], 0, stdout="me@example.com\n", stderr="")
        with patch("python.deployment.surge.shutil.which", return_value="surge"):
            with patch(
                "python.deployment.surge.subprocess.run",
                side_effect=[signed_in, subprocess.CompletedProcess([], 1, stdout="", stderr="failed")],
            ):
                self.assertIsNone(
                    SurgeProvider("site.surge.sh").deploy_directory(self.root_dir, self.public_dir)
                )
            with patch(
                "python.deployment.surge.subprocess.run",
                side_effect=[signed_in, subprocess.CompletedProcess([], 0, stdout="done", stderr="")],
            ):
                self.assertIsNone(
                    SurgeProvider("site.surge.sh").deploy_directory(self.root_dir, self.public_dir)
                )

    def test_authentication_launch_error_or_timeout_returns_none(self):
        with patch("python.deployment.surge.shutil.which", return_value="surge"):
            with patch(
                "python.deployment.surge.subprocess.run", side_effect=OSError("unavailable")
            ):
                self.assertIsNone(SurgeProvider().deploy_directory(self.root_dir, self.public_dir))
            with patch(
                "python.deployment.surge.subprocess.run",
                side_effect=subprocess.TimeoutExpired(["surge", "whoami"], 15),
            ):
                self.assertIsNone(SurgeProvider().deploy_directory(self.root_dir, self.public_dir))
