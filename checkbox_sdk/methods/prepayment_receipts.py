import datetime
from typing import Optional, Union, Dict
from uuid import UUID

from httpx import Response

from checkbox_sdk.methods.base import BaseMethod, HTTPMethod, PaginationMixin
from checkbox_sdk.storage.simple import SessionStorage

URI_PREFIX = "prepayment-receipts/"


class GetPrepaymentReceipts(PaginationMixin, BaseMethod):
    uri = f"{URI_PREFIX}search"

    def __init__(
        self,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        desc: Optional[bool] = False,
        search: Optional[str] = None,
        cash_register_id: Optional[Union[datetime.datetime, str]] = None,
        status: Optional[str] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.to_date = to_date
        self.from_date = from_date
        self.desc = desc
        self.search = search
        self.cash_register_id = cash_register_id
        self.status = status

    @property
    def query(self):
        query = super().query

        if isinstance(self.from_date, datetime.datetime):
            query["from_date"] = self.from_date.isoformat()
        elif self.from_date:
            query["from_date"] = self.from_date

        if isinstance(self.to_date, datetime.datetime):
            query["to_date"] = self.to_date.isoformat()
        elif self.to_date:
            query["to_date"] = self.to_date

        if self.desc is not None:
            query["desc"] = self.desc

        if self.search is not None:
            query["search"] = self.search

        if isinstance(self.cash_register_id, UUID):
            query["cash_register_id"] = str(self.cash_register_id)
        elif self.to_date:
            query["cash_register_id"] = self.cash_register_id

        if self.status is not None:
            query["status"] = self.status

        return query


class GetPrepaymentRelation(BaseMethod):
    def __init__(self, relation_id: str):
        self.relation_id = relation_id

    @property
    def uri(self) -> str:
        return f"{URI_PREFIX}{self.relation_id}"


class CreateAfterPaymentReceipt(BaseMethod):
    method = HTTPMethod.POST

    def __init__(
        self,
        relation_id: str,
        receipt: Optional[Dict] = None,
        **payload,
    ):
        if receipt is not None and payload:
            raise ValueError("'receipt' and '**payload' can not be passed together")
        self.receipt = receipt or payload
        self.relation_id = relation_id

    @property
    def uri(self) -> str:
        return f"{URI_PREFIX}{self.relation_id}"

    @property
    def payload(self):
        payload = super().payload
        payload.update(self.receipt)
        return payload

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        storage.shift = result["shift"]
        return result


class CreatePrepaymentReceipt(BaseMethod):
    method = HTTPMethod.POST
    uri = "prepayment-receipts"

    def __init__(
        self,
        receipt: Optional[Dict] = None,
        **payload,
    ):
        if receipt is not None and payload:
            raise ValueError("'receipt' and '**payload' can not be passed together")
        self.receipt = receipt or payload

    @property
    def payload(self):
        payload = super().payload
        payload.update(self.receipt)
        return payload

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        storage.shift = result["shift"]
        return result


class GetPrepaymentReceiptsChain(BaseMethod):
    method = HTTPMethod.POST

    def __init__(
        self,
        relation_id: str,
        data: Optional[Dict] = None,
        **payload,
    ):
        if data is not None and payload:
            raise ValueError("'data' and '**payload' can not be passed together")
        self.data = data or payload
        self.relation_id = relation_id

    @property
    def uri(self) -> str:
        return f"{URI_PREFIX}{self.relation_id}/return"

    @property
    def payload(self):
        payload = super().payload
        payload.update(self.data)
        return payload
