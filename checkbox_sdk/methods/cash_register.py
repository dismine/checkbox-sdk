import datetime
from typing import Optional, Union, List

from httpx import Response

from checkbox_sdk.methods.base import BaseMethod, HTTPMethod, PaginationMixin
from checkbox_sdk.storage.simple import SessionStorage

URI_PREFIX = "cash-registers/"


class GoOnline(BaseMethod):
    uri = f"{URI_PREFIX}go-online"
    method = HTTPMethod.POST


class GoOffline(BaseMethod):
    uri = f"{URI_PREFIX}go-offline"
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


class PingTaxService(BaseMethod):
    uri: str = f"{URI_PREFIX}ping-tax-service"
    method = HTTPMethod.POST


class AskOfflineCodes(BaseMethod):
    uri = f"{URI_PREFIX}ask-offline-codes"

    def __init__(self, count: int = 2000, sync: bool = False):
        self.count = count
        self.sync = sync

    @property
    def query(self):
        query = super().query
        query.update({"count": self.count, "sync": self.sync})
        return query


class GetOfflineCodes(BaseMethod):
    uri = f"{URI_PREFIX}get-offline-codes"

    def __init__(self, count: int = 2000):
        self.count = count

    @property
    def query(self):
        query = super().query
        query.update({"count": self.count})
        return query


class GetOfflineCodesCount(BaseMethod):
    uri = f"{URI_PREFIX}get-offline-codes-count"


class GetOfflineTime(BaseMethod):
    uri = f"{URI_PREFIX}get-offline-time"

    def __init__(
        self,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.from_date = from_date
        self.to_date = to_date

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

        return query


class GetCashRegisters(PaginationMixin, BaseMethod):
    uri = "cash-registers"

    def __init__(
        self,
        in_use: Optional[bool] = None,
        fiscal_number: Optional[str] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.in_use = in_use
        self.fiscal_number = fiscal_number

    @property
    def query(self):
        query = super().query

        if self.in_use is not None:
            query["in_use"] = self.in_use

        if self.fiscal_number is not None:
            query["fiscal_number"] = self.fiscal_number

        return query


class GetCashRegisterInfo(BaseMethod):
    uri: str = f"{URI_PREFIX}info"

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        storage.cash_register = result
        return result


class GetCashRegisterShifts(PaginationMixin, BaseMethod):
    uri: str = f"{URI_PREFIX}shifts"

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


class GetCashRegister(BaseMethod):
    def __init__(self, cash_register_id: str):
        self.cash_register_id = cash_register_id

    @property
    def uri(self) -> str:
        return f"{URI_PREFIX}{self.cash_register_id}"
