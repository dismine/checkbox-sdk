import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Dict, Optional

from httpx import Response

from checkbox_sdk.storage.simple import SessionStorage

logger = logging.getLogger(__name__)


class HTTPMethod(Enum):
    """
    Enumeration for HTTP methods used in API requests.

    This enum defines the basic HTTP methods that can be used in API calls.

    Members:
        GET: Represents the HTTP GET method.
        POST: Represents the HTTP POST method.
        PUT: Represents the HTTP PUT method.
        DELETE: Represents the HTTP DELETE method.
        PATCH: Represents the HTTP PATCH method.
    """

    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    PATCH = auto()


class AbstractMethod(ABC):
    """
    Abstract base class for defining API methods.

    This class outlines the structure for API methods, including the HTTP method,
    request URI, query parameters, payload, headers, files, and response parsing.

    Attributes:
        method: The HTTP method used for the API request. Defaults to `HTTPMethod.GET`.
        internal: A boolean flag indicating whether the URI follows a non-standard convention,
                  typically used for internal APIs. Defaults to `False`.
    """

    method: HTTPMethod = HTTPMethod.GET
    # Some APIs do not follow regular convention: base_url/api/api_version/uri.
    # For example, /_internal/orders/{order_id}
    internal: bool = False

    @property
    @abstractmethod
    def uri(self) -> str:
        """
        Abstract property that must return the URI of the API endpoint.

        Returns:
            A string representing the URI of the API endpoint.
        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def query(self):
        """
        Abstract property that must return the query parameters for the API request.

        Returns:
            A dictionary or other structure representing the query parameters for the request.
        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def payload(self):
        """
        Abstract property that must return the payload for the API request.

        Returns:
            A dictionary or other structure representing the JSON payload for the request.
        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def headers(self):
        """
        Abstract property that must return the headers for the API request.

        Returns:
            A dictionary representing the headers for the request.
        """
        pass  # pragma: no cover

    @property
    @abstractmethod
    def files(self):
        """
        Abstract property that must return the files to be sent with the API request.

        Returns:
            A dictionary or other structure representing the files to be uploaded with the request.
        """
        pass  # pragma: no cover

    @abstractmethod
    def parse_response(self, storage: SessionStorage, response: Response):
        """
        Abstract method that must parse the API response.

        This method is responsible for processing the response from the API, extracting
        necessary information, and storing it in the session storage if needed.

        Args:
            storage: The session storage instance where parsed data may be stored.
            response: The response object returned from the API request.

        Returns:
            The parsed response data, in a format specific to the API method.
        """
        pass  # pragma: no cover


class BaseMethod(AbstractMethod, ABC):
    """
    Base implementation of an API method.

    This class provides default implementations for the properties and methods defined in the
    :class:`checkbox_sdk.methods.base.AbstractMethod` class.
    It is designed to be extended by specific API method classes, allowing them to override only the properties and
    methods that require customization.

    Methods:
        query: Returns the default query parameters for the API request as an empty dictionary.
        payload: Returns the default payload for the API request as an empty dictionary.
        headers: Returns the default headers for the API request as an empty dictionary.
        files: Returns the default files for the API request as an empty dictionary.
        parse_response: Parses the JSON response from the API and attaches the server date to the result if applicable.
        _parse_server_date: Extracts and parses the "Date" header from the response to return it as a `datetime` object.
    """

    @property
    def query(self):
        """
        Returns the default query parameters for the API request.

        Returns:
            dict: An empty dictionary representing the default query parameters.
        """
        return {}

    @property
    def payload(self):
        """
        Returns the default payload for the API request.

        Returns:
            dict: An empty dictionary representing the default JSON payload.
        """
        return {}

    @property
    def headers(self):
        """
        Returns the default headers for the API request.

        Returns:
            dict: An empty dictionary representing the default headers.
        """
        return {}

    @property
    def files(self):
        """
        Returns the default files for the API request.

        Returns:
            dict: An empty dictionary representing the default files to be sent with the request.
        """
        return {}

    def parse_response(self, storage: SessionStorage, response: Response):
        """
        Parses the JSON response from the API and adds the server date if available.

        This method processes the response received from the API. If the response is a dictionary,
        it adds the server's date (if available) to the result under the key "@date".

        Args:
            storage: The session storage instance where parsed data may be stored.
            response: The response object returned from the API request.

        Returns:
            dict: The parsed JSON response with the server date added, if applicable.
        """
        result = response.json()
        if isinstance(result, dict):
            result["@date"] = self._parse_server_date(response=response)
        return result

    def _parse_server_date(self, response: Response) -> Optional[datetime]:
        """
        Parses the "Date" header from the API response into a `datetime` object.

        This method attempts to parse the "Date" header from the response into a `datetime` object in UTC.
        If the date cannot be parsed, it logs an informational message and returns `None`.

        Args:
            response: The response object containing the headers to parse.

        Returns:
            Optional[datetime]: The parsed server date as a `datetime` object, or `None` if parsing fails.
        """
        try:
            return datetime.strptime(response.headers.get("Date", None), "%a, %d %b %Y %H:%M:%S GMT").replace(
                tzinfo=timezone.utc
            )
        except ValueError:
            logger.info("Unable to parse server date")
            return None


class PaginationMixin:
    """
    A mixin class to manage pagination for API requests.

    This mixin provides methods and properties to handle pagination-related functionality,
    such as setting limits and offsets, shifting to the next or previous pages, and resolving
    pagination data from API responses.

    Attributes:
        limit (int): The maximum number of items to retrieve per request. Defaults to 10.
        offset (int): The starting position of the items to retrieve. Defaults to 0.
    """

    def __init__(self, limit: int = 10, offset: int = 0):
        """
        Initializes the PaginationMixin with the given limit and offset.

        Args:
            limit (int): The maximum number of items to retrieve per request. Defaults to 10.
            offset (int): The starting position of the items to retrieve. Defaults to 0.
        """
        self.limit = limit
        self.offset = offset

    @property
    def query(self):
        """
        Returns a dictionary representing the pagination parameters.

        The `query` dictionary contains `limit` and `offset` keys, which are used to specify
        the pagination for an API request.

        Returns:
            dict: A dictionary with pagination parameters (`limit` and `offset`).
        """
        query = {}
        if self.limit is not None:
            query["limit"] = self.limit
        if self.offset is not None:
            query["offset"] = self.offset
        return query

    def shift_next_page(self):
        """
        Moves the pagination to the next page.

        This method increments the `offset` by the value of `limit`, effectively moving to the next page of results.

        Returns:
            self: The instance itself with the updated `offset`.
        """
        self.offset += self.limit
        return self

    def shift_previous_page(self):
        """
        Moves the pagination to the previous page.

        This method decrements the `offset` by the value of `limit`, effectively moving to the previous page of results.

        Returns:
            self: The instance itself with the updated `offset`.
        """
        self.offset -= self.limit
        return self

    def set_page(self, page: int):
        """
        Sets the pagination to a specific page number.

        This method updates the `offset` based on the specified page number and the value of `limit`.

        Args:
            page (int): The page number to set.
        """
        self.offset = self.limit * page

    def resolve_pagination(self, paginated_result: Dict[str, Any]):
        """
        Updates the pagination parameters from a paginated API result.

        This method extracts the pagination metadata from the result (such as `offset` and `limit`)
        and updates the mixin's attributes accordingly.

        Args:
            paginated_result (Dict[str, Any]): The result of a paginated API request, containing pagination metadata.

        Returns:
            self: The instance itself with updated pagination parameters.
        """
        meta = paginated_result["meta"]
        self.offset = meta["offset"]
        self.limit = meta["limit"]
        return self

    @property
    def page(self):
        """
        Returns the current page number.

        The page number is calculated based on the `offset` and `limit` attributes.

        Returns:
            int: The current page number.
        """
        return self.offset // self.limit
