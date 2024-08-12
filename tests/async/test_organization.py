import pytest
from pydantic import ValidationError

from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
from checkbox_sdk.exceptions import CheckBoxAPIError
from ..models.organization_models import ReceiptConfigShema, SmsBillingSchema


@pytest.mark.asyncio
async def test_organization_receipt_config(auth_token, license_key):
    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        config = await client.organization.get_organization_receipt_config()
        try:
            model = ReceiptConfigShema(**config)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Organization validation schema failed: {e}")


@pytest.mark.asyncio
async def test_organization_logo(auth_token, license_key):
    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        with pytest.raises(CheckBoxAPIError):
            await client.organization.get_organization_logo()


@pytest.mark.asyncio
async def test_organization_text_logo(auth_token, license_key):
    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        with pytest.raises(CheckBoxAPIError):
            await client.organization.get_organization_text_logo()


@pytest.mark.asyncio
async def test_organization_sms_billing(auth_token, license_key):
    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        # sourcery skip: no-loop-in-tests
        sms_billing = await client.organization.get_organization_sms_billing()
        try:
            model = SmsBillingSchema(**sms_billing)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Sms billing validation schema failed: {e}")
