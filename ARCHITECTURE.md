# Architecture

Project: ThreeWayLineMatch

Reusable primitive: buyer PO -> receiver attestation + supplier invoice -> dual crosswalk consensus -> deterministic discrepancy codes.

The contract separates caller-attested public inputs, validator-agreed semantic fields, deterministic state transitions, and role-bound final actions. It stores canonical JSON strings in GenVM maps, validates every identifier and bound before consensus, and keeps source references explicitly unverified.

The mechanism is not a renamed assessment record. Its state transitions, role topology, storage layout, deterministic algorithm, and public ABI are specific to this project.

<!-- correction-release-start -->
## Consensus and storage safety boundary

The validator now canonicalizes the leader's actual PO-to-receipt and PO-to-invoice mappings, recomputes the crosswalk digest from those mappings, compares the full payload independently, and repeats that binding before reconciliation state is written.

The on-chain state transition consumes only the canonical value returned by the post-consensus binding boundary. This contract does not expose a shared permissionless fixed-cap operational registry.
<!-- correction-release-end -->
