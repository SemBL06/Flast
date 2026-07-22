import re
from urllib.parse import urlsplit


EMAIL = re.compile(r"^[^@\s]+@[^@\s]+$")
PLATFORMS = {
    "instagram": ("instagram.com",),
    "facebook": ("facebook.com", "fb.com"),
    "x": ("x.com", "twitter.com"),
    "linkedin": ("linkedin.com",),
    "youtube": ("youtube.com", "youtu.be"),
    "github": ("github.com",),
    "tiktok": ("tiktok.com",),
    "discord": ("discord.com", "discord.gg"),
}


def links(configuration: dict) -> list[dict]:
    """Return safe, template-ready contact and social links."""
    core = configuration.get("core")
    if not isinstance(core, dict):
        return []

    result = []
    email = core.get("contact_email")
    if isinstance(email, str) and EMAIL.fullmatch(email.strip()):
        address = email.strip()
        result.append({"href": f"mailto:{address}", "label": "Email", "icon": "email", "external": False})

    social_urls = core.get("socials")
    if not isinstance(social_urls, list):
        return result

    for url in social_urls:
        if not isinstance(url, str):
            continue
        parsed = urlsplit(url.strip())
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            continue

        icon, label = _platform(parsed.hostname)
        result.append({"href": url.strip(), "label": label, "icon": icon, "external": True})

    return result


def _platform(hostname: str) -> tuple[str, str]:
    hostname = hostname.lower().removeprefix("www.")
    if "mastodon" in hostname:
        return "mastodon", "Mastodon"

    for name, domains in PLATFORMS.items():
        if any(hostname == domain or hostname.endswith(f".{domain}") for domain in domains):
            return name, "X / Twitter" if name == "x" else name.title()

    return "link", "Social link"
