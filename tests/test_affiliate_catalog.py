import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import config


ROOT = Path(__file__).resolve().parents[1]


class AffiliateAnchorParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.affiliate_ids = []
        self.affiliate_hrefs = {}

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        attributes = dict(attrs)
        affiliate_id = attributes.get("data-affiliate-id")
        if affiliate_id:
            self.affiliate_ids.append(affiliate_id)
            self.affiliate_hrefs[affiliate_id] = attributes.get("href", "")


class AffiliateCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / "affiliate-services.json").open(encoding="utf-8") as handle:
            cls.catalog = json.load(handle)
        cls.services = cls.catalog["services"]
        cls.by_id = {service["id"]: service for service in cls.services}

    def test_catalog_has_twenty_travelpayouts_and_one_amazon_entry(self):
        travelpayouts = [
            service for service in self.services
            if service["network"] == "travelpayouts"
        ]
        amazon = [
            service for service in self.services
            if service["network"] == "amazon-associates"
        ]
        self.assertEqual(len(travelpayouts), 20)
        self.assertEqual(len(amazon), 1)
        self.assertEqual(len(self.services), 21)

    def test_catalog_ids_and_urls_are_unique(self):
        ids = [service["id"] for service in self.services]
        urls = [service["url"] for service in self.services]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(urls), len(set(urls)))

    def test_travelpayouts_urls_use_the_configured_marker(self):
        for service in self.services:
            if service["network"] != "travelpayouts":
                continue
            parsed = urlparse(service["url"])
            self.assertTrue(parsed.hostname == "tpo.lv" or parsed.hostname.endswith(".tpo.lv"), parsed.hostname)
            self.assertEqual(parsed.scheme, "https")
            self.assertEqual(parse_qs(parsed.query).get("marker"), [self.catalog["marker"]])

    def test_python_config_loads_the_same_complete_catalog(self):
        self.assertEqual(len(config.AFFILIATE_SERVICES), len(self.services))
        self.assertEqual(
            [service["id"] for service in config.AFFILIATE_SERVICES],
            [service["id"] for service in self.services],
        )
        self.assertEqual(
            [service["url"] for service in config.AFFILIATE_SERVICES],
            [service["url"] for service in self.services],
        )

    def test_super_app_has_every_catalog_entry(self):
        parser = AffiliateAnchorParser()
        parser.feed((ROOT / "super-app.html").read_text(encoding="utf-8"))
        self.assertCountEqual(parser.affiliate_ids, self.by_id.keys())
        for affiliate_id, href in parser.affiliate_hrefs.items():
            self.assertTrue(href, affiliate_id)

    def test_main_store_links_are_catalog_entries(self):
        parser = AffiliateAnchorParser()
        parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertEqual(len(parser.affiliate_ids), 8)
        self.assertEqual(len(parser.affiliate_ids), len(set(parser.affiliate_ids)))
        for affiliate_id, href in parser.affiliate_hrefs.items():
            self.assertIn(affiliate_id, self.by_id)
            self.assertEqual(
                urlparse(href).path,
                urlparse(self.by_id[affiliate_id]["url"]).path,
            )

    def test_both_storefronts_load_the_shared_synchronizer(self):
        for filename in ("index.html", "super-app.html"):
            content = (ROOT / filename).read_text(encoding="utf-8")
            self.assertIn('src="/affiliate-links.js"', content)

    def test_synchronizer_uses_catalog_and_preserves_sub_ids(self):
        script = (ROOT / "affiliate-links.js").read_text(encoding="utf-8")
        self.assertIn('fetch("/affiliate-services.json"', script)
        self.assertIn('current.searchParams.get("sub_id")', script)
        self.assertIn('destination.searchParams.set("sub_id", subId)', script)
        self.assertIn('anchor.rel = "sponsored nofollow noopener noreferrer"', script)


if __name__ == "__main__":
    unittest.main()
