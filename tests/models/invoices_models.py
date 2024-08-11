from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from ..models.base import CheckboxBaseModel


class TerminalAcquiringTypeEnum(str, Enum):
    INTERNET = "INTERNET"
    QR = "QR"


class InvoiceStatusEnum(str, Enum):
    CREATED = "CREATED"
    PROCESSING = "PROCESSING"
    HOLD = "HOLD"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    REVERSED = "REVERSED"
    REQUEST_TO_CANCEL = "REQUEST_TO_CANCEL"
    EXPIRED = "EXPIRED"


class TerminalSchema(CheckboxBaseModel):
    id: UUID
    qr_id: Optional[str]
    cash_register_id: UUID
    organization_id: UUID
    type: str
    acquiring_type: Optional[TerminalAcquiringTypeEnum]
    created_at: datetime
    updated_at: Optional[datetime]


class InvoiceSchema(CheckboxBaseModel):
    id: UUID
    receipt: Optional[UUID]
    terminal_id: UUID
    external_id: str
    status: InvoiceStatusEnum
    transaction_id: Optional[str]
    page_url: Optional[str]
    amount: Optional[int]
    ccy: Optional[int]
    final_amount: Optional[int]
    failure_reason: Optional[str]
    reference: Optional[str]
    validity: Optional[int]
    tips_employee_id: Optional[str]
    card_mask: Optional[str]
    auth_code: Optional[str]
    rrn: Optional[str]
    commission: Optional[int]
    terminal_name: Optional[str]
    created_at: datetime
    updated_at: datetime
