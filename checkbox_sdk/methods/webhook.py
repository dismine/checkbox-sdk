from checkbox_sdk.methods.base import BaseMethod, HTTPMethod


class GetWebhookInfo(BaseMethod):
    uri = "webhook"


class SetWebhook(BaseMethod):
    method = HTTPMethod.POST
    uri = "webhook"

    def __init__(
        self,
        url: str,
    ):
        self.url = url

    @property
    def payload(self):
        payload = super().payload
        payload["url"] = self.url
        return payload


class DeleteWebhook(BaseMethod):
    method = HTTPMethod.DELETE
    uri = "webhook"
