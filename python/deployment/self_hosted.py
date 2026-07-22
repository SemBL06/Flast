"""Self-hosted Linux deployment via rsync over SSH."""

from dataclasses import dataclass
from pathlib import Path
import shlex
import shutil
import subprocess
from typing import Callable

from python.deployment.provider import DeploymentResult


@dataclass(frozen=True)
class SelfHostedTarget:
    host: str
    user: str
    port: int
    remote_path: str

    @classmethod
    def from_configuration(cls, value: dict) -> "SelfHostedTarget | None":
        host = value.get("host")
        user = value.get("user")
        port = value.get("port")
        remote_path = value.get("remote_path")
        if not isinstance(host, str) or not host.strip() or any(char.isspace() for char in host):
            return None
        if not isinstance(user, str) or not user.strip() or any(char.isspace() for char in user):
            return None
        if not isinstance(port, int) or not 1 <= port <= 65535:
            return None
        if (
            not isinstance(remote_path, str)
            or not remote_path.startswith("/")
            or remote_path.rstrip("/") == ""
        ):
            return None
        return cls(host.strip(), user.strip(), port, remote_path.rstrip("/"))

    def as_configuration(self) -> dict:
        return {
            "host": self.host,
            "user": self.user,
            "port": self.port,
            "remote_path": self.remote_path,
        }

    @property
    def destination(self) -> str:
        return f"{self.user}@{self.host}"


@dataclass(frozen=True)
class SyncTools:
    rsync_command: list[str]
    ssh_command: list[str]
    uses_wsl: bool = False


class SelfHostedProvider:
    name = "Self-hosted/VPS"

    def __init__(
        self,
        target: SelfHostedTarget,
        confirm_deletions: Callable[[list[str]], bool] | None = None,
    ):
        self.target = target
        self._confirm_deletions = confirm_deletions or _confirm_deletions

    def deploy_directory(self, root_dir: Path, directory: Path) -> DeploymentResult | None:
        """Create the remote folder and mirror the generated site into it."""
        tools = self._find_sync_tools(root_dir)
        if tools is None:
            return None
        
        source_directory = self._source_directory(directory, root_dir, tools)
        if source_directory is None:
            return None

        if not self._run_ssh(tools, root_dir):
            print("Unable to create or access the configured remote directory.")
            return None

        dry_run = self._run_rsync(tools, root_dir, source_directory, dry_run=True)
        if dry_run is None:
            print("Unable to preview the remote sync.")
            return None

        deletions = [line for line in dry_run.stdout.splitlines() if line.startswith("*deleting ")]
        if deletions:
            print("The following remote files will be deleted:")
            print("\n".join(deletions))
            if not self._confirm_deletions(deletions):
                print("Deployment cancelled; no remote files were changed.")
                return None

        if self._run_rsync(tools, root_dir, source_directory, dry_run=False) is None:
            print("rsync failed while updating the remote site.")
            return None
        return DeploymentResult()

    def _find_sync_tools(self, root_dir: Path) -> SyncTools | None:
        ssh = shutil.which("ssh")
        rsync = shutil.which("rsync")
        if ssh is not None and rsync is not None:
            return SyncTools([rsync], [ssh])

        wsl = shutil.which("wsl")
        if wsl is not None and self._run_probe([wsl, "rsync", "--version"], root_dir):
            return SyncTools([wsl, "rsync"], [wsl, "ssh"], uses_wsl=True)

        if rsync is None:
            print("rsync was not found on PATH or in WSL.")
            print("Install rsync, or install WSL with a Linux distro that includes rsync.")
        if ssh is None and wsl is None:
            print("SSH was not found on PATH. Self-hosted deployment requires SSH.")
        return None

    @staticmethod
    def _run_probe(command: list[str], root_dir: Path) -> bool:
        try:
            return subprocess.run(
                command,
                cwd=root_dir,
                check=False,
                capture_output=True,
                text=True,
            ).returncode == 0
        except OSError:
            return False

    def _source_directory(
        self, directory: Path, root_dir: Path, tools: SyncTools
    ) -> str | None:
        source = str(directory.resolve()).rstrip("\\/") + "/"
        if not tools.uses_wsl:
            return source

        wsl = tools.rsync_command[0]
        # wsl.exe treats backslashes in a Windows argument as escapes before
        # forwarding it to Linux, so pass a C:/... path to wslpath instead.
        windows_path = directory.resolve().as_posix()
        try:
            result = subprocess.run(
                [wsl, "wslpath", "-a", windows_path],
                cwd=root_dir,
                check=False,
                capture_output=True,
                text=True,
            )
        except OSError as error:
            print(f"Unable to translate the public directory for WSL: {error}")
            return None
        if result.returncode != 0 or not result.stdout.strip():
            if result.stderr:
                print(result.stderr.strip())
            print("Unable to translate the public directory for WSL.")
            return None
        return result.stdout.strip().rstrip("/") + "/"

    def _run_ssh(self, tools: SyncTools, root_dir: Path) -> bool:
        remote_command = f"mkdir -p -- {shlex.quote(self.target.remote_path)}"
        try:
            result = subprocess.run(
                [*tools.ssh_command, "-p", str(self.target.port), self.target.destination, remote_command],
                cwd=root_dir,
                check=False,
            )
        except OSError as error:
            print(f"Unable to start SSH: {error}")
            return False
        return result.returncode == 0

    def _run_rsync(
        self, tools: SyncTools, root_dir: Path, source_directory: str, *, dry_run: bool
    ) -> subprocess.CompletedProcess[str] | None:
        remote_path = self.target.remote_path.rstrip("/") + "/"
        command = [
            *tools.rsync_command,
            "-rlptz",
            "--delete",
            "--itemize-changes",
            "-e",
            f"ssh -p {self.target.port}",
        ]
        if dry_run:
            command.append("--dry-run")
        command.extend(
            [
                source_directory,
                f"{self.target.destination}:{shlex.quote(remote_path)}",
            ]
        )
        try:
            result = subprocess.run(
                command,
                cwd=root_dir,
                check=False,
                capture_output=dry_run,
                text=dry_run,
            )
        except OSError as error:
            print(f"Unable to start rsync: {error}")
            return None
        if result.returncode != 0:
            if dry_run and result.stderr:
                print(result.stderr.strip())
            return None
        if dry_run and result.stdout:
            print(result.stdout.strip())
        return result


def _confirm_deletions(_: list[str]) -> bool:
    """Ask only when running Flast interactively, keeping the provider UI-agnostic."""
    import questionary

    return questionary.confirm("Continue with these deletions?", default=False).ask()
