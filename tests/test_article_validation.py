import json
import unittest

import main


def article(body):
    metadata = {
        "title": "Test article",
        "search_description": "A test description",
        "labels": ["Testing"],
        "permalink_slug": "test-article",
    }
    return "[METADATA]" + json.dumps(metadata) + "[/METADATA]" + body


class ArticleValidationTests(unittest.TestCase):
    def test_accepts_two_distinct_sources_in_sources_section(self):
        body = (
            "<h2>Article</h2><p>" + ("Useful content. " * 100) + "</p>"
            "<h2>Sources</h2>"
            '<p><a href="https://europa.eu/source-a">EU</a></p>'
            '<p><a href="https://transport.gov/source-b">Government</a></p>'
        )
        result = main.validate_article_response(article(body))
        self.assertEqual(result["meta"]["title"], "Test article")

    def test_rejects_missing_ai_output(self):
        with self.assertRaises(RuntimeError):
            main.validate_article_response("")

    def test_rejects_missing_sources_heading(self):
        body = "<p>" + ("Useful content. " * 100) + "</p>"
        with self.assertRaises(RuntimeError):
            main.validate_article_response(article(body))

    def test_rejects_duplicate_source_url(self):
        body = (
            "<p>" + ("Useful content. " * 100) + "</p><h2>Sources</h2>"
            '<a href="https://europa.eu/source">One</a>'
            '<a href="https://europa.eu/source">Repeated</a>'
        )
        with self.assertRaises(RuntimeError):
            main.validate_article_response(article(body))

    def test_ignores_affiliate_links_outside_sources_section(self):
        body = (
            '<a href="https://affiliate.example/link">Affiliate</a>'
            "<p>" + ("Useful content. " * 100) + "</p><h2>Sources</h2>"
            '<a href="https://europa.eu/source">Only one source</a>'
        )
        with self.assertRaises(RuntimeError):
            main.validate_article_response(article(body))

    def test_rejects_invalid_metadata(self):
        body = "<p>" + ("Useful content. " * 100) + "</p>"
        with self.assertRaises(RuntimeError):
            main.validate_article_response("[METADATA]{bad json}[/METADATA]" + body)


if __name__ == "__main__":
    unittest.main()
