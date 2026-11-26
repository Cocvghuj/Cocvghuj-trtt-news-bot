import os
import tempfile
import unittest
from pathlib import Path

from scripts.create_blogger_html_draft import ArticleInspector, validate_article


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
        with tempfile.TemporaryDirectory() as directory:
            previous = os.getcwd()
            try:
                os.chdir(directory)
                target = Path("blog/drafts/article.html")
                target.parent.mkdir(parents=True)
                target.write_text(VALID, encoding="utf-8")
                title, content = validate_article("blog/drafts/article.html")
                self.assertEqual(title, "Planning a Calm International Trip")
                self.assertEqual(content, VALID)
            finally:
                os.chdir(previous)

    def test_accepts_personal_reflection_without_affiliate_links_or_faq(self):
        reflection = """<!-- TRTT MAGIC - 787950 LOCKED -->
        <article style="max-width:780px;margin:0 auto;color:#11152D">
        <h1>Rise From Ashes</h1><p><a href="https://trttvoyage.com">TRTT Voyage</a></p>
        <h2>Acknowledge the chapter</h2><p>Reflection.</p>
        <h2>Choose one next step</h2><p>Reflection.</p>
        <h2>Keep moving with care</h2><p>Reflection.</p>
        <p>Disclosure: This is a personal reflection, not professional advice.</p>
        </article>
        """ + ("Personal reflection and practical next steps. " * 45)
        with tempfile.TemporaryDirectory() as directory:
            previous = os.getcwd()
            try:
                os.chdir(directory)
                target = Path("blog/drafts/reflection.html")
                target.parent.mkdir(parents=True)
                target.write_text(reflection, encoding="utf-8")
                title, _ = validate_article("blog/drafts/reflection.html")
                self.assertEqual(title, "Rise From Ashes")
            finally:
                os.chdir(previous)

    def test_inspector_rejects_unsafe_css_url(self):
        parser = ArticleInspector()
        parser.feed('<article><p style="background-image:url(https://evil.example/x)">Text</p></article>')
        self.assertTrue(any("Unsafe CSS" in error for error in parser.errors))

    def test_inspector_rejects_script_tag(self):
        parser = ArticleInspector()
        parser.feed("<article><script>alert(1)</script></article>")
        self.assertTrue(any("Disallowed HTML tag: script" in error for error in parser.errors))

    def test_inspector_rejects_event_handler_and_non_https_image(self):
        parser = ArticleInspector()
        parser.feed('<article><img src="http://example.com/a.jpg" alt="Travel"><p onclick="x()">Text</p></article>')
        self.assertTrue(any("Only absolute HTTPS src URLs" in error for error in parser.errors))
        self.assertTrue(any("Disallowed HTML attribute: onclick" in error for error in parser.errors))

    def test_validation_rejects_article_without_trtt_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            previous = os.getcwd()
            try:
                os.chdir(directory)
                target = Path("blog/drafts/article.html")
                target.parent.mkdir(parents=True)
                target.write_text(VALID.replace("787950", "000000"), encoding="utf-8")
                with self.assertRaisesRegex(RuntimeError, "marker 787950"):
                    validate_article("blog/drafts/article.html")
            finally:
                os.chdir(previous)


if __name__ == "__main__":
    unittest.main()
