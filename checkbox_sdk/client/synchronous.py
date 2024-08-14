import logging
import time
from typing import Any, Optional, Set

from httpcore import NetworkError
from httpx import Client, HTTPError, Timeout

from checkbox_sdk.client.base import BaseCheckBoxClient
from checkbox_sdk.consts import DEFAULT_REQUESTS_RELAX
from checkbox_sdk.exceptions import CheckBoxNetworkError, CheckBoxError
from checkbox_sdk.methods import cash_register, cashier
from checkbox_sdk.methods.base import AbstractMethod, BaseMethod
from checkbox_sdk.storage.simple import SessionStorage
from .api import (
    CashRegisters,
    Cashier,
    Receipts,
    Shifts,
    Tax,
    Transactions,
    Organization,
    PrepaymentReceipts,
    Reports,
    ExtendedReports,
    Goods,
    Orders,
    Currency,
    Webhook,
    Invoices,
    NovaPost,
    Branches,
)

logger = logging.getLogger(__name__)


class CheckBoxClient(BaseCheckBoxClient):
    """
    A client for interacting with the Checkbox API, inheriting from
    :class:`checkbox_sdk.client.base.BaseCheckBoxClient`.

    This class provides methods for accessing various endpoints of the Checkbox API. It initializes
    the necessary components and manages connections to different API sections such as cashier,
    cash registers, shifts, receipts, transactions, tax, organizations, prepayment receipts, reports,
    goods, orders, currency, webhooks, invoices, NovaPost, and branches.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._session = Client(proxies=self.proxy, timeout=Timeout(timeout=self.timeout), verify=self.verify_ssl)
        self.cashier = Cashier(self)
        self.cash_registers = CashRegisters(self)
        self.shifts = Shifts(self)
        self.receipts = Receipts(self)
        self.transactions = Transactions(self)
        self.tax = Tax(self)
        self.organization = Organization(self)
        self.prepayment_receipts = PrepaymentReceipts(self)
        self.reports = Reports(self)
        self.extended_reports = ExtendedReports(self)
        self.goods = Goods(self)
        self.orders = Orders(self)
        self.currency = Currency(self)
        self.webhook = Webhook(self)
        self.invoices = Invoices(self)
        self.nova_post = NovaPost(self)
        self.branches = Branches(self)

    def __del__(self):
        # Attempt to close the session if it hasn't been already
        if self._session:
            self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        """
        Closes the HTTP connection managed by the client.

        This method closes the `httpx.Client` session, if it is currently open, and sets the session
        attribute to `None`. This is useful for releasing resources when the client is no longer needed.

        Notes:
            - After calling this method, the client should no longer be used for making requests.
            - It is a good practice to call this method when you are finished using the client to ensure
              that resources are properly released.
        """
        if self._session:
            self._session.close()
            self._session = None

    def emit(
        self,
        call: AbstractMethod,
        storage: Optional[SessionStorage] = None,
        request_timeout: Optional[float] = None,
    ):
        """
        Sends an HTTP request based on the provided method call and returns the parsed response.

        Args:
            call: An instance of :class:`checkbox_sdk.methods.base.AbstractMethod` representing the API method to be
                  called. This includes details such as HTTP method, URI, query parameters, files, headers, and payload.
            storage: Optional session storage to use for the request. If not provided, the default storage will be used.
            request_timeout: Optional timeout value for the request. If not provided, the default timeout will be used.

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
            response = self._session.request(
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

    def refresh_info(self, storage: Optional[SessionStorage] = None):
        """
        Refreshes and updates the session storage with information about the cashier, active shift, and cash register.

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

        self(cashier.GetMe(), storage=storage)
        self(cashier.GetActiveShift(), storage=storage)
        if storage.license_key:
            self(cash_register.GetCashRegisterInfo(), storage=storage)

    def wait_status(
        self,
        method: BaseMethod,
        expected_value: Set[Any],
        field: str = "status",
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[float] = None,
        storage: Optional[SessionStorage] = None,
    ):
        """
        Waits for a specified field in the result of a method call to change to one of the expected values.

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
        while (result := self(method, storage=storage))[field] not in expected_value:
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
