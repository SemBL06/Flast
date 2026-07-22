"""Netlify implementation of Flast's deployment provider interface."""

import json
from pathlib import Path
import shutil
import subprocess

from python.deployment.provider import DeploymentResult


class NetlifyProvider:
    name = "Netlify"

    def deploy_directory(self, root_dir: Path, directory: Path) -> DeploymentResult | None:
        """Deploy a directory to Netlify production and read its JSON response."""
        netlify_cli = shutil.which("netlify")
        if netlify_cli is None:
            print("Netlify CLI was not found on PATH.")
            print("Install it with: npm install -g netlify-cli")
            print("Then authenticate with: netlify login")
            return None

        try:
            result = subprocess.run(
                [
                    netlify_cli,
                    "deploy",
                    "--dir",
                    str(directory.resolve()),
                    "--prod",
                    "--no-build",
                    "--json",
                ],
                cwd=root_dir.resolve(),
                check=False,
                capture_output=True,
                text=True,
            )
        except OSError as error:
            print(f"Unable to start the Netlify CLI: {error}")
            return None

        if result.returncode != 0:
            print(f"Netlify deployment failed (exit code {result.returncode}).")
            if result.stderr:
                print(result.stderr.strip())
            return None

        try:
            response = json.loads(result.stdout)
        except json.JSONDecodeError:
            print("Netlify deployment succeeded but did not return valid JSON.")
            return None

        if not isinstance(response, dict):
            print("Netlify deployment succeeded but returned an unexpected JSON response.")
            return None

        # The deploy API exposes the live site as ``ssl_url``/``url``. Some CLI
        # versions also provide ``site_url``. Do not use ``deploy_url`` here: it
        # identifies one immutable deploy rather than the site's live URL.
        canonical_url = (
            response.get("site_url")
            or response.get("ssl_url")
            or response.get("url")
        )
        return DeploymentResult(
            canonical_url=canonical_url if isinstance(canonical_url, str) else None
        )


def main(root_dir: Path) -> bool:
    """Backward-compatible direct Netlify deployment entry point."""
    public_dir = root_dir.resolve() / "public"
    if not public_dir.is_dir():
        print("No generated site found. Generate Site first, then try Deploy again.")
        return False
    return NetlifyProvider().deploy_directory(root_dir, public_dir) is not None
