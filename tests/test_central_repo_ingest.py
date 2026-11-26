import unittest

from scripts.ingest_trtt_public_repo_drafts import (
    has_opt_in_marker, is_allowed_path, is_approved_legacy_source, local_draft_path,
)


class CentralRepoIngestTests(unittest.TestCase):
    def test_only_direct_html_files_in_allowed_directories(self):
        allowed = ["blogger-drafts", "blog/drafts"]
        self.assertTrue(is_allowed_path("blogger-drafts/story.html", allowed))
        self.assertTrue(is_allowed_path("blog/drafts/story.HTML", allowed))
        self.assertFalse(is_allowed_path("blogger-drafts/nested/story.html", allowed))
        self.assertFalse(is_allowed_path("posts/story.html", allowed))
        self.assertFalse(is_allowed_path("blogger-drafts/story.md", allowed))

    def test_requires_explicit_opt_in_comment(self):
        self.assertTrue(has_opt_in_marker("<!-- TRTT_BLOGGER_DRAFT: true -->"))
        self.assertTrue(has_opt_in_marker("<!-- trtt_blogger_draft: TRUE -->"))
        self.assertFalse(has_opt_in_marker("TRTT_BLOGGER_DRAFT: true"))
        self.assertFalse(has_opt_in_marker("<!-- TRTT_BLOGGER_DRAFT: false -->"))

    def test_legacy_approval_is_pinned_to_exact_repo_path_and_blob(self):
        approvals = {
            "Cocvghuj/trtt-rise-from-ashes-studio": {
                "blogger-drafts/rise-from-ashes.html": "db641a51d2feb0ad2fb212522fd8aa07b18a3e4f"
            }
        }
        self.assertTrue(is_approved_legacy_source(
            "Cocvghuj/trtt-rise-from-ashes-studio",
            "blogger-drafts/rise-from-ashes.html",
            "db641a51d2feb0ad2fb212522fd8aa07b18a3e4f",
            approvals,
        ))
        self.assertFalse(is_approved_legacy_source(
            "Cocvghuj/trtt-rise-from-ashes-studio",
            "blogger-drafts/rise-from-ashes.html",
            "changed-blob-sha",
            approvals,
        ))
        self.assertFalse(is_approved_legacy_source(
            "Cocvghuj/trtt-muse-gift",
            "blogger-drafts/rise-from-ashes.html",
            "db641a51d2feb0ad2fb212522fd8aa07b18a3e4f",
            approvals,
        ))

    def test_local_staging_name_is_stable_and_safe(self):
        first = local_draft_path("Cocvghuj/trtt-muse-gift", "blogger-drafts/story.html")
        second = local_draft_path("Cocvghuj/trtt-muse-gift", "blogger-drafts/story.html")
        self.assertEqual(first, second)
        self.assertEqual(first.parent.as_posix().split("/")[-2:], ["blog", "drafts"])
        self.assertTrue(first.name.endswith(".html"))
        self.assertNotIn("/", first.name)


if __name__ == "__main__":
    unittest.main()
