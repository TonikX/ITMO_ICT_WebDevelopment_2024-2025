from functools import wraps
from inspect import Parameter
from typing import get_type_hints, Type, Any, List

from dishka import FromDishka
from fastapi import Depends, HTTPException
from fastapi.dependencies.utils import get_typed_signature
from starlette import status
from starlette.requests import Request

from app.domain.entities.jwt import JWTTokenPayload
from app.presentation.api.decorators.common import recreate_signature
from app.presentation.api.dependencies import get_token_payload
from app.services.users import UserService


def only_admin(func):
    wrapped_signature = get_typed_signature(func)
    existing_params = wrapped_signature.parameters
    type_hints = get_type_hints(func)

    param_mapping: dict[Type, str] = {
        UserService: 'user_service',
        Request: 'request',
        JWTTokenPayload: 'token_payload'
    }
    param_annotations: dict[str, Any] = {
        'user_service': FromDishka[UserService],
        'request': Request,
        'token_payload': JWTTokenPayload
    }
    param_defaults: dict[str, Any] = {
        'user_service': Parameter.empty,
        'request': Parameter.empty,
        'token_payload': Depends(get_token_payload)
    }

    param_names = {hint: param_name for param_name, hint in type_hints.items() if hint in param_mapping}

    to_inject: List[Parameter] = [
        Parameter(
            name=name,
            kind=Parameter.POSITIONAL_OR_KEYWORD,
            annotation=param_annotations[name],
            default=param_defaults[name]
        )
        for hint, name in param_mapping.items()
        if name not in existing_params
    ]

    @wraps(func)
    async def wrapper(
        request: Request,
        user_service: UserService,
        token_payload: JWTTokenPayload,
        *args,
        **kwargs
    ):
        user = await user_service.get_user(token_payload.user_id)
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Доступ запрещен'
            )

        # Передаем инжектированные параметры в kwargs
        for hint, param_name in param_names.items():
            kwargs[param_name] = locals()[param_mapping[hint]]

        return await func(*args, **kwargs)

    # Обновляем сигнатуру и аннотации функции
    new_signature = recreate_signature(wrapped_signature, *to_inject)
    wrapper.__signature__ = new_signature
    wrapper.__annotations__ = {param.name: param.annotation for param in new_signature.parameters.values()}

    return wrapper
