from datetime import time

from pydantic import BaseModel


class GetDriverClassSchema(BaseModel):
    id: int
    name: str


class AddDriverClassSchema(BaseModel):
    name: str


class GetDriverSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    passport_info: str
    work_experience_months: int
    driver_class: GetDriverClassSchema
    salary_rub: int | None = None


class AddDriverSchema(BaseModel):
    driver_class_name: str
    first_name: str
    last_name: str
    passport_info: str
    work_experience_months: int


class DayWorkingHoursSchema(BaseModel):
    start_time: time
    end_time: time


class GetWorkScheduleSchema(BaseModel):
    monday: DayWorkingHoursSchema | None
    tuesday: DayWorkingHoursSchema | None
    wednesday: DayWorkingHoursSchema | None
    thursday: DayWorkingHoursSchema | None
    friday: DayWorkingHoursSchema | None
    saturday: DayWorkingHoursSchema | None
    sunday: DayWorkingHoursSchema | None


class ClassDriversCountSchema(BaseModel):
    driver_class: GetDriverClassSchema
    count: int


class DriverClassesCountSchema(BaseModel):
    driver_classes: list[ClassDriversCountSchema]
