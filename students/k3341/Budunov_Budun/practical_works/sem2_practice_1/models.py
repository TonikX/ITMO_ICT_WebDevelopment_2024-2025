from enum import Enum
from typing import Optional, List

from pydantic import BaseModel

# User schemas
class User(BaseModel):
    id: int
    username: str
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


# Category schemas
class Category(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


# Task schemas
class Task(BaseModel):
    id: int
    description: str
    priority: int
    user: Optional[User] = None
    category: Optional[Category] = None