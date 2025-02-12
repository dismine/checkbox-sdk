import datetime
import logging
from typing import Optional, Union, Generator, AsyncGenerator, Dict, Any, List

from checkbox_sdk.client.api.base import AsyncPaginationMixin, PaginationMixin
from checkbox_sdk.client.api.receipts import check_status, check_status_async
from checkbox_sdk.consts import DEFAULT_REQUESTS_RELAX
from checkbox_sdk.methods import prepayment_receipts
from checkbox_sdk.storage.simple import SessionStorage

logger = logging.getLogger(__name__)


class PrepaymentReceipts(PaginationMixin):
    def get_pre_payment_relations_search(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        desc: Optional[bool] = False,
        search: Optional[str] = None,
        cash_register_id: Optional[Union[datetime.datetime, str]] = None,
        status: Optional[str] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
        storage: Optional[SessionStorage] = None,
    ) -> Generator:
        """
        Retrieves prepayment receipts based on search criteria.

        Args:
            from_date: The start date for the search.
            to_date: The end date for the search.
            desc: A flag to indicate descending order.
            search: A string to search within the receipts.
            cash_register_id: The ID of the cash register.
            status: The status of the receipts.
            limit: The maximum number of results to return.
            offset: The offset for paginating results.
            storage: An optional session storage to use for the operation.

        Yields:
            Results of prepayment receipts based on the search criteria.

        """
        get_receipts = prepayment_receipts.GetPrepaymentReceipts(
            from_date=from_date,
            to_date=to_date,
            desc=desc,
            search=search,
            cash_register_id=cash_register_id,
            status=status,
            limit=limit,
            offset=offset,
        )
        yield from self.fetch_paginated_results(get_receipts, storage=storage)

    def get_prepayment_relation(
        self,
        relation_id: str,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves a specific prepayment relation by its ID.

        Args:
            relation_id: The ID of the prepayment relation to retrieve.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the prepayment relation.

        """
        return self.client(
            prepayment_receipts.GetPrepaymentRelation(relation_id=relation_id),
            storage=storage,
        )

    def create_after_payment_receipt(  # pylint: disable=too-many-positional-arguments
        self,
        relation_id: str,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates an after payment receipt for a specific relation.

        Args:
            relation_id: The ID of the relation for which the receipt is created.
            receipt: Additional details for the receipt.
            relax: The relaxation factor for requests.
            timeout: The timeout for the request.
            storage: An optional session storage to use for the operation.
            wait: A flag indicating whether to wait for the operation to complete.
            **payload: Additional payload for the request.

        Returns:
            A dictionary containing the details of the created after payment receipt.

        """
        response = self.client(
            prepayment_receipts.CreateAfterPaymentReceipt(relation_id, receipt=receipt, **payload),
            storage=storage,
        )
        logger.info("Trying create after payment receipt %s", response["id"])
        if not wait:
            return response

        return check_status(self.client, response, storage, relax, timeout)

    def create_prepayment_receipt(  # pylint: disable=too-many-positional-arguments
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates a prepayment receipt.

        Args:
            receipt: Additional details for the receipt.
            relax: The relaxation factor for requests.
            timeout: The timeout for the request.
            storage: An optional session storage to use for the operation.
            wait: A flag indicating whether to wait for the operation to complete.
            **payload: Additional payload for the request.

        Returns:
            A dictionary containing the details of the created prepayment receipt.

        """
        response = self.client(
            prepayment_receipts.CreatePrepaymentReceipt(receipt=receipt, **payload),
            storage=storage,
        )
        logger.info("Trying create prepayment receipt %s", response["id"])
        if not wait:
            return response

        return check_status(self.client, response, storage, relax, timeout)

    def get_prepayment_receipts_chain(
        self,
        relation_id: str,
        data: Optional[Dict] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> List[Dict[str, Any]]:
        """
        Retrieves a chain of after payment and prepayment receipts.

        Args:
            relation_id: The ID of the relation for which the chain is retrieved.
            data: Additional data for the request.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload for the request.

        Returns:
            A list of dictionaries containing details of the prepayment receipts chain.

        """
        return self.client(
            prepayment_receipts.GetPrepaymentReceiptsChain(relation_id=relation_id, data=data, **payload),
            storage=storage,
        )


class AsyncPrepaymentReceipts(AsyncPaginationMixin):
    async def get_pre_payment_relations_search(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        from_date: Optional[Union[datetime.datetime, str]] = None,
        to_date: Optional[Union[datetime.datetime, str]] = None,
        desc: Optional[bool] = False,
        search: Optional[str] = None,
        cash_register_id: Optional[Union[datetime.datetime, str]] = None,
        status: Optional[str] = None,
        limit: Optional[int] = 25,
        offset: Optional[int] = 0,
        storage: Optional[SessionStorage] = None,
    ) -> AsyncGenerator:
        """
        Retrieves prepayment receipts based on search criteria.

        Args:
            from_date: The start date for the search.
            to_date: The end date for the search.
            desc: A flag to indicate descending order.
            search: A string to search within the receipts.
            cash_register_id: The ID of the cash register.
            status: The status of the receipts.
            limit: The maximum number of results to return.
            offset: The offset for paginating results.
            storage: An optional session storage to use for the operation.

        Yields:
            Results of prepayment receipts based on the search criteria.

        """
        get_receipts = prepayment_receipts.GetPrepaymentReceipts(
            from_date=from_date,
            to_date=to_date,
            desc=desc,
            search=search,
            cash_register_id=cash_register_id,
            status=status,
            limit=limit,
            offset=offset,
        )

        async for result in self.fetch_paginated_results(get_receipts, storage=storage):
            yield result

    async def get_prepayment_relation(
        self,
        relation_id: str,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves details of a specific prepayment relation.

        Args:
            relation_id: The ID of the prepayment relation to retrieve.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the prepayment relation.

        """
        return await self.client(
            prepayment_receipts.GetPrepaymentRelation(relation_id=relation_id),
            storage=storage,
        )

    async def create_after_payment_receipt(  # pylint: disable=too-many-positional-arguments
        self,
        relation_id: str,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates an after payment receipt for a specific relation.

        Args:
            relation_id: The ID of the relation for which the receipt is created.
            receipt: Additional details for the receipt.
            relax: The relaxation factor for requests.
            timeout: The timeout for the request.
            storage: An optional session storage to use for the operation.
            wait: A flag indicating whether to wait for the operation to complete.
            **payload: Additional payload for the request.

        Returns:
            A dictionary containing the details of the created after payment receipt.

        """
        response = await self.client(
            prepayment_receipts.CreateAfterPaymentReceipt(relation_id, receipt=receipt, **payload),
            storage=storage,
        )
        logger.info("Trying create after payment receipt %s", response["id"])
        if not wait:
            return response

        return await check_status_async(self.client, response, storage, relax, timeout)

    async def create_prepayment_receipt(  # pylint: disable=too-many-positional-arguments
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates a prepayment receipt.

        Args:
            receipt: Additional details for the receipt.
            relax: The relaxation factor for requests.
            timeout: The timeout for the request.
            storage: An optional session storage to use for the operation.
            wait: A flag indicating whether to wait for the operation to complete.
            **payload: Additional payload for the request.

        Returns:
            A dictionary containing the details of the created prepayment receipt.

        """
        response = await self.client(
            prepayment_receipts.CreatePrepaymentReceipt(receipt=receipt, **payload),
            storage=storage,
        )
        logger.info("Trying create prepayment receipt %s", response["id"])
        if not wait:
            return response

        return await check_status_async(self.client, response, storage, relax, timeout)

    async def get_prepayment_receipts_chain(
        self,
        relation_id: str,
        data: Optional[Dict] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> List[Dict[str, Any]]:
        """
        Retrieves a chain of after payment and prepayment receipts.

        Args:
            relation_id: The ID of the relation for which the chain is retrieved.
            data: Additional data for the request.
            storage: An optional session storage to use for the operation.
            **payload: Additional payload for the request.

        Returns:
            A list of dictionaries containing details of the prepayment receipts chain.

        """
        return await self.client(
            prepayment_receipts.GetPrepaymentReceiptsChain(relation_id=relation_id, data=data, **payload),
            storage=storage,
        )
