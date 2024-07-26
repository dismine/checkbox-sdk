from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID

from .base import CheckboxBaseModel
from .cashier_models import CashierSchema


class ShiftStatusEnum(str, Enum):
    CREATED = "CREATED"
    OPENING = "OPENING"
    OPENED = "OPENED"
    CLOSING = "CLOSING"
    CLOSED = "CLOSED"


class ProviderTypeEnum(str, Enum):
    TAPXPHONE = "TAPXPHONE"
    POSCONTROL = "POSCONTROL"
    TERMINAL = "TERMINAL"


class FiscalApiTypeEnum(str, Enum):
    FSCO_EC = "FSCO_EC"
    EVPEZ = "EVPEZ"
    EVPEZ_EXTERNAL = "EVPEZ_EXTERNAL"


class TransactionTypeEnum(str, Enum):
    SHIFT_OPEN = "SHIFT_OPEN"
    X_REPORT = "X_REPORT"
    Z_REPORT = "Z_REPORT"
    PING = "PING"
    RECEIPT = "RECEIPT"
    LAST_RECEIPT = "LAST_RECEIPT"
    GO_OFFLINE = "GO_OFFLINE"
    ASK_OFFLINE_CODES = "ASK_OFFLINE_CODES"
    GO_ONLINE = "GO_ONLINE"
    DEL_LAST_RECEIPT = "DEL_LAST_RECEIPT"
    STATUS_RRO = "STATUS_RRO"
    INFO_RRO = "INFO_RRO"


class TransactionStatusEnum(str, Enum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    SIGNED = "SIGNED"
    DELIVERED = "DELIVERED"
    DONE = "DONE"
    ERROR = "ERROR"
    CANCELLED = "CANCELLED"


class PaymentTypeEnum(str, Enum):
    CASH = "CASH"
    CARD = "CARD"
    CASHLESS = "CASHLESS"


class PaymentSchema(CheckboxBaseModel):
    id: UUID
    code: Optional[int]
    type: PaymentTypeEnum
    provider_type: Optional[ProviderTypeEnum]
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


class ZReportSchema(CheckboxBaseModel):
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
    transaction_fail: Optional[bool] = False
    rates: Optional[List[RateSchema]]
    fiscal_api_type: Optional[FiscalApiTypeEnum]


class TransactionSchema(CheckboxBaseModel):
    id: UUID
    type: TransactionTypeEnum
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
    z_report: Optional[ZReportSchema]
    opened_at: Optional[datetime]
    closed_at: Optional[datetime]
    initial_transaction: Optional[TransactionSchema]
    closing_transaction: Optional[TransactionSchema]
    created_at: datetime
    updated_at: Optional[datetime]
    balance: Optional[BalanceSchema]
    taxes: List[TaxesSchema]
    fiscal_api_type: Optional[FiscalApiTypeEnum]
    evpez_shift_id: Optional[str]
    emergency_close: Optional[bool]
    emergency_close_details: Optional[str]
    cashier: CashierSchema


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
    z_report: Optional[ZReportSchema]
    opened_at: Optional[datetime]
    closed_at: Optional[datetime]
    initial_transaction: Optional[TransactionSchema]
    closing_transaction: Optional[TransactionSchema]
    created_at: datetime
    updated_at: Optional[datetime]
    balance: Optional[BalanceSchema]
    taxes: List[TaxesSchema]
    fiscal_api_type: Optional[FiscalApiTypeEnum]
    evpez_shift_id: Optional[str]
    emergency_close: Optional[bool]
    emergency_close_details: Optional[str]
    cash_register: CashRegisterSchema
