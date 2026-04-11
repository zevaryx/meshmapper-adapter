from datetime import datetime, timezone
from typing import Literal

from beanie import Document, init_beanie
from pydantic import BaseModel, Field
from pymongo import AsyncMongoClient

from settings import Settings

class Event(Document):
    event: str
    region: str
    timestamp: datetime
    message: str
    data: dict[str, str | int | list[str]]
    
class PingObject(Document):
    type: Literal["TX", "RX", "DISC", "TRACE"]
    lat: float
    lon: float
    timestamp: datetime
    external_antenna: bool
    noisefloor: int | None
    power: str | None
    contact: str | None = None
    iata: str | None = None
    
class TXPingObject(PingObject):
    heard_repeats: str
    
class RXPingObject(PingObject):
    heard_repeats: str

class DISCPingObject(PingObject):
    repeater_id: str
    node_type: str | None = None
    local_snr: float | None = None
    local_rssi: int | None = None
    remote_snr: float | None = None
    public_key: str | None = None
    
class TRACEPingObject(PingObject):
    repeater_id: str
    local_snr: float
    local_rssi: int
    remote_snr: float
    
async def connect(settings: Settings) -> bool:
    if not settings.mongo:
        return False
    client = AsyncMongoClient(
        host=settings.mongo.host,
        username=settings.mongo.username,
        password=settings.mongo.password,
        port=settings.mongo.port,
        tz_aware=True,
        tzinfo=timezone.utc,
    )
    
    db = client.meshmapper
    
    await init_beanie(database=db, document_models=[Event, TXPingObject, RXPingObject, DISCPingObject, TRACEPingObject])
    
    return True