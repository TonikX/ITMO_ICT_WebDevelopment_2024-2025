from dataclasses import dataclass

from app.domain.entities.base import Entity


@dataclass
class BusType(Entity):
    id: int | None
    name: str
    people_capacity: int


@dataclass
class Bus(Entity):
    id: int | None
    state_number: str
    bus_type: BusType
