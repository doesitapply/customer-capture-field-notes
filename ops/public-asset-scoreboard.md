# Customer Capture Field Notes — Public Asset Scoreboard

Updated: 2026-08-03

| Measure | Verified state |
|---|---|
| Public site | https://doesitapply.github.io/customer-capture-field-notes/ |
| Latest public utility | [CTA Choice Matrix](https://doesitapply.github.io/customer-capture-field-notes/cta-choice-matrix.html) |
| Repository path | `cta-choice-matrix.html` |
| Release commit | `6bb421e3c17c3a1cf9722c8f050fd91a9b95c3e0` |
| GitHub Pages release | [Actions run 30761105663](https://github.com/doesitapply/customer-capture-field-notes/actions/runs/30761105663) succeeded for that commit; Pages build `1128746975` is `built` |
| Live-content check | Cache-busted matrix and home URLs returned HTTP 200 with the required new-page and home-link markers |
| Verified spend | **$0** |
| Verified revenue | **$0** |
| Public outreach this run | **No** |

## Current dollar blocker

The CTA Choice Matrix is live. It gives a founder or operator a public-only way to compare two visible next actions before treating one as primary, but publication is not distribution or proof of demand. Fresh read-only preflights on `2026-08-03` retained `WAITING_EXTERNAL`: the human-distribution card has no authority/live-share receipt, and the exact public intake query had **0** matching open `public-only-teardown` issues.

The next dollar blocker remains **human-owned distribution or a genuine inbound request**. The exact-copy human handoff remains `reports/2026-07-31-human-owned-distribution-approval-card.md` for the **CTA Clarity Scorecard**; the newer CTA Choice Matrix is live but is not silently substituted into that private share card. At `2026-08-03T14:11Z`, `tools/check_human_distribution_gate.py` v0.2 returned `WAITING_EXTERNAL` with a pinned-copy match, while `tools/check_public_intake.py` returned `WAITING_EXTERNAL` with `0` matching open requests. The distribution helper preserves the approved public-utility URL and pins the quoted share copy to baseline hash `52e75f66fec5b3a2221ade1d9eb33dd0eed3b6048417b9e5e98977b017d375ed`; a local copy mismatch is `BLOCKED_SAFE`, not permission to post. Its interface and stop gates are in `docs/HUMAN_DISTRIBUTION_GATE.md`; this control upgrade is recorded in `reports/2026-08-01-exact-copy-baseline-gate.md`.

For an actual human-approved share attempt, use the private after-result receipt shape at `reports/2026-08-02-human-distribution-receipt-template.md`. It does not authorize or record a post by itself: a canonical live URL or explicit platform success confirmation is still required before a share is considered live.

Before any human-supervised distribution or reply decision, run both read-only checks:

```bash
python tools/check_human_distribution_gate.py
python tools/check_public_intake.py
```

If either relevant state remains `WAITING_EXTERNAL`, do not invent a post, reply, payment request, or revenue result. A human must choose one policy-compliant channel they own, name the approved identity, confirm exact copy/link, and grant one-time submission authority. If a matching public request appears, a human must inspect the original public issue, confirm public-only scope, and decide whether a narrow paid teardown is appropriate. A canonical live URL or platform confirmation is required before a share is recorded as live.

## Safety state

The CTA Choice Matrix is static and public-only: no form, script, iframe, analytics/tracking embed, payment-provider link, login, private-data request, sensitive intake, or performance claim was added. The repository-local intake monitor is GET-only against the named public GitHub Issues query and is not a GitHub Pages browser surface.
