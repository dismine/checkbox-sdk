from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List
from uuid import UUID

from pydantic import Field

from .base import CheckboxBaseModel
from .shift_models import ShiftSchema, FiscalApiTypeEnum


class PingStatusEnum(str, Enum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    SIGNED = "SIGNED"
    DELIVERED = "DELIVERED"
    DONE = "DONE"
    ERROR = "ERROR"


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


class PingSchema(CheckboxBaseModel):
    status: PingStatusEnum
    error: Optional[str] = None


class OfflineTimeStatusSchema(CheckboxBaseModel):
    current: Optional[timedelta] = None
    total: Optional[timedelta] = None


class OfflineTimeSessionSchema(CheckboxBaseModel):
    start: Optional[datetime]
    end: Optional[datetime]
    duration: Optional[timedelta]


class OfflineTimeSchema(CheckboxBaseModel):
    status: OfflineTimeStatusSchema
    sessions: List[OfflineTimeSessionSchema]
