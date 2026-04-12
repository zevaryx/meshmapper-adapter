from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    password: str
    verify: str
    
class LoginRequest(BaseModel):
    username: str
    password: str