from typing import List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from students.k3341.Lemanov_Andrey.Lr3.app.io.web import schemas
from students.k3341.Lemanov_Andrey.Lr3.app.core.utils import decode_access_token
from students.k3341.Lemanov_Andrey.Lr3.app.io.repository.postgres.repository import Repository
from students.k3341.Lemanov_Andrey.Lr3.app.io.web.schemas import User, UserInDB, TokenData
from students.k3341.Lemanov_Andrey.Lr3.app.io.repository.postgres.database import AsyncSessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Service:

    def __init__(self, database: AsyncSessionLocal):
        self.database = database
        self.repository = Repository(self.database)

    def get_user(self, username: str) -> UserInDB:
        return fake_users_db.get(username)

    def get_current_user(self, token: str = Depends(oauth2_scheme)) -> TokenData:
        payload = decode_access_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return TokenData(username=payload["sub"])

    def add_user(self, user: User, hashed_password: str):
        if user.username in fake_users_db.keys():
            raise HTTPException(status_code=400, detail="Username already registered")
        fake_users_db[user.username] = UserInDB(**user.dict(), hashed_password=hashed_password)
        print(fake_users_db)






