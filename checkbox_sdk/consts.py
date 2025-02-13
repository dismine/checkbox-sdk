"""
checkbox_sdk.constants
======================

This module defines constants used throughout the `checkbox-sdk` package. These constants provide
default values for API interaction, such as the base URL, API version, and request timing settings.

Constants:
----------
- **BASE_API_URL**: The base URL for the Checkbox API.
- **API_VERSION**: The version of the Checkbox API to use.
- **DEFAULT_REQUEST_TIMEOUT**: The default timeout for API requests, in seconds.
- **DEFAULT_REQUESTS_RELAX**: The default delay between API requests, in seconds.
- **DEFAULT_RATE_LIMIT**: The default rate limit in requests per 10 seconds.
"""

BASE_API_URL = "https://api.checkbox.in.ua"
"""
The base URL for the Checkbox API.

This URL is used as the root endpoint for making API requests. It is a constant and does not change.
"""

API_VERSION = "1"
"""
The version of the Checkbox API to use.

This constant specifies the version of the API that the client is interacting with. It ensures compatibility
with the API endpoints and their functionalities.
"""

DEFAULT_REQUEST_TIMEOUT = 60  # seconds
"""
The default timeout for API requests.

This value sets the default amount of time (in seconds) to wait for an API request to complete before timing out.
It helps to handle cases where the API might be slow to respond.
"""

DEFAULT_REQUESTS_RELAX = 0.75  # seconds
"""
The default delay between API requests.

This value sets the default amount of time (in seconds) to wait between consecutive API requests to avoid
 overloading the server or hitting rate limits.
"""

DEFAULT_RATE_LIMIT = 15  # requests per 10 seconds
"""
The default rate limit for API requests.

This constant sets the default number of allowed requests in a 10-second period. It helps to manage API
rate-limiting behavior and prevent overloading the server.
"""
