import json
import re
import unittest
from pathlib import Path

import trtt_787950_master as engine


class DraftOnlyPolicyTests(unittest.TestCase):
    def test_engine_never_requests_live_publication(self):
        source = Path("trtt_787950_master.py").read_text(encoding="utf-8")
        self.assertIn("isDraft=True", source)
        self.assertNotRegex(source, r"isDraft\s*=\s*False")
        self.assertNotIn(".publish(", source)

    def test_workflow_wrapper_does_not_override_draft_policy(self):
        source = Path("scripts/publish_news.py").read_text(encoding="utf-8")
        self.assertNotIn("isDraft", source)
        self.assertNotIn(".publish(", source)
        self.assertIn("engine.main()", source)

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
            "date": "2026-11-06", "price": "€19",
            "airline": "Ryanair", "isDraft": True,
        }
        content = engine.build_content(route, "6 November 2026")
        for required in (
            "<img src=\"https://images.unsplash.com/",
            "787950 LOCKED", "EC 261/2004", "Ghost-SIM = eSIM",
            "Sanluri", "Sardinia", "Cagliari", "Bergamo",
            "https://cocvghuj-trtt-news-bot.vercel.app",
            "amzn.to/4shg6Hn?marker=787950",
            "aviasales.tpo.lv/Fb8U9yav?marker=787950",
            "klook.tpo.lv/TWKnemhz?marker=787950",
            "airalo.tpo.lv/ZZoQC7Mz?marker=787950",
            "gettransfer.tpo.lv/1u8zRU5s?marker=787950",
        ):
            with self.subTest(required=required):
                self.assertIn(required, content)
        self.assertNotIn("EC Regulation 261/2004", content)
        self.assertIn("TRTT VoyageHub Showroom", content)
        self.assertGreater(content.index("TRTT VoyageHub Showroom"), content.index("Useful travel tools"))
        self.assertGreaterEqual(engine._plain_word_count(content), 400)
        self.assertNotIn("xxxxx", content)

    def test_daily_route_queue_has_one_dated_draft_route(self):
        queue = json.loads(Path("news/queue/latest.json").read_text(encoding="utf-8"))
        self.assertEqual(queue["version"], "2026-11-06")
        self.assertEqual(queue["batch_size"], 1)
        self.assertIs(queue["isDraft"], True)
        self.assertEqual(queue["require_marker"], "787950 LOCKED")
        self.assertEqual(len(queue["routes"]), 1)
        self.assertEqual(queue["routes"][0]["date"], "2026-11-06")
        self.assertIs(queue["routes"][0]["isDraft"], True)

    def test_daily_focus_varies(self):
        self.assertNotEqual(engine.daily_focus(1), engine.daily_focus(2))


if __name__ == "__main__":
    unittest.main()
