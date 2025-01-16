from typing import Any

from app.domain.entities.base import Entity


class EntityNotFound(Exception):
    def __init__(
            self,
            entity: type[Entity],
            field_name: str,
            value: Any
    ):
        self.entity = entity
        self.value = value
        self.field_name = field_name
        super().__init__(f'{entity.__name__} with {field_name}={value} not found')


class DriverHasActiveAssignment(Exception):
    pass


class PasswordIsIncorrect(Exception):
    pass


class TokenExpired(Exception):
    pass


class InvalidToken(Exception):
    pass


class AssignmentAlreadyEnded(Exception):
    pass
