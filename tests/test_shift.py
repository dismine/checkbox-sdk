import contextlib
from datetime import datetime

import pytest
from pydantic import ValidationError

from checkbox_sdk.client.sync import CheckBoxClient
from checkbox_sdk.exceptions import CheckBoxAPIError
from checkbox_sdk.storage.simple import SessionStorage
from .models.shift_models import ShiftInfoSchema, ShiftSchema, ZReportSchema


def test_get_shifts(auth_token, license_key):
    # sourcery skip: no-conditionals-in-tests
    if not license_key:
        pytest.fail("License key is empty")

    storage = SessionStorage()
    client = CheckBoxClient(storage=storage)
    client.authenticate_token(auth_token, license_key=license_key)

    register = client.get_cash_register(storage.cash_register["id"])
    assert register["is_test"], "Not test cash register"

    # sourcery skip: no-loop-in-tests
    for shift in client.get_shifts():
        try:
            model = ShiftInfoSchema(**shift)
            assert model is not None
        except ValidationError as e:
            pytest.fail(f"Shift validation schema failed: {e}")


def test_shift(auth_token, license_key):
    # sourcery skip: no-conditionals-in-tests
    if not license_key:
        pytest.fail("License key is empty")

    storage = SessionStorage()
    client = CheckBoxClient(storage=storage)
    client.authenticate_token(auth_token, license_key=license_key)

    register = client.get_cash_register(storage.cash_register["id"])
    assert register["is_test"], "Not test cash register"

    current_date = datetime.now().date()
    auto_close_at = datetime.combine(current_date, datetime.strptime("23:55", "%H:%M").time())

    with contextlib.suppress(CheckBoxAPIError):
        shift = client.create_shift(timeout=5, storage=storage, auto_close_at=auto_close_at.isoformat())
        try:
            model = ShiftSchema(**shift)
            assert model is not None
        except ValidationError as e:
            pytest.fail(f"Shift validation schema failed: {e}")

        assert shift["status"] == "OPENED", "Failed to open shift"

    with contextlib.suppress(ValueError):
        z_report = client.close_shift(timeout=5, storage=storage)
        try:
            if z_report:
                model = ZReportSchema(**z_report)
                assert model is not None
        except ValidationError as e:
            pytest.fail(f"Z report validation schema failed: {e}")
