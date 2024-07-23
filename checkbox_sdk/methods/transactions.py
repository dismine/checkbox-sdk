from typing import List, Optional

from checkbox_sdk.methods.base import BaseMethod, PaginationMixin


class GetTransactions(PaginationMixin, BaseMethod):
    uri = "transactions"

    def __init__(
        self, status: Optional[List[str]] = None, type: Optional[List[str]] = None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.status = status
        self.type = type

    @property
    def query(self):
        query = super().query
        if self.status is not None:
            query["status"] = self.status
        if self.type is not None:
            query["type"] = self.type
        return query


class GetTransaction(BaseMethod):
    def __init__(self, transaction_id: str):
        self.transaction_id = transaction_id

    @property
    def uri(self) -> str:
        return f"transactions/{self.transaction_id}"
