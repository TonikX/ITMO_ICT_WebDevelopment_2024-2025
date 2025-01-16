import logging
from datetime import datetime, date

from app.domain.assignments import do_routes_shifts_intersect
from app.domain.entities.assignments import DriverAssignment, EndAssignmentReason, DayOfWeek
from app.domain.entities.buses import Bus
from app.domain.entities.drivers import Driver
from app.domain.entities.routes import Route, RouteWorkSchedule
from app.domain.entities.schedule import DayWorkingHours
from app.infrastructure.database.repositories.assignments import AssignmentRepository
from app.infrastructure.database.repositories.buses import BusRepository
from app.infrastructure.database.repositories.drivers import DriverRepository
from app.infrastructure.database.repositories.routes import RouteRepository
from app.services.exceptions import DriverHasActiveAssignment, EntityNotFound, AssignmentAlreadyEnded

logger = logging.getLogger(__name__)


class AssignmentService:
    def __init__(
            self,
            assignment_repo: AssignmentRepository,
            driver_repo: DriverRepository,
            route_repo: RouteRepository,
            bus_repo: BusRepository
    ):
        self.assignment_repo = assignment_repo
        self.driver_repo = driver_repo
        self.route_repo = route_repo
        self.bus_repo = bus_repo

    async def get_assignments(self, active: bool = None, route_id: int = None, ended_on_date: date = None) -> list[DriverAssignment]:
        return await self.assignment_repo.get_assignments(
            active=active,
            route_id=route_id,
            ended_on_date=ended_on_date
        )

    async def add_assignment(
            self,
            from_date: datetime,
            day_of_week: DayOfWeek,
            driver_id: int,
            route_id: int,
            bus_id: int
    ) -> DriverAssignment:
        driver = await self.driver_repo.get_driver_by_id(driver_id)
        if not driver:
            raise EntityNotFound(
                entity=Driver,
                field_name='id',
                value=driver_id
            )
        route = await self.route_repo.get_route_by_id(route_id)
        if not route:
            raise EntityNotFound(
                entity=Route,
                field_name='id',
                value=route_id
            )
        bus = await self.bus_repo.get_bus_by_id(bus_id)
        if not bus:
            raise EntityNotFound(
                entity=Bus,
                field_name='id',
                value=bus_id
            )

        driver_current_assigments = await self.assignment_repo.get_driver_active_assignments(
            driver_id=driver_id
        )
        for assignment in driver_current_assigments:
            if do_routes_shifts_intersect(
                route_1=assignment.route,
                route_2=route
            ) and assignment.day_of_week == day_of_week:
                raise DriverHasActiveAssignment()

        return await self.assignment_repo.add_assignment(
            DriverAssignment(
                id=None,
                from_date=from_date,
                end_reason=None,
                to_date=None,
                day_of_week=day_of_week,
                driver=driver,
                route=route,
                bus=bus
            )
        )

    async def delete_assignment(self, assignment_id: int) -> None:
        assignment = await self.assignment_repo.get_assignment_by_id(assignment_id)
        if not assignment:
            raise EntityNotFound(
                entity=DriverAssignment,
                field_name='id',
                value=assignment_id
            )
        await self.assignment_repo.delete_assignment(assignment_id)

    async def end_assignment(self, assignment_id: int, reason: EndAssignmentReason) -> DriverAssignment:
        assignment = await self.assignment_repo.get_assignment_by_id(assignment_id)
        if not assignment:
            raise EntityNotFound(
                entity=DriverAssignment,
                field_name='id',
                value=assignment_id
            )
        if assignment.to_date is not None:
            raise AssignmentAlreadyEnded()
        return await self.assignment_repo.end_assignment(
            assignment_id=assignment_id,
            end_reason=reason
        )
