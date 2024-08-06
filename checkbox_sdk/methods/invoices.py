import datetime
from typing import Optional, Union, List, Dict
from uuid import UUID

from checkbox_sdk.methods.base import BaseMethod, HTTPMethod, PaginationMixin

URI_PREFIX = "invoices/"


class GetTerminals(BaseMethod):
    uri = "terminals"


class GetInvoices(PaginationMixin, BaseMethod):
    uri = "invoices"

    def __init__(
        self,
        status: Optional[str] = None,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.status = status
        self.from_date = from_date
        self.to_date = to_date

    @property
    def query(self):
        query = super().query

        if self.status is not None:
            query["status"] = self.status

        if isinstance(self.from_date, datetime.datetime):
            query["from_date"] = self.from_date.isoformat()
        elif self.from_date:
            query["from_date"] = self.from_date

        if isinstance(self.to_date, datetime.datetime):
            query["to_date"] = self.to_date.isoformat()
        elif self.to_date:
            query["to_date"] = self.to_date

        return query


class CreateInvoice(BaseMethod):
    method = HTTPMethod.POST
    uri = "invoices"

    def __init__(
        self,
        invoice: Optional[List[Dict]] = None,
        **payload,
    ):
        if invoice is not None and payload:
            raise ValueError("'invoice' and '**payload' can not be passed together")
        self.invoice = invoice or payload

    @property
    def payload(self):
        payload = super().payload
        payload.update(self.invoice)
        return payload


class CreateAndFiscalizeInvoice(BaseMethod):
    method = HTTPMethod.POST
    uri = f"{URI_PREFIX}fiscalize"

    def __init__(
        self,
        invoice: Optional[List[Dict]] = None,
        **payload,
    ):
        if invoice is not None and payload:
            raise ValueError("'invoice' and '**payload' can not be passed together")
        self.invoice = invoice or payload

    @property
    def payload(self):
        payload = super().payload
        payload.update(self.invoice)
        return payload


class GetInvoiceById(BaseMethod):
    def __init__(self, invoice_id: Union[str, UUID]):
        self.invoice_id = invoice_id

    @property
    def uri(self) -> str:
        invoice_id_str = str(self.invoice_id) if isinstance(self.invoice_id, UUID) else self.invoice_id
        return f"{URI_PREFIX}{invoice_id_str}"


class CancelInvoiceById(BaseMethod):
    method = HTTPMethod.DELETE

    def __init__(self, invoice_id: Union[str, UUID]):
        self.invoice_id = invoice_id

    @property
    def uri(self) -> str:
        invoice_id_str = str(self.invoice_id) if isinstance(self.invoice_id, UUID) else self.invoice_id
        return f"{URI_PREFIX}{invoice_id_str}"


class RemoveInvoiceById(BaseMethod):
    method = HTTPMethod.DELETE

    def __init__(self, invoice_id: Union[str, UUID]):
        self.invoice_id = invoice_id

    @property
    def uri(self) -> str:
        invoice_id_str = str(self.invoice_id) if isinstance(self.invoice_id, UUID) else self.invoice_id
        return f"{URI_PREFIX}{invoice_id_str}/remove"
