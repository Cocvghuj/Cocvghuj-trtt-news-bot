import json
import re
import unittest
from datetime import date, timedelta
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
            "date": "2026-11-07", "price": "€19",
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
        self.assertIn("TRTT Voyage Showroom", content)
        self.assertGreater(content.index("TRTT Voyage Showroom"), content.index("Useful travel tools"))
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

    def test_daily_route_queue_has_30_contiguous_draft_days(self):
        queue = json.loads(Path("news/queue/30days.json").read_text(encoding="utf-8"))
        self.assertEqual(queue["batch_size"], 1)
        self.assertIs(queue["isDraft"], True)
        self.assertEqual(queue["require_marker"], "787950 LOCKED")
        days = queue["days"]
        self.assertEqual(len(days), 30)
        start = date.fromisoformat(queue["start_date"])
        expected_dates = [(start + timedelta(days=offset)).isoformat() for offset in range(30)]
        self.assertEqual([item["date"] for item in days], expected_dates)
        self.assertEqual(days[-1]["date"], queue["end_date"])
        today = engine.target_date()
        matches = [item for item in days if item["date"] == today]
        self.assertEqual(len(matches), 1, "The active 30-day queue must include today's date exactly once.")
        self.assertEqual(matches[0]["status"], "ready")
        self.assertIs(matches[0]["route"]["isDraft"], True)

    def test_content_accepts_a_non_default_https_image(self):
        route = {
            "from": "Cagliari", "to": "Rome",
            "iata_from": "CAG", "iata_to": "FCO",
            "date": "2026-11-07", "price": "Unverified lead",
            "airline": "Verify operating carrier", "isDraft": True,
            "image_url": "https://images.unsplash.com/photo-custom-route-image?w=800",
        }
        content = engine.build_content(route)
        self.assertIn('<img src="https://images.unsplash.com/photo-custom-route-image?w=800"', content)

    def test_daily_focus_varies(self):
        self.assertNotEqual(engine.daily_focus(1), engine.daily_focus(2))


if __name__ == "__main__":
    unittest.main()
