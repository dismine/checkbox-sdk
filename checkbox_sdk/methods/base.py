from abc import ABC, abstractmethod
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Dict, Optional
import logging

from httpx import Response

from checkbox_sdk.storage.simple import SessionStorage

logger = logging.getLogger(__name__)


class HTTPMethod(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    PATCH = auto()


class AbstractMethod(ABC):
    method: HTTPMethod = HTTPMethod.GET

    @property
    @abstractmethod
    def uri(self) -> str:
        pass

    @property
    @abstractmethod
    def query(self):
        pass

    @property
    @abstractmethod
    def payload(self):
        pass

    @property
    @abstractmethod
    def headers(self):
        pass

    @abstractmethod
    def parse_response(self, storage: SessionStorage, response: Response):
        pass


class BaseMethod(AbstractMethod, ABC):
    @property
    def query(self):
        return {}

    @property
    def payload(self):
        return {}

    @property
    def headers(self):
        return {}

    def parse_response(self, storage: SessionStorage, response: Response):
        result = response.json()
        if isinstance(result, dict):
            result["@date"] = self._parse_server_date(response=response)
        return result

    def _parse_server_date(self, response: Response) -> Optional[datetime]:
        try:
            return datetime.strptime(response.headers.get("Date", None), "%a, %d %b %Y %H:%M:%S GMT").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            logger.info("Unable to parse server date")
            return None


class PaginationMixin:
    def __init__(self, limit: int = 10, offset: int = 0):
        self.limit = limit
        self.offset = offset

    @property
    def query(self):
        query = {}
        if self.limit is not None:
            query["limit"] = self.limit
        if self.offset is not None:
            query["offset"] = self.offset
        return query

    def shift_next_page(self):
        self.offset += self.limit
        return self

    def shift_previous_page(self):
        self.offset -= self.limit
        return self

    def set_page(self, page: int):
        self.offset = self.limit * page

    def resolve_pagination(self, paginated_result: Dict[str, Any]):
        meta = paginated_result["meta"]
        self.offset = meta["offset"]
        self.limit = meta["limit"]
        return self

    @property
    def page(self):
        return self.offset // self.limit
