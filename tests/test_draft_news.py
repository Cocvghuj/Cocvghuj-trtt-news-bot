import unittest
from scripts.draft_news import (
    require_latin_english,
    validate_metadata,
    validate_source_url,
    add_vercel_reference,
    MARKER,
    FIXED,
    DEFAULT_PWA_URL
)

class TestDraftNewsValidation(unittest.TestCase):
    def test_require_latin_english_valid(self):
        require_latin_english("Flight delays in Rome: EC 261 compensation guide 2026!", "Title")

    def test_require_latin_english_invalid(self):
        with self.assertRaises(ValueError):
            require_latin_english("ফ্লাইট বিলম্বের ক্ষতিপূরণ", "Title")
        with self.assertRaises(ValueError):
            require_latin_english("Компенсация за задержку рейса", "Title")

    def test_validate_metadata_valid(self):
        meta = {
            "title": "Cheap Flights from Rome to Sardinia: 2026 Travel Guide",
            "search_description": "Discover how to book cheap flights from Rome to Sardinia with verified transit tips, airport transfers, and 5G eSIM connectivity recommendations.",
            "labels": ["Travel News", "Europe Travel", "Sanluri", "FlightScoutPro"]
        }
        validated = validate_metadata(meta)
        self.assertEqual(validated["title"], meta["title"])
        self.assertEqual(validated["search_description"], meta["search_description"])
        self.assertEqual(len(validated["labels"]), 4)

    def test_validate_metadata_title_too_long(self):
        meta = {
            "title": "A" * 101,
            "search_description": "Valid description length between 120 and 160 characters to ensure Google compliant search snippets without truncation issues.",
            "labels": ["Travel"]
        }
        with self.assertRaises(ValueError):
            validate_metadata(meta)

    def test_validate_metadata_description_bounds(self):
        with self.assertRaises(ValueError):
            validate_metadata({
                "title": "Valid Title",
                "search_description": "Too short description.",
                "labels": ["Travel"]
            })
        with self.assertRaises(ValueError):
            validate_metadata({
                "title": "Valid Title",
                "search_description": "A" * 161,
                "labels": ["Travel"]
            })

    def test_validate_metadata_labels_filtering(self):
        meta = {
            "title": "Valid Flight Title",
            "search_description": "Discover how to book cheap flights from Rome to Sardinia with verified transit tips, airport transfers, and 5G eSIM connectivity recommendations.",
            "labels": ["Travel", "travel", "Europe", "Sanluri", "Flights", "Bonus", "Extra"]
        }
        validated = validate_metadata(meta)
        self.assertEqual(len(validated["labels"]), 5)
        self.assertEqual(validated["labels"], ["Travel", "Europe", "Sanluri", "Flights", "Bonus"])

    def test_validate_source_url(self):
        valid_url = "https://www.enac.gov.it/en/passengers"
        self.assertEqual(validate_source_url(valid_url), valid_url)

        with self.assertRaises(ValueError):
            validate_source_url("http://insecure-domain.com")
        with self.assertRaises(ValueError):
            validate_source_url("https://user:pass@domain.com")
        with self.assertRaises(ValueError):
            validate_source_url("not-a-valid-url")

    def test_add_vercel_reference_injection(self):
        content = "Original article body about European flight logistics."
        result = add_vercel_reference(content, "https://cocvghuj-trtt-news-bot.vercel.app")
        self.assertIn("Plan Your Trip From Sanluri", result)
        self.assertIn(f"marker={MARKER}", result)
        self.assertIn(f"kiwitaxi.tp.st/{FIXED}", result)
        self.assertIn("hotel-bernini.it", result)

    def test_add_vercel_reference_idempotent(self):
        url = "https://cocvghuj-trtt-news-bot.vercel.app"
        content = f"Original article body with {url} already included."
        result = add_vercel_reference(content, url)
        self.assertEqual(content, result)

if __name__ == "__main__":
    unittest.main()
