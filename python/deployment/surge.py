"""Surge implementation of Flast's deployment provider interface."""

from pathlib import Path
import re
import shutil
import subprocess

from python.deployment.provider import DeploymentResult


_PUBLISHED_DOMAIN = re.compile(
    r"Success!.*?Published(?:\s+(?:to|and running at))?\s+"
    r"(?P<domain>https?://[^\s]+|[A-Za-z0-9.-]+\.[A-Za-z]{2,}[^\s]*)",
    re.IGNORECASE | re.DOTALL,
)
_ANSI_ESCAPE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")


class SurgeProvider:
    name = "Surge"

    def __init__(self, domain: str | None = None):
        """Create a provider, optionally targeting an already-known site URL."""
        self.domain = domain

    def deploy_directory(self, root_dir: Path, directory: Path) -> DeploymentResult | None:
        """Publish ``directory`` to Surge and return its production URL."""
        surge = shutil.which("surge")
        if surge is None:
            print("Surge CLI was not found on PATH.")
            print("Install it with: npm install -g surge")
            print("Then run surge once to sign in or create an account.")
            return None

        if not self._is_authenticated(surge, root_dir):
            return None

        if not self.domain:
            print("A Surge domain is required before publishing.")
            return None

        command = [surge, str(directory.resolve()), self.domain]

        try:
            result = subprocess.run(
                command,
                cwd=root_dir.resolve(),
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
        except OSError as error:
            print(f"Unable to start the Surge CLI: {error}")
            return None

        output = "\n".join(part for part in (result.stdout, result.stderr) if part)
        if output:
            print(output.rstrip())
        if result.returncode != 0:
            print(f"Surge deployment failed (exit code {result.returncode}).")
            if "already in use" in output.lower() or "already taken" in output.lower():
                print("That Surge domain is already in use. Choose a different domain and try again.")
            return None

        canonical_url = self._published_url(output)
        if canonical_url is None:
            print("Surge deployment succeeded but did not report a published domain.")
            return None
        return DeploymentResult(canonical_url=canonical_url)

    @staticmethod
    def _is_authenticated(surge: str, root_dir: Path) -> bool:
        """Check credentials before the publish command can open a login prompt."""
        try:
            result = subprocess.run(
                [surge, "whoami"],
                cwd=root_dir.resolve(),
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
                encoding="utf-8",
                errors="replace",
            )
        except subprocess.TimeoutExpired:
            print("Timed out while verifying the Surge sign-in.")
            return False
        except OSError as error:
            print(f"Unable to start the Surge CLI: {error}")
            return False

        if result.returncode == 0:
            return True

        output = "\n".join(part for part in (result.stdout, result.stderr) if part)
        if output:
            print(output.rstrip())
        print("You are not signed in to Surge. Run: surge login")
        return False

    @staticmethod
    def _published_url(output: str) -> str | None:
        """Return Surge's successful production domain as an HTTPS URL."""
        match = _PUBLISHED_DOMAIN.search(_ANSI_ESCAPE.sub("", output))
        if match is None:
            return None
        domain = match.group("domain").rstrip("/.,")
        return domain if domain.startswith(("http://", "https://")) else f"https://{domain}"
