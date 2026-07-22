import unittest
from pathlib import Path
import subprocess
from unittest.mock import patch

from python.deployment.github_pages import GitHubPagesProvider


class GitHubPagesProviderTests(unittest.TestCase):
    def setUp(self):
        self.provider = GitHubPagesProvider()

    def test_project_pages_url_uses_repository_path(self):
        self.assertEqual(
            "https://SemBL06.github.io/Flast/",
            self.provider._default_pages_url("SemBL06/Flast"),
        )

    def test_user_pages_url_has_no_repository_path(self):
        self.assertEqual(
            "https://SemBL06.github.io/",
            self.provider._default_pages_url("SemBL06/SemBL06.github.io"),
        )

    def test_only_gh_pages_root_is_managed(self):
        self.assertTrue(
            self.provider._uses_managed_branch(
                {"source": {"branch": "gh-pages", "path": "/"}}
            )
        )
        self.assertFalse(
            self.provider._uses_managed_branch(
                {"source": {"branch": "main", "path": "/docs"}}
            )
        )

    def test_empty_success_response_enables_pages(self):
        with patch.object(
            self.provider,
            "_run",
            return_value=subprocess.CompletedProcess([], 0, stdout="", stderr=""),
        ):
            self.assertEqual({}, self.provider._create_pages_site(Path("."), "gh", "owner/repo"))
