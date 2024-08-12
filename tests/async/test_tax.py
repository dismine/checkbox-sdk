import pytest
from pydantic import ValidationError

from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
from checkbox_sdk.storage.simple import SessionStorage
from ..models.tax_models import TaxSchema


@pytest.mark.asyncio
async def test_tax(license_key):
    storage = SessionStorage()
    async with AsyncCheckBoxClient() as client:
        client.set_license_key(storage=storage, license_key=license_key)

        taxes = await client.tax.get_all_taxes(storage=storage)  # Await the coroutine to get the list of taxes

        # sourcery skip: no-loop-in-tests
        for tax in taxes:
            try:
                model = TaxSchema(**tax)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Tax validation schema failed: {e}")


@pytest.mark.asyncio
async def test_cashier_tax(auth_token, license_key):
    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        taxes = await client.cashier.get_all_taxes_by_cashier()  # Await the coroutine to get the list of taxes

        # sourcery skip: no-loop-in-tests
        for tax in taxes:
            try:
                model = TaxSchema(**tax)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Tax validation schema failed: {e}")
