import python.text_formatter as formatter
import questionary as q


def main():
    formatter.clear_screen()
    formatter.title("[red]SSG: Configuration of SEO")
    enable_sitemap = q.confirm("Include sitemap (auto generated)").ask()
    enable_robots = q.confirm("Enable robot.txt?").ask()
    if enable_robots:
        all_robots = q.confirm("All robots are allowed?").ask()  # Disallow: / (refuse)
        crawl_delay = q.text("What is the crawl delay?").ask()  # Crawl-delay: 10
        restricted_pages = []

        while True:
            answer = q.text("Restricted pages for robots? (Enter to stop)").ask()
            if answer:
                restricted_pages.append(answer)
            else:
                break
    seo = {
        "enable_robots": enable_robots,
        "all_robots_allowed": all_robots,
        "crawl_delay": crawl_delay,
        "enable_sitemap": enable_sitemap,
        "restricted_pages": restricted_pages,
    }
    formatter.title("[green]SSG: Completed SEO Wizard")
    return seo
