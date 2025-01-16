from dataclasses import dataclass
from datetime import time

from app.domain.entities.base import Entity


@dataclass
class DayWorkingHours:
    start_time: time
    end_time: time


@dataclass
class WorkSchedule(Entity):
    monday: DayWorkingHours | None
    tuesday: DayWorkingHours | None
    wednesday: DayWorkingHours | None
    thursday: DayWorkingHours | None
    friday: DayWorkingHours | None
    saturday: DayWorkingHours | None
    sunday: DayWorkingHours | None
