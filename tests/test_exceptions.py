import pytest
from checkbox_sdk.exceptions import CheckBoxAPIError


@pytest.mark.parametrize(
    "status, content, request_id, expected_message",
    [
        # Happy path tests
        pytest.param(200, {"message": "Success"}, "req_123", "Success", id="happy_path_success"),
        pytest.param(404, {"message": "Not Found"}, "req_404", "Not Found", id="happy_path_not_found"),
        pytest.param(500, {"message": "Server Error"}, None, "Server Error", id="happy_path_server_error"),
        # Edge cases
        pytest.param(200, {}, "req_empty", {}, id="edge_case_empty_content"),
        pytest.param(200, {"message": ""}, "req_empty_message", "", id="edge_case_empty_message"),
        pytest.param(200, {"message": None}, "req_none_message", None, id="edge_case_none_message"),
        pytest.param(
            200, {"other_key": "value"}, "req_no_message", {"other_key": "value"}, id="edge_case_no_message_key"
        ),
        # Error cases
        pytest.param(200, None, "req_none_content", None, id="error_case_none_content"),
    ],
)
def test_api_error(status, content, request_id, expected_message):
    instance = CheckBoxAPIError(status, content, request_id)

    # Assert
    assert instance.status == status
    assert instance.content == content
    assert instance.message == expected_message
    assert instance.request_id == request_id

    params = {"status": status, "request_id": request_id}
    params_str = ", ".join(f"{k}={v}" for k, v in params.items() if v is not None)
    expected_str = f"{expected_message} [{params_str}]"
    assert str(instance) == expected_str
