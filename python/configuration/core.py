import python.text_formatter as formatter
import questionary as q


def main():
    formatter.clear_screen()
    formatter.title("[red]SSG: Core configuration")
    urls = {}
    site_title = ""
    y = q.confirm("Do you want to publish your site?").ask()
    if y:
        y = q.confirm("Do you know the future domain name?").ask()
        while y:
            domain_name: str = q.text("Tell me").ask()
            if "/" not in domain_name:
                print("You need to add /'s")
            elif "http" not in domain_name:
                print("You need to add at least 'http'")
            elif domain_name[-1] != "/":
                print("The last letter should contain '/'")
            else:
                urls["self"] = domain_name
                break
        site_title = q.text("What's the site title?").ask()
    contact_email = ""
    y = q.confirm("Do you have a contact email").ask()
    while y:
        contact_email: str = q.text("Tell me").ask()
        if "@" not in contact_email:
            print("You need to add '@'s")
        else:
            break
    socials = []
    y = q.confirm("Do you use socials?").ask()
    while y:
        social: str = q.text("Tell me (enter to stop)").ask()
        if not social:
            break
        elif "/" not in social:
            print("You need to add /'s")
        elif "http" not in social:
            print("You need to add at least 'http'")
        elif social[-1] != "/":
            print("The last letter should contain '/'")
        else:
            socials.append(social)
    core = {
        "urls": urls,
        "site_title": site_title,
        "contact_email": contact_email,
        "socials": socials,
    }
    return core
