"""Provider-aware canonical URL selection."""

LOCALHOST_URL = "http://localhost/"


def normalise_url(url: str) -> str:
    return url.rstrip("/") + "/"


def active_url(configuration: dict) -> str:
    """Return self first, then the first saved provider URL, then localhost."""
    urls = _urls(configuration)
    self_url = urls.get("self")
    if self_url:
        return self_url
    return next(iter(urls.values()), LOCALHOST_URL)


def provider_urls(configuration: dict) -> dict[str, str]:
    """Return the configured URLs, migrating legacy ``domain_name`` in memory."""
    return _urls(configuration)


def ensure_provider_urls(configuration: dict) -> dict[str, str]:
    """Create the persisted URL mapping and migrate the legacy field once."""
    core = configuration.setdefault("core", {})
    if not isinstance(core, dict):
        raise ValueError("Core configuration must be an object.")

    urls = _urls(configuration)
    core["urls"] = urls
    core.pop("domain_name", None)
    return urls


def _urls(configuration: dict) -> dict[str, str]:
    core = configuration.get("core")
    if not isinstance(core, dict):
        return {}

    configured_urls = core.get("urls")
    if isinstance(configured_urls, dict):
        return {
            provider: normalise_url(url)
            for provider, url in configured_urls.items()
            if isinstance(provider, str) and isinstance(url, str) and url.strip()
        }

    legacy_url = core.get("domain_name")
    if isinstance(legacy_url, str) and legacy_url.strip():
        normalised = normalise_url(legacy_url)
        if normalised != LOCALHOST_URL:
            return {_legacy_provider(normalised): normalised}
    return {}


def _legacy_provider(url: str) -> str:
    hostname = url.split("://", maxsplit=1)[-1].split("/", maxsplit=1)[0].lower()
    if hostname.endswith(".netlify.app"):
        return "netlify"
    if hostname.endswith(".github.io"):
        return "github-pages"
    if hostname.endswith(".surge.sh"):
        return "surge"
    # Other legacy values were normally entered by the user in Core, so preserve
    # them as self-hosted canonical URLs.
    return "self"
