from typing import Optional, Generator, List, AsyncGenerator

from checkbox_sdk.consts import DEFAULT_REQUESTS_RELAX
from checkbox_sdk.exceptions import StatusException
from checkbox_sdk.methods import transactions
from checkbox_sdk.storage.simple import SessionStorage


class Transactions:
    def __init__(self, client):
        self.client = client

    def wait_transaction(
        self,
        transaction_id: str,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
    ):
        transaction = self.client.wait_status(
            transactions.GetTransaction(transaction_id=transaction_id),
            relax=relax,
            timeout=timeout,
            storage=storage,
            field="status",
            expected_value={"DONE", "ERROR"},
        )
        if transaction["status"] == "ERROR":
            raise StatusException(
                f"Transaction status moved to {transaction['status']!r} "
                f"and tax status {transaction['response_status']!r} "
                f"with message {transaction['response_error_message']!r}"
            )
        return transaction

    def get_transactions(
        self,
        status: Optional[List[str]] = None,
        type: Optional[List[str]] = None,
        desc: Optional[bool] = False,
        storage: Optional[SessionStorage] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
    ) -> Generator:
        """
        Retrieves transactions based on specified criteria.

        Args:
            status: The status of the transactions to retrieve.
            type: The type of transactions to retrieve.
            desc: A flag to indicate descending order.
            storage: An optional session storage to use for the operation.
            limit: The maximum number of results to return.
            offset: The offset for paginating results.

        Yields:
            Transactions based on the specified criteria.

        Example:
            .. code-block:: python

                for transaction in client.get_transactions(status=["DONE"], type=["Z_REPORT"]):
                    print(transaction)

        Notes:
            - This method handles pagination automatically, continuing to fetch and yield transactions until no more
              results are available.
        """
        get_transactions = transactions.GetTransactions(
            status=status,
            type=type,
            desc=desc,
            limit=limit,
            offset=offset,
        )

        while True:
            transactions_result = self.client(get_transactions, storage=storage)
            results = transactions_result.get("results", [])

            if not results:
                break

            yield from results
            get_transactions.resolve_pagination(transactions_result)
            get_transactions.shift_next_page()


class AsyncTransactions:
    def __init__(self, client):
        self.client = client

    async def wait_transaction(
        self,
        transaction_id: str,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
    ):
        transaction = await self.client.wait_status(
            transactions.GetTransaction(transaction_id=transaction_id),
            relax=relax,
            timeout=timeout,
            storage=storage,
            field="status",
            expected_value={"DONE", "ERROR"},
        )
        if transaction["status"] == "ERROR":
            raise StatusException(
                f"Transaction status moved to {transaction['status']!r} "
                f"and tax status {transaction['response_status']!r} "
                f"with message {transaction['response_error_message']!r}"
            )
        return transaction

    async def get_transactions(
        self,
        status: Optional[List[str]] = None,
        type: Optional[List[str]] = None,
        desc: Optional[bool] = False,
        storage: Optional[SessionStorage] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
    ) -> AsyncGenerator:
        """
        Asynchronously retrieves transactions based on specified criteria.

        Args:
            status: The status of the transactions to retrieve.
            type: The type of transactions to retrieve.
            desc: A flag to indicate descending order.
            storage: An optional session storage to use for the operation.
            limit: The maximum number of results to return.
            offset: The offset for paginating results.

        Yields:
            Transactions based on the specified criteria.

        Example:
            .. code-block:: python

                async for transaction in client.get_transactions(status=["DONE"], type=["Z_REPORT"]):
                    print(transaction)

        Notes:
            - This method handles pagination automatically, continuing to fetch and yield transactions until no more
              results are available.
        """
        get_transactions = transactions.GetTransactions(
            status=status,
            type=type,
            desc=desc,
            limit=limit,
            offset=offset,
        )

        while True:
            transactions_result = await self.client(get_transactions, storage=storage)
            results = transactions_result.get("results", [])

            if not results:
                break

            for result in results:
                yield result

            get_transactions.resolve_pagination(transactions_result)
            get_transactions.shift_next_page()
