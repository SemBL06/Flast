"""Provider-independent deployment workflow."""

import json
from pathlib import Path
import re
import tempfile
import questionary

from python.deployment.netlify import NetlifyProvider
from python.deployment.github_pages import GitHubPagesProvider
from python.deployment.cloudflare_pages import CloudflarePagesProvider
from python.deployment.surge import SurgeProvider
from python.deployment.self_hosted import SelfHostedProvider, SelfHostedTarget
from python.deployment.provider import DeploymentProvider
from python.configuration.urls import active_url, ensure_provider_urls, normalise_url, provider_urls
import python.text_formatter as formatter

CONFIGURATION_PATH = Path("python") / "configuration" / "configuration.json"
PROVIDERS: dict[str, DeploymentProvider] = {
    "netlify": NetlifyProvider(),
    "github-pages": GitHubPagesProvider(),
    "cloudflare-pages": CloudflarePagesProvider("placeholder"),
    "surge": SurgeProvider(),
}


def main(root_dir: Path) -> bool:
    """Deploy using the configured provider, bootstrapping a provider URL if needed."""

    root_dir = root_dir.resolve()

    configuration_path = root_dir / CONFIGURATION_PATH
    configuration = _read_configuration(configuration_path)
    if configuration is None:
        print("Unable to read configuration. Configure the site before deploying.")
        return False

    formatter.clear_screen()
    formatter.title("[red]SSG: Deploy", "By Sem!")
    
    choice = questionary.select(
                "How do you host the site?",
                choices=["Self-Hosted/VPS", "Third Party"],
            ).ask()
    provider = None
    formatter.clear_screen()

    if choice == "Self-Hosted/VPS":
        provider_name = "self"
        provider = _choose_self_hosted_provider(configuration)
    else:
        provider_name = questionary.select(
            "Which one?",
            choices=[
                questionary.Choice(title=provider.name, value=key)
                for key, provider in PROVIDERS.items()
            ],
        ).ask()
        provider = PROVIDERS.get(provider_name)
        if provider_name == "github-pages":
            provider = _choose_github_pages_provider(root_dir)
        if provider_name == "cloudflare-pages":
            provider = _choose_cloudflare_pages_provider()
        if provider_name == "surge":
            provider = _choose_surge_provider(configuration)

    if provider is None:
        print("No deployment provider was selected.")
        return False

    formatter.clear_screen()

    try:
        urls = ensure_provider_urls(configuration)
    except ValueError as error:
        print(error)
        return False
    if not _write_configuration(configuration_path, configuration):
        return False
    if provider_name == "surge" and urls.get("surge"):
        provider = SurgeProvider(urls["surge"])
    public_dir = root_dir / "public"

    if provider_name == "self" and "self" not in urls:
        print("Self-hosted deployment requires an explicit site URL in Configure → Core.")
        return False

    if provider_name in urls:
        if not public_dir.is_dir():
            print("No generated site found. Generate Site first, then try Deploy again.")
            return False
        return _deploy_directory(provider_name, provider, root_dir, public_dir)

    print(f"No site URL is configured. Creating a {provider.name} site first...")

    # Creating temporary upload folder with small file for getting a small website.
    with tempfile.TemporaryDirectory(prefix="flast-bootstrap-") as temporary_dir:
        bootstrap_dir = Path(temporary_dir)
        (bootstrap_dir / "index.html").write_text(
            "<!doctype html><title>Deploying</title><p>Flast is deploying this site.</p>",
            encoding="utf-8",
        )
        bootstrap = provider.deploy_directory(root_dir, bootstrap_dir) # Deploy the temporary site to the third party

    if bootstrap is None:
        print("Something went wrong with deploying")
        return False
    if not isinstance(bootstrap.canonical_url, str) or not bootstrap.canonical_url:
        print(f"{provider.name} did not return a stable production URL.")
        return False

    # Adding URL to variable
    urls[provider_name] = normalise_url(bootstrap.canonical_url)

    # Saving the new URL
    if not _write_configuration(configuration_path, configuration):
        return False
    print("Saved the provider URL. Generating the site with its final URLs...")

    try:
        _generate_site(root_dir)
    except Exception as error:
        print(f"Site generation failed after bootstrap deployment: {error}")
        return False

    return _deploy_directory(provider_name, provider, root_dir, public_dir)


def _deploy_directory(
    provider_name: str, provider: DeploymentProvider, root_dir: Path, directory: Path
) -> bool:
    print(f"Deploying {directory.name}/ to {provider.name} production...")
    result = provider.deploy_directory(root_dir, directory)
    if result is None:
        return False
    formatter.clear_screen()
    configuration = _read_configuration(root_dir / CONFIGURATION_PATH) or {}
    address = provider_urls(configuration).get(provider_name, active_url(configuration))
    formatter.title(
        f"[red]Address: [bold]{address}", f"{provider.name} - [green]Success"
    )
    return True


def _read_configuration(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _write_configuration(path: Path, configuration: dict) -> bool:
    try:
        path.write_text(json.dumps(configuration, indent=2) + "\n", encoding="utf-8")
    except OSError as error:
        print(f"Unable to save the provider URL: {error}")
        return False
    return True


def _generate_site(root_dir: Path) -> None:
    """Import lazily so direct deployments do not load generator dependencies."""
    from python.generator.main import main as generate_site

    generate_site(root_dir)


def _choose_github_pages_provider(root_dir: Path) -> GitHubPagesProvider | None:
    choice = questionary.select(
        "Which GitHub repository should host the site?",
        choices=[
            questionary.Choice(title="Use the current repository", value="current"),
            questionary.Choice(title="Choose a different repository", value="existing"),
            questionary.Choice(title="Create a new repository", value="new"),
        ],
    ).ask()

    if choice == "current":
        return GitHubPagesProvider()
    if choice == "existing":
        repository = questionary.text("Repository (owner/name):").ask()
        if not isinstance(repository, str) or not _is_github_repository(repository):
            print("Enter a GitHub repository as owner/name.")
            return None
        return GitHubPagesProvider(repository)
    if choice == "new":
        name = questionary.text("New repository name:").ask()
        if not isinstance(name, str) or not name:
            print("A repository name is required.")
            return None
        visibility = questionary.select(
            "Repository visibility:",
            choices=[
                questionary.Choice(title="Public", value="public"),
                questionary.Choice(title="Private", value="private"),
            ],
        ).ask()
        if visibility not in {"public", "private"}:
            return None
        return GitHubPagesProvider.create_repository(root_dir, name, visibility)
    return None


def _is_github_repository(repository: str) -> bool:
    return repository.count("/") == 1 and all(repository.split("/"))


def _choose_cloudflare_pages_provider() -> CloudflarePagesProvider | None:
    choice = questionary.select(
        "Which Cloudflare Pages project should host the site?",
        choices=[
            questionary.Choice(title="Use an existing project", value="existing"),
            questionary.Choice(title="Create a new project", value="new"),
        ],
    ).ask()
    project_name = questionary.text("Cloudflare Pages project name:").ask()
    if not isinstance(project_name, str) or not project_name.strip():
        print("A Cloudflare Pages project name is required.")
        return None
    if choice == "existing":
        return CloudflarePagesProvider(project_name.strip())
    if choice == "new":
        return CloudflarePagesProvider(project_name.strip(), create_project=True)
    return None


def _choose_surge_provider(configuration: dict) -> SurgeProvider | None:
    saved_domain = provider_urls(configuration).get("surge")
    if saved_domain:
        return SurgeProvider(saved_domain)

    domain = questionary.text(
        "Surge domain (for example, my-site.surge.sh):"
    ).ask()
    if not isinstance(domain, str) or not _is_surge_domain(domain):
        print("Enter a valid Surge or custom domain, such as my-site.surge.sh.")
        return None
    return SurgeProvider(domain.strip().rstrip("/"))


def _is_surge_domain(domain: str) -> bool:
    return bool(
        re.fullmatch(
            r"(?:https?://)?[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+(?::[0-9]+)?/?",
            domain.strip(),
        )
    )


def _choose_self_hosted_provider(configuration: dict) -> SelfHostedProvider | None:
    deployment = configuration.setdefault("deployment", {})
    saved_target = deployment.get("self")
    target = SelfHostedTarget.from_configuration(saved_target) if isinstance(saved_target, dict) else None

    if target is not None:
        label = f"{target.destination}:{target.remote_path} (port {target.port})"
        if questionary.confirm(f"Use saved self-hosted target {label}?", default=True).ask():
            return SelfHostedProvider(target)

    host = questionary.text("Linux server hostname or IP:").ask()
    user = questionary.text("SSH username:").ask()
    port_text = questionary.text("SSH port:", default="22").ask()
    remote_path = questionary.text("Remote web directory (absolute path):").ask()
    try:
        port = int(port_text)
    except (TypeError, ValueError):
        port = 0
    target = SelfHostedTarget.from_configuration(
        {"host": host, "user": user, "port": port, "remote_path": remote_path}
    )
    if target is None:
        print("Enter a hostname, username, port from 1 to 65535, and an absolute remote path.")
        return None

    deployment["self"] = target.as_configuration()
    return SelfHostedProvider(target)
