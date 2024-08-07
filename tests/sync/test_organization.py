import pytest
from pydantic import ValidationError

from checkbox_sdk.client.synchronous import CheckBoxClient
from checkbox_sdk.exceptions import CheckBoxAPIError
from ..models.organization_models import ReceiptConfigShema, SmsBillingSchema


def test_organization_receipt_config(auth_token, license_key):
    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        config = client.organization.get_organization_receipt_config()
        try:
            model = ReceiptConfigShema(**config)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Organization validation schema failed: {e}")


def test_organization_logo(auth_token, license_key):
    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        with pytest.raises(CheckBoxAPIError):
            client.organization.get_organization_logo()


def test_organization_text_logo(auth_token, license_key):
    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        with pytest.raises(CheckBoxAPIError):
            client.organization.get_organization_text_logo()


def test_organization_sms_billing(auth_token, license_key):
    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        # sourcery skip: no-loop-in-tests
        sms_billing = client.organization.get_organization_sms_billing()
        try:
            model = SmsBillingSchema(**sms_billing)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Sms billing validation schema failed: {e}")
