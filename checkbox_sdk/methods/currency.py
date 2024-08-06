from typing import Dict, Optional, List

from checkbox_sdk.methods.base import BaseMethod, HTTPMethod

URI_PREFIX = "currency/"


class GetCurrencyRates(BaseMethod):
    uri = f"{URI_PREFIX}rate"

    def __init__(
        self,
        active: Optional[bool] = True,
    ):
        self.active = active

    @property
    def query(self):
        query = super().query

        if self.active is not None:
            query["active"] = self.active

        return query


class SetupCurrencyRates(BaseMethod):
    method = HTTPMethod.POST
    uri = f"{URI_PREFIX}rate/setup"

    def __init__(
        self,
        rates: Optional[List[Dict]] = None,
        **payload,
    ):
        if rates is not None and payload:
            raise ValueError("'rates' and '**payload' can not be passed together")
        self.rates = rates or payload

    @property
    def payload(self):
        payload = super().payload
        payload["rates"] = self.rates
        return payload


class GetCurrencyRate(BaseMethod):
    def __init__(self, currency_code: str):
        self.currency_code = currency_code

    @property
    def uri(self) -> str:
        return f"{URI_PREFIX}rate/{self.currency_code}"
