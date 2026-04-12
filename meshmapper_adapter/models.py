from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

class WebhookRequest(BaseModel):
    event: str
    region: str
    timestamp: datetime
    message: str
    data: dict[str, str | int | list[str]]
    
class IngestRequest(BaseModel):
    data: list[dict] = Field(default_factory=list)