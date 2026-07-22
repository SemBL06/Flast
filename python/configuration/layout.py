import python.text_formatter as formatter
import questionary as q
from pathlib import Path


def main():
    formatter.clear_screen()
    formatter.title("SSG: Style configuration")
    layout_path = Path(__file__).parent.parent.parent / "layouts"

    choices = [template.name for template in layout_path.iterdir() if template.is_dir()]

    return q.select(
        "Which template do you wish to use?",
        choices=choices,
    ).ask()
