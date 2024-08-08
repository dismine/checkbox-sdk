import datetime
import logging
from typing import Any, Dict, List, Optional, Generator, Union, AsyncGenerator
from uuid import UUID

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

    def create_bulk_receipts(
        self,
        receipt_list: Optional[List[Dict]] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> List[Dict[str, str]]:
        """
        Creates multiple receipts in bulk using the provided receipt list and options.

        Args:
            receipt_list: An optional list of dictionaries representing the receipts to create.
            storage: An optional session storage to use for the operation.
            **payload: Additional keyword arguments for creating the receipts.

        Returns:
            A list of dictionaries containing the results of the created receipts.

        """
        response = self.client(
            receipts.CreateBulkReceipts(receipts=receipt_list, **payload),
            storage=storage,
        )

        return response["results"]

    def create_receipt_offline(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates a receipt offline with the provided data and options.

        Args:
            receipt: An optional dictionary representing the receipt data.
            relax: The relaxation factor for requests.
            timeout: The timeout duration for the operation.
            storage: An optional session storage to use for the operation.
            wait: A boolean indicating whether to wait for the operation to complete.
            **payload: Additional keyword arguments for creating the receipt.

        Returns:
            A dictionary containing the response of the created receipt.

        """
        response = self.client(
            receipts.CreateReceiptOffline(receipt=receipt, **payload),
            storage=storage,
            # request_timeout=timeout,
        )
        logger.info("Trying create receipt %s", response["id"])
        if not wait:
            return response

        return self._check_status(response, storage, relax, timeout)

    def create_external_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates an external receipt with the provided data and options.

        This function adds a receipt created in an external system offline, based on the full information about the
        receipt. The external system handles all calculations and the transactional processing saves and sends the
        receipt to the State Tax Service without further analysis.

        Args:
            receipt: An optional dictionary representing the external receipt data.
            relax: The relaxation factor for requests.
            timeout: The timeout duration for the operation.
            storage: An optional session storage to use for the operation.
            wait: A boolean indicating whether to wait for the operation to complete.
            **payload: Additional keyword arguments for creating the external receipt.

        Returns:
            A dictionary containing the response of the created external receipt.

        """
        response = self.client(receipts.AddExternal(receipt, **payload), storage=storage)
        logger.info("Trying to create external receipt %s", response["id"])
        if not wait:
            return response

        return self._check_status(response, storage, relax, timeout)

    def create_service_currency_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates a service currency receipt using the provided data and options.

        Create a service receipt for depositing or withdrawing funds. It is intended for currency exchange offices only.

        Args:
            receipt: Optional dictionary containing the receipt data.
            relax: The relaxation factor for requests.
            timeout: The timeout duration for the operation.
            storage: Optional session storage to use for the operation.
            wait: A boolean indicating whether to wait for the operation to complete.
            **payload: Additional keyword arguments for creating the service currency receipt.

        Returns:
            A dictionary containing the response of the created service currency receipt.

        """
        response = self.client(receipts.ServiceCurrency(receipt, **payload), storage=storage)
        logger.info("Trying to create service currency receipt %s", response["id"])
        if not wait:
            return response

        return self._check_status(response, storage, relax, timeout)

    def create_currency_exchange_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates a currency exchange receipt using the provided data and options.

        Creation of a currency exchange receipt is available only for the respective type of cash registers.

        Args:
            receipt: Optional dictionary containing the receipt data.
            relax: The relaxation factor for requests.
            timeout: The timeout duration for the operation.
            storage: Optional session storage to use for the operation.
            wait: A boolean indicating whether to wait for the operation to complete.
            **payload: Additional keyword arguments for creating the currency exchange receipt.

        Returns:
            A dictionary containing the response of the created currency exchange receipt.

        """
        response = self.client(receipts.CurrencyExchange(receipt, **payload), storage=storage)
        logger.info("Trying to create currency exchange receipt %s", response["id"])
        if not wait:
            return response

        return self._check_status(response, storage, relax, timeout)

    def create_cash_withdrawal_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates a cash withdrawal receipt using the provided data and options.

        Args:
            receipt: Optional dictionary containing the receipt data.
            relax: The relaxation factor for requests.
            timeout: The timeout duration for the operation.
            storage: Optional session storage to use for the operation.
            wait: A boolean indicating whether to wait for the operation to complete.
            **payload: Additional keyword arguments for creating the cash withdrawal receipt.

        Returns:
            A dictionary containing the response of the created cash withdrawal receipt.

        """
        response = self.client(receipts.CreateCashWithdrawalReceipt(receipt, **payload), storage=storage)
        logger.info("Trying to create cash withdrawal receipt %s", response["id"])
        if not wait:
            return response

        return self._check_status(response, storage, relax, timeout)

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
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates a service receipt about depositing change to the cash register or cash collection and checks its status.

        Args:
            receipt (Optional[Dict[str, Any]): A dictionary containing receipt information.
            relax: A float indicating the relaxation factor.
            timeout: An optional float for request timeout.
            storage: An optional SessionStorage object.
            wait: A boolean indicating whether to wait for the operation to complete.
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
        if not wait:
            return response

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

    def get_receipt_visualization_html(
        self,
        receipt_id: Union[str, UUID],
        is_second_copy: Optional[bool] = False,
        simple: Optional[bool] = False,
        show_buttons: Optional[bool] = None,
        x_show_buttons: Optional[bool] = None,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Retrieves the HTML visualization of a receipt.

        Args:
            receipt_id: The ID of the receipt to visualize.
            is_second_copy: A flag indicating if it is a second copy of the receipt.
            simple: A flag indicating if the visualization should be simplified.
            show_buttons: A flag to show buttons in the visualization.
            x_show_buttons: A flag to show additional buttons in the visualization.
            storage: An optional session storage to use for the operation.

        Returns:
            A string containing the HTML visualization of the receipt.
        """
        return self.client(
            receipts.GetReceiptVisualizationHtml(
                receipt_id=receipt_id,
                is_second_copy=is_second_copy,
                simple=simple,
                show_buttons=show_buttons,
                x_show_buttons=x_show_buttons,
            ),
            storage=storage,
        )

    def get_receipt_visualization_pdf(
        self,
        receipt_id: Union[str, UUID],
        is_second_copy: Optional[bool] = False,
        download: Optional[bool] = False,
        storage: Optional[SessionStorage] = None,
    ) -> bytes:
        """
        Retrieves the PDF visualization of a receipt for download.

        Args:
            receipt_id: The ID of the receipt to visualize.
            is_second_copy: A flag indicating if it is a second copy of the receipt.
            download: A flag indicating if the PDF should be downloaded.
            storage: An optional session storage to use for the operation.

        Returns:
            A bytes object containing the PDF visualization of the receipt.

        """
        return self.client(
            receipts.GetReceiptVisualizationPdf(
                receipt_id=receipt_id,
                is_second_copy=is_second_copy,
                download=download,
            ),
            storage=storage,
        )

    def get_receipt_visualization_text(
        self,
        receipt_id: Union[str, UUID],
        is_second_copy: Optional[bool] = False,
        width: Optional[int] = 42,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Retrieves the text visualization of a receipt.

        Args:
            receipt_id: The ID of the receipt to visualize.
            is_second_copy: A flag indicating if it is a second copy of the receipt.
            width: The width of the text visualization.
            storage: An optional session storage to use for the operation.

        Returns:
            A string containing the text visualization of the receipt.

        """
        return self.client(
            receipts.GetReceiptVisualizationText(
                receipt_id=receipt_id,
                is_second_copy=is_second_copy,
                width=width,
            ),
            storage=storage,
        )

    def get_receipt_visualization_png(
        self,
        receipt_id: Union[str, UUID],
        is_second_copy: Optional[bool] = False,
        width: Optional[int] = 30,
        paper_width: Optional[int] = 58,
        qrcode_scale: Optional[int] = 75,
        storage: Optional[SessionStorage] = None,
    ) -> bytes:
        """
        Retrieves the PNG visualization of a receipt.

        Args:
            receipt_id: The ID of the receipt to visualize.
            is_second_copy: A flag indicating if it is a second copy of the receipt.
            width: The width of the PNG visualization.
            paper_width: The width of the paper for the visualization.
            qrcode_scale: The scale of the QR code in the visualization.
            storage: An optional session storage to use for the operation.

        Returns:
            A bytes object containing the PNG visualization of the receipt.

        """
        return self.client(
            receipts.GetReceiptVisualizationPng(
                receipt_id=receipt_id,
                is_second_copy=is_second_copy,
                width=width,
                paper_width=paper_width,
                qrcode_scale=qrcode_scale,
            ),
            storage=storage,
        )

    def get_receipt_visualization_qrcode(
        self,
        receipt_id: Union[str, UUID],
        storage: Optional[SessionStorage] = None,
    ) -> bytes:
        """
        Retrieves the QR code visualization of a receipt.

        Args:
            receipt_id: The ID of the receipt to visualize.
            storage: An optional session storage to use for the operation.

        Returns:
            A bytes object containing the QR code visualization of the receipt.

        """
        return self.client(
            receipts.GetReceiptVisualizationQrCode(
                receipt_id=receipt_id,
            ),
            storage=storage,
        )

    def get_receipt_visualization_xml(
        self,
        receipt_id: Union[str, UUID],
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Retrieves the XML visualization of a receipt.

        Args:
            receipt_id: The ID of the receipt to visualize.
            storage: An optional session storage to use for the operation.

        Returns:
            A string containing the XML visualization of the receipt.

        """
        return self.client(
            receipts.GetReceiptVisualizationXml(
                receipt_id=receipt_id,
            ),
            storage=storage,
        )

    def send_receipt_to_email(
        self,
        receipt_id: Union[str, UUID],
        email: str,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Sends a receipt to the specified email address.

        Args:
            receipt_id: The ID of the receipt to send.
            email: The email address to send the receipt to.
            storage: An optional session storage to use for the operation.

        Returns:
            A string indicating the status of the email sending process.

        """
        return self.client(
            receipts.SendEmail(
                receipt_id=receipt_id,
                email=email,
            ),
            storage=storage,
        )

    def send_receipt_via_sms(
        self,
        receipt_id: Union[str, UUID],
        phone: str,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Sends a receipt via SMS to the specified phone number.

        Args:
            receipt_id: The ID of the receipt to send.
            phone: The phone number to send the receipt to.
            storage: An optional session storage to use for the operation.

        Returns:
            A string indicating the status of the SMS sending process.

        """
        return self.client(
            receipts.SendSMS(
                receipt_id=receipt_id,
                phone=phone,
            ),
            storage=storage,
        )


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
        Asynchronously creates a receipt and optionally waits for its status.

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

    async def create_bulk_receipts(
        self,
        receipt_list: Optional[List[Dict]] = None,
        storage: Optional[SessionStorage] = None,
        **payload,
    ) -> List[Dict[str, str]]:
        """
        Asynchronously creates multiple receipts in bulk using the provided receipt list and options.

        Args:
            receipt_list: An optional list of dictionaries representing the receipts to create.
            storage: An optional session storage to use for the operation.
            **payload: Additional keyword arguments for creating the receipts.

        Returns:
            A list of dictionaries containing the results of the created receipts.

        """
        response = await self.client(
            receipts.CreateBulkReceipts(receipts=receipt_list, **payload),
            storage=storage,
        )

        return response["results"]

    async def create_receipt_offline(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Asynchronously creates a receipt offline with the provided data and options.

        Args:
            receipt: An optional dictionary representing the receipt data.
            relax: The relaxation factor for requests.
            timeout: The timeout duration for the operation.
            storage: An optional session storage to use for the operation.
            wait: A boolean indicating whether to wait for the operation to complete.
            **payload: Additional keyword arguments for creating the receipt.

        Returns:
            A dictionary containing the response of the created receipt.

        """
        response = await self.client(
            receipts.CreateReceiptOffline(receipt=receipt, **payload),
            storage=storage,
            # request_timeout=timeout,
        )
        logger.info("Trying create receipt %s", response["id"])
        if not wait:
            return response

        return await self._check_status(response, storage, relax, timeout)

    async def create_external_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Asynchronously creates an external receipt using the provided data and options.

        This function adds a receipt created in an external system offline, based on the full information about the
        receipt. The external system handles all calculations and the transactional processing saves and sends the
        receipt to the State Tax Service without further analysis.

        Args:
            receipt: Optional dictionary containing the receipt data.
            relax: The relaxation factor for requests.
            timeout: The timeout duration for the operation.
            storage: Optional session storage to use for the operation.
            wait: A boolean indicating whether to wait for the operation to complete.
            **payload: Additional keyword arguments for creating the external receipt.

        Returns:
            A dictionary containing the response of the created external receipt.

        """
        response = await self.client(receipts.AddExternal(receipt, **payload), storage=storage)
        logger.info("Trying to create external receipt %s", response["id"])
        if not wait:
            return response

        return await self._check_status(response, storage, relax, timeout)

    async def create_service_currency_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Asynchronously creates a service currency receipt using the provided data and options.

        Create a service receipt for depositing or withdrawing funds. It is intended for currency exchange offices only.

        Args:
            receipt: Optional dictionary containing the receipt data.
            relax: The relaxation factor for requests.
            timeout: The timeout duration for the operation.
            storage: Optional session storage to use for the operation.
            wait: A boolean indicating whether to wait for the operation to complete.
            **payload: Additional keyword arguments for creating the service currency receipt.

        Returns:
            A dictionary containing the response of the created service currency receipt.

        """
        response = await self.client(receipts.ServiceCurrency(receipt, **payload), storage=storage)
        logger.info("Trying to create service currency receipt %s", response["id"])
        if not wait:
            return response

        return await self._check_status(response, storage, relax, timeout)

    async def create_currency_exchange_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Asynchronously creates a currency exchange receipt using the provided data and options.

        Creation of a currency exchange receipt is available only for the respective type of cash registers.

        Args:
            receipt: Optional dictionary containing the receipt data.
            relax: The relaxation factor for requests.
            timeout: The timeout duration for the operation.
            storage: Optional session storage to use for the operation.
            wait: A boolean indicating whether to wait for the operation to complete.
            **payload: Additional keyword arguments for creating the currency exchange receipt.

        Returns:
            A dictionary containing the response of the created currency exchange receipt.

        """
        response = await self.client(receipts.CurrencyExchange(receipt, **payload), storage=storage)
        logger.info("Trying to create currency exchange receipt %s", response["id"])
        if not wait:
            return response

        return await self._check_status(response, storage, relax, timeout)

    async def create_cash_withdrawal_receipt(
        self,
        receipt: Optional[Dict[str, Any]] = None,
        relax: float = DEFAULT_REQUESTS_RELAX,
        timeout: Optional[int] = None,
        storage: Optional[SessionStorage] = None,
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Asynchronously creates a cash withdrawal receipt using the provided data and options.

        Args:
            receipt: Optional dictionary containing the receipt data.
            relax: The relaxation factor for requests.
            timeout: The timeout duration for the operation.
            storage: Optional session storage to use for the operation.
            wait: A boolean indicating whether to wait for the operation to complete.
            **payload: Additional keyword arguments for creating the cash withdrawal receipt.

        Returns:
            A dictionary containing the response of the created cash withdrawal receipt.

        """
        response = await self.client(receipts.CreateCashWithdrawalReceipt(receipt, **payload), storage=storage)
        logger.info("Trying to create cash withdrawal receipt %s", response["id"])
        if not wait:
            return response

        return await self._check_status(response, storage, relax, timeout)

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
        wait: bool = True,
        **payload,
    ) -> Dict[str, Any]:
        """
        Creates a service receipt about depositing change to the cash register or cash collection and checks its status.

        Args:
            receipt (Optional[Dict[str, Any]): A dictionary containing receipt information.
            relax: A float indicating the relaxation factor.
            timeout: An optional float for request timeout.
            storage: An optional SessionStorage object.
            wait: A boolean indicating whether to wait for the operation to complete.
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
        if not wait:
            return response

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

    async def get_receipt_visualization_html(
        self,
        receipt_id: Union[str, UUID],
        is_second_copy: Optional[bool] = False,
        simple: Optional[bool] = False,
        show_buttons: Optional[bool] = None,
        x_show_buttons: Optional[bool] = None,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Retrieves the HTML visualization of a receipt for display.

        Args:
            receipt_id: The ID of the receipt to visualize.
            is_second_copy: A flag indicating if it is a second copy of the receipt.
            simple: A flag indicating if the visualization should be simplified.
            show_buttons: A flag to show buttons in the visualization.
            x_show_buttons: A flag to show additional buttons in the visualization.
            storage: An optional session storage to use for the operation.

        Returns:
            A string containing the HTML visualization of the receipt.

        """
        return await self.client(
            receipts.GetReceiptVisualizationHtml(
                receipt_id=receipt_id,
                is_second_copy=is_second_copy,
                simple=simple,
                show_buttons=show_buttons,
                x_show_buttons=x_show_buttons,
            ),
            storage=storage,
        )

    async def get_receipt_visualization_pdf(
        self,
        receipt_id: Union[str, UUID],
        is_second_copy: Optional[bool] = False,
        download: Optional[bool] = False,
        storage: Optional[SessionStorage] = None,
    ) -> bytes:
        """
        Retrieves the PDF visualization of a receipt for download.

        Args:
            receipt_id: The ID of the receipt to visualize.
            is_second_copy: A flag indicating if it is a second copy of the receipt.
            download: A flag indicating if the PDF should be downloaded.
            storage: An optional session storage to use for the operation.

        Returns:
            A bytes object containing the PDF visualization of the receipt.

        """
        return await self.client(
            receipts.GetReceiptVisualizationPdf(
                receipt_id=receipt_id,
                is_second_copy=is_second_copy,
                download=download,
            ),
            storage=storage,
        )

    async def get_receipt_visualization_text(
        self,
        receipt_id: Union[str, UUID],
        is_second_copy: Optional[bool] = False,
        width: Optional[int] = 42,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Retrieves the text visualization of a receipt.

        Args:
            receipt_id: The ID of the receipt to visualize.
            is_second_copy: A flag indicating if it is a second copy of the receipt.
            width: The width of the text visualization.
            storage: An optional session storage to use for the operation.

        Returns:
            A string containing the text visualization of the receipt.

        """
        return await self.client(
            receipts.GetReceiptVisualizationText(
                receipt_id=receipt_id,
                is_second_copy=is_second_copy,
                width=width,
            ),
            storage=storage,
        )

    async def get_receipt_visualization_png(
        self,
        receipt_id: Union[str, UUID],
        is_second_copy: Optional[bool] = False,
        width: Optional[int] = 30,
        paper_width: Optional[int] = 58,
        qrcode_scale: Optional[int] = 75,
        storage: Optional[SessionStorage] = None,
    ) -> bytes:
        """
        Retrieves the PNG visualization of a receipt.

        Args:
            receipt_id: The ID of the receipt to visualize.
            is_second_copy: A flag indicating if it is a second copy of the receipt.
            width: The width of the PNG visualization.
            paper_width: The width of the paper for the visualization.
            qrcode_scale: The scale of the QR code in the visualization.
            storage: An optional session storage to use for the operation.

        Returns:
            A bytes object containing the PNG visualization of the receipt.

        """
        return await self.client(
            receipts.GetReceiptVisualizationPng(
                receipt_id=receipt_id,
                is_second_copy=is_second_copy,
                width=width,
                paper_width=paper_width,
                qrcode_scale=qrcode_scale,
            ),
            storage=storage,
        )

    async def get_receipt_visualization_qrcode(
        self,
        receipt_id: Union[str, UUID],
        storage: Optional[SessionStorage] = None,
    ) -> bytes:
        """
        Retrieves the QR code visualization of a receipt.

        Args:
            receipt_id: The ID of the receipt to visualize.
            storage: An optional session storage to use for the operation.

        Returns:
            A bytes object containing the QR code visualization of the receipt.

        """
        return await self.client(
            receipts.GetReceiptVisualizationQrCode(
                receipt_id=receipt_id,
            ),
            storage=storage,
        )

    async def get_receipt_visualization_xml(
        self,
        receipt_id: Union[str, UUID],
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Retrieves the XML visualization of a receipt.

        Args:
            receipt_id: The ID of the receipt to visualize.
            storage: An optional session storage to use for the operation.

        Returns:
            A string containing the XML visualization of the receipt.

        """
        return await self.client(
            receipts.GetReceiptVisualizationXml(
                receipt_id=receipt_id,
            ),
            storage=storage,
        )

    async def send_receipt_to_email(
        self,
        receipt_id: Union[str, UUID],
        email: str,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Sends a receipt to the specified email address.

        Args:
            receipt_id: The ID of the receipt to send.
            email: The email address to send the receipt to.
            storage: An optional session storage to use for the operation.

        Returns:
            A string indicating the status of the email sending process.

        """
        return await self.client(
            receipts.SendEmail(
                receipt_id=receipt_id,
                email=email,
            ),
            storage=storage,
        )

    async def send_receipt_via_sms(
        self,
        receipt_id: Union[str, UUID],
        phone: str,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Sends a receipt via SMS to the specified phone number.

        Args:
            receipt_id: The ID of the receipt to send.
            phone: The phone number to send the receipt to.
            storage: An optional session storage to use for the operation.

        Returns:
            A string indicating the status of the SMS sending process.

        """
        return await self.client(
            receipts.SendSMS(
                receipt_id=receipt_id,
                phone=phone,
            ),
            storage=storage,
        )
