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
    """
    Asynchronous client for interacting with the Checkbox API.

    This client provides methods for various operations such as managing cashiers, cash registers, shifts,
    receipts, transactions, taxes, and more, all in an asynchronous manner. It supports context management,
    making it easier to handle resources automatically.
    """

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
        """
        Closes the asynchronous HTTPX session.

        This method closes the `httpx.Client` session, if it is currently open, and sets the session
        attribute to `None`. This is useful for releasing resources when the client is no longer needed.

        Notes:
            - After calling this method, the client should no longer be used for making requests.
            - It is a good practice to call this method when you are finished using the client to ensure
              that resources are properly released.
        """
        if self._session:
            await self._session.aclose()
            self._session = None

    async def emit(
        self,
        call: AbstractMethod,
        storage: Optional[SessionStorage] = None,
        request_timeout: Optional[float] = None,
    ):
        """
        Sends an asynchronous request to the Checkbox API using the specified method.

        Args:
            call: The method to be called, encapsulating the request details.
            storage: Optional session storage to use for the request. If not provided, the default storage will be used.
            request_timeout: Optional timeout for the request. If not provided, the client's default timeout will be used.

        Returns:
            The parsed response from the API call, as determined by the `call.parse_response` method.

        Raises:
            CheckBoxError: If an HTTP error occurs during the request.
            CheckBoxNetworkError: If a network error occurs during the request.

        Notes:
            - The `url` for the request is constructed based on whether the call is internal or external.
            - The response is checked and parsed according to the method call's specifications.
        """
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
        """
        Asynchronously refreshes and updates the session storage with information about the cashier, active shift, and
        cash register.

        Args:
            storage: Optional session storage to use for the operation. If not provided, the default storage will be
                     used.

        Returns:
            None

        Notes:
            - This method retrieves and updates information about the current cashier, and the active shift.
            - If a `license_key` is present in the storage, information about the cash register is also updated.
            - The method makes API calls to fetch and update this information based on the provided storage.
        """
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
        """
        Asynchronously waits for a specified field in the result of a method call to change to one of the expected
        values.

        Args:
            method: The method to call repeatedly to check the status.
            expected_value: A set of expected values for the specified field.
            field: The field in the result to monitor for changes. Defaults to "status".
            relax: The amount of time (in seconds) to wait between checks. Defaults to `DEFAULT_REQUESTS_RELAX`.
            timeout: The maximum amount of time (in seconds) to wait for the status change. If `None`, waits
                     indefinitely.
            storage: Optional session storage to use for the method calls. If not provided, the default storage will be
                     used.

        Returns:
            A dictionary containing the result of the last method call where the field matched one of the expected
            values.

        Raises:
            ValueError: If the status field does not change to one of the expected values within the timeout period.

        Notes:
            - This method repeatedly calls the specified method and checks the value of the specified field.
            - If the field's value does not match any of the expected values within the timeout period, a `ValueError`
              is raised.
            - The method logs the status of the wait operation and the time taken.
        """
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
