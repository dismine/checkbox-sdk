from checkbox_sdk.client.sync import CheckBoxClient
from checkbox_sdk.storage.simple import SessionStorage
from checkbox_sdk.exceptions import CheckBoxAPIError
import pytest


def test_authenticate_login(login, license_key):
    storage = SessionStorage()
    client = CheckBoxClient(storage=storage)
    client.authenticate(login=login, password=login, license_key=license_key)
    assert isinstance(storage.token, str), "The result should be a string"
    assert storage.token, "The token should be a non-empty string"

    token = storage.token

    client.sign_out(storage)
    assert storage.shift is None, "The shift should be None"
    assert storage.cashier is None, "The cashier should be None"
    assert storage.token is None, "The token should be None"

    with pytest.raises(CheckBoxAPIError):
        client.authenticate_token(token, license_key=license_key, storage=storage)


def test_authenticate_pin_code(pincode, license_key):
    storage = SessionStorage()
    client = CheckBoxClient(storage=storage)
    client.authenticate_pin_code(pin_code=pincode, license_key=license_key)
    assert isinstance(storage.token, str), "The result should be a string"
    assert storage.token, "The token should be a non-empty string"

    token = storage.token

    client.sign_out(storage)
    assert storage.shift is None, "The shift should be None"
    assert storage.cashier is None, "The cashier should be None"
    assert storage.token is None, "The token should be None"

    with pytest.raises(CheckBoxAPIError):
        client.authenticate_token(token, license_key=license_key, storage=storage)


def test_authenticate_token(pincode, license_key):
    storage = SessionStorage()
    client = CheckBoxClient(storage=storage)
    client.authenticate_pin_code(pin_code=pincode, license_key=license_key)
    assert isinstance(storage.token, str), "The result should be a string"
    assert storage.token, "The token should be a non-empty string"

    storage2 = SessionStorage()
    client2 = CheckBoxClient(storage=storage2)
    client2.authenticate_token(storage.token, license_key=license_key, storage=storage2)
    assert isinstance(storage2.token, str), "The result should be a string"
    assert storage2.token, "The token should be a non-empty string"
    assert storage.token == storage2.token, f"Tokens are not equal: {storage.token} != {storage2.token}"

    client2.sign_out(storage)
    assert storage.shift is None, "The shift should be None"
    assert storage.cashier is None, "The cashier should be None"
    assert storage.token is None, "The token should be None"
