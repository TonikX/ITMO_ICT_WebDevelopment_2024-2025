from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from students.k3341.Lemanov_Andrey.Lr3.app.io.repository.postgres.repositories.assignments_repository import \
    AssignmentsRepository
from students.k3341.Lemanov_Andrey.Lr3.app.api.v1.assigments import schemas


class AssignmentsService:
    def __init__(self, db_session: AsyncSession):
        self.repository = AssignmentsRepository(db_session)

    async def create_assignment(self, request: schemas.RequestCreateAssignment) -> schemas.ResponseCreateAssignment:
        return schemas.ResponseCreateAssignment(assignment_id=await self.repository.create_assignment(request))

    async def get_assignment_by_id(self, assignment_id: int) -> schemas.ResponseAssignment:
        assignment = await self.repository.get_assignment_by_id(assignment_id)
        return schemas.ResponseAssignment(
            assignment=schemas.Assignment(id=assignment.id,
                                          title=assignment.title, description=assignment.description))

    async def get_all_assignments(self) -> schemas.ResponseAllAssignments:
        assignments = await self.repository.get_all_assignments()
        return schemas.ResponseAllAssignments(assignments=[
            schemas.Assignment(id=assignment.id, title=assignment.title, description=assignment.description) for
            assignment in assignments])

    async def update_assignment(self, request: schemas.RequestUpdateAssignment) -> schemas.ResponseAssignment:
        new_assignment = await self.repository.update_assignment(request)
        return schemas.ResponseAssignment(
            assignment=schemas.Assignment(id=new_assignment.id, title=new_assignment.title,
                                          description=new_assignment.description))

    async def delete_assignment(self, assignment_id: int) -> schemas.ResponseDeleteAssignment:
        is_deleted = await self.repository.delete_assignment(assignment_id)
        return schemas.ResponseDeleteAssignment(assignment_id=assignment_id)
