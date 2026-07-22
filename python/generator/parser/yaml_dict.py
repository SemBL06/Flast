# Yaml parsen en doorsturen
import yaml


def main(yml: str):
    dict = yaml.load(yml, Loader=yaml.SafeLoader)
    sitemap = {}
    meta = {}
    for key, value in dict.items():
        if key != "sitemap":
            meta.setdefault(key, value)
    try:
        for key, value in dict["sitemap"].items():
            sitemap[key] = value
    except KeyError:
        pass  # Silent error, skip

    return meta, sitemap


if __name__ == "__main__":
    main()
