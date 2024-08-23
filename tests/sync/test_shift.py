# pylint: disable=duplicate-code
import contextlib
from datetime import datetime

import pytest
from pydantic import ValidationError

from checkbox_sdk.client.synchronous import CheckBoxClient
from checkbox_sdk.exceptions import CheckBoxAPIError
from checkbox_sdk.storage.simple import SessionStorage
from ..models.shift_models import ShiftInfoSchema
from ..models.transactions_models import TransactionsSchema


def test_get_shifts(auth_token, license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    with CheckBoxClient(storage=storage) as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        register = client.cash_registers.get_cash_register(storage.cash_register["id"])
        assert register["is_test"], "Not test cash register"

        # sourcery skip: no-loop-in-tests
        for shift in client.shifts.get_shifts():
            try:
                model = ShiftInfoSchema(**shift)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Shift validation schema failed: {e}")


def test_close_shift_online(auth_token, license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    with CheckBoxClient(storage=storage) as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        current_date = datetime.now().date()
        auto_close_at = datetime.combine(current_date, datetime.strptime("23:55", "%H:%M").time())

        with contextlib.suppress(CheckBoxAPIError):
            shift = client.shifts.create_shift(timeout=5, storage=storage, auto_close_at=auto_close_at.isoformat())
            assert shift["status"] == "OPENED", "Failed to open shift"

        with contextlib.suppress(ValueError):
            z_report = client.shifts.close_shift_online(timeout=5, storage=storage)
            try:
                # sourcery skip: no-conditionals-in-tests
                if z_report:
                    model = TransactionsSchema(**z_report)
                    assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Z report validation schema failed: {e}")


def test_close_shift_by_senior_cashier(auth_token, license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    with CheckBoxClient(storage=storage) as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        current_date = datetime.now().date()
        auto_close_at = datetime.combine(current_date, datetime.strptime("23:55", "%H:%M").time())

        with contextlib.suppress(CheckBoxAPIError):
            shift = client.shifts.create_shift(timeout=5, storage=storage, auto_close_at=auto_close_at.isoformat())
            assert shift["status"] == "OPENED", "Failed to open shift"

        with contextlib.suppress(ValueError):
            z_report = client.shifts.close_shift_by_senior_cashier(shift["id"], timeout=5, storage=storage)
            try:
                # sourcery skip: no-conditionals-in-tests
                if z_report:
                    model = TransactionsSchema(**z_report)
                    assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Z report validation schema failed: {e}")
