import json
import os
import io
import tempfile
import unittest
from datetime import datetime
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

import trtt_787950_master as engine
import api.trtt_787950_master as status_api
from http.server import BaseHTTPRequestHandler


class FakeRequest:
    def __init__(self, result):
        self.result = result

    def execute(self):
        return self.result


class FakePosts:
    def __init__(self):
        self.items = {}
        self.insert_calls = []

    def list(self, **kwargs):
        return FakeRequest({"items": list(self.items.get(kwargs["blogId"], []))})

    def insert(self, blogId, body, isDraft):
        self.insert_calls.append({"blogId": blogId, "body": body, "isDraft": isDraft})
        post = {
            "id": f"{blogId}-draft-{len(self.items.get(blogId, [])) + 1}",
            "title": body["title"],
            "status": "DRAFT",
        }
        self.items.setdefault(blogId, []).append(post)
        return FakeRequest(post)

    def get(self, blogId, postId):
        post = next(item for item in self.items.get(blogId, []) if item["id"] == postId)
        return FakeRequest(dict(post))


class FakeService:
    def __init__(self):
        self.posts_api = FakePosts()

    def posts(self):
        return self.posts_api


class DraftEngineRegressionTests(unittest.TestCase):
    def test_vercel_python_api_uses_supported_http_handler_and_exports_engine(self):
        self.assertTrue(issubclass(status_api.handler, BaseHTTPRequestHandler))
        self.assertTrue(callable(status_api.build_content))
        self.assertTrue(callable(status_api.build))
        self.assertTrue(callable(status_api.find_duplicate_post))
        self.assertTrue(callable(status_api.main))

    def test_empty_queue_generates_today_fallback_instead_of_zero_skip(self):
        with tempfile.TemporaryDirectory() as directory:
            queue_path = Path(directory) / "latest.json"
            queue_path.write_text(json.dumps({
                "version": "2026-11-07",
                "batch_size": 1,
                "isDraft": True,
                "require_image": True,
                "require_marker": "787950 LOCKED",
                "routes": [],
            }), encoding="utf-8")
            fixed_now = datetime(2026, 11, 7, 0, 1, tzinfo=ZoneInfo("Europe/Rome"))
            with (
                mock.patch.object(engine, "QUEUE_FILE", queue_path),
                mock.patch.object(engine, "publish_date", return_value=fixed_now),
            ):
                _, route = engine._load_today_route()
            self.assertEqual(route["from"], "Cagliari")
            self.assertEqual(route["to"], "Bergamo")
            self.assertEqual(route["date"], "2026-11-07")
            self.assertIs(route["isDraft"], True)

    def test_history_keeps_latest_12_and_shifts_oldest(self):
        with tempfile.TemporaryDirectory() as directory:
            history_path = Path(directory) / "drafted_history.txt"
            initial = [f"route-{index}" for index in range(12)]
            history_path.write_text("\n".join(initial) + "\n", encoding="utf-8")
            with mock.patch.object(engine, "HISTORY_FILE", history_path):
                engine.append_history("new-route")
                result = engine.load_history()
            self.assertEqual(result, initial[1:] + ["new-route"])
            self.assertEqual(len(result), 12)

    def test_today_override_ignores_history_and_creates_both_drafts(self):
        route = {
            "from": "Cagliari", "to": "Bergamo",
            "iata_from": "CAG", "iata_to": "BGY",
            "date": "2026-11-07", "price": "€19",
            "airline": "Ryanair", "isDraft": True,
        }
        queue = {
            "version": "2026-11-07",
            "generated_at": "2026-11-07T22:50:00+01:00",
            "routes": [route],
            "batch_size": 1,
            "isDraft": True,
            "require_image": True,
            "require_marker": "787950 LOCKED",
        }
        fixed_now = datetime(2026, 11, 7, 23, 0, tzinfo=ZoneInfo("Europe/Rome"))
        service = FakeService()
        with tempfile.TemporaryDirectory() as directory:
            queue_path = Path(directory) / "latest.json"
            history_path = Path(directory) / "drafted_history.txt"
            queue_path.write_text(json.dumps(queue), encoding="utf-8")
            history_path.write_text("Cagliari to Bergamo | 2026-11-07\n", encoding="utf-8")
            env = {
                "BLOGGER_BLOG_ID": "main-blog",
                "FLIGHTSCOUTPRO_BLOG_ID": "partner-blog",
                "BLOGGER_CLIENT_ID": "client",
                "BLOGGER_CLIENT_SECRET": "secret",
                "BLOGGER_REFRESH_TOKEN": "refresh",
            }
            with (
                mock.patch.object(engine, "QUEUE_FILE", queue_path),
                mock.patch.object(engine, "HISTORY_FILE", history_path),
                mock.patch.object(engine, "publish_date", return_value=fixed_now),
                mock.patch.object(engine, "build", return_value=service),
                mock.patch.dict(os.environ, env, clear=True),
            ):
                output = io.StringIO()
                with redirect_stdout(output):
                    self.assertEqual(engine.main(), 0)
            self.assertIn("Republish allowed - today's date override", output.getvalue())
            self.assertIn("SUCCESS: Draft created - trttnews24bd - Post ID: main-blog-draft-1", output.getvalue())
            self.assertIn("SUCCESS: Draft created - flightscoutpro - Post ID: partner-blog-draft-1", output.getvalue())
            self.assertEqual(len(service.posts_api.insert_calls), 2)
            self.assertTrue(all(call["isDraft"] is True for call in service.posts_api.insert_calls))
            self.assertEqual(
                {call["blogId"] for call in service.posts_api.insert_calls},
                {"main-blog", "partner-blog"},
            )
            self.assertIn("Cagliari to Bergamo | 2026-11-07", history_path.read_text(encoding="utf-8"))

    def test_live_duplicate_is_rejected_and_never_changed(self):
        service = FakeService()
        service.posts_api.items["main-blog"] = [{
            "id": "live-1",
            "title": "Existing dated title",
            "status": "LIVE",
        }]
        with self.assertRaisesRegex(AssertionError, "refusing unsafe action"):
            engine._create_or_recover_draft(
                service, "main-blog", "Existing dated title", "<p>Draft</p>"
            )
        self.assertEqual(service.posts_api.insert_calls, [])


if __name__ == "__main__":
    unittest.main()
