import datetime
from typing import Dict, Optional, List, Union
from uuid import UUID

from httpx import Response

from checkbox_sdk.methods.base import BaseMethod, HTTPMethod, PaginationMixin
from checkbox_sdk.storage.simple import SessionStorage

URI_PREFIX = "receipts/"


class GetReceipts(PaginationMixin, BaseMethod):
    uri = "receipts"

    def __init__(
        self,
        fiscal_code: Optional[str] = None,
        serial: Optional[int] = None,
        desc: Optional[bool] = False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        if fiscal_code is not None and serial is not None:
            raise ValueError("'fiscal_code' and 'serial' can not be passed together")

        self.fiscal_code = fiscal_code
        self.serial = serial
        self.desc = desc

    @property
    def query(self):
        query = super().query

        if self.fiscal_code is not None:
            query["fiscal_code"] = self.fiscal_code

        if self.serial is not None:
            query["serial"] = self.serial

        if self.desc is not None:
            query["desc"] = self.desc

        return query


class GetReceiptsSearch(PaginationMixin, BaseMethod):
    uri = f"{URI_PREFIX}search"

    def __init__(
        self,
        fiscal_code: Optional[str] = None,
        barcode: Optional[str] = None,
        shift_id: Optional[List[str]] = None,
        branch_id: Optional[List[str]] = None,
        cash_register_id: Optional[List[str]] = None,
        stock_code: Optional[str] = None,
        desc: Optional[bool] = False,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        self_receipts: Optional[bool] = True,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.fiscal_code = fiscal_code
        self.barcode = barcode
        self.shift_id = shift_id
        self.branch_id = branch_id
        self.cash_register_id = cash_register_id
        self.stock_code = stock_code
        self.from_date = from_date
        self.to_date = to_date
        self.desc = desc
        self.self_receipts = self_receipts

    @property
    def query(self):
        query = super().query

        if self.fiscal_code is not None:
            query["fiscal_code"] = self.fiscal_code

        if self.barcode is not None:
            query["barcode"] = self.barcode

        if self.shift_id is not None:
            query["shift_id"] = self.shift_id

        if self.branch_id is not None:
            query["branch_id"] = self.branch_id

        if self.cash_register_id is not None:
            query["cash_register_id"] = self.cash_register_id

        if self.stock_code is not None:
            query["stock_code"] = self.stock_code

        if isinstance(self.from_date, datetime.datetime):
            query["from_date"] = self.from_date.isoformat()
        elif self.from_date:
            query["from_date"] = self.from_date

        if isinstance(self.to_date, datetime.datetime):
            query["to_date"] = self.to_date.isoformat()
        elif self.to_date:
            query["to_date"] = self.to_date

        if self.desc is not None:
            query["desc"] = self.desc

        if self.self_receipts is not None:
            query["self_receipts"] = self.self_receipts

        return query


class GetReceipt(BaseMethod):
    def __init__(self, receipt_id: Union[str, UUID]):
        self.receipt_id = receipt_id

    @property
    def uri(self) -> str:
        receipt_id_str = str(self.receipt_id) if isinstance(self.receipt_id, UUID) else self.receipt_id
        return f"{URI_PREFIX}{receipt_id_str}"


class CreateBulkReceipts(BaseMethod):
    method = HTTPMethod.POST
    uri = f"{URI_PREFIX}bulk-sell"

    def __init__(
        self,
        receipts: Optional[List[Dict]] = None,
        **payload,
    ):
        if receipts is not None and payload:
            raise ValueError("'receipts' and '**payload' can not be passed together")
        self.receipts = receipts or payload

    @property
    def payload(self):
        payload = super().payload
        payload["receipts"] = self.receipts
        return payload


class CreateReceipt(BaseMethod):
    method = HTTPMethod.POST
    uri = f"{URI_PREFIX}sell"

    def __init__(
        self,
        receipt: Optional[Dict] = None,
        **payload,
    ):
        if receipt is not None and payload:
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


class CreateReceiptOffline(CreateReceipt):
    uri = f"{URI_PREFIX}sell-offline"


class AddExternal(CreateReceipt):
    uri = f"{URI_PREFIX}add-external"


class CreateServiceReceipt(CreateReceipt):
    uri = f"{URI_PREFIX}service"


class ServiceCurrency(CreateReceipt):
    uri = f"{URI_PREFIX}service-currency"


class CurrencyExchange(CreateReceipt):
    uri = f"{URI_PREFIX}currency-exchange"


class CreateCashWithdrawalReceipt(CreateReceipt):
    method = HTTPMethod.POST


class GetReceiptVisualization(GetReceipt):
    def __init__(self, receipt_id: Union[str, UUID], fmt: str = "text", **query):
        super().__init__(receipt_id=receipt_id)
        self.format = fmt
        self.params = query

    @property
    def query(self):
        query = super().query

        # Clean query before passing to URL. Remove None values
        cleaned_params = {k: v for k, v in self.params.items() if v is not None}
        query.update(cleaned_params)

        return query

    @property
    def uri(self) -> str:
        uri = super().uri
        return f"{uri}/{self.format}"

    def parse_response(self, storage: SessionStorage, response: Response):
        return response.content


class GetReceiptVisualizationHtml(GetReceiptVisualization):
    def __init__(
        self,
        receipt_id: Union[str, UUID],
        is_second_copy: Optional[bool] = False,
        simple: Optional[bool] = False,
        show_buttons: Optional[bool] = None,
        x_show_buttons: Optional[bool] = None,
    ):
        super().__init__(
            receipt_id=receipt_id, fmt="html", is_second_copy=is_second_copy, simple=simple, show_buttons=show_buttons
        )
        self.x_show_buttons = x_show_buttons

    @property
    def headers(self):
        headers = super(GetReceiptVisualizationHtml, self).headers
        if self.x_show_buttons is not None:
            headers.update({"X-Show-Buttons": self.x_show_buttons})
        return headers

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        return result.decode()


class GetReceiptVisualizationPdf(GetReceiptVisualization):
    def __init__(
        self,
        receipt_id: Union[str, UUID],
        is_second_copy: Optional[bool] = False,
        download: Optional[bool] = False,
    ):
        super().__init__(receipt_id=receipt_id, fmt="pdf", is_second_copy=is_second_copy, download=download)


class GetReceiptVisualizationText(GetReceiptVisualization):
    def __init__(
        self, receipt_id: Union[str, UUID], is_second_copy: Optional[bool] = False, width: Optional[int] = 42
    ):
        super().__init__(receipt_id=receipt_id, fmt="text", is_second_copy=is_second_copy, width=width)

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        return result.decode()


class GetReceiptVisualizationPng(GetReceiptVisualization):
    def __init__(
        self,
        receipt_id: Union[str, UUID],
        is_second_copy: Optional[bool] = False,
        width: Optional[int] = 30,
        paper_width: Optional[int] = 58,
        qrcode_scale: Optional[int] = 75,
    ):
        super().__init__(
            receipt_id=receipt_id,
            fmt="png",
            is_second_copy=is_second_copy,
            width=width,
            paper_width=paper_width,
            qrcode_scale=qrcode_scale,
        )


class GetReceiptVisualizationQrCode(GetReceiptVisualization):
    def __init__(self, receipt_id: Union[str, UUID]):
        super().__init__(receipt_id=receipt_id, fmt="qrcode")


class GetReceiptVisualizationXml(GetReceiptVisualization):
    def __init__(self, receipt_id: Union[str, UUID]):
        super().__init__(receipt_id=receipt_id, fmt="xml")

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        return result.decode()


class SendEmail(BaseMethod):
    method = HTTPMethod.POST

    def __init__(self, receipt_id: Union[str, UUID], email: str):
        self.receipt_id = receipt_id
        self.email = email

    @property
    def uri(self) -> str:
        receipt_id_str = str(self.receipt_id) if isinstance(self.receipt_id, UUID) else self.receipt_id
        return f"{URI_PREFIX}{receipt_id_str}/email"

    @property
    def payload(self):
        return [self.email]


class SendSMS(BaseMethod):
    method = HTTPMethod.POST

    def __init__(self, receipt_id: Union[str, UUID], phone: str):
        self.receipt_id = receipt_id
        self.phone = phone

    @property
    def uri(self) -> str:
        receipt_id_str = str(self.receipt_id) if isinstance(self.receipt_id, UUID) else self.receipt_id
        return f"{URI_PREFIX}{receipt_id_str}/sms"

    @property
    def payload(self):
        return {"phone": self.phone}
