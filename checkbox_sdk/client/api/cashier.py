from typing import Optional, Dict, Any

from checkbox_sdk.methods import cashier
from checkbox_sdk.storage.simple import SessionStorage


class Cashier:
    def __init__(self, client):
        self.client = client

    def authenticate(
        self,
        login: str,
        password: str,
        license_key: Optional[str] = None,
        storage: Optional[SessionStorage] = None,
    ) -> None:
        """
        Authenticate using cashier's login credentials.

        This method sets the cash license key, signs in using the provided cashier's login and password,
        and refreshes the user (cashier) information.

        Args:
            login (str): The user's login.
            password (str): The user's password.
            license_key (Optional[str]): The cash register license key to set.
            storage (Optional[SessionStorage]): The session storage to use.

        Returns:
            None
        """
        self.client.set_license_key(storage=storage, license_key=license_key)
        self.client(cashier.SignIn(login=login, password=password), storage=storage)
        self.client.refresh_info(storage=storage)

    def authenticate_pin_code(
        self,
        pin_code: str,
        license_key: Optional[str] = None,
        storage: Optional[SessionStorage] = None,
    ) -> None:
        """
        Authenticate using a PIN code (recommended method).

        This method sets the cash license key, signs in using the provided cashier's PIN code,
        and refreshes the user (cashier) information.

        Args:
            pin_code (str): The PIN code for cashier authentication.
            license_key (Optional[str]): The cash register license key to set.
            storage (Optional[SessionStorage]): The session storage to use.

        Returns:
            None
        """
        self.client.set_license_key(storage=storage, license_key=license_key)
        self.client(cashier.SignInPinCode(pin_code=pin_code), storage=storage)
        self.client.refresh_info(storage=storage)

    def authenticate_token(
        self,
        token: str,
        license_key: Optional[str] = None,
        storage: Optional[SessionStorage] = None,
    ) -> None:
        """
        Authenticate using a token.

        This method sets the cash license key, assigns the token to the storage,
        and refreshes the user (cashier) information. Use this method if you already have an access token.

        Args:
            token (str): The token for authentication.
            license_key (Optional[str]): The cash register license key to set.
            storage (Optional[SessionStorage]): The session storage to use.

        Returns:
            None
        """
        storage = storage or self.client.storage
        self.client.set_license_key(storage=storage, license_key=license_key)
        storage.token = token
        self.client.refresh_info(storage=storage)

    def sign_out(self, storage: Optional[SessionStorage] = None) -> None:
        """
        Sign out cashier.

        This method signs out the current user (cashier) by calling the SignOut endpoint.

        Args:
            storage (Optional[SessionStorage]): The session storage to use.

        Returns:
            None
        """
        self.client(cashier.SignOut(), storage=storage)

    def check_signature(self, storage: Optional[SessionStorage] = None) -> Dict[str, Any]:
        """
        Checks the signature using the client with the provided storage.

        Args:
            storage: An optional session storage to use for the signature check.

        Returns:
            A dictionary containing the signature key.

        """
        return self.client(cashier.GetSignatureKey(), storage=storage)

    def get_all_taxes_by_cashier(self, storage: Optional[SessionStorage] = None) -> Dict[str, Any]:
        """
        Retrieves all taxes associated with a cashier using the client with the provided storage.

        Args:
            storage: An optional session storage to use for the retrieval.

        Returns:
            A dictionary containing all taxes associated with the cashier.

        """
        return self.client(cashier.GetAllTaxesByCashier(), storage=storage)


class AsyncCashier:
    def __init__(self, client):
        self.client = client

    async def authenticate(
        self,
        login: str,
        password: str,
        license_key: Optional[str] = None,
        storage: Optional[SessionStorage] = None,
    ) -> None:
        """
        Authenticate using cashier's login credentials.

        This method sets the cash license key, signs in using the provided cashier's login and password,
        and refreshes the user (cashier) information.

        Args:
            login (str): The user's login.
            password (str): The user's password.
            license_key (Optional[str]): The cash register license key to set.
            storage (Optional[SessionStorage]): The session storage to use.

        Returns:
            None
        """
        self.client.set_license_key(storage=storage, license_key=license_key)
        await self.client(cashier.SignIn(login=login, password=password), storage=storage)
        await self.client.refresh_info(storage=storage)

    async def authenticate_pin_code(
        self,
        pin_code: str,
        license_key: Optional[str] = None,
        storage: Optional[SessionStorage] = None,
    ) -> None:
        """
        Authenticate using a PIN code (recommended method).

        This method sets the cash license key, signs in using the provided cashier's PIN code,
        and refreshes the user (cashier) information.

        Args:
            pin_code (str): The PIN code for cashier authentication.
            license_key (Optional[str]): The cash register license key to set.
            storage (Optional[SessionStorage]): The session storage to use.

        Returns:
            None
        """
        self.client.set_license_key(storage=storage, license_key=license_key)
        await self.client(cashier.SignInPinCode(pin_code=pin_code), storage=storage)
        await self.client.refresh_info(storage=storage)

    async def authenticate_token(
        self,
        token: str,
        license_key: Optional[str] = None,
        storage: Optional[SessionStorage] = None,
    ) -> None:
        """
        Authenticate using a token.

        This method sets the cash license key, assigns the token to the storage,
        and refreshes the user (cashier) information. Use this method if you already have an access token.

        Args:
            token (str): The token for authentication.
            license_key (Optional[str]): The cash register license key to set.
            storage (Optional[SessionStorage]): The session storage to use.

        Returns:
            None
        """
        storage = storage or self.client.storage
        self.client.set_license_key(storage=storage, license_key=license_key)
        storage.token = token
        await self.client.refresh_info(storage=storage)

    async def sign_out(self, storage: Optional[SessionStorage] = None) -> None:
        """
        Sign out cashier.

        This method signs out the current user (cashier) by calling the SignOut endpoint.

        Args:
            storage (Optional[SessionStorage]): The session storage to use.

        Returns:
            None
        """
        await self.client(cashier.SignOut(), storage=storage)

    async def check_signature(self, storage: Optional[SessionStorage] = None) -> Dict[str, Any]:
        """
        Checks the signature asynchronously using the client with the provided storage.

        Args:
            storage: An optional session storage to use for the signature check.

        Returns:
            A dictionary containing the signature key.

        """
        return await self.client(cashier.GetSignatureKey(), storage=storage)

    async def get_all_taxes_by_cashier(self, storage: Optional[SessionStorage] = None) -> Dict[str, Any]:
        """
        Retrieves all taxes associated with a cashier asynchronously using the client with the provided storage.

        Args:
            storage: An optional session storage to use for the retrieval.

        Returns:
            A dictionary containing all taxes associated with the cashier.

        """
        return await self.client(cashier.GetAllTaxesByCashier(), storage=storage)
