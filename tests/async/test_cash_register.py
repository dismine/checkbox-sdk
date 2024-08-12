import pytest
from pydantic import ValidationError

from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
from checkbox_sdk.exceptions import CheckBoxError
from checkbox_sdk.storage.simple import SessionStorage
from ..models.cash_register_models import CashRegistersSchema, PingSchema, OfflineTimeSchema
from ..models.shift_models import ShiftSchema


@pytest.mark.asyncio
async def test_get_cash_registers(auth_token, license_key):
    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        # sourcery skip: no-loop-in-tests
        async for register in client.cash_registers.get_cash_registers():
            try:
                model = CashRegistersSchema(**register)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Cash register validation schema failed: {e}")


@pytest.mark.asyncio
async def test_get_cash_register(auth_token, license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    async with AsyncCheckBoxClient(storage=storage) as client:
        await get_cash_register(client, auth_token, license_key, storage)

    storage2 = SessionStorage()
    async with AsyncCheckBoxClient(storage=storage2) as client2:
        await client2.cashier.authenticate_token(auth_token, storage=storage2)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        with pytest.raises(CheckBoxError):
            await client2.cash_registers.get_cash_register()


async def get_cash_register(client, auth_token, license_key, storage):
    await client.cashier.authenticate_token(auth_token, license_key=license_key)

    register = await client.cash_registers.get_cash_register(storage.cash_register["id"])
    assert register["is_test"], "Not test cash register"
    try:
        model = CashRegistersSchema(**register)
        assert model is not None
    except ValidationError as e:  # pragma: no cover
        pytest.fail(f"Cash register validation schema failed: {e}")

    register = await client.cash_registers.get_cash_register()
    assert register["is_test"], "Not test cash register"
    try:
        model = CashRegistersSchema(**register)
        assert model is not None
    except ValidationError as e:  # pragma: no cover
        pytest.fail(f"Cash register validation schema failed: {e}")


@pytest.mark.asyncio
async def test_ping_tax_service(auth_token, license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    async with AsyncCheckBoxClient(storage=storage) as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        ping = await client.cash_registers.ping_tax_service()
        try:
            model = PingSchema(**ping)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Cash register validation schema failed: {e}")


@pytest.mark.asyncio
async def test_go_online(auth_token, license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    async with AsyncCheckBoxClient(storage=storage) as client:
        await get_offline_codes(client, auth_token, license_key, storage)


async def get_offline_codes(client, auth_token, license_key, storage):
    await client.cashier.authenticate_token(auth_token, license_key=license_key)

    register = await client.cash_registers.get_cash_register(storage.cash_register["id"])
    assert register["is_test"], "Not test cash register"

    response = await client.cash_registers.go_online(storage)
    assert response["status"] == "ok"

    fiscal_codes = await client.cash_registers.get_offline_codes()
    assert fiscal_codes, "List of fiscal codes is empty"


@pytest.mark.asyncio
async def test_go_offline(auth_token, license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    async with AsyncCheckBoxClient(storage=storage) as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        register = await client.cash_registers.get_cash_register(storage.cash_register["id"])
        assert register["is_test"], "Not test cash register"

        if storage.cash_register["offline_mode"]:
            pytest.skip("Cash register in offline mode")  # pragma: no cover
        else:
            fiscal_codes = await client.cash_registers.get_offline_codes()
            assert fiscal_codes, "List of fiscal codes is empty"

            response = await client.cash_registers.go_offline(storage=storage)
            assert response["status"] == "ok"


@pytest.mark.asyncio
async def test_get_offline_time(license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    async with AsyncCheckBoxClient(storage=storage) as client:
        client.set_license_key(storage, license_key)

        offline_time = await client.cash_registers.get_offline_time()
        try:
            model = OfflineTimeSchema(**offline_time)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Offline time validation schema failed: {e}")


@pytest.mark.asyncio
async def test_get_cash_register_shifts(license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    async with AsyncCheckBoxClient() as client:
        client.set_license_key(storage, license_key)

        # sourcery skip: no-loop-in-tests
        async for register in client.cash_registers.get_cash_register_shifts(storage=storage):
            try:
                model = ShiftSchema(**register)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Shift validation schema failed: {e}")
