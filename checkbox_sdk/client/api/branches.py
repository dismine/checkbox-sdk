from typing import Optional, Generator, AsyncGenerator

from checkbox_sdk.client.api.base import AsyncPaginationMixin, PaginationMixin
from checkbox_sdk.methods import branches
from checkbox_sdk.storage.simple import SessionStorage


class Branches(PaginationMixin):
    def get_all_branches(
        self, limit: int = 25, offset: int = 0, storage: Optional[SessionStorage] = None
    ) -> Generator:
        """
        Retrieves all branches from the system with pagination support.

        Args:
            limit: The number of branches to retrieve per page.
            offset: The starting point for retrieving branches.
            storage: Optional session storage to use for the request.

        Yields:
            Dictionaries, each containing details of a branch.

        Example:
            .. code-block:: python

                for branch in client.branches.get_all_branches():
                    print(branch)

        Notes:
            - This method handles pagination to retrieve all branches.
            - It yields branches one by one.
        """
        get_branches = branches.GetAllBranches(limit=limit, offset=offset)
        yield from self.fetch_paginated_results(get_branches, storage=storage)


class AsyncBranches(AsyncPaginationMixin):
    async def get_all_branches(
        self, limit: int = 25, offset: int = 0, storage: Optional[SessionStorage] = None
    ) -> AsyncGenerator:
        """
        Asynchronously retrieves all branches from the system with pagination support.

        Args:
            limit: The number of branches to retrieve per page.
            offset: The starting point for retrieving branches.
            storage: Optional session storage to use for the request.

        Yields:
            Dictionaries, each containing details of a branch.

        Example:
            .. code-block:: python

                async for branch in client.branches.get_all_branches():
                    print(branch)

        Notes:
            - This method handles pagination to retrieve all branches.
            - It yields branches one by one.
        """
        get_branches = branches.GetAllBranches(limit=limit, offset=offset)

        async for result in self.fetch_paginated_results(get_branches, storage=storage):
            yield result
