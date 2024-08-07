import logging
from typing import Any, Dict, Optional

from checkbox_sdk.methods import organization
from checkbox_sdk.storage.simple import SessionStorage

logger = logging.getLogger(__name__)


class Organization:
    def __init__(self, client):
        self.client = client

    def get_organization_receipt_config(
        self,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves the organization's receipt configuration using the client with the provided storage.

        Args:
            storage: An optional session storage to use for the retrieval.

        Returns:
            A dictionary containing the organization's receipt configuration.

        """
        return self.client(organization.GetOrganizationReceiptConfig(), storage=storage)

    def get_organization_logo(
        self,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Retrieves the organization's logo as a string using the client with the provided storage.

        Args:
            storage: An optional session storage to use for the retrieval.

        Returns:
            A string representing the organization's logo.

        """
        return self.client(organization.GetOrganizationLogo(), storage=storage)

    def get_organization_text_logo(
        self,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Retrieves the organization's text logo as a string using the client with the provided storage.

        Args:
            storage: An optional session storage to use for the retrieval.

        Returns:
            A string representing the organization's text logo.

        """
        return self.client(organization.GetOrganizationTextLogo(), storage=storage)

    def get_organization_sms_billing(
        self,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves the organization's SMS billing information using the client with the provided storage.

        Args:
            storage: An optional session storage to use for the retrieval.

        Returns:
            A dictionary containing the organization's SMS billing information.

        """
        return self.client(organization.GetOrganizationSmsBilling(), storage=storage)


class AsyncOrganization:
    def __init__(self, client):
        self.client = client

    async def get_organization_receipt_config(
        self,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves the organization's receipt configuration using the client with the provided storage.

        Args:
            storage: An optional session storage to use for the retrieval.

        Returns:
            A dictionary containing the organization's receipt configuration.

        """
        return await self.client(organization.GetOrganizationReceiptConfig(), storage=storage)

    async def get_organization_logo(
        self,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Retrieves the organization's logo as a string using the client with the provided storage.

        Args:
            storage: An optional session storage to use for the retrieval.

        Returns:
            A string representing the organization's logo.

        """
        return await self.client(organization.GetOrganizationLogo(), storage=storage)

    async def get_organization_text_logo(
        self,
        storage: Optional[SessionStorage] = None,
    ) -> str:
        """
        Retrieves the organization's text logo as a string using the client with the provided storage.

        Args:
            storage: An optional session storage to use for the retrieval.

        Returns:
            A string representing the organization's text logo.

        """
        return await self.client(organization.GetOrganizationTextLogo(), storage=storage)

    async def get_organization_sms_billing(
        self,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves the organization's SMS billing information using the client with the provided storage.

        Args:
            storage: An optional session storage to use for the retrieval.

        Returns:
            A dictionary containing the organization's SMS billing information.

        """
        return await self.client(organization.GetOrganizationSmsBilling(), storage=storage)
