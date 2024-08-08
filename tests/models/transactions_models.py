from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from .base import CheckboxBaseModel


class TransactionsTypeEnum(str, Enum):
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


class TransactionsStatusEnum(str, Enum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    SIGNED = "SIGNED"
    DELIVERED = "DELIVERED"
    DONE = "DONE"
    ERROR = "ERROR"
    CANCELLED = "CANCELLED"


class TransactionsSchema(CheckboxBaseModel):
    id: UUID
    type: TransactionsTypeEnum
    serial: int
    status: TransactionsStatusEnum
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
    request_data: Optional[bytes]
    request_signature: Optional[bytes]
    response_id_signature: Optional[bytes]
    response_data_signature: Optional[bytes]
    response_data: Optional[bytes]
