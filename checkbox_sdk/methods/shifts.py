from typing import List, Optional

from httpx import Response

from checkbox_sdk.methods.base import BaseMethod, HTTPMethod, PaginationMixin
from checkbox_sdk.storage.simple import SessionStorage


class GetShifts(PaginationMixin, BaseMethod):
    uri = "shifts"

    def __init__(self, statuses: Optional[List[str]] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.statuses = statuses

    @property
    def query(self):
        query = super().query
        if self.statuses is not None:
            query["statuses"] = self.statuses
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


class GetShiftLastReceiptID(BaseMethod):
    def __init__(self, shift_id: str):
        self.shift_id = shift_id

    @property
    def uri(self) -> str:
        return f"shifts/last_receipt_id/{self.shift_id}"

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        return result["status"], result["last_receipt_id"]
