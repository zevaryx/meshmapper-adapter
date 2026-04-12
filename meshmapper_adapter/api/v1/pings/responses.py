from pydantic import BaseModel

class CountResponse(BaseModel):
    tx: int
    rx: int
    disc: int
    trace: int