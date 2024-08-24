# pylint: disable=duplicate-code
import json
import pathlib

import pytest

from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient


@pytest.mark.asyncio
async def test_ettn_order(auth_token, license_key, client_email, client_phone):
    assert license_key, "License key is empty"

    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        base_path = pathlib.Path(__file__).resolve().parent.parent
        receipt_path = base_path / "test_data/ettn_order.json"
        receipt_data = json.loads(receipt_path.resolve().read_text())

        # sourcery skip: no-conditionals-in-tests
        if client_email:
            receipt_data["receipt_body"]["delivery"] = {"delivery_email": client_email}

        if client_phone:
            receipt_data["receipt_body"]["delivery"] = {"delivery_phone": client_phone}

        # Cannot make API section /api/v1/np/* to work.

        response = await client.nova_post.post_ettn_order(
            order=receipt_data,
        )
        assert response, "Response is empty"

        response = await client.nova_post.get_ettn_order(
            order_id=response,
        )
        assert response, "Response is empty"

        response = await client.nova_post.update_ettn_order(order_id=response, delivery_email="test@example.com")
        assert response, "Response is empty"

        response = await client.nova_post.delete_ettn_order(
            order_id=response,
        )
        assert response, "Response is empty"


@pytest.mark.asyncio
async def test_get_ettn_orders(auth_token, license_key):
    assert license_key, "License key is empty"

    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        assert client.storage.cash_register["is_test"], "Not test cash register"

        await client.nova_post.get_ettn_orders()
