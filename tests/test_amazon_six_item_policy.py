import unittest
from pathlib import Path

class AmazonSixItemPolicyTests(unittest.TestCase):
    def test_blogger_menu_page_contains_exactly_six_owner_links(self):
        page = Path('blogger-pages/amazon-picks.html').read_text(encoding='utf-8')
        expected = {
            'https://amzn.to/4f0psll',
            'https://amzn.to/3XPGTiC',
            'https://amzn.to/4AOBrei',
            'https://amzn.to/48LAF5K',
            'https://amzn.to/4tmjVeR',
            'https://amzn.to/4j6yfVj',
        }
        self.assertEqual({url for url in expected if url in page}, expected)
        self.assertEqual(page.count('rel="sponsored nofollow noopener"'), 6)
        self.assertEqual(page.count('target="_blank"'), 6)

    def test_draft_engine_uses_amazon_picks_hub_not_unapproved_product(self):
        source = Path('trtt_787950_master.py').read_text(encoding='utf-8')
        self.assertIn('https://www.trttvoyage.com/p/amazon-picks.html', source)
        self.assertNotIn('https://amzn.to/4shg6Hn', source)
        self.assertIn('six approved items', source)

    def test_editorial_allowlist_has_six_items(self):
        policy = Path('docs/AMAZON-SIX-ITEM-RECOMMENDATION-POLICY.md').read_text(encoding='utf-8')
        self.assertEqual(policy.count('https://amzn.to/'), 6)

if __name__ == '__main__':
    unittest.main()
