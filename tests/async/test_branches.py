# pylint: disable=duplicate-code
import pytest
from pydantic import ValidationError

from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
from ..models.cash_register_models import BranchSchema


@pytest.mark.asyncio
async def test_get_all_branches(auth_token, license_key):
    assert license_key, "License key is empty"

    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        # sourcery skip: no-loop-in-tests
        async for branch in client.branches.get_all_branches():
            try:
                model = BranchSchema(**branch)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Branch validation schema failed: {e}")
