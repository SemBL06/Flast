import json
from pathlib import Path

import questionary
from questionary import Choice

import python.configuration.core as core
import python.configuration.layout as layout
import python.configuration.seo as seo
import python.text_formatter as formatter


BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "configuration.json"


def main():
    """Run the interactive configuration wizard."""
    configuration = get_configuration()



    while True:
        formatter.clear_screen()
        formatter.title("SSG: Configuration")
        choice = questionary.select(
            "What do you want to configure?",
            choices=[
                Choice(
                    title="Core ✅" if configuration["core"] else "Core",
                    value="core",
                ),
                Choice(
                    title="SEO ✅" if configuration["seo"] else "SEO",
                    value="SEO",
                ),
                Choice(
                    title="Layout ✅" if configuration["layout"] else "Layout",
                    value="layout",
                ),
                Choice(title="Exit", value="exit"),
            ],
        ).ask()

        match choice:
            case "SEO":
                configuration["seo"] = seo.main()
            case "layout":
                configuration["layout"] = layout.main()
            case "core":
                configuration["core"] = core.main()
            case "exit":
                if not _is_complete(configuration):
                    if questionary.confirm(
                        "You did not configure everything. Continue?"
                    ).ask():
                        return False
                    continue

                CONFIG_PATH.write_text(
                    json.dumps(configuration, indent=2) + "\n", encoding="utf-8"
                )
                return True


def get_configuration() -> dict:
    try:
        configuration = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        configuration = {"robots": "", "layout": "", "core": ""}

    return configuration


def _is_complete(configuration: dict) -> bool:
    return bool(
        configuration.get("seo")
        and configuration.get("layout")
        and configuration.get("core")
    )
