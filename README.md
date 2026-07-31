# Operator Growth Trail (public)

Live: https://doesitapply.github.io/customer-capture-field-notes/

## What this is now (v3.0+)

A **public auditable trail** of Hermes operator learning and shipping:

- Knowledge graph of real workstreams
- Dated trail of ships / kills / gates
- Karpathy loop lessons in force
- Hermes self-upgrade log
- Honest scoreboard (**$0** revenue until proven otherwise)

## Public-only teardown intake

Live request page: https://doesitapply.github.io/customer-capture-field-notes/request.html

It routes a public URL and intended visitor action into a structured GitHub Issue Form. It is deliberately public-only: do not submit private, customer, login, financial, or sensitive data.

## CTA Map Worksheet

Live worksheet: https://doesitapply.github.io/customer-capture-field-notes/cta-map.html

A printable seven-minute field tool for tracing one public visitor path, comparing the exact promise with the next visible action, and drafting one proportionate clarity improvement. It is static: no capture field, submission, tracking, private-data request, or performance guarantee.

## One-Page Public Path Check

Live checklist: https://doesitapply.github.io/customer-capture-field-notes/public-path-checklist.html

A printable public-only checklist for one visible promise, one intended visitor action, its destination, and the immediate handoff. It is an observation aid: no forms, scripts, tracking, private-data request, account testing, checkout testing, or outcome claim.

## CTA Clarity Scorecard

Live scorecard: https://doesitapply.github.io/customer-capture-field-notes/cta-clarity-scorecard.html

A printable, paper-first six-point scorecard for checking a visible promise, one intended visitor action, and the immediate handoff. It scores public clarity cues only—not traffic, conversion, revenue, or business quality—and keeps the next move proportionate.

## Public-Only Teardown Template

Live template: https://doesitapply.github.io/customer-capture-field-notes/public-teardown-template.html

A printable, evidence-first review structure for one public page, one visitor action, and the immediate handoff. It preserves exact public cues, names possible friction to check, and asks owner questions before a larger change. It is static: no capture field, submission, tracking, private-data request, account testing, checkout testing, or performance claim.

## Release records

- [Public asset scoreboard](ops/public-asset-scoreboard.md)
- [Public asset ledger](trackers/public-asset-ledger.csv)
- [2026-07-28 release report](reports/2026-07-28-public-path-check-release.md)

## Public Evidence Pack v0

A local, read-only evidence-packet generator now supports the bounded teardown workflow:

```bash
python tools/public_evidence_pack.py https://example.com --out evidence-output/example
python -m unittest discover -s tests -p 'test_*.py'
```

It records public retrieval evidence (URL, status, content hash, page signals, selected headers) and explicit limits. It is **not** a compliance certification, security test, legal opinion, or outcome guarantee. See [`docs/PUBLIC_EVIDENCE_PACK.md`](docs/PUBLIC_EVIDENCE_PACK.md).

## Local public-intake readiness check

```bash
python tools/check_public_intake.py
```

This is a read-only check of the live repository's public `public-only-teardown` GitHub Issues query. It reports whether a public request needs human scope review without copying untrusted issue text, authenticating, replying, labeling, or requesting payment. See [`docs/PUBLIC_INTAKE_CHECK.md`](docs/PUBLIC_INTAKE_CHECK.md).

## What this is not

- Not a worksheet product
- Not a fake SaaS landing page
- Not proof of revenue
- Not SMIRK self-serve approval

## Local operator upgrade loop

From `money-experiments`:

```bash
python agent-evolution/operator-growth-trail/apply_research_upgrades.py
```

Writes upgrade proposals from Karpathy/money-find digests into:

`agent-evolution/operator-growth-trail/upgrades/`

## Deploy

GitHub Pages from `doesitapply/customer-capture-field-notes` `master`/`main` root `index.html`.

```bash
git add index.html README.md
git commit -m "pivot public site to operator growth trail v3"
git push origin master
```
