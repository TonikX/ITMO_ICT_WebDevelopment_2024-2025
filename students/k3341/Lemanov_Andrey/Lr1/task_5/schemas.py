from pydantic import BaseModel


class Discipline(BaseModel):
    description: str
    mark: int


class Response(BaseModel):
    code: int
    message: str
    headers: dict
    body: str