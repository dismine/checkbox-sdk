import pytest
from pydantic import ValidationError

from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
from .base import open_shift, close_shift
from ..models.shift_models import RateSchema


@pytest.mark.asyncio
async def test_currency_rates(auth_token, license_key):
    assert license_key, "License key is empty"

    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        await open_shift(client)

        rate_data = {
            "code": "980",
            "sell": 0,
            "buy": 0,
            "regulator": 0,
        }

        # sourcery skip: no-loop-in-tests
        for rate in await client.currency.setup_currency_rates(rates=[rate_data]):
            try:
                model = RateSchema(**rate)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Rate validation schema failed: {e}")

        # sourcery skip: no-loop-in-tests
        for rate in await client.currency.get_currency_rates():
            try:
                model = RateSchema(**rate)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Rate validation schema failed: {e}")

        rate = await client.currency.get_currency_rate("980")
        try:
            model = RateSchema(**rate)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Rate validation schema failed: {e}")

        await close_shift(client)
