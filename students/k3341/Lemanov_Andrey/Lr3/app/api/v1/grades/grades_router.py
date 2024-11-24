from fastapi import Header, Depends

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from students.k3341.Lemanov_Andrey.Lr3.app.io.repository.postgres.database import get_db
from students.k3341.Lemanov_Andrey.Lr3.app.api.v1.grades import schemas
from students.k3341.Lemanov_Andrey.Lr3.app.core.services.grades_service import GradesService

grade_router = APIRouter()


@grade_router.post("/create_grade", response_model=schemas.ResponseCreateGrade)
async def create_grade(request: schemas.RequestCreateGrade, db_session: AsyncSession = Depends(get_db)):
    service = GradesService(db_session)
    return await service.create_grade(request)


@grade_router.get("/get_grade/{grade_id}", response_model=schemas.ResponseGradeWithRelationships)
async def get_grade(grade_id: int, db_session: AsyncSession = Depends(get_db)):
    service = GradesService(db_session)
    return await service.get_grade_by_id(grade_id)


@grade_router.get("/get_grades/student/{student_id}", response_model=schemas.ResponseAllGradesOfStudent)
async def get_grades_for_student(student_id: int, db_session: AsyncSession = Depends(get_db)):
    service = GradesService(db_session)
    grades = await service.get_grades_by_student_id(student_id)
    return grades


@grade_router.get("/get_grades/submission/{submission_id}", response_model=schemas.ResponseAllGradesOfSubmission)
async def get_grades_for_submission(submission_id: int, db_session: AsyncSession = Depends(get_db)):
    service = GradesService(db_session)
    grades = await service.get_grades_for_submission(submission_id)
    return grades


@grade_router.post("/create_grading_criteria", response_model=schemas.ResponseCreateGradingCriteria)
async def create_grade(request: schemas.RequestCreateGradingCriteria, db_session: AsyncSession = Depends(get_db)):
    service = GradesService(db_session)
    return await service.create_grading_criteria(request)


@grade_router.get("/get_grading_criteria/{submission_id}", response_model=schemas.ResponseGradingCriteria)
async def get_grading_criteria(submission_id: int, db: AsyncSession = Depends(get_db)):
    service = GradesService(db)
    grading_criteria = await service.get_grading_criteria_for_submission(submission_id)
    return grading_criteria

