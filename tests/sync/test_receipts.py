import contextlib
import json
import pathlib
import time
import warnings
from datetime import datetime

import magic
import pytest
from pydantic import ValidationError

from checkbox_sdk.client.synchronous import CheckBoxClient
from checkbox_sdk.exceptions import CheckBoxAPIError
from checkbox_sdk.storage.simple import SessionStorage
from ..models.receipts_models import ReceiptSchema, BulkReceiptSchema
from ..models.shift_models import ShiftSchema, ZReportSchema


def test_get_receipts(auth_token, license_key, client_email, client_phone):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    with CheckBoxClient(storage=storage) as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert storage.cash_register["is_test"], "Not test cash register"

        visualization_tested = False

        # sourcery skip: no-loop-in-tests
        for receipt in client.receipts.get_receipts(storage=storage):
            try:
                model = ReceiptSchema(**receipt)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Receipt validation schema failed: {e}")

            # sourcery skip: no-conditionals-in-tests
            if not visualization_tested and receipt["type"] == "SELL":
                visualization = client.receipts.get_receipt_visualization_html(receipt["id"])
                assert visualization, "HTML visualization is empty"

                time.sleep(0.5)

                mime = magic.Magic(mime=True)

                visualization = client.receipts.get_receipt_visualization_pdf(receipt["id"])
                file_type = mime.from_buffer(visualization)
                assert file_type == "application/pdf"

                time.sleep(0.5)

                visualization = client.receipts.get_receipt_visualization_text(receipt["id"])
                assert visualization, "Text visualization is empty"

                time.sleep(0.5)

                visualization = client.receipts.get_receipt_visualization_png(receipt["id"])
                file_type = mime.from_buffer(visualization)
                assert file_type == "image/png", "Not recognized as PDF"

                time.sleep(0.5)

                visualization = client.receipts.get_receipt_visualization_qrcode(receipt["id"])
                file_type = mime.from_buffer(visualization)
                assert file_type == "image/png", "Not recognized as PNG"

                time.sleep(0.5)

                visualization = client.receipts.get_receipt_visualization_xml(receipt["id"])
                assert visualization, "XML visualization is empty"

                time.sleep(0.5)

                if client_email:
                    response = client.receipts.send_receipt_to_email(receipt["id"], client_email)
                    assert response["ok"] is True
                    time.sleep(0.5)

                if client_phone:
                    response = client.receipts.send_receipt_via_sms(receipt["id"], client_phone)
                    assert response["ok"] is True

                # Calling for one receipt will be enough
                visualization_tested = True


def test_get_receipts_search(auth_token, license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    with CheckBoxClient(storage=storage) as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert storage.cash_register["is_test"], "Not test cash register"

        # sourcery skip: no-loop-in-tests
        for receipt in client.receipts.get_receipts_search(
            storage=storage,
            cash_register_id=[
                storage.cash_register["id"],
            ],
        ):
            try:
                model = ReceiptSchema(**receipt)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Receipt validation schema failed: {e}")


def test_receipts(auth_token, license_key, check_receipt_creation, client_email):
    # sourcery skip: no-conditionals-in-tests
    if not check_receipt_creation:
        pytest.skip("Skip testing receipt creation")

    assert license_key, "License key is empty"

    storage = SessionStorage()
    with CheckBoxClient(storage=storage) as client:
        create_receipt(client, auth_token, license_key, storage, client_email)


def create_receipt(client, auth_token, license_key, storage, client_email):
    client.cashier.authenticate_token(auth_token, license_key=license_key)

    assert storage.cash_register["is_test"], "Not test cash register"

    current_date = datetime.now().date()
    auto_close_at = datetime.combine(current_date, datetime.strptime("23:55", "%H:%M").time())

    with contextlib.suppress(CheckBoxAPIError):
        shift = client.shifts.create_shift(timeout=5, storage=storage, auto_close_at=auto_close_at.isoformat())
        try:
            model = ShiftSchema(**shift)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Shift validation schema failed: {e}")

        assert shift["status"] == "OPENED", "Failed to open shift"

    payment_value = 550 * 100
    payment = {"value": payment_value}
    response = create_service_receipt(client, payment, "SERVICE_IN")
    assert response["payments"][0]["value"] == payment_value

    base_path = pathlib.Path(__file__).resolve().parent.parent
    receipt_path = base_path / "test_data/receipt.json"
    receipt_data = json.loads(receipt_path.resolve().read_text())

    if client_email:
        receipt_data["delivery"] = {"email": "dismine@gmail.com"}

    receipt = client.receipts.create_receipt(
        receipt=receipt_data,
        timeout=5,
        storage=storage,
    )

    try:
        model = ReceiptSchema(**receipt)
        assert model is not None
    except ValidationError as e:  # pragma: no cover
        pytest.fail(f"Receipt validation schema failed: {e}")

    payment = {"value": -payment_value}
    response = create_service_receipt(client, payment, "SERVICE_OUT")
    assert response["payments"][0]["value"] == payment_value

    with contextlib.suppress(ValueError):
        z_report = client.shifts.close_shift(timeout=5, storage=storage)
        try:
            # sourcery skip: no-conditionals-in-tests
            if z_report:
                model = ZReportSchema(**z_report)
                assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Z report validation schema failed: {e}")


def test_bulk_receipts(auth_token, license_key, check_receipt_creation, client_email):
    # sourcery skip: no-conditionals-in-tests
    if not check_receipt_creation:
        pytest.skip("Skip testing receipt creation")

    assert license_key, "License key is empty"

    storage = SessionStorage()
    with CheckBoxClient(storage=storage) as client:
        create_bulk_receipts(client, auth_token, license_key, storage, client_email)


def create_bulk_receipts(client, auth_token, license_key, storage, client_email):
    client.cashier.authenticate_token(auth_token, license_key=license_key)

    assert storage.cash_register["is_test"], "Not test cash register"

    current_date = datetime.now().date()
    auto_close_at = datetime.combine(current_date, datetime.strptime("23:55", "%H:%M").time())

    with contextlib.suppress(CheckBoxAPIError):
        shift = client.shifts.create_shift(timeout=5, storage=storage, auto_close_at=auto_close_at.isoformat())
        try:
            model = ShiftSchema(**shift)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Shift validation schema failed: {e}")

        assert shift["status"] == "OPENED", "Failed to open shift"

    payment_value = 550 * 100
    payment = {"value": payment_value}
    response = create_service_receipt(client, payment, "SERVICE_IN")
    assert response["payments"][0]["value"] == payment_value

    base_path = pathlib.Path(__file__).resolve().parent.parent
    receipt_path = base_path / "test_data/receipt.json"
    receipt_data = json.loads(receipt_path.resolve().read_text())

    if client_email:
        receipt_data["delivery"] = {"email": "dismine@gmail.com"}

    results = client.receipts.create_bulk_receipts(
        receipt_list=[receipt_data],
        storage=storage,
    )

    for result in results:
        try:
            model = BulkReceiptSchema(**result)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Bulk receipt validation schema failed: {e}")

    payment = {"value": -payment_value}
    response = create_service_receipt(client, payment, "SERVICE_OUT")
    assert response["payments"][0]["value"] == payment_value

    with contextlib.suppress(ValueError):
        z_report = client.shifts.close_shift(timeout=5, storage=storage)
        try:
            # sourcery skip: no-conditionals-in-tests
            if z_report:
                model = ZReportSchema(**z_report)
                assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Z report validation schema failed: {e}")


def test_receipts_offline(auth_token, license_key, check_receipt_creation, client_email):
    # sourcery skip: no-conditionals-in-tests
    if not check_receipt_creation:
        pytest.skip("Skip testing receipt creation")

    assert license_key, "License key is empty"

    storage = SessionStorage()
    with CheckBoxClient(storage=storage) as client:
        create_receipt_offline(client, auth_token, license_key, storage, client_email)


def create_receipt_offline(client, auth_token, license_key, storage, client_email):
    client.cashier.authenticate_token(auth_token, license_key=license_key)

    assert storage.cash_register["is_test"], "Not test cash register"

    current_date = datetime.now().date()
    auto_close_at = datetime.combine(current_date, datetime.strptime("23:55", "%H:%M").time())

    with contextlib.suppress(CheckBoxAPIError):
        shift = client.shifts.create_shift(timeout=5, storage=storage, auto_close_at=auto_close_at.isoformat())
        try:
            model = ShiftSchema(**shift)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Shift validation schema failed: {e}")

        assert shift["status"] == "OPENED", "Failed to open shift"

    payment_value = 550 * 100
    payment = {"value": payment_value}
    response = create_service_receipt(client, payment, "SERVICE_IN")
    assert response["payments"][0]["value"] == payment_value

    base_path = pathlib.Path(__file__).resolve().parent.parent
    receipt_path = base_path / "test_data/receipt.json"
    receipt_data = json.loads(receipt_path.resolve().read_text())

    if storage.cash_register["offline_mode"]:
        response = client.cash_registers.go_online(storage)
        assert response["status"] == "ok"

    fiscal_codes = client.cash_registers.get_offline_codes()
    assert fiscal_codes, "List of fiscal codes is empty"

    response = client.cash_registers.go_offline(storage=storage)
    assert response["status"] == "ok"

    receipt_data["fiscal_code"] = fiscal_codes[0]
    receipt_data["fiscal_date"] = datetime.now().isoformat()

    if client_email:
        receipt_data["delivery"] = {"email": "dismine@gmail.com"}

    receipt = client.receipts.create_receipt_offline(
        receipt=receipt_data,
        timeout=5,
        storage=storage,
    )

    try:
        model = ReceiptSchema(**receipt)
        assert model is not None
    except ValidationError as e:  # pragma: no cover
        pytest.fail(f"Receipt validation schema failed: {e}")

    response = client.cash_registers.go_online(storage)
    assert response["status"] == "ok"

    payment = {"value": -payment_value}
    response = create_service_receipt(client, payment, "SERVICE_OUT")
    assert response["payments"][0]["value"] == payment_value

    with contextlib.suppress(ValueError):
        z_report = client.shifts.close_shift(timeout=5, storage=storage)
        try:
            # sourcery skip: no-conditionals-in-tests
            if z_report:
                model = ZReportSchema(**z_report)
                assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Z report validation schema failed: {e}")


def test_external_receipt(auth_token, license_key, check_receipt_creation, client_email):
    # sourcery skip: no-conditionals-in-tests
    if not check_receipt_creation:
        pytest.skip("Skip testing receipt creation")

    assert license_key, "License key is empty"

    storage = SessionStorage()
    with CheckBoxClient(storage=storage) as client:
        create_external_receipt(client, auth_token, license_key, storage, client_email)


def create_external_receipt(client, auth_token, license_key, storage, client_email):
    client.cashier.authenticate_token(auth_token, license_key=license_key)

    assert storage.cash_register["is_test"], "Not test cash register"

    current_date = datetime.now().date()
    auto_close_at = datetime.combine(current_date, datetime.strptime("23:55", "%H:%M").time())

    with contextlib.suppress(CheckBoxAPIError):
        shift = client.shifts.create_shift(timeout=5, storage=storage, auto_close_at=auto_close_at.isoformat())
        try:
            model = ShiftSchema(**shift)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Shift validation schema failed: {e}")

        assert shift["status"] == "OPENED", "Failed to open shift"

    payment_value = 550 * 100
    payment = {"value": payment_value}
    response = create_service_receipt(client, payment, "SERVICE_IN")
    assert response["payments"][0]["value"] == payment_value

    base_path = pathlib.Path(__file__).resolve().parent.parent
    receipt_path = base_path / "test_data/external_receipt.json"
    receipt_data = json.loads(receipt_path.resolve().read_text())

    if storage.cash_register["offline_mode"]:
        response = client.cash_registers.go_online(storage)
        assert response["status"] == "ok"

    fiscal_codes = client.cash_registers.get_offline_codes()
    assert fiscal_codes, "List of fiscal codes is empty"

    response = client.cash_registers.go_offline(storage=storage)
    assert response["status"] == "ok"

    receipt_data["fiscal_code"] = fiscal_codes[0]
    receipt_data["fiscal_date"] = datetime.now().isoformat()

    if client_email:
        receipt_data["delivery"] = {"email": "dismine@gmail.com"}

    receipt = client.receipts.create_external_receipt(
        receipt=receipt_data,
        timeout=5,
        storage=storage,
    )

    try:
        model = ReceiptSchema(**receipt)
        assert model is not None
    except ValidationError as e:  # pragma: no cover
        pytest.fail(f"Receipt validation schema failed: {e}")

    response = client.cash_registers.go_online(storage)
    assert response["status"] == "ok"

    payment = {"value": -payment_value}
    response = create_service_receipt(client, payment, "SERVICE_OUT")
    assert response["payments"][0]["value"] == payment_value

    with contextlib.suppress(ValueError):
        z_report = client.shifts.close_shift(timeout=5, storage=storage)
        try:
            # sourcery skip: no-conditionals-in-tests
            if z_report:
                model = ZReportSchema(**z_report)
                assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Z report validation schema failed: {e}")


def create_service_receipt(client, payment, type):
    result = client.receipts.create_service_receipt(payment=payment, timeout=5)
    try:
        model = ReceiptSchema(**result)
        assert model is not None
    except ValidationError as e:  # pragma: no cover
        pytest.fail(f"Service receipt validation schema failed: {e}")

    assert result["type"] == type
    assert result["status"] == "DONE"
    return result


def test_service_currency_receipt(auth_token, license_key, check_receipt_creation):
    # sourcery skip: no-conditionals-in-tests
    if not check_receipt_creation:
        pytest.skip("Skip testing receipt creation")

    assert license_key, "License key is empty"

    storage = SessionStorage()
    with CheckBoxClient(storage=storage) as client:
        create_service_currency_receipt(client, auth_token, license_key, storage)


def create_service_currency_receipt(client, auth_token, license_key, storage):
    client.cashier.authenticate_token(auth_token, license_key=license_key)

    assert storage.cash_register["is_test"], "Not test cash register"

    current_date = datetime.now().date()
    auto_close_at = datetime.combine(current_date, datetime.strptime("23:55", "%H:%M").time())

    with contextlib.suppress(CheckBoxAPIError):
        shift = client.shifts.create_shift(timeout=5, storage=storage, auto_close_at=auto_close_at.isoformat())
        try:
            model = ShiftSchema(**shift)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Shift validation schema failed: {e}")

        assert shift["status"] == "OPENED", "Failed to open shift"

    payment = {
        "type": "ADVANCE",
        "currencies": [{"currency": "UAH", "value": 1}],
    }

    try:
        receipt = client.receipts.create_service_currency_receipt(
            receipt=payment,
            timeout=5,
            storage=storage,
        )
        try:
            model = ReceiptSchema(**receipt)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Receipt validation schema failed: {e}")
    except CheckBoxAPIError as e:
        if e.status == 400:
            warnings.warn("Not supported cash register type")
        else:
            raise

    with contextlib.suppress(ValueError):
        z_report = client.shifts.close_shift(timeout=5, storage=storage)
        try:
            # sourcery skip: no-conditionals-in-tests
            if z_report:
                model = ZReportSchema(**z_report)
                assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Z report validation schema failed: {e}")


def test_currency_exchange_receipt(auth_token, license_key, check_receipt_creation):
    # sourcery skip: no-conditionals-in-tests
    if not check_receipt_creation:
        pytest.skip("Skip testing receipt creation")

    assert license_key, "License key is empty"

    storage = SessionStorage()
    with CheckBoxClient(storage=storage) as client:
        create_currency_exchange_receipt(client, auth_token, license_key, storage)


def create_currency_exchange_receipt(client, auth_token, license_key, storage):
    client.cashier.authenticate_token(auth_token, license_key=license_key)

    assert storage.cash_register["is_test"], "Not test cash register"

    current_date = datetime.now().date()
    auto_close_at = datetime.combine(current_date, datetime.strptime("23:55", "%H:%M").time())

    with contextlib.suppress(CheckBoxAPIError):
        shift = client.shifts.create_shift(timeout=5, storage=storage, auto_close_at=auto_close_at.isoformat())
        try:
            model = ShiftSchema(**shift)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Shift validation schema failed: {e}")

        assert shift["status"] == "OPENED", "Failed to open shift"

    payment = {
        "type": "SELL",
        "sell": {"currency": "USD", "value": 1},
        "delivery": {
            "email": "dismine@gmail.com",
        },
    }

    try:
        receipt = client.receipts.create_currency_exchange_receipt(
            receipt=payment,
            timeout=5,
            storage=storage,
        )
        try:
            model = ReceiptSchema(**receipt)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Receipt validation schema failed: {e}")
    except CheckBoxAPIError as e:
        if e.status == 400:
            warnings.warn("Not supported cash register type")
        else:
            raise

    with contextlib.suppress(ValueError):
        z_report = client.shifts.close_shift(timeout=5, storage=storage)
        try:
            # sourcery skip: no-conditionals-in-tests
            if z_report:
                model = ZReportSchema(**z_report)
                assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Z report validation schema failed: {e}")
