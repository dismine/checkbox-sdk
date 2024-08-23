# pylint: disable=duplicate-code
import pytest
from pydantic import ValidationError

from checkbox_sdk.client.synchronous import CheckBoxClient
from ..models.transactions_models import TransactionsSchema


def test_get_transactions(auth_token, license_key):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        # sourcery skip: no-loop-in-tests
        for transaction in client.transactions.get_transactions():
            try:
                model = TransactionsSchema(**transaction)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Transaction validation schema failed: {e}")
