from adaptix import P
from adaptix.conversion import allow_unlinked_optional

from sqlalchemy import delete, select, func

from app.domain.entities.drivers import Driver, DriverClass, DriverSalary
from app.infrastructure.database.converters.drivers import from_driver_dm_to_db, from_driver_db_to_dm
from app.infrastructure.database.converters.universal import from_db_to_entity
from app.infrastructure.database.models import DriverDB, DriverClassDB, DriverSalaryDB
from app.infrastructure.database.repositories.base import BaseRepository


class DriverRepository(BaseRepository):
    async def add_driver(self, driver: Driver) -> Driver:
        driver_db = from_driver_dm_to_db(driver)
        self.session.add(driver_db)
        await self.session.commit()
        await self.session.refresh(driver_db)
        return from_driver_db_to_dm(driver_db)

    async def get_drivers(self) -> list[Driver]:
        q = select(DriverDB)
        result = await self.session.execute(q)
        drivers = result.unique().scalars().all()
        return [
            from_driver_db_to_dm(driver)
            for driver in drivers
        ]

    # async def get_drivers(self) -> list[Driver]:
    #     DriverSalaryAlias = aliased(DriverSalaryDB)
    #
    #     subquery = (
    #         select(DriverSalaryAlias.id, DriverSalaryAlias.salary_rub)
    #         .where(DriverSalaryAlias.driver_class_id == DriverDB.driver_class_id)
    #         .where(DriverSalaryAlias.work_experience_over_months <= DriverDB.work_experience_months)
    #         .order_by(DriverSalaryAlias.work_experience_over_months.desc())
    #         .limit(1)
    #         .subquery()  # Create a subquery
    #     )
    #
    #     # Main query to fetch drivers with the corresponding salary
    #     query = (
    #         select(
    #             DriverDB.id,
    #             DriverDB.first_name,
    #             DriverDB.last_name,
    #             subquery.c.salary_rub.label("driver_salary"),
    #         )
    #         .outerjoin(subquery, subquery.c.id == DriverDB.id)  # Correctly join using the subquery
    #     )
    #
    #     # Execute the query in the async session
    #     result = await self.session.execute(query)
    #     drivers = result.unique().all()
    #     print(drivers)
    #     return [
    #         from_db_to_entity(driver, Driver)
    #         for driver in drivers
    #     ]

    async def get_salary(self, work_experience_months: int, driver_class: DriverClass) -> DriverSalary:
        q = select(DriverSalaryDB).where(
            DriverSalaryDB.work_experience_over_months <= work_experience_months
        ).where(
            DriverSalaryDB.driver_class_id == driver_class.id
        ).order_by(
            DriverSalaryDB.work_experience_over_months.desc()
        ).limit(1)
        result = await self.session.execute(q)
        driver_salary = result.unique().scalar()
        if driver_salary:
            return from_db_to_entity(driver_salary, DriverSalary)

    async def delete_driver(self, driver_id: int):
        q = delete(DriverDB).where(DriverDB.id == driver_id)
        await self.session.execute(q)
        await self.session.commit()

    async def get_driver_class_by_name(self, name: str) -> DriverClass | None:
        q = select(DriverClassDB).where(DriverClassDB.name == name)
        result = await self.session.execute(q)
        driver_class = result.unique().scalar()
        if driver_class:
            return from_db_to_entity(driver_class, DriverClass)

    async def add_driver_class(self, driver_class: DriverClass) -> DriverClass:
        driver_class_db = DriverClassDB(
            name=driver_class.name
        )
        self.session.add(driver_class_db)
        await self.session.commit()
        await self.session.refresh(driver_class_db)
        return from_db_to_entity(driver_class_db, DriverClass)

    async def get_driver_by_id(self, driver_id: int) -> Driver | None:
        q = select(DriverDB).where(DriverDB.id == driver_id)
        result = await self.session.execute(q)
        driver = result.unique().scalar()
        if driver:
            return from_driver_db_to_dm(driver)

    async def get_driver_class_by_id(self, driver_class_id: int) -> DriverClass | None:
        q = select(DriverClassDB).where(DriverClassDB.id == driver_class_id)
        result = await self.session.execute(q)
        driver_class = result.unique().scalar()
        if driver_class:
            return from_db_to_entity(driver_class, DriverClass)

    async def get_driver_classes(self) -> list[DriverClass]:
        q = select(DriverClassDB)
        result = await self.session.execute(q)
        driver_classes = result.unique().scalars().all()
        return [from_db_to_entity(driver_class, DriverClass) for driver_class in driver_classes]

    async def delete_driver_class(self, driver_class_id: int):
        q = delete(DriverClassDB).where(DriverClassDB.id == driver_class_id)
        await self.session.execute(q)
        await self.session.commit()

    async def get_driver_count_by_class(self, driver_class_id: int) -> int:
        q = select(func.count(DriverDB.id)).where(DriverDB.driver_class_id == driver_class_id)
        result = await self.session.execute(q)
        return result.scalar_one()
