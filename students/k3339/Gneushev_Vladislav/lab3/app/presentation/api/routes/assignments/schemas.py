from datetime import datetime
from enum import Enum, auto

from pydantic import BaseModel

from app.domain.entities.assignments import EndAssignmentReason, DayOfWeek
from app.presentation.api.routes.buses.schemas import GetBusSchema
from app.presentation.api.routes.drivers.schemas import GetDriverSchema
from app.presentation.api.routes.routes.schemas import GetRouteSchema


class GetAssignmentSchema(BaseModel):
    id: int
    from_date: datetime
    to_date: datetime | None
    end_reason: EndAssignmentReason | None
    day_of_week: DayOfWeek
    driver: GetDriverSchema
    route: GetRouteSchema
    bus: GetBusSchema


class AddAssignmentSchema(BaseModel):
    day_of_week: DayOfWeek
    driver_id: int
    route_id: int
    bus_id: int


class EndAssignmentSchema(BaseModel):
    reason: EndAssignmentReason
