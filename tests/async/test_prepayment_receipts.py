import contextlib
import json
import pathlib
from datetime import datetime

import pytest
from pydantic import ValidationError

from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
from checkbox_sdk.exceptions import CheckBoxAPIError
from checkbox_sdk.storage.simple import SessionStorage
from ..models.prepayment_receipts_models import PrepaymentRelationSchema
from ..models.receipts_models import ReceiptSchema
from ..models.shift_models import ShiftSchema, ZReportSchema


@pytest.mark.asyncio
async def test_create_prepayment_receipt(auth_token, license_key, check_receipt_creation, client_email):
    if not check_receipt_creation:
        pytest.skip("Skip testing receipt creation")

    assert license_key, "License key is empty"

    storage = SessionStorage()
    async with AsyncCheckBoxClient(storage=storage) as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert storage.cash_register["is_test"], "Not test cash register"

        current_date = datetime.now().date()
        auto_close_at = datetime.combine(current_date, datetime.strptime("23:55", "%H:%M").time())

        with contextlib.suppress(CheckBoxAPIError):
            shift = await client.shifts.create_shift(
                timeout=5, storage=storage, auto_close_at=auto_close_at.isoformat()
            )
            try:
                model = ShiftSchema(**shift)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Shift validation schema failed: {e}")

            assert shift["status"] == "OPENED", "Failed to open shift"

        base_path = pathlib.Path(__file__).resolve().parent.parent
        receipt_path = base_path / "test_data/prepayment_receipt.json"
        receipt_data = json.loads(receipt_path.resolve().read_text())

        if client_email:
            receipt_data["delivery"] = {"email": client_email}

        prepayment_receipt = await client.prepayment_receipts.create_prepayment_receipt(
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

        after_payment_receipt = await client.prepayment_receipts.create_after_payment_receipt(
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

        relation = await client.prepayment_receipts.get_prepayment_relation(
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

        receipts_chain = await client.prepayment_receipts.get_prepayment_receipts_chain(
            relation_id=prepayment_receipt["pre_payment_relation_id"],
            data=chain_data,
            storage=storage,
        )

        for receipt in receipts_chain:
            try:
                model = ReceiptSchema(**receipt)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Receipt validation schema failed: {e}")

        with contextlib.suppress(ValueError):
            z_report = await client.shifts.close_shift(timeout=5, storage=storage)
            try:
                if z_report:
                    model = ZReportSchema(**z_report)
                    assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Z report validation schema failed: {e}")


@pytest.mark.asyncio
async def test_get_pre_payment_relations_search(auth_token, license_key):
    assert license_key, "License key is empty"

    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        # sourcery skip: no-loop-in-tests
        async for receipt in client.prepayment_receipts.get_pre_payment_relations_search():
            try:
                model = PrepaymentRelationSchema(**receipt)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Prepayment receipt validation schema failed: {e}")
