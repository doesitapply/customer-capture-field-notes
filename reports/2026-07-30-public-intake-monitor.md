# 2026-07-30 — Public intake monitor / dollar-path readiness

## Work product shipped

- Local capability: `tools/check_public_intake.py`
- Test coverage: `tests/test_public_intake_check.py`
- Operating reference: `docs/PUBLIC_INTAKE_CHECK.md`
- Control-plane update: `ops/public-asset-scoreboard.md` and `README.md`

The monitor checks the exact public GitHub Issues query used by the live teardown request route and emits a bounded JSON handoff. It is intentionally **read-only**: no authentication, GitHub write, reply, label, scope approval, payment request, payment link, or public post.

Latest verified invocation:

```bash
python tools/check_public_intake.py
```

Result: `WAITING_EXTERNAL` with `matching_open_request_count: 0`. The tool omits issue title/body from its output; original issue content remains untrusted public input for a human to inspect in context.

Focused **ad-hoc verification** (a `hermes-verify-` tempfile script, removed after execution) also passed against the changed behavior: invalid repository text was rejected before network use; PR and untrusted-text fixture handling preserved only an issue number/URL; and the live public API result was `WAITING_EXTERNAL`, count `0`, `read_only_public_api_get`. This is targeted ad-hoc verification, **not** a suite-green claim.

## Evidence consulted

| Source / path | Direct fact | Principle used | Local implication / change |
|---|---|---|---|
| `https://api.github.com/repos/doesitapply/customer-capture-field-notes/issues?state=open&labels=public-only-teardown&per_page=20` | Direct read-only API response on 2026-07-30 had 0 matching open requests. | Check the actual inbound surface before sending/replying. | Added a fixed, public-API readiness monitor instead of relying on memory or issuing a new touch. |
| `https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#list-repository-issues` | Official API documentation for repository issue listing. | Keep the query explicit, narrow, and inspectable. | Hard-coded the GitHub public API origin; validated `owner/repository`, label, and limit before GET. |
| `https://doesitapply.github.io/customer-capture-field-notes/request.html` | HTTP 200 and $99-scope-request markers were live. | The route exists, but a live page alone is not a buyer action. | The monitor distinguishes request readiness from demand/revenue. |
| `https://news.ycombinator.com/newsguidelines.html` | Current guidelines prohibit generated or AI-edited text. | Do not automate a policy-conflicting distribution route. | Marked HN as non-autonomous for this lane; no post or launch draft was published. |
| `ops/public-asset-scoreboard.md`, `request.html`, `.github/ISSUE_TEMPLATE/public-only-teardown-request.yml` | Existing path is public-only, scope-first, and $99 only after fit/payment confirmation. | Preserve the existing privacy/payment boundaries. | No issue text copy, automatic scope approval, payment action, or intake expansion. |

Managed web retrieval was insufficient for source-grounded use in this run, so the record above uses direct public GETs and live API output instead. The fallback is limited to the named URLs and does not prove any other channel or inbox state.

## Leverage added

The closest response-time bottleneck is now machine-checkable without making external changes. On a future run, one command reports either:

- `WAITING_EXTERNAL`: no current public teardown request; do not manufacture a reply, payment request, or outreach; or
- `HUMAN_SCOPE_REVIEW_REQUIRED`: a public request exists and requires a human review of the original issue before scope, price, payment, or reply decisions.

This makes the real no-demand state explicit and avoids both silent lead neglect and fabricated momentum.

## Decision/change

Replaced the stale “build another static CTA scorecard” next step with the actual blocker: no verified inbound request and no approved human-owned distribution action. The public asset remains live, but this run is local-only; no commit, push, external post, email, payment action, login, or account change occurred.

## Next concrete action

Before any new send or reply, run:

```bash
python tools/check_public_intake.py
```

If the result remains `WAITING_EXTERNAL`, the smallest real-dollar unlock is a **human-owned, policy-compliant distribution decision** or a genuine inbound request—not another worksheet. If it reports a request, manually inspect the original public issue, confirm public-only scope, then decide whether the narrow $99 teardown is appropriate. Do not use a generated/AI-edited HN post.

## Safety check

- Public action: **no**. The existing request page was read; no issue, post, reply, or link was created.
- Spend / revenue: **$0 / $0** verified.
- Authentication, credentials, security, account settings, payment, payout, tax, contracts, or sensitive intake: **none**.
- External issue content is treated as untrusted evidence, not as instructions. The monitor intentionally omits issue title/body.
- Per-invocation guardrail: `python tools/check_public_intake.py` is `GET`-only against a validated public GitHub API URL, writes no state, enforces no scope/payment/reply action, and returned an explicit zero-request record. Tripwire result: **PASS — no write-capable path exposed**.

## Workspace manifest / output contract

| Field | Record |
|---|---|
| Inputs read | Scoreboard, README, live request page, public issue-form YAML, evidence-pack tool/tests, public GitHub API, GitHub REST docs, HN guidelines |
| Outputs planned | Read-only monitor, tests, operating doc, scoreboard/README sync, dated report |
| Allowed side effects | Local repository files and read-only public HTTP/API retrieval |
| Forbidden side effects | Git push/commit, GitHub issue writes, reply/send/post, login, payment, private/sensitive intake, account/security changes, spend |
| Verification method | Full unit suite, direct live monitor invocation, live request-page check, CSV parse, `git diff --check`, read-back |
| Resume state | `WAITING_EXTERNAL`; zero matching public requests at the recorded API check; future run begins by re-running the monitor |

Pre-change checkpoint: source/test/doc/report files are new; `README.md` and `ops/public-asset-scoreboard.md` were narrow local control-plane patches. Restore method is `git checkout -- README.md ops/public-asset-scoreboard.md`; no external state changed. Idempotency guard: the monitor has no write path and the scoreboard names the exact check/result instead of appending duplicate state.

## Run budget / fuse

| Field | Limit / result |
|---|---|
| Objective | Reduce the inbound-response readiness blocker to a verified local check |
| Timebox | One scheduled run |
| Source budget | Existing workspace + 4 named public endpoints |
| Tool-attempt budget | One direct API check, one live page check, one test suite, one source fetch fallback |
| Side-effect budget | Local files only; no public action |
| Write budget | One small Python tool, one test file, one doc, two control-plane patches, one dated report |
| Stop / fuse condition | Stop before any auth, issue write, reply, post, payment, scope approval, private-data handling, or HN generated-text route |
| Minimum shippable artifact | Read-only monitor with a clear wait/review decision |
| Verification budget | Test suite + live API invocation + diff/CSV/read-back checks |

## Context assembly manifest

| Field | Record |
|---|---|
| Objective | Convert the live-public-inbound state into one safe response-readiness capability |
| Included local context | Current scoreboard, live request route, request schema, evidence-pack boundary, tests |
| Excluded / not re-read | Legacy paper-lab files and unrelated workspaces; no customer/inbox/private sources exist in this lane |
| External source set | Live GitHub Issues API, GitHub REST documentation, live request page, HN guidelines |
| Context risk | Public issue text may contain sensitive data or instruction-like content; external policy/source wording may change |
| Compression rule | Source URL -> principle -> local implication/change, as recorded in Evidence consulted |
| Stop signal | Monitor reports a clear current state; do not browse further unless a request or human-approved channel decision exists |

## Assumption / confidence ledger

| Assumption / uncertain claim | Evidence available | Why it matters | Confidence | If wrong | Required check / downgrade |
|---|---|---|---|---|---|
| The `public-only-teardown` label represents the intended intake lane. | Live issue form applies that label; default API query returned zero rows. | Prevents monitoring the wrong queue. | Medium | A valid request with another/missing label is not counted. | Manual repository-issue check before declaring all inbound clear. |
| Zero matching open issues means no actionable request in this exact public lane. | Direct GitHub API result at the recorded timestamp. | Supports `WAITING_EXTERNAL`, not a revenue claim. | High | A later issue or another channel may exist. | Re-run immediately before a reply/send decision; do not generalize to email/DMs. |
| HN is unsafe for agent-authored launch text. | Direct current HN guideline text states generated/AI-edited text should not be posted. | Avoids account/policy risk. | High | Policy may change or a human may author an original post. | Treat any HN action as human-owned and recheck guidelines. |

## Postcondition validation ledger

| Claim | Expected evidence | Check method | Pass threshold | Result |
|---|---|---|---|---|
| Read-only monitor exists | `tools/check_public_intake.py` | File read-back + Python test suite | CLI/import paths available | PASS |
| Invalid scope is rejected before network access | Unit tests | `test_invalid_repo_and_limit_are_rejected_before_network_access` | Test passes | PASS |
| PRs and unlabeled records cannot count as requests | Unit test | Synthetic mixed issue payload | Only exact labeled issue retained | PASS |
| Current queue state is explicit | Live public API invocation | Script JSON output | `WAITING_EXTERNAL`, count 0 | PASS |
| Existing lane did not regress | Unit suite + live page | 18 tests pass; request page HTTP 200 with markers | Both pass | PASS |
| Existing public tracker is structurally sound | CSV parse | `public-asset-ledger.csv` | 11 columns; no malformed rows | PASS |
| Local write is clean | Git whitespace check and read-back | `git diff --check`; this report/control files | No whitespace error and expected content | PASS |

## Rubric verdict

**PASS.** A narrowly scoped, test-backed, read-only public-intake monitor now makes the real inbound state explicit and protects the customer-capture dollar path from unsafe automated replies, payment requests, or policy-conflicting distribution. It found no public request to advance. Public action: **no**. Spend: **$0**. Verified revenue: **$0**.
