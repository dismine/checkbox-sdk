import pytest
from pydantic import ValidationError

from checkbox_sdk.client.synchronous import CheckBoxClient
from checkbox_sdk.exceptions import CheckBoxError
from checkbox_sdk.storage.simple import SessionStorage
from ..models.cash_register_models import CashRegistersSchema, PingSchema


def test_get_cash_registers(auth_token, license_key):
    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        # sourcery skip: no-loop-in-tests
        for register in client.cash_registers.get_cash_registers():
            try:
                model = CashRegistersSchema(**register)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Cash register validation schema failed: {e}")


def test_get_cash_register(auth_token, license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    with CheckBoxClient(storage=storage) as client:
        get_cash_register(client, auth_token, license_key, storage)

    storage2 = SessionStorage()
    with CheckBoxClient(storage=storage2) as client2:
        client2.cashier.authenticate_token(auth_token, storage=storage2)

        with pytest.raises(CheckBoxError):
            client2.cash_registers.get_cash_register()


def get_cash_register(client, auth_token, license_key, storage):
    client.cashier.authenticate_token(auth_token, license_key=license_key)

    register = client.cash_registers.get_cash_register(storage.cash_register["id"])
    assert register["is_test"], "Not test cash register"
    try:
        model = CashRegistersSchema(**register)
        assert model is not None
    except ValidationError as e:  # pragma: no cover
        pytest.fail(f"Cash register validation schema failed: {e}")

    register = client.cash_registers.get_cash_register()
    assert register["is_test"], "Not test cash register"
    try:
        model = CashRegistersSchema(**register)
        assert model is not None
    except ValidationError as e:  # pragma: no cover
        pytest.fail(f"Cash register validation schema failed: {e}")


def test_ping_tax_service(auth_token, license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    with CheckBoxClient(storage=storage) as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        ping = client.cash_registers.ping_tax_service()
        try:
            model = PingSchema(**ping)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Cash register validation schema failed: {e}")


def test_go_online(auth_token, license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    with CheckBoxClient(storage=storage) as client:
        get_offline_codes(client, auth_token, license_key, storage)


def get_offline_codes(client, auth_token, license_key, storage):
    client.cashier.authenticate_token(auth_token, license_key=license_key)

    register = client.cash_registers.get_cash_register(storage.cash_register["id"])
    assert register["is_test"], "Not test cash register"

    response = client.cash_registers.go_online(storage)
    assert response["status"] == "ok"

    fiscal_codes = client.cash_registers.get_offline_codes()
    assert fiscal_codes, "List of fiscal codes is empty"


def test_go_offline(auth_token, license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    with CheckBoxClient(storage=storage) as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        register = client.cash_registers.get_cash_register(storage.cash_register["id"])
        assert register["is_test"], "Not test cash register"

        if storage.cash_register["offline_mode"]:
            pytest.skip("Cash register in offline mode")  # pragma: no cover
        else:
            fiscal_codes = client.cash_registers.get_offline_codes()
            assert fiscal_codes, "List of fiscal codes is empty"

            response = client.cash_registers.go_offline(storage=storage)
            assert response["status"] == "ok"
