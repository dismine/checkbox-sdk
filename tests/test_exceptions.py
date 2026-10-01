import time

import pytest

from checkbox_sdk.client.base import BaseCheckBoxClient
from checkbox_sdk.exceptions import CheckBoxError, StatusException, StatusWaitTimeout


def test_handle_wait_status_timeout_raises_status_wait_timeout():
    with pytest.raises(StatusWaitTimeout) as exc_info:
        BaseCheckBoxClient.handle_wait_status({"status": "CREATED"}, "status", {"OPENED"}, time.monotonic())

    exc = exc_info.value
    assert isinstance(exc, StatusException)
    assert isinstance(exc, CheckBoxError)
    assert isinstance(exc, ValueError)
    assert exc.field == "status"
    assert exc.expected_value == {"OPENED"}
    assert exc.actual == "CREATED"
    assert exc.elapsed >= 0


def test_status_wait_timeout_message():
    exc = StatusWaitTimeout(field="status", expected_value={"OPENED"}, actual="CREATED", elapsed=35.3961)

    assert str(exc) == (
        "Object did not change field 'status' to one of expected values {'OPENED'} (actually 'CREATED') "
        "in 35.396 seconds"
    )


def test_handle_wait_status_expected_value_does_not_raise():
    BaseCheckBoxClient.handle_wait_status({"status": "OPENED"}, "status", {"OPENED", "CLOSED"}, time.monotonic())
