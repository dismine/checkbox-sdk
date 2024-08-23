from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from ..models.base import CheckboxBaseModel


class PrePaymentStatusEnum(str, Enum):
    PARTIAL_PAID = "PARTIAL_PAID"
    FULL_PAID = "FULL_PAID"
    CANCELLED = "CANCELLED"
    PARTIAL_CANCELLED = "PARTIAL_CANCELLED"


class ReceiptChainSchema(CheckboxBaseModel):
    returned_receipts: List[UUID]
    after_payment_receipt: UUID
    pre_payment_receipts: List[UUID]


class PrepaymentRelationSchema(CheckboxBaseModel):
    id: UUID
    relation_id: str
    paid_sum: float
    total_sum: float
    left_to_pay: Optional[float] = 0
    paid_by_cash_sum: Optional[float]
    last_returned_receipt_at: Optional[datetime]
    receipt_chain_count: Optional[int]
    is_debt_receipt: Optional[bool]
    pre_payment_status: PrePaymentStatusEnum
    created_at: datetime
    updated_at: Optional[datetime]
    receipt_chain: ReceiptChainSchema
