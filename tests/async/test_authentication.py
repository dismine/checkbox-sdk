import pytest
from pydantic import ValidationError

from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
from checkbox_sdk.exceptions import CheckBoxAPIError
from checkbox_sdk.storage.simple import SessionStorage
from ..models.cash_register_models import CashRegistersInfoSchema


@pytest.mark.asyncio
async def test_authenticate_login(login, license_key):
    storage = SessionStorage()
    async with AsyncCheckBoxClient(storage=storage) as client:
        await client.cashier.authenticate(login=login, password=login, license_key=license_key)
        assert isinstance(storage.token, str), "The result should be a string"
        assert storage.token, "The token should be a non-empty string"

        # sourcery skip: no-conditionals-in-tests
        if license_key:
            assert storage.cash_register["is_test"], "Not test cash register"

            try:
                model = CashRegistersInfoSchema(**storage.cash_register)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Cash register validation schema failed: {e}")

        token = storage.token

        await client.cashier.sign_out(storage)
        assert storage.shift is None, "The shift should be None"
        assert storage.cashier is None, "The cashier should be None"
        assert storage.token is None, "The token should be None"

        with pytest.raises(CheckBoxAPIError):
            await client.cashier.authenticate_token(token, license_key=license_key, storage=storage)


@pytest.mark.asyncio
async def test_authenticate_pin_code(pincode, license_key):
    storage = SessionStorage()
    async with AsyncCheckBoxClient(storage=storage) as client:
        await client.cashier.authenticate_pin_code(pin_code=pincode, license_key=license_key)
        assert isinstance(storage.token, str), "The result should be a string"
        assert storage.token, "The token should be a non-empty string"

        # sourcery skip: no-conditionals-in-tests
        if license_key:
            assert storage.cash_register["is_test"], "Not test cash register"

            try:
                model = CashRegistersInfoSchema(**storage.cash_register)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Cash register validation schema failed: {e}")

        token = storage.token

        await client.cashier.sign_out(storage)
        assert storage.shift is None, "The shift should be None"
        assert storage.cashier is None, "The cashier should be None"
        assert storage.token is None, "The token should be None"

        with pytest.raises(CheckBoxAPIError):
            await client.cashier.authenticate_token(token, license_key=license_key, storage=storage)


@pytest.mark.asyncio
async def test_authenticate_token(pincode, license_key):
    storage = SessionStorage()
    async with AsyncCheckBoxClient(storage=storage) as client:
        await client.cashier.authenticate_pin_code(pin_code=pincode, license_key=license_key)
        assert isinstance(storage.token, str), "The result should be a string"
        assert storage.token, "The token should be a non-empty string"

    storage2 = SessionStorage()
    async with AsyncCheckBoxClient(storage=storage) as client2:
        await authenticate_token(client2, storage.token, license_key, storage2)


async def authenticate_token(client, token, license_key, storage2):
    await client.cashier.authenticate_token(token, license_key=license_key, storage=storage2)
    assert isinstance(storage2.token, str), "The result should be a string"
    assert storage2.token, "The token should be a non-empty string"
    assert token == storage2.token, f"Tokens are not equal: {token} != {storage2.token}"

    # sourcery skip: no-conditionals-in-tests
    if license_key:
        assert storage2.cash_register["is_test"], "Not test cash register"

        try:
            model = CashRegistersInfoSchema(**storage2.cash_register)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Cash register validation schema failed: {e}")

    await client.cashier.sign_out(storage2)
    assert storage2.shift is None, "The shift should be None"
    assert storage2.cashier is None, "The cashier should be None"
    assert storage2.token is None, "The token should be None"
