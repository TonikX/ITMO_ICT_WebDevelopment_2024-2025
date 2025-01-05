from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from students.k3341.Lemanov_Andrey.Lr3.app.core.errors import NotFoundEntityError
from students.k3341.Lemanov_Andrey.Lr3.app.io.repository.postgres.models import models
from students.k3341.Lemanov_Andrey.Lr3.app.api.v1.submissions import schemas
from typing import List


class SubmissionsRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_submission(self, request: schemas.RequestCreateSubmission) -> int:
        async with self.db_session.begin():
            new_submission = models.Submission(
                content=request.submission.content,
                student_id=request.submission.student_id,
                assignment_id=request.submission.assignment_id
            )
            self.db_session.add(new_submission)

        await self.db_session.refresh(new_submission)
        return new_submission.id

    async def get_submission_by_id(self, submission_id: int) -> models.Submission:
        async with self.db_session.begin():
            result = await self.db_session.execute(
                select(models.Submission).filter(models.Submission.id == submission_id))
            submission = result.scalar_one_or_none()

            if submission:
                return submission
            raise NotFoundEntityError(entity="submission")

    async def get_all_submissions(self) -> List[models.Submission]:
        async with self.db_session.begin():
            result = await self.db_session.execute(select(models.Submission))
            submissions = result.scalars().all()

            return [
                schemas.Submission(
                    id=submission.id,
                    content=submission.content,
                    student_id=submission.student_id,
                    assignment_id=submission.assignment_id
                ) for submission in submissions
            ]

    async def delete_submission(self, submission_id: int) -> bool:
        submission = await self.get_submission_by_id(submission_id)

        if submission:
            async with self.db_session.begin():
                await self.db_session.delete(submission)
            await self.db_session.commit()
            return True
        raise NotFoundEntityError(entity="submission")

    async def update_submission(self, request: schemas.RequestUpdateSubmission) -> models.Submission:
        submission = await self.get_submission_by_id(request.id)

        if submission:
            async with self.db_session.begin():
                submission.content = request.new_content
                await self.db_session.commit()

            await self.db_session.refresh(submission)
            return submission
        raise NotFoundEntityError(entity="submission")
