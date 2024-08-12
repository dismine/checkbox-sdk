import datetime
from typing import Optional, List, Dict, Any, Union, Generator, AsyncGenerator
from uuid import UUID

from checkbox_sdk.methods import invoices
from checkbox_sdk.storage.simple import SessionStorage


class Invoices:
    def __init__(self, client):
        self.client = client

    def get_terminals(self, storage: Optional[SessionStorage] = None) -> List[Dict[str, Any]]:
        """
        Retrieves a list of terminals.

        Args:
            storage: An optional session storage to use for the operation.

        Returns:
            A list of dictionaries containing terminal details.

        Example:
            .. code-block:: python

                terminals = client.invoices.get_terminals()
                print(terminals)

        Notes:
            - This method sends a GET request to retrieve terminals information.
        """
        return self.client(invoices.GetTerminals(), storage=storage)

    def get_invoices(
        self,
        status: Optional[str] = None,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        storage: Optional[SessionStorage] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
    ) -> Generator:
        """
        Retrieves a list of invoices based on specified criteria.

        Args:
            status: The status of the invoices to filter by.
            from_date: The start date for filtering invoices.
            to_date: The end date for filtering invoices.
            storage: An optional session storage to use for the operation.
            limit: The maximum number of results to return per request.
            offset: The offset for paginating results.

        Yields:
            Invoices based on the specified criteria.

        Example:
            .. code-block:: python

                for invoice in client.invoices.get_invoices(status="paid"):
                    print(invoice)

        Notes:
            - This method handles pagination automatically, continuing to fetch and yield invoices until no more results
              are available.
        """
        invoices_request = invoices.GetInvoices(
            status=status,
            from_date=from_date,
            to_date=to_date,
            limit=limit,
            offset=offset,
        )

        while True:
            invoices_result = self.client(invoices_request, storage=storage)
            results = invoices_result.get("results", [])

            if not results:
                break

            yield from results
            invoices_request.resolve_pagination(invoices_result)
            invoices_request.shift_next_page()

    def create_invoice(
        self,
        invoice: Optional[List[Dict]] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates new invoices in the system.

        Args:
            invoice: A list of invoice details to create. If provided, this will be used as the request payload.
            **payload: Additional payload for the request. If `invoice` is provided, `**payload` should not be used.

        Returns:
            A dictionary containing the details of the created invoices.

        Example:
            .. code-block:: python

                response = client.invoices.create_invoice(invoice=[{"item": "item1", "amount": 100}])
                print(response)

        Notes:
            - This method sends a POST request to create invoices.
        """
        return self.client(invoices.CreateInvoice(invoice=invoice, **payload))

    def create_and_fiscalize_invoice(
        self,
        invoice: Optional[List[Dict]] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates and fiscalizes invoices in the system.

        Args:
            invoice: A list of invoice details to create and fiscalize. If provided, this will be used as the request
                     payload.
            **payload: Additional payload for the request. If `invoice` is provided, `**payload` should not be used.

        Returns:
            A dictionary containing the details of the created and fiscalized invoices.

        Example:
            .. code-block:: python

                response = client.invoices.create_and_fiscalize_invoice(invoice=[{"item": "item1", "amount": 100}])
                print(response)

        Notes:
            - This method sends a POST request to create and fiscalize invoices.
        """
        return self.client(invoices.CreateAndFiscalizeInvoice(invoice=invoice, **payload))

    def get_invoice_by_id(
        self, invoice_id: Union[str, UUID], storage: Optional[SessionStorage] = None
    ) -> Dict[str, Any]:
        """
        Retrieves an invoice by its ID.

        Args:
            invoice_id: The ID of the invoice to retrieve.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the invoice.

        Example:
            .. code-block:: python

                invoice = client.invoices.get_invoice_by_id(invoice_id="12345")
                print(invoice)

        Notes:
            - This method sends a GET request to retrieve an invoice by its ID.
        """
        return self.client(invoices.GetInvoiceById(invoice_id=invoice_id), storage=storage)

    def cancel_invoice_by_id(
        self, invoice_id: Union[str, UUID], storage: Optional[SessionStorage] = None
    ) -> Dict[str, Any]:
        """
        Cancels an invoice by its ID.

        Args:
            invoice_id: The ID of the invoice to cancel.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the response from the cancellation request.

        Example:
            .. code-block:: python

                response = client.invoices.cancel_invoice_by_id(invoice_id="12345")
                print(response)

        Notes:
            - This method sends a DELETE request to cancel an invoice by its ID.
        """
        return self.client(invoices.CancelInvoiceById(invoice_id=invoice_id), storage=storage)

    def remove_invoice_by_id(
        self, invoice_id: Union[str, UUID], storage: Optional[SessionStorage] = None
    ) -> Dict[str, Any]:
        """
        Removes an invoice by its ID.

        Args:
            invoice_id: The ID of the invoice to remove.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the response from the removal request.

        Example:
            .. code-block:: python

                response = client.invoices.remove_invoice_by_id(invoice_id="12345")
                print(response)

        Notes:
            - This method sends a DELETE request to remove an invoice by its ID.
        """
        return self.client(invoices.RemoveInvoiceById(invoice_id=invoice_id), storage=storage)


class AsyncInvoices:
    def __init__(self, client):
        self.client = client

    async def get_terminals(self, storage: Optional[SessionStorage] = None) -> List[Dict[str, Any]]:
        """
        Asynchronously retrieves a list of terminals.

        Args:
            storage: An optional session storage to use for the operation.

        Returns:
            A list of dictionaries containing terminal details.

        Example:
            .. code-block:: python

                terminals = await client.invoices.get_terminals()
                print(terminals)

        Notes:
            - This method sends an asynchronous GET request to retrieve terminals information.
        """
        return await self.client(invoices.GetTerminals(), storage=storage)

    async def get_invoices(
        self,
        status: Optional[str] = None,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        storage: Optional[SessionStorage] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
    ) -> AsyncGenerator:
        """
        Asynchronously retrieves a list of invoices based on specified criteria.

        Args:
            status: The status of the invoices to filter by.
            from_date: The start date for filtering invoices.
            to_date: The end date for filtering invoices.
            storage: An optional session storage to use for the operation.
            limit: The maximum number of results to return per request.
            offset: The offset for paginating results.

        Yields:
            Invoices based on the specified criteria.

        Example:
            .. code-block:: python

                async for invoice in client.invoices.get_invoices(status="paid"):
                    print(invoice)

        Notes:
            - This method handles pagination automatically, continuing to fetch and yield invoices until no more results
              are available.
        """
        get_invoices = invoices.GetInvoices(
            status=status,
            from_date=from_date,
            to_date=to_date,
            limit=limit,
            offset=offset,
        )

        while True:
            shifts_result = await self.client(get_invoices, storage=storage)
            results = shifts_result.get("results", [])

            if not results:
                break

            for result in results:
                yield result

            get_invoices.resolve_pagination(shifts_result)
            get_invoices.shift_next_page()

    async def create_invoice(
        self,
        invoice: Optional[List[Dict]] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Asynchronously creates new invoices in the system.

        Args:
            invoice: A list of invoice details to create. If provided, this will be used as the request payload.
            **payload: Additional payload for the request. If `invoice` is provided, `**payload` should not be used.

        Returns:
            A dictionary containing the details of the created invoices.

        Example:
            .. code-block:: python

                response = await client.invoices.create_invoice(invoice=[{"item": "item1", "amount": 100}])
                print(response)

        Notes:
            - This method sends a POST request to create invoices.
        """
        return await self.client(invoices.CreateInvoice(invoice=invoice, **payload))

    async def create_and_fiscalize_invoice(
        self,
        invoice: Optional[List[Dict]] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Asynchronously creates and fiscalizes invoices in the system.

        Args:
            invoice: A list of invoice details to create and fiscalize. If provided, this will be used as the request
                     payload.
            **payload: Additional payload for the request. If `invoice` is provided, `**payload` should not be used.

        Returns:
            A dictionary containing the details of the created and fiscalized invoices.

        Example:
            .. code-block:: python

                response = await client.invoices.create_and_fiscalize_invoice(invoice=[{"item": "item1",
                                                                                        "amount": 100}])
                print(response)

        Notes:
            - This method sends a POST request to create and fiscalize invoices.
        """
        return await self.client(invoices.CreateAndFiscalizeInvoice(invoice=invoice, **payload))

    async def get_invoice_by_id(
        self, invoice_id: Union[str, UUID], storage: Optional[SessionStorage] = None
    ) -> Dict[str, Any]:
        """
        Asynchronously retrieves an invoice by its ID.

        Args:
            invoice_id: The ID of the invoice to retrieve.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the invoice.

        Example:
            .. code-block:: python

                invoice = await client.invoices.get_invoice_by_id(invoice_id="12345")
                print(invoice)

        Notes:
            - This method sends a GET request to retrieve an invoice by its ID.
        """
        return await self.client(invoices.GetInvoiceById(invoice_id=invoice_id), storage=storage)

    async def cancel_invoice_by_id(
        self, invoice_id: Union[str, UUID], storage: Optional[SessionStorage] = None
    ) -> Dict[str, Any]:
        """
        Asynchronously cancels an invoice by its ID.

        Args:
            invoice_id: The ID of the invoice to cancel.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the response from the cancellation request.

        Example:
            .. code-block:: python

                response = await client.invoices.cancel_invoice_by_id(invoice_id="12345")
                print(response)

        Notes:
            - This method sends a DELETE request to cancel an invoice by its ID.
        """
        return await self.client(invoices.CancelInvoiceById(invoice_id=invoice_id), storage=storage)

    async def remove_invoice_by_id(
        self, invoice_id: Union[str, UUID], storage: Optional[SessionStorage] = None
    ) -> Dict[str, Any]:
        """
        Asynchronously removes an invoice by its ID.

        Args:
            invoice_id: The ID of the invoice to remove.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the response from the removal request.

        Example:
            .. code-block:: python

                response = await client.invoices.remove_invoice_by_id(invoice_id="12345")
                print(response)

        Notes:
            - This method sends a DELETE request to remove an invoice by its ID.
        """
        return await self.client(invoices.RemoveInvoiceById(invoice_id=invoice_id), storage=storage)
