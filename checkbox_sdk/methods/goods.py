from typing import Optional, Union
from uuid import UUID

from httpx import Response

from checkbox_sdk.methods.base import BaseMethod, PaginationMixin, HTTPMethod
from checkbox_sdk.storage.simple import SessionStorage

URI_PREFIX = "goods/"


class GetGoods(PaginationMixin, BaseMethod):
    uri = "goods"

    def __init__(
        self,
        group_id: Optional[Union[str, UUID]] = None,
        without_group_only: Optional[bool] = False,
        query: Optional[str] = None,
        order_by_name: Optional[str] = None,
        order_by_code: Optional[str] = None,
        order_by_position: Optional[str] = None,
        load_children: Optional[bool] = False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.group_id = group_id
        self.without_group_only = without_group_only
        self.query_search = query
        self.order_by_name = order_by_name
        self.order_by_code = order_by_code
        self.order_by_position = order_by_position
        self.load_children = load_children

    @property
    def query(self):
        query = super().query

        if isinstance(self.group_id, UUID):
            query["group_id"] = str(self.group_id)
        elif self.group_id:
            query["group_id"] = self.group_id

        if self.without_group_only is not None:
            query["without_group_only"] = self.without_group_only

        if self.query_search is not None:
            query["query"] = self.query_search

        if self.order_by_name is not None:
            query["order_by_name"] = self.order_by_name

        if self.order_by_code is not None:
            query["order_by_code"] = self.order_by_code

        if self.order_by_position is not None:
            query["order_by_position"] = self.order_by_position

        return query


class GetGroups(PaginationMixin, BaseMethod):
    uri = f"{URI_PREFIX}groups"

    def __init__(
        self,
        search: Optional[str] = None,
        parent_groups_only: Optional[bool] = False,
        parent_id: Optional[str] = None,
        order_by_name: Optional[str] = None,
        order_by_created_at: Optional[str] = None,
        order_by_updated_at: Optional[str] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.search = search
        self.parent_groups_only = parent_groups_only
        self.parent_id = parent_id
        self.order_by_name = order_by_name
        self.order_by_created_at = order_by_created_at
        self.order_by_updated_at = order_by_updated_at

    @property
    def query(self):
        query = super().query

        if self.search is not None:
            query["search"] = self.search

        if self.parent_groups_only is not None:
            query["parent_groups_only"] = self.parent_groups_only

        if self.parent_id is not None:
            query["parent_id"] = self.parent_id

        if self.order_by_name is not None:
            query["order_by_name"] = self.order_by_name

        if self.order_by_created_at is not None:
            query["order_by_created_at"] = self.order_by_created_at

        if self.order_by_updated_at is not None:
            query["order_by_updated_at"] = self.order_by_updated_at

        return query


class GetGood(BaseMethod):
    def __init__(self, good_id: Union[str, UUID]):
        self.good_id = good_id

    @property
    def uri(self) -> str:
        good_id_str = str(self.good_id) if isinstance(self.good_id, UUID) else self.good_id
        return f"{URI_PREFIX}{good_id_str}"


class ExportGoods(BaseMethod):
    def __init__(self, export_extension: str):
        self.export_extension = export_extension

    @property
    def uri(self) -> str:
        return f"{URI_PREFIX}export/{self.export_extension}"


class ExportGoodsTaskStatus(BaseMethod):
    def __init__(self, task_id: Union[str, UUID]):
        self.task_id = task_id

    @property
    def uri(self) -> str:
        task_id_str = str(self.task_id) if isinstance(self.task_id, UUID) else self.task_id
        return f"{URI_PREFIX}export/task_status/{task_id_str}"


class ExportGoodsFile(BaseMethod):
    def __init__(
        self,
        task_id: Union[str, UUID],
        export_extension: str,
    ):
        self.task_id = task_id
        self.export_extension = export_extension

    @property
    def uri(self) -> str:
        task_id_str = str(self.task_id) if isinstance(self.task_id, UUID) else self.task_id
        return f"{URI_PREFIX}export/file/{task_id_str}"

    def parse_response(self, storage: SessionStorage, response: Response):
        if self.export_extension == "json":
            return response.json()
        elif self.export_extension == "csv":
            return response.content.decode()
        else:
            return response.content


class ImportGoodsFromFile(BaseMethod):
    method = HTTPMethod.POST
    uri = f"{URI_PREFIX}import/upload"

    def __init__(
        self,
        file: str,
        ignore_barcode_duplicates: Optional[bool] = False,
        auto_supply: Optional[bool] = False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.file = file
        self.ignore_barcode_duplicates = ignore_barcode_duplicates
        self.auto_supply = auto_supply

    @property
    def query(self):
        query = super().query

        if self.ignore_barcode_duplicates is not None:
            query["ignore_barcode_duplicates"] = self.ignore_barcode_duplicates

        if self.auto_supply is not None:
            query["auto_supply"] = self.auto_supply

        return query

    @property
    def files(self):
        return {"file": open(self.file, "rb")}


class ImportGoodsTaskStatus(BaseMethod):
    def __init__(self, task_id: Union[str, UUID]):
        self.task_id = task_id

    @property
    def uri(self) -> str:
        task_id_str = str(self.task_id) if isinstance(self.task_id, UUID) else self.task_id
        return f"{URI_PREFIX}import/task_status/{task_id_str}"


class ImportGoodsApplyChanges(BaseMethod):
    method = HTTPMethod.POST

    def __init__(self, task_id: Union[str, UUID]):
        self.task_id = task_id

    @property
    def uri(self) -> str:
        task_id_str = str(self.task_id) if isinstance(self.task_id, UUID) else self.task_id
        return f"{URI_PREFIX}import/apply_changes/{task_id_str}"
