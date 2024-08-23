# pylint: disable=duplicate-code
import pytest
from pydantic import ValidationError

from checkbox_sdk.client.synchronous import CheckBoxClient
from checkbox_sdk.storage.simple import SessionStorage
from ..models.tax_models import TaxSchema


def test_tax(license_key):
    storage = SessionStorage()
    with CheckBoxClient() as client:
        client.set_license_key(storage=storage, license_key=license_key)

        # sourcery skip: no-loop-in-tests
        for tax in client.tax.get_all_taxes(storage=storage):
            try:
                model = TaxSchema(**tax)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Tax validation schema failed: {e}")


def test_cashier_tax(auth_token, license_key):
    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        # sourcery skip: no-loop-in-tests
        for tax in client.cashier.get_all_taxes_by_cashier():
            try:
                model = TaxSchema(**tax)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Tax validation schema failed: {e}")
