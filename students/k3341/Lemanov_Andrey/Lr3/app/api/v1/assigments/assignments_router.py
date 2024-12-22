from fastapi import Header, Depends
from typing import Annotated, Union

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from students.k3341.Lemanov_Andrey.Lr3.app.io.repository.postgres.database import get_db
from students.k3341.Lemanov_Andrey.Lr3.app.api.v1.assigments import schemas
from students.k3341.Lemanov_Andrey.Lr3.app.core.services.assignments_service import AssignmentsService

assignments_router = APIRouter()


@assignments_router.post("/create_assignment", response_model=schemas.ResponseCreateAssignment)
async def create_assignment(request: schemas.RequestCreateAssignment, db_session: AsyncSession = Depends(get_db)):
    service = AssignmentsService(db_session)
    return await service.create_assignment(request)


@assignments_router.get("/get_assignment/{assignment_id}", response_model=schemas.ResponseAssignment)
async def get_assignment(assignment_id: int, db_session: AsyncSession = Depends(get_db)):
    service = AssignmentsService(db_session)
    return await service.get_assignment_by_id(assignment_id)


@assignments_router.get("/get_all_assignments", response_model=schemas.ResponseAllAssignments)
async def get_all_assignments(db_session: AsyncSession = Depends(get_db)):
    service = AssignmentsService(db_session)
    return await service.get_all_assignments()


@assignments_router.put("/update_assignment", response_model=schemas.ResponseAssignment)
async def update_assignment(request: schemas.RequestUpdateAssignment, db_session: AsyncSession = Depends(get_db)):
    service = AssignmentsService(db_session)
    return await service.update_assignment(request)

'''
@assignments_router.delete("/delete_assignment/{assignment_id}", response_model=schemas.ResponseAssignment)
async def update_assignment(assignment_id: int, db_session: AsyncSession = Depends(get_db)):
    service = AssignmentsService(db_session)
    return await service.delete_assignment(assignment_id)
'''