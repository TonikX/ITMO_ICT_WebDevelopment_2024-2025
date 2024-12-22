from pydantic import BaseModel
from typing import Optional, List


class AuthUser(BaseModel):
    name: str
    surname: str
    password: str
    user_role: str


class UserInDB(AuthUser):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class Teacher(BaseModel):
    name: str
    surname: str


class Assignment(BaseModel):
    title: str
    description: str


class Submission(BaseModel):
    content: str
    student_id: int
    assignment_id: int


class Grade(BaseModel):
    grade: float
    student_id: int
    submission_id: int
    criteria_id: int


class GradingCriteria(BaseModel):
    criterion_name: str
    max_points: float
    assignment_id: int


class RequestAssignment(BaseModel):
    assignment: Assignment
    teacher_id: int


class RequestTeacher(BaseModel):
    teacher: Teacher


class RequestSubmission(BaseModel):
    submission: Submission


class RequestGrade(BaseModel):
    grade: float
    student_id: int
    submission_id: int
    criteria_id: int

    class Config:
        orm_mode = True


class GradeResponse(BaseModel):
    id: int
    grade: float
    student_id: int
    submission_id: int
    criteria_id: int

    class Config:
        orm_mode = True


# Response schemas for related entities (Student, Submission, GradingCriteria)
class StudentResponse(BaseModel):
    id: int
    name: str
    surname: str

    class Config:
        orm_mode = True


class SubmissionResponse(BaseModel):
    id: int
    content: str

    class Config:
        orm_mode = True


class GradingCriteriaResponse(BaseModel):
    id: int
    criterion_name: str
    max_points: float
    assignment_id: int

    class Config:
        orm_mode = True


# Full response for Grade including related entities (with relationships)
class GradeWithRelationshipsResponse(BaseModel):
    id: int
    grade: float
    student: StudentResponse
    submission: SubmissionResponse
    grading_criteria: GradingCriteriaResponse

    class Config:
        orm_mode = True


# Repository schema to return lists of grades
class GradeListResponse(BaseModel):
    grades: List[GradeResponse]

    class Config:
        orm_mode = True


# GradingCriteria response for a submissions
class GradingCriteriaForSubmissionResponse(BaseModel):
    id: int
    criterion_name: str
    max_points: float
    assignment_id: int

    class Config:
        orm_mode = True


class GradesForSubmissionResponse(BaseModel):
    grades: List[GradeResponse]

    class Config:
        orm_mode = True
