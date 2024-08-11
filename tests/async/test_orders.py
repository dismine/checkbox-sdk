import json
import pathlib

import pytest
from pydantic import ValidationError

from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
from checkbox_sdk.exceptions import CheckBoxAPIError
from ..models.orders_models import OrderSchema


@pytest.mark.asyncio
async def test_orders_synchronization(auth_token, license_key):
    assert license_key, "License key is empty"

    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        with pytest.raises(CheckBoxAPIError):
            await client.orders.run_orders_synchronization()


@pytest.mark.asyncio
async def test_add_orders(auth_token, license_key, client_email):
    assert license_key, "License key is empty"

    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        base_path = pathlib.Path(__file__).resolve().parent.parent
        orders_path = base_path / "test_data/order.json"
        orders_data = json.loads(orders_path.resolve().read_text())

        # sourcery skip: no-conditionals-in-tests
        if client_email:
            orders_data["receipt_draft"]["delivery"] = {"email": client_email}

        # sourcery skip: no-loop-in-tests
        async for order in client.orders.add_orders(orders_list=orders_data):
            try:
                model = OrderSchema(**order)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Order validation schema failed: {e}")

            response = await client.orders.get_order(order_id=order["id"])
            try:
                model = OrderSchema(**response)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Order validation schema failed: {e}")

            order_update = {"goods": [{"quantity": 1000}], "id": order["id"]}
            response = await client.orders.edit_order(order_update=order_update)
            try:
                model = OrderSchema(**response)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Order validation schema failed: {e}")

            response = await client.orders.update_custom_order_status(order_id=order["id"], new_status="TEST")
            try:
                model = OrderSchema(**response)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Order validation schema failed: {e}")

            response = await client.orders.cancel_order(order_id=order["id"])
            try:
                model = OrderSchema(**response)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Order validation schema failed: {e}")

            response = await client.orders.close_not_fiscalize_order(order_id=order["id"])
            try:
                model = OrderSchema(**response)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Order validation schema failed: {e}")


@pytest.mark.asyncio
async def test_get_orders(auth_token, license_key, client_email):
    assert license_key, "License key is empty"

    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        # sourcery skip: no-loop-in-tests
        async for order in client.orders.get_orders():
            try:
                model = OrderSchema(**order)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Order validation schema failed: {e}")


@pytest.mark.asyncio
async def test_integration(auth_token, license_key, client_email):
    assert license_key, "License key is empty"

    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        url = "https://example.com/"

        response = await client.orders.set_integration(url=url)
        assert response["url"] == url

        response = await client.orders.get_integration()
        assert response["url"] == url

        response = await client.orders.delete_integration()
        assert response["ok"] is True
