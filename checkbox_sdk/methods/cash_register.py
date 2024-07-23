import datetime
from typing import Optional, Union

from httpx import Response

from checkbox_sdk.methods.base import BaseMethod, HTTPMethod, PaginationMixin
from checkbox_sdk.storage.simple import SessionStorage


class GetCashRegisters(PaginationMixin, BaseMethod):
    uri = "cash-registers"


class GetCashRegister(BaseMethod):
    def __init__(self, cash_register_id: str):
        self.cash_register_id = cash_register_id

    @property
    def uri(self) -> str:
        return f"cash-registers/{self.cash_register_id}"


class GetCashRegisterInfo(BaseMethod):
    uri: str = "cash-registers/info"

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        storage.cash_register = result
        return result


class AskOfflineCodes(BaseMethod):
    uri = "cash-registers/ask-offline-codes"

    def __init__(self, count: int = 2000, sync: bool = False):
        self.count = count
        self.sync = sync

    @property
    def query(self):
        query = super().query
        query.update({"count": self.count, "sync": self.sync})
        return query


class GetOfflineCodes(BaseMethod):
    uri = "cash-registers/get-offline-codes"

    def __init__(self, count: int = 2000):
        self.count = count

    @property
    def query(self):
        query = super().query
        query.update({"count": self.count})
        return query


class GoOnline(BaseMethod):
    uri = "cash-registers/go-online"
    method = HTTPMethod.POST


class GoOffline(BaseMethod):
    uri = "cash-registers/go-offline"
    method = HTTPMethod.POST

    def __init__(
        self,
        go_offline_date: Optional[Union[datetime.datetime, str]] = None,
        fiscal_code: Optional[str] = None,
    ):
        self.go_offline_date = go_offline_date
        self.fiscal_code = fiscal_code

    @property
    def payload(self):
        payload = super().payload
        if isinstance(self.go_offline_date, datetime.datetime):
            payload["go_offline_date"] = self.go_offline_date.isoformat()
        elif self.go_offline_date:
            payload["go_offline_date"] = self.go_offline_date
        if self.fiscal_code:
            payload["fiscal_code"] = self.fiscal_code
        return payload


class UpdateForceSeamlessMode(BaseMethod):
    uri = "cash-registers/force_seamless_mode"
    method = HTTPMethod.PATCH

    def __init__(self, new_status: bool):
        self.new_status = new_status

    @property
    def payload(self):
        payload = super().payload
        payload["new_status"] = self.new_status
        return payload
