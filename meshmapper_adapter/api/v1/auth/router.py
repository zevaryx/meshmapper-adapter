from typing import Annotated

import ulid
from argon2 import PasswordHasher
from fastapi import APIRouter, HTTPException, Header

from meshmapper_adapter.db import User
from .requests import RegisterRequest, LoginRequest
from .responses import RegisterResponse, LoginResponse

router = APIRouter(prefix="/auth")

@router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest, origin: Annotated[str | None, Header()] = None) -> RegisterResponse:
    if not origin:
        raise HTTPException(status_code=400, detail="missing origin")
    if request.password != request.verify:
        raise HTTPException(status_code=400, detail="verify does not match")
    user = await User.find_one(User.username == request.username)
    if user:
        raise HTTPException(status_code=409, detail="user already exists")
    
    hasher = PasswordHasher()
    pwhash = hasher.hash(request.password)
    
    user = User(username=request.username, pwhash=pwhash, api_key=ulid.new().str)
    await user.save()
    
    origin = origin.split("/")[-1]
    app_url = f"meshmapper://custom-api?url={origin}/ingest&key={user.api_key}"
    
    return RegisterResponse(username=user.username, api_key=user.api_key, app_url=app_url)

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, origin: Annotated[str | None, Header()] = None) -> LoginResponse:
    if not origin:
        raise HTTPException(status_code=400, detail="missing origin")
    user = await User.find_one(User.username == request.username)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    hasher = PasswordHasher()
    if not hasher.verify(user.pwhash, request.password):
        raise HTTPException(status_code=404, detail="user not found")
    
    origin = origin.split("/")[-1]
    app_url = f"meshmapper://custom-api?url={origin}/ingest&key={user.api_key}"
    
    return LoginResponse(username=user.username, api_key=user.api_key, app_url=app_url)
    