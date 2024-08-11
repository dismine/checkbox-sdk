import logging
import time
from typing import Any, Optional, Set

from httpcore import NetworkError
from httpx import AsyncClient, HTTPError, Timeout

from checkbox_sdk.client.base import BaseCheckBoxClient
from checkbox_sdk.consts import DEFAULT_REQUESTS_RELAX
from checkbox_sdk.exceptions import CheckBoxNetworkError, CheckBoxError
from checkbox_sdk.methods import cash_register, cashier
from checkbox_sdk.methods.base import AbstractMethod, BaseMethod
from checkbox_sdk.storage.simple import SessionStorage
from .api import (
    AsyncCashRegisters,
    AsyncCashier,
    AsyncReceipts,
    AsyncShifts,
    AsyncTax,
    AsyncTransactions,
    AsyncOrganization,
    AsyncPrepaymentReceipts,
    AsyncReports,
    AsyncExtendedReports,
    AsyncGoods,
    AsyncOrders,
    AsyncCurrency,
    AsyncWebhook,
    AsyncInvoices,
    AsyncNovaPost,
    AsyncBranches,
)

logger = logging.getLogger(__name__)


class AsyncCheckBoxClient(BaseCheckBoxClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._session = AsyncClient(proxies=self.proxy, timeout=Timeout(timeout=self.timeout), verify=self.verify_ssl)
        self.cashier = AsyncCashier(self)
        self.cash_registers = AsyncCashRegisters(self)
        self.shifts = AsyncShifts(self)
        self.receipts = AsyncReceipts(self)
        self.transactions = AsyncTransactions(self)
        self.tax = AsyncTax(self)
        self.organization = AsyncOrganization(self)
        self.prepayment_receipts = AsyncPrepaymentReceipts(self)
        self.reports = AsyncReports(self)
        self.extended_reports = AsyncExtendedReports(self)
        self.goods = AsyncGoods(self)
        self.orders = AsyncOrders(self)
        self.currency = AsyncCurrency(self)
        self.webhook = AsyncWebhook(self)
        self.invoices = AsyncInvoices(self)
        self.nova_post = AsyncNovaPost(self)
        self.branches = AsyncBranches(self)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def close(self):
        if self._session:
            await self._session.aclose()
            self._session = None

    async def emit(
        self,
        call: AbstractMethod,
        storage: Optional[SessionStorage] = None,
        request_timeout: Optional[float] = None,
    ):
        storage = storage or self.storage

        if not call.internal:
            url = f"{self.base_url}/api/v{self.api_version}/{call.uri}"
        else:
            url = f"{self.base_url}/{call.uri}"

        try:
            response = await self._session.request(
                method=call.method.name,
                url=url,
                timeout=request_timeout or self.timeout,
                params=call.query,
                files=call.files,
                headers={**storage.headers, **call.headers, **self.client_headers},
                json=call.payload,
            )
        except HTTPError as e:
            raise CheckBoxError(e) from e
        except NetworkError as e:
            raise CheckBoxNetworkError(e) from e

        logger.debug("Request response: %s", response)
        self._check_response(response=response)
        return call.parse_response(storage=storage, response=response)

    async def refresh_info(self, storage: Optional[SessionStorage] = None):
        storage = storage or self.storage

        await self(cashier.GetMe(), storage=storage)
        await self(cashier.GetActiveShift(), storage=storage)
        if storage.license_key:
            await self(cash_register.GetCashRegisterInfo(), storage=storage)

    async def wait_status(
        self,
        method: BaseMethod,
        expected_value: Set[Any],
        field: str = "status",
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[float] = None,
        storage: Optional[SessionStorage] = None,
    ):
        logger.info("Wait until %r will be changed to one of %s", field, expected_value)
        initial = time.monotonic()
        while (result := await self(method, storage=storage))[field] not in expected_value:
            if timeout is not None and time.monotonic() > initial + timeout:
                logger.error("Status did not changed in required time")
                break
            time.sleep(relax)

        if result[field] not in expected_value:
            raise ValueError(
                f"Object did not change field {field!r} "
                f"to one of expected values {expected_value} (actually {result[field]!r}) "
                f"in {time.monotonic() - initial:.3f} seconds"
            )

        logger.info(
            "Status changed in %.3f seconds to %r",
            time.monotonic() - initial,
            result[field],
        )
        return result
