import asyncio
import time
from threading import Lock
from typing import Optional

import httpx

from checkbox_sdk.consts import DEFAULT_RATE_LIMIT


class RateLimitTransport(httpx.BaseTransport):
    """Transport wrapper to enforce rate limiting using requests per 10 seconds.

    This class wraps a synchronous HTTP transport to implement rate limiting, ensuring
    that no more than a specified number of requests are made within a 10-second window.

    Attributes:
        transport (httpx.BaseTransport): The underlying HTTP transport to handle requests.
        lock (Lock): A lock to ensure thread-safe request handling.
        min_interval (float): The minimum time interval between requests, calculated from the rate limit.
        last_request_time (float): The timestamp of the last request, used to track elapsed time.
    """

    def __init__(self, transport: httpx.BaseTransport, requests_per_10s: Optional[int] = None):
        """
        :param transport: The underlying HTTP transport (httpx.HTTPTransport).
        :param requests_per_10s: Maximum number of requests per 10 seconds (default: `DEFAULT_RATE_LIMIT`).
        """

        self.transport = transport
        self.lock = Lock()
        rate_limit = requests_per_10s or DEFAULT_RATE_LIMIT
        self.min_interval = 10.0 / rate_limit  # Calculate the interval for requests per 10 seconds
        self.last_request_time = 0

    def handle_request(self, request):
        """
        Handles the request, enforcing the rate limit by ensuring the time between requests
        does not exceed the specified interval.

        The method calculates the elapsed time since the last request and waits if necessary
        to maintain the rate limit before forwarding the request to the underlying transport.

        :param request: The HTTP request to be handled.
        :return: The response returned by the underlying transport after handling the request.
        """

        with self.lock:
            now = time.time()
            elapsed = now - self.last_request_time

            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)  # Wait to stay within the rate limit

            self.last_request_time = time.time()  # Update last request timestamp
            return self.transport.handle_request(request)  # Forward the request


class AsyncRateLimitTransport(httpx.AsyncBaseTransport):
    """Transport wrapper to enforce rate limiting using requests per 10 seconds.

    This class wraps an asynchronous HTTP transport to implement rate limiting, ensuring
    that no more than a specified number of requests are made within a 10-second window.

    Attributes:
        transport (httpx.AsyncBaseTransport): The underlying asynchronous HTTP transport to handle requests.
        lock (Lock): A lock to ensure thread-safe request handling.
        min_interval (float): The minimum time interval between requests, calculated from the rate limit.
        last_request_time (float): The timestamp of the last request, used to track elapsed time.
    """

    def __init__(self, transport: httpx.AsyncBaseTransport, requests_per_10s: Optional[int] = None):
        """
        :param transport: The underlying HTTP transport (httpx.AsyncHTTPTransport).
        :param requests_per_10s: Maximum number of requests per 10 seconds (default: `DEFAULT_RATE_LIMIT`).
        """

        self.transport = transport
        self.lock = Lock()
        rate_limit = requests_per_10s or DEFAULT_RATE_LIMIT
        self.min_interval = 10.0 / rate_limit  # Calculate the interval for requests per 10 seconds
        self.last_request_time = 0

    async def handle_async_request(self, request):
        """
        Handles the asynchronous request, enforcing the rate limit by ensuring the time between requests
        does not exceed the specified interval.

        The method calculates the elapsed time since the last request and waits if necessary
        to maintain the rate limit before forwarding the request to the underlying transport.

        :param request: The asynchronous HTTP request to be handled.
        :return: The response returned by the underlying transport after handling the request.
        """

        with self.lock:
            now = time.time()
            elapsed = now - self.last_request_time

            if elapsed < self.min_interval:
                await asyncio.sleep(self.min_interval - elapsed)  # Wait to stay within the rate limit

            self.last_request_time = time.time()  # Update last request timestamp
            return await self.transport.handle_async_request(request)  # Forward the request
