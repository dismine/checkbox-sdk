import datetime
from typing import List, Optional, Union, Dict
from uuid import UUID

from httpx import Response

from checkbox_sdk.methods.base import BaseMethod, HTTPMethod, PaginationMixin
from checkbox_sdk.storage.simple import SessionStorage


class GetShifts(PaginationMixin, BaseMethod):
    uri = "shifts"

    def __init__(
        self,
        statuses: Optional[List[str]] = None,
        desc: Optional[bool] = False,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.statuses = statuses
        self.desc = desc
        self.from_date = from_date
        self.to_date = to_date

    @property
    def query(self):
        query = super().query

        if self.statuses is not None:
            query["statuses"] = self.statuses

        if self.desc is not None:
            query["desc"] = self.desc

        if isinstance(self.from_date, datetime.datetime):
            query["from_date"] = self.from_date.isoformat()
        elif self.from_date:
            query["from_date"] = self.from_date

        if isinstance(self.to_date, datetime.datetime):
            query["to_date"] = self.to_date.isoformat()
        elif self.to_date:
            query["to_date"] = self.to_date

        return query


class CreateShift(BaseMethod):
    method = HTTPMethod.POST
    uri = "shifts"

    def __init__(self, **payload):
        self._payload = payload

    @property
    def payload(self):
        payload = super().payload
        payload.update(self._payload)
        return payload

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        storage.shift = result
        return result


class GetShift(BaseMethod):
    def __init__(self, shift_id: str):
        self.shift_id = shift_id

    @property
    def uri(self) -> str:
        return f"shifts/{self.shift_id}"

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        if storage.shift and storage.shift["id"] == result["id"]:
            storage.shift = result
        return result


class CloseShiftBySeniorCashier(BaseMethod):
    method = HTTPMethod.POST

    def __init__(self, shift_id: Union[str, UUID], shift: Optional[Dict] = None, **payload):
        self.shift_id = shift_id

        if shift is not None and payload:
            raise ValueError("'shift' and '**payload' can not be passed together")
        self.shift = shift or payload

    @property
    def uri(self) -> str:
        shift_id_str = str(self.shift_id) if isinstance(self.shift_id, UUID) else self.shift_id
        return f"shifts/{shift_id_str}/close"

    @property
    def payload(self):
        payload = super().payload
        payload.update(self.shift)
        return payload

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        storage.shift = result
        return result


class CloseShift(BaseMethod):
    method = HTTPMethod.POST
    uri = "shifts/close"

    def __init__(self, **payload):
        self._payload = payload

    @property
    def payload(self):
        payload = super().payload
        payload.update(self._payload)
        return payload

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        storage.shift = result
        return result
