import datetime
from typing import Optional, Union, List, Dict
from uuid import UUID

from httpx import Response

from checkbox_sdk.methods.base import BaseMethod, HTTPMethod, PaginationMixin
from checkbox_sdk.storage.simple import SessionStorage

URI_PREFIX = "reports/"


class GetPeriodicalReport(BaseMethod):
    uri = f"{URI_PREFIX}periodical"

    def __init__(
        self,
        from_date: Union[datetime.datetime, str],
        to_date: Union[datetime.datetime, str],
        width: Optional[int] = 42,
        is_short: Optional[bool] = False,
    ):
        super().__init__()
        self.from_date = from_date
        self.to_date = to_date
        self.width = width
        self.is_short = is_short

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

        if self.width:
            query["width"] = self.width

        if self.is_short is not None:
            query["is_short"] = self.is_short

        return query

    def parse_response(self, storage: SessionStorage, response: Response):
        return response.content.decode()


class GetReports(PaginationMixin, BaseMethod):
    uri = "reports"

    def __init__(
        self,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        shift_id: Optional[List[str]] = None,
        serial: Optional[int] = None,
        is_z_report: Optional[bool] = None,
        desc: Optional[bool] = False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.from_date = from_date
        self.to_date = to_date
        self.shift_id = shift_id
        self.serial = serial
        self.is_z_report = is_z_report
        self.desc = desc

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

        if self.shift_id is not None:
            query["shift_id"] = self.shift_id

        if self.serial is not None:
            query["serial"] = self.serial

        if self.is_z_report is not None:
            query["is_z_report"] = self.is_z_report

        if self.desc is not None:
            query["desc"] = self.desc

        return query


class CreateXReport(BaseMethod):
    method = HTTPMethod.POST
    uri = "reports"


class SearchReports(PaginationMixin, BaseMethod):
    uri = f"{URI_PREFIX}search"

    def __init__(
        self,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        shift_id: Optional[List[str]] = None,
        serial: Optional[int] = None,
        is_z_report: Optional[bool] = None,
        desc: Optional[bool] = False,
        cash_register_id: Optional[List[str]] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.from_date = from_date
        self.to_date = to_date
        self.shift_id = shift_id
        self.serial = serial
        self.is_z_report = is_z_report
        self.desc = desc
        self.cash_register_id = cash_register_id

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

        if self.shift_id is not None:
            query["shift_id"] = self.shift_id

        if self.serial is not None:
            query["serial"] = self.serial

        if self.is_z_report is not None:
            query["is_z_report"] = self.is_z_report

        if self.desc is not None:
            query["desc"] = self.desc

        if self.cash_register_id is not None:
            query["cash_register_id"] = self.cash_register_id

        return query


class AddExternal(BaseMethod):
    method = HTTPMethod.POST
    uri = f"{URI_PREFIX}add-external"

    def __init__(
        self,
        report: Optional[Dict] = None,
        **payload,
    ):
        if report is not None and payload:
            raise ValueError("'report' and '**payload' can not be passed together")
        self.report = report or payload

    @property
    def payload(self):
        payload = super().payload
        payload.update(self.report)
        return payload


class GetReport(BaseMethod):
    def __init__(self, report_id: Union[str, UUID]):
        self.report_id = report_id

    @property
    def uri(self) -> str:
        report_id_str = str(self.report_id) if isinstance(self.report_id, UUID) else self.report_id
        return f"{URI_PREFIX}{report_id_str}"


class GetReportVisualization(GetReport):
    def __init__(self, report_id: Union[str, UUID], fmt: str = "text", **query):
        super().__init__(report_id=report_id)
        self.format = fmt
        self.params = query

    @property
    def query(self):
        query = super().query
        query.update(self.params)
        return query

    @property
    def uri(self) -> str:
        uri = super().uri
        return f"{uri}/{self.format}"

    def parse_response(self, storage: SessionStorage, response: Response):
        return response.content


class GetReportVisualizationText(GetReportVisualization):
    def __init__(self, report_id: Union[str, UUID], width: Optional[int] = 42):
        super().__init__(report_id=report_id, fmt="text", width=width)

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        return result.decode()


class GetReportVisualizationPng(GetReportVisualization):
    def __init__(self, report_id: Union[str, UUID], width: Optional[int] = 34, paper_width: Optional[int] = 58):
        super().__init__(report_id=report_id, fmt="text", width=width, paper_width=paper_width)

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        return result.decode()
