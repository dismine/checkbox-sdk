# pylint: disable=duplicate-code
import contextlib
from datetime import datetime

import pytest
import pytz
from pydantic import ValidationError

from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
from checkbox_sdk.exceptions import CheckBoxAPIError
from checkbox_sdk.methods.base import BaseMethod
from ..models.reports_models import FiscalReportSchema
from ..models.shift_models import ShiftSchema


async def open_shift(client: AsyncCheckBoxClient):
    tz = pytz.timezone("Europe/Kyiv")
    current_date = datetime.now(tz).date()
    closing_time = datetime.strptime("23:55", "%H:%M").time()
    auto_close_at = tz.localize(datetime.combine(current_date, closing_time))

    with contextlib.suppress(CheckBoxAPIError):
        shift = await client.shifts.create_shift(
            timeout=5, auto_close_at=BaseMethod.format_datetime_to_iso_with_ms(auto_close_at)
        )
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
