"""GitHub Pages implementation of Flast's deployment provider interface."""

import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Literal

from python.deployment.provider import DeploymentResult


PAGES_BRANCH = "gh-pages"
GITHUB_REMOTE_PATTERNS = (
    re.compile(r"https://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$"),
    re.compile(r"git@github\.com:([^/]+)/([^/]+?)(?:\.git)?/?$"),
)


class GitHubPagesProvider:
    name = "GitHub Pages"

    def __init__(self, repository: str | None = None):
        self.repository = repository

    def deploy_directory(self, root_dir: Path, directory: Path) -> DeploymentResult | None:
        """Publish ``directory`` to the repository's managed ``gh-pages`` branch."""
        git = shutil.which("git")
        gh = shutil.which("gh")
        if git is None:
            print("Git was not found on PATH. GitHub Pages deployment requires Git.")
            return None
        if gh is None:
            print("GitHub CLI was not found on PATH.")
            print("Install it from https://cli.github.com/ and run: gh auth login")
            return None

        repository = self._repository(root_dir, git)
        if repository is None:
            return None

        pages = self._get_pages_site(root_dir, gh, repository)
        if pages is False:
            return None
        if pages is not None and not self._uses_managed_branch(pages):
            print(
                "GitHub Pages is already configured from a different source. "
                f"Configure it to use {PAGES_BRANCH}/ (root) before deploying with Flast."
            )
            return None

        if not self._push_pages_branch(root_dir, directory, git):
            return None

        if pages is None:
            pages = self._create_pages_site(root_dir, gh, repository)
            if pages is None:
                return None

        canonical_url = pages.get("html_url")
        if not isinstance(canonical_url, str):
            canonical_url = self._default_pages_url(repository)
        return DeploymentResult(canonical_url=canonical_url)

    def _repository(self, root_dir: Path, git: str) -> str | None:
        if self.repository is not None:
            return self.repository

        remote = self._run([git, "config", "--get", "remote.origin.url"], root_dir)
        if remote is None:
            print("GitHub Pages deployment requires an origin remote on GitHub.")
            return None

        remote_url = remote.stdout.strip()
        for pattern in GITHUB_REMOTE_PATTERNS:
            match = pattern.fullmatch(remote_url)
            if match:
                return f"{match.group(1)}/{match.group(2)}"

        print("The origin remote is not a github.com repository.")
        return None

    def _get_pages_site(self, root_dir: Path, gh: str, repository: str) -> dict | None | bool:
        result = self._run_raw([gh, "api", f"repos/{repository}/pages"], root_dir)
        if result is not None and result.returncode == 0:
            try:
                response = json.loads(result.stdout)
            except json.JSONDecodeError:
                print("GitHub returned an invalid Pages response.")
                return False
            return response if isinstance(response, dict) else False

        # A 404 is expected before Pages has been enabled. Other failures are not.
        error_output = "" if result is None else result.stderr
        if "404" in error_output or "Not Found" in error_output:
            return None
        if error_output:
            print(error_output.strip())
        return False

    def _uses_managed_branch(self, pages: dict) -> bool:
        source = pages.get("source")
        return (
            isinstance(source, dict)
            and source.get("branch") == PAGES_BRANCH
            and source.get("path", "/") == "/"
        )

    def _push_pages_branch(self, root_dir: Path, directory: Path, git: str) -> bool:
        with tempfile.TemporaryDirectory(prefix="flast-github-pages-") as temporary_dir:
            pages_dir = Path(temporary_dir)
            shutil.copytree(directory, pages_dir, dirs_exist_ok=True)
            (pages_dir / ".nojekyll").touch()

            commands = (
                [git, "init"],
                [git, "config", "user.name", "Flast"],
                [git, "config", "user.email", "flast@local.invalid"],
                [git, "add", "--all"],
                [git, "commit", "-m", "Deploy Flast site"],
                [git, "remote", "add", "origin", self._origin_url(root_dir, git)],
                [git, "push", "--force", "origin", f"HEAD:refs/heads/{PAGES_BRANCH}"],
            )
            for command in commands:
                if self._run(command, pages_dir) is None:
                    print("Unable to publish the generated files to the gh-pages branch.")
                    return False
        return True

    def _origin_url(self, root_dir: Path, git: str) -> str:
        if self.repository is not None:
            return f"https://github.com/{self.repository}.git"
        result = self._run([git, "remote", "get-url", "origin"], root_dir)
        # _repository already verified this command and remote, so this is safe.
        return result.stdout.strip()  # type: ignore[union-attr]

    def _create_pages_site(self, root_dir: Path, gh: str, repository: str) -> dict | None:
        result = self._run(
            [
                gh,
                "api",
                "--method",
                "POST",
                f"repos/{repository}/pages",
                "-f",
                "build_type=legacy",
                "-f",
                f"source[branch]={PAGES_BRANCH}",
                "-f",
                "source[path]=/",
            ],
            root_dir,
        )
        if result is None:
            print("Unable to enable GitHub Pages for this repository.")
            return None
        if not result.stdout.strip():
            # GitHub can respond with 204 No Content after it accepts the Pages
            # configuration. The branch push still triggers the site build.
            return {}
        try:
            response = json.loads(result.stdout)
        except json.JSONDecodeError:
            print("GitHub returned an invalid Pages creation response.")
            return None
        return response if isinstance(response, dict) else None

    @classmethod
    def create_repository(
        cls, root_dir: Path, name: str, visibility: Literal["public", "private"]
    ) -> "GitHubPagesProvider | None":
        """Create an empty repository for Pages and return a provider for it."""
        gh = shutil.which("gh")
        if gh is None:
            print("GitHub CLI was not found on PATH.")
            return None
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
            print("Repository names may contain letters, numbers, dots, dashes, and underscores.")
            return None

        user = cls._run([gh, "api", "user"], root_dir)
        if user is None:
            return None
        try:
            login = json.loads(user.stdout).get("login")
        except json.JSONDecodeError:
            login = None
        if not isinstance(login, str):
            print("GitHub did not return the authenticated account name.")
            return None

        created = cls._run(
            [gh, "repo", "create", name, f"--{visibility}", "--confirm"], root_dir
        )
        if created is None:
            print("Unable to create the GitHub repository.")
            return None
        return cls(f"{login}/{name}")

    @staticmethod
    def _default_pages_url(repository: str) -> str:
        owner, name = repository.split("/", maxsplit=1)
        if name.lower() == f"{owner.lower()}.github.io":
            return f"https://{owner}.github.io/"
        return f"https://{owner}.github.io/{name}/"

    @staticmethod
    def _run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str] | None:
        result = GitHubPagesProvider._run_raw(command, cwd)
        if result is None:
            return None
        if result.returncode == 0:
            return result
        if result.stderr:
            print(result.stderr.strip())
        return None

    @staticmethod
    def _run_raw(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str] | None:
        try:
            return subprocess.run(
                command,
                cwd=cwd,
                check=False,
                capture_output=True,
                text=True,
            )
        except OSError as error:
            print(f"Unable to run {command[0]}: {error}")
            return None
