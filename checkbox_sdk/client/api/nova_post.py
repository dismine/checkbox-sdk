import datetime
from typing import Optional, Union, Dict, List
from uuid import UUID

from checkbox_sdk.methods import nova_post
from checkbox_sdk.storage.simple import SessionStorage


class NovaPost:
    def __init__(self, client):
        self.client = client

    def get_ettn_orders(
        self,
        status: Optional[str] = None,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        limit: int = 25,
        offset: int = 0,
        storage: Optional[SessionStorage] = None,
    ) -> List[str]:
        """
        Retrieves Ettn orders based on specified criteria.

        Args:
            status: The status of the orders to retrieve (e.g., "completed", "pending").
            from_date: The start date for filtering orders. Can be a datetime object or a string.
            to_date: The end date for filtering orders. Can be a datetime object or a string.
            limit: The maximum number of orders to retrieve per request.
            offset: The number of orders to skip before starting to collect results.
            storage: An optional session storage to use for the operation.

        Returns:
            A list of strings containing Ettn orders data based on the specified criteria.

        Example:
            .. code-block:: python

                orders = client.nova_post.get_ettn_orders(status="completed", from_date="2024-01-01",
                                                          to_date="2024-01-31")
                for order in orders:
                    print(order)

        Notes:
            - This method returns a list of raw Ettn orders data.
            - Pagination is handled using `limit` and `offset` parameters.
        """
        return self.client(
            nova_post.GetEttnOrders(status=status, from_date=from_date, to_date=to_date, limit=limit, offset=offset),
            storage=storage,
        )

    def post_ettn_order(self, order: Optional[Dict] = None, **payload) -> str:
        """
        Posts Ettn orders to the system.

        Args:
            order: A list of orders to post. If provided, this will be used as the request payload.
            **payload: Additional payload for the request. If `order` is provided, `**payload` should not be used.

        Returns:
            A string containing the response from the system.

        Example:
            .. code-block:: python

                response = client.nova_post.post_ettn_order(order=[{"item": "item1", "quantity": 10}])
                print(response)

        Notes:
            - This method sends a POST request to create Ettn orders.
        """
        return self.client(nova_post.PostEttnOrder(order=order, **payload))

    def post_ettn_prepayment_order(self, order: Optional[Dict] = None, **payload) -> str:
        """
        Posts Ettn prepayment orders to the system.

        Args:
            order: A list of prepayment orders to post. If provided, this will be used as the request payload.
            **payload: Additional payload for the request. If `order` is provided, `**payload` should not be used.

        Returns:
            A string containing the response from the system.

        Example:
            .. code-block:: python

                response = client.nova_post.post_ettn_prepayment_order(order=[{"item": "item1", "quantity": 10}])
                print(response)

        Notes:
            - This method sends a POST request to create Ettn prepayment orders.
        """
        return self.client(nova_post.PostEttnPrepaymentOrder(order=order, **payload))

    def get_ettn_order(self, order_id: Union[str, UUID]) -> str:
        """
        Retrieves an Ettn order by its ID.

        Args:
            order_id: The ID of the Ettn order to retrieve. Can be a string or UUID.

        Returns:
            A string containing the response from the system.

        Example:
            .. code-block:: python

                response = client.nova_post.get_ettn_order(order_id="12345")
                print(response)

        Notes:
            - This method sends a GET request to retrieve the specified Ettn order.
        """
        return self.client(nova_post.GetEttnOrder(order_id=order_id))

    def update_ettn_order(
        self, order_id: Union[str, UUID], delivery_phone: Optional[str] = None, delivery_email: Optional[str] = None
    ) -> str:
        """
        Updates an Ettn order with the specified delivery details.

        Args:
            order_id: The ID of the Ettn order to update. Can be a string or UUID.
            delivery_phone: The new delivery phone number.
            delivery_email: The new delivery email address.

        Returns:
            A string containing the response from the system.

        Example:
            .. code-block:: python

                response = client.nova_post.update_ettn_order(order_id="12345", delivery_phone="555-1234",
                                                              delivery_email="example@example.com")
                print(response)

        Notes:
            - This method sends a PUT request to update the specified Ettn order.
        """
        return self.client(
            nova_post.UpdateEttnOrder(order_id=order_id, delivery_phone=delivery_phone, delivery_email=delivery_email)
        )

    def delete_ettn_order(self, order_id: Union[str, UUID]) -> str:
        """
        Deletes an Ettn order with the specified ID.

        Args:
            order_id: The ID of the Ettn order to delete. Can be a string or UUID.

        Returns:
            A string containing the response from the system.

        Example:
            .. code-block:: python

                response = client.nova_post.delete_ettn_order(order_id="12345")
                print(response)

        Notes:
            - This method sends a DELETE request to remove the specified Ettn order.
        """
        return self.client(nova_post.DeleteEttnOrder(order_id=order_id))


class AsyncNovaPost:
    def __init__(self, client):
        self.client = client

    async def get_ettn_orders(
        self,
        status: Optional[str] = None,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        limit: int = 25,
        offset: int = 0,
        storage: Optional[SessionStorage] = None,
    ) -> List[str]:
        """
        Asynchronously retrieves Ettn orders based on specified criteria.

        Args:
            status: The status of the orders to retrieve (e.g., "completed", "pending").
            from_date: The start date for filtering orders. Can be a datetime object or a string.
            to_date: The end date for filtering orders. Can be a datetime object or a string.
            limit: The maximum number of orders to retrieve per request.
            offset: The number of orders to skip before starting to collect results.
            storage: An optional session storage to use for the operation.

        Returns:
            A list of strings containing Ettn orders data based on the specified criteria.

        Example:
            .. code-block:: python

                orders = await client.nova_post.get_ettn_orders(status="completed", from_date="2024-01-01",
                                                                to_date="2024-01-31")
                for order in orders:
                    print(order)

        Notes:
            - This method returns a list of raw Ettn orders data.
            - Pagination is handled using `limit` and `offset` parameters.
        """
        return await self.client(
            nova_post.GetEttnOrders(status=status, from_date=from_date, to_date=to_date, limit=limit, offset=offset),
            storage=storage,
        )

    async def post_ettn_order(self, order: Optional[Dict] = None, **payload) -> str:
        """
        Asynchronously posts Ettn orders to the system.

        Args:
            order: A list of orders to post. If provided, this will be used as the request payload.
            **payload: Additional payload for the request. If `order` is provided, `**payload` should not be used.

        Returns:
            A string containing the response from the system.

        Example:
            .. code-block:: python

                response = await client.nova_post.post_ettn_order(order=[{"item": "item1", "quantity": 10}])
                print(response)

        Notes:
            - This method sends a POST request to create Ettn orders.
        """
        return await self.client(nova_post.PostEttnOrder(order=order, **payload))

    async def post_ettn_prepayment_order(self, order: Optional[Dict] = None, **payload) -> str:
        """
        Asynchronously posts Ettn prepayment orders to the system.

        Args:
            order: A list of prepayment orders to post. If provided, this will be used as the request payload.
            **payload: Additional payload for the request. If `order` is provided, `**payload` should not be used.

        Returns:
            A string containing the response from the system.

        Example:
            .. code-block:: python

                response = await client.nova_post.post_ettn_prepayment_order(order=[{"item": "item1", "quantity": 10}])
                print(response)

        Notes:
            - This method sends a POST request to create Ettn prepayment orders.
        """
        return await self.client(nova_post.PostEttnPrepaymentOrder(order=order, **payload))

    async def get_ettn_order(self, order_id: Union[str, UUID]) -> str:
        """
        Asynchronously retrieves an Ettn order by its ID.

        Args:
            order_id: The ID of the Ettn order to retrieve. Can be a string or UUID.

        Returns:
            A string containing the response from the system.

        Example:
            .. code-block:: python

                response = await client.nova_post.get_ettn_order(order_id="12345")
                print(response)

        Notes:
            - This method sends a GET request to retrieve the specified Ettn order.
        """
        return await self.client(nova_post.GetEttnOrder(order_id=order_id))

    async def update_ettn_order(
        self, order_id: Union[str, UUID], delivery_phone: Optional[str] = None, delivery_email: Optional[str] = None
    ) -> str:
        """
        Asynchronously updates an Ettn order with the specified delivery details.

        Args:
            order_id: The ID of the Ettn order to update. Can be a string or UUID.
            delivery_phone: The new delivery phone number.
            delivery_email: The new delivery email address.

        Returns:
            A string containing the response from the system.

        Example:
            .. code-block:: python

                response = await client.nova_post.update_ettn_order(order_id="12345", delivery_phone="555-1234",
                                                                    delivery_email="example@example.com")
                print(response)

        Notes:
            - This method sends a PUT request to update the specified Ettn order.
        """
        return await self.client(
            nova_post.UpdateEttnOrder(order_id=order_id, delivery_phone=delivery_phone, delivery_email=delivery_email)
        )

    async def delete_ettn_order(self, order_id: Union[str, UUID]) -> str:
        """
        Asynchronously deletes an Ettn order with the specified ID.

        Args:
            order_id: The ID of the Ettn order to delete. Can be a string or UUID.

        Returns:
            A string containing the response from the system.

        Example:
            .. code-block:: python

                response = await client.nova_post.delete_ettn_order(order_id="12345")
                print(response)

        Notes:
            - This method sends a DELETE request to remove the specified Ettn order.
        """
        return await self.client(nova_post.DeleteEttnOrder(order_id=order_id))
