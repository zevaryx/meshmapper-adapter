from pydantic import BaseModel

class WebhookRequest(BaseModel):
    event: str
    region: str
    timestamp: int
    message: str
    data: dict[str, str | int | list[str]]