import datetime
import logging
from typing import Any, Dict, List, Optional, Generator, Union, AsyncGenerator

from checkbox_sdk.consts import DEFAULT_REQUESTS_RELAX
from checkbox_sdk.exceptions import StatusException
from checkbox_sdk.methods import receipts
from checkbox_sdk.storage.simple import SessionStorage

logger = logging.getLogger(__name__)


class Receipts:
    def __init__(self, client):
        self.client = client

    def create_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates a receipt and optionally waits for its status.

        This function creates a receipt with the provided payload and waits for its status if specified.

        Args:
            receipt (Optional[Dict[str, Any]): A dictionary containing receipt information.
            relax (float): A float indicating the relaxation factor.
            timeout (Optional[int]): An optional timeout value.
            storage (Optional[SessionStorage]): The session storage to use.
            wait (bool): Flag to indicate whether to wait for the receipt status.
            **payload: Additional keyword arguments for creating the receipt. Cannot be used together with @receipt.

        Returns:
            Dict[str, Any]: The result of checking the status of the created receipt if wait is True, otherwise the created
            receipt itself.
        """
        response = self.client(
            receipts.CreateReceipt(receipt=receipt, **payload),
            storage=storage,
            # request_timeout=timeout,
        )
        logger.info("Trying create receipt %s", response["id"])  # type: ignore[index]
        if not wait:
            return response

        return self._check_status(response, storage, relax, timeout)  # type: ignore[index,arg-type]

    def create_external_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ):
        receipt = self.client(receipts.AddExternal(receipt, **payload), storage=storage)
        logger.info("Trying to create external receipt %s", receipt["id"])  # type: ignore[index]

        return self._check_status(receipt, storage, relax, timeout)  # type: ignore[index,arg-type]

    def get_receipts(
        self,
        fiscal_code: Optional[str] = None,
        serial: Optional[int] = None,
        desc: Optional[bool] = False,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        storage: Optional[SessionStorage] = None,
    ) -> Generator:
        """
        Generator to retrieve a list of receipts.

        This function fetches receipts based on filters and yields the results.

        Args:
            fiscal_code (Optional[str]): Filter for receipts with a specific fiscal code.
            serial (Optional[int]): Filter for receipts with a specific serial number.
            desc (Optional[bool]): Flag to sort results in descending order.
            limit (Optional[int]): The maximum number of receipts to retrieve.
            offset (Optional[int]): The offset for pagination.
            storage (Optional[SessionStorage]): The session storage to use.

        Returns:
            Generator: Yields the information of retrieved receipts.
        """
        get_receipts = receipts.GetReceipts(
            fiscal_code=fiscal_code, serial=serial, desc=desc, limit=limit, offset=offset
        )
        while (receipts_result := self.client(get_receipts, storage=storage))["results"]:
            get_receipts.resolve_pagination(receipts_result).shift_next_page()
            yield from receipts_result["results"]

    def get_receipts_search(
        self,
        fiscal_code: Optional[str] = None,
        barcode: Optional[str] = None,
        shift_id: Optional[List[str]] = None,
        branch_id: Optional[List[str]] = None,
        cash_register_id: Optional[List[str]] = None,
        stock_code: Optional[str] = None,
        desc: Optional[bool] = False,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        self_receipts: Optional[bool] = True,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        storage: Optional[SessionStorage] = None,
    ) -> Generator:
        """
        Generator to search and retrieve receipts.

        This function searches for receipts based on various filters and yields the results.

        Args:
            fiscal_code (Optional[str]): Filter for receipts with a specific fiscal code.
            barcode (Optional[str]): Filter for receipts with a specific barcode.
            shift_id (Optional[List[str]]): Filter for receipts with specific shift IDs.
            branch_id (Optional[List[str]]): Filter for receipts with specific branch IDs.
            cash_register_id (Optional[List[str]]): Filter for receipts with specific cash register IDs.
            stock_code (Optional[str]): Filter for receipts with a specific stock code.
            desc (Optional[bool]): Flag to sort results in descending order.
            from_date (Optional[Union[datetime.datetime, str]]): Filter for receipts from a specific date.
            to_date (Optional[Union[datetime.datetime, str]]): Filter for receipts up to a specific date.
            self_receipts (Optional[bool]): Flag to include self-issued receipts.
            limit (Optional[int]): The maximum number of receipts to retrieve.
            offset (Optional[int]): The offset for pagination.
            storage (Optional[SessionStorage]): The session storage to use.

        Returns:
            Generator: Yields the information of retrieved receipts.
        """
        get_receipts = receipts.GetReceiptsSearch(
            fiscal_code=fiscal_code,
            barcode=barcode,
            shift_id=shift_id,
            branch_id=branch_id,
            cash_register_id=cash_register_id,
            stock_code=stock_code,
            desc=desc,
            from_date=from_date,
            to_date=to_date,
            self_receipts=self_receipts,
            limit=limit,
            offset=offset,
        )
        while (receipts_result := self.client(get_receipts, storage=storage))["results"]:
            get_receipts.resolve_pagination(receipts_result).shift_next_page()
            yield from receipts_result["results"]

    def create_service_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[float] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates a service receipt about depositing change to the cash register or cash collection and checks its status.

        Args:
            receipt (Optional[Dict[str, Any]): A dictionary containing receipt information.
            relax: A float indicating the relaxation factor.
            timeout: An optional float for request timeout.
            storage: An optional SessionStorage object.
            **payload: Additional keyword arguments for creating the receipt. Cannot be used together with @receipt.

        Returns:
            The result of checking the status of the created receipt.
        """
        response = self.client(
            receipts.CreateServiceReceipt(receipt=receipt, **payload),
            storage=storage,
            request_timeout=timeout,
        )
        logger.info("Trying to create receipt %s", response["id"])

        return self._check_status(response, storage, relax, timeout)

    def create_cash_withdrawal_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[float] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        response = self.client(
            receipts.CreateCashWithdrawalReceipt(receipt=receipt, **payload),
            storage=storage,
            request_timeout=timeout,
        )
        logger.info("Trying to create receipt %s", response["id"])

        return self._check_status(response, storage, relax, timeout)

    def _check_status(
        self,
        receipt: Dict[str, Any],
        storage: Optional[SessionStorage] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[float] = None,
    ):
        shift = self.client.wait_status(
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


class AsyncReceipts:
    def __init__(self, client):
        self.client = client

    async def create_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates a receipt and optionally waits for its status.

        This function creates a receipt with the provided payload and waits for its status if specified.

        Args:
            receipt (Optional[Dict[str, Any]): A dictionary containing receipt information.
            relax (float): A float indicating the relaxation factor.
            timeout (Optional[int]): An optional timeout value.
            storage (Optional[SessionStorage]): The session storage to use.
            wait (bool): Flag to indicate whether to wait for the receipt status.
            **payload: Additional keyword arguments for creating the receipt. Cannot be used together with @receipt.

        Returns:
            Dict[str, Any]: The result of checking the status of the created receipt if wait is True, otherwise the created
            receipt itself.
        """
        response = await self.client(
            receipts.CreateReceipt(receipt=receipt, **payload),
            storage=storage,
            # request_timeout=timeout,
        )
        logger.info("Trying create receipt %s", response["id"])  # type: ignore[index]
        if not wait:
            return response

        return await self._check_status(response, storage, relax, timeout)  # type: ignore[index,arg-type]

    async def create_external_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ):
        receipt = await self.client(receipts.AddExternal(receipt, **payload), storage=storage)
        logger.info("Trying to create external receipt %s", receipt["id"])  # type: ignore[index]

        return await self._check_status(receipt, storage, relax, timeout)  # type: ignore[index,arg-type]

    async def get_receipts(
        self,
        fiscal_code: Optional[str] = None,
        serial: Optional[int] = None,
        desc: Optional[bool] = False,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        storage: Optional[SessionStorage] = None,
    ) -> AsyncGenerator:
        """
        Generator to retrieve a list of receipts.

        This function fetches receipts based on filters and yields the results.

        Args:
            fiscal_code (Optional[str]): Filter for receipts with a specific fiscal code.
            serial (Optional[int]): Filter for receipts with a specific serial number.
            desc (Optional[bool]): Flag to sort results in descending order.
            limit (Optional[int]): The maximum number of receipts to retrieve.
            offset (Optional[int]): The offset for pagination.
            storage (Optional[SessionStorage]): The session storage to use.

        Returns:
            Generator: Yields the information of retrieved receipts.
        """
        get_receipts = receipts.GetReceipts(
            fiscal_code=fiscal_code, serial=serial, desc=desc, limit=limit, offset=offset
        )
        while True:
            receipts_result = await self.client(get_receipts, storage=storage)
            results = receipts_result.get("results", [])

            if not results:
                break

            for result in results:
                yield result

            get_receipts.resolve_pagination(receipts_result)
            get_receipts.shift_next_page()

    async def get_receipts_search(
        self,
        fiscal_code: Optional[str] = None,
        barcode: Optional[str] = None,
        shift_id: Optional[List[str]] = None,
        branch_id: Optional[List[str]] = None,
        cash_register_id: Optional[List[str]] = None,
        stock_code: Optional[str] = None,
        desc: Optional[bool] = False,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        self_receipts: Optional[bool] = True,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        storage: Optional[SessionStorage] = None,
    ) -> AsyncGenerator:
        """
        Generator to search and retrieve receipts.

        This function searches for receipts based on various filters and yields the results.

        Args:
            fiscal_code (Optional[str]): Filter for receipts with a specific fiscal code.
            barcode (Optional[str]): Filter for receipts with a specific barcode.
            shift_id (Optional[List[str]]): Filter for receipts with specific shift IDs.
            branch_id (Optional[List[str]]): Filter for receipts with specific branch IDs.
            cash_register_id (Optional[List[str]]): Filter for receipts with specific cash register IDs.
            stock_code (Optional[str]): Filter for receipts with a specific stock code.
            desc (Optional[bool]): Flag to sort results in descending order.
            from_date (Optional[Union[datetime.datetime, str]]): Filter for receipts from a specific date.
            to_date (Optional[Union[datetime.datetime, str]]): Filter for receipts up to a specific date.
            self_receipts (Optional[bool]): Flag to include self-issued receipts.
            limit (Optional[int]): The maximum number of receipts to retrieve.
            offset (Optional[int]): The offset for pagination.
            storage (Optional[SessionStorage]): The session storage to use.

        Returns:
            Generator: Yields the information of retrieved receipts.
        """
        get_receipts = receipts.GetReceiptsSearch(
            fiscal_code=fiscal_code,
            barcode=barcode,
            shift_id=shift_id,
            branch_id=branch_id,
            cash_register_id=cash_register_id,
            stock_code=stock_code,
            desc=desc,
            from_date=from_date,
            to_date=to_date,
            self_receipts=self_receipts,
            limit=limit,
            offset=offset,
        )

        while True:
            receipts_result = await self.client(get_receipts, storage=storage)
            results = receipts_result.get("results", [])

            if not results:
                break

            for result in results:
                yield result

            get_receipts.resolve_pagination(receipts_result)
            get_receipts.shift_next_page()

    async def create_service_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[float] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates a service receipt about depositing change to the cash register or cash collection and checks its status.

        Args:
            receipt (Optional[Dict[str, Any]): A dictionary containing receipt information.
            relax: A float indicating the relaxation factor.
            timeout: An optional float for request timeout.
            storage: An optional SessionStorage object.
            **payload: Additional keyword arguments for creating the receipt. Cannot be used together with @receipt.

        Returns:
            The result of checking the status of the created receipt.
        """
        response = await self.client(
            receipts.CreateServiceReceipt(receipt=receipt, **payload),
            storage=storage,
            request_timeout=timeout,
        )
        logger.info("Trying to create receipt %s", response["id"])

        return await self._check_status(response, storage, relax, timeout)

    async def create_cash_withdrawal_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[float] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        response = await self.client(
            receipts.CreateCashWithdrawalReceipt(receipt=receipt, **payload),
            storage=storage,
            request_timeout=timeout,
        )
        logger.info("Trying to create receipt %s", response["id"])

        return await self._check_status(response, storage, relax, timeout)

    async def _check_status(
        self,
        receipt: Dict[str, Any],
        storage: Optional[SessionStorage] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[float] = None,
    ):
        shift = await self.client.wait_status(
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
