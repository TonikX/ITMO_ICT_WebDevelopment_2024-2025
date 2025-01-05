from typing import List
from students.k3341.Lemanov_Andrey.Lr3.app.api.v1.submissions import schemas
from students.k3341.Lemanov_Andrey.Lr3.app.io.repository.postgres.repositories.submissions_repository import \
    SubmissionsRepository
from sqlalchemy.ext.asyncio import AsyncSession


class SubmissionsService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.repository = SubmissionsRepository(db_session)

    async def create_submission(self, request: schemas.RequestCreateSubmission) -> schemas.ResponseCreateSubmission:

        submission_id = await self.repository.create_submission(request)
        return schemas.ResponseCreateSubmission(
            submission_id=submission_id,
        )

    async def get_submission_by_id(self, submission_id: int) -> schemas.ResponseSubmission:

        submission = await self.repository.get_submission_by_id(submission_id)
        if submission is None:
            raise Exception(f"Submission with ID {submission_id} not found.")

        return schemas.ResponseSubmission(
            submission=schemas.Submission(
                id=submission.id,
                content=submission.content,
                student_id=submission.student_id,
                assignment_id=submission.assignment_id
            )
        )

    async def get_all_submissions(self) -> schemas.ResponseAllSubmissions:

        submissions = await self.repository.get_all_submissions()
        return schemas.ResponseAllSubmissions(
            submissions=[
                schemas.Submission(id=submission.id,
                                   content=submission.content,
                                   student_id=submission.student_id,
                                   assignment_id=submission.assignment_id) for submission in
                submissions]
        )

    async def delete_submission(self, submission_id: int) -> bool:

        return await self.repository.delete_submission(submission_id)

    async def update_submission(self, request: schemas.RequestUpdateSubmission) -> schemas.ResponseSubmission:

        updated_submission = await self.repository.update_submission(request)
        if updated_submission is None:
            raise Exception(f"Submission with ID {request.id} not found.")
        return schemas.ResponseSubmission(
            submission=schemas.Submission(id=updated_submission.id,
                                          content=updated_submission.content,
                                          student_id=updated_submission.student_id,
                                          assignment_id=updated_submission.assignment_id)
        )
