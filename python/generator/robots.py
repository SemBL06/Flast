from python.configuration.urls import active_url


def main(configuration):
    robots_configuration: dict = configuration.get("SEO", None)
    robots_text = ""
    if robots_configuration:
        if robots_configuration["enable_robots"]:
            if robots_configuration.get("all_robots_allowed", True):
                robots_text += "User-agent: *\n"
                robots_text += "Disallow:\n"
            else:
                robots_text += "User-agent:\n"
                robots_text += "Disallow: /\n"
            if robots_configuration.get("crawl_delay", "0") != "0":
                robots_text += "Crawl-delay: 10\n"
            if robots_configuration.get("enable_sitemap", True):
                robots_text += f"Sitemap: {active_url(configuration)}sitemap.xml\n"
            for disallowed_file in robots_configuration.get("restricted_pages", []):
                robots_text += f"Disallow: /{disallowed_file}\n"
    return robots_text
