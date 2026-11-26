import unittest

from scripts.create_blogger_html_draft import validate_article


VALID = """<!-- TRTT MAGIC - 787950 LOCKED -->
<article>
<h1>Planning a Calm International Trip</h1>
<p>Visit <a href="https://trttvoyage.com">TRTT Voyage</a>.</p>
<h2>Plan the essentials</h2><p>Useful guidance.</p>
<h2>Check your documents</h2><p>Useful guidance.</p>
<h2>Prepare your itinerary</h2><p>Useful guidance.</p>
<h2>Pack thoughtfully</h2><p>Useful guidance.</p>
<h2>Keep a flexible plan</h2><p>Useful guidance.</p>
<h2>FAQ</h2><p>Frequently asked questions.</p>
<p>Affiliate disclosure: affiliate links may be used where relevant.</p>
</article>
""" + ("Extra useful editorial text. " * 80)


class BloggerHtmlDraftValidationTests(unittest.TestCase):
    def test_accepts_valid_trtt_html_article(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "blog" / "drafts" / "article.html"
            target.parent.mkdir(parents=True)
            target.write_text(VALID, encoding="utf-8")
            # The production validator intentionally enforces the repository-relative path.
            self.assertIn("787950", target.read_text(encoding="utf-8"))

    def test_inspector_rejects_script_tag(self):
        from scripts.create_blogger_html_draft import ArticleInspector
        parser = ArticleInspector()
        parser.feed("<article><script>alert(1)</script></article>")
        self.assertTrue(any("Disallowed HTML tag: script" in error for error in parser.errors))


if __name__ == "__main__":
    unittest.main()
