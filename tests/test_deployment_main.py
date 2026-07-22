import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from python.deployment.main import main as deploy_site
from python.deployment.provider import DeploymentResult


class FakeProvider:
    name = "Fake"

    def __init__(self, results):
        self.results = iter(results)
        self.directories = []
        self.bootstrap_contents = None

    def deploy_directory(self, root_dir, directory):
        self.directories.append(directory)
        index_file = directory / "index.html"
        if index_file.exists() and directory.name.startswith("flast-bootstrap-"):
            self.bootstrap_contents = index_file.read_text(encoding="utf-8")
        return next(self.results)


class DeploymentWorkflowTests(unittest.TestCase):
    def _write_configuration(self, root_dir, domain_name, provider="surge"):
        config_path = root_dir / "python" / "configuration"
        config_path.mkdir(parents=True)
        (config_path / "configuration.json").write_text(
            json.dumps(
                {
                    "robots": {},
                    "layout": "default",
                    "core": {"domain_name": domain_name, "site_title": "Test"},
                    "deployment": {"provider": provider},
                }
            ),
            encoding="utf-8",
        )

    def test_unknown_url_bootstraps_saves_url_generates_then_deploys(self):
        with tempfile.TemporaryDirectory() as directory:
            root_dir = Path(directory)
            self._write_configuration(root_dir, "http://localhost/")
            provider = FakeProvider(
                [DeploymentResult("https://example.surge.sh"), DeploymentResult()]
            )

            with (
                patch("python.deployment.main.PROVIDERS", {"surge": provider}),
                patch(
                    "python.deployment.main.questionary.select",
                    side_effect=[
                        Mock(ask=Mock(return_value="Third Party")),
                        Mock(ask=Mock(return_value="surge")),
                    ],
                ),
                patch("python.deployment.main._choose_surge_provider", return_value=provider),
                patch("python.deployment.main._generate_site") as generate_site,
            ):
                self.assertTrue(deploy_site(root_dir))

            configuration = json.loads(
                (root_dir / "python" / "configuration" / "configuration.json").read_text()
            )
            self.assertEqual(
                "https://example.surge.sh/", configuration["core"]["urls"]["surge"]
            )
            self.assertEqual(2, len(provider.directories))
            self.assertIn("Flast is deploying", provider.bootstrap_contents)
            generate_site.assert_called_once_with(root_dir.resolve())

    def test_known_url_deploys_public_without_regenerating(self):
        with tempfile.TemporaryDirectory() as directory:
            root_dir = Path(directory)
            self._write_configuration(root_dir, "https://site.netlify.app/", provider="netlify")
            public_dir = root_dir / "public"
            public_dir.mkdir()
            provider = FakeProvider([DeploymentResult()])

            with (
                patch("python.deployment.main.PROVIDERS", {"netlify": provider}),
                patch(
                    "python.deployment.main.questionary.select",
                    side_effect=[
                        Mock(ask=Mock(return_value="Third Party")),
                        Mock(ask=Mock(return_value="netlify")),
                    ],
                ),
                patch("python.deployment.main._generate_site") as generate_site,
            ):
                self.assertTrue(deploy_site(root_dir))

            self.assertEqual([public_dir], provider.directories)
            generate_site.assert_not_called()

    def test_no_provider_does_not_deploy(self):
        with tempfile.TemporaryDirectory() as directory:
            root_dir = Path(directory)
            self._write_configuration(root_dir, "http://localhost/", provider=None)
            with (
                patch("python.deployment.main.PROVIDERS", {}),
                patch(
                    "python.deployment.main.questionary.select",
                    side_effect=[
                        Mock(ask=Mock(return_value="Third Party")),
                        Mock(ask=Mock(return_value=None)),
                    ],
                ),
            ):
                self.assertFalse(deploy_site(root_dir))
