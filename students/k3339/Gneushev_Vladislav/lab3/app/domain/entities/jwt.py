from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.base import Entity


@dataclass
class JWTToken(Entity):
    token: str
    expires_at: datetime


@dataclass
class JWTTokenPayload(Entity):
    user_id: int
    expires_at: datetime
