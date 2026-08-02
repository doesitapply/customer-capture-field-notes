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

    def test_public_path_check_is_a_printable_public_only_checklist(self):
        page = (ROOT / "public-path-checklist.html").read_text(encoding="utf-8")
        self.assertIn('id="public-path-checklist"', page)
        self.assertIn("One-Page Public Path Check", page)
        self.assertIn("@media print", page)
        self.assertIn("Immediate handoff", page)
        self.assertIn("Public-only and observational", page)

    def test_public_path_check_does_not_add_capture_or_payment_surface(self):
        page = (ROOT / "public-path-checklist.html").read_text(encoding="utf-8").lower()
        for forbidden in ("<form", "<script", "<iframe", "href=\"https://buy.stripe.com", "href=\"https://paypal.me"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, page)

    def test_growth_trail_links_to_public_path_check(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="public-path-checklist.html"', homepage)

    def test_public_teardown_template_is_printable_and_evidence_first(self):
        page = (ROOT / "public-teardown-template.html").read_text(encoding="utf-8")
        self.assertIn('id="public-only-teardown-template"', page)
        self.assertIn("Public-Only Teardown Template", page)
        self.assertIn("@media print", page)
        self.assertIn("Evidence ledger", page)
        self.assertIn("Owner questions before a bigger change", page)
        self.assertIn("possible friction", page.lower())

    def test_public_teardown_template_does_not_add_capture_or_payment_surface(self):
        page = (ROOT / "public-teardown-template.html").read_text(encoding="utf-8").lower()
        for forbidden in ("<form", "<script", "<iframe", "href=\"https://buy.stripe.com", "href=\"https://paypal.me"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, page)

    def test_growth_trail_links_to_public_teardown_template(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="public-teardown-template.html"', homepage)

    def test_cta_clarity_scorecard_is_printable_and_public_only(self):
        page = (ROOT / "cta-clarity-scorecard.html").read_text(encoding="utf-8")
        self.assertIn('id="cta-clarity-scorecard"', page)
        self.assertIn("CTA Clarity Scorecard", page)
        self.assertIn("Score: ____ / 6", page)
        self.assertIn("@media print", page)
        self.assertIn("Public-only and observational", page)
        for forbidden in ("<form", "<script", "<iframe", "href=\"https://buy.stripe.com", "href=\"https://paypal.me"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, page.lower())

    def test_growth_trail_and_cta_map_link_to_cta_clarity_scorecard(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        cta_map = (ROOT / "cta-map.html").read_text(encoding="utf-8")
        self.assertIn('href="cta-clarity-scorecard.html"', homepage)
        self.assertIn('href="cta-clarity-scorecard.html"', cta_map)

    def test_cta_choice_matrix_is_printable_public_only_and_linked(self):
        page = (ROOT / "cta-choice-matrix.html").read_text(encoding="utf-8")
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        cta_map = (ROOT / "cta-map.html").read_text(encoding="utf-8")
        scorecard = (ROOT / "cta-clarity-scorecard.html").read_text(encoding="utf-8")
        self.assertIn('id="cta-choice-matrix"', page)
        self.assertIn("CTA Choice Matrix", page)
        self.assertIn("Primary action or distinct action?", page)
        self.assertIn("Public-only and observational", page)
        self.assertIn("@media print", page)
        for forbidden in ("<form", "<script", "<iframe", "href=\"https://buy.stripe.com", "href=\"https://paypal.me"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, page.lower())
        self.assertIn('href="cta-choice-matrix.html"', homepage)
        self.assertIn('href="cta-choice-matrix.html"', cta_map)
        self.assertIn('href="cta-choice-matrix.html"', scorecard)

    def test_public_cta_handoff_example_is_printable_and_boundaried(self):
        page = (ROOT / "public-cta-handoff-example.html").read_text(encoding="utf-8")
        self.assertIn('id="public-cta-handoff-example"', page)
        self.assertIn("Fictional example; not a teardown of a real business.", page)
        self.assertIn("Possible friction to check", page)
        self.assertIn("Ask one owner question before a larger change", page)
        self.assertIn("@media print", page)

    def test_public_cta_handoff_example_does_not_add_capture_or_payment_surface(self):
        page = (ROOT / "public-cta-handoff-example.html").read_text(encoding="utf-8").lower()
        for forbidden in ("<form", "<script", "<iframe", "href=\"https://buy.stripe.com", "href=\"https://paypal.me"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, page)

    def test_growth_trail_links_to_public_cta_handoff_example(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="public-cta-handoff-example.html"', homepage)


if __name__ == "__main__":
    unittest.main()
