import datetime
from typing import Optional, Union, List, Generator, AsyncGenerator, Dict, Any
from uuid import UUID

from checkbox_sdk.methods import orders
from checkbox_sdk.storage.simple import SessionStorage


class Orders:
    def __init__(self, client):
        self.client = client

    def run_orders_synchronization(
        self,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Runs the synchronization of orders.

        Args:
            storage: An optional session storage to use for the operation.

        Returns:
            A string containing the result of the synchronization process.

        Example:
            .. code-block:: python

                result = client.orders.run_orders_synchronization()
                print(result)

        Notes:
            - This method sends a POST request to run the synchronization of orders.
        """
        return self.client(
            orders.RunOrdersSynchronization(),
            storage=storage,
        )

    def get_orders(
        self,
        desc: Optional[bool] = True,
        delivery_desc: Optional[bool] = None,
        orders_all: Optional[bool] = False,
        delivered_from_date: Optional[Union[datetime.datetime, str]] = None,
        delivered_to_date: Optional[Union[datetime.datetime, str]] = None,
        status: Optional[List[str]] = None,
        stock_code: Optional[str] = None,
        storage: Optional[SessionStorage] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
    ) -> Generator:
        """
        Retrieves orders based on specified criteria.

        Args:
            desc: A flag indicating if the results should be in descending order.
            delivery_desc: A flag indicating if the delivery date should be included in the results.
            orders_all: A flag indicating if all orders should be retrieved.
            delivered_from_date: The start date for filtering orders based on delivery date.
            delivered_to_date: The end date for filtering orders based on delivery date.
            status: A list of statuses to filter orders by.
            stock_code: The stock code to filter orders by.
            storage: An optional session storage to use for the operation.
            limit: The maximum number of results to return.
            offset: The offset for paginating results.

        Yields:
            Orders based on the specified criteria.

        Example:
            .. code-block:: python

                for order in client.orders.get_orders(status=["shipped"], limit=50):
                    print(order)

        Notes:
            - This method handles pagination automatically, continuing to fetch and yield orders until no more results
              are available.
        """
        orders_request = orders.GetOrders(
            desc=desc,
            delivery_desc=delivery_desc,
            orders_all=orders_all,
            delivered_from_date=delivered_from_date,
            delivered_to_date=delivered_to_date,
            status=status,
            stock_code=stock_code,
            limit=limit,
            offset=offset,
        )

        while True:
            orders_result = self.client(orders_request, storage=storage)
            results = orders_result.get("results", [])

            if not results:
                break

            yield from results
            orders_request.resolve_pagination(orders_result)
            orders_request.shift_next_page()

    def add_orders(
        self,
        orders_list: Optional[Union[List[Dict], Dict]] = None,
        **payload,
    ) -> List[Dict[str, Any]]:
        """
        Adds orders to the system.

        Args:
            orders_list: A list or dictionary of orders to add. If provided, this will be used as the request payload.
            **payload: Additional payload for the request. If `orders_list` is provided, `**payload` should not be used.

        Returns:
            A list of dictionaries containing the details of the added orders.

        Example:
            .. code-block:: python

                response = client.orders.add_orders(orders_list=[{"item": "item1", "quantity": 10}])
                print(response)

        Notes:
            - This method sends a POST request to add orders.
            - If both `orders_list` and `**payload` are provided, `orders_list` will take precedence.
        """
        return self.client(orders.AddOrders(orders=orders_list, **payload))

    def get_integration(
        self,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves integration details.

        Args:
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the integration.

        Example:
            .. code-block:: python

                integration_details = client.orders.get_integration()
                print(integration_details)

        Notes:
            - This method sends a GET request to retrieve integration details.
        """
        return self.client(
            orders.GetIntegration(),
            storage=storage,
        )

    def set_integration(
        self,
        url: str,
    ) -> Dict[str, Any]:
        """
        Sets the integration URL.

        Args:
            url: The URL to set for the integration.

        Returns:
            A dictionary containing the details of the set integration.

        Example:
            .. code-block:: python

                response = client.orders.set_integration(url="https://example.com")
                print(response)

        Notes:
            - This method sends a POST request to set the integration URL.
        """
        return self.client(
            orders.SetIntegration(url=url),
        )

    def delete_integration(self) -> Dict[str, bool]:
        """
        Deletes the current integration.

        Returns:
            A dictionary containing the result of the delete operation,
            with a boolean value indicating success.

        Example:
            .. code-block:: python

                response = client.orders.delete_integration()
                print(response)

        Notes:
            - This method sends a DELETE request to remove the current integration.
        """
        return self.client(orders.DeleteIntegration())

    def get_order(
        self, order_id: Union[str, UUID], orders_all: Optional[bool] = False, storage: Optional[SessionStorage] = None
    ) -> Dict[str, Any]:
        """
        Retrieves details of a specific order.

        Args:
            order_id: The ID of the order to retrieve.
            orders_all: A flag indicating if all related orders should be retrieved.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the specified order.

        Example:
            .. code-block:: python

                order = client.orders.get_order(order_id="123e4567-e89b-12d3-a456-426614174000", orders_all=True)
                print(order)

        Notes:
            - This method sends a GET request to retrieve the order with the specified ID.
        """
        return self.client(
            orders.GetOrder(order_id=order_id, orders_all=orders_all),
            storage=storage,
        )

    def cancel_order(self, order_id: Union[str, UUID], storage: Optional[SessionStorage] = None) -> Dict[str, Any]:
        """
        Cancels a specific order.

        Args:
            order_id: The ID of the order to cancel.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the result of the cancellation.

        Example:
            .. code-block:: python

                result = client.orders.cancel_order(order_id="123e4567-e89b-12d3-a456-426614174000")
                print(result)

        Notes:
            - This method sends a PATCH request to cancel the order with the specified ID.
        """
        return self.client(
            orders.CancelOrder(order_id=order_id),
            storage=storage,
        )

    def close_not_fiscalize_order(
        self, order_id: Union[str, UUID], storage: Optional[SessionStorage] = None
    ) -> Dict[str, Any]:
        """
        Closes an order without fiscalizing it.

        Args:
            order_id: The ID of the order to close.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the result of the operation.

        Example:
            .. code-block:: python

                result = client.orders.close_not_fiscalize_order(order_id="123e4567-e89b-12d3-a456-426614174000")
                print(result)

        Notes:
            - This method sends a PATCH request to close the specified order without fiscalizing it.
        """
        return self.client(
            orders.CloseNotFiscalizeOrder(order_id=order_id),
            storage=storage,
        )

    def edit_order(
        self,
        order_update: Optional[Dict] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Edits an existing order in the system.

        Args:
            order_update: A dictionary representing the order details to edit. If provided, this will be used as the
            request payload.
            **payload: Additional payload for the request. If `order_update` is provided, `**payload` should not be used.

        Returns:
            A dictionary containing the details of the edited order.

        Example:
            .. code-block:: python

                response = client.orders.edit_order(order_update={"order_id": "123", "status": "shipped"})
                print(response)

        Notes:
            - This method sends a POST request to edit the specified order.
        """
        return self.client(orders.EditOrder(order=order_update, **payload))

    def update_custom_order_status(
        self, order_id: Union[str, UUID], new_status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Updates the custom status of an order.

        Args:
            order_id: The ID of the order to update.
            new_status: The new custom status to apply to the order.

        Returns:
            A dictionary containing the details of the updated order status.

        Example:
            .. code-block:: python

                response = client.orders.update_custom_order_status(order_id="123", new_status="processing")
                print(response)

        Notes:
            - This method sends a PATCH request to update the custom status of the specified order.
        """
        return self.client(orders.UpdateCustomOrderStatus(order_id=order_id, new_status=new_status))

    def delete_order(self, order_id: Union[str, UUID]) -> Dict[str, Any]:
        """
        Deletes an order from the system.

        Args:
            order_id: The ID of the order to delete.

        Returns:
            A dictionary containing the result of the deletion operation.

        Example:
            .. code-block:: python

                response = client.orders.delete_order(order_id="123")
                print(response)

        Notes:
            - This method sends a POST request to delete the specified order.
            - This method is internal and uses a specific endpoint format.
        """
        return self.client(orders.DeleteOrder(order_id=order_id))


class AsyncOrders:
    def __init__(self, client):
        self.client = client

    async def run_orders_synchronization(
        self,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Asynchronously runs the synchronization of orders.

        Args:
            storage: An optional session storage to use for the operation.

        Returns:
            A string containing the result of the synchronization process.

        Example:
            .. code-block:: python

                result = await client.orders.run_orders_synchronization()
                print(result)

        Notes:
            - This method sends a POST request to asynchronously run the synchronization of orders.
        """
        return await self.client(
            orders.RunOrdersSynchronization(),
            storage=storage,
        )

    async def get_orders(
        self,
        desc: Optional[bool] = True,
        delivery_desc: Optional[bool] = None,
        orders_all: Optional[bool] = False,
        delivered_from_date: Optional[Union[datetime.datetime, str]] = None,
        delivered_to_date: Optional[Union[datetime.datetime, str]] = None,
        status: Optional[List[str]] = None,
        stock_code: Optional[str] = None,
        storage: Optional[SessionStorage] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
    ) -> AsyncGenerator:
        """
        Asynchronously retrieves orders based on specified criteria.

        Args:
            desc: A flag indicating if the results should be in descending order.
            delivery_desc: A flag indicating if the delivery date should be included in the results.
            orders_all: A flag indicating if all orders should be retrieved.
            delivered_from_date: The start date for filtering orders based on delivery date.
            delivered_to_date: The end date for filtering orders based on delivery date.
            status: A list of statuses to filter orders by.
            stock_code: The stock code to filter orders by.
            storage: An optional session storage to use for the operation.
            limit: The maximum number of results to return.
            offset: The offset for paginating results.

        Yields:
            Orders based on the specified criteria.

        Example:
            .. code-block:: python

                async for order in client.get_orders(status=["shipped"], limit=50):
                    print(order)

        Notes:
            - This method handles pagination automatically, continuing to fetch and yield orders until no more results
              are available.
        """
        get_orders = orders.GetOrders(
            desc=desc,
            delivery_desc=delivery_desc,
            orders_all=orders_all,
            delivered_from_date=delivered_from_date,
            delivered_to_date=delivered_to_date,
            status=status,
            stock_code=stock_code,
            limit=limit,
            offset=offset,
        )

        while True:
            shifts_result = await self.client(get_orders, storage=storage)
            results = shifts_result.get("results", [])

            if not results:
                break

            for result in results:
                yield result

            get_orders.resolve_pagination(shifts_result)
            get_orders.shift_next_page()

    async def add_orders(
        self,
        orders_list: Optional[Union[List[Dict], Dict]] = None,
        **payload,
    ) -> List[Dict[str, Any]]:
        """
        Asynchronously adds orders to the system.

        Args:
            orders_list: A list or dictionary of orders to add. If provided, this will be used as the request payload.
            **payload: Additional payload for the request. If `orders_list` is provided, `**payload` should not be used.

        Returns:
            A list of dictionaries containing the details of the added orders.

        Example:
            .. code-block:: python

                response = await client.orders.add_orders(orders_list=[{"item": "item1", "quantity": 10}])
                print(response)

        Notes:
            - This method sends a POST request to add orders asynchronously.
            - If both `orders_list` and `**payload` are provided, `orders_list` will take precedence.
        """

        return await self.client(orders.AddOrders(orders=orders_list, **payload))

    async def get_integration(
        self,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Asynchronously retrieves integration details.

        Args:
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the integration.

        Example:
            .. code-block:: python

                integration_details = await client.orders.get_integration()
                print(integration_details)

        Notes:
            - This method sends a GET request to retrieve integration details asynchronously.
        """
        return await self.client(
            orders.GetIntegration(),
            storage=storage,
        )

    async def set_integration(
        self,
        url: str,
    ) -> Dict[str, Any]:
        """
        Asynchronously sets the integration URL.

        Args:
            url: The URL to set for the integration.

        Returns:
            A dictionary containing the details of the set integration.

        Example:
            .. code-block:: python

                response = await client.orders.set_integration(url="https://example.com")
                print(response)

        Notes:
            - This method sends a POST request to set the integration URL asynchronously.
        """
        return await self.client(
            orders.SetIntegration(url=url),
        )

    async def delete_integration(self) -> Dict[str, bool]:
        """
        Asynchronously deletes the current integration.

        Returns:
            A dictionary containing the result of the delete operation,
            with a boolean value indicating success.

        Example:
            response = await client.orders.delete_integration()
            print(response)

        Notes:
            - This method sends a DELETE request to remove the current integration asynchronously.
        """
        return await self.client(orders.DeleteIntegration())

    async def get_order(
        self, order_id: Union[str, UUID], orders_all: Optional[bool] = False, storage: Optional[SessionStorage] = None
    ) -> Dict[str, Any]:
        """
        Asynchronously retrieves details of a specific order.

        Args:
            order_id: The ID of the order to retrieve.
            orders_all: A flag indicating if all related orders should be retrieved.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the specified order.

        Example:
            order = await client.get_order(order_id="123e4567-e89b-12d3-a456-426614174000", orders_all=True)
            print(order)

        Notes:
            - This method sends a GET request to retrieve the order with the specified ID asynchronously.
        """
        return await self.client(
            orders.GetOrder(order_id=order_id, orders_all=orders_all),
            storage=storage,
        )

    async def cancel_order(
        self, order_id: Union[str, UUID], storage: Optional[SessionStorage] = None
    ) -> Dict[str, Any]:
        """
        Asynchronously cancels a specific order.

        Args:
            order_id: The ID of the order to cancel.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the result of the cancellation.

        Example:
            result = await client.orders.cancel_order(order_id="123e4567-e89b-12d3-a456-426614174000")
            print(result)

        Notes:
            - This method sends a PATCH request to cancel the order with the specified ID asynchronously.
        """
        return await self.client(
            orders.CancelOrder(order_id=order_id),
            storage=storage,
        )

    async def close_not_fiscalize_order(
        self, order_id: Union[str, UUID], storage: Optional[SessionStorage] = None
    ) -> Dict[str, Any]:
        """
        Asynchronously closes an order without fiscalizing it.

        Args:
            order_id: The ID of the order to close.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the result of the operation.

        Example:
            result = await client.orders.close_not_fiscalize_order(order_id="123e4567-e89b-12d3-a456-426614174000")
            print(result)

        Notes:
            - This method sends a PATCH request to close the specified order without fiscalizing it asynchronously.
        """
        return await self.client(
            orders.CloseNotFiscalizeOrder(order_id=order_id),
            storage=storage,
        )

    async def edit_order(
        self,
        order_update: Optional[Dict] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Asynchronously edits an existing order in the system.

        Args:
            order_update: A dictionary representing the order details to edit. If provided, this will be used as the
            request payload.
            **payload: Additional payload for the request. If `order_update` is provided, `**payload` should not be used.

        Returns:
            A dictionary containing the details of the edited order.

        Example:
            response = await client.orders.edit_order(order_update={"order_id": "123", "status": "shipped"})
            print(response)

        Notes:
            - This method sends a POST request to edit the specified order asynchronously.
        """
        return await self.client(orders.EditOrder(order=order_update, **payload))

    async def update_custom_order_status(
        self, order_id: Union[str, UUID], new_status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Asynchronously updates the custom status of an order.

        Args:
            order_id: The ID of the order to update.
            new_status: The new custom status to apply to the order.

        Returns:
            A dictionary containing the details of the updated order status.

        Example:
            response = await client.orders.update_custom_order_status(order_id="123", new_status="processing")
            print(response)

        Notes:
            - This method sends a PATCH request to update the custom status of the specified order asynchronously.
        """
        return await self.client(orders.UpdateCustomOrderStatus(order_id=order_id, new_status=new_status))

    async def delete_order(self, order_id: Union[str, UUID]) -> Dict[str, Any]:
        """
        Asynchronously deletes an order from the system.

        Args:
            order_id: The ID of the order to delete.

        Returns:
            A dictionary containing the result of the deletion operation.

        Example:
            response = await client.orders.delete_order(order_id="123")
            print(response)

        Notes:
            - This method sends a POST request to delete the specified order asynchronously.
            - This method is internal and uses a specific endpoint format.
        """
        return await self.client(orders.DeleteOrder(order_id=order_id))
