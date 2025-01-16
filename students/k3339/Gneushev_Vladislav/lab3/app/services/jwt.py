from datetime import datetime, timezone, timedelta

import jwt
from jwt import DecodeError

from app.config.models import AuthConfig
from app.domain.entities.jwt import JWTToken, JWTTokenPayload
from app.services.exceptions import InvalidToken


class JWTService:
    def __init__(self, auth_config: AuthConfig):
        self.auth_config = auth_config

    def create_token(self, user_id: int) -> JWTToken:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.auth_config.access_token_lifetime)
        to_encode = {
            "user_id": user_id,
            "exp": expire
        }
        encoded_jwt = jwt.encode(
            payload=to_encode,
            key=self.auth_config.secret_token,
            algorithm="HS256"
        )
        return JWTToken(
            token=encoded_jwt,
            expires_at=expire
        )

    def decode_token(self, token: str) -> JWTTokenPayload:
        try:
            decoded = jwt.decode(
                jwt=token,
                key=self.auth_config.secret_token,
                algorithms=["HS256"]
            )
        except DecodeError:
            raise InvalidToken()
        return JWTTokenPayload(
            user_id=decoded["user_id"],
            expires_at=datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
        )
