from pathlib import Path
import os


def meta(yaml_dict: dict, PUBLIC: Path, output_file: Path):
    css_file = PUBLIC / "css" / "documentation.css"
    syntax_file = PUBLIC / "css" / "syntax.css"
    favicon_file = PUBLIC / "favicon.ico"
    js_file = PUBLIC / "js" / "main.js"
    
    relative_css = os.path.relpath(css_file, start=output_file.parent).replace("\\", "/")
    relative_syntax = os.path.relpath(syntax_file, start=output_file.parent).replace("\\", "/")
    relative_favicon = os.path.relpath(favicon_file, start=output_file.parent).replace("\\", "/")
    relative_js = os.path.relpath(js_file, start=output_file.parent).replace("\\", "/")
    
    return f"""
    <meta charset="{yaml_dict.get("charset", "UTF-8")}" />
    <meta name="description" content="{yaml_dict.get("description", "Change me in the .md!")}" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="icon" type="image/x-icon" href="{relative_favicon}">
    <link rel="stylesheet" href="{relative_css}" />
    <link rel="stylesheet" href="{relative_syntax}" />
    <script src="{relative_js}" defer></script>
    <title>{yaml_dict.get("title", "Default Title")}</title>
    """


def nav(configuration, pages, output_file, PUBLIC):
    core = configuration["core"]
    tree = build_tree(pages, PUBLIC)
    sidebar_tree = renderable_tree(tree, output_file)
    
    # Calculate Prev and Next page
    flat_pages = flatten_tree(tree)
    prev_page = None
    next_page = None
    
    current_index = -1
    for i, p in enumerate(flat_pages):
        if p["output_file"] == output_file:
            current_index = i
            break
            
    if current_index != -1:
        if current_index > 0:
            p_page = flat_pages[current_index - 1]
            prev_page = {
                "title": p_page["title"],
                "path": os.path.relpath(p_page["output_file"], start=output_file.parent).replace("\\", "/"),
            }
        if current_index < len(flat_pages) - 1:
            n_page = flat_pages[current_index + 1]
            next_page = {
                "title": n_page["title"],
                "path": os.path.relpath(n_page["output_file"], start=output_file.parent).replace("\\", "/"),
            }

    return core["site_title"], sidebar_tree, prev_page, next_page


def build_tree(pages, PUBLIC):
    tree = {}

    for page in pages:
        relative = page["output_file"].relative_to(PUBLIC)
        parts = relative.parts

        node = tree

        for part in parts[:-1]:
            node = node.setdefault(part, {})

        node.setdefault("__pages__", []).append(page)

    return tree


def get_min_order(node):
    min_ord = 99999
    if "__pages__" in node:
        for p in node["__pages__"]:
            min_ord = min(min_ord, p["order"])
    for key, value in node.items():
        if key != "__pages__":
            min_ord = min(min_ord, get_min_order(value))
    return min_ord


def renderable_tree(node, current_page):
    result = []

    # Sort pages by order, then title
    pages = node.get("__pages__", [])
    sorted_pages = sorted(pages, key=lambda p: (p["order"], p["title"].lower()))

    for page in sorted_pages:
        is_active = (page["output_file"] == current_page)
        result.append(
            {
                "type": "page",
                "title": page["title"],
                "path": os.path.relpath(
                    page["output_file"], start=current_page.parent
                ).replace("\\", "/"),
                "active": is_active,
            }
        )

    # Sort subfolders by their minimum page order, then alphabetically
    subfolders = [k for k in node.keys() if k != "__pages__"]
    sorted_folders = sorted(subfolders, key=lambda k: (get_min_order(node[k]), k.lower()))

    for key in sorted_folders:
        children = renderable_tree(node[key], current_page)
        has_active_child = any(child.get("active") or child.get("open") for child in children)
        result.append(
            {
                "type": "folder",
                "title": key.replace("_", " ").title(),
                "children": children,
                "open": has_active_child,
            }
        )

    return result


def flatten_tree(node):
    flat = []
    
    # Add sorted pages
    pages = node.get("__pages__", [])
    sorted_pages = sorted(pages, key=lambda p: (p["order"], p["title"].lower()))
    flat.extend(sorted_pages)
    
    # Add sorted subfolders
    subfolders = [k for k in node.keys() if k != "__pages__"]
    sorted_folders = sorted(subfolders, key=lambda k: (get_min_order(node[k]), k.lower()))
    
    for key in sorted_folders:
        flat.extend(flatten_tree(node[key]))
        
    return flat
