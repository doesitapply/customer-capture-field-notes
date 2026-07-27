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

## Public Evidence Pack v0

A local, read-only evidence-packet generator now supports the bounded teardown workflow:

```bash
python tools/public_evidence_pack.py https://example.com --out evidence-output/example
python -m unittest discover -s tests -p 'test_*.py'
```

It records public retrieval evidence (URL, status, content hash, page signals, selected headers) and explicit limits. It is **not** a compliance certification, security test, legal opinion, or outcome guarantee. See [`docs/PUBLIC_EVIDENCE_PACK.md`](docs/PUBLIC_EVIDENCE_PACK.md).

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
