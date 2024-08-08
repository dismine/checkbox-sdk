from datetime import datetime
from enum import Enum
from typing import Optional, List, Union
from uuid import UUID

from pydantic import conint, constr

from .base import CheckboxBaseModel
from .shift_models import ShiftSchema, TransactionSchema


class ReceiptStatusEnum(str, Enum):
    CREATED = "CREATED"
    DONE = "DONE"
    ERROR = "ERROR"
    CANCELLATION = "CANCELLATION"
    CANCELLED = "CANCELLED"


class DiscountTypeEnum(str, Enum):
    DISCOUNT = "DISCOUNT"
    PRE_PAYMENT = "PRE_PAYMENT"
    EXTRA_CHARGE = "EXTRA_CHARGE"


class DiscountModeEnum(str, Enum):
    PERCENT = "PERCENT"
    VALUE = "VALUE"


class CashPaymentTypeEnum(str, Enum):
    CASH = "CASH"


class CardPaymentTypeEnum(str, Enum):
    CASHLESS = "CASHLESS"


class CardPaymentProviderTypeEnum(str, Enum):
    TAPXPHONE = "TAPXPHONE"
    POSCONTROL = "POSCONTROL"
    TERMINAL = "TERMINAL"


class ReceiptFiscalApiTypeEnum(str, Enum):
    FSCO_EC = "FSCO_EC"
    EVPEZ = "EVPEZ"
    EVPEZ_EXTERNAL = "EVPEZ_EXTERNAL"


class ReceiptTypeEnum(str, Enum):
    SELL = "SELL"
    RETURN = "RETURN"
    SERVICE_IN = "SERVICE_IN"
    SERVICE_OUT = "SERVICE_OUT"
    SERVICE_CURRENCY = "SERVICE_CURRENCY"
    CURRENCY_EXCHANGE = "CURRENCY_EXCHANGE"
    PAWNSHOP = "PAWNSHOP"
    CASH_WITHDRAWAL = "CASH_WITHDRAWAL"


class CurrencyExchangeTypeEnum(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    CONVERT = "CONVERT"


class ServiceCurrencyExchangeTypeEnum(str, Enum):
    ADVANCE = "ADVANCE"
    REINFORCEMENT = "REINFORCEMENT"
    COLLECTION = "COLLECTION"


class GoodsTaxSchema(CheckboxBaseModel):
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
    value: int
    extra_value: int


class ReceiptGoodSchema(CheckboxBaseModel):
    code: str
    barcode: Optional[str]
    name: str
    excise_barcodes: Optional[List[str]]
    header: Optional[str]
    footer: Optional[str]
    uktzed: Optional[str]
    price: int


class ReceiptDiscountsSchema(CheckboxBaseModel):
    type: DiscountTypeEnum
    mode: DiscountModeEnum
    value: conint(gt=0)  # type: ignore[valid-type]
    tax_code: Optional[Union[int, str]]
    tax_codes: Optional[List[Union[int, str]]]
    name: Optional[str]
    privilege: Optional[str]
    sum: int


class ReceiptGoodsSchema(CheckboxBaseModel):
    good: ReceiptGoodSchema
    good_id: Optional[UUID]
    sum: int
    quantity: int
    is_return: bool
    taxes: List[GoodsTaxSchema]
    discounts: Optional[List[ReceiptDiscountsSchema]]


class CashPaymentSchema(CheckboxBaseModel):
    type: Optional[CashPaymentTypeEnum] = CashPaymentTypeEnum.CASH
    pawnshop_is_return: Optional[bool]
    value: int
    label: Optional[str] = "Готівка"


class CardPaymentSchema(CheckboxBaseModel):
    type: Optional[CardPaymentTypeEnum] = CardPaymentTypeEnum.CASHLESS
    pawnshop_is_return: Optional[bool]
    provider_type: Optional[CardPaymentProviderTypeEnum]
    code: Optional[conint(ge=0, le=10)]  # type: ignore[valid-type]
    value: Optional[conint(ge=-100000000000, le=100000000000)]  # type: ignore[valid-type]
    commission: Optional[int]
    label: Optional[constr(min_length=1, max_length=128)] = "Картка"  # type: ignore[valid-type]
    card_mask: Optional[constr(max_length=19)]  # type: ignore[valid-type]
    bank_name: Optional[str]
    auth_code: Optional[str]
    rrn: Optional[str]
    payment_system: Optional[str]
    owner_name: Optional[str]
    terminal: Optional[str]
    acquirer_and_seller: Optional[str]
    receipt_no: Optional[str]
    signature_required: Optional[bool]
    tapxphone_terminal: Optional[UUID]


class ServiceReceiptTaxesSchema(CheckboxBaseModel):
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
    value: int
    extra_value: int


class ServiceReceiptCustomSchema(CheckboxBaseModel):
    html_global_header: Optional[str]
    html_global_footer: Optional[str]
    html_body_style: Optional[str]
    html_receipt_style: Optional[str]
    html_ruler_style: Optional[str]
    html_light_block_style: Optional[str]
    text_global_header: Optional[str]
    text_global_footer: Optional[str]


class ServiceReceiptCurrencyOperationRateSchema(CheckboxBaseModel):
    code: str
    symbol_codes: str
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


class ServiceReceiptCurrencyOperationSchema(CheckboxBaseModel):
    currency: str
    value: Optional[float]
    rate: ServiceReceiptCurrencyOperationRateSchema


class ServiceReceiptCurrencyExchangeSchema(CheckboxBaseModel):
    sell: Optional[ServiceReceiptCurrencyOperationSchema]
    buy: Optional[ServiceReceiptCurrencyOperationSchema]
    type: CurrencyExchangeTypeEnum
    reversal: Optional[bool] = False
    client_info: Optional[str]
    commission: Optional[float]
    cross: Optional[float]


class ServiceReceiptServiceCurrencyExchangeSchema(CheckboxBaseModel):
    type: ServiceCurrencyExchangeTypeEnum
    currency: str
    value: float


class ReceiptSchema(CheckboxBaseModel):
    id: UUID
    serial: int
    status: ReceiptStatusEnum
    goods: List[ReceiptGoodsSchema]
    payments: List[Union[CashPaymentSchema, CardPaymentSchema]]
    total_sum: int
    total_payment: int
    total_rest: int
    round_sum: Optional[int]
    fiscal_code: Optional[str]
    fiscal_date: Optional[datetime]
    delivered_at: Optional[datetime]
    taxes: List[ServiceReceiptTaxesSchema]
    discounts: Optional[List[ReceiptDiscountsSchema]]
    created_at: datetime
    updated_at: Optional[datetime]
    is_created_offline: Optional[bool] = False
    is_sent_dps: Optional[bool] = False
    fiscal_api_type: Optional[ReceiptFiscalApiTypeEnum] = None
    type: ReceiptTypeEnum
    transaction: Optional[TransactionSchema]
    order_id: Optional[UUID]
    header: Optional[str]
    footer: Optional[str]
    barcode: Optional[str]
    custom: Optional[ServiceReceiptCustomSchema]
    context: Optional[Union[str, int, float, bool]]
    sent_dps_at: Optional[datetime]
    tax_url: Optional[str]
    related_receipt_id: Optional[UUID]
    technical_return: Optional[bool] = False
    stock_code: Optional[str]
    currency_exchange: Optional[List[ServiceReceiptCurrencyExchangeSchema]]
    service_currency_exchange: Optional[List[ServiceReceiptServiceCurrencyExchangeSchema]]
    pre_payment_relation_id: Optional[str]
    control_number: Optional[str]
    shift: ShiftSchema


class BulkReceiptSchema(CheckboxBaseModel):
    id: Optional[str]
    status: str
    message: Optional[str]
