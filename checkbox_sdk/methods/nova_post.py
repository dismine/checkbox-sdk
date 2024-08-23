from typing import Optional, Union, Dict
from uuid import UUID

from httpx import Response

from checkbox_sdk.methods.base import BaseMethod, HTTPMethod
from checkbox_sdk.methods.invoices import GetInvoices
from checkbox_sdk.storage.simple import SessionStorage

URI_PREFIX = "np/"


class GetEttnOrders(GetInvoices):
    uri = f"{URI_PREFIX}ettn"


class PostEttnOrder(BaseMethod):
    method = HTTPMethod.POST
    uri = f"{URI_PREFIX}ettn"

    def __init__(
        self,
        order: Optional[Dict] = None,
        **payload,
    ):  # pylint: disable=duplicate-code
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
