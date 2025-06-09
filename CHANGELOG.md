# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.3.0] - 2025-06-09

### Added

- Support for new GET /api/v1/organization/billing-status method.
  This endpoint allows clients to retrieve the current billing status of an organization.
  [More details](https://checkbox.ua/blog/novi-funktsii-checkbox-u-travni-2025/)

## [1.2.0] - 2025-02-13

### Added

- Explicitly defined `httpx` package as a dependency.
- Added rate-limiting support through HTTPX's transport.

### Changed

- Updated project dependencies to newer versions.
- Replaced the deprecated `proxies` argument in HTTP proxies with `proxy` and `proxy_mounts` for improved proxy
  configuration.
- Rewritten the changelog to the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format and improve clarity.
- Increased the minimum required Python version to 3.9.
- Minor fixes in documentation.

### Fixed

- Corrected conversion of datetime objects to ISO 8601 formatted strings.

### Migration Guide

If you were previously using the `proxies` argument, update your code to use the new `proxy` and `proxy_mounts`
parameters.

#### Global Proxy Configuration

To apply a single proxy for all requests, use the `proxy` argument:

```python
from checkbox_sdk.client.synchronous import CheckBoxClient
from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient

client = CheckBoxClient(proxy="http://localhost:8030")
# or for async usage:
async_client = AsyncCheckBoxClient(proxy="http://localhost:8030")
```

#### Per-Protocol Proxy Configuration

To configure different proxies for HTTP and HTTPS, use `proxy_mounts`:

```python
import httpx

from checkbox_sdk.client.synchronous import CheckBoxClient
from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient

proxy_mounts = {
    "http://": httpx.HTTPTransport(proxy="http://localhost:8030"),
    "https://": httpx.HTTPTransport(proxy="http://localhost:8031"),
}

client = CheckBoxClient(proxy_mounts=proxy_mounts)
# or for async usage:
async_client = AsyncCheckBoxClient(proxy_mounts=proxy_mounts)
```

## [1.1.0] - 2024-08-24

### Added

- Method to call Ask Offline codes.

### Changed

- Improved documentation.
- Updated dependency variables.
- Removed code duplication and fixed warnings.

### Fixed

- Corrected logic for the `get_offline_codes` method.

## [1.0.0] - 2024-08-14

### Added

- First public release.