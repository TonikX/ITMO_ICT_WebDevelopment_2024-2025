from app.domain.entities.buses import Bus, BusType
from app.infrastructure.database.models import BusDB, BusTypeDB


def from_bus_type_dm_to_db(entity: BusType) -> BusTypeDB:
    return BusTypeDB(
        id=entity.id,
        name=entity.name,
        people_capacity=entity.people_capacity
    )


def from_bus_dm_to_db(entity: Bus) -> BusDB:
    return BusDB(
        id=entity.id,
        state_number=entity.state_number,
        bus_type_id=entity.bus_type.id
    )


def from_bus_type_db_to_dm(model: BusTypeDB) -> BusType:
    return BusType(
        id=model.id,
        name=model.name,
        people_capacity=model.people_capacity
    )


def from_bus_db_to_dm(model: BusDB) -> Bus:
    return Bus(
        id=model.id,
        state_number=model.state_number,
        bus_type=from_bus_type_db_to_dm(model.bus_type)
    )
