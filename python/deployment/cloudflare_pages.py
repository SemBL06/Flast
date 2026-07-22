"""Cloudflare Pages implementation of Flast's deployment provider interface."""

from pathlib import Path
import shutil
import subprocess

from python.deployment.provider import DeploymentResult


class CloudflarePagesProvider:
    name = "Cloudflare Pages"

    def __init__(self, project_name: str, create_project: bool = False):
        self.project_name = project_name
        self.create_project = create_project

    def deploy_directory(self, root_dir: Path, directory: Path) -> DeploymentResult | None:
        """Direct-upload generated files to a Cloudflare Pages project."""
        wrangler = shutil.which("wrangler")
        if wrangler is None:
            print("Wrangler was not found on PATH.")
            print("Install it with: npm install -g wrangler")
            print("Then authenticate with: wrangler login")
            return None

        if self.create_project and not self._run(
            [
                wrangler,
                "pages",
                "project",
                "create",
                self.project_name,
                "--production-branch",
                "production",
            ],
            root_dir,
        ):
            print("Unable to create the Cloudflare Pages project.")
            return None

        if not self._run(
            [
                wrangler,
                "pages",
                "deploy",
                str(directory.resolve()),
                "--project-name",
                self.project_name,
            ],
            root_dir,
        ):
            print("Cloudflare Pages deployment failed.")
            return None

        return DeploymentResult(
            canonical_url=f"https://{self.project_name}.pages.dev/"
        )

    @staticmethod
    def _run(command: list[str], cwd: Path) -> bool:
        try:
            result = subprocess.run(command, cwd=cwd, check=False)
        except OSError as error:
            print(f"Unable to run Wrangler: {error}")
            return False
        return result.returncode == 0
