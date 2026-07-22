"""Shared interfaces and result types for deployment providers."""

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class DeploymentResult:
    """The outcome returned by a provider after a successful deployment."""

    canonical_url: str | None = None


class DeploymentProvider(Protocol):
    """A provider capable of publishing a directory to its production site."""

    name: str

    def deploy_directory(self, root_dir: Path, directory: Path) -> DeploymentResult | None:
        """Deploy ``directory`` and return ``None`` when the provider fails."""
