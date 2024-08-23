# pylint: disable=duplicate-code
import pytest
from pydantic import ValidationError

from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
from ..models.transactions_models import TransactionsSchema


@pytest.mark.asyncio
async def test_get_transactions(auth_token, license_key):
    assert license_key, "License key is empty"

    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        # sourcery skip: no-loop-in-tests
        async for transaction in client.transactions.get_transactions():
            try:
                model = TransactionsSchema(**transaction)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Transaction validation schema failed: {e}")
