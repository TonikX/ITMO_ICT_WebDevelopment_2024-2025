from pydantic import BaseModel
from typing import Optional, List


class Grade(BaseModel):
    grade: float
    student_id: int
    submission_id: int
    criteria_id: int


class Student(BaseModel):
    id: int
    name: str
    surname: str


class Submission(BaseModel):
    id: int
    content: str
    student_id: int
    assignment_id: int


class GradingCriteria(BaseModel):
    id: int
    criterion_name: str
    max_points: float
    assignment_id: int


class CreateGradingCriteria(BaseModel):
    criterion_name: str
    max_points: float
    assignment_id: int


class RequestCreateGradingCriteria(BaseModel):
    grade_criteria: CreateGradingCriteria


class ResponseCreateGradingCriteria(BaseModel):
    grading_criteria_id: int


class RequestCreateGrade(BaseModel):
    grade: Grade


class ResponseCreateGrade(BaseModel):
    grade_id: int


class ResponseGradingCriteria(BaseModel):
    grading_criteria: GradingCriteria


class RequestUpdateGrade(BaseModel):
    grade_id: int
    new_grade: Grade


class RequestUpdateGradingCriteria(BaseModel):
    grade_criteria_id: int
    new_grade_criteria: CreateGradingCriteria


class ResponseGrade(BaseModel):
    grade_id: int
    grade: Grade


class ResponseAllGradesOfStudent(BaseModel):
    grades: List[Grade]


class ResponseAllGradesOfSubmission(BaseModel):
    grades: List[Grade]


class ResponseGradeWithRelationships(BaseModel):
    id: int
    grade: float
    student: Student
    submission: Submission
    grading_criteria: GradingCriteria
