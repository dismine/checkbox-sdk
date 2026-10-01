import asyncio
from unittest import mock
from uuid import UUID

import pytest

from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
from checkbox_sdk.client.synchronous import CheckBoxClient
from checkbox_sdk.methods.receipts import GetReceipt

RECEIPT_ID = "9887a5ed-37b8-486f-b525-1760412d40c9"
RECEIPT = {"id": RECEIPT_ID, "status": "DONE"}


@pytest.mark.parametrize("receipt_id", [RECEIPT_ID, UUID(RECEIPT_ID)])
def test_get_receipt(receipt_id):
    with CheckBoxClient() as client, mock.patch.object(client, "emit", return_value=RECEIPT) as emit:
        result = client.receipts.get_receipt(receipt_id)

    assert result == RECEIPT
    call = emit.call_args.args[0]
    assert isinstance(call, GetReceipt)
    assert call.uri == f"receipts/{RECEIPT_ID}"


@pytest.mark.parametrize("receipt_id", [RECEIPT_ID, UUID(RECEIPT_ID)])
def test_get_receipt_async(receipt_id):
    async def run():
        async with AsyncCheckBoxClient() as client:
            with mock.patch.object(client, "emit", new=mock.AsyncMock(return_value=RECEIPT)) as emit:
                return await client.receipts.get_receipt(receipt_id), emit

    result, emit = asyncio.run(run())

    assert result == RECEIPT
    call = emit.call_args.args[0]
    assert isinstance(call, GetReceipt)
    assert call.uri == f"receipts/{RECEIPT_ID}"
