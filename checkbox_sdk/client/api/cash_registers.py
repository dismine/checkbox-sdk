import datetime
import logging
from typing import Any, Dict, Optional, Generator, Union, List, AsyncGenerator

from checkbox_sdk.client.api.base import AsyncPaginationMixin, PaginationMixin
from checkbox_sdk.exceptions import CheckBoxError
from checkbox_sdk.methods import cash_register
from checkbox_sdk.storage.simple import SessionStorage

logger = logging.getLogger(__name__)


class CashRegisters(PaginationMixin):
    def get_cash_registers(  # pylint: disable=too-many-positional-arguments
        self,
        storage: Optional[SessionStorage] = None,
        in_use: Optional[bool] = None,
        fiscal_number: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> Generator:
        """
        Generator to retrieve a list of available cash registers.

        This function fetches cash registers using pagination and yields the results.

        Args:
            storage (Optional[SessionStorage]): The session storage to use.
            in_use (Optional[bool]): Filter for cash registers in use.
            fiscal_number (Optional[str]): Filter for cash registers with a specific fiscal number.
            limit (int): The maximum number of cash registers to retrieve.
            offset (int): The offset for pagination.

        Returns:
            Generator: Yields the information of available cash registers.
        """
        get_cash_registers = cash_register.GetCashRegisters(
            in_use=in_use, fiscal_number=fiscal_number, limit=limit, offset=offset
        )
        yield from self.fetch_paginated_results(get_cash_registers, storage=storage)

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

        storage = storage or self.client.storage

        if not cash_register_id:
            if not storage.license_key:
                raise CheckBoxError("Field cash_register_id is required")

            if storage.cash_register is None:
                raise CheckBoxError("Cash register storage is None")

            cash_register_id = storage.cash_register.get("id")  # type: ignore[attr-defined]
            if not cash_register_id:
                raise CheckBoxError("Cash register ID not found in session storage")
        elif not isinstance(cash_register_id, str):
            raise CheckBoxError("Cash register ID must be a string")

        return self.client(cash_register.GetCashRegister(cash_register_id=cash_register_id), storage=storage)

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
        return self.client(cash_register.PingTaxService(), storage=storage)

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

        return self.client(cash_register.GoOnline(), storage=storage)

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

        return self.client(
            cash_register.GoOffline(go_offline_date=go_offline_date, fiscal_code=fiscal_code), storage=storage
        )

    def ask_offline_codes(
        self,
        ask_count: int = 2000,
        sync: bool = False,
        storage: Optional[SessionStorage] = None,
    ) -> None:
        """
        Requests offline codes from the tax service to fill Checkbox's cache.

        This method directly asks for a specified number of offline codes from the tax service and fills Checkbox's
        cache. It should only be used in scenarios where you need to pre-fill the cache with offline codes but do not
        intend to use them immediately.

        Note:
            If you plan to use the offline codes, it is recommended to call
            :meth:`get_offline_codes <checkbox_sdk.client.api.cash_registers.CashRegisters.get_offline_codes>`
            instead, as it includes logic to request and retrieve codes efficiently.

        Args:
            ask_count (int): The number of offline codes to request from the tax service (default is 2000).
            sync (bool): Whether to perform the request synchronously (default is False).
            storage (Optional[SessionStorage]): An optional session storage object for managing the state of requests.
        """
        self.client(cash_register.AskOfflineCodes(count=ask_count, sync=sync), storage=storage)

    def get_offline_codes(
        self,
        ask_count: int = 2000,
        threshold: int = 500,
        storage: Optional[SessionStorage] = None,
    ) -> List[str]:
        """
        Retrieves offline fiscal codes from Checkbox's cache and refills it when necessary.

        This method is designed to obtain offline codes for fiscal transactions using the Checkbox SDK. It first
        checks the available number of offline codes in the cache. If the number of available codes falls below the
        specified threshold, it requests additional codes from the tax server. The method then returns a list of
        fiscal codes for offline transactions.

        Args:
            ask_count (int): The number of offline codes to retrieve (default is 2000).
            threshold (int): The number of minimal number of offline codes after which new set will be asked from the
                             tax server
            storage (Optional[SessionStorage]): An optional session storage object for managing the state of requests.

        Returns:
            List[str]: A list of fiscal codes for offline transactions.
        """
        logger.info("Checking available number of offline codes...")
        response = self.client(cash_register.GetOfflineCodesCount(), storage=storage)

        if not response.get("enough_offline_codes", False) or response.get("available", 0) <= threshold:
            logger.info("Ask for more offline codes (count=%d)", ask_count)
            self.client(cash_register.AskOfflineCodes(count=ask_count, sync=True), storage=storage)

        logger.info("Load offline codes...")
        codes = self.client(cash_register.GetOfflineCodes(count=ask_count), storage=storage)
        return [item["fiscal_code"] for item in codes]

    def get_offline_time(
        self,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves the offline time information using the client with the provided storage.

        Args:
            from_date: The start date for the offline time query.
            to_date: The end date for the offline time query.
            storage: An optional session storage to use for the retrieval.

        Returns:
            A dictionary containing the offline time information.

        """
        return self.client(cash_register.GetOfflineTime(from_date=from_date, to_date=to_date), storage=storage)

    def get_cash_register_shifts(  # pylint: disable=too-many-positional-arguments
        self,
        storage: Optional[SessionStorage] = None,
        statuses: Optional[List[str]] = None,
        desc: Optional[bool] = False,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
    ) -> Generator:
        """
        Retrieves cash register shifts using the client with the provided storage and filter options.

        Args:
            storage: An optional session storage to use for the retrieval.
            statuses: An optional list of status strings to filter the shifts.
            desc: A boolean indicating whether to sort the shifts in descending order.
            from_date: The start date for the shift query.
            to_date: The end date for the shift query.
            limit: The maximum number of shifts to retrieve.
            offset: The offset for pagination.

        Yields:
            Generator yielding cash register shift results.

        """
        get_cash_register_shifts = cash_register.GetCashRegisterShifts(
            statuses=statuses,
            desc=desc,
            from_date=from_date,
            to_date=to_date,
            limit=limit,
            offset=offset,
        )
        yield from self.fetch_paginated_results(get_cash_register_shifts, storage=storage)


class AsyncCashRegisters(AsyncPaginationMixin):
    async def get_cash_registers(  # pylint: disable=too-many-positional-arguments
        self,
        storage: Optional[SessionStorage] = None,
        in_use: Optional[bool] = None,
        fiscal_number: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> AsyncGenerator:
        """
        Generator to retrieve a list of available cash registers.

        This function fetches cash registers using pagination and yields the results.

        Args:
            storage (Optional[SessionStorage]): The session storage to use.
            in_use (Optional[bool]): Filter for cash registers in use.
            fiscal_number (Optional[str]): Filter for cash registers with a specific fiscal number.
            limit (int): The maximum number of cash registers to retrieve.
            offset (int): The offset for pagination.

        Returns:
            Generator: Yields the information of available cash registers.
        """
        get_cash_registers = cash_register.GetCashRegisters(
            in_use=in_use, fiscal_number=fiscal_number, limit=limit, offset=offset
        )

        async for result in self.fetch_paginated_results(get_cash_registers, storage=storage):
            yield result

    async def get_cash_register(
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

        storage = storage or self.client.storage

        if not cash_register_id:
            if not storage.license_key:
                raise CheckBoxError("Field cash_register_id is required")

            if storage.cash_register is None:
                raise CheckBoxError("Cash register storage is None")

            cash_register_id = storage.cash_register.get("id")  # type: ignore[attr-defined]
            if not cash_register_id:
                raise CheckBoxError("Cash register ID not found in session storage")
        elif not isinstance(cash_register_id, str):
            raise CheckBoxError("Cash register ID must be a string")

        return await self.client(cash_register.GetCashRegister(cash_register_id=cash_register_id), storage=storage)

    async def ping_tax_service(
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
        return await self.client(cash_register.PingTaxService(), storage=storage)

    async def go_online(
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

        return await self.client(cash_register.GoOnline(), storage=storage)

    async def go_offline(
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

        return await self.client(
            cash_register.GoOffline(go_offline_date=go_offline_date, fiscal_code=fiscal_code), storage=storage
        )

    async def ask_offline_codes(
        self,
        ask_count: int = 2000,
        sync: bool = False,
        storage: Optional[SessionStorage] = None,
    ) -> None:
        """
        Asynchronously requests offline codes from the tax service to fill Checkbox's cache.

        This method directly asks for a specified number of offline codes from the tax service and fills Checkbox's
        cache. It should only be used in scenarios where you need to pre-fill the cache with offline codes but do not
        intend to use them immediately.

        Note:
            If you plan to use the offline codes, it is recommended to call
            :meth:`get_offline_codes <checkbox_sdk.client.api.cash_registers.AsyncCashRegisters.get_offline_codes>`
            instead, as it includes logic to request and retrieve codes efficiently.

        Args:
            ask_count (int): The number of offline codes to request from the tax service (default is 2000).
            sync (bool): Whether to perform the request synchronously (default is False).
            storage (Optional[SessionStorage]): An optional session storage object for managing the state of requests.
        """
        await self.client(cash_register.AskOfflineCodes(count=ask_count, sync=sync), storage=storage)

    async def get_offline_codes(
        self,
        ask_count: int = 2000,
        threshold: int = 500,
        storage: Optional[SessionStorage] = None,
    ) -> List[str]:
        """
        Asynchronously retrieves offline fiscal codes from Checkbox's cache and refills it when necessary.

        This method is designed to asynchronously obtain offline codes for fiscal transactions using the Checkbox SDK.
        It checks the available number of offline codes in the cache. If the available count falls below the specified
        threshold, it requests additional codes from the tax server. The method then returns a list of fiscal codes
        for offline transactions.

        Args:
            ask_count (int): The number of offline codes to retrieve (default is 2000).
            threshold (int): The number of minimal number of offline codes after which new set will be asked from the
                             tax server
            storage (Optional[SessionStorage]): An optional session storage object for managing the state of requests.

        Returns:
            List[str]: A list of fiscal codes for offline transactions.
        """
        logger.info("Checking available number of offline codes...")
        response = await self.client(cash_register.GetOfflineCodesCount(), storage=storage)

        if not response.get("enough_offline_codes", False) or response.get("available", 0) <= threshold:
            logger.info("Ask for more offline codes (count=%d)", ask_count)
            await self.client(cash_register.AskOfflineCodes(count=ask_count, sync=True), storage=storage)

        logger.info("Load offline codes...")
        codes = await self.client(cash_register.GetOfflineCodes(count=ask_count), storage=storage)
        return [item["fiscal_code"] for item in codes]

    async def get_offline_time(
        self,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves the offline time information using the client with the provided storage.

        Args:
            from_date: The start date for the offline time query.
            to_date: The end date for the offline time query.
            storage: An optional session storage to use for the retrieval.

        Returns:
            A dictionary containing the offline time information.

        """
        return await self.client(cash_register.GetOfflineTime(from_date=from_date, to_date=to_date), storage=storage)

    async def get_cash_register_shifts(  # pylint: disable=too-many-positional-arguments
        self,
        storage: Optional[SessionStorage] = None,
        statuses: Optional[List[str]] = None,
        desc: Optional[bool] = False,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
    ) -> AsyncGenerator:
        """
        Asynchronously retrieves cash register shifts using the client with the provided storage and filter options.

        Args:
            storage: An optional session storage to use for the retrieval.
            statuses: An optional list of status strings to filter the shifts.
            desc: A boolean indicating whether to sort the shifts in descending order.
            from_date: The start date for the shift query.
            to_date: The end date for the shift query.
            limit: The maximum number of shifts to retrieve.
            offset: The offset for pagination.

        Yields:
            AsyncGenerator yielding cash register shift results.

        """
        get_cash_register_shifts = cash_register.GetCashRegisterShifts(
            statuses=statuses,
            desc=desc,
            from_date=from_date,
            to_date=to_date,
            limit=limit,
            offset=offset,
        )

        async for result in self.fetch_paginated_results(get_cash_register_shifts, storage=storage):
            yield result
