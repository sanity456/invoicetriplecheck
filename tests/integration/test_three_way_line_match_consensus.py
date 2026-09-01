import hashlib
import json
from pathlib import Path

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def _context(fragment, response):
    validators = get_validator_factory().batch_create_mock_validators(
        5,
        mock_llm_response={"nondet_exec_prompt": {fragment: json.dumps(response)}},
    )
    return {
        "validators": [validator.to_dict() for validator in validators],
        "genvm_datetime": "2026-08-25T12:00:00Z",
    }


def _deploy(contract_file, owner_account):
    factory = get_contract_factory(
        contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / contract_file
    )
    receipt = factory.deploy_contract_tx(
        args=[],
        account=owner_account,
        wait_transaction_status=TransactionStatus.FINALIZED,
    )
    _ok(receipt)
    return factory, extract_contract_address(receipt)


def _send(method, args, context=None):
    if context is None:
        receipt = method(args=args).transact(
            wait_transaction_status=TransactionStatus.FINALIZED
        )
    else:
        receipt = method(args=args).transact(
            transaction_context=context,
            wait_transaction_status=TransactionStatus.FINALIZED,
        )
    _ok(receipt)
    return receipt


def test_five_validator_three_role_reconciliation_flow():
    buyer_account, receiver_account, supplier_account = create_accounts(3)
    factory, address = _deploy("three_way_line_match.py", buyer_account)
    buyer = factory.build_contract(address, account=buyer_account)
    receiver = factory.build_contract(address, account=receiver_account)
    supplier = factory.build_contract(address, account=supplier_account)
    order_id = f"{str(buyer_account.address).lower()}:ORDER-1"
    po = json.dumps({"lines": [{"id": "PO1", "description": "Blue archive storage boxes", "quantity": 2, "unit_price": 500}]})
    receipt = json.dumps({"lines": [{"id": "R1", "description": "Blue archive storage boxes received", "quantity": 2}]})
    invoice = json.dumps({"lines": [{"id": "I1", "description": "Blue archive storage boxes", "quantity": 2, "unit_price": 500}]})
    crosswalk = {
        "receipt_to_po": [{"receipt_id": "R1", "po_id": "PO1"}],
        "invoice_to_po": [{"invoice_id": "I1", "po_id": "PO1"}],
    }
    _send(buyer.create_order, ["ORDER-1", receiver_account.address, supplier_account.address, po, "purchase-order-snapshot"])
    _send(receiver.attest_receipt, [order_id, receipt, "receiver-docket-1"])
    _send(supplier.submit_invoice, [order_id, invoice, "supplier-invoice-1"])
    _send(buyer.reconcile_order, [order_id], _context("Crosswalk one receipt", crosswalk))
    _send(buyer.buyer_close, [order_id, True, "Buyer accepts the public three-way reconciliation result."])
    assert buyer.get_order(args=[order_id]).call()["state"] == "ACCEPTED"
