from rich.console import Console
from rich import print
from rich.panel import Panel


def clear_screen():
    console = Console()
    console.clear()


def title(title: str, subtitle=""):
    print(
        Panel(
            title, padding=1, subtitle=subtitle, subtitle_align="left", style="yellow"
        )
    )
