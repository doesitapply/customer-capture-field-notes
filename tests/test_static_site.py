import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class StaticSiteTests(unittest.TestCase):
    def test_cta_map_is_a_printable_public_only_worksheet(self):
        page = (ROOT / "cta-map.html").read_text(encoding="utf-8")
        self.assertIn('id="cta-map-worksheet"', page)
        self.assertIn("CTA Map Worksheet", page)
        self.assertIn("@media print", page)
        self.assertIn("What happens if clicked?", page)
        self.assertIn("possible friction", page.lower())

    def test_cta_map_does_not_add_capture_or_payment_surface(self):
        page = (ROOT / "cta-map.html").read_text(encoding="utf-8").lower()
        for forbidden in ("<form", "<script", "<iframe", "href=\"https://buy.stripe.com", "href=\"https://paypal.me"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, page)

    def test_growth_trail_links_to_cta_map(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="cta-map.html"', homepage)


if __name__ == "__main__":
    unittest.main()
