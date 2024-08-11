import datetime
from typing import Optional, Union, Dict
from uuid import UUID

from httpx import Response

from checkbox_sdk.methods.base import BaseMethod, HTTPMethod, PaginationMixin
from checkbox_sdk.storage.simple import SessionStorage

URI_PREFIX = "np/"


class GetEttnOrders(PaginationMixin, BaseMethod):
    uri = f"{URI_PREFIX}ettn"

    def __init__(
        self,
        status: Optional[str] = None,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.status = status
        self.from_date = from_date
        self.to_date = to_date

    @property
    def query(self):
        query = super().query

        if self.status is not None:
            query["status"] = self.status

        if isinstance(self.from_date, datetime.datetime):
            query["from_date"] = self.from_date.isoformat()
        elif self.from_date:
            query["from_date"] = self.from_date

        if isinstance(self.to_date, datetime.datetime):
            query["to_date"] = self.to_date.isoformat()
        elif self.to_date:
            query["to_date"] = self.to_date

        return query


class PostEttnOrder(BaseMethod):
    method = HTTPMethod.POST
    uri = f"{URI_PREFIX}ettn"

    def __init__(
        self,
        order: Optional[Dict] = None,
        **payload,
    ):
        if order is not None and payload:
            raise ValueError("'order' and '**payload' can not be passed together")
        self.order = order or payload

    @property
    def payload(self):
        payload = super().payload
        payload.update(self.order)
        return payload

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        return result.decode()


class PostEttnPrepaymentOrder(BaseMethod):
    method = HTTPMethod.POST
    uri = f"{URI_PREFIX}ettn/prepayment"

    def __init__(
        self,
        order: Optional[Dict] = None,
        **payload,
    ):
        if order is not None and payload:
            raise ValueError("'order' and '**payload' can not be passed together")
        self.order = order or payload

    @property
    def payload(self):
        payload = super().payload
        payload.update(self.order)
        return payload

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        return result.decode()


class GetEttnOrder(BaseMethod):
    def __init__(self, order_id: Union[str, UUID]):
        self.order_id = order_id

    @property
    def uri(self) -> str:
        order_id_str = str(self.order_id) if isinstance(self.order_id, UUID) else self.order_id
        return f"{URI_PREFIX}ettn/{order_id_str}"

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        return result.decode()


class UpdateEttnOrder(BaseMethod):
    method = HTTPMethod.PUT

    def __init__(
        self,
        order_id: Union[str, UUID],
        delivery_phone: Optional[str] = None,
        delivery_email: Optional[str] = None,
    ):
        self.order_id = order_id
        self.delivery_phone = delivery_phone
        self.delivery_email = delivery_email

    @property
    def uri(self) -> str:
        order_id_str = str(self.order_id) if isinstance(self.order_id, UUID) else self.order_id
        return f"{URI_PREFIX}ettn/{order_id_str}"

    @property
    def payload(self):
        payload = super().payload

        if self.delivery_phone is not None:
            payload["delivery_phone"] = self.delivery_phone

        if self.delivery_email is not None:
            payload["delivery_email"] = self.delivery_email

        return payload

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        return result.decode()


class DeleteEttnOrder(BaseMethod):
    method = HTTPMethod.DELETE

    def __init__(
        self,
        order_id: Union[str, UUID],
    ):
        self.order_id = order_id

    @property
    def uri(self) -> str:
        order_id_str = str(self.order_id) if isinstance(self.order_id, UUID) else self.order_id
        return f"{URI_PREFIX}ettn/{order_id_str}"

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        return result.decode()
