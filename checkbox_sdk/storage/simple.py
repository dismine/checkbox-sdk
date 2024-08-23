from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

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
        cashier (Optional[Dict]): The cashier information for the session.
        cash_register (Optional[Dict]): The cash register information for the session.
        shift (Optional[Dict]): The active shift information for the session.
    """

    token: Optional[str] = None
    license_key: Optional[str] = None
    machine_id: Optional[str] = None
    cashier: Optional[Dict[str, Any]] = None
    cash_register: Optional[Dict[str, Any]] = None
    shift: Optional[Dict[str, Any]] = None

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
    def token_data(self) -> Union[Dict[str, Any], None]:
        return jwt.decode(self.token, options={"verify_signature": False}) if self.token else None
