from httpx import Response

from checkbox_sdk.methods.base import BaseMethod
from checkbox_sdk.storage.simple import SessionStorage


class KasaSpecialChannel(BaseMethod):
    uri = "update/check"

    def parse_response(self, storage: SessionStorage, response: Response):
        return response.json().get("channel")
