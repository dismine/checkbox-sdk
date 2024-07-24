import datetime
import logging
import time
from typing import Any, Dict, List, Optional, Set

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

    def get_shifts(
        self,
        statuses: Optional[List[str]] = None,
        limit: int = 10,
        storage: Optional[SessionStorage] = None,
    ):
        get_shift = shifts.GetShifts(statuses=statuses, limit=limit)
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
    ):
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
    ):
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

    def get_offline_codes(self, count: int = 2000):
        logger.info("Ask offline codes (count=%d)", count)
        self(cash_register.AskOfflineCodes(count=count, sync=True))
        logger.info("Load offline codes...")
        codes = self(cash_register.GetOfflineCodes(count=count))
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
