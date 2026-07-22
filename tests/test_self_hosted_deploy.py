from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from python.deployment.self_hosted import SelfHostedProvider, SelfHostedTarget


class SelfHostedProviderTests(unittest.TestCase):
    def setUp(self):
        self.target = SelfHostedTarget("example.com", "deploy", 2222, "/var/www/site")

    def test_target_validation_requires_absolute_path_and_valid_port(self):
        self.assertIsNone(
            SelfHostedTarget.from_configuration(
                {"host": "example.com", "user": "deploy", "port": 22, "remote_path": "site"}
            )
        )
        self.assertIsNone(
            SelfHostedTarget.from_configuration(
                {"host": "example.com", "user": "deploy", "port": 22, "remote_path": "/"}
            )
        )
        self.assertIsNone(
            SelfHostedTarget.from_configuration(
                {"host": "example.com", "user": "deploy", "port": 0, "remote_path": "/site"}
            )
        )

    def test_confirms_before_applying_the_previewed_sync(self):
        with tempfile.TemporaryDirectory() as temporary:
            root_dir = Path(temporary)
            public_dir = root_dir / "public"
            public_dir.mkdir()
            confirmation = MagicMock(return_value=True)
            provider = SelfHostedProvider(self.target, confirm_deletions=confirmation)

            def run(command, **_):
                return subprocess.CompletedProcess(command, 0)

            with (
                patch("python.deployment.self_hosted.shutil.which", side_effect=["ssh", "rsync"]),
                patch("python.deployment.self_hosted.subprocess.run", side_effect=run) as run,
            ):
                self.assertIsNotNone(provider.deploy_directory(root_dir, public_dir))

            self.assertEqual(2, run.call_count)
            self.assertIn("--dry-run", run.call_args_list[0].args[0])
            self.assertIn("--mkpath", run.call_args_list[0].args[0])
            self.assertNotIn("capture_output", run.call_args_list[0].kwargs)
            confirmation.assert_called_once_with([])

    def test_uses_wsl_rsync_when_native_rsync_is_missing(self):
        provider = SelfHostedProvider(self.target)
        with (
            patch(
                "python.deployment.self_hosted.shutil.which",
                side_effect=["ssh", None, "wsl"],
            ),
            patch(
                "python.deployment.self_hosted.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, stdout="rsync version", stderr=""),
            ) as run,
        ):
            tools = provider._find_sync_tools(Path("."))

        self.assertTrue(tools.uses_wsl)
        self.assertEqual(["wsl", "rsync"], tools.rsync_command)
        self.assertEqual(["wsl", "ssh"], tools.ssh_command)
        self.assertEqual(["wsl", "rsync", "--version"], run.call_args.args[0])

    def test_wsl_path_translation_uses_forward_slashes(self):
        provider = SelfHostedProvider(self.target)
        tools = type("Tools", (), {"uses_wsl": True, "rsync_command": ["wsl"]})()
        with (
            patch(
                "python.deployment.self_hosted.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, stdout="/mnt/c/site\n", stderr=""),
            ) as run,
        ):
            source = provider._source_directory(Path("C:/Users/Sem/site"), Path("."), tools)

        self.assertEqual("/mnt/c/site/", source)
        self.assertNotIn("\\", run.call_args.args[0][-1])
