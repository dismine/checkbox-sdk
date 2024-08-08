import datetime
import logging
from typing import Any, Dict, List, Optional, Generator, Union, AsyncGenerator
from uuid import UUID

from checkbox_sdk.consts import DEFAULT_REQUESTS_RELAX
from checkbox_sdk.exceptions import StatusException
from checkbox_sdk.methods import shifts
from checkbox_sdk.storage.simple import SessionStorage

logger = logging.getLogger(__name__)


class Shifts:
    def __init__(self, client):
        self.client = client

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
        while (shifts_result := self.client(get_shift, storage=storage))["results"]:
            get_shift.resolve_pagination(shifts_result).shift_next_page()
            yield from shifts_result["results"]

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
        storage = storage or self.client.storage
        self.client.refresh_info(storage=storage)
        if storage.shift is not None:
            logger.info(
                "Shift is already opened %s in status %s",
                storage.shift["id"],
                storage.shift["status"],
            )
            shift = storage.shift
        else:
            shift = self.client(shifts.CreateShift(**kwargs), storage=storage, request_timeout=timeout)
            logger.info("Created shift %s", shift["id"])

        if shift["status"] == "OPENED":
            return shift

        shift = self.client.wait_status(
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

        storage = storage or self.client.storage
        self.client.refresh_info(storage=storage)
        if storage.shift is None:
            logger.info("Shift is already closed")
            return storage.shift

        shift = self.client(shifts.CloseShift(**payload), storage=storage)
        logger.info("Trying to close shift %s", shift["id"])

        shift = self.client.wait_status(
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
    ) -> Union[Dict, None]:
        """
        Closes a shift online with the provided payload and options, waiting for the shift to be closed.

        Args:
            relax: The relaxation factor for requests.
            timeout: The timeout duration for the request.
            transaction_timeout: The timeout duration for the transaction.
            storage: An optional session storage to use for the operation.
            **payload: Additional keyword arguments for the shift closure.

        Raises:
            StatusException: If the shift cannot be closed due to transaction status.

        Returns:
            The zreport transaction for the closed shift, or None if the shift is already closed.

        """
        storage = storage or self.client.storage
        self.client.refresh_info(storage=storage)
        if storage.shift is None:
            logger.info("Shift is already closed")
            return storage.shift

        shift = self.client(shifts.CloseShift(**payload), storage=storage, request_timeout=timeout)
        logger.info("Trying to close shift %s", shift["id"])

        shift = self.client.wait_status(
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
        return self.client.transactions.wait_transaction(
            transaction_id=shift["closing_transaction"]["id"],
            timeout=transaction_timeout,
        )

    def close_shift_by_senior_cashier(
        self,
        shift_id: Union[str, UUID],
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        transaction_timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        shift: Optional[Dict] = None,
        **payload,
    ) -> Dict:
        """
        Closes a shift by a senior cashier with the provided shift ID, payload, and options.

        Args:
            shift_id: The ID of the shift to be closed.
            relax: The relaxation factor for requests.
            timeout: The timeout duration for the request.
            transaction_timeout: The timeout duration for the transaction.
            storage: An optional session storage to use for the operation.
            shift: An optional dictionary representing the shift details.
            **payload: Additional keyword arguments for the shift closure.

        Raises:
            StatusException: If the shift cannot be closed due to transaction status.

        Returns:
            The zreport transaction for the closed shift.

        """
        shift_response = self.client(
            shifts.CloseShiftBySeniorCashier(shift_id, shift=shift, **payload),
            storage=storage,
            request_timeout=timeout,
        )
        logger.info("Trying to close shift %s", shift_response["id"])

        shift_status = self.client.wait_status(
            shifts.GetShift(shift_id=shift_response["id"]),
            storage=storage,
            relax=relax,
            field="status",
            expected_value={"OPENED", "CLOSED"},
            timeout=timeout,
        )
        if shift_status["status"] == "OPENED":
            closing_transaction = shift_status["closing_transaction"]
            raise StatusException(
                "Shift can not be closed in due to transaction status moved to "
                f"{closing_transaction['status']!r}: {closing_transaction['response_status']!r} "
                f"{closing_transaction['response_error_message']!r}"
            )

        # zreport transaction
        return self.client.transactions.wait_transaction(
            transaction_id=shift_status["closing_transaction"]["id"],
            timeout=transaction_timeout,
        )


class AsyncShifts:
    def __init__(self, client):
        self.client = client

    async def get_shifts(
        self,
        statuses: Optional[List[str]] = None,
        desc: Optional[bool] = False,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        storage: Optional[SessionStorage] = None,
    ) -> AsyncGenerator:
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

        while True:
            shifts_result = await self.client(get_shift, storage=storage)
            results = shifts_result.get("results", [])

            if not results:
                break

            for result in results:
                yield result

            get_shift.resolve_pagination(shifts_result)
            get_shift.shift_next_page()

    async def create_shift(
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
        storage = storage or self.client.storage
        await self.client.refresh_info(storage=storage)
        if storage.shift is not None:
            logger.info(
                "Shift is already opened %s in status %s",
                storage.shift["id"],
                storage.shift["status"],
            )
            shift = storage.shift
        else:
            shift = await self.client(shifts.CreateShift(**kwargs), storage=storage, request_timeout=timeout)
            logger.info("Created shift %s", shift["id"])

        if shift["status"] == "OPENED":
            return shift

        shift = await self.client.wait_status(
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

    async def close_shift(
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

        storage = storage or self.client.storage
        await self.client.refresh_info(storage=storage)
        if storage.shift is None:
            logger.info("Shift is already closed")
            return storage.shift

        shift = await self.client(shifts.CloseShift(**payload), storage=storage)
        logger.info("Trying to close shift %s", shift["id"])

        shift = await self.client.wait_status(
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

    async def close_shift_online(
        self,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        transaction_timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Union[Dict, None]:
        """
        Asynchronously closes a shift online with the provided payload and options, waiting for the shift to be closed.

        Args:
            relax: The relaxation factor for requests.
            timeout: The timeout duration for the request.
            transaction_timeout: The timeout duration for the transaction.
            storage: An optional session storage to use for the operation.
            **payload: Additional keyword arguments for the shift closure.

        Raises:
            StatusException: If the shift cannot be closed due to transaction status.

        Returns:
            The zreport transaction for the closed shift, or None if the shift is already closed.

        """
        storage = storage or self.client.storage
        await self.client.refresh_info(storage=storage)
        if storage.shift is None:
            logger.info("Shift is already closed")
            return storage.shift

        shift = await self.client(shifts.CloseShift(**payload), storage=storage, request_timeout=timeout)
        logger.info("Trying to close shift %s", shift["id"])

        shift = await self.client.wait_status(
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
        return await self.client.transactions.wait_transaction(
            transaction_id=shift["closing_transaction"]["id"],
            timeout=transaction_timeout,
        )

    async def close_shift_by_senior_cashier(
        self,
        shift_id: Union[str, UUID],
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        transaction_timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        shift: Optional[Dict] = None,
        **payload,
    ) -> Dict:
        """
        Asynchronously closes a shift by a senior cashier with the provided shift ID, payload, and options.

        Args:
            shift_id: The ID of the shift to be closed.
            relax: The relaxation factor for requests.
            timeout: The timeout duration for the request.
            transaction_timeout: The timeout duration for the transaction.
            storage: An optional session storage to use for the operation.
            shift: An optional dictionary representing the shift details.
            **payload: Additional keyword arguments for the shift closure.

        Raises:
            StatusException: If the shift cannot be closed due to transaction status.

        Returns:
            The zreport transaction for the closed shift, or None if the shift is already closed.
        """
        shift_response = await self.client(
            shifts.CloseShiftBySeniorCashier(shift_id, shift=shift, **payload),
            storage=storage,
            request_timeout=timeout,
        )
        logger.info("Trying to close shift %s", shift_response["id"])

        shift_status = await self.client.wait_status(
            shifts.GetShift(shift_id=shift_response["id"]),
            storage=storage,
            relax=relax,
            field="status",
            expected_value={"OPENED", "CLOSED"},
            timeout=timeout,
        )
        if shift_status["status"] == "OPENED":
            closing_transaction = shift_status["closing_transaction"]
            raise StatusException(
                "Shift can not be closed in due to transaction status moved to "
                f"{closing_transaction['status']!r}: {closing_transaction['response_status']!r} "
                f"{closing_transaction['response_error_message']!r}"
            )

        # zreport transaction
        return await self.client.transactions.wait_transaction(
            transaction_id=shift_status["closing_transaction"]["id"],
            timeout=transaction_timeout,
        )
