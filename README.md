# ThreeWayLineMatch

A reusable role-separated PO, receipt, and invoice workflow where validators build two semantic crosswalks and code independently checks received quantities, invoiced quantities, and unit prices.

The repository is standalone and the contract is reusable: one deployment can hold multiple independent records for unrelated callers. It has no frontend and moves no funds.

## Native mechanism

buyer PO -> receiver attestation + supplier invoice -> dual crosswalk consensus -> deterministic discrepancy codes.

## Actors

buyer, receiver, supplier, GenLayer validators.

## Source boundary

No web collection. All document lines and references are public caller-attested snapshots and are not authenticated.

## Safety boundary

It does not approve payment, detect fraud, validate tax, establish delivery, or replace accounting controls.

All inputs and results are public. Untrusted public data is delimited in prompts and cannot change the closed response schema. A malformed or non-consensus model result fails without committing the intended state transition.

## Verification

    genvm-lint check contracts/three_way_line_match.py
    genvm-lint typecheck contracts/three_way_line_match.py --strict
    python -m pytest tests/direct -q -p no:cacheprovider
    python tests/run_glsim.py --port 4000 --validators 5 --no-browser
    python -m pytest tests/integration -q -s -p no:cacheprovider

See ARCHITECTURE.md, SECURITY.md, SOURCE_PROVENANCE.md, AUDIT.md, SUBMISSION_CHECKLIST.md, and deployments/studionet.json.

MIT licensed.

<!-- correction-release-start -->
## Corrected release integrity

The full twelve-repository correction audit applied both steward findings to this contract. The validator now canonicalizes the leader's actual PO-to-receipt and PO-to-invoice mappings, recomputes the crosswalk digest from those mappings, compares the full payload independently, and repeats that binding before reconciliation state is written.

The current StudioNet release is `0x7dF76B677258378afeE3999D7EE21F5B70af6955`. Its source bytes and full schema were read back from StudioNet and matched this repository exactly. Use `CORRECTION.md`, `REVIEW_RESPONSE.txt`, and the commit-pinned `deployments/studionet.json` for submission evidence; do not reuse the superseded address `0x7ca12fC62B8ccFD897DF45Df79046a41A2623298`.
<!-- correction-release-end -->
