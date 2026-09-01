# Correction and release record

Repository: invoicetriplecheck

Contract: ThreeWayLineMatch

Corrected release verified: 2026-09-01T09:09:18.372466Z

## Findings applied

This repository was checked against both steward findings from the rejected Boxcomplete and Baggate submissions:

1. A leader-provided digest is not proof of its attached substantive payload. Every result that affects state must be canonicalized, independently compared, and rebound after consensus.
2. A shared permissionless registry with fixed global capacity can be captured or exhausted. Operational catalogs must be explicitly owner-scoped, bounded per catalog, or safely reclaimable.
3. Corrected repository source is insufficient when the submitted Studio/Explorer address still runs an earlier build. The active address, deployed source, ABI, transaction, and evidence URLs must identify one release.

## Contract-specific correction

The validator now canonicalizes the leader's actual PO-to-receipt and PO-to-invoice mappings, recomputes the crosswalk digest from those mappings, compares the full payload independently, and repeats that binding before reconciliation state is written.

## Verified release lock

Current StudioNet address: 0x7dF76B677258378afeE3999D7EE21F5B70af6955

Deployment transaction: 0x75266a7291346d230b28dc1cfdca4adc8051b604f05094d8458637f837a18e3f

Source SHA-256: a03ebfb9d1f293d79591de2fc1ce9d10b43e322cc7420189087325cba61cd6cf

Superseded address: 0x7ca12fC62B8ccFD897DF45Df79046a41A2623298

The deployment manifest records exact byte-for-byte source readback, exact full ABI/schema equality, successful finalized execution for all 6 release transactions, role-separated external wallets, and the final state observed from StudioNet. The superseded address is historical only and must not be used in a new submission.

## Regression evidence

GenVM lint and strict typecheck: pass

Direct tests: 11 pass

Five-validator integration tests: 1 pass

Leader-payload or post-consensus injection regression tests: pass

Registry isolation and reclaim tests: not applicable

## Review boundary

No web collection. All document lines and references are public caller-attested snapshots and are not authenticated.

It does not approve payment, detect fraud, validate tax, establish delivery, or replace accounting controls.

This record documents the implemented controls and verified release. It does not promise a particular human review outcome.
