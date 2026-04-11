from datetime import datetime, timezone

from pymongo import AsyncMongoClient
from beanie import Document, init_beanie

from settings import Settings

class Event(Document):
    event: str
    region: str
    timestamp: datetime
    message: str
    data: dict[str, str | int | list[str]]
    
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
    
    await init_beanie(database=db, document_models=[Event])
    
    return True