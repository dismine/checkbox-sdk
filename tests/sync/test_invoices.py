import json
import pathlib

import pytest
from pydantic import ValidationError

from checkbox_sdk.client.synchronous import CheckBoxClient
from .base import open_shift, close_shift
from ..models.invoices_models import TerminalSchema, InvoiceSchema


def test_get_terminals(auth_token, license_key):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        # sourcery skip: no-loop-in-tests
        for terminal in client.invoices.get_terminals():
            try:
                model = TerminalSchema(**terminal)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Terminal validation schema failed: {e}")


def test_create_invoice(auth_token, license_key, client_email):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        terminals = client.invoices.get_terminals()
        # sourcery skip: no-conditionals-in-tests
        if not terminals:
            pytest.skip("No terminals available")

        open_shift(client)

        base_path = pathlib.Path(__file__).resolve().parent.parent
        invoice_path = base_path / "test_data/receipt.json"
        invoice_data = json.loads(invoice_path.resolve().read_text())

        # sourcery skip: no-conditionals-in-tests
        if client_email:
            invoice_data["delivery"] = {"email": client_email}

        invoice = client.invoices.create_invoice(
            invoice=invoice_data,
        )
        assert invoice["status"] == "CREATED"

        invoice_by_id = client.invoices.get_invoice_by_id(invoice_id=invoice["id"])
        try:
            model = InvoiceSchema(**invoice_by_id)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Invoice validation schema failed: {e}")

        response = client.invoices.cancel_invoice_by_id(invoice_id=invoice["id"])
        assert response["ok"] is True

        response = client.invoices.remove_invoice_by_id(invoice_id=invoice["id"])
        assert response["ok"] is True

        close_shift(client)


def test_create_and_fiscalize_invoice(auth_token, license_key, client_email):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        terminals = client.invoices.get_terminals()
        # sourcery skip: no-conditionals-in-tests
        if not terminals:
            pytest.skip("No terminals available")

        base_path = pathlib.Path(__file__).resolve().parent.parent
        invoice_path = base_path / "test_data/receipt.json"
        invoice_data = json.loads(invoice_path.resolve().read_text())

        # sourcery skip: no-conditionals-in-tests
        if client_email:
            invoice_data["delivery"] = {"email": client_email}

        invoice = client.invoices.create_and_fiscalize_invoice(
            invoice=invoice_data,
        )
        assert invoice["status"] == "CREATED"
