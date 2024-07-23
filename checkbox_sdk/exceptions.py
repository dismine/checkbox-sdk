from typing import Any, Dict, Optional


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
        self.message = content.get("message", content)
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
            validations.append(f"{location}:\n    {description} (type={error_type})")
        validations_str = "\n".join(validations)
        message = super().__str__()
        return f"{message}\n{validations_str}"


class StatusException(CheckBoxError):
    pass
