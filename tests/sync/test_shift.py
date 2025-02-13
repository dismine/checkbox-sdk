# pylint: disable=duplicate-code
import contextlib
from datetime import datetime

import pytest
import pytz
from pydantic import ValidationError

from checkbox_sdk.client.synchronous import CheckBoxClient
from checkbox_sdk.exceptions import CheckBoxAPIError
from checkbox_sdk.methods.base import BaseMethod
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

        tz = pytz.timezone("Europe/Kyiv")
        current_date = datetime.now(tz).date()
        closing_time = datetime.strptime("23:55", "%H:%M").time()
        auto_close_at = tz.localize(datetime.combine(current_date, closing_time))

        with contextlib.suppress(CheckBoxAPIError):
            shift = client.shifts.create_shift(
                timeout=5, storage=storage, auto_close_at=BaseMethod.format_datetime_to_iso_with_ms(auto_close_at)
            )
            assert shift["status"] == "OPENED", "Failed to open shift"

        with contextlib.suppress(ValueError):
            z_report = client.shifts.close_shift_online(timeout=5, storage=storage)
            try:
                if z_report:  # sourcery skip: no-conditionals-in-tests
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

        tz = pytz.timezone("Europe/Kyiv")
        current_date = datetime.now(tz).date()
        closing_time = datetime.strptime("23:55", "%H:%M").time()
        auto_close_at = tz.localize(datetime.combine(current_date, closing_time))

        with contextlib.suppress(CheckBoxAPIError):
            shift = client.shifts.create_shift(
                timeout=5, storage=storage, auto_close_at=BaseMethod.format_datetime_to_iso_with_ms(auto_close_at)
            )
            assert shift["status"] == "OPENED", "Failed to open shift"

        with contextlib.suppress(ValueError):
            z_report = client.shifts.close_shift_by_senior_cashier(shift["id"], timeout=5, storage=storage)
            try:
                if z_report:  # sourcery skip: no-conditionals-in-tests
                    model = TransactionsSchema(**z_report)
                    assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Z report validation schema failed: {e}")
