import pytest
from pydantic import ValidationError

from checkbox_sdk.client.sync import CheckBoxClient
from .models.cash_register_models import CashRegistersSchema


def test_cash_registers(auth_token, license_key):
    client = CheckBoxClient()
    client.authenticate_token(auth_token, license_key=license_key)

    # sourcery skip: no-loop-in-tests
    for register in client.get_cash_registers():
        try:
            model = CashRegistersSchema(**register)
            assert model is not None
        except ValidationError as e:
            pytest.fail(f"Cash register validation schema failed: {e}")
