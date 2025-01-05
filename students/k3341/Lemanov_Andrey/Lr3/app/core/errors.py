from typing import List

from fastapi import HTTPException, status


class NotFoundEntityError(HTTPException):
    def __init__(self, entity: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Не удалось найти данный {entity} в базе данных"
        )
