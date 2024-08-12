from typing import Optional, Dict, Any, List, Union
from uuid import UUID

from checkbox_sdk.methods import extended_reports
from checkbox_sdk.storage.simple import SessionStorage


class ExtendedReports:
    def __init__(self, client):
        self.client = client

    def goods_report(
        self,
        data: Optional[List[Dict]] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Generates a goods report.

        Args:
            data: Additional data for the report.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload for the request.

        Returns:
            A dictionary containing the details of the generated goods report.

        Example:
            .. code-block:: python

                report = client.extended_reports.goods_report(data=[{"item": "example"}])
                print(report)

        Notes:
            - This method sends a POST request to generate the goods report.
        """
        return self.client(
            extended_reports.CreateGoodsReport(data=data, **payload),
            storage=storage,
        )

    def create_z_report(
        self,
        data: Optional[List[Dict]] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates a Z report.

        Args:
            data: Additional data for the report.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload for the request.

        Returns:
            A dictionary containing the details of the created Z report.

        Example:
            .. code-block:: python

                z_report = client.extended_reports.create_z_report(data=[{"item": "example"}])
                print(z_report)

        Notes:
            - This method sends a POST request to create a Z report.
            - The `data` argument can be used to provide additional data required for generating the report.
            - Additional payload parameters can be passed as keyword arguments.
        """
        return self.client(
            extended_reports.CreateZReport(data=data, **payload),
            storage=storage,
        )

    def actual_revenue_report(
        self,
        data: Optional[List[Dict]] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates an actual revenue report.

        Args:
            data: Optional list of dictionaries containing additional data for the report.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload to include in the request.

        Returns:
            A dictionary containing the details of the created actual revenue report.

        Example:
            .. code-block:: python

                revenue_report = client.extended_reports.actual_revenue_report(data=[{"item": "example"}])
                print(revenue_report)

        Notes:
            - This method sends a POST request to create an actual revenue report.
            - The `data` argument can be used to provide additional data required for generating the report.
            - Additional payload parameters can be passed as keyword arguments.
        """
        return self.client(
            extended_reports.CreateActualRevenueReport(data=data, **payload),
            storage=storage,
        )

    def net_turnover_report(
        self,
        data: Optional[List[Dict]] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates a net turnover report.

        Args:
            data: Optional list of dictionaries containing additional data for the report.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload to include in the request.

        Returns:
            A dictionary containing the details of the created net turnover report.

        Example:
            .. code-block:: python

                turnover_report = client.extended_reports.net_turnover_report(data=[{"item": "example"}])
                print(turnover_report)

        Notes:
            - This method sends a POST request to create a net turnover report.
            - The `data` argument can be used to provide additional data required for generating the report.
            - Additional payload parameters can be passed as keyword arguments.
        """
        return self.client(
            extended_reports.CreateNetTurnoverReport(data=data, **payload),
            storage=storage,
        )

    def bookkeeper_z_report(
        self,
        data: Optional[List[Dict]] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates a bookkeeper Z report.

        Args:
            data: Optional list of dictionaries containing additional data for the report.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload to include in the request.

        Returns:
            A dictionary containing the details of the created bookkeeper Z report.

        Example:
            .. code-block:: python

                z_report = client.extended_reports.bookkeeper_z_report(data=[{"item": "example"}])
                print(z_report)

        Notes:
            - This method sends a POST request to create a bookkeeper Z report.
            - The `data` argument can be used to provide additional data required for generating the report.
            - Additional payload parameters can be passed as keyword arguments.
        """
        return self.client(
            extended_reports.CreateBookkeeperZReport(data=data, **payload),
            storage=storage,
        )

    def daily_cash_flow_report(
        self,
        data: Optional[List[Dict]] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates a daily cash flow report.

        Args:
            data: Optional list of dictionaries containing additional data for the report.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload to include in the request.

        Returns:
            A dictionary containing the details of the created daily cash flow report.

        Example:
            .. code-block:: python

                cash_flow_report = client.extended_reports.daily_cash_flow_report(data=[{"item": "example"}])
                print(cash_flow_report)

        Notes:
            - This method sends a POST request to create a daily cash flow report.
            - The `data` argument can be used to provide additional data required for generating the report.
            - Additional payload parameters can be passed as keyword arguments.
        """
        return self.client(
            extended_reports.CreateDailyCashFlowReport(data=data, **payload),
            storage=storage,
        )

    def create_receipt_report(
        self,
        data: Optional[List[Dict]] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates a receipt report.

        Args:
            data: Optional list of dictionaries containing additional data for the report.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload to include in the request.

        Returns:
            A dictionary containing the details of the created receipt report.

        Example:
            .. code-block:: python

                receipt_report = client.extended_reports.create_receipt_report(data=[{"item": "example"}])
                print(receipt_report)

        Notes:
            - This method sends a POST request to create a receipt report.
            - The `data` argument can be used to provide additional data required for generating the report.
            - Additional payload parameters can be passed as keyword arguments.
        """
        return self.client(
            extended_reports.CreateReceiptReport(data=data, **payload),
            storage=storage,
        )

    def get_report_task_by_id(
        self,
        report_task_id: Union[str, UUID],
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves a specific report task by its ID.

        Args:
            report_task_id: The ID of the report task to retrieve.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the retrieved report task.

        Example:
            .. code-block:: python

                report_task =
                    client.extended_reports.get_report_task_by_id(report_task_id="123e4567-e89b-12d3-a456-426614174000")
                print(report_task)

        Notes:
            - This method sends a GET request to retrieve the report task with the specified ID.
        """
        return self.client(
            extended_reports.GetReportTaskById(report_task_id=report_task_id),
            storage=storage,
        )

    def report_xlsx_task_by_id(
        self,
        report_task_id: Union[str, UUID],
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves the details of a specific report task by its ID, including the XLSX file if available.

        Args:
            report_task_id: The ID of the report task to retrieve. Can be a string or a UUID.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the report task and possibly the XLSX file.

        Example:
            .. code-block:: python

                report_task_details =
                    client.extended_reports.report_xlsx_task_by_id(report_task_id="123e4567-e89b-12d3-a456-426614174000")
                print(report_task_details)

        Notes:
            - This method sends a GET request to retrieve the details of the report task with the specified ID.
        """
        return self.client(
            extended_reports.GetReportXlsxTaskById(report_task_id=report_task_id),
            storage=storage,
        )

    def report_json_task_by_id(
        self,
        report_task_id: Union[str, UUID],
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves the details of a specific report task by its ID, including the JSON file if available.

        Args:
            report_task_id: The ID of the report task to retrieve. Can be a string or a UUID.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the report task and possibly the JSON file.

        Example:
            .. code-block:: python

                report_task_details =
                    client.extended_reports.
                    report_json_task_by_id(report_task_id="123e4567-e89b-12d3-a456-426614174000")
                print(report_task_details)

        Notes:
            - This method sends a GET request to retrieve the details of the report task with the specified ID.
        """
        return self.client(
            extended_reports.GetReportJsonTaskById(report_task_id=report_task_id),
            storage=storage,
        )


class AsyncExtendedReports:
    def __init__(self, client):
        self.client = client

    async def goods_report(
        self,
        data: Optional[List[Dict]] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Asynchronously generates a goods report.

        Args:
            data: Additional data for the report.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload for the request.

        Returns:
            A dictionary containing the details of the generated goods report.

        Example:
            .. code-block:: python

                report = await client.extended_reports.goods_report(data=[{"item": "example"}])
                print(report)

        Notes:
            - This method sends a POST request to generate the goods report asynchronously.
        """
        return await self.client(
            extended_reports.CreateGoodsReport(data=data, **payload),
            storage=storage,
        )

    async def create_z_report(
        self,
        data: Optional[List[Dict]] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Asynchronously creates a Z report.

        Args:
            data: Optional list of dictionaries containing additional data for the report.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload to include in the request.

        Returns:
            A dictionary containing the details of the created Z report.

        Example:
            .. code-block:: python

                z_report = await client.create_z_report(data=[{"item": "example"}])
                print(z_report)

        Notes:
            - This method sends a POST request to create a Z report asynchronously.
            - The `data` argument can be used to provide additional data required for generating the report.
            - Additional payload parameters can be passed as keyword arguments.
        """
        return await self.client(
            extended_reports.CreateZReport(data=data, **payload),
            storage=storage,
        )

    async def actual_revenue_report(
        self,
        data: Optional[List[Dict]] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Asynchronously creates an actual revenue report.

        Args:
            data: Optional list of dictionaries containing additional data for the report.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload to include in the request.

        Returns:
            A dictionary containing the details of the created actual revenue report.

        Example:
            .. code-block:: python

                revenue_report = await client.extended_reports.actual_revenue_report(data=[{"item": "example"}])
                print(revenue_report)

        Notes:
            - This method sends a POST request to create an actual revenue report asynchronously.
            - The `data` argument can be used to provide additional data required for generating the report.
            - Additional payload parameters can be passed as keyword arguments.
        """
        return await self.client(
            extended_reports.CreateActualRevenueReport(data=data, **payload),
            storage=storage,
        )

    async def net_turnover_report(
        self,
        data: Optional[List[Dict]] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Asynchronously creates a net turnover report.

        Args:
            data: Optional list of dictionaries containing additional data for the report.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload to include in the request.

        Returns:
            A dictionary containing the details of the created net turnover report.

        Example:
            .. code-block:: python

                turnover_report = await client.extended_reports.net_turnover_report(data=[{"item": "example"}])
                print(turnover_report)

        Notes:
            - This method sends a POST request to create a net turnover report asynchronously.
            - The `data` argument can be used to provide additional data required for generating the report.
            - Additional payload parameters can be passed as keyword arguments.
        """
        return await self.client(
            extended_reports.CreateNetTurnoverReport(data=data, **payload),
            storage=storage,
        )

    async def bookkeeper_z_report(
        self,
        data: Optional[List[Dict]] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Asynchronously creates a bookkeeper Z report.

        Args:
            data: Optional list of dictionaries containing additional data for the report.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload to include in the request.

        Returns:
            A dictionary containing the details of the created bookkeeper Z report.

        Example:
            .. code-block:: python

                z_report = await client.extended_reports.bookkeeper_z_report(data=[{"item": "example"}])
                print(z_report)

        Notes:
            - This method sends a POST request to create a bookkeeper Z report asynchronously.
            - The `data` argument can be used to provide additional data required for generating the report.
            - Additional payload parameters can be passed as keyword arguments.
        """
        return await self.client(
            extended_reports.CreateBookkeeperZReport(data=data, **payload),
            storage=storage,
        )

    async def daily_cash_flow_report(
        self,
        data: Optional[List[Dict]] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Asynchronously creates a daily cash flow report.

        Args:
            data: Optional list of dictionaries containing additional data for the report.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload to include in the request.

        Returns:
            A dictionary containing the details of the created daily cash flow report.

        Example:
            .. code-block:: python

                cash_flow_report = await client.extended_reports.daily_cash_flow_report(data=[{"item": "example"}])
                print(cash_flow_report)

        Notes:
            - This method sends a POST request to create a daily cash flow report asynchronously.
            - The `data` argument can be used to provide additional data required for generating the report.
            - Additional payload parameters can be passed as keyword arguments.
        """
        return await self.client(
            extended_reports.CreateDailyCashFlowReport(data=data, **payload),
            storage=storage,
        )

    async def create_receipt_report(
        self,
        data: Optional[List[Dict]] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> Dict[str, Any]:
        """
        Asynchronously creates a receipt report.

        Args:
            data: Optional list of dictionaries containing additional data for the report.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload to include in the request.

        Returns:
            A dictionary containing the details of the created receipt report.

        Example:
            .. code-block:: python

                receipt_report = await client.extended_reports.create_receipt_report(data=[{"item": "example"}])
                print(receipt_report)

        Notes:
            - This method sends a POST request to create a receipt report asynchronously.
            - The `data` argument can be used to provide additional data required for generating the report.
            - Additional payload parameters can be passed as keyword arguments.
        """
        return await self.client(
            extended_reports.CreateReceiptReport(data=data, **payload),
            storage=storage,
        )

    async def get_report_task_by_id(
        self,
        report_task_id: Union[str, UUID],
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Asynchronously retrieves a specific report task by its ID.

        Args:
            report_task_id: The ID of the report task to retrieve.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the retrieved report task.

        Example:
            .. code-block:: python

                report_task = await client.extended_reports.get_report_task_by_id(
                    report_task_id="123e4567-e89b-12d3-a456-426614174000")
                print(report_task)

        Notes:
            - This method sends a GET request to retrieve the report task with the specified ID asynchronously.
        """
        return await self.client(
            extended_reports.GetReportTaskById(report_task_id=report_task_id),
            storage=storage,
        )

    async def report_xlsx_task_by_id(
        self,
        report_task_id: Union[str, UUID],
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Asynchronously retrieves the details of a specific report task by its ID, including the XLSX file if available.

        Args:
            report_task_id: The ID of the report task to retrieve. Can be a string or a UUID.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the report task and possibly the XLSX file.

        Example:
            .. code-block:: python

                report_task_details = await client.report_xlsx_task_by_id(
                    report_task_id="123e4567-e89b-12d3-a456-426614174000")
                print(report_task_details)

        Notes:
            - This method sends a GET request to asynchronously retrieve the details of the report task with the
              specified ID.
        """
        return await self.client(
            extended_reports.GetReportXlsxTaskById(report_task_id=report_task_id),
            storage=storage,
        )

    async def report_json_task_by_id(
        self,
        report_task_id: Union[str, UUID],
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Asynchronously retrieves the details of a specific report task by its ID, including the JSON file if available.

        Args:
            report_task_id: The ID of the report task to retrieve. Can be a string or a UUID.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the report task and possibly the JSON file.

        Example:
            .. code-block:: python

                report_task_details = await client.report_json_task_by_id(
                    report_task_id="123e4567-e89b-12d3-a456-426614174000")
                print(report_task_details)

        Notes:
            - This method sends a GET request to asynchronously retrieve the details of the report task with the
              specified ID.
        """
        return await self.client(
            extended_reports.GetReportJsonTaskById(report_task_id=report_task_id),
            storage=storage,
        )
