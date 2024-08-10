from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from ..models.base import CheckboxBaseModel


class PublicReportTaskTypeEnum(str, Enum):
    GOODS = "GOODS"
    Z_REPORTS = "Z_REPORTS"
    RECEIPTS = "RECEIPTS"
    SHIFT_STATUSES = "SHIFT_STATUSES"
    NET_TURNOVER = "NET_TURNOVER"
    ACTUAL_REVENUE = "ACTUAL_REVENUE"
    BOOKKEEPER_Z_REPORT = "BOOKKEEPER_Z_REPORT"
    RECEIPTS_PACKAGE = "RECEIPTS_PACKAGE"
    DAILY_CASH_FLOW = "DAILY_CASH_FLOW"


class PublicReportTaskStatusEnum(str, Enum):
    PENDING = "PENDING"
    DONE = "DONE"
    ERROR = "ERROR"


class PublicReportTaskSchema(CheckboxBaseModel):
    id: UUID
    organization_id: UUID
    type: PublicReportTaskTypeEnum
    status: PublicReportTaskStatusEnum
    created_at: datetime
    updated_at: Optional[datetime]
