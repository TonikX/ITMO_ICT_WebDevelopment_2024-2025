from adaptix import P
from adaptix._internal.conversion.facade.provider import allow_unlinked_optional

from app.domain.entities.drivers import Driver
from app.infrastructure.database.converters.universal import from_db_to_entity
from app.infrastructure.database.models import DriverDB


def from_driver_dm_to_db(entity: Driver) -> DriverDB:
    return DriverDB(
        id=entity.id,
        first_name=entity.first_name,
        last_name=entity.last_name,
        passport_info=entity.passport_info,
        driver_class_id=entity.driver_class.id,
        work_experience_months=entity.work_experience_months
    )


def from_driver_db_to_dm(model: DriverDB) -> Driver:
    return from_db_to_entity(
        db_obj=model,
        entity_cls=Driver,
        options=[allow_unlinked_optional(P[Driver].salary)]
    )
