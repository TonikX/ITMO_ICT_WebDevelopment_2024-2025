from pydantic import BaseModel
from typing import Optional, List


class Assignment(BaseModel):
    id: int
    title: str
    description: str


class RequestCreateAssignment(BaseModel):
    assignment: Assignment
    teacher_id: int


class ResponseCreateAssignment(BaseModel):
    assignment_id: int


class RequestUpdateAssignment(BaseModel):
    teacher_id: int
    assignment: Assignment


class ResponseAssignment(BaseModel):
    assignment: Assignment


class ResponseAllAssignments(BaseModel):
    assignments: List[Assignment]


class ResponseDeleteAssignment(BaseModel):
    assignment_id: int
