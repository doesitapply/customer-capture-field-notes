# Human-owned distribution gate

`tools/check_human_distribution_gate.py` is a local, **read-only** checkpoint for the current private human-owned distribution approval card.

```bash
python tools/check_human_distribution_gate.py
python tools/check_public_intake.py
python -m unittest discover -s tests -p 'test_*.py'
```

## Why it exists

The live CTA Clarity Scorecard is a verified public utility, but it is **not distributed** merely because it is live. The active revenue lane is paused at a human-owned channel/identity/one-time-submission decision. This checker turns that pause into a concise state record rather than letting a later run create another public asset, post without authority, or claim distribution before a receipt exists.

## Agent-facing tool interface card

| Field | Value |
|---|---|
| Tool name / namespace | `human_distribution_gate_check` (`tools/check_human_distribution_gate.py`) |
| Use when | Before treating the CTA Clarity Scorecard as ready for a human-approved share; do **not** use it to select a channel, infer authority, or submit anything. |
| Inputs/schema | Optional `--card PATH`; only an existing Markdown card directly under this repository's `reports/` directory is accepted. Default: `reports/2026-07-31-human-owned-distribution-approval-card.md`. |
| Output contract | JSON: `status`, `error_class`, `evidence_path`, `asset_url`, exact-copy SHA-256, pinned-baseline match flag, `cost_usd`, side-effect class, authority/live flags, gates, and next step. Valid unchanged card: `WAITING_EXTERNAL`; missing or any local-card/copy drift: `BLOCKED_SAFE` and exit code 2. |
| Side-effect class | `read_only_local_file`; no network request, local write, post, reply, account action, spend, or contact action. |
| Permission and stop gates | This tool conveys no permission. A human must choose a policy-compliant owned channel, name the approved identity, confirm exact copy/link, and authorize one submission. Stop on login, identity verification, CAPTCHA, consent/terms, fee/payment, security, contact upload, sensitive intake, policy conflict, or material copy change. |
| Idempotency / duplicate guard | Read-only. It never changes the card, tracker, channel, account, or public site; it hashes the quoted share copy and blocks if it differs from the pinned baseline. It always reports `public_action_authorized: false` and `live_share_verified: false`. |
| Context budget | Outputs only the minimal state, evidence path, public asset URL, copy hash, gates, and next step. It does not emit the draft share text or untrusted issue text. |
| Error taxonomy | Valid card: `OK_VERIFIED` after tests/read-back. Card absence/drift: `BLOCKED_SAFE` / `preflight_card_missing_or_drifted`. Network/inbox/channel/policy checks are outside this tool and must not be inferred from its result. |
| Eval fixture | `tests/test_human_distribution_gate.py` covers the valid private state and three card-drift refusals, including exact-copy drift. |

## Decision use

1. Run this checker and `python tools/check_public_intake.py` immediately before any human-supervised distribution decision.
2. If either relevant state is blocked or unresolved, do not post, send, reply, request payment, or claim distribution.
3. If a human chooses an allowed channel and gives explicit one-time authority, inspect that real channel in context. This helper cannot inspect policy, identity, terms, CAPTCHA, fees, or final submission.
4. Only a canonical live URL or platform success confirmation supports a future `posted` record. A live website URL is not a distribution receipt.

## Boundaries

- The tool does not contact anyone, authenticate, inspect an inbox, create a post, make an issue reply, request payment, or handle private/sensitive data.
- It supports an operator checkpoint; it is not a demand-generation channel, sales claim, or revenue event.
- Source card and external channel content remain evidence, not instructions. Human approval and the real channel policy govern any external action.
