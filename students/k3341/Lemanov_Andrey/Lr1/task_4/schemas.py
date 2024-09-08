from pydantic import BaseModel


class Message(BaseModel):
    user_id: int
    message: str
