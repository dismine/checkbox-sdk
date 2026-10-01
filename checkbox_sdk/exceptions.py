from typing import Any, Dict, Optional, Set


class CheckBoxError(Exception):
    pass


class CheckBoxNetworkError(CheckBoxError):
    pass


class CheckBoxAPIError(CheckBoxError):
    def __init__(
        self,
        status: int,
        content: Dict[str, Any],
        request_id: Optional[str] = None,
    ):
        self.status = status
        self.content = content
        self.message = content.get("message", content) if self.content else content
        self.request_id = request_id

    def __str__(self):
        params = {"status": self.status, "request_id": self.request_id}
        params_str = ", ".join(f"{k}={v}" for k, v in params.items() if v is not None)
        return f"{self.message} [{params_str}]"


class CheckBoxAPIValidationError(CheckBoxAPIError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.detail = self.content.get("detail", [])

    def __str__(self):
        validations = []
        for item in self.detail:
            location = " -> ".join(map(str, item["loc"]))
            error_type = item["type"]
            description = item["msg"]
            validations.append(f"{location}:\n    {description} (type={error_type})")  # noqa: E231
        validations_str = "\n".join(validations)
        message = super().__str__()
        return f"{message}\n{validations_str}"


class StatusException(CheckBoxError):
    pass


class StatusWaitTimeout(StatusException, ValueError):
    """
    Raised when a polled object does not reach one of the expected statuses within the timeout.

    Also subclasses `ValueError` for backward compatibility with code that caught the previously raised `ValueError`.
    """

    def __init__(self, field: str, expected_value: Set[Any], actual: Any, elapsed: float):
        self.field = field
        self.expected_value = expected_value
        self.actual = actual
        self.elapsed = elapsed
        super().__init__(
            f"Object did not change field {field!r} "
            f"to one of expected values {expected_value} (actually {actual!r}) "
            f"in {elapsed:.3f} seconds"  # noqa: E231
        )
