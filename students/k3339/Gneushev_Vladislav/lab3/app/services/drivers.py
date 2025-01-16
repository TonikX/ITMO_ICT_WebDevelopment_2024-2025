from datetime import datetime, timedelta

from app.domain.entities.assignments import DayOfWeek
from app.domain.entities.drivers import Driver, DriverClass, DriverWorkSchedule
from app.domain.entities.schedule import DayWorkingHours
from app.infrastructure.database.repositories.assignments import AssignmentRepository
from app.infrastructure.database.repositories.drivers import DriverRepository
from app.services.exceptions import EntityNotFound


class DriverService:
    def __init__(
            self,
            driver_repo: DriverRepository,
            assignment_repo: AssignmentRepository
    ):
        self.driver_repo = driver_repo
        self.assignment_repo = assignment_repo

    async def add_driver(self, driver: Driver) -> Driver:
        driver_class = await self.driver_repo.get_driver_class_by_name(driver.driver_class.name)
        if driver_class:
            driver.driver_class = driver_class
        else:
            driver.driver_class = await self.add_driver_class(driver.driver_class)

        driver = await self.driver_repo.add_driver(driver)
        return driver

    async def get_drivers(self) -> list[Driver]:
        drivers = await self.driver_repo.get_drivers()
        for driver in drivers:
            driver.salary = await self.driver_repo.get_salary(
                work_experience_months=driver.work_experience_months,
                driver_class=driver.driver_class
            )
        return drivers

    async def delete_driver(self, driver_id: int):
        driver = await self.driver_repo.get_driver_by_id(driver_id)
        if not driver:
            raise EntityNotFound(
                entity=Driver,
                field_name='id',
                value=driver_id
            )
        await self.driver_repo.delete_driver(driver_id)

    async def add_driver_class(self, driver_class: DriverClass) -> DriverClass:
        return await self.driver_repo.add_driver_class(driver_class)

    async def get_driver_classes(self) -> list[DriverClass]:
        return await self.driver_repo.get_driver_classes()

    async def delete_driver_class(self, driver_class_id: int) -> None:
        driver_class = await self.driver_repo.get_driver_class_by_id(driver_class_id)
        if not driver_class:
            raise EntityNotFound(
                entity=DriverClass,
                field_name='id',
                value=driver_class_id
            )
        await self.driver_repo.delete_driver_class(driver_class_id)

    async def get_driver_work_schedule(self, driver_id: int) -> DriverWorkSchedule:
        driver = await self.driver_repo.get_driver_by_id(driver_id)
        if not driver:
            raise EntityNotFound(
                entity=Driver,
                field_name='id',
                value=driver_id
            )
        assignments = await self.assignment_repo.get_driver_active_assignments(driver_id)
        if not assignments:
            return DriverWorkSchedule(
                driver=driver,
                monday=None,
                tuesday=None,
                wednesday=None,
                thursday=None,
                friday=None,
                saturday=None,
                sunday=None
            )

        schedule = {day: None for day in DayOfWeek}

        for assignment in assignments:
            day = assignment.day_of_week
            route = assignment.route

            if schedule[day] is None:
                schedule[day] = DayWorkingHours(
                    start_time=route.start_time,
                    end_time=route.end_time
                )
            else:
                existing_hours = schedule[day]
                schedule[day] = DayWorkingHours(
                    start_time=min(existing_hours.start_time, route.start_time),
                    end_time=max(existing_hours.end_time, route.end_time)
                )

        return DriverWorkSchedule(
            driver=driver,
            monday=schedule[DayOfWeek.monday],
            tuesday=schedule[DayOfWeek.tuesday],
            wednesday=schedule[DayOfWeek.wednesday],
            thursday=schedule[DayOfWeek.thursday],
            friday=schedule[DayOfWeek.friday],
            saturday=schedule[DayOfWeek.saturday],
            sunday=schedule[DayOfWeek.sunday]
        )

    async def get_driver_classes_count(self) -> dict[DriverClass, int]:
        driver_classes = await self.driver_repo.get_driver_classes()
        driver_classes_count = {}
        for driver_class in driver_classes:
            count = await self.driver_repo.get_driver_count_by_class(driver_class.id)  # todo: убрать N + 1
            driver_classes_count[driver_class] = count
        return driver_classes_count
