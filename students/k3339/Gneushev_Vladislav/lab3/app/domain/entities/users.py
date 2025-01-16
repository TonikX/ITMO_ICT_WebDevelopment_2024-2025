from dataclasses import dataclass

from app.domain.entities.base import Entity


@dataclass
class User(Entity):
    id: int | None
    username: str
    password_hash: str
    is_admin: bool
