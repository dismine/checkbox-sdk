from typing import Optional, Dict, List

from checkbox_sdk.methods import tax
from checkbox_sdk.storage.simple import SessionStorage


class Tax:
    def __init__(self, client):
        self.client = client

    def get_all_taxes(self, storage: Optional[SessionStorage] = None) -> List[Dict]:
        return self.client(tax.GetTax(), storage=storage)


class AsyncTax:
    def __init__(self, client):
        self.client = client

    async def get_all_taxes(self, storage: Optional[SessionStorage] = None) -> List[Dict]:
        return await self.client(tax.GetTax(), storage=storage)
