# Bestand opsplitsen in yml en HTML
from pathlib import Path


def main(file: Path):
    content = file.read_text(encoding="utf-8")

    if "---" not in content:
        return ("title: Default", content)

    return tuple(content.split("---", 2)[1:])
