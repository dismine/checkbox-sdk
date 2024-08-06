from checkbox_sdk.methods.base import BaseMethod, PaginationMixin


class GetAllBranches(PaginationMixin, BaseMethod):
    uri = "invoices"

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
