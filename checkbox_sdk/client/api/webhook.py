from typing import Optional, Dict, Any

from checkbox_sdk.methods import webhook
from checkbox_sdk.storage.simple import SessionStorage


class Webhook:
    def __init__(self, client):
        self.client = client

    def get_webhook_info(self, storage: Optional[SessionStorage] = None) -> Dict[str, Any]:
        """
        Retrieves information about the current webhook configuration.

        Args:
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the current webhook configuration.

        Example:
            .. code-block:: python

                response = client.webhook.get_webhook_info()
                print(response)

        Notes:
            - This method sends a GET request to retrieve the current webhook configuration.
        """
        return self.client(webhook.GetWebhookInfo(), storage=storage)

    def set_webhook(self, url: str) -> Dict[str, Any]:
        """
        Sets the URL for the webhook.

        Args:
            url: The URL to which webhook notifications will be sent.

        Returns:
            A dictionary containing the details of the updated webhook configuration.

        Example:
            .. code-block:: python

                response = client.webhook.set_webhook(url="https://example.com/webhook")
                print(response)

        Notes:
            - This method sends a POST request to update the webhook URL.
        """
        return self.client(webhook.SetWebhook(url=url))

    def delete_webhook(self) -> Dict[str, Any]:
        """
        Deletes the current webhook configuration.

        Returns:
            A dictionary containing the result of the delete operation.

        Example:
            .. code-block::

                response = client.webhook.delete_webhook()
                print(response)

        Notes:
            - This method sends a DELETE request to remove the webhook configuration.
        """
        return self.client(webhook.DeleteWebhook())


class AsyncWebhook:
    def __init__(self, client):
        self.client = client

    async def get_webhook_info(
        self,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Asynchronously retrieves information about the current webhook configuration.

        Args:
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the current webhook configuration.

        Example:
            .. code-block:: python

                response = await client.webhook.get_webhook_info()
                print(response)

        Notes:
            - This method sends an asynchronous GET request to retrieve the current webhook configuration.
        """
        return await self.client(webhook.GetWebhookInfo(), storage=storage)

    async def set_webhook(self, url: str) -> Dict[str, Any]:
        """
        Asynchronously sets the URL for the webhook.

        Args:
            url: The URL to which webhook notifications will be sent.

        Returns:
            A dictionary containing the details of the updated webhook configuration.

        Example:
            .. code-block:: python

                response = await client.webhook.set_webhook(url="https://example.com/webhook")
                print(response)

        Notes:
            - This method sends an asynchronous POST request to update the webhook URL.
        """
        return await self.client(webhook.SetWebhook(url=url))

    async def delete_webhook(self) -> Dict[str, Any]:
        """
        Asynchronously deletes the current webhook configuration.

        Returns:
            A dictionary containing the result of the delete operation.

        Example:
            .. code-block:: python

                response = await client.webhook.delete_webhook()
                print(response)

        Notes:
            - This method sends an asynchronous DELETE request to remove the webhook configuration.
        """
        return await self.client(webhook.DeleteWebhook())
