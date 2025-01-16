from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException
from starlette import status

from app.presentation.api.routes.auth.schemas import LoginSchema, GetJWTTokenSchema, RegisterSchema, RefreshTokenSchema
from app.services.auth import AuthenticationService
from app.services.exceptions import PasswordIsIncorrect, TokenExpired, InvalidToken

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
    route_class=DishkaRoute
)


@router.post(
    "/login",
    response_model=GetJWTTokenSchema,
)
async def login(
        body: LoginSchema,
        auth_service: FromDishka[AuthenticationService]
):
    try:
        jwt = await auth_service.login(
            username=body.username,
            password=body.password
        )
    except PasswordIsIncorrect:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )
    return GetJWTTokenSchema(
        token=jwt.token,
        expires_at=jwt.expires_at
    )


@router.post(
    "/register",
    response_model=GetJWTTokenSchema,
)
async def register(
        body: RegisterSchema,
        auth_service: FromDishka[AuthenticationService]
):
    jwt = await auth_service.register(
            username=body.username,
            password=body.password
        )
    return GetJWTTokenSchema(
        token=jwt.token,
        expires_at=jwt.expires_at
    )


@router.post(
    "/refresh-token",
    response_model=GetJWTTokenSchema,
)
async def refresh_token(
        body: RefreshTokenSchema,
        auth_service: FromDishka[AuthenticationService]
):
    try:
        jwt = await auth_service.refresh_token(body.token)
    except TokenExpired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен устарел"
        )
    except InvalidToken:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен"
        )
    return GetJWTTokenSchema(
        token=jwt.token,
        expires_at=jwt.expires_at
    )
