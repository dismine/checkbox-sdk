from httpx import Response

from checkbox_sdk.methods.base import BaseMethod
from checkbox_sdk.storage.simple import SessionStorage


class GetOrganizationReceiptConfig(BaseMethod):
    uri = "organization/receipt-config"


class GetReceiptConfigLogo(BaseMethod):
    uri = "organization/logo.png"

    def parse_response(self, storage: SessionStorage, response: Response):
        return response.content


class GetReceiptConfigTextLogo(BaseMethod):
    uri = "organization/text_logo.png"

    def parse_response(self, storage: SessionStorage, response: Response):
        return response.content
