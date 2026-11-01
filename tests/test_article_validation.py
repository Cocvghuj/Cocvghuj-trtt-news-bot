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

    def test_history_not_saved_when_any_blog_target_failed(self):
        outcomes = [
            {"blog_name": "Main", "post_id": "123", "status": "created"},
            {"blog_name": "Partner", "status": "failed", "error": "API unavailable"},
        ]
        with mock.patch.object(main, "save_history") as save:
            recorded = main.record_topic_after_draft("A topic", outcomes)
        self.assertFalse(recorded)
        save.assert_not_called()

    def test_history_saved_when_all_blog_targets_created_drafts(self):
        outcomes = [
            {"blog_name": "Main", "post_id": "123", "status": "created"},
            {"blog_name": "Partner", "post_id": "456", "status": "created"},
        ]
        with mock.patch.object(main, "save_history") as save:
            recorded = main.record_topic_after_draft("A topic", outcomes)
        self.assertTrue(recorded)
        save.assert_called_once_with(main.topic_history_key("A topic"))

    def test_existing_duplicate_counts_as_confirmed_blog_coverage(self):
        outcomes = [
            {"blog_name": "Main", "post_id": "123", "status": "created"},
            {"blog_name": "Partner", "post_id": "789", "status": "already_exists"},
        ]
        self.assertTrue(main.all_blog_targets_accounted_for(outcomes))

    def test_failed_or_missing_post_id_does_not_count_as_coverage(self):
        outcomes = [
            {"blog_name": "Main", "post_id": "123", "status": "created"},
            {"blog_name": "Partner", "status": "already_exists"},
        ]
        self.assertFalse(main.all_blog_targets_accounted_for(outcomes))

    def test_empty_blog_outcomes_do_not_mark_topic_complete(self):
        self.assertFalse(main.all_blog_targets_accounted_for([]))

    def test_legacy_history_entries_are_preserved_without_guessed_mapping(self):
        legacy = [
            "claim-up-to-600-flight-delay-ec-261",
            "how-to-claim-600-euro-flight-delay-ec261",
        ]
        loaded = main.apply_history_migrations(legacy, {})
        self.assertEqual(loaded, legacy)
        self.assertNotIn(main.topic_history_key(main.TOPIC_POOL[0]["topic"]), loaded)

    def test_explicit_legacy_mapping_adds_topic_key_without_deleting_legacy_key(self):
        legacy_key = "claim-up-to-600-flight-delay-ec-261"
        topic_key = main.topic_history_key(main.TOPIC_POOL[0]["topic"])
        loaded = main.apply_history_migrations(
            [legacy_key],
            {legacy_key: topic_key},
        )
        self.assertIn(legacy_key, loaded)
        self.assertIn(topic_key, loaded)

    def test_mapping_for_absent_legacy_key_is_ignored(self):
        topic_key = main.topic_history_key(main.TOPIC_POOL[0]["topic"])
        loaded = main.apply_history_migrations(
            ["some-other-legacy-entry"],
            {"missing-legacy-entry": topic_key},
        )
        self.assertEqual(loaded, ["some-other-legacy-entry"])

    def test_invalid_migration_map_type_does_not_change_history(self):
        legacy = ["legacy-entry"]
        self.assertEqual(main.apply_history_migrations(legacy, []), legacy)



class DuplicateTextNormalizationTests(unittest.TestCase):
    def test_decodes_html_entities_before_comparing_titles(self):
        self.assertEqual(
            main.normalize_article_text("Flight &amp; Travel&nbsp;Guide"),
            "flight & travel guide",
        )

    def test_strips_markup_and_normalizes_whitespace(self):
        self.assertEqual(
            main.normalize_article_text("<p>Flight</p>   <strong>Delay</strong>\nClaim"),
            "flight delay claim",
        )

    def test_decodes_numeric_and_named_entities(self):
        self.assertEqual(
            main.normalize_article_text("Tom&#39;s&nbsp;Aviation &quot;Guide&quot;"),
            "tom's aviation \"guide\"",
        )


class UnicodeDuplicateNormalizationTests(unittest.TestCase):
    def test_bengali_text_is_preserved_and_casefolded_only_by_lowercase(self):
        self.assertEqual(
            main.normalize_article_text("বাংলাদেশের বিমানযাত্রী অধিকার"),
            "বাংলাদেশের বিমানযাত্রী অধিকার",
        )

    def test_bengali_canonical_composition_matches_decomposed_text(self):
        composed = "ড়"
        decomposed = "ড\u09bc"
        self.assertEqual(
            main.normalize_article_text(composed),
            main.normalize_article_text(decomposed),
        )

    def test_bengali_vowel_signs_and_joiners_are_preserved(self):
        text = "কি ক্\\u200dষ"
        self.assertEqual(main.normalize_article_text(text), text)

    def test_unicode_normalization_does_not_remove_distinct_marks(self):
        self.assertNotEqual(
            main.normalize_article_text("কি"),
            main.normalize_article_text("কী"),
        )


class DuplicatePaginationTests(unittest.TestCase):
    class FakeRequest:
        def __init__(self, response):
            self.response = response
        def execute(self):
            if isinstance(self.response, Exception):
                raise self.response
            return self.response

    class FakePosts:
        def __init__(self, responses):
            self.responses = list(responses)
            self.calls = []
        def list(self, **kwargs):
            self.calls.append(kwargs)
            if not self.responses:
                raise AssertionError("Unexpected extra page request")
            return DuplicatePaginationTests.FakeRequest(self.responses.pop(0))

    class FakeService:
        def __init__(self, responses):
            self.posts_api = DuplicatePaginationTests.FakePosts(responses)
        def posts(self):
            return self.posts_api

    def test_duplicate_found_on_second_page(self):
        service = self.FakeService([
            {"items": [{"title": "Unrelated", "content": "x"}], "nextPageToken": "page-2"},
            {"items": [{"id": "existing-2", "title": "Test article", "content": "body"}]},
        ])
        duplicate = main.find_duplicate_post(service, "blog-1", "Test article", "new body")
        self.assertEqual(duplicate["id"], "existing-2")
        self.assertEqual(len(service.posts_api.calls), 2)
        self.assertEqual(service.posts_api.calls[1]["pageToken"], "page-2")
        self.assertEqual(service.posts_api.calls[0]["status"], ["LIVE", "DRAFT"])

    def test_refuses_to_claim_no_duplicate_when_scan_limit_reached(self):
        service = self.FakeService([
            {"items": [], "nextPageToken": "page-2"},
            {"items": [], "nextPageToken": "page-3"},
        ])
        with mock.patch.object(main, "DUPLICATE_CHECK_MAX_PAGES", 2):
            with self.assertRaisesRegex(RuntimeError, "Duplicate check could not be completed"):
                main.find_duplicate_post(service, "blog-1", "Test article", "new body")
        self.assertEqual(len(service.posts_api.calls), 2)

    def test_returns_none_only_after_last_page(self):
        service = self.FakeService([
            {"items": [], "nextPageToken": "page-2"},
            {"items": []},
        ])
        self.assertIsNone(main.find_duplicate_post(service, "blog-1", "Test article", "new body"))
        self.assertEqual(len(service.posts_api.calls), 2)

    def test_api_failure_on_first_page_fails_closed_with_blog_context(self):
        service = self.FakeService([OSError("temporary Blogger API outage")])
        with self.assertRaisesRegex(
            RuntimeError,
            r"Duplicate check could not be completed for blog blog-1: temporary Blogger API outage",
        ):
            main.find_duplicate_post(service, "blog-1", "Test article", "new body")
        self.assertEqual(len(service.posts_api.calls), 1)

    def test_api_failure_on_later_page_does_not_report_no_duplicate(self):
        service = self.FakeService([
            {"items": [], "nextPageToken": "page-2"},
            OSError("page token request failed"),
        ])
        with self.assertRaisesRegex(
            RuntimeError,
            r"Duplicate check could not be completed for blog blog-2: page token request failed",
        ):
            main.find_duplicate_post(service, "blog-2", "Test article", "new body")
        self.assertEqual(len(service.posts_api.calls), 2)
        self.assertEqual(service.posts_api.calls[1]["pageToken"], "page-2")


    def test_same_title_with_different_html_entity_format_is_duplicate(self):
        service = self.FakeService([
            {"items": [{"id": "existing-title", "title": "Flight &amp; Travel Guide", "content": "older content"}]},
        ])
        duplicate = main.find_duplicate_post(
            service, "blog-1", "Flight & Travel Guide", "different article content"
        )
        self.assertEqual(duplicate["id"], "existing-title")

    def test_same_body_with_different_html_formatting_is_duplicate(self):
        body = ("Flight delay compensation rules and passenger rights explained clearly. " * 10).strip()
        html_body = "<article><p>" + body + "</p></article>"
        service = self.FakeService([
            {"items": [{"id": "existing-body", "title": "Older headline", "content": html_body}]},
        ])
        duplicate = main.find_duplicate_post(service, "blog-1", "New headline", body)
        self.assertEqual(duplicate["id"], "existing-body")

    def test_article_body_inside_enterprise_wrapper_is_duplicate_with_changed_title(self):
        body = ("A detailed guide to passenger rights and flight compensation. " * 15).strip()
        wrapped_body = (
            '<div class="fs-article-wrap"><div class="site-header">Shared layout text</div>'
            '<div class="article-body"><p>' + body + '</p></div>'
            '<div class="affiliate-footer">Shared footer text</div></div>'
        )
        service = self.FakeService([
            {"items": [{"id": "wrapped-duplicate", "title": "Older headline", "content": wrapped_body}]},
        ])
        duplicate = main.find_duplicate_post(
            service, "blog-1", "Updated headline", body
        )
        self.assertEqual(duplicate["id"], "wrapped-duplicate")

    def test_near_duplicate_body_inside_enterprise_wrapper_is_detected(self):
        original = ("A detailed guide to passenger rights and flight compensation. " * 15).strip()
        changed = original.replace("detailed guide", "practical guide", 1)
        wrapped_body = (
            '<div class="fs-article-wrap"><div class="article-body"><p>'
            + original
            + '</p></div><div class="footer">Shared site footer</div></div>'
        )
        service = self.FakeService([
            {"items": [{"id": "wrapped-near-duplicate", "title": "Older headline", "content": wrapped_body}]},
        ])
        duplicate = main.find_duplicate_post(
            service, "blog-1", "Different headline", changed
        )
        self.assertEqual(duplicate["id"], "wrapped-near-duplicate")


    def test_mixed_bengali_english_title_matches_html_and_entity_variant(self):
        stored_title = "ফ্লাইট Delay &amp; Compensation — Europe ২০২৬"
        new_title = "ফ্লাইট Delay & Compensation — Europe ২০২৬"
        service = self.FakeService([
            {"items": [{"id": "mixed-title", "title": stored_title, "content": "short old body"}]},
        ])
        duplicate = main.find_duplicate_post(
            service, "blog-1", new_title, "a different short article body"
        )
        self.assertEqual(duplicate["id"], "mixed-title")

    def test_mixed_bengali_english_article_matches_markup_variant(self):
        sentence = (
            "বিমান বিলম্ব হলে passenger rights ও compensation rules "
            "জানুন before submitting an airline claim. "
        )
        plain_body = sentence * 12
        html_body = "<article><p>" + (sentence.replace("&", "&amp;") * 12) + "</p></article>"
        service = self.FakeService([
            {"items": [{"id": "mixed-body", "title": "Older mixed-language title", "content": html_body}]},
        ])
        duplicate = main.find_duplicate_post(
            service, "blog-1", "A different headline", plain_body
        )
        self.assertEqual(duplicate["id"], "mixed-body")


if __name__ == "__main__":
    unittest.main()


class DraftWorkflowFailClosedTests(unittest.TestCase):
    def test_missing_blogger_oauth_credentials_raise_instead_of_successful_skip(self):
        with (
            mock.patch.object(main, "BLOGGER_CLIENT_ID", None),
            mock.patch.object(main, "BLOGGER_CLIENT_SECRET", None),
            mock.patch.object(main, "BLOGGER_REFRESH_TOKEN", None),
        ):
            with self.assertRaisesRegex(RuntimeError, "OAuth credentials are incomplete"):
                main.create_drafts_on_blogs("Title", "<p>body</p>", {"labels": []})

    def test_missing_target_blog_ids_raise_instead_of_successful_skip(self):
        with (
            mock.patch.object(main, "BLOGGER_CLIENT_ID", "client"),
            mock.patch.object(main, "BLOGGER_CLIENT_SECRET", "secret"),
            mock.patch.object(main, "BLOGGER_REFRESH_TOKEN", "refresh"),
            mock.patch.object(main, "BLOGGER_BLOG_ID", None),
            mock.patch.object(main, "FLIGHTSCOUTPRO_BLOG_ID", None),
            mock.patch.object(main, "PARTNER_BLOG_IDS", ""),
            mock.patch.object(main.os.path, "exists", return_value=False),
        ):
            with self.assertRaisesRegex(RuntimeError, "No Blogger target blog IDs"):
                main.create_drafts_on_blogs("Title", "<p>body</p>", {"labels": []})

    def test_incomplete_draft_run_raises_and_does_not_advance_history(self):
        article_data = {
            "meta": {"title": "Test", "labels": ["Test"]},
            "content": "<p>Article</p>",
        }
        with (
            mock.patch.object(main, "load_history", return_value=[]),
            mock.patch.object(main, "fetch_unsplash_photo", return_value={"url": "https://example.com/image.jpg", "author": "Test", "alt": "Test"}),
            mock.patch.object(main, "generate_article_with_metadata", return_value=article_data),
            mock.patch.object(main, "build_enterprise_html", return_value="<p>HTML</p>"),
            mock.patch.object(main, "create_drafts_on_blogs", return_value=[]),
            mock.patch.object(main, "record_topic_after_draft") as record,
        ):
            with self.assertRaisesRegex(RuntimeError, "Draft workflow incomplete"):
                main.main()
        record.assert_called_once_with(main.TOPIC_POOL[0]["topic"], [])

    def test_missing_generated_article_raises_instead_of_successful_skip(self):
        with (
            mock.patch.object(main, "load_history", return_value=[]),
            mock.patch.object(main, "fetch_unsplash_photo", return_value={"url": "https://example.com/image.jpg", "author": "Test", "alt": "Test"}),
            mock.patch.object(main, "generate_article_with_metadata", return_value=None),
        ):
            with self.assertRaisesRegex(RuntimeError, "Article generation returned no validated content"):
                main.main()


if __name__ == "__main__":
    unittest.main()
