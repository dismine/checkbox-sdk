from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID

from pydantic import Field

from .base import CheckboxBaseModel


class ShiftStatusEnum(str, Enum):
    CREATED = "CREATED"
    OPENING = "OPENING"
    OPENED = "OPENED"
    CLOSING = "CLOSING"
    CLOSED = "CLOSED"


class FiscalApiTypeEnum(str, Enum):
    FSCO_EC = "FSCO_EC"
    EVPEZ = "EVPEZ"
    EVPEZ_EXTERNAL = "EVPEZ_EXTERNAL"


class PaymentTypeEnum(str, Enum):
    CASH = "CASH"
    CARD = "CARD"
    CASHLESS = "CASHLESS"


class ProviderTypeEnum(str, Enum):
    TAPXPHONE = "TAPXPHONE"
    POSCONTROL = "POSCONTROL"
    TERMINAL = "TERMINAL"


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


class OrdersSourceEnum(str, Enum):
    UNSET = "UNSET"
    MOYO = "MOYO"
    FOXTROT = "FOXTROT"


class OrganizationSchema(CheckboxBaseModel):
    id: UUID
    title: str
    edrpou: str
    tax_number: str
    created_at: datetime
    updated_at: Optional[datetime]
    subscription_exp: Optional[datetime]
    receipts_ratelimit_count: Optional[int]
    receipts_ratelimit_interval: Optional[int]
    can_send_sms: Optional[bool]
    use_seamless_mode: Optional[bool]
    allowed_offline_duration: Optional[int]
    is_vat: Optional[bool]
    offline_mode: Optional[bool]
    auto_collection_on_close: Optional[bool]


class BranchSchema(CheckboxBaseModel):
    id: UUID
    name: str
    address: str
    organization: OrganizationSchema
    vehicle_license_plate: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]


class PaymentSchema(CheckboxBaseModel):
    id: UUID
    code: Optional[int]
    type: ProviderTypeEnum
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


class CashRegistersSchema(CheckboxBaseModel):
    id: UUID
    fiscal_number: str
    active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    number: Optional[str]
    is_test: bool
    shift: Optional[ShiftSchema]
    offline_mode: Optional[bool] = False
    stay_offline: Optional[bool] = False
    branch: Optional[BranchSchema]
    address: Optional[str]
    type: Optional[int]


class DocumentsState(CheckboxBaseModel):
    last_receipt_code: int
    last_report_code: int
    last_z_report_code: int


class CashRegistersInfoSchema(CheckboxBaseModel):
    id: UUID
    organization_id: UUID
    fiscal_number: str
    created_at: datetime
    updated_at: Optional[datetime]
    number: Optional[str]
    address: str
    title: str
    offline_mode: bool
    stay_offline: bool
    has_shift: bool
    documents_state: DocumentsState
    emergency_date: Optional[datetime]
    emergency_details: Optional[str]
    is_test: bool
    type: Optional[int]
    has_monobank_terminal: Optional[bool]
    has_qr_acquiring: Optional[bool]
    has_internet_acquiring: Optional[bool]
    has_iban_acquiring: Optional[bool]
    fiscal_api_type: Optional[FiscalApiTypeEnum] = None
    vehicle_license_plate: Optional[str] = None
    object_type: Optional[str] = None
    show_type_object: Optional[bool] = None
    date_field: Optional[datetime] = Field(None, alias="@date")
