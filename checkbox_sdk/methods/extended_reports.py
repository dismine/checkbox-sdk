from abc import ABC
from typing import Dict, Optional, List, Union
from uuid import UUID

from checkbox_sdk.methods.base import BaseMethod, HTTPMethod

URI_PREFIX = "extended-reports/"


class CreateReport(BaseMethod, ABC):
    method = HTTPMethod.POST

    def __init__(
        self,
        data: Optional[List[Dict]] = None,
        **payload,
    ):
        if data is not None and payload:
            raise ValueError("'data' and '**payload' can not be passed together")
        self.data = data or payload

    @property
    def payload(self):
        payload = super().payload
        payload.update(self.data)
        return payload


class CreateGoodsReport(CreateReport):
    uri = f"{URI_PREFIX}goods"


class CreateZReport(CreateReport):
    uri = f"{URI_PREFIX}z"


class CreateActualRevenueReport(CreateReport):
    uri = f"{URI_PREFIX}actual_revenue"


class CreateNetTurnoverReport(CreateReport):
    uri = f"{URI_PREFIX}net_turnover"


class CreateBookkeeperZReport(CreateReport):
    uri = f"{URI_PREFIX}bookkeeper_z_report"


class CreateDailyCashFlowReport(CreateReport):
    uri = f"{URI_PREFIX}daily_cash_flow"


class CreateReceiptReport(CreateReport):
    uri = f"{URI_PREFIX}receipt"


class GetReportTaskById(BaseMethod):
    def __init__(self, report_task_id: Union[str, UUID]):
        self.report_task_id = report_task_id

    @property
    def uri(self) -> str:
        report_task_id_str = str(self.report_task_id) if isinstance(self.report_task_id, UUID) else self.report_task_id
        return f"{URI_PREFIX}{report_task_id_str}"


class GetReportXlsxTaskById(BaseMethod):
    def __init__(self, report_task_id: Union[str, UUID]):
        self.report_task_id = report_task_id

    @property
    def uri(self) -> str:
        report_task_id_str = str(self.report_task_id) if isinstance(self.report_task_id, UUID) else self.report_task_id
        return f"{URI_PREFIX}{report_task_id_str}/report.xlsx"


class GetReportJsonTaskById(BaseMethod):
    def __init__(self, report_task_id: Union[str, UUID]):
        self.report_task_id = report_task_id

    @property
    def uri(self) -> str:
        report_task_id_str = str(self.report_task_id) if isinstance(self.report_task_id, UUID) else self.report_task_id
        return f"{URI_PREFIX}{report_task_id_str}/report.json"
