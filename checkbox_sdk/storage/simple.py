from dataclasses import dataclass
from typing import Any, Dict, Optional

import jwt


@dataclass
class SessionStorage:
    """
    A class to store session-related data for making authenticated API requests.

    This class stores session-specific information such as the authorization token, license key,
    and machine ID. It also manages the headers required for authentication and provides decoded
    token data.

    Attributes:
        token (Optional[str]): The authentication token used for API requests.
        license_key (Optional[str]): The license key associated with the session.
        machine_id (Optional[str]): The machine/device ID used in requests.
        cashier (Optional[Any]): The cashier information for the session.
        cash_register (Optional[Any]): The cash register information for the session.
        shift (Optional[Any]): The active shift information for the session.
    """

    def __init__(
        self,
        token: Optional[str] = None,
        license_key: Optional[str] = None,
        machine_id: Optional[str] = None,
    ):
        self.token = token
        self.license_key = license_key
        self.machine_id = machine_id
        self.cashier = None
        self.cash_register = None
        self.shift = None

    @property
    def headers(self):
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if self.license_key:
            headers["X-License-Key"] = self.license_key
        if self.machine_id:
            headers["X-Device-ID"] = self.machine_id  # pragma: no cover
        return headers

    @property
    def token_data(self) -> Optional[Dict[str, Any]]:
        return jwt.decode(self.token, verify=False) if self.token else None
