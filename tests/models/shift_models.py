from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID

from .base import CheckboxBaseModel
from .cashier_models import CashierSchema
from .reports_models import ReportFiscalAPITypeEnum, FiscalReportSchema
from .transactions_models import TransactionsTypeEnum


class ShiftStatusEnum(str, Enum):
    CREATED = "CREATED"
    OPENING = "OPENING"
    OPENED = "OPENED"
    CLOSING = "CLOSING"
    CLOSED = "CLOSED"


class TransactionStatusEnum(str, Enum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    SIGNED = "SIGNED"
    DELIVERED = "DELIVERED"
    DONE = "DONE"
    ERROR = "ERROR"
    CANCELLED = "CANCELLED"


# pylint: disable=duplicate-code
class TaxSchema(CheckboxBaseModel):
    id: UUID
    code: int
    label: str
    symbol: str
    rate: int
    extra_rate: Optional[int]
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
    sell: int
    buy: int
    regulator: int
    created_at: datetime
    active: bool
    initial: Optional[int] = 0
    balance: Optional[int] = 0
    sell_sum: Optional[int] = 0
    reversal_sell_sum: Optional[int] = 0
    convert_sell_sum: Optional[int] = 0
    reversal_convert_sell_sum: Optional[int] = 0
    buy_sum: Optional[int] = 0
    reversal_buy_sum: Optional[int] = 0
    convert_buy_sum: Optional[int] = 0
    reversal_convert_buy_sum: Optional[int] = 0
    commission_sum: Optional[int] = 0
    reversal_commission_sum: Optional[int] = 0
    advance: Optional[int] = 0
    reinforcement: Optional[int] = 0
    collection: Optional[int] = 0
    updated_at: Optional[datetime]


class TransactionSchema(CheckboxBaseModel):
    id: UUID
    type: TransactionsTypeEnum
    serial: int
    status: TransactionStatusEnum
    request_signed_at: Optional[datetime]
    request_received_at: Optional[datetime]
    response_status: Optional[str]
    response_error_message: Optional[str]
    response_id: Optional[str]
    offline_id: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    original_datetime: Optional[datetime]
    previous_hash: Optional[str]


class BalanceSchema(CheckboxBaseModel):
    initial: int
    balance: int
    cash_sales: int
    card_sales: int
    discounts_sum: Optional[int]
    extra_charge_sum: Optional[int]
    cash_returns: int
    card_returns: int
    service_in: int
    service_out: int
    updated_at: Optional[datetime]


class TaxesSchema(CheckboxBaseModel):
    id: UUID
    code: int
    label: str
    symbol: str
    rate: int
    extra_rate: Optional[int]
    included: bool
    is_gambling: Optional[bool]
    created_at: datetime
    updated_at: Optional[datetime]
    no_vat: Optional[bool]
    advanced_code: Optional[str]
    sales: int
    returns: int
    sales_turnover: int
    returns_turnover: int


class ShiftSchema(CheckboxBaseModel):
    id: UUID
    serial: int
    status: ShiftStatusEnum
    z_report: Optional[FiscalReportSchema]
    opened_at: Optional[datetime]
    closed_at: Optional[datetime]
    initial_transaction: Optional[TransactionSchema]
    closing_transaction: Optional[TransactionSchema]
    created_at: datetime
    updated_at: Optional[datetime]
    balance: Optional[BalanceSchema]
    taxes: List[TaxesSchema]
    fiscal_api_type: Optional[ReportFiscalAPITypeEnum] = None
    evpez_shift_id: Optional[str] = None
    emergency_close: Optional[bool]
    emergency_close_details: Optional[str]
    cashier: Optional[CashierSchema] = None


class CashRegisterSchema(CheckboxBaseModel):
    id: UUID
    fiscal_number: str
    active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    number: Optional[str]


class ShiftInfoSchema(CheckboxBaseModel):
    id: UUID
    serial: int
    status: ShiftStatusEnum
    z_report: Optional[FiscalReportSchema]
    opened_at: Optional[datetime]
    closed_at: Optional[datetime]
    initial_transaction: Optional[TransactionSchema]
    closing_transaction: Optional[TransactionSchema]
    created_at: datetime
    updated_at: Optional[datetime]
    balance: Optional[BalanceSchema]
    taxes: List[TaxesSchema]
    fiscal_api_type: Optional[ReportFiscalAPITypeEnum]
    evpez_shift_id: Optional[str]
    emergency_close: Optional[bool]
    emergency_close_details: Optional[str]
    cash_register: CashRegisterSchema
