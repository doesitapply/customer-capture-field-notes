# Public Evidence Pack v0

`tools/public_evidence_pack.py` creates a small, repeatable packet from one **public** HTTP(S) page.

It is the product seed behind a bounded public-only teardown: first collect the observable record; then make a clear, human-readable recommendation. It is deliberately narrower than a compliance platform.

## What it records

- requested and final URL, status, retrieval timestamp, and SHA-256 content hash;
- page title, meta description, H1 headings, public form/control counts;
- public cues for Privacy, Terms, and cookie language;
- selected HTTP response-header observations;
- a small sample of public links.

## What it does not claim or check

- certification, legal compliance, WCAG conformance, HIPAA/SOC 2/GDPR status;
- authenticated pages, private data, forms, checkout, APIs, or JavaScript behavior;
- vulnerabilities, exploitation, penetration testing, or revenue/conversion results.

The scanner rejects localhost, private-network, embedded-credential, and non-HTTP(S) URLs before network access. Redirects are checked against the same public-only boundary.

## Run locally

```bash
python tools/public_evidence_pack.py https://example.com --out evidence-output/example
python -m unittest discover -s tests -p 'test_*.py'
```

## Positioning rule

This is not “115 agents across seven compliance suites.” It is:

> One public URL. A reproducible observation record. The next safest fix.

Use it to support a scoped public teardown, never to make an audit, certification, security, or legal claim.
