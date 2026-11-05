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

    def test_content_contains_editorial_requirements_and_footer_order(self):
        content = engine.build_content("Rome to Cagliari", "5 November 2026")
        for required in (
            "ghost-esim", "787950", "photo-1501785888041-af3ef285b470",
            "aviasales.tpo.lv", "klook.tpo.lv", "airalo.tpo.lv",
            "gettransfer.tpo.lv", "amzn.to/4shg6Hn", "EC Regulation 261/2004",
            "Published:", "Updated:", "Sanluri, Sardinia, Italy",
            "Live App:", "Make every journey feel effortless.", "editorial planning guide",
        ):
            with self.subTest(required=required):
                self.assertIn(required, content)
        self.assertGreater(content.index("Live App:"), content.index("Marker 787950 Locked"))
        self.assertNotIn("xxxxx", content)
        self.assertIn("tpo.lv/Fb8U9yav", content)
        self.assertIn("tpo.lv/TWKnemhz", content)
        self.assertIn("tpo.lv/ZZoQC7Mz", content)
        self.assertIn("tpo.lv/1u8zRU5s", content)
        self.assertIn("automated assistance", content)
        self.assertGreater(len(re.findall(r"\b[\w'-]+\b", content)), 100)

    def test_daily_route_queue_has_exactly_one_route(self):
        routes = json.loads(Path("news/queue/latest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(routes), 1)

    def test_daily_focus_varies(self):
        self.assertNotEqual(engine.daily_focus(1), engine.daily_focus(2))


if __name__ == "__main__":
    unittest.main()
