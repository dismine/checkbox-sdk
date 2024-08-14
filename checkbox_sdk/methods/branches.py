from checkbox_sdk.methods.base import BaseMethod, PaginationMixin


class GetAllBranches(PaginationMixin, BaseMethod):
    """
    A method class for retrieving all branches with pagination support.

    This class is used to fetch all branches from the "branches" endpoint, utilizing the pagination features
    provided by the `PaginationMixin`.

    Attributes:
        uri (str): The API endpoint for retrieving branches, set to "branches".
    """

    uri = "branches"

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
