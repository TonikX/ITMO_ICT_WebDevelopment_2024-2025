from app.domain.entities.buses import Bus, BusType
from app.infrastructure.database.repositories.buses import BusRepository
from app.services.exceptions import EntityNotFound


class BusService:
    def __init__(self, bus_repo: BusRepository):
        self.bus_repo = bus_repo

    async def get_buses(self) -> list[Bus]:
        return await self.bus_repo.get_buses()

    async def add_bus_type(self, bus_type: BusType) -> BusType:
        return await self.bus_repo.add_bus_type(bus_type)

    async def get_bus_types(self) -> list[BusType]:
        return await self.bus_repo.get_bus_types()

    async def delete_bus_type(self, bus_type_id: int) -> None:
        bus_type = await self.bus_repo.get_bus_type_by_id(bus_type_id)
        if not bus_type:
            raise EntityNotFound(
                entity=BusType,
                field_name='id',
                value=bus_type_id
            )
        await self.bus_repo.delete_bus_type(bus_type_id)

    async def delete_bus(self, bus_id: int) -> None:
        bus = await self.bus_repo.get_bus_by_id(bus_id)
        if not bus:
            raise EntityNotFound(
                entity=Bus,
                field_name='id',
                value=bus_id
            )
        await self.bus_repo.delete_bus(bus_id)
        
    async def add_bus(
            self,
            state_number: str,
            bus_type_id: int
    ) -> Bus:
        bus_type = await self.bus_repo.get_bus_type_by_id(bus_type_id)
        if not bus_type:
            raise EntityNotFound(
                entity=BusType,
                field_name='id',
                value=bus_type_id
            )
        return await self.bus_repo.add_bus(
            Bus(
                id=None,
                state_number=state_number,
                bus_type=bus_type
            )
        )
