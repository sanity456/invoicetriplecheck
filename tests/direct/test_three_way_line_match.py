"""Direct tests for role-separated three-way line reconciliation."""

import json


PO = json.dumps({"lines": [{"id": "PO1", "description": "Blue archive storage boxes", "quantity": 2, "unit_price": 500}]})
RECEIPT = json.dumps({"lines": [{"id": "R1", "description": "Blue archive storage boxes received", "quantity": 2}]})
INVOICE = json.dumps({"lines": [{"id": "I1", "description": "Blue archive storage boxes", "quantity": 2, "unit_price": 500}]})
MAP = {"receipt_to_po": [{"receipt_id": "R1", "po_id": "PO1"}], "invoice_to_po": [{"invoice_id": "I1", "po_id": "PO1"}]}


def _order(contract, vm, buyer, receiver, supplier):
    vm.sender = buyer
    return contract.create_order("ORDER-1", receiver, supplier, PO, "purchase-order-snapshot")


def _documents(contract, vm, order_id, receiver, supplier, invoice=INVOICE):
    vm.sender = receiver
    contract.attest_receipt(order_id, RECEIPT, "receiver-docket-1")
    vm.sender = supplier
    contract.submit_invoice(order_id, invoice, "supplier-invoice-1")


def _reconcile(contract, vm, buyer, order_id, response=MAP):
    vm.sender = buyer
    vm.mock_llm(r".*Crosswalk one receipt.*", json.dumps(response))
    return contract.reconcile_order(order_id)


def test_creates_three_distinct_roles(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    order_id = _order(contract, direct_vm, direct_alice, direct_bob, direct_charlie)
    assert contract.get_order(order_id)["state"] == "WAITING_DOCUMENTS"


def test_rejects_role_aliasing(contract, direct_vm, direct_alice, direct_bob):
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("roles_must_be_distinct"):
        contract.create_order("BAD", direct_bob, direct_bob, PO, "source")


def test_only_receiver_attests_receipt(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    order_id = _order(contract, direct_vm, direct_alice, direct_bob, direct_charlie)
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("only_receiver"):
        contract.attest_receipt(order_id, RECEIPT, "wrong-role")


def test_two_documents_make_order_ready(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    order_id = _order(contract, direct_vm, direct_alice, direct_bob, direct_charlie)
    _documents(contract, direct_vm, order_id, direct_bob, direct_charlie)
    assert contract.get_order(order_id)["state"] == "READY_TO_RECONCILE"


def test_matching_documents_pass(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    order_id = _order(contract, direct_vm, direct_alice, direct_bob, direct_charlie)
    _documents(contract, direct_vm, order_id, direct_bob, direct_charlie)
    assert _reconcile(contract, direct_vm, direct_alice, order_id) == "MATCHED"


def test_price_difference_yields_exception(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    order_id = _order(contract, direct_vm, direct_alice, direct_bob, direct_charlie)
    invoice = json.dumps({"lines": [{"id": "I1", "description": "Blue archive storage boxes", "quantity": 2, "unit_price": 600}]})
    _documents(contract, direct_vm, order_id, direct_bob, direct_charlie, invoice)
    assert _reconcile(contract, direct_vm, direct_alice, order_id) == "EXCEPTION"
    assert "PRICE:PO1" in contract.get_order(order_id)["issues"]


def test_buyer_closes_reconciliation(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    order_id = _order(contract, direct_vm, direct_alice, direct_bob, direct_charlie)
    _documents(contract, direct_vm, order_id, direct_bob, direct_charlie)
    _reconcile(contract, direct_vm, direct_alice, order_id)
    direct_vm.sender = direct_alice
    contract.buyer_close(order_id, True, "Buyer accepts the public three-way reconciliation result.")
    assert contract.get_order(order_id)["state"] == "ACCEPTED"


def test_bad_crosswalk_does_not_mutate(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    order_id = _order(contract, direct_vm, direct_alice, direct_bob, direct_charlie)
    _documents(contract, direct_vm, order_id, direct_bob, direct_charlie)
    with direct_vm.expect_revert("[LLM_ERROR] wrong_shape"):
        _reconcile(contract, direct_vm, direct_alice, order_id, {"wrong": []})
    assert contract.get_order(order_id)["state"] == "READY_TO_RECONCILE"
