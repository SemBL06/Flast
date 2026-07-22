from datetime import datetime
from math import ceil
from pathlib import Path
import re
import subprocess


WORDS_PER_MINUTE = 200
FENCED_CODE_BLOCK = re.compile(r"^(```|~~~).*?^\1\s*$", re.MULTILINE | re.DOTALL)
WORD = re.compile(r"[\w'-]+", re.UNICODE)


def last_updated(source_file: Path, root: Path) -> tuple[str, str]:
    """Return a human-readable and ISO timestamp for a content source file."""
    timestamp = _git_timestamp(source_file, root) or datetime.fromtimestamp(source_file.stat().st_mtime)
    return _format_date(timestamp), timestamp.isoformat()


def reading_time(markdown: str) -> str:
    """Return a prose-only reading estimate for Markdown content."""
    prose = FENCED_CODE_BLOCK.sub("", markdown)
    minutes = max(1, ceil(len(WORD.findall(prose)) / WORDS_PER_MINUTE))
    return f"{minutes} min read"


def _git_timestamp(source_file: Path, root: Path) -> datetime | None:
    try:
        relative_path = source_file.relative_to(root)
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(relative_path)],
            cwd=root,
            capture_output=True,
            check=False,
            text=True,
        )
    except (OSError, ValueError):
        return None

    timestamp = result.stdout.strip()
    if not timestamp:
        return None

    try:
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return None


def _format_date(timestamp: datetime) -> str:
    return f"Last updated {timestamp.strftime('%b')} {timestamp.day}, {timestamp.year}"
