from typing import Optional
from uuid import UUID

from .base import CheckboxBaseModel


class OrganizationSchema(CheckboxBaseModel):
    id: UUID
    title: str
    edrpou: str
    tax_number: str


class ReceiptConfigShema(CheckboxBaseModel):
    text_global_header: Optional[str]
    text_global_footer: Optional[str]
    html_title: Optional[str]
    email_subject: Optional[str]
    html_global_header: Optional[str]
    html_global_footer: Optional[str]
    html_body_style: Optional[str]
    html_receipt_style: Optional[str]
    html_ruler_style: Optional[str]
    html_light_block_style: Optional[str]
    organization: OrganizationSchema


class SmsBillingSchema(CheckboxBaseModel):
    can_send_sms: bool
    billing_enabled: bool
    balance: Optional[int] = 0
