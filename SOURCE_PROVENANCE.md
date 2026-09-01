# Source provenance

No web collection. All document lines and references are public caller-attested snapshots and are not authenticated.

The contract does not claim live web collection, publisher authentication, or freshness. A source_reference field is provenance metadata supplied by a caller and is stored with source_verified set to false. Reviewers and downstream consumers must inspect and pin the exact public snapshot themselves.

<!-- correction-release-start -->
## Explicit source-collection boundary

No live source is collected by this contract. Every text, image, document line, catalog entry, policy, reference, or other evidentiary input is a public caller-supplied snapshot. The contract does not authenticate its publisher, provenance, completeness, freshness, or real-world truth. Every source reference is unverified metadata, even when it is stored alongside a `source_verified` field set to false. Reviewers and downstream callers must independently inspect and pin the precise public snapshot they intend to use.
<!-- correction-release-end -->
