# pylint: disable=duplicate-code
import contextlib
from datetime import datetime

import pytest
from pydantic import ValidationError

from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
from checkbox_sdk.exceptions import CheckBoxAPIError
from ..models.reports_models import FiscalReportSchema
from ..models.shift_models import ShiftSchema


async def open_shift(client: AsyncCheckBoxClient):
    current_date = datetime.now().date()
    auto_close_at = datetime.combine(current_date, datetime.strptime("23:55", "%H:%M").time())

    with contextlib.suppress(CheckBoxAPIError):
        shift = await client.shifts.create_shift(timeout=5, auto_close_at=auto_close_at.isoformat())
        try:
            model = ShiftSchema(**shift)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Shift validation schema failed: {e}")

        assert shift["status"] == "OPENED", "Failed to open shift"


async def close_shift(client: AsyncCheckBoxClient):
    with contextlib.suppress(ValueError):
        z_report = await client.shifts.close_shift(timeout=5)
        try:
            # sourcery skip: no-conditionals-in-tests
            if z_report:
                model = FiscalReportSchema(**z_report)
                assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Z report validation schema failed: {e}")
