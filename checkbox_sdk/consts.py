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
