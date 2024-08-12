from typing import Optional, Generator, AsyncGenerator

from checkbox_sdk.methods import branches
from checkbox_sdk.storage.simple import SessionStorage


class Branches:
    def __init__(self, client):
        self.client = client

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
        while (shifts_result := self.client(get_branches, storage=storage))["results"]:
            get_branches.resolve_pagination(shifts_result).shift_next_page()
            yield from shifts_result["results"]


class AsyncBranches:
    def __init__(self, client):
        self.client = client

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
        while True:
            shifts_result = await self.client(get_branches, storage=storage)
            results = shifts_result.get("results", [])

            if not results:
                break

            for result in results:
                yield result

            get_branches.resolve_pagination(shifts_result)
            get_branches.shift_next_page()
