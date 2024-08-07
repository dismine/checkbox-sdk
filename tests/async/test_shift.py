import pytest
from pydantic import ValidationError

from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
from checkbox_sdk.storage.simple import SessionStorage
from ..models.shift_models import ShiftInfoSchema


@pytest.mark.asyncio
async def test_get_shifts(auth_token, license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    async with AsyncCheckBoxClient(storage=storage) as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        register = await client.cash_registers.get_cash_register(storage.cash_register["id"])
        assert register["is_test"], "Not test cash register"

        # sourcery skip: no-loop-in-tests
        async for shift in client.shifts.get_shifts():
            try:
                model = ShiftInfoSchema(**shift)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Shift validation schema failed: {e}")
