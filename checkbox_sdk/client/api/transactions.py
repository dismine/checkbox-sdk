from typing import Optional

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
