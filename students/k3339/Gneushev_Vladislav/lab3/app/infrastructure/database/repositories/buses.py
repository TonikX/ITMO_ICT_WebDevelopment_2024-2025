import logging

from sqlalchemy import select, delete

from app.domain.entities.buses import Bus, BusType
from app.infrastructure.database.converters.buses import from_bus_type_dm_to_db, from_bus_type_db_to_dm, \
    from_bus_db_to_dm, from_bus_dm_to_db
from app.infrastructure.database.converters.universal import from_db_to_entity, from_entity_to_db
from app.infrastructure.database.models import BusDB, BusTypeDB
from app.infrastructure.database.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class BusRepository(BaseRepository):
    async def get_bus_by_id(self, bus_id: int) -> Bus | None:
        q = select(BusDB).where(BusDB.id == bus_id)
        result = await self.session.execute(q)
        bus = result.scalars().first()
        if bus:
            return from_bus_db_to_dm(bus)

    async def get_buses(self) -> list[Bus]:
        q = select(BusDB)
        result = await self.session.execute(q)
        buses = result.scalars().all()
        return [
            from_bus_db_to_dm(bus)
            for bus in buses
        ]

    async def add_bus(self, bus: Bus) -> Bus:
        bus_db = from_bus_dm_to_db(bus)
        self.session.add(bus_db)
        await self.session.commit()
        await self.session.refresh(bus_db)
        return from_bus_db_to_dm(bus_db)

    async def add_bus_type(self, bus_type: BusType) -> BusType:
        bus_type_db = from_bus_type_dm_to_db(bus_type)
        self.session.add(bus_type_db)
        await self.session.commit()
        await self.session.refresh(bus_type_db)
        return from_bus_type_db_to_dm(bus_type_db)

    async def get_bus_type_by_name(self, name: str) -> BusType | None:
        q = select(BusTypeDB).where(BusTypeDB.name == name)
        result = await self.session.execute(q)
        bus_type = result.scalars().first()
        if bus_type:
            return from_bus_type_db_to_dm(bus_type)

    async def get_bus_types(self) -> list[BusType]:
        q = select(BusTypeDB)
        result = await self.session.execute(q)
        bus_types = result.scalars().all()
        return [from_bus_type_db_to_dm(bus_type) for bus_type in bus_types]

    async def delete_bus_type(self, bus_type_id: int) -> None:
        q = delete(BusTypeDB).where(BusTypeDB.id == bus_type_id)
        await self.session.execute(q)
        await self.session.commit()

    async def get_bus_type_by_id(self, bus_type_id: int) -> BusType | None:
        q = select(BusTypeDB).where(BusTypeDB.id == bus_type_id)
        result = await self.session.execute(q)
        bus_type = result.scalars().first()
        if bus_type:
            return from_bus_type_db_to_dm(bus_type)

    async def delete_bus(self, bus_id: int) -> None:
        q = delete(BusDB).where(BusDB.id == bus_id)
        await self.session.execute(q)
        await self.session.commit()
