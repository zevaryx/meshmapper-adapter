from pydantic import BaseModel

class RegisterResponse(BaseModel):
    username: str
    api_key: str
    app_url: str
    
class LoginResponse(BaseModel):
    username: str
    api_key: str
    app_url: str