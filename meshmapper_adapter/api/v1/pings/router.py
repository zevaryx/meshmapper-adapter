from fastapi import APIRouter, HTTPException

from meshmapper_adapter.db import TXPingObject, RXPingObject, DISCPingObject, TRACEPingObject, User

from .errors import UnknownKey
from .requests import CountRequest
from .responses import CountResponse

router = APIRouter(prefix="/pings")

@router.get("/", response_model=CountResponse)
async def count() -> CountResponse:
    tx = await TXPingObject.count()
    rx = await RXPingObject.count()
    disc = await DISCPingObject.count()
    trace = await TRACEPingObject.count()
    
    return CountResponse(tx=tx, rx=rx, disc=disc, trace=trace)

@router.get(
    "/{key}", 
    response_model=CountResponse,
)
async def count_by_key(key: str) -> CountResponse:
    user = await User.find_one(User.api_key == key)
    if not user:
        raise HTTPException(status_code=404, detail=f"key not found: {key}")
    tx = await TXPingObject.find(TXPingObject.user == user, fetch_links=True).count()
    rx = await RXPingObject.find(RXPingObject.user == user, fetch_links=True).count()
    disc = await DISCPingObject.find(DISCPingObject.user == user, fetch_links=True).count()
    trace = await TRACEPingObject.find(TRACEPingObject.user == user, fetch_links=True).count()
    
    return CountResponse(tx=tx, rx=rx, disc=disc, trace=trace)