from httpx import Response

from checkbox_sdk.methods.base import BaseMethod
from checkbox_sdk.storage.simple import SessionStorage

URI_PREFIX = "organization/"


class GetOrganizationReceiptConfig(BaseMethod):
    uri = f"{URI_PREFIX}receipt-config"


class GetOrganizationLogo(BaseMethod):
    uri = f"{URI_PREFIX}logo.png"

    def parse_response(self, storage: SessionStorage, response: Response):
        return response.content


class GetOrganizationTextLogo(BaseMethod):
    uri = f"{URI_PREFIX}text_logo.png"

    def parse_response(self, storage: SessionStorage, response: Response):
        return response.content


class GetOrganizationSmsBilling(BaseMethod):
    uri = f"{URI_PREFIX}sms-billing"
