import logging
from typing import Optional, Union, Generator, AsyncGenerator, Dict, Any
from uuid import UUID

from checkbox_sdk.consts import DEFAULT_REQUESTS_RELAX
from checkbox_sdk.exceptions import StatusException
from checkbox_sdk.methods import goods
from checkbox_sdk.storage.simple import SessionStorage

logger = logging.getLogger(__name__)


class Goods:
    def __init__(self, client):
        self.client = client

    def get_goods(
        self,
        group_id: Optional[Union[str, UUID]] = None,
        without_group_only: Optional[bool] = False,
        query: Optional[str] = None,
        order_by_name: Optional[str] = None,
        order_by_code: Optional[str] = None,
        order_by_position: Optional[str] = None,
        load_children: Optional[bool] = False,
        storage: Optional[SessionStorage] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
    ) -> Generator:
        """
        Retrieves goods based on specified criteria.

        Args:
            group_id: The ID of the group to filter goods by.
            without_group_only: A flag indicating if only goods without a group should be included.
            query: A search query to filter goods.
            order_by_name: Criteria to order results by name.
            order_by_code: Criteria to order results by code.
            order_by_position: Criteria to order results by position.
            load_children: A flag indicating if children should be loaded.
            storage: An optional session storage to use for the operation.
            limit: The maximum number of results to return.
            offset: The offset for paginating results.

        Yields:
            Goods based on the specified criteria.

        Example:
            .. code-block:: python

                for good in client.goods.get_goods(group_id="123", query="item"):
                    print(good)

        Notes:
            - This method handles pagination automatically, continuing to fetch and yield goods until no more results
              are available.
        """
        goods_request = goods.GetGoods(
            group_id=group_id,
            without_group_only=without_group_only,
            query=query,
            order_by_name=order_by_name,
            order_by_code=order_by_code,
            order_by_position=order_by_position,
            load_children=load_children,
            limit=limit,
            offset=offset,
        )

        while True:
            goods_result = self.client(goods_request, storage=storage)
            results = goods_result.get("results", [])

            if not results:
                break

            yield from results
            goods_request.resolve_pagination(goods_result)
            goods_request.shift_next_page()

    def get_groups(
        self,
        search: Optional[str] = None,
        parent_groups_only: Optional[bool] = False,
        parent_id: Optional[str] = None,
        order_by_name: Optional[str] = None,
        order_by_created_at: Optional[str] = None,
        order_by_updated_at: Optional[str] = None,
        storage: Optional[SessionStorage] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
    ) -> Generator:
        """
        Retrieves groups based on specified criteria.

        Args:
            search: A search query to filter groups.
            parent_groups_only: A flag indicating if only parent groups should be included.
            parent_id: The ID of the parent group to filter by.
            order_by_name: Criteria to order results by name.
            order_by_created_at: Criteria to order results by creation date.
            order_by_updated_at: Criteria to order results by last update date.
            storage: An optional session storage to use for the operation.
            limit: The maximum number of results to return.
            offset: The offset for paginating results.

        Yields:
            Groups based on the specified criteria.

        Example:
            .. code-block:: python

                for group in client.goods.get_groups(search="Electronics"):
                    print(group)

        Notes:
            - This method handles pagination automatically, continuing to fetch and yield groups until no more results
              are available.
        """
        groups_request = goods.GetGroups(
            search=search,
            parent_groups_only=parent_groups_only,
            parent_id=parent_id,
            order_by_name=order_by_name,
            order_by_created_at=order_by_created_at,
            order_by_updated_at=order_by_updated_at,
            limit=limit,
            offset=offset,
        )

        while True:
            groups_result = self.client(groups_request, storage=storage)
            results = groups_result.get("results", [])

            if not results:
                break

            yield from results
            groups_request.resolve_pagination(groups_result)
            groups_request.shift_next_page()

    def get_good(
        self,
        good_id: Union[str, UUID],
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves a specific good based on its ID.

        Args:
            good_id: The ID of the good to retrieve.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the retrieved good.

        Example:
            .. code-block:: python

                good = client.goods.get_good(good_id="123e4567-e89b-12d3-a456-426614174000")
                print(good)

        Notes:
            - This method sends a GET request to retrieve the good with the specified ID.
        """
        return self.client(
            goods.GetGood(good_id=good_id),
            storage=storage,
        )

    def export_goods(
        self,
        export_extension: str,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
    ) -> Union[str | bytes]:
        """
        Exports goods data in the specified format.

        Args:
            export_extension: The format in which to export the goods data (e.g., "csv", "json").
            relax: The time to wait between checks while waiting for the export task to complete. Default is
                   `DEFAULT_REQUESTS_RELAX`.
            timeout: The maximum time to wait for the export task to complete. If `None`, it will wait indefinitely.
            storage: An optional session storage to use for the operation.

        Returns:
            The exported goods data as a string or bytes, depending on the format.

        Example:
            .. code-block:: python

                export_result = client.goods.export_goods(export_extension="csv")
                print(export_result)

        Notes:
            - This method sends a request to export the goods data in the specified format.
            - The method waits for the export task to complete before returning the exported data.
        """
        response = self.client(
            goods.ExportGoods(export_extension=export_extension),
            storage=storage,
        )

        logger.info("Trying to export goods with task %s", response["task_id"])
        return self._wait_export_task(response, export_extension, storage, relax, timeout)

    def _wait_export_task(
        self,
        task: Dict[str, Any],
        export_extension: str,
        storage: Optional[SessionStorage] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[float] = None,
    ) -> Union[str | bytes]:
        export_task = self.client.wait_status(
            goods.ExportGoodsTaskStatus(task_id=task["task_id"]),
            storage=storage,
            relax=relax,
            field="status",
            expected_value={"done", "error"},
            timeout=timeout,
        )
        if export_task["status"] == "error":
            error_messages = [
                f"Address: {error['address']}, Error: {error['error']}" for error in export_task.get("errors", [])
            ]
            error_details = "; ".join(error_messages) if error_messages else "Unknown error"
            raise StatusException(f"Export task failed with status 'error'. Details: {error_details}")

        return self.client(
            goods.ExportGoodsFile(task_id=task["task_id"], export_extension=export_extension),
            storage=storage,
        )

    def import_goods(
        self,
        file: str,
        ignore_barcode_duplicates: Optional[bool] = False,
        auto_supply: Optional[bool] = False,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Imports goods from a file.

        Args:
            file: The path to the file containing goods data to be imported.
            ignore_barcode_duplicates: A flag to indicate if barcode duplicates should be ignored. Default is `False`.
            auto_supply: A flag to indicate if auto supply should be enabled. Default is `False`.
            relax: The time to wait between checks while waiting for the import task to complete. Default is
                   `DEFAULT_REQUESTS_RELAX`.
            timeout: The maximum time to wait for the import task to complete. If `None`, it will wait indefinitely.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the result of the import operation.

        Example:
            .. code-block:: python

                result = client.goods.import_goods(file="/path/to/file.csv", ignore_barcode_duplicates=True)
                print(result)

        Notes:
            - This method sends a POST request to import goods from the specified file.
            - The method waits for the import task to complete before returning the result.
        """
        response = self.client(
            goods.ImportGoodsFromFile(
                file=file,
                ignore_barcode_duplicates=ignore_barcode_duplicates,
                auto_supply=auto_supply,
            ),
            storage=storage,
        )

        logger.info("Trying to import goods with task %s", response["task_id"])
        return self._wait_import_task(response, storage, relax, timeout)

    def _wait_import_task(
        self,
        task: Dict[str, Any],
        storage: Optional[SessionStorage] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        import_task = self.client.wait_status(
            goods.ImportGoodsTaskStatus(task_id=task["task_id"]),
            storage=storage,
            relax=relax,
            field="status",
            expected_value={"completed", "error"},
            timeout=timeout,
        )
        if import_task["status"] == "error":
            self._handle_error(import_task)

        self.client(
            goods.ImportGoodsApplyChanges(
                task_id=task["task_id"],
            ),
            storage=storage,
        )

        import_task = self.client.wait_status(
            goods.ImportGoodsTaskStatus(task_id=task["task_id"]),
            storage=storage,
            relax=relax,
            field="status",
            expected_value={"done", "error"},
            timeout=timeout,
        )
        if import_task["status"] == "error":
            self._handle_error(import_task)

        return import_task

    @staticmethod
    def _handle_error(import_task):
        error_messages = [
            f"Address: {error['address']}, Error: {error['error']}" for error in import_task.get("errors", [])
        ]
        error_details = "; ".join(error_messages) if error_messages else "Unknown error"
        raise StatusException(f"Import task failed with status 'error'. Details: {error_details}")


class AsyncGoods:
    def __init__(self, client):
        self.client = client

    async def get_goods(
        self,
        group_id: Optional[Union[str, UUID]] = None,
        without_group_only: Optional[bool] = False,
        query: Optional[str] = None,
        order_by_name: Optional[str] = None,
        order_by_code: Optional[str] = None,
        order_by_position: Optional[str] = None,
        load_children: Optional[bool] = False,
        storage: Optional[SessionStorage] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
    ) -> AsyncGenerator:
        """
        Asynchronously retrieves goods based on specified criteria.

        Args:
            group_id: The ID of the group to filter goods by.
            without_group_only: A flag indicating if only goods without a group should be included.
            query: A search query to filter goods.
            order_by_name: Criteria to order results by name.
            order_by_code: Criteria to order results by code.
            order_by_position: Criteria to order results by position.
            load_children: A flag indicating if children should be loaded.
            storage: An optional session storage to use for the operation.
            limit: The maximum number of results to return.
            offset: The offset for paginating results.

        Yields:
            Goods based on the specified criteria.

        Example:
            .. code-block:: python

                async for good in client.goods.get_goods(group_id="123", query="item"):
                    print(good)

        Notes:
            - This method handles pagination automatically, continuing to fetch and yield goods until no more results
              are available.
        """
        goods_request = goods.GetGoods(
            group_id=group_id,
            without_group_only=without_group_only,
            query=query,
            order_by_name=order_by_name,
            order_by_code=order_by_code,
            order_by_position=order_by_position,
            load_children=load_children,
            limit=limit,
            offset=offset,
        )

        while True:
            goods_result = await self.client(goods_request, storage=storage)
            results = goods_result.get("results", [])

            if not results:
                break

            for result in results:
                yield result

            goods_request.resolve_pagination(goods_result)
            goods_request.shift_next_page()

    async def get_groups(
        self,
        search: Optional[str] = None,
        parent_groups_only: Optional[bool] = False,
        parent_id: Optional[str] = None,
        order_by_name: Optional[str] = None,
        order_by_created_at: Optional[str] = None,
        order_by_updated_at: Optional[str] = None,
        storage: Optional[SessionStorage] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
    ) -> AsyncGenerator:
        """
        Asynchronously retrieves groups based on specified criteria.

        Args:
            search: A search query to filter groups.
            parent_groups_only: A flag indicating if only parent groups should be included.
            parent_id: The ID of the parent group to filter by.
            order_by_name: Criteria to order results by name.
            order_by_created_at: Criteria to order results by creation date.
            order_by_updated_at: Criteria to order results by last update date.
            storage: An optional session storage to use for the operation.
            limit: The maximum number of results to return.
            offset: The offset for paginating results.

        Yields:
            Groups based on the specified criteria.

        Example:
            .. code-block:: python

                async for group in client.goods.get_groups(search="Electronics"):
                    print(group)

        Notes:
            - This method handles pagination automatically, continuing to fetch and yield groups until no more results
              are available.
        """
        groups_request = goods.GetGroups(
            search=search,
            parent_groups_only=parent_groups_only,
            parent_id=parent_id,
            order_by_name=order_by_name,
            order_by_created_at=order_by_created_at,
            order_by_updated_at=order_by_updated_at,
            limit=limit,
            offset=offset,
        )

        while True:
            groups_result = await self.client(groups_request, storage=storage)
            results = groups_result.get("results", [])

            if not results:
                break

            for result in results:
                yield result

            groups_request.resolve_pagination(groups_result)
            groups_request.shift_next_page()

    async def get_good(
        self,
        good_id: Union[str, UUID],
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Asynchronously retrieves a specific good based on its ID.

        Args:
            good_id: The ID of the good to retrieve.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the retrieved good.

        Example:
            .. code-block:: python

                good = await client.goods.get_good(good_id="123e4567-e89b-12d3-a456-426614174000")
                print(good)

        Notes:
            - This method sends a GET request to retrieve the good with the specified ID asynchronously.
        """
        return await self.client(
            goods.GetGood(good_id=good_id),
            storage=storage,
        )

    async def export_goods(
        self,
        export_extension: str,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
    ) -> Union[str | bytes]:
        """
        Asynchronously exports goods data in the specified format.

        Args:
            export_extension: The format in which to export the goods data (e.g., "csv", "json").
            relax: The time to wait between checks while waiting for the export task to complete. Default
                   is `DEFAULT_REQUESTS_RELAX`.
            timeout: The maximum time to wait for the export task to complete. If `None`, it will wait indefinitely.
            storage: An optional session storage to use for the operation.

        Returns:
            The exported goods data as a string or bytes, depending on the format.

        Example:
            .. code-block:: python

                export_result = await client.goods.export_goods(export_extension="csv")
                print(export_result)

        Notes:
            - This method sends a request to export the goods data in the specified format asynchronously.
            - The method waits for the export task to complete before returning the exported data.
        """
        response = await self.client(
            goods.ExportGoods(export_extension=export_extension),
            storage=storage,
        )

        logger.info("Trying to export goods with task %s", response["task_id"])
        return await self._wait_export_task(response, export_extension, storage, relax, timeout)

    async def _wait_export_task(
        self,
        task: Dict[str, Any],
        export_extension: str,
        storage: Optional[SessionStorage] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[float] = None,
    ) -> Union[str | bytes]:
        export_task = await self.client.wait_status(
            goods.ExportGoodsTaskStatus(task_id=task["task_id"]),
            storage=storage,
            relax=relax,
            field="status",
            expected_value={"done", "error"},
            timeout=timeout,
        )
        if export_task["status"] == "error":
            error_messages = [
                f"Address: {error['address']}, Error: {error['error']}" for error in export_task.get("errors", [])
            ]
            error_details = "; ".join(error_messages) if error_messages else "Unknown error"
            raise StatusException(f"Export task failed with status 'error'. Details: {error_details}")

        return await self.client(
            goods.ExportGoodsFile(task_id=task["task_id"], export_extension=export_extension),
            storage=storage,
        )

    async def import_goods(
        self,
        file: str,
        ignore_barcode_duplicates: Optional[bool] = False,
        auto_supply: Optional[bool] = False,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Asynchronously imports goods from a file.

        Args:
            file: The path to the file containing goods data to be imported.
            ignore_barcode_duplicates: A flag to indicate if barcode duplicates should be ignored. Default is `False`.
            auto_supply: A flag to indicate if auto supply should be enabled. Default is `False`.
            relax: The time to wait between checks while waiting for the import task to complete. Default is
                   `DEFAULT_REQUESTS_RELAX`.
            timeout: The maximum time to wait for the import task to complete. If `None`, it will wait indefinitely.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the result of the import operation.

        Example:
            .. code-block:: python

                result = await client.goods.import_goods(file="/path/to/file.csv", ignore_barcode_duplicates=True)
                print(result)

        Notes:
            - This method sends a POST request to asynchronously import goods from the specified file.
            - The method waits for the import task to complete before returning the result.
        """
        response = await self.client(
            goods.ImportGoodsFromFile(
                file=file,
                ignore_barcode_duplicates=ignore_barcode_duplicates,
                auto_supply=auto_supply,
            ),
            storage=storage,
        )

        logger.info("Trying to import goods with task %s", response["task_id"])
        return await self._wait_import_task(response, storage, relax, timeout)

    async def _wait_import_task(
        self,
        task: Dict[str, Any],
        storage: Optional[SessionStorage] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        import_task = await self.client.wait_status(
            goods.ImportGoodsTaskStatus(task_id=task["task_id"]),
            storage=storage,
            relax=relax,
            field="status",
            expected_value={"completed", "error"},
            timeout=timeout,
        )
        if import_task["status"] == "error":
            self._handle_error(import_task)

        await self.client(
            goods.ImportGoodsApplyChanges(
                task_id=task["task_id"],
            ),
            storage=storage,
        )

        import_task = await self.client.wait_status(
            goods.ImportGoodsTaskStatus(task_id=task["task_id"]),
            storage=storage,
            relax=relax,
            field="status",
            expected_value={"done", "error"},
            timeout=timeout,
        )
        if import_task["status"] == "error":
            self._handle_error(import_task)

        return import_task

    @staticmethod
    def _handle_error(import_task):
        error_messages = [
            f"Address: {error['address']}, Error: {error['error']}" for error in import_task.get("errors", [])
        ]
        error_details = "; ".join(error_messages) if error_messages else "Unknown error"
        raise StatusException(f"Import task failed with status 'error'. Details: {error_details}")
