from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from .base import CheckboxBaseModel


class OrdersSourceEnum(str, Enum):
    UNSET = "UNSET"
    MOYO = "MOYO"
    FOXTROT = "FOXTROT"


class CashierPermissionsSchema(CheckboxBaseModel):
    self_return: Optional[bool] = True
    orders: Optional[bool] = False
    add_discounts: Optional[bool] = True
    editing_goods_sum: Optional[bool] = True
    deferred_receipt: Optional[bool] = True
    editing_good_price: Optional[bool] = True
    can_add_manual_good: Optional[bool] = True
    service_in: Optional[bool] = True
    service_out: Optional[bool] = True
    returns: Optional[bool] = True
    sales: Optional[bool] = True
    card_payment: Optional[bool]
    cash_payment: Optional[bool]
    other_payment: Optional[bool]
    mixed_payment: Optional[bool]
    iban_payment: Optional[bool]
    branch_params: Optional[bool] = True
    reports_history: Optional[bool] = True
    additional_service_receipt: Optional[bool] = False
    free_return: Optional[bool] = False
    orders_source: Optional[OrdersSourceEnum] = OrdersSourceEnum.UNSET


class CashierSchema(CheckboxBaseModel):
    id: UUID
    full_name: str
    nin: str
    key_id: str
    signature_type: str
    permissions: Optional[CashierPermissionsSchema]
    created_at: datetime
    updated_at: Optional[datetime]
    certificate_end: Optional[datetime]
    blocked: Optional[str]
