from datetime import datetime
from enum import Enum
from typing import List, Optional, Union
from uuid import UUID

from pydantic import EmailStr, Field

from .base import CheckboxBaseModel
from .receipts_models import ReceiptDiscountsSchema


class OrderStatusEnum(str, Enum):
    PENDING = "PENDING"
    SAVING = "SAVING"
    SUCCESS = "SUCCESS"
    CANCELLED = "CANCELLED"


class OrderCustomStatusEnum(str, Enum):
    NEW = "NEW"
    IN_WORK = "IN_WORK"
    APPROVED = "APPROVED"
    TRANSFERRED_TO_WMS = "TRANSFERRED_TO_WMS"
    PREPARING = "PREPARING"
    DELIVERING = "DELIVERING"
    DELIVERED = "DELIVERED"
    DONE = "DONE"
    CANCELED = "CANCELED"
    TEST = "TEST"


class OrderPaymentMethodEnum(str, Enum):
    CARD_AFTER_ASSEMBLING = "CARD_AFTER_ASSEMBLING"
    CASH_ON_DELIVERY = "CASH_ON_DELIVERY"
    CASHLESS_ON_DELIVERY = "CASHLESS_ON_DELIVERY"


class OrderReceiptDraftTypeEnum(str, Enum):
    SELL = "SELL"
    RETURN = "RETURN"
    SERVICE_IN = "SERVICE_IN"
    SERVICE_OUT = "SERVICE_OUT"
    SERVICE_CURRENCY = "SERVICE_CURRENCY"
    CURRENCY_EXCHANGE = "CURRENCY_EXCHANGE"
    PAWNSHOP = "PAWNSHOP"
    CASH_WITHDRAWAL = "CASH_WITHDRAWAL"


class DeliveryAddressTypeEnum(str, Enum):
    FLAT = "flat"
    HOUSE = "house"
    OFFICE = "office"


class GoodSchema(CheckboxBaseModel):
    code: str
    name: str
    barcode: Optional[str]
    excise_barcode: Optional[str]
    excise_barcodes: Optional[List[str]]
    header: Optional[str]
    footer: Optional[str]
    price: int
    tax: Optional[Union[List[int], List[str]]]
    uktzed: Optional[str]


class ReceiptGoodSchema(CheckboxBaseModel):
    good: Optional[GoodSchema]
    good_id: Optional[UUID]
    quantity: int
    is_return: Optional[bool]
    discounts: Optional[List[ReceiptDiscountsSchema]] = []
    total_sum: Optional[int]


class DeliverySchema(CheckboxBaseModel):
    email: Optional[EmailStr]
    emails: Optional[List[EmailStr]]
    phone: Optional[str] = Field(pattern=r"^380\d{9}$")


class DeliveryAddressSchema(CheckboxBaseModel):
    address_type: Optional[DeliveryAddressTypeEnum]
    street: Optional[str]
    entrance: Optional[str]
    floor: Optional[str]
    apartment_number: Optional[str]
    elevator: Optional[bool]
    intercom: Optional[bool]


class DeliveryDetailsSchema(CheckboxBaseModel):
    address: Optional[DeliveryAddressSchema]
    box_id: Optional[List[int]] = []
    client_name: Optional[str]
    client_phone_number: Optional[str]
    delivery_time: Optional[datetime]
    client_comment: Optional[str]
    thermal_dependence: Optional[bool]


class ReceiptDraftSchema(CheckboxBaseModel):
    cashier_name: Optional[str]
    departament: Optional[str]
    goods: List[ReceiptGoodSchema]
    additional_goods: Optional[List[ReceiptGoodSchema]]
    discounts: Optional[List[str]] = []
    payments: Optional[List[str]] = []
    bonuses: Optional[List[str]] = []
    header: Optional[str]
    footer: Optional[str]
    barcode: Optional[str]
    delivery: Optional[DeliverySchema]
    type: Optional[OrderReceiptDraftTypeEnum] = OrderReceiptDraftTypeEnum.SELL


class OrderSchema(CheckboxBaseModel):
    id: UUID
    order_id: Optional[str]
    status: OrderStatusEnum
    custom_status: Optional[OrderCustomStatusEnum]
    is_paid: bool
    payment_method: Optional[OrderPaymentMethodEnum]
    receipt_draft: ReceiptDraftSchema
    delivery_details: Optional[DeliveryDetailsSchema]
    created_at: datetime
    updated_at: Optional[datetime]
    not_fiscalize: Optional[bool]
    stock_code: Optional[str]
