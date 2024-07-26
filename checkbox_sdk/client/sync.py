import datetime
import logging
import time
from typing import Any, Dict, List, Optional, Set, Generator, Union

from httpcore import NetworkError
from httpx import Client, HTTPError, Timeout

from checkbox_sdk.client.base import BaseCheckBoxClient
from checkbox_sdk.consts import DEFAULT_REQUESTS_RELAX
from checkbox_sdk.exceptions import CheckBoxError, CheckBoxNetworkError, StatusException
from checkbox_sdk.methods import cash_register, cashier, receipts, shifts, transactions
from checkbox_sdk.methods.base import AbstractMethod, BaseMethod
from checkbox_sdk.storage.simple import SessionStorage

logger = logging.getLogger(__name__)


class CheckBoxClient(BaseCheckBoxClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._session = Client(proxies=self.proxy, timeout=Timeout(timeout=self.timeout), verify=self.verify_ssl)

    def emit(
        self,
        call: AbstractMethod,
        storage: Optional[SessionStorage] = None,
        request_timeout: Optional[float] = None,
    ):
        storage = storage or self.storage

        url = f"{self.base_url}/api/v{self.api_version}/{call.uri}"
        try:
            response = self._session.request(
                method=call.method.name,
                url=url,
                timeout=request_timeout or self.timeout,
                params=call.query,
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
        storage = storage or self.storage

        self(cashier.GetMe(), storage=storage)
        self(cashier.GetActiveShift(), storage=storage)
        if storage.license_key:
            self(cash_register.GetCashRegisterInfo(), storage=storage)

    def authenticate(
        self,
        login: str,
        password: str,
        license_key: Optional[str] = None,
        storage: Optional[SessionStorage] = None,
    ) -> None:
        """
        Authenticate using cashier's login credentials.

        This method sets the cash license key, signs in using the provided cashier's login and password,
        and refreshes the user (cashier) information.

        Args:
            login (str): The user's login.
            password (str): The user's password.
            license_key (Optional[str]): The cash register license key to set.
            storage (Optional[SessionStorage]): The session storage to use.

        Returns:
            None
        """
        self._set_license_key(storage=storage, license_key=license_key)
        self(cashier.SignIn(login=login, password=password), storage=storage)
        self.refresh_info(storage=storage)

    def authenticate_pin_code(
        self,
        pin_code: str,
        license_key: Optional[str] = None,
        storage: Optional[SessionStorage] = None,
    ) -> None:
        """
        Authenticate using a PIN code (recommended method).

        This method sets the cash license key, signs in using the provided cashier's PIN code,
        and refreshes the user (cashier) information.

        Args:
            pin_code (str): The PIN code for cashier authentication.
            license_key (Optional[str]): The cash register license key to set.
            storage (Optional[SessionStorage]): The session storage to use.

        Returns:
            None
        """
        self._set_license_key(storage=storage, license_key=license_key)
        self(cashier.SignInPinCode(pin_code=pin_code), storage=storage)
        self.refresh_info(storage=storage)

    def authenticate_token(
        self,
        token: str,
        license_key: Optional[str] = None,
        storage: Optional[SessionStorage] = None,
    ) -> None:
        """
        Authenticate using a token.

        This method sets the cash license key, assigns the token to the storage,
        and refreshes the user (cashier) information. Use this method if you already have an access token.

        Args:
            token (str): The token for authentication.
            license_key (Optional[str]): The cash register license key to set.
            storage (Optional[SessionStorage]): The session storage to use.

        Returns:
            None
        """
        storage = storage or self.storage
        self._set_license_key(storage=storage, license_key=license_key)
        storage.token = token
        self.refresh_info(storage=storage)

    def sign_out(self, storage: Optional[SessionStorage] = None) -> None:
        """
        Sign out cashier.

        This method signs out the current user (cashier) by calling the SignOut endpoint.

        Args:
            storage (Optional[SessionStorage]): The session storage to use.

        Returns:
            None
        """
        self(cashier.SignOut(), storage=storage)

    def get_cash_registers(
        self, storage: Optional[SessionStorage] = None, limit: int = 10, offset: int = 0
    ) -> Generator:
        """
        Generator to retrieve a list of available cash registers.

        This function fetches cash registers using pagination and yields the results.

        Args:
            storage (Optional[SessionStorage]): The session storage to use.
            limit (int): The maximum number of cash registers to retrieve.
            offset (int): The offset for pagination.

        Returns:
            Generator: Yields the information of available cash registers.
        """
        get_cash_registers = cash_register.GetCashRegisters(limit=limit, offset=offset)
        while (shifts_result := self(get_cash_registers, storage=storage))["results"]:
            get_cash_registers.resolve_pagination(shifts_result).shift_next_page()
            yield from shifts_result["results"]

    def get_cash_register(
        self,
        cash_register_id: Optional[str] = None,
        storage: Optional[SessionStorage] = None,
    ) -> Dict:
        """
        Retrieves information about a cash register using the Checkbox SDK client based on the UUID.

        This function retrieves information about a specific cash register identified by its UUID. If the UUID is not
        provided, it attempts to use the cash register UUID from the session storage. If no UUID is found, it
        raises a CheckBoxError.

        Args:
            cash_register_id (Optional[str]): The UUID of the cash register to retrieve information for.
            storage (Optional[SessionStorage]): An optional session storage to use.

        Returns:
            Dict: Information about the cash register as a dictionary.
        """

        storage = storage or self.storage

        if not cash_register_id:
            if not storage.license_key:
                raise CheckBoxError("Field cash_register_id is required")

            cash_register_id = storage.cash_register.get("id")  # type: ignore[attr-defined]
            if not cash_register_id:
                raise CheckBoxError("Cash register ID not found in session storage")
        elif not isinstance(cash_register_id, str):
            raise CheckBoxError("Cash register ID must be a string")

        return self(cash_register.GetCashRegister(cash_register_id=cash_register_id), storage=storage)

    def ping_tax_service(
        self,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Pings the tax service using the Checkbox SDK client and returns the response as a dictionary.

        This function sends a ping request to the tax service using the Checkbox SDK client and returns the response
        as a dictionary.

        Args:
            storage (Optional[SessionStorage]): An optional session storage to use.

        Returns:
            Dict: The response from the tax service as a dictionary.
        """
        return self(cash_register.PingTaxService(), storage=storage)

    def go_online(
        self,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, str]:
        """
        Puts the cash register online using the Checkbox SDK.

        This function puts the client online to enable online operations using the Checkbox SDK.

        Args:
            storage (Optional[SessionStorage]): An optional session storage to use.

        Returns:
            Dict[str, str]: The response from putting the client online as a dictionary.
        """

        return self(cash_register.GoOnline(), storage=storage)

    def go_offline(
        self,
        go_offline_date: Optional[Union[datetime.datetime, str]] = None,
        fiscal_code: Optional[str] = None,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, str]:
        """
        Puts the cash register offline using the Checkbox SDK.

        This function puts the cash register offline to disable online operations using the Checkbox SDK.

        Args:
            go_offline_date (Optional[Union[datetime.datetime, str]]): The date and time to go offline after the last
            successful transaction.
            fiscal_code (Optional[str]): The fiscal code that was not used before.
            storage (Optional[SessionStorage]): An optional session storage to use.

        Returns:
            Dict[str, str]: The response from putting the cash register offline as a dictionary.
        """

        return self(cash_register.GoOffline(go_offline_date=go_offline_date, fiscal_code=fiscal_code), storage=storage)

    def get_shifts(
        self,
        statuses: Optional[List[str]] = None,
        desc: Optional[bool] = False,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        storage: Optional[SessionStorage] = None,
    ) -> Generator:
        """
        Retrieves shifts information using the Checkbox SDK.

        This function retrieves shifts information based on specified filters like statuses, date range, limit, and
        offset, yielding results in batches.

        Args:
            statuses (Optional[List[str]]): A list of statuses to filter shifts.
            desc (Optional[bool]): A flag to indicate descending order (default is False).
            from_date (Optional[Union[datetime.datetime, str]]): The start date for filtering shifts.
            to_date (Optional[Union[datetime.datetime, str]]): The end date for filtering shifts.
            limit (Optional[int]): The maximum number of shifts to retrieve (default is 10).
            offset (Optional[int]): The offset for pagination (default is 0).
            storage (Optional[SessionStorage]): An optional session storage to use.

        Returns:
            Generator: A generator yielding shifts information in batches.
        """

        get_shift = shifts.GetShifts(
            statuses=statuses, desc=desc, from_date=from_date, to_date=to_date, limit=limit, offset=offset
        )
        while (shifts_result := self(get_shift, storage=storage))["results"]:
            get_shift.resolve_pagination(shifts_result).shift_next_page()
            yield from shifts_result["results"]

    def wait_status(
        self,
        method: BaseMethod,
        expected_value: Set[Any],
        field: str = "status",
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
    ):
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

    def create_shift(
        self,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        **kwargs: Any,
    ) -> Dict:
        """
        Creates a shift using the Checkbox SDK and handles shift status checks and exceptions.

        This function creates a shift, refreshes information, and ensures the shift is successfully opened or handles
        exceptions if the shift cannot be opened.

        Args:
            relax (float): The relaxation time for requests (default is DEFAULT_REQUESTS_RELAX).
            timeout (Optional[int]): The timeout duration for the request.
            storage (Optional[SessionStorage]): An optional session storage to use.
            **kwargs (Any): Additional keyword arguments for creating the shift.

        Returns:
            Dict: Information about the created or updated shift.
        """
        storage = storage or self.storage
        self.refresh_info(storage=storage)
        if storage.shift is not None:
            logger.info(
                "Shift is already opened %s in status %s",
                storage.shift["id"],
                storage.shift["status"],
            )
            shift = storage.shift
        else:
            shift = self(shifts.CreateShift(**kwargs), storage=storage, request_timeout=timeout)
            logger.info("Created shift %s", shift["id"])

        if shift["status"] == "OPENED":
            return shift

        shift = self.wait_status(
            shifts.GetShift(shift_id=shift["id"]),
            storage=storage,
            relax=relax,
            field="status",
            expected_value={"OPENED", "CLOSED"},
            timeout=timeout,
        )
        if shift["status"] == "CLOSED":
            initial_transaction = shift["initial_transaction"]
            raise StatusException(
                "Shift can not be opened in due to transaction status moved to "
                f"{initial_transaction['status']!r}: {initial_transaction['response_status']!r} "
                f"{initial_transaction['response_error_message']!r}"
            )
        return shift

    def close_shift(
        self,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Union[Dict, None]:
        """
        Closes a shift using the Checkbox SDK and handles shift status checks and exceptions.

        This function closes the current shift, refreshes information, and ensures the shift is successfully closed or
        handles exceptions if the shift cannot be closed.

        Args:
            relax (float): The relaxation time for requests (default is DEFAULT_REQUESTS_RELAX).
            timeout (Optional[int]): The timeout duration for the request.
            storage (Optional[SessionStorage]): An optional session storage to use.
            **payload: Additional keyword arguments for closing the shift.

        Returns:
            Union[Dict, None]: The Z report of the closed shift or None if the shift is already closed.
        """

        storage = storage or self.storage
        self.refresh_info(storage=storage)
        if storage.shift is None:
            logger.info("Shift is already closed")
            return storage.shift

        shift = self(shifts.CloseShift(**payload), storage=storage)
        logger.info("Trying to close shift %s", shift["id"])

        shift = self.wait_status(
            shifts.GetShift(shift_id=shift["id"]),
            storage=storage,
            relax=relax,
            field="status",
            expected_value={"OPENED", "CLOSED"},
            timeout=timeout,
        )
        if shift["status"] == "OPENED":
            closing_transaction = shift["closing_transaction"]
            raise StatusException(
                "Shift can not be closed in due to transaction status moved to "
                f"{closing_transaction['status']!r}: {closing_transaction['response_status']!r} "
                f"{closing_transaction['response_error_message']!r}"
            )

        return shift["z_report"]

    def close_shift_online(
        self,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        transaction_timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ):
        storage = storage or self.storage
        self.refresh_info(storage=storage)
        if storage.shift is None:
            logger.info("Shift is already closed")
            return storage.shift

        shift = self(shifts.CloseShift(**payload), storage=storage, request_timeout=timeout)
        logger.info("Trying to close shift %s", shift["id"])

        shift = self.wait_status(
            shifts.GetShift(shift_id=shift["id"]),
            storage=storage,
            relax=relax,
            field="status",
            expected_value={"OPENED", "CLOSED"},
            timeout=timeout,
        )
        if shift["status"] == "OPENED":
            closing_transaction = shift["closing_transaction"]
            raise StatusException(
                "Shift can not be closed in due to transaction status moved to "
                f"{closing_transaction['status']!r}: {closing_transaction['response_status']!r} "
                f"{closing_transaction['response_error_message']!r}"
            )

        # zreport transaction
        return self.wait_transaction(
            transaction_id=shift["closing_transaction"]["id"],
            timeout=transaction_timeout,
        )

    def create_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        wait: bool = True,
        **payload,
    ):
        receipt = self(
            receipts.CreateReceipt(receipt=receipt, **payload),
            storage=storage,
            # request_timeout=timeout,
        )
        logger.info("Trying create receipt %s", receipt["id"])  # type: ignore[index]
        if not wait:
            return receipt

        return self._check_status(receipt, storage, relax, timeout)  # type: ignore[index,arg-type]

    def create_external_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ):
        receipt = self(receipts.AddExternal(receipt, **payload), storage=storage)
        logger.info("Trying to create external receipt %s", receipt["id"])  # type: ignore[index]

        return self._check_status(receipt, storage, relax, timeout)  # type: ignore[index,arg-type]

    def create_service_receipt(
        self,
        payment: Dict[str, Any],
        id: Optional[str] = None,
        fiscal_code: Optional[str] = None,
        fiscal_date: Optional[datetime.datetime] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
    ):
        receipt = self(
            receipts.CreateServiceReceipt(payment=payment, id=id, fiscal_code=fiscal_code, fiscal_date=fiscal_date),
            storage=storage,
            # request_timeout=timeout,
        )
        logger.info("Trying to create receipt %s", receipt["id"])

        return self._check_status(receipt, storage, relax, timeout)

    def create_cash_withdrawal_receipt(
        self,
        payment: Dict[str, Any],
        id: Optional[str] = None,
        fiscal_code: Optional[str] = None,
        fiscal_date: Optional[datetime.datetime] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
    ):
        receipt = self(
            receipts.CreateCashWithdrawalReceipt(
                payment=payment, id=id, fiscal_code=fiscal_code, fiscal_date=fiscal_date
            ),
            storage=storage,
            # request_timeout=timeout,
        )
        logger.info("Trying to create receipt %s", receipt["id"])

        return self._check_status(receipt, storage, relax, timeout)

    def _check_status(
        self,
        receipt: Dict[str, Any],
        storage: Optional[SessionStorage] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
    ):
        shift = self.wait_status(
            receipts.GetReceipt(receipt_id=receipt["id"]),
            storage=storage,
            relax=relax,
            field="status",
            expected_value={"DONE", "ERROR"},
            timeout=timeout,
        )
        if shift["status"] == "ERROR":
            initial_transaction = shift["transaction"]
            raise StatusException(
                f"Receipt can not be created in due to transaction status moved to {initial_transaction['status']!r}: "
                f"{initial_transaction['response_status']!r} {initial_transaction['response_error_message']!r}"
            )
        return shift

    def get_offline_codes(self, ask_count: int = 2000, threshold: int = 500) -> List[str]:
        """
        Retrieves offline codes for fiscal transactions using the Checkbox SDK.

        This function requests and loads offline codes for fiscal transactions, returning a list of fiscal codes.

        Args:
            ask_count (int): The number of offline codes to retrieve (default is 2000).
            threshold (int): The number of minimal number of offline codes after which new set will be asked from the
            tax server

        Returns:
            List[str]: A list of fiscal codes for offline transactions.
        """
        logger.info("Checking available number of offline codes...")
        response = self(cash_register.GetOfflineCodesCount())
        if not response.get("enough_offline_codes", False):
            return []

        if response.get("available", 0) <= threshold:
            logger.info("Ask for more offline codes (count=%d)", ask_count)
            self(cash_register.AskOfflineCodes(count=ask_count, sync=True))

        logger.info("Load offline codes...")
        codes = self(cash_register.GetOfflineCodes(count=ask_count))
        return [item["fiscal_code"] for item in codes]

    def wait_transaction(
        self,
        transaction_id: str,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
    ):
        transaction = self.wait_status(
            transactions.GetTransaction(transaction_id=transaction_id),
            relax=relax,
            timeout=timeout,
            storage=storage,
            field="status",
            expected_value={"DONE", "ERROR"},
        )
        if transaction["status"] == "ERROR":
            raise StatusException(
                f"Transaction status moved to {transaction['status']!r} "
                f"and tax status {transaction['response_status']!r} "
                f"with message {transaction['response_error_message']!r}"
            )
        return transaction
