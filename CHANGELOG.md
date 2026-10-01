# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [1.6.0] - 2026-10-01

### Added

- `receipts.get_receipt(receipt_id)` (sync and async): fetches a single receipt by its ID (`GET /receipts/{id}`)
  without polling, e.g. to recover a receipt after `create_receipt` timed out or was rejected with
  `receipt.already_exists`.

### Changed

- `wait_status` (and every method that polls through it: opening/closing shifts, receipt status checks, goods
  export/import, transactions) now raises `StatusWaitTimeout` on timeout instead of a bare `ValueError`.
  `StatusWaitTimeout` subclasses both `StatusException` (and therefore `CheckBoxError`) and `ValueError`, so existing
  `except ValueError` handlers keep working while `except CheckBoxError` now catches it too. The message text is
  unchanged; the exception also exposes `field`, `expected_value`, `actual` and `elapsed` attributes.

### Documentation

- Documented how to avoid duplicate fiscal receipts when `create_receipt` times out while polling: set and persist
  your own receipt `id` before the call and retry only with the same `id`. Checkbox rejects a reused `id` with
  HTTP 400 `receipt.already_exists` (verified against the sandbox) instead of issuing a second receipt. Added to the
  `create_receipt` docstrings, as a pointer on the other receipt-creating methods, and as a new "Захист від
  дублювання чеків" section with sync/async examples in `docs/examples.rst`.

## [1.5.0] - 2026-08-05

### Changed

- Increased the minimum required Python version to 3.10 (Python 3.9 reached end-of-life on 2025-10-31).
- Updated `black` and `pytest` dev dependencies to versions without known security vulnerabilities; this was
  blocked while Python 3.9 was supported, since upstream fixes for `black`, `pytest`, `cryptography`, `filelock`,
  `marshmallow`, `nltk`, `requests`, and `urllib3` all dropped Python 3.9 support.

### Fixed

- Fixed the `license-files` glob pattern (`LICEN[CS]E.*` → `LICEN[CS]E*`), which never matched the repo's
  extension-less `LICENSE` file. Recent `poetry-core` raises a hard build error (per PEP 639) when a declared
  license-files pattern matches nothing, so this broke `poetry install`/`poetry build` on a clean environment.

## [1.4.0] - 2025-08-11

### Added

- Enhanced HTML content cleaning for better error log readability:
    * Introduced MLStripper parser that removes HTML tags and ignores content inside \<style> \<script>, and \<title>
      tags.
    * Added strip_tags utility to normalize whitespace and return clean, plain text.
    * This improvement targets Checkbox 503 error page responses, producing concise and user-friendly logs.

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