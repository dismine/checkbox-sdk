from datetime import datetime
from typing import Optional, List
from uuid import UUID

from ..models.base import CheckboxBaseModel


# pylint: disable=duplicate-code
class GoodTaxSchema(CheckboxBaseModel):
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


class GoodChildSchema(CheckboxBaseModel):
    id: UUID
    code: str
    name: str
    price: int
    type: str
    barcode: Optional[str]
    group_id: Optional[UUID]
    uktzed: Optional[str]
    taxes: List[GoodTaxSchema]
    count: Optional[int]
    image_url: Optional[str]
    is_weight: Optional[bool]
    created_at: datetime
    updated_at: Optional[datetime]


class GoodSchema(CheckboxBaseModel):
    id: UUID
    code: str
    name: str
    price: int
    type: str
    barcode: Optional[str]
    group_id: Optional[UUID]
    uktzed: Optional[str]
    taxes: List[GoodTaxSchema]
    count: Optional[int]
    image_url: Optional[str]
    is_weight: Optional[bool]
    created_at: datetime
    updated_at: Optional[datetime]
    children: Optional[List[GoodChildSchema]] = []
    related_barcodes: Optional[str]


class GoodGroupChildSchema(CheckboxBaseModel):
    id: UUID
    name: str
    description: Optional[str]
    parent_id: Optional[UUID]
    image_url: Optional[str]


class GoodGroupSchema(CheckboxBaseModel):
    id: UUID
    name: str
    description: Optional[str]
    parent_id: Optional[UUID]
    image_url: Optional[str]
    children: Optional[List[GoodGroupChildSchema]] = []
