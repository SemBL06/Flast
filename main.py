import questionary
import python.text_formatter as formatter
from python.configuration.main import main as configure
from python.deployment.main import main as deploy_site
from python.generator.main import main as generator
from pathlib import Path


def main():
    ROOT_DIR = Path(__file__).parent
    while True:
        formatter.clear_screen()
        formatter.title("[red]SSG: Startup", "By Sem!")

        choice = questionary.select(
            "What do you want to do?",
            choices=["Configure", "Generate Site", "Deploy", "Exit"],
        ).ask()

        match choice:
            case "Configure":
                configure()

            case "Generate Site":
                config_path = ROOT_DIR / "python" / "configuration" / "configuration.json"
                is_configured = False
                if config_path.exists():
                    try:
                        import json
                        config = json.loads(config_path.read_text(encoding="utf-8"))
                        if config.get("seo") and config.get("layout") and config.get("core"):
                            is_configured = True
                    except Exception:
                        pass
                
                if not is_configured:
                    if questionary.confirm("Warning: Site is not fully configured yet. Would you like to run the configuration wizard first?").ask():
                        configure()
                        # Re-check config
                        if config_path.exists():
                            try:
                                config = json.loads(config_path.read_text(encoding="utf-8"))
                                if config.get("robots") and config.get("layout") and config.get("core"):
                                    is_configured = True
                            except Exception:
                                pass
                        if not is_configured:
                            print("Continuing site generation with default or partial configuration...")

                generator(ROOT_DIR)

            case "Deploy":
                deploy_site(ROOT_DIR)
                input("\nPress Enter to return to the main menu...")

            case "Exit":
                formatter.clear_screen()
                formatter.title("[red]Thank you for using SSG")
                break


if __name__ == "__main__":
    main()
