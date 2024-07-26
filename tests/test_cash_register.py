import pytest
from pydantic import ValidationError

from checkbox_sdk.client.sync import CheckBoxClient
from checkbox_sdk.exceptions import CheckBoxError
from checkbox_sdk.storage.simple import SessionStorage
from .models.cash_register_models import CashRegistersSchema, PingSchema


def test_get_cash_registers(auth_token, license_key):
    client = CheckBoxClient()
    client.authenticate_token(auth_token, license_key=license_key)

    # sourcery skip: no-loop-in-tests
    for register in client.get_cash_registers():
        try:
            model = CashRegistersSchema(**register)
            assert model is not None
        except ValidationError as e:
            pytest.fail(f"Cash register validation schema failed: {e}")


def test_get_cash_register(auth_token, license_key):
    # sourcery skip: no-conditionals-in-tests
    if not license_key:
        pytest.fail("License key is empty")

    storage = SessionStorage()
    client = CheckBoxClient(storage=storage)
    client.authenticate_token(auth_token, license_key=license_key)

    register = client.get_cash_register(storage.cash_register["id"])
    assert register["is_test"], "Not test cash register"
    try:
        model = CashRegistersSchema(**register)
        assert model is not None
    except ValidationError as e:
        pytest.fail(f"Cash register validation schema failed: {e}")

    register = client.get_cash_register()
    assert register["is_test"], "Not test cash register"
    try:
        model = CashRegistersSchema(**register)
        assert model is not None
    except ValidationError as e:
        pytest.fail(f"Cash register validation schema failed: {e}")

    storage2 = SessionStorage()
    client2 = CheckBoxClient(storage=storage2)
    client2.authenticate_token(auth_token, storage=storage2)

    with pytest.raises(CheckBoxError):
        client2.get_cash_register()


def test_ping_tax_service(auth_token, license_key):
    # sourcery skip: no-conditionals-in-tests
    if not license_key:
        pytest.fail("License key is empty")

    storage = SessionStorage()
    client = CheckBoxClient(storage=storage)
    client.authenticate_token(auth_token, license_key=license_key)

    ping = client.ping_tax_service()
    try:
        model = PingSchema(**ping)
        assert model is not None
    except ValidationError as e:
        pytest.fail(f"Cash register validation schema failed: {e}")


def test_go_online(auth_token, license_key):
    # sourcery skip: no-conditionals-in-tests
    if not license_key:
        pytest.fail("License key is empty")

    storage = SessionStorage()
    client = CheckBoxClient(storage=storage)
    client.authenticate_token(auth_token, license_key=license_key)

    register = client.get_cash_register(storage.cash_register["id"])
    assert register["is_test"], "Not test cash register"

    response = client.go_online(storage)
    assert response["status"] == "ok"

    fiscal_codes = client.get_offline_codes()
    assert fiscal_codes, "List of fiscal codes is empty"


def test_go_offline(auth_token, license_key):
    # sourcery skip: no-conditionals-in-tests
    if not license_key:
        pytest.fail("License key is empty")

    storage = SessionStorage()
    client = CheckBoxClient(storage=storage)
    client.authenticate_token(auth_token, license_key=license_key)

    register = client.get_cash_register(storage.cash_register["id"])
    assert register["is_test"], "Not test cash register"

    if storage.cash_register["offline_mode"]:
        pytest.skip("Cash register in offline mode")
    else:
        fiscal_codes = client.get_offline_codes()
        assert fiscal_codes, "List of fiscal codes is empty"

        response = client.go_offline(storage=storage)
        assert response["status"] == "ok"
