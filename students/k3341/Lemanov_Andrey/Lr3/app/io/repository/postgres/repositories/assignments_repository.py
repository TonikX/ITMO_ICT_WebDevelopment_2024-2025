from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from students.k3341.Lemanov_Andrey.Lr3.app.core.errors import NotFoundEntityError
from students.k3341.Lemanov_Andrey.Lr3.app.io.repository.postgres.models import models
from students.k3341.Lemanov_Andrey.Lr3.app.api.v1.assigments import schemas
from typing import List


class AssignmentsRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_assignment(self, request: schemas.RequestCreateAssignment) -> int:
        async with self.db_session.begin():
            new_assignment = models.Assignment(
                title=request.assignment.title,
                description=request.assignment.description,
                teacher_id=request.teacher_id
            )
            self.db_session.add(new_assignment)

        await self.db_session.refresh(new_assignment)
        return new_assignment.id

    async def get_assignment_by_id(self, assignment_id: int) -> models.Assignment:
        async with self.db_session.begin():
            result = await self.db_session.execute(
                select(models.Assignment).filter(models.Assignment.id == assignment_id))
            assignment = result.scalar_one_or_none()

            if not assignment:
                raise NotFoundEntityError(entity="assignment")

            return models.Assignment(
                id=assignment.id,
                title=assignment.title,
                description=assignment.description
            )

    async def get_all_assignments(self) -> List[models.Assignment]:
        async with self.db_session.begin():
            result = await self.db_session.execute(select(models.Assignment))
            assignments = result.scalars().all()
            return [
                models.Assignment(
                    id=assignment.id,
                    title=assignment.title,
                    description=assignment.description
                ) for assignment in assignments
            ]

    async def update_assignment(self, request: schemas.RequestUpdateAssignment) -> models.Assignment:
        async with self.db_session.begin():
            result = await self.db_session.execute(
                select(models.Assignment).filter(models.Assignment.id == request.assignment.id)
            )
            assignment = result.scalar_one_or_none()

            if assignment:
                if request.assignment.title is not None:
                    assignment.title = request.assignment.title
                if request.assignment.description is not None:
                    assignment.description = request.assignment.description
                if request.teacher_id is not None:
                    assignment.teacher_id = request.teacher_id

                await self.db_session.commit()
                return assignment
        raise NotFoundEntityError(entity="assignment")

    async def delete_assignment(self, assignment_id: int) -> bool:
        async with self.db_session.begin():
            result = await self.db_session.execute(
                select(models.Assignment).filter(models.Assignment.id == assignment_id)
            )
            assignment = result.scalar_one_or_none()

            if assignment:
                await self.db_session.delete(assignment)
                await self.db_session.commit()
                return True
        raise NotFoundEntityError(entity="assignment")
