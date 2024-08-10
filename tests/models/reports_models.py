from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from .base import CheckboxBaseModel


class PaymentTypeEnum(str, Enum):
    CASH = "CASH"
    CARD = "CARD"
    CASHLESS = "CASHLESS"


class PaymentProviderTypeEnum(str, Enum):
    TAPXPHONE = "TAPXPHONE"
    POSCONTROL = "POSCONTROL"
    TERMINAL = "TERMINAL"
    ANDROID_PAYLINK = "ANDROID_PAYLINK"
    DESKTOP_PAYLINK = "DESKTOP_PAYLINK"


class ReportFiscalAPITypeEnum(str, Enum):
    FSCO_EC = "FSCO_EC"
    EVPEZ = "EVPEZ"
    EVPEZ_EXTERNAL = "EVPEZ_EXTERNAL"


class PaymentSchema(CheckboxBaseModel):
    id: UUID
    code: Optional[int]
    type: PaymentTypeEnum
    provider_type: Optional[PaymentProviderTypeEnum]
    label: str
    sell_sum: int
    return_sum: int
    service_in: int
    service_out: int
    cash_withdrawal: int
    cash_withdrawal_commission: int


class TaxSchema(CheckboxBaseModel):
    id: UUID
    code: int
    label: str
    symbol: str
    rate: float
    extra_rate: Optional[float]
    sell_sum: int
    return_sum: int
    sales_turnover: int
    returns_turnover: int
    no_vat: Optional[bool]
    advanced_code: Optional[str]
    created_at: datetime
    setup_date: datetime


class RateSchema(CheckboxBaseModel):
    code: str
    symbol_code: str
    name: str
    sell: float
    buy: float
    regulator: float
    created_at: datetime
    active: bool
    initial: Optional[float] = 0
    balance: Optional[float] = 0
    sell_sum: Optional[float] = 0
    reversal_sell_sum: Optional[float] = 0
    convert_sell_sum: Optional[float] = 0
    reversal_convert_sell_sum: Optional[float] = 0
    buy_sum: Optional[float] = 0
    reversal_buy_sum: Optional[float] = 0
    convert_buy_sum: Optional[float] = 0
    reversal_convert_buy_sum: Optional[float] = 0
    commission_sum: Optional[float] = 0
    reversal_commission_sum: Optional[float] = 0
    advance: Optional[float] = 0
    reinforcement: Optional[float] = 0
    collection: Optional[float] = 0
    updated_at: Optional[datetime]


class FiscalReportSchema(CheckboxBaseModel):
    id: UUID
    shift_id: UUID
    last_receipt_id: Optional[UUID]
    fiscal_code: Optional[str]
    serial: int
    is_z_report: bool
    payments: List[PaymentSchema]
    taxes: List[TaxSchema]
    sell_receipts_count: int
    return_receipts_count: int
    cash_withdrawal_receipts_count: int
    transfers_count: int
    transfers_sum: int
    balance: int
    initial: int
    sales_round_up: int
    sales_round_down: int
    returns_round_up: int
    returns_round_down: int
    created_at: datetime
    updated_at: Optional[datetime]
    discounts_sum: Optional[int]
    extra_charge_sum: Optional[int]
    transaction_fail: Optional[bool]
    rates: Optional[List[RateSchema]]
    fiscal_api_type: Optional[ReportFiscalAPITypeEnum]
