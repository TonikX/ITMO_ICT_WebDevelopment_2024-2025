from sqlmodel import ARRAY, Column, Integer, SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING, ForwardRef
from datetime import datetime, timedelta
from pydantic import field_validator

if TYPE_CHECKING:
    from .models import Task, User, Category, Tag, Schedule, ScheduleTask

# Forward references to resolve circular dependencies
TaskRef = ForwardRef("Task")
UserRef = ForwardRef("User")
CategoryRef = ForwardRef("Category")
TagRef = ForwardRef("Tag")
ScheduleRef = ForwardRef("Schedule")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    
    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")
    schedules: List["Schedule"] = Relationship(back_populates="user")


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    
    # Relationships
    tasks: List["Task"] = Relationship(back_populates="category")


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    
    # Relationships
    tasks: List["TaskTag"] = Relationship(back_populates="tag")


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    deadline: datetime
    priority: int = Field(ge=1, le=10)  # Assuming priority is 1-10
    start_time: Optional[datetime] = Field(default=None)
    end_time: Optional[datetime] = Field(default=None)

    # Foreign keys
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    @property
    def tag_ids(self) -> List[int]:
        """Return a list of tag IDs associated with this task."""
        return [tag_link.tag_id for tag_link in self.tags]
    
    # Relationships
    user: Optional["User"] = Relationship(back_populates="tasks")
    category: Optional["Category"] = Relationship(back_populates="tasks")
    tags: List["TaskTag"] = Relationship(back_populates="task")
    schedules: List["ScheduleTask"] = Relationship(back_populates="task")
    
    @field_validator("priority")
    def validate_priority(cls, v):
        if not 1 <= v <= 10:
            raise ValueError("Priority must be between 1 and 10")
        return v
    
    @field_validator("end_time")
    def validate_end_time(cls, v, values):
        if v and "start_time" in values.data and values.data["start_time"] and v < values.data["start_time"]:
            raise ValueError("End time must be after start time")
        return v


class TaskTag(SQLModel, table=True):
    task_id: Optional[int] = Field(
        default=None, foreign_key="task.id", primary_key=True
    )
    tag_id: Optional[int] = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )
    added_at: datetime = Field(default_factory=datetime.now)
    
    # Relationships
    task: "Task" = Relationship(back_populates="tags")
    tag: "Tag" = Relationship(back_populates="tasks")


class Schedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime
    
    # Foreign keys
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relationships
    user: "User" = Relationship(back_populates="schedules")
    tasks: List["ScheduleTask"] = Relationship(back_populates="schedule")


class ScheduleTask(SQLModel, table=True):
    schedule_id: Optional[int] = Field(
        default=None, foreign_key="schedule.id", primary_key=True
    )
    task_id: Optional[int] = Field(
        default=None, foreign_key="task.id", primary_key=True
    )
    planned_start: Optional[datetime] = None
    planned_duration: Optional[timedelta] = None
    
    # Relationships
    schedule: "Schedule" = Relationship(back_populates="tasks")
    task: "Task" = Relationship(back_populates="schedules")


# Resolve forward references
Task.model_rebuild()
User.model_rebuild()
Category.model_rebuild()
Tag.model_rebuild()
Schedule.model_rebuild()
TaskTag.model_rebuild()
ScheduleTask.model_rebuild()
