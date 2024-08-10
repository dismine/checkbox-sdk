import datetime
import logging
from typing import Optional, Union, Generator, AsyncGenerator, Dict, Any, List

from checkbox_sdk.consts import DEFAULT_REQUESTS_RELAX
from checkbox_sdk.exceptions import StatusException
from checkbox_sdk.methods import prepayment_receipts, receipts
from checkbox_sdk.storage.simple import SessionStorage

logger = logging.getLogger(__name__)


class PrepaymentReceipts:
    def __init__(self, client):
        self.client = client

    def get_pre_payment_relations_search(
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
        while (receipts_result := self.client(get_receipts, storage=storage))["results"]:
            get_receipts.resolve_pagination(receipts_result).shift_next_page()
            yield from receipts_result["results"]

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

    def create_after_payment_receipt(
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

        return self._check_status(response, storage, relax, timeout)

    def create_prepayment_receipt(
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

        return self._check_status(response, storage, relax, timeout)

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


class AsyncPrepaymentReceipts:
    def __init__(self, client):
        self.client = client

    async def get_pre_payment_relations_search(
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

        while True:
            receipts_result = await self.client(get_receipts, storage=storage)
            results = receipts_result.get("results", [])

            if not results:
                break

            for result in results:
                yield result

            get_receipts.resolve_pagination(receipts_result)
            get_receipts.shift_next_page()

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

    async def create_after_payment_receipt(
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

        return await self._check_status(response, storage, relax, timeout)

    async def create_prepayment_receipt(
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

        return await self._check_status(response, storage, relax, timeout)

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
