from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from students.k3341.Lemanov_Andrey.Lr3.app.core.errors import NotFoundEntityError
from students.k3341.Lemanov_Andrey.Lr3.app.io.repository.postgres.models import models
from students.k3341.Lemanov_Andrey.Lr3.app.api.v1.grades import schemas
from typing import List, Optional


class GradesRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_grade(self, request: schemas.RequestCreateGrade) -> int:
        async with self.db_session.begin():
            grade = models.Grade(
                grade=request.grade.grade,
                student_id=request.grade.student_id,
                submission_id=request.grade.submission_id,
                criteria_id=request.grade.criteria_id
            )
            self.db_session.add(grade)

        await self.db_session.refresh(grade)
        return grade.id

    async def get_grades_by_student_id(self, student_id: int) -> List[models.Grade]:
        async with self.db_session.begin():
            result = await self.db_session.execute(
                select(models.Grade).filter(models.Grade.student_id == student_id)
            )
            grades = result.scalars().all()
            if grades:
                return [
                    models.Grade(
                        id=grade.id,
                        grade=grade.grade,
                        student_id=grade.student_id,
                        submission_id=grade.submission_id,
                        criteria_id=grade.criteria_id
                    ) for grade in grades
                ]

        raise NotFoundEntityError(entity="grades")

    async def get_grades_for_submission(self, submission_id: int) -> List[models.Grade]:
        async with self.db_session.begin():
            result = await self.db_session.execute(
                select(models.Grade).filter(models.Grade.submission_id == submission_id)
            )
            grades = result.scalars().all()
            return [
                models.Grade(
                    id=grade.id,
                    grade=grade.grade,
                    student_id=grade.student_id,
                    submission_id=grade.submission_id,
                    criteria_id=grade.criteria_id
                ) for grade in grades
            ]

    async def create_grading_criteria(self, request: schemas.RequestCreateGradingCriteria) -> int:
        async with self.db_session.begin():
            grading_criteria = models.GradingCriteria(
                criterion_name=request.grade_criteria.criterion_name,
                max_points=request.grade_criteria.max_points,
                assignment_id=request.grade_criteria.assignment_id
            )
            self.db_session.add(grading_criteria)

        await self.db_session.refresh(grading_criteria)
        return grading_criteria.id

    async def get_grade_with_relationships(self, grade_id: int) -> schemas.ResponseGradeWithRelationships:
        async with self.db_session.begin():
            result = await self.db_session.execute(
                select(models.Grade)
                .options(
                    joinedload(models.Grade.student),
                    joinedload(models.Grade.submission),
                    joinedload(models.Grade.criteria)
                )
                .filter(models.Grade.id == grade_id)
            )
            grade = result.scalar_one_or_none()

            if grade:
                return schemas.ResponseGradeWithRelationships(
                    id=grade.id,
                    grade=grade.grade,
                    student=schemas.Student(
                        id=grade.student.id,
                        name=grade.student.name,
                        surname=grade.student.surname
                    ),
                    submission=schemas.Submission(
                        id=grade.submission.id,
                        content=grade.submission.content,
                        student_id=grade.submission.student_id,
                        assignment_id=grade.criteria.assignment_id
                    ),
                    grading_criteria=schemas.GradingCriteria(
                        id=grade.criteria.id,
                        criterion_name=grade.criteria.criterion_name,
                        max_points=grade.criteria.max_points,
                        assignment_id=grade.criteria.assignment_id
                    )
                )
            raise NotFoundEntityError(entity="grade")
