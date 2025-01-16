from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import HTTPException, Header
from starlette import status

from app.services.exceptions import InvalidToken
from app.services.jwt import JWTService


@inject
async def get_token_payload(
        jwt_service: FromDishka[JWTService],
        token: str = Header(alias='Authorization')
):
    token = token.split(' ')[-1]
    try:
        payload = jwt_service.decode_token(token)
    except InvalidToken:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный токен'
        )
    return payload
