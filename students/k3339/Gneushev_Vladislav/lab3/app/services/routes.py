from app.domain.entities.assignments import DayOfWeek
from app.domain.entities.routes import Route, RouteWorkSchedule
from app.domain.entities.schedule import DayWorkingHours
from app.infrastructure.database.repositories.assignments import AssignmentRepository
from app.infrastructure.database.repositories.routes import RouteRepository
from app.services.exceptions import EntityNotFound


class RouteService:
    def __init__(self, route_repo: RouteRepository, assignment_repo: AssignmentRepository):
        self.route_repo = route_repo
        self.assignment_repo = assignment_repo

    async def get_routes(self) -> list[Route]:
        return await self.route_repo.get_routes()

    async def add_route(self, route: Route) -> Route:
        return await self.route_repo.add_route(route)

    async def delete_route(self, route_id: int) -> None:
        route = await self.route_repo.get_route_by_id(route_id)
        if not route:
            raise EntityNotFound(
                entity=Route,
                field_name='id',
                value=route_id
            )
        await self.route_repo.delete_route(route_id)

    async def get_route_schedules(self) -> list[RouteWorkSchedule]:
        routes = await self.route_repo.get_routes()
        assignments = await self.assignment_repo.get_assignments(active=True)
        if not routes:
            return []

        route_schedules = {
            route.id: {day: None for day in DayOfWeek} for route in routes
        }

        for assignment in assignments:
            route_id = assignment.route.id
            day = assignment.day_of_week
            route = assignment.route

            if route_schedules[route_id][day] is None:
                route_schedules[route_id][day] = DayWorkingHours(
                    start_time=route.start_time,
                    end_time=route.end_time
                )
            else:
                existing_hours = route_schedules[route_id][day]
                route_schedules[route_id][day] = DayWorkingHours(
                    start_time=min(existing_hours.start_time, route.start_time),
                    end_time=max(existing_hours.end_time, route.end_time)
                )

        route_work_schedules = []
        for route in routes:
            schedule = route_schedules[route.id]
            route_work_schedules.append(RouteWorkSchedule(
                route=route,
                monday=schedule[DayOfWeek.monday],
                tuesday=schedule[DayOfWeek.tuesday],
                wednesday=schedule[DayOfWeek.wednesday],
                thursday=schedule[DayOfWeek.thursday],
                friday=schedule[DayOfWeek.friday],
                saturday=schedule[DayOfWeek.saturday],
                sunday=schedule[DayOfWeek.sunday]
            ))

        return route_work_schedules

    async def get_total_length(self) -> int:
        return await self.route_repo.get_total_length()
