from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from students.k3341.Lemanov_Andrey.Lr3.app.api.v1.submissions import schemas
from students.k3341.Lemanov_Andrey.Lr3.app.core.services.submissions_service import SubmissionsService
from students.k3341.Lemanov_Andrey.Lr3.app.io.repository.postgres.database import get_db

submission_router = APIRouter()


@submission_router.post("/create_submission")
async def create_submission(
        request: schemas.RequestCreateSubmission,
        db_session: AsyncSession = Depends(get_db)
):
    service = SubmissionsService(db_session)
    return await service.create_submission(request)


@submission_router.get("/get_submission/{submission_id}")
async def get_submission(
        submission_id: int,
        db_session: AsyncSession = Depends(get_db)
):
    service = SubmissionsService(db_session)
    return await service.get_submission_by_id(submission_id)


@submission_router.get("/get_all_submissions")
async def get_all_submissions(
        db_session: AsyncSession = Depends(get_db)
):
    service = SubmissionsService(db_session)
    return await service.get_all_submissions()


@submission_router.delete("/delete_submission/{submission_id}")
async def delete_submission(
        submission_id: int,
        db_session: AsyncSession = Depends(get_db)
):
    service = SubmissionsService(db_session)
    success = await service.delete_submission(submission_id)
    if not success:
        raise Exception(f"Submission with ID {submission_id} not found.")
    return {"message": "Submission deleted successfully"}


@submission_router.put("/update_submission")
async def update_submission(
        request: schemas.RequestUpdateSubmission,
        db_session: AsyncSession = Depends(get_db)
):
    service = SubmissionsService(db_session)
    return await service.update_submission(request)
