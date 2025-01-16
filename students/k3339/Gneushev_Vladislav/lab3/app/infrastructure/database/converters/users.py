from app.domain.entities.users import User
from app.infrastructure.database.models import UserDB


def from_user_dm_to_db(entity: User) -> UserDB:
    return UserDB(
        id=entity.id,
        username=entity.username,
        password_hash=entity.password_hash,
        is_admin=entity.is_admin
    )
