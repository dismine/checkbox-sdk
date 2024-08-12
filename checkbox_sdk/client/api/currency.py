from typing import Optional, Any, Dict, List

from checkbox_sdk.methods import currency
from checkbox_sdk.storage.simple import SessionStorage


class Currency:
    def __init__(self, client):
        self.client = client

    def get_currency_rates(
        self, active: Optional[bool] = True, storage: Optional[SessionStorage] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves currency rates based on the specified criteria.

        Args:
            active: A flag indicating whether to retrieve only active currency rates. Defaults to True.
            storage: An optional session storage to use for the operation.

        Returns:
            A list of dictionaries, where each dictionary contains details of a currency rate.

        Example:
            .. code-block:: python

                rates = client.currency.get_currency_rates(active=True)
                for rate in rates:
                    print(rate)

        Notes:
            - This method sends a request to retrieve currency rates.
            - The `active` parameter determines if only active rates are retrieved.
        """
        return self.client(currency.GetCurrencyRates(active=active), storage=storage)

    def setup_currency_rates(
        self,
        rates: Optional[List[Dict]] = None,
        **payload,
    ) -> List[Dict[str, Any]]:
        """
        Sets up currency rates in the system.

        Args:
            rates: A list of dictionaries representing currency rates to be set up. If provided, this will be used as
                   the request payload.
            **payload: Additional payload for the request. If `rates` is provided, `**payload` should not be used.

        Returns:
            A list of dictionaries containing the details of the setup operation.

        Example:
            .. code-block:: python

                response = client.currency.setup_currency_rates(rates=[{"currency": "USD", "rate": 1.0}])
                print(response)

        Notes:
            - This method sends a POST request to set up currency rates.
            - If `rates` is provided, it will be used for the request payload; otherwise, `**payload` can be used.
        """
        return self.client(currency.SetupCurrencyRates(rates=rates, **payload))

    def get_currency_rate(
        self,
        currency_code: str,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves the current exchange rate for a specified currency.

        Args:
            currency_code: The code of the currency to retrieve the rate for.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the current exchange rate for the specified currency.

        Example:
            .. code-block:: python

                response = client.currency.get_currency_rate(currency_code="USD")
                print(response)

        Notes:
            - This method sends a GET request to retrieve the current exchange rate for the specified currency.
        """
        return self.client(currency.GetCurrencyRate(currency_code=currency_code), storage=storage)


class AsyncCurrency:
    def __init__(self, client):
        self.client = client

    async def get_currency_rates(
        self, active: Optional[bool] = True, storage: Optional[SessionStorage] = None
    ) -> List[Dict[str, Any]]:
        """
        Asynchronously retrieves currency rates based on the specified criteria.

        Args:
            active: A flag indicating whether to retrieve only active currency rates. Defaults to True.
            storage: An optional session storage to use for the operation.

        Returns:
            A list of dictionaries, where each dictionary contains details of a currency rate.

        Example:
            .. code-block:: python

                rates = await client.currency.get_currency_rates(active=True)
                for rate in rates:
                    print(rate)

        Notes:
            - This method sends an asynchronous request to retrieve currency rates.
            - The `active` parameter determines if only active rates are retrieved.
        """
        return await self.client(currency.GetCurrencyRates(active=active), storage=storage)

    async def setup_currency_rates(
        self,
        rates: Optional[List[Dict]] = None,
        **payload,
    ) -> List[Dict[str, Any]]:
        """
        Asynchronously sets up currency rates in the system.

        Args:
            rates: A list of dictionaries representing currency rates to be set up. If provided, this will be used as
                   the request payload.
            **payload: Additional payload for the request. If `rates` is provided, `**payload` should not be used.

        Returns:
            A list of dictionaries containing the details of the setup operation.

        Example:
            .. code-block:: python

                response = await client.currency.setup_currency_rates(rates=[{"currency": "USD", "rate": 1.0}])
                print(response)

        Notes:
            - This method sends an asynchronous POST request to set up currency rates.
            - If `rates` is provided, it will be used for the request payload; otherwise, `**payload` can be used.
        """
        return await self.client(currency.SetupCurrencyRates(rates=rates, **payload))

    async def get_currency_rate(
        self,
        currency_code: str,
        storage: Optional[SessionStorage] = None,
    ) -> Dict[str, Any]:
        """
        Asynchronously retrieves the current exchange rate for a specified currency.

        Args:
            currency_code: The code of the currency to retrieve the rate for.
            storage: An optional session storage to use for the operation.

        Returns:
            A dictionary containing the details of the current exchange rate for the specified currency.

        Example:
            .. code-block:: python

                response = await client.currency.get_currency_rate(currency_code="USD")
                print(response)

        Notes:
            - This method sends an asynchronous GET request to retrieve the current exchange rate for the specified
              currency.
        """
        return await self.client(currency.GetCurrencyRate(currency_code=currency_code), storage=storage)
