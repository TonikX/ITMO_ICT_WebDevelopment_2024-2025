from students.k3341.Lemanov_Andrey.Lr3.app.api.v1.grades import schemas
from students.k3341.Lemanov_Andrey.Lr3.app.io.repository.postgres.models import models
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from students.k3341.Lemanov_Andrey.Lr3.app.io.repository.postgres.repositories.grades_repository import GradesRepository


class GradesService:
    def __init__(self, db_session: AsyncSession):
        self.grades_repository = GradesRepository(db_session)

    async def create_grade(self, grade_data: schemas.RequestCreateGrade) -> schemas.ResponseCreateGrade:
        grade_id = await self.grades_repository.create_grade(grade_data)
        return schemas.ResponseCreateGrade(grade_id=grade_id)

    async def get_grade_by_id(self, grade_id: int) -> Optional[schemas.ResponseGradeWithRelationships]:
        grade = await self.grades_repository.get_grade_with_relationships(grade_id)
        return grade

    async def get_grades_by_student_id(self, student_id: int) -> schemas.ResponseAllGradesOfStudent:
        grades = await self.grades_repository.get_grades_by_student_id(student_id)

        return schemas.ResponseAllGradesOfStudent(grades=[
            schemas.Grade(
                grade=grade.grade,
                student_id=grade.student_id,
                submission_id=grade.submission_id,
                criteria_id=grade.criteria_id
            ) for grade in grades])

    async def get_grades_for_submission(self, submission_id: int) -> schemas.ResponseAllGradesOfSubmission:
        grades = await self.grades_repository.get_grades_for_submission(submission_id)
        return schemas.ResponseAllGradesOfSubmission(grades=[
            schemas.Grade(
                grade=grade.grade,
                student_id=grade.student_id,
                submission_id=grade.submission_id,
                criteria_id=grade.criteria_id
            ) for grade in grades
        ])

    async def get_grading_criteria_for_submission(self, submission_id: int) -> Optional[schemas.GradingCriteria]:
        grading_criteria = await self.grades_repository.get_grading_criteria_for_submission(submission_id)
        if grading_criteria:
            return schemas.GradingCriteria(
                id=grading_criteria.id,
                criterion_name=grading_criteria.criterion_name,
                max_points=grading_criteria.max_points,
                assignment_id=grading_criteria.assignment_id
            )
        return None

    async def create_grading_criteria(self,
                                      request: schemas.RequestCreateGradingCriteria) -> schemas.ResponseCreateGradingCriteria:
        grading_criteria_id = await self.grades_repository.create_grading_criteria(request)
        return schemas.ResponseCreateGradingCriteria(grading_criteria_id=grading_criteria_id)
