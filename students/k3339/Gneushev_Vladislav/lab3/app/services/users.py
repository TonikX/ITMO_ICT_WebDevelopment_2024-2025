from app.domain.entities.users import User
from app.infrastructure.database.repositories.users import UserRepository
from app.services.exceptions import EntityNotFound


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user(self, user_id: int) -> User:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise EntityNotFound(
                entity=User,
                field_name='id',
                value=user_id
            )
        return user
