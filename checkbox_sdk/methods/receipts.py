import datetime
from typing import Any, Dict, Optional

from httpx import Response

from checkbox_sdk.methods.base import BaseMethod, HTTPMethod, PaginationMixin
from checkbox_sdk.storage.simple import SessionStorage


class GetReceipts(PaginationMixin, BaseMethod):
    uri = "receipts"


class GetReceipt(BaseMethod):
    def __init__(self, receipt_id: str):
        self.receipt_id = receipt_id

    @property
    def uri(self) -> str:
        return f"receipts/{self.receipt_id}"


class CreateReceipt(BaseMethod):
    method = HTTPMethod.POST
    uri = "receipts/sell"

    def __init__(
        self,
        receipt: Optional[Dict] = None,
        **payload,
    ):
        if receipt is not None and payload is not None:
            raise ValueError("'receipt' and '**payload' can not be passed together")
        self.receipt = receipt or payload

    @property
    def headers(self):
        headers = super(CreateReceipt, self).headers
        if "id" in self.receipt:
            headers.update({"x-request-id": self.receipt["id"]})
        return headers

    @property
    def payload(self):
        payload = super().payload
        payload.update(self.receipt)
        return payload

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        storage.shift = result["shift"]
        return result


class DeleteReceipt(BaseMethod):
    method = HTTPMethod.DELETE

    def __init__(self, receipt_id: str):
        self.receipt_id = receipt_id

    @property
    def uri(self) -> str:
        return f"receipts/{self.receipt_id}"


class CreateServiceReceipt(BaseMethod):
    method = HTTPMethod.POST
    uri = "receipts/service"

    def __init__(
        self,
        payment: Dict[str, Any],
        id: Optional[str] = None,
        fiscal_code: Optional[str] = None,
        fiscal_date: Optional[datetime.datetime] = None,
    ):
        self.payment = payment
        self.id = id
        self.fiscal_code = fiscal_code
        self.fiscal_date = fiscal_date

    @property
    def payload(self):
        payload = super().payload
        payload["payment"] = self.payment
        if self.id:
            payload["id"] = self.id
        if self.fiscal_code:
            payload["fiscal_code"] = self.fiscal_code
        if self.fiscal_date:
            payload["fiscal_date"] = self.fiscal_date
        return payload

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        storage.shift = result["shift"]
        return result


class GetReceiptVisualization(GetReceipt):
    def __init__(self, receipt_id: str, fmt: str = "text", **query):
        super().__init__(receipt_id=receipt_id)
        self.format = fmt
        self.params = query

    @property
    def query(self):
        query = super().query
        query.update(self.params)
        return query

    @property
    def uri(self) -> str:
        uri = super().uri
        return f"{uri}/{self.format}"

    def parse_response(self, storage: SessionStorage, response: Response):
        return response.content


class GetReceiptVisualizationText(GetReceiptVisualization):
    def __init__(self, receipt_id: str, width: int = 50):
        super().__init__(receipt_id=receipt_id, fmt="text", width=width)

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        return result.decode()


class GetReceiptVisualizationHtml(GetReceiptVisualization):
    def __init__(self, receipt_id: str):
        super().__init__(receipt_id=receipt_id, fmt="html")


class GetReceiptVisualizationPdf(GetReceiptVisualization):
    def __init__(self, receipt_id: str):
        super().__init__(receipt_id=receipt_id, fmt="pdf")


class GetReceiptVisualizationPng(GetReceiptVisualization):
    def __init__(self, receipt_id: str):
        super().__init__(receipt_id=receipt_id, fmt="png")


class GetReceiptVisualizationQrCode(GetReceiptVisualization):
    def __init__(self, receipt_id: str):
        super().__init__(receipt_id=receipt_id, fmt="qrcode")


class AddExternal(BaseMethod):
    method = HTTPMethod.POST
    uri = "receipts/add-external"

    def __init__(
        self,
        receipt: Optional[Dict] = None,
        **payload,
    ):
        if receipt is not None and payload is not None:
            raise ValueError("'receipt' and '**payload' can not be passed together")
        self.receipt = receipt or payload

    @property
    def payload(self):
        return self.receipt


class SendEmail(BaseMethod):
    method = HTTPMethod.POST

    def __init__(self, receipt_id: str, email: str):
        self.receipt_id = receipt_id
        self.email = email

    @property
    def uri(self) -> str:
        return f"receipts/{self.receipt_id}/email"

    @property
    def payload(self):
        return [self.email]


class SendSMS(BaseMethod):
    method = HTTPMethod.POST

    def __init__(self, receipt_id: str, phone: str):
        self.receipt_id = receipt_id
        self.phone = phone

    @property
    def uri(self) -> str:
        return f"receipts/{self.receipt_id}/sms"

    @property
    def payload(self):
        return {"phone": self.phone}


class CreateCashWithdrawalReceipt(BaseMethod):
    method = HTTPMethod.POST
    uri = "receipts/cash-withdrawal"

    def __init__(
        self,
        payment: Dict[str, Any],
        id: Optional[str] = None,
        fiscal_code: Optional[str] = None,
        fiscal_date: Optional[datetime.datetime] = None,
    ):
        self.payment = payment
        self.id = id
        self.fiscal_code = fiscal_code
        self.fiscal_date = fiscal_date

    @property
    def payload(self):
        payload = super().payload
        payload["payment"] = self.payment
        if self.id:
            payload["id"] = self.id
        if self.fiscal_code:
            payload["fiscal_code"] = self.fiscal_code
        if self.fiscal_date:
            payload["fiscal_date"] = self.fiscal_date
        return payload


class ReplaceFiscalCode(BaseMethod):
    method = HTTPMethod.PATCH

    def __init__(self, receipt_id: str, new_fiscal_code: str):
        self.receipt_id = receipt_id
        self.new_fiscal_code = new_fiscal_code

    @property
    def uri(self) -> str:
        return f"receipts/{self.receipt_id}/offline"

    @property
    def payload(self):
        return {"fiscal_code": self.new_fiscal_code}
