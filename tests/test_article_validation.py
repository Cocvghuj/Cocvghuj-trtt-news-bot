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


    def test_official_and_provider_domains_are_separate(self):
        self.assertTrue(main.is_official_source_url("https://www.gov.uk/"))
        self.assertFalse(main.is_provider_source_url("https://www.gov.uk/"))
        self.assertTrue(main.is_provider_source_url("https://www.airalo.com/"))
        self.assertFalse(main.is_official_source_url("https://www.airalo.com/"))

    def test_trusted_source_accepts_both_classes(self):
        self.assertTrue(main.is_trusted_source_url("https://www.gov.uk/"))
        self.assertTrue(main.is_trusted_source_url("https://www.airalo.com/"))

    def test_official_source_rejects_provider_and_http(self):
        self.assertFalse(main.is_official_source_url("https://airalo.com/"))
        self.assertFalse(main.is_official_source_url("http://gov.uk/"))

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

        with mock.patch.object(main.requests, "get", return_value=FakeResponse()):
            self.assertFalse(main.verify_source_url("https://europa.eu/source"))

    def test_rejects_non_html_response(self):
        class FakeResponse:
            status_code = 200
            url = "https://europa.eu/document"
            headers = {"Content-Type": "application/pdf"}
            def close(self):
                pass

        with mock.patch.object(main.requests, "get", return_value=FakeResponse()):
            self.assertFalse(main.verify_source_url("https://europa.eu/document"))


class EvidenceLedgerTests(unittest.TestCase):
    def test_rejects_missing_evidence_block(self):
        body = "<p>" + ("Useful content. " * 100) + "</p><h2>Sources</h2>"
        with self.assertRaises(RuntimeError):
            main.validate_article_response(article(body))

    def test_rejects_invalid_evidence_json(self):
        metadata = {
            "title": "Test article",
            "search_description": "A test description",
            "labels": ["Testing"],
            "permalink_slug": "test-article",
        }
        raw = "[METADATA]" + json.dumps(metadata) + "[/METADATA]"
        raw += "[EVIDENCE]{invalid json}[/EVIDENCE]"
        raw += "<p>" + ("Useful content. " * 100) + "</p>"
        with self.assertRaises(RuntimeError):
            main.validate_article_response(raw)

    def test_rejects_claim_mapped_to_non_inline_source(self):
        metadata = {
            "title": "Test article",
            "search_description": "A test description",
            "labels": ["Testing"],
            "permalink_slug": "test-article",
        }
        evidence = {"claims": [
            {"claim": "A factual claim with sufficient descriptive length.", "source_urls": ["https://example.com/not-cited"]}
            for _ in range(2)
        ]}
        raw = "[METADATA]" + json.dumps(metadata) + "[/METADATA]"
        raw += "[EVIDENCE]" + json.dumps(evidence) + "[/EVIDENCE]"
        raw += "<p>" + ("Useful content. " * 100) + "</p>"
        raw += "<h2>Sources</h2>"
        raw += '<a href="https://europa.eu/source">EU</a><a href="https://gov.uk/source">UK</a>'
        with self.assertRaises(RuntimeError):
            main.validate_article_response(raw)


class ArticleValidationTests(unittest.TestCase):
    def test_accepts_two_distinct_sources_in_sources_section(self):
        source_a = "https://europa.eu/source-a"
        source_b = "https://gov.uk/source-b"
        evidence = {"claims": [
            {"claim": "The first factual claim is supported by the EU source.", "source_urls": [source_a]},
            {"claim": "The second factual claim is supported by the UK source.", "source_urls": [source_b]},
        ]}
        body = (
            "<h2>Article</h2><p>" + ("Useful content. " * 100) + "</p>"
            + f'<p>First claim <a href="{source_a}">EU source</a></p>'
            + f'<p>Second claim <a href="{source_b}">UK source</a></p>'
            + "<h2>Sources</h2>"
            + f'<p><a href="{source_a}">EU</a></p>'
            + f'<p><a href="{source_b}">Government</a></p>'
        )
        raw = article(body).replace(
            "[/METADATA]",
            "[/METADATA][EVIDENCE]" + json.dumps(evidence) + "[/EVIDENCE]",
        )
        with mock.patch.object(main, "verify_source_url", return_value=True):
            result = main.validate_article_response(raw)
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


class DraftHistoryTests(unittest.TestCase):
    def test_topic_history_key_matches_topic_selection_key(self):
        topic = "Schengen Transit Checklist: Flight Safe Power Banks, SIMs and Rights"
        self.assertEqual(main.topic_history_key(topic), main.slugify(topic))

    def test_select_next_topic_skips_recorded_topic(self):
        topics = [
            {"topic": "First topic"},
            {"topic": "Second topic"},
        ]
        selected = main.select_next_topic(
            topics,
            [main.topic_history_key("First topic")],
        )
        self.assertEqual(selected["topic"], "Second topic")

    def test_select_next_topic_retries_first_when_all_topics_recorded(self):
        topics = [{"topic": "First topic"}, {"topic": "Second topic"}]
        history = [main.topic_history_key(item["topic"]) for item in topics]
        self.assertEqual(main.select_next_topic(topics, history), topics[0])

    def test_history_is_not_saved_without_confirmed_drafts(self):
        with mock.patch.object(main, "save_history") as save:
            recorded = main.record_topic_after_draft("A topic", [])
        self.assertFalse(recorded)
        save.assert_not_called()

    def test_history_saves_topic_key_after_confirmed_draft(self):
        drafts = [{"blog_name": "Test blog", "post_id": "123"}]
        with mock.patch.object(main, "save_history") as save:
            recorded = main.record_topic_after_draft("A topic", drafts)
        self.assertTrue(recorded)
        save.assert_called_once_with(main.topic_history_key("A topic"))


if __name__ == "__main__":
    unittest.main()
