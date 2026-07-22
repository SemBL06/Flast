from rich.progress import track

import python.generator.sitemap as sitemap
import python.generator.robots as robots
import python.generator.search as search
import python.generator.metadata as metadata
import python.generator.images as images
import python.generator.parser.main as parser
import python.generator.parser.yaml_dict as yamlParser
import python.generator.html.markdown as mdHTML
import python.generator.html.yaml as yamlHTML
import python.generator.html.main as combine
from pathlib import Path
import shutil
import os
from json import loads


def main(ROOT_DIR: Path):
    CONTENT_DIR = ROOT_DIR / "content"
    PUBLIC = ROOT_DIR / "public"

    configuration: dict = loads(
        (ROOT_DIR / "python" / "configuration" / "configuration.json").read_text()
    )

    clear_public(PUBLIC)

    output_files, input_files, converted_images = create_files(CONTENT_DIR, PUBLIC, configuration)
    layout: str = configuration.get("layout")
    copy_layout_assets(ROOT_DIR, layout, PUBLIC)
    from pygments.formatters import HtmlFormatter

    css = HtmlFormatter().get_style_defs(".codehilite")
    (PUBLIC / "css" / "syntax.css").write_text(css)

    # Pre-parse all pages to get titles and order
    pages = []
    for output_file, input_file in zip(output_files, input_files):
        yaml, markdown = parser.main(input_file)
        dict_meta, dict_sitemap = yamlParser.main(yaml)
        
        # Extract title and order
        title = dict_meta.get("title")
        if not title:
            title = input_file.stem.replace("_", " ").title()
            
        order = dict_meta.get("order")
        if order is None:
            order = dict_meta.get("weight")
        if order is None:
            order = 9999
        else:
            try:
                order = int(order)
            except ValueError:
                order = 9999
                
        dict_sitemap["url"] = output_file.relative_to(PUBLIC).as_posix()
        
        pages.append({
            "input_file": input_file,
            "output_file": output_file,
            "title": title,
            "order": order,
            "meta": dict_meta,
            "sitemap": dict_sitemap,
            "markdown": markdown,
            "body": mdHTML.main(markdown),
            "last_updated": metadata.last_updated(input_file, ROOT_DIR),
            "reading_time": metadata.reading_time(markdown),
        })

    search.create_index(pages, PUBLIC)

    xml = ""
    for page in track(pages, description="Making pages..."):
        output_file = page["output_file"]
        
        # HTML
        body = images.rewrite_converted_image_sources(
            page["body"], page["input_file"], output_file, converted_images
        )
        meta = yamlHTML.meta(page["meta"], PUBLIC, output_file)
        
        title, sidebar_tree, prev_page, next_page = yamlHTML.nav(
            configuration, pages, output_file, PUBLIC
        )
        
        search_index_path = os.path.relpath(
            PUBLIC / "search-index.json", start=output_file.parent
        ).replace("\\", "/")
        html = combine.main(
            meta,
            body,
            title,
            sidebar_tree,
            prev_page,
            next_page,
            search_index_path,
            page["last_updated"],
            page["reading_time"],
            configuration,
            ROOT_DIR,
        )
        output_file.write_text(html, encoding="utf-8")

        # Sitemap
        xml += sitemap.generate_xml(page["sitemap"], configuration)

    sitemap.create_xml(xml, ROOT_DIR)


def copy_layout_assets(root: Path, layout: str, public: Path):
    for asset_type in ("css", "js"):
        source = root / "layouts" / layout / asset_type
        if not source.exists():
            source = root / "layouts" / layout / asset_type.upper()
        if source.exists():
            destination = public / asset_type
            destination.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, destination, dirs_exist_ok=True)


def clear_public(public: Path):
    if public.exists():
        shutil.rmtree(public)


def create_files(CONTENT_DIR: Path, PUBLIC: Path, configuration):
    """
    Creates all the files

    Returns:
    The created files.
    """
    output_files = []
    input_files = []
    converted_images = {}
    robot_exists = False
    for file in CONTENT_DIR.rglob("*"):
        # Skip directories
        if file.is_dir():
            continue
        relative_path = file.relative_to(CONTENT_DIR)

        if file.suffix == ".md":
            output_path = PUBLIC / relative_path.with_suffix(".html")

            output_files.append(output_path)
            input_files.append(file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        elif file.suffix.lower() in images.CONVERTIBLE_EXTENSIONS:
            output_path = (PUBLIC / relative_path).with_suffix(".webp")
            images.convert_to_webp(file, output_path)
            converted_images[file.resolve()] = output_path.resolve()

        else:
            # Avoid error for dir not found
            output_path = PUBLIC / relative_path
            output_path.parent.mkdir(parents=True, exist_ok=True)

            output_path.write_bytes(file.read_bytes())
            if file.name == "robots.txt":
                robot_exists = True

    # Robots.txt generation
    if not robot_exists:
        robots_txt = robots.main(configuration)
        (PUBLIC / "robots.txt").write_text(robots_txt)

    return output_files, input_files, converted_images
