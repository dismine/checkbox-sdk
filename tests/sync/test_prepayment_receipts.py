import json
import pathlib

import pytest
from pydantic import ValidationError

from checkbox_sdk.client.synchronous import CheckBoxClient
from checkbox_sdk.storage.simple import SessionStorage
from .base import open_shift, close_shift
from ..models.prepayment_receipts_models import PrepaymentRelationSchema
from ..models.receipts_models import ReceiptSchema


def test_create_prepayment_receipt(auth_token, license_key, check_receipt_creation, client_email):
    # sourcery skip: no-conditionals-in-tests
    if not check_receipt_creation:
        pytest.skip("Skip testing receipt creation")

    assert license_key, "License key is empty"

    storage = SessionStorage()
    with CheckBoxClient(storage=storage) as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert storage.cash_register["is_test"], "Not test cash register"

        open_shift(client)

        base_path = pathlib.Path(__file__).resolve().parent.parent
        receipt_path = base_path / "test_data/prepayment_receipt.json"
        receipt_data = json.loads(receipt_path.resolve().read_text())

        # sourcery skip: no-conditionals-in-tests
        if client_email:
            receipt_data["delivery"] = {"email": client_email}

        prepayment_receipt = client.prepayment_receipts.create_prepayment_receipt(
            receipt=receipt_data,
            timeout=5,
            storage=storage,
        )

        try:
            model = ReceiptSchema(**prepayment_receipt)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Receipt validation schema failed: {e}")

        after_payment = {"payments": [{"type": "CASHLESS", "value": 5500}]}

        if client_email:
            after_payment["delivery"] = {"email": client_email}

        after_payment_receipt = client.prepayment_receipts.create_after_payment_receipt(
            relation_id=prepayment_receipt["pre_payment_relation_id"],
            receipt=after_payment,
            timeout=5,
            storage=storage,
        )

        try:
            model = ReceiptSchema(**after_payment_receipt)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Receipt validation schema failed: {e}")

        relation = client.prepayment_receipts.get_prepayment_relation(
            relation_id=prepayment_receipt["pre_payment_relation_id"],
            storage=storage,
        )

        try:
            model = PrepaymentRelationSchema(**relation)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Relation validation schema failed: {e}")

        chain_data = {}
        if client_email:
            chain_data["delivery"] = {"email": client_email}

        receipts_chain = client.prepayment_receipts.get_prepayment_receipts_chain(
            relation_id=prepayment_receipt["pre_payment_relation_id"],
            data=chain_data,
            storage=storage,
        )

        # sourcery skip: no-loop-in-tests
        for receipt in receipts_chain:
            try:
                model = ReceiptSchema(**receipt)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Receipt validation schema failed: {e}")

        close_shift(client)


def test_get_pre_payment_relations_search(auth_token, license_key):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        # sourcery skip: no-loop-in-tests
        for receipt in client.prepayment_receipts.get_pre_payment_relations_search():
            try:
                model = PrepaymentRelationSchema(**receipt)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Prepayment receipt validation schema failed: {e}")
