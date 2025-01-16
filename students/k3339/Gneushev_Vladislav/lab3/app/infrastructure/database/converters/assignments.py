from app.domain.entities.assignments import DriverAssignment, EndAssignmentReason, DayOfWeek
from app.domain.entities.drivers import Driver
from app.infrastructure.database.converters.buses import from_bus_db_to_dm
from app.infrastructure.database.converters.drivers import from_driver_db_to_dm
from app.infrastructure.database.converters.routes import from_route_db_to_dm
from app.infrastructure.database.converters.universal import from_db_to_entity
from app.infrastructure.database.models import DriverAssignmentDB


def from_assignment_dm_to_db(assignment: DriverAssignment) -> DriverAssignmentDB:
    return DriverAssignmentDB(
        id=assignment.id,
        from_date=assignment.from_date,
        to_date=assignment.to_date,
        end_reason=assignment.end_reason,
        day_of_week=assignment.day_of_week,
        bus_id=assignment.bus.id,
        route_id=assignment.route.id,
        driver_id=assignment.driver.id,
    )


def from_assignment_db_to_dm(assignment: DriverAssignmentDB) -> DriverAssignment:
    return DriverAssignment(
        id=assignment.id,
        from_date=assignment.from_date,
        to_date=assignment.to_date,
        end_reason=EndAssignmentReason(assignment.end_reason) if assignment.end_reason else None,
        day_of_week=DayOfWeek(assignment.day_of_week),
        bus=from_bus_db_to_dm(assignment.bus),
        route=from_route_db_to_dm(assignment.route),
        driver=from_driver_db_to_dm(assignment.driver),
    )
