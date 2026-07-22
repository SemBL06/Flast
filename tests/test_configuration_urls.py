import unittest

from python.configuration.urls import active_url, ensure_provider_urls, provider_urls


class ProviderUrlTests(unittest.TestCase):
    def test_self_url_has_priority(self):
        configuration = {
            "core": {
                "urls": {
                    "netlify": "https://site.netlify.app/",
                    "self": "https://docs.example.com/",
                }
            }
        }
        self.assertEqual("https://docs.example.com/", active_url(configuration))

    def test_first_provider_is_used_without_self(self):
        configuration = {
            "core": {
                "urls": {
                    "github-pages": "https://owner.github.io/project/",
                    "netlify": "https://site.netlify.app/",
                }
            }
        }
        self.assertEqual("https://owner.github.io/project/", active_url(configuration))

    def test_legacy_domain_is_migrated_to_self(self):
        configuration = {"core": {"domain_name": "https://docs.example.com"}}
        urls = ensure_provider_urls(configuration)
        self.assertEqual({"self": "https://docs.example.com/"}, urls)
        self.assertNotIn("domain_name", configuration["core"])
        self.assertEqual(urls, provider_urls(configuration))

    def test_legacy_netlify_domain_is_migrated_to_netlify(self):
        configuration = {"core": {"domain_name": "https://site.netlify.app/"}}
        self.assertEqual(
            {"netlify": "https://site.netlify.app/"},
            ensure_provider_urls(configuration),
        )

    def test_legacy_surge_domain_is_migrated_to_surge(self):
        configuration = {"core": {"domain_name": "https://site.surge.sh/"}}
        self.assertEqual(
            {"surge": "https://site.surge.sh/"},
            ensure_provider_urls(configuration),
        )
