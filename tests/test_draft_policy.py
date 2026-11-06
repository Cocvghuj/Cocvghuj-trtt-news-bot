import json
import re
import unittest
from pathlib import Path

import trtt_787950_master as engine


class DraftOnlyPolicyTests(unittest.TestCase):
    def test_engine_never_requests_live_publication(self):
        source = Path("trtt_787950_master.py").read_text(encoding="utf-8")
        self.assertNotIn("service.posts()", source)
        publisher = Path("scripts/publish_news.py").read_text(encoding="utf-8")
        self.assertIn("isDraft=True", publisher)
        self.assertIn("service.posts().insert(", publisher)
        self.assertIn("service.posts().get(", publisher)
        self.assertNotRegex(source, r"isDraft\s*=\s*False")
        self.assertNotIn(".publish(", source)

    def test_workflow_wrapper_does_not_override_draft_policy(self):
        source = Path("scripts/publish_news.py").read_text(encoding="utf-8")
        self.assertIn("service.posts().insert(", source)
        self.assertIn("service.posts().get(", source)
        self.assertIn("Status: {status} - DRAFT Verified", source)
        self.assertNotIn(".publish(", source)

    def test_legacy_sync_script_is_draft_only(self):
        source = Path("scripts/sync_blogger_content.py").read_text(encoding="utf-8")
        self.assertIn("isDraft=True", source)
        self.assertNotIn("isDraft=False", source)
        self.assertNotIn("isDraft = False", source)
        self.assertNotIn("publish=True", source)
        self.assertNotIn("resource.delete(", source)

    def test_content_contains_exact_editorial_requirements(self):
        route = {
            "from": "Cagliari", "to": "Bergamo",
            "iata_from": "CAG", "iata_to": "BGY",
            "date": "2026-11-07", "price": "€19",
            "airline": "Ryanair", "isDraft": True,
        }
        content = engine.build_content(route, "6 November 2026")
        for required in (
            "<img src=\"https://images.unsplash.com/",
            "787950 LOCKED", "EC 261/2004", "Ghost-SIM = eSIM",
            "Sanluri", "Sardinia", "Cagliari", "Bergamo",
            "https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950",
        ):
            with self.subTest(required=required):
                self.assertIn(required, content)
        self.assertNotIn("EC Regulation 261/2004", content)
        self.assertFalse(engine.contains_direct_affiliate_links(content))
        self.assertIn("TRTT VoyageHub Showroom", content)
        self.assertEqual(content.count('href="https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950"'), 1)
        self.assertGreater(content.index("TRTT VoyageHub Showroom"), content.index("Useful travel tools"))
        self.assertGreaterEqual(engine._plain_word_count(content), 800)
        self.assertNotIn("xxxxx", content)

    def test_vaults_are_frozen_hex_encoded_and_byte_identical(self):
        source = Path("roksana-vault.js").read_text(encoding="utf-8")
        final = Path("roksana-vault-final.js").read_text(encoding="utf-8")
        self.assertEqual(source.encode("utf-8"), final.encode("utf-8"))
        self.assertIn("Object.freeze(", source)
        self.assertIn('markerHex: "373837393530"', source)
        self.assertNotIn("xxxxx", source.lower())
        self.assertNotRegex(source, r"Roksana|Ripu")
        self.assertIn("Revenue Protection Protocol", source)
        self.assertIn('markerHex: "373837393530"', source)

    def test_daily_route_queue_has_one_dated_draft_route(self):
        queue = json.loads(Path("news/queue/latest.json").read_text(encoding="utf-8"))
        self.assertEqual(queue["version"], "2026-11-07")
        self.assertEqual(queue["batch_size"], 1)
        self.assertIs(queue["isDraft"], True)
        self.assertEqual(queue["require_marker"], "787950 LOCKED")
        self.assertEqual(len(queue["routes"]), 1)
        self.assertEqual(queue["routes"][0]["date"], "2026-11-07")
        self.assertIs(queue["routes"][0]["isDraft"], True)

    def test_daily_focus_varies(self):
        self.assertNotEqual(engine.daily_focus(1), engine.daily_focus(2))


if __name__ == "__main__":
    unittest.main()


class FakeRequest:
    def __init__(self, callback):
        self.callback = callback

    def execute(self):
        return self.callback()


class FakeBloggerPosts:
    def __init__(self, existing=None, readback_status="DRAFT", list_error=None):
        self.existing = existing or []
        self.readback_status = readback_status
        self.list_error = list_error
        self.calls = []
        self.insert_count = 0

    def list(self, **kwargs):
        self.calls.append(("list", kwargs))
        def execute():
            if self.list_error:
                raise self.list_error
            return {"items": self.existing}
        return FakeRequest(execute)

    def insert(self, **kwargs):
        self.calls.append(("insert", kwargs))
        self.insert_count += 1
        return FakeRequest(lambda: {"id": "new-post-1"})

    def get(self, **kwargs):
        self.calls.append(("get", kwargs))
        return FakeRequest(lambda: {"id": kwargs["postId"], "status": self.readback_status})


class FakeBloggerService:
    def __init__(self, posts):
        self._posts = posts

    def posts(self):
        return self._posts


class PublisherSafetyTests(unittest.TestCase):
    def setUp(self):
        import main
        from scripts import publish_news
        self.context = main
        self.publisher = publish_news
        self.title = "Cagliari to Bergamo flight guide - 2026-11-07 - TRTT"
        self.topic_key = "cagliari-bergamo-2026-11-07"
        self.content = "<p>" + ("Useful verified travel guidance. " * 30) + "</p>"

    def test_publisher_has_one_authoritative_create_or_verify_definition(self):
        import ast
        tree = ast.parse(Path("scripts/publish_news.py").read_text(encoding="utf-8"))
        definitions = [
            node for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == "create_or_verify_draft"
        ]
        self.assertEqual(len(definitions), 1)

    def test_insert_is_draft_and_immediately_read_back_verified(self):
        posts = FakeBloggerPosts()
        service = FakeBloggerService(posts)
        result, created = self.publisher.create_or_verify_draft(
            service, "blog-1", self.title, self.content,
            topic_key=self.topic_key, context=self.context,
        )
        self.assertTrue(created)
        self.assertEqual(result["status"], "DRAFT")
        self.assertEqual(posts.insert_count, 1)
        insert_call = next(call for call in posts.calls if call[0] == "insert")
        self.assertIs(insert_call[1]["isDraft"], True)
        self.assertIn(self.context.topic_draft_marker(self.topic_key), insert_call[1]["body"]["content"])
        self.assertEqual([call[0] for call in posts.calls], ["list", "insert", "get"])

    def test_retry_recovers_existing_draft_without_second_insert(self):
        marker = self.context.topic_draft_marker(self.topic_key)
        posts = FakeBloggerPosts(existing=[{
            "id": "existing-draft", "status": "DRAFT",
            "title": self.title, "content": self.content + marker,
        }])
        result, created = self.publisher.create_or_verify_draft(
            FakeBloggerService(posts), "blog-1", self.title, self.content,
            topic_key=self.topic_key, context=self.context,
        )
        self.assertFalse(created)
        self.assertEqual(result["id"], "existing-draft")
        self.assertEqual(posts.insert_count, 0)
        self.assertEqual([call[0] for call in posts.calls], ["list", "get"])

    def test_matching_live_post_fails_closed_without_insert(self):
        marker = self.context.topic_draft_marker(self.topic_key)
        posts = FakeBloggerPosts(existing=[{
            "id": "live-post", "status": "LIVE",
            "title": self.title, "content": self.content + marker,
        }])
        with self.assertRaisesRegex(AssertionError, "is LIVE"):
            self.publisher.create_or_verify_draft(
                FakeBloggerService(posts), "blog-1", self.title, self.content,
                topic_key=self.topic_key, context=self.context,
            )
        self.assertEqual(posts.insert_count, 0)

    def test_server_readback_rejects_non_draft_status(self):
        posts = FakeBloggerPosts(readback_status="LIVE")
        with self.assertRaisesRegex(RuntimeError, "expected DRAFT"):
            self.publisher.create_or_verify_draft(
                FakeBloggerService(posts), "blog-1", self.title, self.content,
                topic_key=self.topic_key, context=self.context,
            )
        self.assertEqual(posts.insert_count, 1)
        self.assertEqual([call[0] for call in posts.calls], ["list", "insert", "get"])

    def test_duplicate_scan_failure_prevents_insert(self):
        posts = FakeBloggerPosts(list_error=TimeoutError("Blogger list timed out"))
        with self.assertRaisesRegex(RuntimeError, "Duplicate check could not be completed"):
            self.publisher.create_or_verify_draft(
                FakeBloggerService(posts), "blog-1", self.title, self.content,
                topic_key=self.topic_key, context=self.context,
            )
        self.assertEqual(posts.insert_count, 0)

    def test_duplicate_scan_page_overflow_prevents_insert(self):
        class PaginatedPosts(FakeBloggerPosts):
            def list(self, **kwargs):
                self.calls.append(("list", kwargs))
                return FakeRequest(lambda: {"items": [], "nextPageToken": "next"})
        posts = PaginatedPosts()
        with self.assertRaisesRegex(RuntimeError, "exceeded 1 pages"):
            self.publisher.find_duplicate_post(
                FakeBloggerService(posts), "blog-1", self.title, self.content,
                max_pages=1, context=self.context,
            )
        self.assertEqual(posts.insert_count, 0)


class WorkflowDeploymentSafetyTests(unittest.TestCase):
    def setUp(self):
        import main
        from scripts import publish_news
        self.context = main
        self.publisher = publish_news
        self.title = "Cagliari to Bergamo flight guide - 2026-11-07 - TRTT"
        self.topic_key = "cagliari-bergamo-2026-11-07"
        self.content = "<p>" + ("Useful verified travel guidance. " * 30) + "</p>"

    def test_manual_draft_workflow_cannot_push_to_main(self):
        workflow = Path(".github/workflows/trtt-english-news-drafts.yml").read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("contents: read", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertNotIn("contents: write", workflow)
        self.assertNotIn("git push", workflow)
        self.assertNotIn("git commit", workflow)
        self.assertIn("actions/upload-artifact@v4", workflow)

    def test_manual_draft_workflow_is_main_only_and_serialized(self):
        workflow = Path(".github/workflows/trtt-english-news-drafts.yml").read_text(encoding="utf-8")
        self.assertIn("if: github.ref == 'refs/heads/main'", workflow)
        self.assertIn("group: trtt-daily-draft", workflow)
        self.assertIn("cancel-in-progress: false", workflow)

    def test_no_workflow_step_invokes_live_publish_api(self):
        workflow = Path(".github/workflows/trtt-english-news-drafts.yml").read_text(encoding="utf-8")
        self.assertIn("python scripts/publish_news.py", workflow)
        self.assertNotIn("posts().publish", workflow)
        self.assertNotIn("isDraft=False", workflow)


    def test_ambiguous_insert_timeout_is_recovered_without_duplicate_insert(self):
        class AcceptedThenTimedOutPosts(FakeBloggerPosts):
            def insert(self, **kwargs):
                self.calls.append(("insert", kwargs))
                self.insert_count += 1
                def accepted_but_response_lost():
                    self.existing.append({
                        "id": "new-post-1",
                        "status": "DRAFT",
                        "title": kwargs["body"]["title"],
                        "content": kwargs["body"]["content"],
                    })
                    raise TimeoutError("Blogger accepted insert but response timed out")
                return FakeRequest(accepted_but_response_lost)

        posts = AcceptedThenTimedOutPosts()
        service = FakeBloggerService(posts)
        with self.assertRaisesRegex(TimeoutError, "response timed out"):
            self.publisher.create_or_verify_draft(
                service, "blog-1", self.title, self.content,
                topic_key=self.topic_key, context=self.context,
            )
        result, created = self.publisher.create_or_verify_draft(
            service, "blog-1", self.title, self.content,
            topic_key=self.topic_key, context=self.context,
        )
        self.assertFalse(created)
        self.assertEqual(result["id"], "new-post-1")
        self.assertEqual(posts.insert_count, 1)

    def test_readback_without_post_id_fails_closed(self):
        class MissingIdPosts(FakeBloggerPosts):
            def get(self, **kwargs):
                self.calls.append(("get", kwargs))
                return FakeRequest(lambda: {"status": "DRAFT"})

        posts = MissingIdPosts()
        with self.assertRaisesRegex(RuntimeError, "returned no post ID"):
            self.publisher.create_or_verify_draft(
                FakeBloggerService(posts), "blog-1", self.title, self.content,
                topic_key=self.topic_key, context=self.context,
            )
        self.assertEqual(posts.insert_count, 1)


    def test_vercel_production_build_requires_explicit_owner_opt_in(self):
        build = Path("build.js").read_text(encoding="utf-8")
        self.assertIn("process.env.VERCEL_ENV === 'production'", build)
        self.assertIn("TRTT_PRODUCTION_DEPLOY_APPROVED !== 'true'", build)
        self.assertIn("TRTT Production Lock: deployment blocked", build)
        workflow = Path(".github/workflows/article-validation-tests.yml").read_text(encoding="utf-8")
        self.assertIn("Verify unauthorized Vercel Production builds are blocked", workflow)
        self.assertIn("VERCEL_ENV=production node build.js", workflow)


class BloggerHubOnlyTests(unittest.TestCase):
    def test_multi_blog_template_strips_direct_affiliate_links(self):
        import main
        source = Path("main.py").read_text(encoding="utf-8")
        self.assertIn("strip_direct_affiliate_links(article_data[\"content\"])", source)
        self.assertIn("Blogger gadget: Vercel hub only", source)
        self.assertIn('href=\"{VERCEL_HUB_URL}\"', source)
        self.assertNotIn("airhelp_link =", source)
        self.assertNotIn("aviasales_link =", source)
        sample = (
            '<p><a href=\"https://airhelp.tpo.lv/3ItXS0E4?marker=787950\">AirHelp</a></p>'
            '<p>https://amzn.to/4shg6Hn?marker=787950</p>'
            '<p><a href=\"https://europa.eu/youreurope/citizens/travel/passenger-rights/air/index_en.htm\">EU rights</a></p>'
        )
        cleaned = main.strip_direct_affiliate_links(sample)
        self.assertNotIn("airhelp.tpo.lv", cleaned)
        self.assertNotIn("amzn.to", cleaned)
        self.assertIn("europa.eu", cleaned)

    def test_blogger_vault_menu_renders_only_vercel_hub(self):
        source = Path("roksana-vault.js").read_text(encoding="utf-8")
        self.assertIn("var BLOGGER_MENU_TOOLS = Object.freeze([", source)
        self.assertIn("var ACTIVE_MENU_TOOLS = IS_BLOGGER_HOST ? BLOGGER_MENU_TOOLS : MENU_TOOLS;", source)
        self.assertIn('url:\"https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950\"', source)
        self.assertIn("ACTIVE_MENU_TOOLS.forEach(function(t)", source)
