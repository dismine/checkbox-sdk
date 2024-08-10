import pytest

from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient


@pytest.mark.asyncio
async def test_webhook(auth_token, license_key):
    assert license_key, "License key is empty"

    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        webhook_url = "https://example.com/"

        response = await client.webhook.set_webhook(webhook_url)
        assert response["url"] == webhook_url

        response = await client.webhook.get_webhook_info()
        assert response["url"] == webhook_url

        response = await client.webhook.delete_webhook()
        assert response["ok"] is True
