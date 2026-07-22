import os
from pathlib import Path
import re
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from PIL import Image, UnidentifiedImageError


CONVERTIBLE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
IMAGE_SOURCE = re.compile(r'(<img\b[^>]*\bsrc=")([^"]+)(")', re.IGNORECASE)


def convert_to_webp(source: Path, destination: Path, quality: int = 85):
    """Convert a JPEG or PNG to WebP, retaining alpha transparency when present."""
    try:
        with Image.open(source) as image:
            has_alpha = image.mode in {"RGBA", "LA"} or (
                image.mode == "P" and "transparency" in image.info
            )
            converted = image.convert("RGBA" if has_alpha else "RGB")
            destination.parent.mkdir(parents=True, exist_ok=True)
            converted.save(destination, "WEBP", quality=quality, method=6)
    except (OSError, UnidentifiedImageError) as error:
        raise RuntimeError(f"Unable to convert image to WebP: {source}") from error


def rewrite_converted_image_sources(
    html: str,
    source_page: Path,
    output_page: Path,
    converted_images: dict[Path, Path],
) -> str:
    """Point local rendered image tags at converted WebP assets."""
    def replace(match: re.Match) -> str:
        original_url = match.group(2)
        parsed = urlsplit(original_url)
        if parsed.scheme or parsed.netloc or parsed.path.startswith("/"):
            return match.group(0)

        source_image = (source_page.parent / unquote(parsed.path)).resolve()
        converted_image = converted_images.get(source_image)
        if not converted_image:
            return match.group(0)

        relative_url = os.path.relpath(converted_image, output_page.parent).replace("\\", "/")
        rewritten_url = urlunsplit(("", "", quote(relative_url, safe="/"), parsed.query, parsed.fragment))
        return f"{match.group(1)}{rewritten_url}{match.group(3)}"

    return IMAGE_SOURCE.sub(replace, html)
