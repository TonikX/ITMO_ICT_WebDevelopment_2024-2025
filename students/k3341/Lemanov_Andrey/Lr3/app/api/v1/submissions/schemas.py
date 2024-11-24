from pydantic import BaseModel
from typing import Optional, List


class Submission(BaseModel):
    id: int
    content: str
    student_id: int
    assignment_id: int


class RequestCreateSubmission(BaseModel):
    submission: Submission


class ResponseCreateSubmission(BaseModel):
    submission_id: int


class RequestUpdateSubmission(BaseModel):
    id: int
    new_content: str


class ResponseSubmission(BaseModel):
    submission: Submission


class ResponseAllSubmissions(BaseModel):
    submissions: List[Submission]
