# Markdown to HTML and send it to main
from markdown import markdown


def main(md: str):
    return markdown(
        md,
        extensions=[
            "fenced_code",
            "tables",
            "toc",
            "codehilite",
            "smarty",
        ],
    )


if __name__ == "__main__":
    main()
