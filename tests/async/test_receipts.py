import contextlib
import json
import pathlib
from datetime import datetime

import pytest
from pydantic import ValidationError

from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
from checkbox_sdk.exceptions import CheckBoxAPIError
from checkbox_sdk.storage.simple import SessionStorage
from ..models.receipts_models import ReceiptSchema
from ..models.shift_models import ShiftSchema, ZReportSchema


@pytest.mark.asyncio
async def test_get_receipts(auth_token, license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    async with AsyncCheckBoxClient(storage=storage) as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert storage.cash_register["is_test"], "Not test cash register"

        # sourcery skip: no-loop-in-tests
        async for receipt in client.receipts.get_receipts(storage=storage):
            try:
                model = ReceiptSchema(**receipt)
                assert model is not None
            except ValidationError as e:
                pytest.fail(f"Receipt validation schema failed: {e}")


@pytest.mark.asyncio
async def test_get_receipts_search(auth_token, license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    async with AsyncCheckBoxClient(storage=storage) as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert storage.cash_register["is_test"], "Not test cash register"

        # sourcery skip: no-loop-in-tests
        async for receipt in client.receipts.get_receipts_search(
            storage=storage,
            cash_register_id=[
                storage.cash_register["id"],
            ],
        ):
            try:
                model = ReceiptSchema(**receipt)
                assert model is not None
            except ValidationError as e:
                pytest.fail(f"Receipt validation schema failed: {e}")


@pytest.mark.asyncio
async def test_receipts(auth_token, license_key, check_receipt_creation):
    # sourcery skip: no-conditionals-in-tests
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
            except ValidationError as e:
                pytest.fail(f"Shift validation schema failed: {e}")

            assert shift["status"] == "OPENED", "Failed to open shift"

        payment_value = 550 * 100
        payment = {"value": payment_value}
        response = await create_service_receipt(client, payment, "SERVICE_IN")
        assert response["payments"][0]["value"] == payment_value

        base_path = pathlib.Path(__file__).resolve().parent.parent
        receipt_path = base_path / "test_data/receipt.json"
        receipt_data = json.loads(receipt_path.resolve().read_text())
        receipt = await client.receipts.create_receipt(
            receipt=receipt_data,
            timeout=5,
            storage=storage,
        )

        try:
            model = ReceiptSchema(**receipt)
            assert model is not None
        except ValidationError as e:
            pytest.fail(f"Receipt validation schema failed: {e}")

        payment = {"value": -payment_value}
        response = await create_service_receipt(client, payment, "SERVICE_OUT")
        assert response["payments"][0]["value"] == payment_value

        with contextlib.suppress(ValueError):
            z_report = await client.shifts.close_shift(timeout=5, storage=storage)
            try:
                # sourcery skip: no-conditionals-in-tests
                if z_report:
                    model = ZReportSchema(**z_report)
                    assert model is not None
            except ValidationError as e:
                pytest.fail(f"Z report validation schema failed: {e}")


async def create_service_receipt(client, payment, type):
    result = await client.receipts.create_service_receipt(payment=payment, timeout=5)
    try:
        model = ReceiptSchema(**result)
        assert model is not None
    except ValidationError as e:
        pytest.fail(f"Service receipt validation schema failed: {e}")

    assert result["type"] == type
    assert result["status"] == "DONE"
    return result
