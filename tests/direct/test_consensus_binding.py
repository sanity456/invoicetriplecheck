"""Adversarial crosswalk binding regressions."""

import hashlib
import json

from tests.direct.test_three_way_line_match import MAP, _documents, _order, _reconcile


def _hash(value):
    wire = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return "sha256:" + hashlib.sha256(wire.encode("ascii")).hexdigest()


HONEST_HASH = _hash(MAP)
FORGED = {
    "receipt_to_po": [{"receipt_id": "R1", "po_id": "UNMATCHED"}],
    "invoice_to_po": [{"invoice_id": "I1", "po_id": "PO1"}],
    "crosswalk_sha256": HONEST_HASH,
}


def _captured(contract, vm, buyer, receiver, supplier):
    order_id = _order(contract, vm, buyer, receiver, supplier)
    _documents(contract, vm, order_id, receiver, supplier)
    _reconcile(contract, vm, buyer, order_id)
    return order_id


def test_validator_rejects_changed_pairs_with_honest_hash(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    _captured(contract, direct_vm, direct_alice, direct_bob, direct_charlie)
    assert direct_vm.run_validator(leader_result=FORGED) is False


def test_validator_accepts_honest_complete_crosswalk(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    _captured(contract, direct_vm, direct_alice, direct_bob, direct_charlie)
    assert direct_vm.run_validator() is True


def test_post_consensus_forgery_preserves_ready_order(contract, direct_vm, direct_alice, direct_bob, direct_charlie, monkeypatch):
    from genlayer import gl

    order_id = _order(contract, direct_vm, direct_alice, direct_bob, direct_charlie)
    _documents(contract, direct_vm, order_id, direct_bob, direct_charlie)
    before = contract.get_order(order_id)
    direct_vm.sender = direct_alice
    monkeypatch.setattr(gl.vm, "run_nondet_unsafe", lambda *args: FORGED)
    with direct_vm.expect_revert("crosswalk_hash_mismatch"):
        contract.reconcile_order(order_id)
    assert contract.get_order(order_id) == before
