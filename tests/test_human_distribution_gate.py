import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from check_human_distribution_gate import (
    GateCheckError,
    PINNED_EXACT_SHARE_COPY_SHA256,
    build_result,
)


CARD = """# Human-owned distribution approval card

**State: PRIVATE / NOT POSTED / WAITING FOR HUMAN CHANNEL + IDENTITY AUTHORITY**

**Live public utility:** https://doesitapply.github.io/customer-capture-field-notes/cta-clarity-scorecard.html

**Exact share copy:**

> I made a free, printable CTA Clarity Scorecard for checking one visible promise, one intended visitor action, and the immediate handoff. It is public-only and observational: no login, form submission, analytics, private data, checkout testing, or performance claims. Use it to spot one clarity cue to preserve or one narrow question to ask before proposing a bigger change: https://doesitapply.github.io/customer-capture-field-notes/cta-clarity-scorecard.html

**Human decision required before any post:** select one specific channel; name the account/identity; and authorize one submission.

Stop before submission if any of these appear:

No receipt URL or confirmation means **not posted**.
"""


class HumanDistributionGateTests(unittest.TestCase):
    def test_valid_private_card_returns_waiting_external_without_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "card.md"
            path.write_text(CARD, encoding="utf-8")
            result = build_result(CARD, path)
        self.assertEqual(result["status"], "WAITING_EXTERNAL")
        self.assertFalse(result["public_action_authorized"])
        self.assertFalse(result["live_share_verified"])
        self.assertEqual(
            result["asset_url"],
            "https://doesitapply.github.io/customer-capture-field-notes/cta-clarity-scorecard.html",
        )
        self.assertEqual(result["exact_share_copy_sha256"], PINNED_EXACT_SHARE_COPY_SHA256)
        self.assertEqual(result["pinned_exact_share_copy_sha256"], PINNED_EXACT_SHARE_COPY_SHA256)
        self.assertTrue(result["exact_share_copy_matches_pinned_baseline"])
        self.assertEqual(result["side_effect_class"], "read_only_local_file")

    def test_changed_exact_share_copy_is_blocked_safe(self):
        drifted_card = CARD.replace("free, printable", "free downloadable")
        with self.assertRaises(GateCheckError) as context:
            build_result(drifted_card, Path("card.md"))
        self.assertIn("pinned baseline", str(context.exception))

    def test_missing_human_authority_marker_is_blocked_safe(self):
        unsafe_card = CARD.replace("authorize one submission", "prepare a post")
        with self.assertRaises(GateCheckError) as context:
            build_result(unsafe_card, Path("card.md"))
        self.assertIn("authorize one submission", str(context.exception))

    def test_missing_not_posted_receipt_rule_is_blocked_safe(self):
        unsafe_card = CARD.replace("No receipt URL or confirmation means **not posted**.", "")
        with self.assertRaises(GateCheckError) as context:
            build_result(unsafe_card, Path("card.md"))
        self.assertIn("No receipt URL", str(context.exception))


if __name__ == "__main__":
    unittest.main()
