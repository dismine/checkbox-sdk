import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

from httpx import Response

from checkbox_sdk import __version__
from checkbox_sdk.consts import API_VERSION, BASE_API_URL, DEFAULT_REQUEST_TIMEOUT
from checkbox_sdk.exceptions import CheckBoxAPIError, CheckBoxAPIValidationError, CheckBoxError
from checkbox_sdk.methods.base import AbstractMethod
from checkbox_sdk.storage.simple import SessionStorage

logger = logging.getLogger(__name__)


class BaseCheckBoxClient(ABC):
    def __init__(
        self,
        base_url: str = BASE_API_URL,
        requests_timeout: int = DEFAULT_REQUEST_TIMEOUT,
        proxy: Optional[Union[str, Dict[str, str]]] = None,
        verify_ssl: bool = True,
        trust_env: bool = True,
        api_version: str = API_VERSION,
        storage: Optional[SessionStorage] = None,
        client_name: str = "CheckBox Python SDK",
        client_version: str = __version__,
        integration_key: Optional[str] = None,
    ) -> None:
        self.base_url = base_url
        self.api_version = api_version
        self.timeout = requests_timeout
        self.proxy = proxy
        self.verify_ssl = verify_ssl
        self.storage = storage or SessionStorage()
        self.client_name = client_name
        self.client_version = client_version
        self.integration_key = integration_key
        self.trust_env = trust_env

    @property
    def client_headers(self) -> Dict[str, Any]:
        headers = {
            "X-Client-Name": self.client_name,
            "X-Client-Version": self.client_version,
        }
        if self.integration_key:
            headers["X-Access-Key"] = self.integration_key
        return headers

    @abstractmethod
    def emit(self, storage: SessionStorage, method: AbstractMethod):
        pass

    def __call__(self, *args, **kwargs):
        return self.emit(*args, **kwargs)

    @classmethod
    def _check_response(cls, response: Response):
        if response.status_code >= 500:
            raise CheckBoxError(
                f"Failed to make request [status={response.status_code}, text={response.text!r}]"
            )
        if response.status_code == 422:
            raise CheckBoxAPIValidationError(status=response.status_code, content=response.json())
        if response.status_code >= 400:
            raise CheckBoxAPIError(status=response.status_code, content=response.json())

    def _set_license_key(
        self, storage: Optional[SessionStorage], license_key: Optional[str]
    ) -> None:
        if license_key is None:
            return
        storage = storage or self.storage
        storage.license_key = license_key
