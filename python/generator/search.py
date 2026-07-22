import json
import re
from html.parser import HTMLParser
from pathlib import Path


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data: str):
        self.parts.append(data)


def plain_text(html: str) -> str:
    """Return whitespace-normalized text from rendered page HTML."""
    parser = _TextExtractor()
    parser.feed(html)
    parser.close()
    return re.sub(r"\s+", " ", " ".join(parser.parts)).strip()


def create_index(pages: list[dict], public: Path) -> Path:
    """Write a browser-searchable index for generated Markdown pages."""
    entries = [
        {
            "title": page["title"],
            "url": page["output_file"].relative_to(public).as_posix(),
            "content": plain_text(page["body"]),
        }
        for page in pages
    ]
    index_path = public / "search-index.json"
    index_path.write_text(
        json.dumps(entries, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    return index_path
