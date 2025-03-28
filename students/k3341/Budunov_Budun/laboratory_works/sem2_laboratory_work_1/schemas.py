from datetime import datetime, timezone, timedelta
from typing import List, Optional, ForwardRef
from pydantic import BaseModel, field_validator, constr, computed_field


# Forward references
TaskReadRef = ForwardRef("TaskRead")
TaskTagReadRef = ForwardRef("TaskTagRead")
CategoryReadRef = ForwardRef("CategoryRead")
TagReadRef = ForwardRef("TagRead")
ScheduleReadRef = ForwardRef("ScheduleRead")


# User schemas
class UserBase(BaseModel):
    username: str = constr(min_length=3, max_length=50)


class UserCreate(UserBase):
    password: str = constr(min_length=8)


class UserRead(UserBase):
    id: int
    username: str
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    created_at: Optional[datetime] = None
    hashed_password: Optional[str] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None


class UserPasswordChange(BaseModel):
    current_password: str
    new_password: str = constr(min_length=8)

# Схема для отображения пользователей с количеством задач
class UserWithTaskCount(UserRead):
    task_count: int


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# Category schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int


# Tag schemas
class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int

# Task schemas
class TaskBase(BaseModel):
    description: str
    deadline: datetime
    priority: int
    
    # @field_validator("deadline")
    # def deadline_not_in_past(cls, value):
    #     now = datetime.now(timezone.utc)
    #     if value.replace(tzinfo=timezone.utc) < now:
    #         raise ValueError("Deadline cannot be in the past")
    #     return value

    @field_validator("priority")
    def priority_range(cls, v):
        if v < 1 or v > 10:  # Updated to match model's 1-10 range
            raise ValueError("Priority must be between 1 and 10")
        return v


class TaskCreate(TaskBase):
    user_id: int
    category_id: Optional[int] = None
    tag_ids: List[int] = []  # List of tag IDs


class TaskUpdate(BaseModel):
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: Optional[int] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None


class TaskRead(TaskBase):
    id: int
    user: UserRead
    category: Optional[CategoryRead] = None
    tags: List[TagRead] = []
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    @computed_field
    def time_spent_minutes(self) -> Optional[int]:
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            return int(delta.total_seconds() // 60)  # Convert to minutes and round down
        return None
    
    @computed_field
    def is_active(self) -> bool:
        return self.start_time is not None and self.end_time is None


# Task action schemas
class TaskStartAction(BaseModel):
    start_time: Optional[datetime] = None  # If not provided, current time will be used


class TaskEndAction(BaseModel):
    end_time: Optional[datetime] = None  # If not provided, current time will be used


# Schedule schemas
class ScheduleBase(BaseModel):
    date: datetime


class ScheduleCreate(ScheduleBase):
    user_id: int
    task_ids: List[int] = []


class ScheduleRead(ScheduleBase):
    id: int
    user: UserRead
    tasks: List[TaskRead] = []


# TaskTag schema
class TaskTagRead(BaseModel):
    task_id: int
    tag_id: int
    added_at: datetime


# ScheduleTask schema
class ScheduleTaskBase(BaseModel):
    planned_start: Optional[datetime] = None
    planned_duration: Optional[timedelta] = None
    
    @computed_field
    def planned_duration_minutes(self) -> Optional[int]:
        if self.planned_duration:
            return int(self.planned_duration.total_seconds() // 60)  # Convert to minutes
        return None


class ScheduleTaskCreate(ScheduleTaskBase):
    task_id: int
    schedule_id: int


class ScheduleTaskRead(ScheduleTaskBase):
    task: TaskRead
    schedule: ScheduleRead


# Resolve forward references
TaskRead.model_rebuild()
CategoryRead.model_rebuild()
TagRead.model_rebuild()
ScheduleRead.model_rebuild()
TaskTagRead.model_rebuild()