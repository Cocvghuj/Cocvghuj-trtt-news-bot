import json
import unittest
from unittest import mock

import main


def article(body):
    metadata = {
        "title": "Test article",
        "search_description": "A test description",
        "labels": ["Testing"],
        "permalink_slug": "test-article",
    }
    return "[METADATA]" + json.dumps(metadata) + "[/METADATA]" + body


class TrustedSourceDomainTests(unittest.TestCase):
    def test_accepts_https_eu_official_domain(self):
        self.assertTrue(main.is_trusted_source_url("https://eur-lex.europa.eu/legal-content/EN/TXT/"))

    def test_accepts_subdomain_of_allowlisted_domain(self):
        self.assertTrue(main.is_trusted_source_url("https://www.gov.uk/"))

    def test_rejects_http_even_on_allowlisted_domain(self):
        self.assertFalse(main.is_trusted_source_url("http://europa.eu/example"))

    def test_rejects_lookalike_domain(self):
        self.assertFalse(main.is_trusted_source_url("https://europa.eu.example.com/fake"))

    def test_rejects_unlisted_domain(self):
        self.assertFalse(main.is_trusted_source_url("https://example.com/source"))


class SourceUrlReachabilityTests(unittest.TestCase):
    def test_rejects_untrusted_url_without_network(self):
        self.assertFalse(main.verify_source_url("https://example.com/source"))

    def test_rejects_non_https_url_without_network(self):
        self.assertFalse(main.verify_source_url("http://europa.eu/source"))

    def test_accepts_reachable_trusted_html_page(self):
        class FakeResponse:
            status_code = 200
            url = "https://europa.eu/source"
            headers = {"Content-Type": "text/html; charset=utf-8"}
            def close(self):
                pass

        with mock.patch.object(main.requests, "get", return_value=FakeResponse()):
            self.assertTrue(main.verify_source_url("https://europa.eu/source"))

    def test_rejects_redirect_to_untrusted_domain(self):
        class FakeResponse:
            status_code = 200
            url = "https://example.com/redirected"
            headers = {"Content-Type": "text/html"}
            def close(self):
                pass

        with unittest.mock.patch.object(main.requests, "get", return_value=FakeResponse()):
            self.assertFalse(main.verify_source_url("https://europa.eu/source"))

    def test_rejects_non_html_response(self):
        class FakeResponse:
            status_code = 200
            url = "https://europa.eu/document"
            headers = {"Content-Type": "application/pdf"}
            def close(self):
                pass

        with unittest.mock.patch.object(main.requests, "get", return_value=FakeResponse()):
            self.assertFalse(main.verify_source_url("https://europa.eu/document"))


class ArticleValidationTests(unittest.TestCase):
    def test_accepts_two_distinct_sources_in_sources_section(self):
        body = (
            "<h2>Article</h2><p>" + ("Useful content. " * 100) + "</p>"
            "<h2>Sources</h2>"
            '<p><a href="https://europa.eu/source-a">EU</a></p>'
            '<p><a href="https://gov.uk/source-b">Government</a></p>'
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
