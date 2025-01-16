from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.domain.entities.base import Entity
from app.domain.entities.buses import Bus
from app.domain.entities.drivers import Driver
from app.domain.entities.routes import Route


class EndAssignmentReason(str, Enum):
    driver_ill = "driver_ill"
    bus_broken = "bus_broken"
    route_canceled = "route_canceled"
    bus_write_off = "bus_write_off"
    other = "other"


class DayOfWeek(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


@dataclass
class DriverAssignment(Entity):
    id: int | None
    from_date: datetime
    to_date: datetime | None
    end_reason: EndAssignmentReason | None
    day_of_week: DayOfWeek
    driver: Driver
    route: Route
    bus: Bus
