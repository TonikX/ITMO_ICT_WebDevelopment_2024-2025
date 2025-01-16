from datetime import datetime

from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    password: str


class RegisterSchema(BaseModel):
    username: str
    password: str


class RefreshTokenSchema(BaseModel):
    token: str


class GetJWTTokenSchema(BaseModel):
    token: str
    expires_at: datetime
