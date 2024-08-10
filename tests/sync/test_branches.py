import pytest
from pydantic import ValidationError

from checkbox_sdk.client.synchronous import CheckBoxClient
from ..models.cash_register_models import BranchSchema


def test_get_all_branches(auth_token, license_key):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        # sourcery skip: no-loop-in-tests
        for branch in client.branches.get_all_branches():
            try:
                model = BranchSchema(**branch)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Branch validation schema failed: {e}")
