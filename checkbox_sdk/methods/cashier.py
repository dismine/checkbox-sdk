from httpx import Response

from checkbox_sdk.methods.base import BaseMethod, HTTPMethod
from checkbox_sdk.storage.simple import SessionStorage

URI_PREFIX = "cashier/"


class _SignInMixin:
    method = HTTPMethod.POST

    def parse_response(self, storage: SessionStorage, response: Response):
        result = response.json()
        storage.token = result["access_token"]
        return result


class SignIn(_SignInMixin, BaseMethod):
    uri = f"{URI_PREFIX}signin"

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

    @property
    def payload(self):
        return {"login": self.login, "password": self.password}


class SignInPinCode(_SignInMixin, BaseMethod):
    uri = f"{SignIn.uri}PinCode"

    def __init__(self, pin_code: str):
        self.pin_code = pin_code

    @property
    def payload(self):
        return {"pin_code": self.pin_code}


class SignOut(BaseMethod):
    method = HTTPMethod.POST
    uri = f"{URI_PREFIX}signout"

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)

        storage.shift = None
        storage.cashier = None
        storage.token = None

        return result


class GetMe(BaseMethod):
    method = HTTPMethod.GET
    uri = f"{URI_PREFIX}me"

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        storage.cashier = result
        return result


class GetActiveShift(BaseMethod):
    uri = f"{URI_PREFIX}shift"

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        storage.shift = result
        return result


class GetSignatureKey(BaseMethod):
    uri = f"{URI_PREFIX}check-signature"

    def parse_response(self, storage: SessionStorage, response: Response):
        result = super().parse_response(storage=storage, response=response)
        return result.get("shift_open_possibility", True)


class GetAllTaxesByCashier(BaseMethod):
    uri = f"{URI_PREFIX}tax"
