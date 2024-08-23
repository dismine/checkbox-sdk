from typing import Optional, AsyncGenerator, Generator

from checkbox_sdk.methods.base import AbstractMethod
from checkbox_sdk.storage.simple import SessionStorage


class PaginationMixin:  # pylint: disable=too-few-public-methods
    def __init__(self, client):
        self.client = client

    def fetch_paginated_results(
        self, request_obj: AbstractMethod, storage: Optional[SessionStorage] = None
    ) -> Generator:
        """
        Generic method to handle fetching and yielding paginated results synchronously.

        Args:
            request_obj (AbstractMethod): The request object for fetching results.
            storage (Optional[SessionStorage]): Optional session storage to use.

        Yields:
            Dict[str, Any]: A dictionary representing each result.
        """
        while True:
            transactions_result = self.client(request_obj, storage=storage)
            results = transactions_result.get("results", [])

            if not results:
                break

            yield from results
            request_obj.resolve_pagination(transactions_result)  # type: ignore[attr-defined]
            request_obj.shift_next_page()  # type: ignore[attr-defined]


class AsyncPaginationMixin:  # pylint: disable=too-few-public-methods
    def __init__(self, client):
        self.client = client

    async def fetch_paginated_results(
        self, request_obj: AbstractMethod, storage: Optional[SessionStorage] = None
    ) -> AsyncGenerator:
        """
        Generic method to handle fetching and yielding paginated results.

        Args:
            request_obj (AbstractMethod): The request object for fetching results.
            storage (Optional[SessionStorage]): Optional session storage to use.

        Yields:
            Dict[str, Any]: A dictionary representing each result.
        """
        while True:
            result = await self.client(request_obj, storage=storage)
            results = result.get("results", [])

            if not results:
                break

            for item in results:
                yield item

            request_obj.resolve_pagination(result)  # type: ignore[attr-defined]
            request_obj.shift_next_page()  # type: ignore[attr-defined]
