import json
import os
import io
import tempfile
import unittest
from datetime import datetime, timedelta
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock
from zoneinfo import ZoneInfo

import trtt_787950_master as engine


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


def make_queue(today):
    route = {
        "from": "Cagliari",
        "to": "Bergamo",
        "iata_from": "CAG",
        "iata_to": "BGY",
        "date": today.date().isoformat(),
        "price": "€19 (unverified queue lead)",
        "airline": "Verify operating carrier",
        "image_url": "https://images.unsplash.com/photo-test-route?w=800",
        "category": "Flight News",
        "isDraft": True,
    }
    days = []
    for offset in range(30):
        day = (today.date() + timedelta(days=offset)).isoformat()
        if offset == 0:
            days.append({"date": day, "status": "ready", "route": route})
        else:
            days.append({"date": day, "status": "pending", "route": None})
    return {
        "version": today.date().isoformat(),
        "start_date": days[0]["date"],
        "end_date": days[-1]["date"],
        "batch_size": 1,
        "isDraft": True,
        "require_marker": "787950 LOCKED",
        "days": days,
    }


class DraftEngineRegressionTests(unittest.TestCase):
    def test_empty_queue_fails_closed_instead_of_inventing_a_route(self):
        fixed_now = datetime(2026, 11, 7, 0, 1, tzinfo=ZoneInfo("Europe/Rome"))
        with tempfile.TemporaryDirectory() as directory:
            queue_path = Path(directory) / "30days.json"
            queue_path.write_text(json.dumps({
                "isDraft": True,
                "batch_size": 1,
                "require_marker": "787950 LOCKED",
                "days": [],
            }), encoding="utf-8")
            with (
                mock.patch.object(engine, "QUEUE_FILE", queue_path),
                mock.patch.object(engine, "publish_date", return_value=fixed_now),
            ):
                with self.assertRaisesRegex(AssertionError, "exactly 30 dated entries"):
                    engine._load_today_route()

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

    def test_main_creates_exactly_one_verified_draft_for_the_ready_queue_entry(self):
        fixed_now = datetime(2026, 11, 7, 12, 0, tzinfo=ZoneInfo("Europe/Rome"))
        service = FakeService()
        with tempfile.TemporaryDirectory() as directory:
            queue_path = Path(directory) / "30days.json"
            history_path = Path(directory) / "drafted_history.txt"
            queue_path.write_text(json.dumps(make_queue(fixed_now)), encoding="utf-8")
            history_path.write_text("", encoding="utf-8")
            env = {
                "BLOGGER_BLOG_ID": "main-blog",
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

            self.assertIn("CONFIRMED: One Blogger DRAFT created", output.getvalue())
            self.assertEqual(len(service.posts_api.insert_calls), 1)
            call = service.posts_api.insert_calls[0]
            self.assertEqual(call["blogId"], "main-blog")
            self.assertIs(call["isDraft"], True)
            self.assertIn("2026-11-07 | Cagliari to Bergamo | 2026-11-07", history_path.read_text(encoding="utf-8"))

    def test_daily_guard_skips_a_second_draft_for_the_same_date(self):
        fixed_now = datetime(2026, 11, 7, 12, 0, tzinfo=ZoneInfo("Europe/Rome"))
        with tempfile.TemporaryDirectory() as directory:
            queue_path = Path(directory) / "30days.json"
            history_path = Path(directory) / "drafted_history.txt"
            queue_path.write_text(json.dumps(make_queue(fixed_now)), encoding="utf-8")
            history_path.write_text("2026-11-07 | Cagliari to Bergamo | 2026-11-07\n", encoding="utf-8")
            env = {
                "BLOGGER_BLOG_ID": "main-blog",
                "BLOGGER_CLIENT_ID": "client",
                "BLOGGER_CLIENT_SECRET": "secret",
                "BLOGGER_REFRESH_TOKEN": "refresh",
            }
            with (
                mock.patch.object(engine, "QUEUE_FILE", queue_path),
                mock.patch.object(engine, "HISTORY_FILE", history_path),
                mock.patch.object(engine, "publish_date", return_value=fixed_now),
                mock.patch.object(engine, "build", side_effect=AssertionError("Must not connect to Blogger")),
                mock.patch.dict(os.environ, env, clear=True),
            ):
                output = io.StringIO()
                with redirect_stdout(output):
                    self.assertEqual(engine.main(), 0)
            self.assertIn("SKIP: A daily draft was already confirmed", output.getvalue())

    def test_live_duplicate_is_rejected_and_never_changed(self):
        service = FakeService()
        service.posts_api.items["main-blog"] = [{
            "id": "live-1",
            "title": "Existing dated title",
            "status": "LIVE",
        }]
        with self.assertRaisesRegex(AssertionError, "refusing unsafe action"):
            engine._create_or_recover_draft(
                service, "main-blog", "Existing dated title", "<p>Draft</p>", "Flight News"
            )
        self.assertEqual(service.posts_api.insert_calls, [])


if __name__ == "__main__":
    unittest.main()
