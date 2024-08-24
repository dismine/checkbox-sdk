# pylint: disable=duplicate-code
import json
import pathlib

import pytest
from pydantic import ValidationError

from checkbox_sdk.client.synchronous import CheckBoxClient
from checkbox_sdk.exceptions import CheckBoxAPIError, CheckBoxError
from ..models.orders_models import OrderSchema


def test_orders_synchronization(auth_token, license_key):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        with pytest.raises(CheckBoxAPIError):
            client.orders.run_orders_synchronization()


# pylint: disable=duplicate-code,too-many-statements
def test_add_orders(auth_token, license_key, client_email):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        base_path = pathlib.Path(__file__).resolve().parent.parent
        orders_path = base_path / "test_data/order.json"
        orders_data = json.loads(orders_path.resolve().read_text())

        # sourcery skip: no-conditionals-in-tests
        if client_email:
            orders_data["receipt_draft"]["delivery"] = {"email": client_email}

        try:
            # sourcery skip: no-loop-in-tests
            for order in client.orders.add_orders(orders_list=orders_data):
                try:
                    model = OrderSchema(**order)
                    assert model is not None
                except ValidationError as e:  # pragma: no cover
                    pytest.fail(f"Order validation schema failed: {e}")

                response = client.orders.get_order(order_id=order["id"])
                try:
                    model = OrderSchema(**response)
                    assert model is not None
                except ValidationError as e:  # pragma: no cover
                    pytest.fail(f"Order validation schema failed: {e}")

                order_update = {"goods": [{"quantity": 1000}], "id": order["id"]}
                response = client.orders.edit_order(order_update=order_update)
                try:
                    model = OrderSchema(**response)
                    assert model is not None
                except ValidationError as e:  # pragma: no cover
                    pytest.fail(f"Order validation schema failed: {e}")

                response = client.orders.update_custom_order_status(order_id=order["id"], new_status="TEST")
                try:
                    model = OrderSchema(**response)
                    assert model is not None
                except ValidationError as e:  # pragma: no cover
                    pytest.fail(f"Order validation schema failed: {e}")

                response = client.orders.cancel_order(order_id=order["id"])
                try:
                    model = OrderSchema(**response)
                    assert model is not None
                except ValidationError as e:  # pragma: no cover
                    pytest.fail(f"Order validation schema failed: {e}")

                response = client.orders.close_not_fiscalize_order(order_id=order["id"])
                try:
                    model = OrderSchema(**response)
                    assert model is not None
                except ValidationError as e:  # pragma: no cover
                    pytest.fail(f"Order validation schema failed: {e}")
        except CheckBoxError as e:
            error_message = str(e)
            if "status=500" in error_message and '{"message":"Internal Server Error"}' in error_message:
                pytest.skip("No valid integration")
            else:
                raise


def test_get_orders(auth_token, license_key):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        # sourcery skip: no-loop-in-tests
        for order in client.orders.get_orders():
            try:
                model = OrderSchema(**order)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Order validation schema failed: {e}")


def test_integration(auth_token, license_key):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        url = "https://example.com/"

        response = client.orders.set_integration(url=url)
        assert response["url"] == url

        response = client.orders.get_integration()
        assert response["url"] == url

        response = client.orders.delete_integration()
        assert response["ok"] is True
