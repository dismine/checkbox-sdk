from checkbox_sdk.client.synchronous import CheckBoxClient


def test_webhook(auth_token, license_key):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        webhook_url = "https://example.com/"

        response = client.webhook.set_webhook(webhook_url)
        assert response["url"] == webhook_url

        response = client.webhook.get_webhook_info()
        assert response["url"] == webhook_url

        response = client.webhook.delete_webhook()
        assert response["ok"] is True
