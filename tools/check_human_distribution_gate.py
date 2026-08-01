#!/usr/bin/env python
"""Read-only preflight for the human-owned distribution checkpoint.

This helper reads the approved private distribution card and emits a compact,
machine-readable state. It cannot authorize, select, or perform a post. Use it
only to prevent a future run from treating the public asset as distributed
before a human has selected a permitted channel and supplied one-time authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CARD = ROOT / "reports" / "2026-07-31-human-owned-distribution-approval-card.md"
STATE_MARKER = "PRIVATE / NOT POSTED / WAITING FOR HUMAN CHANNEL + IDENTITY AUTHORITY"
COPY_START = "**Exact share copy:**"
COPY_END = "**Human decision required before any post:**"
ASSET_URL_PATTERN = re.compile(
    r"https://doesitapply\.github\.io/customer-capture-field-notes/cta-clarity-scorecard\.html"
)
# A future human must confirm exact copy, but this baseline prevents the helper
# from calling a modified local card "the same exact share" by hash alone.
# It conveys no approval to post.
PINNED_EXACT_SHARE_COPY_SHA256 = "52e75f66fec5b3a2221ade1d9eb33dd0eed3b6048417b9e5e98977b017d375ed"
REQUIRED_PHRASES = (
    "select one specific channel",
    "name the account/identity",
    "authorize one submission",
    "Stop before submission if any of these appear:",
    "No receipt URL or confirmation means **not posted**.",
)


class GateCheckError(ValueError):
    """Raised when the local handoff is missing or has drifted from its safe shape."""


def _approved_card_path(value: str) -> Path:
    candidate = Path(value).expanduser().resolve()
    reports_dir = (ROOT / "reports").resolve()
    if candidate.parent != reports_dir or candidate.suffix.lower() != ".md":
        raise GateCheckError("card must be a Markdown file directly under this repository's reports directory")
    return candidate


def _extract_share_copy(card_text: str) -> str:
    try:
        after_start = card_text.split(COPY_START, 1)[1]
        copy_block = after_start.split(COPY_END, 1)[0]
    except IndexError as exc:
        raise GateCheckError("approval card is missing the bounded exact-share-copy section") from exc
    lines = [line[2:] for line in copy_block.splitlines() if line.startswith("> ")]
    share_copy = "\n".join(lines).strip()
    if not share_copy:
        raise GateCheckError("approval card has no quoted exact share copy")
    return share_copy


def build_result(card_text: str, card_path: Path) -> dict[str, Any]:
    missing = [phrase for phrase in REQUIRED_PHRASES if phrase not in card_text]
    if STATE_MARKER not in card_text:
        missing.append("private/not-posted human-authority state marker")
    asset_urls = sorted(set(ASSET_URL_PATTERN.findall(card_text)))
    if len(asset_urls) != 1:
        missing.append("one unambiguous approved CTA Clarity Scorecard URL")
    if missing:
        raise GateCheckError("approval card drifted or is incomplete: " + "; ".join(missing))

    share_copy = _extract_share_copy(card_text)
    share_copy_sha256 = hashlib.sha256(share_copy.encode("utf-8")).hexdigest()
    if share_copy_sha256 != PINNED_EXACT_SHARE_COPY_SHA256:
        raise GateCheckError(
            "approval card exact share copy drifted from the pinned baseline; "
            "do not post until the human reviews the changed copy and the local baseline/test are deliberately updated"
        )
    return {
        "tool": "human_distribution_gate_check",
        "version": "0.2",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "WAITING_EXTERNAL",
        "error_class": None,
        "side_effect_class": "read_only_local_file",
        "cost_usd": 0,
        "public_action_authorized": False,
        "live_share_verified": False,
        "evidence_path": str(card_path),
        "asset_url": asset_urls[0],
        "exact_share_copy_sha256": share_copy_sha256,
        "pinned_exact_share_copy_sha256": PINNED_EXACT_SHARE_COPY_SHA256,
        "exact_share_copy_matches_pinned_baseline": True,
        "human_required": [
            "Select one policy-compliant channel the human owns.",
            "Name the approved account/identity for that one channel.",
            "Confirm the exact title, copy, and asset URL in the approval card.",
            "Provide one-time authority for one submission.",
        ],
        "submission_stop_gates": [
            "login or identity verification",
            "CAPTCHA, terms, or consent decision",
            "fee, payment, account/security, contact-upload, or sensitive-data prompt",
            "copy change or channel policy conflict",
        ],
        "next_step": (
            "Remain WAITING_EXTERNAL. Before any human-supervised submission, run "
            "python tools/check_public_intake.py, inspect the selected channel in context, "
            "and stop at every listed gate. A canonical live URL or platform confirmation "
            "is required before recording a share as live."
        ),
        "idempotency_guard": "Read-only; never changes the card, channel, account, tracker, or public surface.",
        "context_budget": "Returns only state, path, one approved asset URL, copy hash, gates, and next step; it does not return the draft copy or untrusted inbound text.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--card", default=str(DEFAULT_CARD), help="Private approval card under this repository's reports directory")
    args = parser.parse_args()
    try:
        card_path = _approved_card_path(args.card)
        card_text = card_path.read_text(encoding="utf-8")
        result = build_result(card_text, card_path)
    except (GateCheckError, OSError) as exc:
        result = {
            "tool": "human_distribution_gate_check",
            "version": "0.1",
            "status": "BLOCKED_SAFE",
            "error_class": "preflight_card_missing_or_drifted",
            "side_effect_class": "read_only_local_file",
            "cost_usd": 0,
            "public_action_authorized": False,
            "live_share_verified": False,
            "evidence_path": args.card,
            "next_step": "Do not post or claim distribution. Repair or replace the private approval card through human review, then rerun this read-only check.",
            "error": str(exc),
        }
        print(json.dumps(result, indent=2, sort_keys=True), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
