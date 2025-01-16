from dataclasses import dataclass

from app.domain.entities.base import Entity
from app.domain.entities.schedule import WorkSchedule


@dataclass
class DriverClass(Entity):
    id: int | None
    name: str

    def __hash__(self):
        return hash(self.id)


@dataclass
class DriverSalary(Entity):
    id: int | None
    work_experience_over_months: int
    driver_class: DriverClass
    salary_rub: int


@dataclass
class Driver(Entity):
    id: int | None
    first_name: str
    last_name: str
    passport_info: str
    driver_class: DriverClass
    work_experience_months: int
    salary: DriverSalary | None = None


@dataclass
class DriverWorkSchedule(WorkSchedule):
    driver: Driver
