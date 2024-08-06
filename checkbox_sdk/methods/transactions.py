from typing import List, Optional

from checkbox_sdk.methods.base import BaseMethod, PaginationMixin

URI_PREFIX = "transactions/"


class GetTransactions(PaginationMixin, BaseMethod):
    uri = "transactions"

    def __init__(
        self,
        status: Optional[List[str]] = None,
        type: Optional[List[str]] = None,
        desc: Optional[bool] = False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.status = status
        self.type = type
        self.desc = desc

    @property
    def query(self):
        query = super().query
        if self.status is not None:
            query["status"] = self.status
        if self.type is not None:
            query["type"] = self.type
        if self.desc is not None:
            query["desc"] = self.desc
        return query


class GetTransaction(BaseMethod):
    def __init__(self, transaction_id: str):
        self.transaction_id = transaction_id

    @property
    def uri(self) -> str:
        return f"{URI_PREFIX}{self.transaction_id}"
