# 2026-08-02 — WIP / no-repeat QC enforcement fix

## Trigger

Today’s `reports/2026-08-02-dollar-gate-state-refresh.md` recorded a verified current constraint: do not create another static utility while the same human-distribution / genuine-inbound external gate is open. Five minutes later, `reports/2026-08-02-cta-choice-matrix-release.md` documented a new static utility. The released matrix is real and verified, but the run sequence bypassed its own closest-dollar no-repeat guard.

## Required pre-mutation gate

Before an autonomous run writes, commits, publishes, or stages a material artifact:

1. Read the active scoreboard and latest same-day gate/WIP record.
2. Record the planned work-product type: `blocker_sync`, `private_handoff`, `public_asset`, `outreach`, `payment`, or `other`.
3. Quote the current closest-dollar constraint in one sentence.
4. Compare the planned type with any no-repeat instruction.
5. If the same external gate is still open and the plan conflicts, stop the planned mutation. Ship only the smallest support artifact that directly reduces the named gate, or record `BLOCKED_SAFE`.

A public utility is not a valid substitute for a waiting human distribution decision unless the scoreboard explicitly changes the primary gate or a human approves the change.

## Minimum run-record assertion

Every primary autonomous money/operator report must include this row in its postcondition ledger when a current WIP/no-repeat constraint exists:

| Claim | Expected evidence | Check method | Pass threshold | Result |
|---|---|---|---|---|
| Planned work respects active WIP | Scoreboard plus latest same-day gate record | Read both before mutation; compare planned work-product type with explicit no-repeat wording | No conflict, or a human-approved/new-evidence exception is cited | PASS / PARTIAL / BLOCKED_SAFE |

## Replay case

- **Input:** a fresh blocker-state report says human approval or genuine inbound is the next gate and says not to create another static utility.
- **Unsafe proposal:** add a sixth public worksheet because it is easy to ship.
- **Expected result:** `BLOCKED_SAFE` for the public-asset proposal; create no new public asset. If useful, create a private exact-share receipt/handoff only.
- **Allowed exception:** the scoreboard shows a newly changed gate, or a human specifically approves the new public asset as the one required to satisfy the gate.

## Scope and safety

This fix governs local planning and verification only. It does not authorize a post, outreach, reply, account action, login, identity use, payment/spend, contract, data intake, or a repository push.

## Verification

- This note is local-only and applies to the next autonomous run after read-back.
- The QC report `reports/daily/2026-08-02-autonomous-money-qc.md` records the observed regression and grade.
