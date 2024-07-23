import datetime

from httpx import Response

from checkbox_sdk.methods.base import BaseMethod, HTTPMethod, PaginationMixin
from checkbox_sdk.storage.simple import SessionStorage


class GetReports(PaginationMixin, BaseMethod):
    uri = "reports"


class GetReport(BaseMethod):
    def __init__(self, report_id: str):
        self.report_id = report_id

    @property
    def uri(self) -> str:
        return f"reports/{self.report_id}"


class CreateReport(BaseMethod):
    method = HTTPMethod.POST
    uri = "reports"


class GetReportVisualization(GetReport):
    def __init__(self, report_id: str, fmt: str = "text", **query):
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
    def __init__(self, report_id: str, width: int = 50):
        super().__init__(report_id=report_id, fmt="text", width=width)

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        return result.decode()


class GetPeriodicalReportVisualizationText(BaseMethod):
    uri = "reports/periodical"

    def __init__(
        self,
        from_date: datetime.datetime,
        to_date: datetime.datetime,
        width: int = 50,
        is_short: bool = False,
    ):
        super().__init__()
        self.from_date = from_date
        self.to_date = to_date
        self.width = width
        self.is_short = is_short

    @property
    def query(self):
        query = super().query
        query.update(
            {
                "from_date": self.from_date.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "to_date": self.to_date.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "is_short": self.is_short,
            }
        )
        if self.width:
            query["width"] = self.width
        return query

    def parse_response(self, storage: SessionStorage, response: Response):
        return response.content.decode()
