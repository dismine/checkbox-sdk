import datetime
from typing import Optional, Union, List, Dict
from uuid import UUID

from httpx import Response

from checkbox_sdk.methods.base import BaseMethod, HTTPMethod, PaginationMixin
from checkbox_sdk.storage.simple import SessionStorage

URI_PREFIX = "orders/"


class RunOrdersSynchronization(BaseMethod):
    method = HTTPMethod.POST
    uri = f"{URI_PREFIX}sync"

    def parse_response(self, storage: SessionStorage, response: Response):
        return response.content.decode()


class GetOrders(PaginationMixin, BaseMethod):
    uri = "orders"

    def __init__(
        self,
        desc: Optional[bool] = True,
        delivery_desc: Optional[bool] = None,
        orders_all: Optional[bool] = False,
        delivered_from_date: Optional[Union[datetime.datetime, str]] = None,
        delivered_to_date: Optional[Union[datetime.datetime, str]] = None,
        status: Optional[List[str]] = None,
        stock_code: Optional[str] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.desc = desc
        self.delivery_desc = delivery_desc
        self.orders_all = orders_all
        self.delivered_from_date = delivered_from_date
        self.delivered_to_date = delivered_to_date
        self.status = status
        self.stock_code = stock_code

    @property
    def query(self):
        query = super().query

        if self.desc is not None:
            query["desc"] = self.desc

        if self.delivery_desc is not None:
            query["delivery_desc"] = self.delivery_desc

        if self.orders_all is not None:
            query["orders_all"] = self.orders_all

        if isinstance(self.delivered_from_date, datetime.datetime):
            query["delivered_from_date"] = self.delivered_from_date.isoformat()
        elif self.delivered_from_date:
            query["delivered_from_date"] = self.delivered_from_date

        if isinstance(self.delivered_to_date, datetime.datetime):
            query["delivered_to_date"] = self.delivered_to_date.isoformat()
        elif self.delivered_to_date:
            query["delivered_to_date"] = self.delivered_to_date

        if self.status is not None:
            query["status"] = self.status

        if self.stock_code is not None:
            query["stock_code"] = self.stock_code

        return query


class AddOrders(BaseMethod):
    method = HTTPMethod.POST
    uri = "orders"

    def __init__(
        self,
        orders: Optional[Union[List[Dict], Dict]] = None,
        **payload,
    ):
        if orders is not None and payload:
            raise ValueError("'orders' and '**payload' can not be passed together")
        self.orders = orders or payload

    @property
    def payload(self):
        payload = super().payload
        payload.update(self.orders)
        return payload


class GetIntegration(BaseMethod):
    uri = f"{URI_PREFIX}integration"


class SetIntegration(BaseMethod):
    method = HTTPMethod.POST
    uri = f"{URI_PREFIX}integration"

    def __init__(
        self,
        url: str,
    ):
        self.url = url

    @property
    def payload(self):
        payload = super().payload
        payload["url"] = self.url
        return payload


class DeleteIntegration(BaseMethod):
    method = HTTPMethod.DELETE
    uri = f"{URI_PREFIX}integration"


class GetOrder(BaseMethod):
    def __init__(self, order_id: Union[str, UUID], orders_all: Optional[bool] = False):
        self.order_id = order_id
        self.orders_all = orders_all

    @property
    def uri(self) -> str:
        order_id_str = str(self.order_id) if isinstance(self.order_id, UUID) else self.order_id
        return f"{URI_PREFIX}{order_id_str}"

    @property
    def query(self):
        query = super().query

        if self.orders_all is not None:
            query["orders_all"] = self.orders_all

        return query


class CancelOrder(BaseMethod):
    method = HTTPMethod.PATCH

    def __init__(self, order_id: Union[str, UUID]):
        self.order_id = order_id

    @property
    def uri(self) -> str:
        order_id_str = str(self.order_id) if isinstance(self.order_id, UUID) else self.order_id
        return f"{URI_PREFIX}{order_id_str}"


class CloseNotFiscalizeOrder(BaseMethod):
    method = HTTPMethod.PATCH
    uri = f"{URI_PREFIX}close"

    def __init__(self, order_id: Union[str, UUID]):
        self.order_id = order_id

    @property
    def query(self):
        query = super().query
        query["order_id"] = str(self.order_id) if isinstance(self.order_id, UUID) else self.order_id
        return query


class EditOrder(BaseMethod):
    method = HTTPMethod.POST
    uri = f"{URI_PREFIX}integration/edit-order"

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


class UpdateCustomOrderStatus(BaseMethod):
    method = HTTPMethod.PATCH

    def __init__(self, order_id: Union[str, UUID], new_status: Optional[str] = None):
        self.order_id = order_id
        self.new_status = new_status

    @property
    def uri(self) -> str:
        order_id_str = str(self.order_id) if isinstance(self.order_id, UUID) else self.order_id
        return f"{URI_PREFIX}custom_status/{order_id_str}"

    @property
    def query(self):
        query = super().query

        if self.new_status is not None:
            query["new_status"] = self.new_status

        return query


class DeleteOrder(BaseMethod):
    method = HTTPMethod.POST
    internal = True

    def __init__(self, order_id: Union[str, UUID]):
        self.order_id = order_id

    @property
    def uri(self) -> str:
        order_id_str = str(self.order_id) if isinstance(self.order_id, UUID) else self.order_id
        return f"_internal/{URI_PREFIX}{order_id_str}"
