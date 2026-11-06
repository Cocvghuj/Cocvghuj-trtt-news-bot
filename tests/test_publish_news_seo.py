import unittest

from scripts.publish_news import _build_search_description


class BloggerSearchDescriptionTests(unittest.TestCase):
    def test_description_is_route_specific_and_uses_iata_codes(self):
        route = {
            "from": "Cagliari",
            "to": "Bergamo",
            "iata_from": "CAG",
            "iata_to": "BGY",
            "date": "2026-11-07",
        }
        description = _build_search_description(route)
        self.assertIn("Cagliari (CAG)", description)
        self.assertIn("Bergamo (BGY)", description)
        self.assertIn("7 November 2026", description)
        self.assertIn("airport transfers", description)
        self.assertLessEqual(len(description), 160)
        self.assertGreaterEqual(len(description), 120)

    def test_description_does_not_promote_unverified_queue_fare(self):
        route = {
            "from": "Milan",
            "to": "Cagliari",
            "iata_from": "MXP",
            "iata_to": "CAG",
            "date": "2026-11-08",
            "price": "€19",
            "airline": "Wizz Air",
        }
        description = _build_search_description(route)
        self.assertNotIn("€19", description)
        self.assertNotIn("Wizz Air", description)
        self.assertLessEqual(len(description), 160)


if __name__ == "__main__":
    unittest.main()
