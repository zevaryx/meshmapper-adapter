from pydantic import BaseModel

class CountRequest(BaseModel):
    include_trace: bool = True