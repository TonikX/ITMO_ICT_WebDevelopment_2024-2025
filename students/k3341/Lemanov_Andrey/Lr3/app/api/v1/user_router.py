from fastapi import Header, Depends
from typing import Annotated, Union, List

from fastapi import APIRouter

from students.k3341.Lemanov_Andrey.Lr3.app.io.repository.postgres.database import AsyncSessionLocal, get_db
from students.k3341.Lemanov_Andrey.Lr3.app.io.web import schemas
from students.k3341.Lemanov_Andrey.Lr3.app.core.services.users_service import UserService

user_router = APIRouter()


@user_router.post("/authorize_user")
async def authorize_user(request: schemas.AuthorizeUser):
    service = UserService(Depends(await get_db()))
    return await service.create_submission(request)


@user_router.post("/register_user")
async def create_user(request: schemas.RequestUser):
    service = UserService(Depends(await get_db()))
    return await service.create_submission(request)


@user_router.post("/get_user/{user_id}")
async def get_user(submission_id: int):
    service = UserService(Depends(await get_db()))
    return await service.get_submission_by_id(submission_id)


@user_router.post("/get_all_users")
async def get_all_users():
    service = UserService(Depends(await get_db()))
    return await service.get_all_submissions()
