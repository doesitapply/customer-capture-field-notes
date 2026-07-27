import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from public_evidence_pack import EvidencePackError, PublicPageParser, assert_public_url, render_markdown, write_packet


class PublicEvidencePackTests(unittest.TestCase):
    def test_parser_extracts_bounded_public_signals(self):
        parser = PublicPageParser()
        parser.feed(
            """<html><head><title>Example</title><meta name='description' content='A sample page'></head>
            <body><h1>Ship proof</h1><a href='/privacy'>Privacy Policy</a><a href='/terms'>Terms</a>
            <form><label for='email'>Email</label><input id='email' type='email'></form>
            Cookie preferences</body></html>"""
        )
        signals = parser.signals()
        self.assertEqual(signals.title, "Example")
        self.assertEqual(signals.headings_h1, ["Ship proof"])
        self.assertTrue(signals.privacy_link_detected)
        self.assertTrue(signals.terms_link_detected)
        self.assertTrue(signals.cookie_text_detected)
        self.assertEqual(signals.forms, 1)
        self.assertEqual(signals.visible_input_controls, 1)
        self.assertEqual(signals.labels_with_for, 1)

    def test_private_urls_are_refused_before_network_access(self):
        with self.assertRaises(EvidencePackError):
            assert_public_url("http://127.0.0.1/private")
        with self.assertRaises(EvidencePackError):
            assert_public_url("file:///private/record")

    def test_legal_cues_are_checked_beyond_the_public_link_sample(self):
        parser = PublicPageParser()
        parser.feed("".join(f"<a href='/page-{index}'>Page {index}</a>" for index in range(45)))
        parser.feed("<a href='/terms'>Terms of Service</a>")
        self.assertTrue(parser.signals().terms_link_detected)

    def test_packet_writes_json_and_markdown(self):
        packet = {
            "tool": "Public Evidence Pack",
            "version": "0.1",
            "observed_at_utc": "2026-07-27T00:00:00+00:00",
            "boundary": "Read-only.",
            "retrieval": {
                "requested_url": "https://example.com",
                "final_url": "https://example.com",
                "status_code": 200,
                "content_type": "text/html",
                "bytes_read": 12,
                "sha256": "abc",
            },
            "http_header_observations": {"x-content-type-options": "nosniff"},
            "page_observations": {
                "title": "Example",
                "meta_description": None,
                "headings_h1": ["Hello"],
                "forms": 0,
                "visible_input_controls": 0,
                "labels_with_for": 0,
                "privacy_link_detected": True,
                "terms_link_detected": True,
                "cookie_text_detected": False,
                "links_sample": [],
            },
            "not_checked": ["Anything private"],
        }
        with tempfile.TemporaryDirectory() as tmp:
            json_path, markdown_path = write_packet(packet, Path(tmp))
            self.assertTrue(json_path.exists())
            self.assertIn("Public Evidence Pack", markdown_path.read_text(encoding="utf-8"))
            self.assertIn("Read-only.", render_markdown(packet))


if __name__ == "__main__":
    unittest.main()
