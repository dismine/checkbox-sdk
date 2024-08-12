import datetime
from typing import Union, Optional, List, Generator, AsyncGenerator, Dict, Any
from uuid import UUID

from checkbox_sdk.methods import reports
from checkbox_sdk.storage.simple import SessionStorage


class Reports:
    def __init__(self, client):
        self.client = client

    def get_periodical_report(
        self,
        from_date: Union[datetime.datetime, str],
        to_date: Union[datetime.datetime, str],
        width: Optional[int] = 42,
        is_short: Optional[bool] = False,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        return self.client(
            reports.GetPeriodicalReport(from_date=from_date, to_date=to_date, width=width, is_short=is_short),
            storage=storage,
        )

    def get_reports(
        self,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        shift_id: Optional[List[str]] = None,
        serial: Optional[int] = None,
        is_z_report: Optional[bool] = None,
        desc: Optional[bool] = False,
        storage: Optional[SessionStorage] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
    ) -> Generator:
        """
        Retrieves reports based on specified criteria.

        Args:
            from_date: The start date for the report search.
            to_date: The end date for the report search.
            shift_id: The ID(s) of the shift(s) associated with the reports.
            serial: The serial number of the report.
            is_z_report: A flag indicating if the report is a Z report.
            desc: A flag to indicate descending order.
            storage: An optional session storage to use for the operation.
            limit: The maximum number of results to return.
            offset: The offset for paginating results.

        Yields:
            Results of reports based on the specified criteria.

        """
        get_report = reports.GetReports(
            from_date=from_date,
            to_date=to_date,
            shift_id=shift_id,
            serial=serial,
            is_z_report=is_z_report,
            desc=desc,
            limit=limit,
            offset=offset,
        )
        while (receipts_result := self.client(get_report, storage=storage))["results"]:
            get_report.resolve_pagination(receipts_result).shift_next_page()
            yield from receipts_result["results"]

    def create_x_report(
        self,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Creates an X report.

        Args:
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the created X report.

        Example:
            .. code-block:: python

                report = client.reports.create_x_report()
                print(report)
        """
        return self.client(
            reports.CreateXReport(),
            storage=storage,
        )

    def get_search_reports(
        self,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        shift_id: Optional[List[str]] = None,
        serial: Optional[int] = None,
        is_z_report: Optional[bool] = None,
        desc: Optional[bool] = False,
        cash_register_id: Optional[List[str]] = None,
        storage: Optional[SessionStorage] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
    ) -> Generator:
        """
        Retrieves search reports based on specified criteria.

        Args:
            from_date: The start date for the report search.
            to_date: The end date for the report search.
            shift_id: The ID(s) of the shift(s) associated with the reports.
            serial: The serial number of the report.
            is_z_report: A flag indicating if the report is a Z report.
            desc: A flag to indicate descending order.
            cash_register_id: The ID(s) of the cash register(s) associated with the reports.
            storage: An optional session storage to use for the operation.
            limit: The maximum number of results to return.
            offset: The offset for paginating results.

        Yields:
            Results of search reports based on the specified criteria.

        Example:
            .. code-block:: python

                for report in client.reports.get_search_reports(from_date="2024-01-01", to_date="2024-01-31"):
                    print(report)

        Notes:
            - This method handles pagination automatically, continuing to fetch and yield reports until no more results
            are available.
        """
        search_reports = reports.SearchReports(
            from_date=from_date,
            to_date=to_date,
            shift_id=shift_id,
            serial=serial,
            is_z_report=is_z_report,
            desc=desc,
            cash_register_id=cash_register_id,
            limit=limit,
            offset=offset,
        )

        while True:
            reports_result = self.client(search_reports, storage=storage)
            results = reports_result.get("results", [])

            if not results:
                break

            yield from results
            search_reports.resolve_pagination(reports_result)
            search_reports.shift_next_page()

    def add_external_report(
        self,
        report: Optional[Dict] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Adds an external report.

        Args:
            report: The external report to add.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload for the request.

        Returns:
            A dictionary containing the details of the added external report.

        Raises:
            ValueError: If both 'report' and '**payload' are passed together.

        Notes:
            - This method sends a POST request to add an external report.
        """
        if report is not None and payload:
            raise ValueError("'report' and '**payload' cannot be passed together")

        return self.client(
            reports.AddExternal(report=report, **payload),
            storage=storage,
        )

    def get_report(
        self,
        report_id: Union[str, UUID],
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves a specific report.

        Args:
            report_id: The ID of the report to retrieve.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the retrieved report.

        Example:
            .. code-block:: python

                report = client.reports.get_report(report_id="123e4567-e89b-12d3-a456-426614174000")
                print(report)

        Notes:
            - This method sends a GET request to retrieve the report with the specified ID.
        """
        return self.client(
            reports.GetReport(report_id=report_id),
            storage=storage,
        )

    def get_report_text(
        self,
        report_id: Union[str, UUID],
        width: Optional[int] = 42,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Retrieves the text visualization of a specific report.

        Args:
            report_id: The ID of the report to retrieve.
            width: The width of the text visualization. Default is 42.
            storage: An optional session storage to use for the operation.

        Returns:
            A string containing the text visualization of the report.

        Example:
            .. code-block:: python

                report_text = client.reports.get_report_text(report_id="123e4567-e89b-12d3-a456-426614174000", width=80)
                print(report_text)

        Notes:
            - This method sends a GET request to retrieve the text visualization of the report with the specified ID.
            - The response is decoded from bytes to a string.
        """
        return self.client(
            reports.GetReportVisualizationText(report_id=report_id, width=width),
            storage=storage,
        )

    def get_report_png(
        self,
        report_id: Union[str, UUID],
        width: Optional[int] = 34,
        paper_width: Optional[int] = 58,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Retrieves an ASCII image visualization of a specific report.

        Args:
            report_id: The ID of the report to retrieve.
            width: The width of the ASCII image visualization. Default is 34.
            paper_width: The width of the paper for the ASCII image visualization. Default is 58.
            storage: An optional session storage to use for the operation.

        Returns:
            The ASCII image visualization of the report as a string.

        Example:
            .. code-block:: python

                report_ascii_image = client.reports.get_report_png(report_id="123e4567-e89b-12d3-a456-426614174000",
                                                                   width=50, paper_width=70)
                print(report_ascii_image)

        Notes:
            - This method sends a GET request to retrieve the ASCII image visualization of the report with the
              specified ID.
            - The method returns an ASCII image that can be printed, not a PNG file.
        """
        return self.client(
            reports.GetReportVisualizationPng(report_id=report_id, width=width, paper_width=paper_width),
            storage=storage,
        )


class AsyncReports:
    def __init__(self, client):
        self.client = client

    async def get_periodical_report(
        self,
        from_date: Union[datetime.datetime, str],
        to_date: Union[datetime.datetime, str],
        width: Optional[int] = 42,
        is_short: Optional[bool] = False,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        return await self.client(
            reports.GetPeriodicalReport(from_date=from_date, to_date=to_date, width=width, is_short=is_short),
            storage=storage,
        )

    async def get_reports(
        self,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        shift_id: Optional[List[str]] = None,
        serial: Optional[int] = None,
        is_z_report: Optional[bool] = None,
        desc: Optional[bool] = False,
        storage: Optional[SessionStorage] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
    ) -> AsyncGenerator:
        """
        Retrieves reports based on specified criteria.

        Args:
            from_date: The start date for the report search.
            to_date: The end date for the report search.
            shift_id: The ID(s) of the shift(s) associated with the reports.
            serial: The serial number of the report.
            is_z_report: A flag indicating if the report is a Z report.
            desc: A flag to indicate descending order.
            storage: An optional session storage to use for the operation.
            limit: The maximum number of results to return.
            offset: The offset for paginating results.

        Yields:
            Results of reports based on the specified criteria.

        Example:
            .. code-block:: python

                async for report in client.reports.get_reports(from_date="2024-01-01", to_date="2024-01-31"):
                    print(report)

        Notes:
            - This method is designed to be used in an asynchronous context.
            - It handles pagination automatically, continuing to fetch and yield reports until no more results are available.

        """
        get_report = reports.GetReports(
            from_date=from_date,
            to_date=to_date,
            shift_id=shift_id,
            serial=serial,
            is_z_report=is_z_report,
            desc=desc,
            limit=limit,
            offset=offset,
        )
        while True:
            receipts_result = await self.client(get_report, storage=storage)
            results = receipts_result.get("results", [])

            if not results:
                break

            for result in results:
                yield result

            get_report.resolve_pagination(receipts_result)
            get_report.shift_next_page()

    async def create_x_report(
        self,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Asynchronously creates an X report.

        Args:
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the created X report.

        Example:
            .. code-block:: python

                report = await client.reports.create_x_report()
                print(report)
        """
        return await self.client(
            reports.CreateXReport(),
            storage=storage,
        )

    async def get_search_reports(
        self,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        shift_id: Optional[List[str]] = None,
        serial: Optional[int] = None,
        is_z_report: Optional[bool] = None,
        desc: Optional[bool] = False,
        cash_register_id: Optional[List[str]] = None,
        storage: Optional[SessionStorage] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
    ) -> AsyncGenerator:
        """
        Asynchronously retrieves search reports based on specified criteria.

        Args:
            from_date: The start date for the report search.
            to_date: The end date for the report search.
            shift_id: The ID(s) of the shift(s) associated with the reports.
            serial: The serial number of the report.
            is_z_report: A flag indicating if the report is a Z report.
            desc: A flag to indicate descending order.
            cash_register_id: The ID(s) of the cash register(s) associated with the reports.
            storage: An optional session storage to use for the operation.
            limit: The maximum number of results to return.
            offset: The offset for paginating results.

        Yields:
            Results of search reports based on the specified criteria.

        Example:
            .. code-block:: python

                async for report in client.reports.get_search_reports(from_date="2024-01-01", to_date="2024-01-31"):
                    print(report)

        Notes:
            - This method handles pagination automatically, continuing to fetch and yield reports until no more results
            are available.
        """
        search_reports = reports.SearchReports(
            from_date=from_date,
            to_date=to_date,
            shift_id=shift_id,
            serial=serial,
            is_z_report=is_z_report,
            desc=desc,
            cash_register_id=cash_register_id,
            limit=limit,
            offset=offset,
        )

        while True:
            reports_result = await self.client(search_reports, storage=storage)
            results = reports_result.get("results", [])

            if not results:
                break

            for result in results:
                yield result

            search_reports.resolve_pagination(reports_result)
            search_reports.shift_next_page()

    async def add_external_report(
        self,
        report: Optional[Dict] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Asynchronously adds an external report.

        Args:
            report: The external report to add.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload for the request.

        Returns:
            A dictionary containing the details of the added external report.

        Raises:
            ValueError: If both 'report' and '**payload' are passed together.

        Notes:
            - This method sends a POST request to add an external report asynchronously.
        """
        if report is not None and payload:
            raise ValueError("'report' and '**payload' cannot be passed together")

        return await self.client(
            reports.AddExternal(report=report, **payload),
            storage=storage,
        )

    async def get_report(
        self,
        report_id: Union[str, UUID],
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Asynchronously retrieves a specific report.

        Args:
            report_id: The ID of the report to retrieve.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the retrieved report.

        Example:
            .. code-block:: python

                report = await client.reports.get_report(report_id="123e4567-e89b-12d3-a456-426614174000")
                print(report)

        Notes:
            - This method sends a GET request to retrieve the report with the specified ID asynchronously.
        """
        return await self.client(
            reports.GetReport(report_id=report_id),
            storage=storage,
        )

    async def get_report_text(
        self,
        report_id: Union[str, UUID],
        width: Optional[int] = 42,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Asynchronously retrieves the text visualization of a specific report.

        Args:
            report_id: The ID of the report to retrieve.
            width: The width of the text visualization. Default is 42.
            storage: An optional session storage to use for the operation.

        Returns:
            A string containing the text visualization of the report.

        Example:
            .. code-block:: python

                report_text = await client.reports.get_report_text(report_id="123e4567-e89b-12d3-a456-426614174000",
                                                                   width=80)
                print(report_text)

        Notes:
            - This method sends a GET request to retrieve the text visualization of the report with the specified ID asynchronously.
            - The response is decoded from bytes to a string.
        """
        return await self.client(
            reports.GetReportVisualizationText(report_id=report_id, width=width),
            storage=storage,
        )

    async def get_report_png(
        self,
        report_id: Union[str, UUID],
        width: Optional[int] = 34,
        paper_width: Optional[int] = 58,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Asynchronously retrieves an ASCII image visualization of a specific report.

        Args:
            report_id: The ID of the report to retrieve.
            width: The width of the ASCII image visualization. Default is 34.
            paper_width: The width of the paper for the ASCII image visualization. Default is 58.
            storage: An optional session storage to use for the operation.

        Returns:
            The ASCII image visualization of the report as a string.

        Example:
            .. code-block:: python

                report_ascii_image = await client.reports.get_report_png(report_id="123e4567-e89b-12d3-a456-426614174000",
                                                                         width=50, paper_width=70)
                print(report_ascii_image)

        Notes:
            - This method sends a GET request to retrieve the ASCII image visualization of the report with the
              specified ID asynchronously.
            - The method returns an ASCII image that can be printed, not a PNG file.
        """
        return await self.client(
            reports.GetReportVisualizationPng(report_id=report_id, width=width, paper_width=paper_width),
            storage=storage,
        )
