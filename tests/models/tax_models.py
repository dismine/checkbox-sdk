from datetime import datetime
from typing import Optional
from uuid import UUID

from .base import CheckboxBaseModel


class TaxSchema(CheckboxBaseModel):
    id: UUID
    code: int
    label: str
    symbol: str
    rate: float
    extra_rate: Optional[float]
    included: bool
    is_gambling: Optional[bool]
    created_at: datetime
    updated_at: Optional[datetime]
    no_vat: Optional[bool]
    advanced_code: Optional[str]
    decimal_rate: Optional[float]
    decimal_extra_rate: Optional[float]
