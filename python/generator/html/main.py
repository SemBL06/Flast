from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import python.generator.socials as socials


def main(
    meta: str,
    body: str,
    title,
    tree,
    prev_page,
    next_page,
    search_index_path,
    last_updated,
    reading_time,
    configuration: dict,
    root: Path,
):
    layout: str = configuration.get("layout")
    layout_dir: Path = root / "layouts" / layout
    # Setup Jinja2
    env = Environment(loader=FileSystemLoader((layout_dir / "html")))
    document_page = env.get_template("doc.html")

    # Render template with markdown HTML
    return document_page.render(
        body=body,
        meta=meta,
        title=title,
        sidebar_tree=tree,
        prev_page=prev_page,
        next_page=next_page,
        search_index_path=search_index_path,
        last_updated=last_updated[0],
        last_updated_iso=last_updated[1],
        reading_time=reading_time,
        social_links=socials.links(configuration),
        configuration=configuration
    )


if __name__ == "__main__":
    main()
