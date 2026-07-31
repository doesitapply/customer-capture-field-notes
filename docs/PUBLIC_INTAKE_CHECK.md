# Public Intake Monitor v0

`tools/check_public_intake.py` is a **read-only** readiness check for the live public teardown-request lane.

```bash
python tools/check_public_intake.py
python -m unittest discover -s tests -p 'test_*.py'
```

## What it does

- Calls GitHub's public Issues API for the exact repository and `public-only-teardown` label.
- Counts only open labeled issues; pull requests and unlabeled records are excluded.
- Emits compact JSON with an explicit `WAITING_EXTERNAL` or `HUMAN_SCOPE_REVIEW_REQUIRED` state.
- Retains only issue number, creation time, and public URL. It deliberately does **not** copy title/body text, because issue content is untrusted public input and may contain data or instructions outside scope.

## What it does not do

- It never authenticates or changes a GitHub account.
- It never creates, replies to, labels, assigns, closes, or deletes an issue.
- It never approves scope, asks for private data, sends a payment request/link, accepts payment, or contacts anyone.
- It is not proof that every inbox or public channel is clear; it checks only the exact public GitHub Issues query in its output.

## Decision use

- `WAITING_EXTERNAL`: there is no matching open public request. Do not manufacture outreach or a payment request. Re-run the monitor before a new reply/send decision.
- `HUMAN_SCOPE_REVIEW_REQUIRED`: open the original public issue manually, verify it contains only public information, confirm whether the narrow $99 teardown is a fit, and decide the next action. A human must make any scope, price, payment, or reply decision.

## Provenance and safety

- Operational source: `https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#list-repository-issues`
- Live endpoint used by the default invocation: `https://api.github.com/repos/doesitapply/customer-capture-field-notes/issues?state=open&labels=public-only-teardown&per_page=20`
- The implementation uses `GET` only and hard-codes the public GitHub API origin. Repository and label inputs are validated before network access.
- This is an operator-response readiness capability, not a demand-generation channel or revenue claim.
